import os
from typing import List, Tuple, Dict

# Interface and Models
from ragformance.generators.data_generator_interface import (
    RAGformanceGeneratorInterface,
)
from ragformance.generators.alpha.config import AlphaGeneratorConfig
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel

from .main import (
    summarize,
    _split_into_sentences,
    _chunk_document_fast,
    generate_questions,
    parquet_to_jsonl,
)

# TODO uniformize markdown conversion across generators
try:
    from forcolate import convert_folders_to_markdown
except ImportError:

    def convert_folders_to_markdown(*args, **kwargs):
        raise ImportError(
            "'forcolate' module is not installed. "
            "Please install ragformance with the [all] option:\n"
            "    pip install ragformance[all]"
        )


class AlphaGenerator(RAGformanceGeneratorInterface):
    def run(
        self, config: AlphaGeneratorConfig = None, config_dict: Dict = None
    ) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
        """
        Generates corpus and queries using the Alpha generation method.

        Args:
            config: A dictionary containing configuration parameters:
                - data_path (str): Path to the folder containing the data.
                - output_path (str): Path to save the generated files.
                - temporary_folder (str, optional): Path for temporary files. Defaults to "converted_data".
                - llm_api_key (str): API key for the LLM.
                - llm_base_url (str): Base URL for the LLM API.
                - llm_model_name (str): Name of the LLM model.
        """

        if config is None:
            config_model = AlphaGeneratorConfig(**config_dict)
        else:
            config_model = config

        folder_path = config_model.data_path
        output_path = config_model.output_path
        temporary_folder = config_model.temporary_folder
        api_key = config_model.llm_api_key
        api_base_url = config_model.llm_base_url
        api_model = config_model.llm_model_name

        # Ensure output and temporary folders exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        if not os.path.exists(temporary_folder):
            os.makedirs(temporary_folder)

        # Convert the folders to markdown files
        # Assuming convert_folders_to_markdown is correctly imported or defined
        convert_folders_to_markdown("", folder_path, temporary_folder)

        for file_name in os.listdir(temporary_folder):
            if not file_name.endswith(".md"):
                continue

            file_path = os.path.join(temporary_folder, file_name)
            with open(file_path, encoding="utf-8") as f:
                print(f"Reading file {file_name}")
                document = f.read()

                # Assuming summarize is correctly imported or defined
                doc_summary = summarize(document, api_key, api_base_url, api_model)

                sentences = _split_into_sentences(document)

                # Using file_name without .md as doc_id
                doc_id = file_name.replace(".md", "")
                chunks = _chunk_document_fast(
                    sentences, 512, doc_id
                )  # Max tokens is hardcoded, consider making it configurable

                print(f"Generating questions for {file_name}")

                # generate_questions writes parquet files to output_path
                # TODO write directly in jsonl, ensure all generator write similar files
                generate_questions(
                    chunks,
                    file_name,  # Pass file_name (e.g. "doc.md")
                    doc_summary,
                    output_path,  # output_path for parquet files
                    api_key,
                    api_base_url,
                    api_model,
                )

        # TODO Clean up the temporary folder (optional, consider making it configurable)

        # Convert generated parquet files to JSONL and return
        corpus, queries = parquet_to_jsonl(output_path)

        return corpus, queries
