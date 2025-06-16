import os
from pathlib import Path
from typing import List, Tuple, Dict, Any

from ragformance.generators.data_generator_interface import RAGformanceGeneratorInterface
from ragformance.generators.ragas.config import RagasGeneratorConfig
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel

# Core logic from the existing ragas.py script
from .ragas import run_ragas_core # Updated to match the actual function name

# Setup logic from ragas_setup.py
from .ragas_setup import (
    get_configured_llm, 
    get_configured_embeddings,
    get_configured_query_distribution, # New function to handle question distribution
    get_ragas_testset_generator 
)

class RagasGenerator(RAGformanceGeneratorInterface):
    def run(self, config: Dict) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
        """
        Generates corpus and queries using the RAGAS testset generation method.

        Args:
            config: A dictionary containing configuration parameters:
                - data_path (str): Path to directory with source .txt or .md files.
                - output_path (str): Directory to save generated files.
                - llm_config (dict): Configuration for the generator LLM. 
                                     Example: {"name": "gen_llm", "provider": "openai", "model": "gpt-3.5-turbo", 
                                                "api_key_env": "OPENAI_API_KEY", "params": {"temperature": 0.7}}
                - embedding_config (dict): Configuration for the embedding model.
                                           Example: {"name": "emb", "provider": "openai", "model": "text-embedding-ada-002", 
                                                      "api_key_env": "OPENAI_API_KEY", "params": {}}
                - critique_llm_config (dict, optional): Configuration for the critique LLM. If not provided, generator_llm is used.
                - n_questions (int, optional): Number of QA pairs to generate. Defaults to 10.
                - save_ragas_kg (bool, optional): Whether to save the RAGAS knowledge graph. Defaults to True.
                - question_distribution (list[dict], optional): Distribution for question types.
                                           (e.g., [{"type": "singlehop-specific", "ratio": 0.5}])
        """
        config_model = RagasGeneratorConfig(**config)

        datapath = config_model.data_path
        output_path_str = config_model.output_path
        output_dir = Path(output_path_str)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 1. Setup RAGAS components using ragas_setup.py logic
        generator_llm = get_configured_llm(config_model.llm_config.model_dump())
        
        critique_llm = generator_llm 
        if config_model.critique_llm_config:
             critique_llm = get_configured_llm(config_model.critique_llm_config.model_dump())

        generator_embeddings = get_configured_embeddings(config_model.embedding_config.model_dump())
        
        testset_generator = get_ragas_testset_generator(
            llm=generator_llm,
            embeddings=generator_embeddings,
            critique_llm=critique_llm
        )

        # Prepare query distribution if specified
        ragas_query_distribution = None
        if config_model.question_distribution:
            ragas_query_distribution = get_configured_query_distribution(
                distribution_config_list=[item.model_dump() for item in config_model.question_distribution],
                llm=generator_llm # Synthesizers need the LLM
            )

        # 2. Prepare arguments for the core run function
        n_questions = config_model.n_questions
        save_ragas_kg = config_model.save_ragas_kg
        
        # 3. Call the core RAGAS generation logic
        # run_ragas_core is expected to return Tuple[List[Dict], List[Dict]]
        # and handle its own file saving to output_path_str.
        raw_corpus, raw_queries = run_ragas_core(
            datapath=datapath,
            output_path=output_path_str,
            ragas_testset_generator=testset_generator,
            n_questions=n_questions,
            query_distribution=ragas_query_distribution, # Pass the processed distribution
            save_ragas_kg=save_ragas_kg
        )
        
        # Convert raw dicts to Pydantic models
        corpus_models: List[DocModel] = [DocModel(**doc) for doc in raw_corpus]
        queries_models: List[AnnotatedQueryModel] = []
        for query_dict in raw_queries:
            queries_models.append(AnnotatedQueryModel(
                _id=query_dict["_id"],
                query_text=query_dict["text"], # In ragas.py, it's "text" not "query_text"
                relevant_document_ids=query_dict.get("references", []),
                ref_answer=query_dict.get("ref_answer", ""),
                metadata=query_dict.get("metadata", {})
            ))
            
        print(f"[RagasGenerator.run] RAGAS generation complete. Corpus and queries saved in {output_path_str}")
        return corpus_models, queries_models
