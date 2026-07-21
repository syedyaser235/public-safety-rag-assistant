from pathlib import Path
import fitz
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = PROJECT_ROOT / "data" / "Safety SOGs.pdf"
OUTPUT_PDF = PROJECT_ROOT / "data" / "fire_operations.pdf"

START_PAGE = 42 # Idenitified as the beginning of the fire operations section in the PDF
END_PAGE = 55 # Idenitified as the end of the fire operations section in the PDF


def extract_fire_sop_pages():
    """Extract pages 42–55 into a smaller PDF."""

    source_pdf = fitz.open(PDF_PATH)
    output_pdf = fitz.open()

    for page_number in range(START_PAGE - 1, END_PAGE):
        output_pdf.insert_pdf(
            source_pdf,
            from_page=page_number,
            to_page=page_number
        )

    output_pdf.save(OUTPUT_PDF)

    output_pdf.close()
    source_pdf.close()

    print("Filtered PDF created.")


def extract_text():
    """Extract raw text from the filtered PDF."""

    pdf = fitz.open(OUTPUT_PDF)

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()
    

    return text

def clean_text(text):
    """
    Cleans extracted SOP text while preserving semantic structure.
    """

    # # Remove repeated page headers
    # text = re.sub(r"_+\s*Fire Department SOG.?s", "", text)
    # # Remove lines like:
    # # # SOG 7.2 Vehicle Fires
    # # text = re.sub(r"SOG\s+\d+\.\d+.*", "", text)
    # # Remove adoption date
    # text = re.sub(r"Adopted\s+\d{2}/\d{2}/\d{4}", "", text)

    lines = text.splitlines()
    cleaned_lines = []
    seen_sogs = set()
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Remove page banner
        if "Fire Department SOG" in line:
            i += 1
            continue

        # Handle SOG headers
        match = re.match(r"SOG\s+(\d+\.\d+)\s+(.+)", line)
        if match:
            sog_id = match.group(1) 
            if sog_id in seen_sogs:
                # Skip duplicate page header
                i += 1
                # Skip Adopted line if present
                while i < len(lines) and (
                    "Adopted" in lines[i]
                    or lines[i].strip() == ""
                ):
                    i += 1
                continue

            seen_sogs.add(sog_id)
            cleaned_lines.append(line)
            i += 1
            continue

        # Remove Adopted lines
        if line.startswith("Adopted"):
            i += 1
            continue

        # Normalize bullet characters
        line = line.replace("", "-")
        # Remove tabs
        line = line.replace("\t", " ")
        # Collapse multiple spaces
        line = re.sub(r"[ ]{2,}", " ", line)
        cleaned_lines.append(line)
        i += 1
    text = "\n".join(cleaned_lines)

    # Normalize bullets
    text = text.replace("", "-")

    # Join bullets with their content
    # -
    # Recognition...
    # -->
    # - Recognition...

    text = re.sub(r"-\s*\n\s*", "- ", text)
    # Join orphan list markers
    # I.
    # Text...
    # -->
    # I. Text...
    text = re.sub(
        r"\b([A-Za-z]|\d+)\.\s*\n\s*",
        r"\1. ",
        text
    )

    # Remove multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Replace tabs
    text = text.replace("\t", " ")

    # Remove whitespace-only lines
    text = re.sub(r"\n[ \t]+\n", "\n\n", text)

    # Collapse 3+ blank lines into one blank line
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def split_into_sops(cleaned_text: str, output_dir: Path) -> None:
    """
    Split cleaned SOP text into one text file per SOP.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    # Split while retaining each SOG header
    sop_blocks = re.split(r'(?=^SOG\s+\d+\.\d+\s+)', cleaned_text, flags=re.MULTILINE)

    # Remove any empty blocks
    sop_blocks = [block.strip() for block in sop_blocks if block.strip()]

    for block in sop_blocks:

        header = block.split("\n", 1)[0]

        match = re.match(r"SOG\s+(\d+\.\d+)\s+(.+)", header)

        if not match:
            print(f"Skipping malformed block:\n{header}")
            continue

        sog_id = match.group(1)
        title = match.group(2).strip()

        filename = (
            title.lower()
                 .replace(" ", "_")
                 .replace("/", "_")
                 .replace("-", "_")
        )

        output_path = output_dir / f"{filename}.txt"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(block)

        print(f"Saved SOG {sog_id} -> {output_path.name}")

    print(f"\nSuccessfully created {len(sop_blocks)} SOP files.")

if __name__ == "__main__":

    # # Step 1 Creating a smaller PDF (Knowledge Base) from the Large PDF
    # Only run this once if the fire operations PDF doesn't exist

    # extract_fire_sop_pages()
   
    # # Step 2 Extracting raw text from the filtered PDF and saving it to raw_fire_sop_text.txt
    raw_text = extract_text()
    # saving text as raw_fire_sop_text.txt
    with open(PROJECT_ROOT / "data" / "raw_fire_sop_text.txt", "w", encoding="utf-8") as f:
        f.write(raw_text)
    print("Raw text extracted and saved to raw_text.txt.")
    # print(raw_text[:2000])

    # Step 3 Cleaning the extracted text and saving it to cleaned_fire_sop_text.txt
    cleaned_text = clean_text(raw_text)
    #  saving text as cleaned_fire_sop_text.txt
    with open(PROJECT_ROOT / "data" / "cleaned_fire_sop_text.txt", "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    # print(cleaned_text[:2000])

    # Step 4 Splitting the cleaned text into individual SOPs and saving them to the sops directory
    processed_dir = PROJECT_ROOT / "data" / "processed"
    split_into_sops(cleaned_text, processed_dir)
