from pathlib import Path
from typing import List, Tuple

from ragformance.generators.data_generator_interface import (
    RAGformanceGeneratorInterface,
)
from ragformance.generators.structural_generator.config import (
    StructuralGeneratorConfig,
)
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel

from .main import run as run_structural_core_logic


class StructuralGenerator(RAGformanceGeneratorInterface):
    def run(
        self, config: StructuralGeneratorConfig
    ) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
        """
        Generates corpus and queries based on document structure.

        Args:
            config: A dictionary containing configuration parameters:
                - data_folder_path (str): Path to the folder containing source documents.
                                          (Original 'folder_path')
                - data_file_name (str): Name of the data file within data_folder_path.
                                        (Original 'file_name')
                - output_path (str): Path to save the generated files.
        """
        folder_path_str = config.data_path

        file_name_str = config.data_file_name
        output_path_str = config.output_path

        output_dir = Path(output_path_str)
        output_dir.mkdir(parents=True, exist_ok=True)

        # TODO convert from PDF

        # Call the core logic. It returns (List[Dict_for_DocModel], List[Dict_for_QueryModel])
        # It also handles its own file creation (corpus.jsonl, queries.jsonl) within output_path_str.
        raw_corpus_list, raw_queries_list = run_structural_core_logic(
            folder_path_str,
            file_name_str,
            output_path_str,  # Pass output_path for the core logic to save its files
        )

        # Convert List[Dict] to List[DocModel]
        corpus_models: List[DocModel] = []
        for doc_dict in raw_corpus_list:
            corpus_models.append(DocModel(**doc_dict))

        # Convert List[Dict_for_QueryModel] to List[AnnotatedQueryModel]
        # The dictionaries from structural_generator.main.format_query have:
        # "_id": str
        # "text": str
        # "references": list[{"corpus_id": str, "score": int}] -> This needs to match AnnotatedQueryModel
        # "ref_answer": str
        # "metadata": dict
        annotated_queries: List[AnnotatedQueryModel] = []
        for query_dict in raw_queries_list:
            # The 'references' field from format_query is already in the correct structure
            # List[Dict[str, Any]] for relevant_document_ids.

            annotated_queries.append(
                AnnotatedQueryModel(
                    _id=query_dict["_id"],
                    query_text=query_dict["text"],
                    relevant_document_ids=query_dict.get(
                        "references", []
                    ),  # format_query uses "references"
                    ref_answer=query_dict.get("ref_answer", ""),
                    metadata=query_dict.get("metadata", {}),
                )
            )

        print(
            f"[StructuralGenerator.run] Structural generation complete. Files saved in {output_path_str}"
        )

        return corpus_models, annotated_queries
