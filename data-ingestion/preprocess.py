from pathlib import Path
import fitz

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = PROJECT_ROOT / "data" / "Safety SOGs.pdf"
OUTPUT_PDF = PROJECT_ROOT / "data" / "fire_operations.pdf"

START_PAGE = 42
END_PAGE = 55


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


if __name__ == "__main__":

    # # Only run this once if the PDF doesn't exist
    # extract_fire_sop_pages()

    raw_text = extract_text()

    print(raw_text[:3000])

    