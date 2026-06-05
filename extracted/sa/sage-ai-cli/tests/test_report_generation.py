import os
import pytest
from pathlib import Path

def test_report_pdf_exists():
    """Verify that report.pdf is created and is not empty."""
    pdf_path = Path("report.pdf")
    assert pdf_path.exists(), "report.pdf was not created"
    assert pdf_path.stat().st_size > 0, "report.pdf is empty"

def test_report_pdf_content():
    """Verify that the PDF contains the expected text 'Quarterly results'."""
    pdf_path = Path("report.pdf")
    
    # Since PDF is a binary format, we read it as bytes and check for the string
    # This is a basic check; for complex PDFs, a library like PyPDF2 would be used.
    content = pdf_path.read_bytes()
    assert b"Quarterly results" in content, "The text 'Quarterly results' was not found in the PDF"

if __name__ == "__main__":
    # Allow running the test directly via python3
    pytest.main([__file__])