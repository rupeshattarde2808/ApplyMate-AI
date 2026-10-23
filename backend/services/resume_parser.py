from pathlib import Path

import pymupdf


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract readable text from a PDF resume."""

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {pdf_path}")

    if not path.is_file():
        raise ValueError("The provided path is not a file.")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    try:
        with pymupdf.open(path) as document:
            if document.is_encrypted:
                raise ValueError(
                    "Password-protected PDFs are not supported."
                )

            text = "\n".join(
                page.get_text("text") for page in document
            ).strip()

    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"Unable to read PDF: {exc}") from exc

    if not text:
        raise ValueError(
            "No readable text found. The PDF may require OCR."
        )

    return text