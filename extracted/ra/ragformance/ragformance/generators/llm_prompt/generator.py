from pathlib import Path
from typing import List, Tuple, Dict


from ragformance.generators.data_generator_interface import (
    RAGformanceGeneratorInterface,
)
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel

from .corpus_builder import CorpusBuilder

# Corrected import paths for file_processors assuming 'generator.py' is at the same level as 'corpus_builder.py'
# and 'file_processors' is a subdirectory at that level.
from .file_processors.pdf_processor import PdfProcessor
from .file_processors.md_processor import MarkdownProcessor

from .generate_synthetic_queries import generate_queries_from_corpus
from .generate_synthetic_answers import generate_answers_for_queries

from .config import LLMPromptGeneratorConfig


# TODO : merge llm prompt with based llm and summary with alpha generator, allowing variation on prompts; commonalize parts with mic generator
class LLMPromptGenerator(RAGformanceGeneratorInterface):
    def run(
        self, config: LLMPromptGeneratorConfig = None, config_dict: Dict = None
    ) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
        """
        Generates corpus, queries, and answers using LLM prompts.

        Args:
            config: A dictionary containing configuration parameters:
                - data_path (str): Path to the folder containing source documents (PDFs, MDs).
                - output_path (str): Path to save the generated files (corpus.jsonl, queries.jsonl).
                - llm_api_key (str): API key for the LLM.
                - llm_base_url (str): Base URL for the LLM API.
                - llm_model_name (str): Name of the LLM model for generation tasks.
                - query_gen_prompt_template (str, optional): Path to a custom prompt template for query generation.
                - answer_gen_prompt_template (str, optional): Path to a custom prompt template for answer generation.
                - max_questions_per_doc (int, optional): Max questions to generate per document. Defaults to 5.
                - process_pdfs (bool, optional): Whether to process PDF files. Defaults to True.
                - process_markdown (bool, optional): Whether to process Markdown files. Defaults to True.
        """

        if config is None:
            config_model = LLMPromptGeneratorConfig(**config_dict)
        else:
            config_model = config

        docs_folder = Path(config_model.data_path)
        output_dir = Path(config_model.output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        llm_api_key = config_model.llm_api_key
        llm_base_url = config_model.llm_base_url
        llm_model_name = config_model.llm_model_name

        # Corpus Generation
        corpus_jsonl_path = output_dir / "corpus.jsonl"

        processors = []
        if config_model.process_pdfs:
            processors.append(PdfProcessor())
        if config_model.process_markdown:
            processors.append(MarkdownProcessor())

        if not processors:
            print("Warning: No file processors enabled. Corpus will be empty.")

        corpus_builder = CorpusBuilder(
            output_file=str(corpus_jsonl_path), processors=processors
        )  # CorpusBuilder expects string path

        # generate_corpus expects a Path object
        corpus: List[DocModel] = corpus_builder.generate_corpus(docs_folder)

        if not corpus:
            print(
                "Corpus generation resulted in an empty list. Skipping query and answer generation."
            )
            return [], []

        # Query Generation
        # generate_queries_from_corpus expects: corpus (List[DocModel]), model_name, api_key, base_url,
        # output_file_path (Path), prompt_template_path=None, max_questions_per_doc=5
        # It writes to a file and returns List[Dict] (raw_queries_list)
        queries_temp_jsonl_path = (
            output_dir / "temp_queries.jsonl"
        )  # Temporary path for raw queries

        raw_queries_list = generate_queries_from_corpus(
            corpus=corpus,
            model_name=llm_model_name,
            api_key=llm_api_key,
            base_url=llm_base_url,
            output_file_path=queries_temp_jsonl_path,
            prompt_template_path=config_model.query_gen_prompt_template,
            max_questions_per_doc=config_model.max_questions_per_doc,
        )

        if not raw_queries_list:
            print(
                "Query generation resulted in an empty list. Skipping answer generation."
            )
            # Return corpus and empty queries list
            # Write empty queries.jsonl for consistency if expected by downstream tasks
            final_queries_jsonl_path = output_dir / "queries.jsonl"
            # with open(final_queries_jsonl_path, "w", encoding="utf-8") as fq:
            #    pass  # Create empty file
            return corpus, []

        # Answer Generation
        # generate_answers_for_queries expects:
        # queries (List[Dict]), corpus (List[DocModel]), model_name, api_key, base_url,
        # output_file_path (Path), prompt_template_path=None
        # It updates the query dicts with an 'answer' field and writes to output_file_path.

        final_queries_jsonl_path = (
            output_dir / "queries.jsonl"
        )  # Final path for queries with answers

        answered_queries_list_of_dicts = generate_answers_for_queries(
            queries=raw_queries_list,  # Pass list of dicts with 'question' and 'doc_id'
            corpus=corpus,
            model_name=llm_model_name,
            api_key=llm_api_key,
            base_url=llm_base_url,
            output_file_path=final_queries_jsonl_path,
            prompt_template_path=config_model.answer_gen_prompt_template,
        )

        # Convert the final list of dicts (with answers) to List[AnnotatedQueryModel]
        final_queries: List[AnnotatedQueryModel] = []
        for answered_query_dict in answered_queries_list_of_dicts:
            # Ensure all necessary fields are present, providing defaults if some are missing
            query_id = answered_query_dict.get(
                "query_id", f"generated_query_{len(final_queries)}"
            )
            question_text = answered_query_dict.get("question", "")
            doc_id = answered_query_dict.get("doc_id")
            answer_text = answered_query_dict.get(
                "answer", ""
            )  # Default to empty if no answer generated

            relevant_docs = []
            if doc_id:  # Only add if doc_id is present
                relevant_docs.append({"corpus_id": doc_id, "score": 1.0})

            final_queries.append(
                AnnotatedQueryModel(
                    _id=query_id,
                    query_text=question_text,
                    relevant_document_ids=relevant_docs,
                    ref_answer=answer_text,
                    metadata={"doc_id": doc_id} if doc_id else {},
                )
            )

        return corpus, final_queries
