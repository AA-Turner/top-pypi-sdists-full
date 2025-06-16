import os
from typing import List, Tuple, Dict

from ragformance.generators.data_generator_interface import (
    RAGformanceGeneratorInterface,
)
from ragformance.generators.error_code.config import ErrorCodeGeneratorConfig
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel

from .parsing_engine import (
    find_pages,
    merge_pages,
    extract_keywords,
)
from .question_generation import (
    generate_easy_question,
    question_variation,
    add_augmented_question,
)


class ErrorCodeGenerator(RAGformanceGeneratorInterface):
    def run(self, config: Dict) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
        """
        Generates corpus and queries for error codes from manuals.

        Args:
            config: A dictionary containing configuration parameters:
                - data_path (str): Path to the folder containing the processed manual (e.g., page_X.md files and output.md).
                - output_path (str): Path to save the output files (corpus.jsonl, queries.jsonl).
                - corpus_id_prefix (str): Prefix for corpus document IDs.
                - document_title (str): Title of the document being processed.
                - llm_api_key (str): API key for the LLM.
                - llm_base_url (str): Base URL for the LLM API (used as API_URL).
                - llm_model_name (str): Name of the LLM model (used as API_MODEL).
                - error_keywords (str, optional): Keywords to find error pages. Defaults to "error, information, or alarm codes (e.g., E09)".
                - max_token_context (int, optional): Max token context for LLM calls. Defaults to 64000.
                - question_tags (list[str], optional): Tags for question metadata. Defaults to [].
                - question_category (str, optional): Category for question metadata. Defaults to "error code".

        """
        config_model = ErrorCodeGeneratorConfig(**config)

        folder_path = config_model.data_path
        output_path = config_model.output_path
        prefix_id = config_model.corpus_id_prefix
        title = config_model.document_title
        api_key = config_model.llm_api_key
        api_url = config_model.llm_base_url
        api_model = config_model.llm_model_name

        error_keywords = config_model.error_keywords
        max_token_context = config_model.max_token_context
        question_tags = config_model.question_tags
        question_category = config_model.question_category

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        manual_file_path = os.path.join(folder_path, "output.md")
        if not os.path.exists(manual_file_path):
            raise FileNotFoundError(
                f"Expected 'output.md' not found in data_path: {folder_path}"
            )

        with open(manual_file_path, encoding="utf-8") as file:
            manual_text = file.read()

        page_numbers = find_pages(
            keyword=error_keywords,
            document=manual_text,
            max_token_context=max_token_context,
            API_KEY=api_key,
            API_URL=api_url,
            API_MODEL=api_model,
        )

        if not page_numbers or len(page_numbers) == 0:
            print(
                "No relevant page numbers found for error codes. Skipping generation."
            )
            return [], []

        # merge_pages creates a temporary merged document string AND initial corpus list
        # The folder_path here is crucial: it expects page_X.md files to be in this folder.
        merged_pages_text, initial_corpus_dicts = merge_pages(
            page_numbers, folder_path, prefix_id, title
        )

        extracted_error_data = extract_keywords(
            keyword=error_keywords,  # Uses the same keywords as find_pages
            document=merged_pages_text,
            API_KEY=api_key,
            API_URL=api_url,
            API_MODEL=api_model,
        )

        if not extracted_error_data:
            print("No error keywords extracted. Skipping question generation.")
            return (
                [],
                [],
            )  # Or return initial_corpus_dicts as DocModels if that's desired

        # Generate initial questions
        # generate_easy_question returns: queries_list, query_augmentation_list
        easy_queries_dicts, query_augmentation_list = generate_easy_question(
            tabular_data=extracted_error_data,
            category=question_category,
            tags=question_tags,
            prefix_id=prefix_id,
        )

        # TODO Placeholder for medium questions

        augmented_question_variations = question_variation(
            question=query_augmentation_list,  # This expects a list of dicts like [{"_id": ID, "query_text": TEXT}, ...]
            API_KEY=api_key,
            API_URL=api_url,
            API_MODEL=api_model,
        )

        final_queries_dicts = add_augmented_question(
            easy_queries_dicts, augmented_question_variations
        )

        # The corpus should be based on all unique pages found and processed.
        # The `initial_corpus_dicts` from the first `merge_pages` call is based on `page_numbers`.
        final_corpus_docs: List[DocModel] = [
            DocModel(**doc) for doc in initial_corpus_dicts
        ]

        final_annotated_queries: List[AnnotatedQueryModel] = []
        for query_dict in final_queries_dicts:
            # Ensure relevant_document_ids are dicts, not strings, if necessary.
            # The generate_easy_question already creates them as dicts.
            final_annotated_queries.append(
                AnnotatedQueryModel(
                    _id=query_dict["_id"],
                    query_text=query_dict["query_text"],
                    relevant_document_ids=query_dict.get("relevant_document_ids", []),
                    ref_answer=query_dict.get(
                        "ref_anwser", ""
                    ),  # Typo "ref_anwser" in original generate_easy_question
                    metadata=query_dict.get("metadata", {}),
                )
            )

        # Save to files
        corpus_jsonl_path = os.path.join(output_path, "corpus.jsonl")
        with open(corpus_jsonl_path, "w", encoding="utf-8") as f_corp:
            for doc_model_instance in final_corpus_docs:
                f_corp.write(doc_model_instance.model_dump_json() + "\n")

        queries_jsonl_path = os.path.join(output_path, "queries.jsonl")
        with open(queries_jsonl_path, "w", encoding="utf-8") as f_que:
            for query_model_instance in final_annotated_queries:
                f_que.write(query_model_instance.model_dump_json() + "\n")

        return final_corpus_docs, final_annotated_queries
