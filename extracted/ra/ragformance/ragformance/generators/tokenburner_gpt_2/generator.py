import json
from pathlib import Path
from typing import List, Tuple, Dict

from ragformance.generators.data_generator_interface import (
    RAGformanceGeneratorInterface,
)
from ragformance.generators.tokenburner_gpt_2.config import (
    TokenBurnerGPT2GeneratorConfig,
)
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel

from .main import main as run_gpt2_script_logic


class TokenBurnerGPT2Generator(RAGformanceGeneratorInterface):
    def run(self, config: Dict) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
        """
        Generates corpus and Q&A from PDFs using TokenBurner GPT-2 logic.

        Args:
            config: A dictionary containing configuration parameters:
                - pdf_path (str): Path to the source PDF file.
                - output_path (str): Directory to save generated files.
                - model_path (str, optional): Path to a local GPT-2 model (if applicable).
                - max_pages (int, optional): Max pages to process from PDF.
                - llm_api_key (str): API key for OpenAI (or compatible) API.
                - llm_base_url (str): Base URL for OpenAI (or compatible) API.
                - llm_model_name (str): Model name to use for OpenAI calls (e.g., OCR, Q&A).
        """
        config_model = TokenBurnerGPT2GeneratorConfig(**config)

        pdf_path_str = config_model.pdf_path
        output_dir_str = config_model.output_path

        Path(output_dir_str).mkdir(parents=True, exist_ok=True)

        script_args = {
            "pdf_path": pdf_path_str,
            "output_dir": output_dir_str,
            "model_path": config_model.model_path,
            "max_pages": config_model.max_pages,
            "api_key": config_model.llm_api_key,
            "base_url": config_model.llm_base_url,
            "model_name": config_model.llm_model_name,
        }

        # This call assumes run_gpt2_script_logic is refactored to accept
        # a dictionary of arguments, and that it saves
        # 'corpus.jsonl' and 'queries.jsonl' in the output_dir_str.
        run_gpt2_script_logic(script_args)

        # After run_gpt2_script_logic completes, load the generated files.
        corpus: List[DocModel] = []
        corpus_file = Path(output_dir_str) / "corpus.jsonl"
        if corpus_file.exists():
            with open(corpus_file, encoding="utf-8") as f:
                for line in f:
                    data = json.loads(line)
                    corpus.append(DocModel(**data))
        else:
            print(
                f"Warning: {corpus_file} not found after TokenBurner GPT-2 execution."
            )

        queries: List[AnnotatedQueryModel] = []
        queries_file = Path(output_dir_str) / "queries.jsonl"
        if queries_file.exists():
            with open(queries_file, encoding="utf-8") as f:
                for line in f:
                    data = json.loads(line)
                    # Handle potential variations in relevant_document_ids key
                    relevant_docs = []
                    if (
                        "relevant_doc_id" in data and data["relevant_doc_id"]
                    ):  # Single ID case
                        relevant_docs = [
                            {"corpus_id": str(data["relevant_doc_id"]), "score": 1.0}
                        ]
                    elif "relevant_document_ids" in data:  # List of dicts case
                        relevant_docs = data["relevant_document_ids"]

                    queries.append(
                        AnnotatedQueryModel(
                            _id=data.get("_id", f"query_gpt2_{len(queries)}"),
                            query_text=data.get(
                                "question", data.get("query_text", "")
                            ),  # Accept "question" or "query_text"
                            relevant_document_ids=relevant_docs,
                            ref_answer=data.get(
                                "answer", data.get("ref_answer", "")
                            ),  # Accept "answer" or "ref_answer"
                            metadata=data.get("metadata", {}),
                        )
                    )
        else:
            print(
                f"Warning: {queries_file} not found after TokenBurner GPT-2 execution."
            )

        print(
            f"[TokenBurnerGPT2Generator.run] TokenBurner GPT-2 processing complete. Files in {output_dir_str}"
        )
        return corpus, queries
