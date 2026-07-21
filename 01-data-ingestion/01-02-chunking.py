from pathlib import Path
import json
import re
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHUNKS_DIR = PROJECT_ROOT / "data" / "chunks"

def load_sop_files(processed_dir: Path) -> list[Path]:
    """
    Load all processed SOP text files.

    Args:
        processed_dir (Path): Path to the processed SOP directory.

    Returns:
        list[Path]: Sorted list of SOP text file paths.
    """

    return sorted(processed_dir.glob("*.txt"))

def read_sop(file_path: Path) -> str:
    """
    Read the contents of a single SOP text file.

    Args:
        file_path (Path): Path to the SOP text file.

    Returns:
        str: Contents of the SOP.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    

def extract_metadata(text: str) -> dict:
    """
    Extract the SOG ID and title from an SOP.

    Args:
        text (str): Full SOP text.

    Returns:
        dict: SOP metadata containing the SOG ID and title.
    """

    first_line = text.split("\n", 1)[0]

    match = re.match(r"SOG\s+(\d+\.\d+)\s+(.+)", first_line)

    if not match:
        raise ValueError("Invalid SOP format. Could not find SOG header.")

    return {
        "sog_id": match.group(1),
        "title": match.group(2).strip()
    }

def split_into_sections(text: str) -> list[dict]:
    """
    Split an SOP into logical sections.

    Args:
        text (str): Full SOP text.

    Returns:
        list[dict]: List of sections with heading and content.
    """

    # Remove the SOG header and repeated title
    lines = text.splitlines()

    body = "\n".join(lines[2:]).strip()

    body = body.replace(
    f"SOG {extract_metadata(text)['sog_id']} {extract_metadata(text)['title']}",
    "",
    1
    )

    body = body.replace(
        extract_metadata(text)["title"],
        "",
        1
    ).strip()

    # All section headings found in your SOPs
    pattern = (
        r"(?=^(Definitions|"
        r"Arrival on Scene|"
        r"Arrival On Scene|"
        r"Scene Safety|"
        r"Incident Actions|"
        r"Incidents with an Explosion- Incident Actions|"
        r"Incidents with No Explosion- Incident Actions|"
        r"Reports and Documentation|"
        r"Clean-Up)"
        r"$)"
    )

    parts = re.split(pattern, body, flags=re.MULTILINE)

    sections = []

    # re.split() returns:
    # [intro_text, heading1, content1, heading2, content2, ...]

    intro = parts[0].strip()

    if intro:
        sections.append({
            "section": "Introduction",
            "text": intro
        })

    for i in range(1, len(parts), 2):

        heading = parts[i].strip()
        content = parts[i + 1].strip()

        if content.startswith(heading):
            content = content[len(heading):].strip()

        sections.append({
            "section": heading,
            "text": content
        })

    return sections

def create_chunks(metadata: dict, sections: list[dict]) -> list[dict]:
    """
    Create chunk objects from SOP metadata and sections.

    Args:
        metadata (dict): SOP metadata.
        sections (list[dict]): Sections extracted from the SOP.

    Returns:
        list[dict]: List of chunk dictionaries.
    """

    chunks = []

    for index, section in enumerate(sections, start=1):

        chunk = {
            "chunk_id": f"{metadata['sog_id']}_{index}",
            "sog_id": metadata["sog_id"],
            "title": metadata["title"],
            "section": section["section"],
            "text": section["text"]
        }

        chunks.append(chunk)

    return chunks

def save_chunks(chunks: list[dict], output_path: Path) -> None:
    """
    Save all chunks to a JSON file.

    Args:
        chunks (list[dict]): List of chunk dictionaries.
        output_path (Path): Path to the output JSON file.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)

def main():
    processed_dir = PROJECT_ROOT / "data" / "processed"
    # Step 1 : Load all processed SOP text files
    files = load_sop_files(processed_dir)

    print(f"Found {len(files)} SOP files:\n")

    all_chunks = []

    for file in files:
        # Step 2 : Read the contents of each SOP file
        text = read_sop(file)
        # Step 3 : Extract metadata from the SOP text
        metadata = extract_metadata(text)
        # Step 4 : Split the SOP text into sections
        sections = split_into_sections(text)
        # Step 5 : Create chunks from the metadata and sections
        chunks = create_chunks(metadata, sections)
        all_chunks.extend(chunks) 
    # Step 6 : Save all chunks to a JSON file     
    output_file = CHUNKS_DIR / "fire_sop_chunks.json"

    save_chunks(all_chunks, output_file)

    print(f"\nCreated {len(all_chunks)} chunks.")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()