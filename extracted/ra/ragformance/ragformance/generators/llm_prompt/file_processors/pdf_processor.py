import fitz  # PyMuPDF
from pathlib import Path
from typing import List
from ragformance.generators.llm_prompt.file_processors.file_processor_interface import (
    FileProcessor,
)
from ragformance.models.corpus import DocModel


class PdfProcessor(FileProcessor):
    def can_process(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == ".pdf"

    def process(self, file_path: Path) -> List[DocModel]:
        documents = []
        name = file_path.stem
        try:
            doc = fitz.open(str(file_path))
            for page_num in range(len(doc)):
                text = doc.load_page(page_num).get_text().strip()
                documents.append(
                    DocModel(
                        _id=f"{name}-page={page_num + 1}",
                        title=name,
                        text=text,
                        metadata={"document_id": name, "page_number": page_num + 1},
                    )
                )
            doc.close()
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")
        return documents
