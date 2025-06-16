from pathlib import Path
from typing import List, Tuple, Dict

from ragformance.generators.data_generator_interface import (
    RAGformanceGeneratorInterface,
)
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel


from .TokenBurner import run_tokenburner_processing


class TokenBurnerGenerator(RAGformanceGeneratorInterface):
    def run(self, config: Dict) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
        """
        Generates corpus and Q&A pairs from a PDF using the TokenBurner logic.

        Args:
            config: A dictionary containing configuration parameters:
                - pdf_path (str): Path to the source PDF file.
                - categories_file_path (str): Path to the categories definition file.
                - user_queries (List[str]): List of user queries to process.
                - output_path (str): Directory to save generated files.
                - llm_model_name (str): LLM model for generation tasks.
                - llm_api_key (str): API key for the LLM.
                - llm_base_url (str): Base URL for LLM API.
        """
        pdf_file_path_str = config["pdf_path"]
        categories_file_path_str = config["categories_file_path"]
        user_queries_list = config["user_queries"]
        output_dir_str = config["output_path"]

        model_name = config["llm_model_name"]
        api_key = config["llm_api_key"]
        base_url = config["llm_base_url"]

        output_dir = Path(output_dir_str)
        output_dir.mkdir(parents=True, exist_ok=True)

        # This call assumes run_tokenburner_processing is refactored to:
        # 1. Accept parameters: pdf_file_path, categories_file_path, output_dir,
        #    model_name, api_key, base_url, user_queries.
        # 2. Return Tuple[List[Dict_for_DocModel], List[Dict_for_AQueryModel]]
        #    These dicts should be directly convertible to DocModel and AnnotatedQueryModel.
        #    The script itself will *not* write to jsonl files anymore; the generator will.

        raw_corpus_list, raw_queries_list = run_tokenburner_processing(
            pdf_file_path=pdf_file_path_str,
            categories_file_path=categories_file_path_str,
            # output_dir=output_dir_str, # output_dir is for generator to save, not the script
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            user_questions=user_queries_list,
        )

        # Convert raw dicts to Pydantic models
        corpus_models: List[DocModel] = []
        if raw_corpus_list:  # Ensure it's not None
            for doc_dict in raw_corpus_list:
                corpus_models.append(DocModel(**doc_dict))

        queries_models: List[AnnotatedQueryModel] = []
        if raw_queries_list:  # Ensure it's not None
            for query_dict in raw_queries_list:
                queries_models.append(AnnotatedQueryModel(**query_dict))

        # Save to files
        corpus_jsonl_path = output_dir / "corpus.jsonl"
        with open(corpus_jsonl_path, "w", encoding="utf-8") as f_corp:
            for doc_model_instance in corpus_models:
                f_corp.write(doc_model_instance.model_dump_json() + "\n")

        queries_jsonl_path = output_dir / "queries.jsonl"
        with open(queries_jsonl_path, "w", encoding="utf-8") as f_que:
            for query_model_instance in queries_models:
                f_que.write(query_model_instance.model_dump_json() + "\n")

        print(
            f"[TokenBurnerGenerator.run] TokenBurner processing complete. Files saved in {output_dir_str}"
        )
        return corpus_models, queries_models
