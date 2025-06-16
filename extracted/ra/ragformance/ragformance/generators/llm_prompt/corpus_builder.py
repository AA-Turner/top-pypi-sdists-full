import os
import json
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm
from ragformance.models.corpus import DocModel
from ragformance.generators.llm_prompt.file_processors.file_processor_interface import (
    FileProcessor,
)


class CorpusBuilder:
    def __init__(self, output_file: str, processors: List[FileProcessor]):
        self.output_file = output_file
        self.processors = processors
        self.documents: List[DocModel] = []

    def generate_corpus(self, docs_folder: Path, config: Dict = {}) -> List[DocModel]:
        if config is None:
            config = {}
        all_documents = []
        print(docs_folder)
        for file_path in tqdm(docs_folder.glob("*"), desc="Processing files"):
            for processor in self.processors:
                if processor.can_process(file_path):
                    documents = processor.process(file_path)
                    all_documents.extend(documents)
                    break
        self.documents = all_documents
        self._save_to_jsonl()
        return self.documents  # Return the generated documents

    def _save_to_jsonl(self):
        if not self.documents:
            print("No documents to save.")
            return

        output_dir = os.path.dirname(self.output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(self.output_file, "w", encoding="utf-8") as fout:
            for doc in self.documents:
                fout.write(json.dumps(doc.model_dump(), ensure_ascii=False) + "\n")
        print(f"Saved {len(self.documents)} documents to {self.output_file}")
