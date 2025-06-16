import re
from pathlib import Path
from typing import List
from ragformance.generators.llm_prompt.file_processors.file_processor_interface import (
    FileProcessor,
)
from ragformance.models.corpus import DocModel


class MarkdownProcessor(FileProcessor):
    def can_process(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == ".md"

    def process(self, file_path: Path) -> List[DocModel]:
        documents = []
        name = file_path.stem
        try:
            match = re.match(r".*page_(\\d+)", file_path.name)
            page_num = match.group(1) if match else "0"
            with file_path.open(encoding="utf-8") as f:
                text = f.read()
            documents.append(
                DocModel(
                    _id=f"{name}-page={page_num}",
                    title=name,
                    text=text,
                    metadata={"document_id": name, "page_number": int(page_num)},
                )
            )
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")
        return documents
