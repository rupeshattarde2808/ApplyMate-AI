import pymupdf
import pytest

from services.resume_parser import extract_text_from_pdf


def test_missing_pdf():
    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf("missing_resume.pdf")


def test_non_pdf_file(tmp_path):
    file_path = tmp_path / "resume.txt"
    file_path.write_text("Sample resume")

    with pytest.raises(ValueError):
        extract_text_from_pdf(str(file_path))


def test_empty_pdf(tmp_path):
    pdf_path = tmp_path / "empty.pdf"

    with pymupdf.open() as document:
        document.new_page()
        document.save(pdf_path)

    with pytest.raises(ValueError):
        extract_text_from_pdf(str(pdf_path))


def test_extract_pdf_text(tmp_path):
    pdf_path = tmp_path / "sample.pdf"

    with pymupdf.open() as document:
        page = document.new_page()
        page.insert_text(
            (72, 72),
            "Candidate: Rahul Sharma\nSkills: Python, SQL",
        )
        document.save(pdf_path)

    text = extract_text_from_pdf(str(pdf_path))

    assert "Rahul Sharma" in text
    assert "Python" in text
    assert "SQL" in text