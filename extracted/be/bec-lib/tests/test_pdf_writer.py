import os

from bec_lib.pdf_writer import PDFWriter


def test_pdf_writer():
    with PDFWriter("test_output.pdf") as file:
        file.write("Hello World")

    assert os.path.exists("test_output.pdf")

    os.remove("test_output.pdf")


def test_pdf_writer_with_title():
    with PDFWriter("test_output.pdf", title="title") as file:
        file.write("Hello World")

    assert os.path.exists("test_output.pdf")

    os.remove("test_output.pdf")
