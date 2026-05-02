
from docx import Document
import PyPDF2


class GraderPayloadReader:
    @staticmethod
    def read_docx(file_stream):
        doc = Document(file_stream)
        return '\n'.join([para.text for para in doc.paragraphs])

    @staticmethod
    def read_pdf(file_stream):
        reader = PyPDF2.PdfReader(file_stream)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

