"""
RAGformance End-to-End Runner

This module allows you to run the full pipeline for question generation, upload, evaluation, metrics computation, and visualization
for RAG datasets, either from the command line or as a Python library.
Each step is controlled by flags in the JSON configuration file.

CLI usage:
    ragformance --config config.json
"""

import os
import json
import logging
import argparse
from typing import List, Dict, Any
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel, AnswerModel
from pydantic import TypeAdapter, ValidationError

# Import RAG config models
from ragformance.rag.config import (
    NaiveRagConfig,
    OpenWebUIRagConfig,
    HaystackRagConfig,
    MultiEmbeddingLLMRagConfig,
)


# load config file
def load_config(config_path):
    with open(config_path) as f:
        config = json.load(f)
    return config


# set up logging
def setup_logging(log_path):
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.info("Logging setup complete.")


def run_question_generation(config: Dict[str, Any]):
    """
    Execute question generation according to the provided configuration.
    Selects the generator, builds the Pydantic config, and launches the generation.
    Returns (corpus, queries).
    """
    from ragformance.generators.alpha import AlphaGenerator, AlphaGeneratorConfig
    from ragformance.generators.aida import AidaGenerator, AidaGeneratorConfig
    from ragformance.generators.based_llm_and_summary import (
        BasedLLMSummaryGenerator,
        BasedLLMSummaryGeneratorConfig,
    )
    from ragformance.generators.error_code import (
        ErrorCodeGenerator,
        ErrorCodeGeneratorConfig,
    )
    from ragformance.generators.llm_prompt import (
        LLMPromptGenerator,
        LLMPromptGeneratorConfig,
    )
    from ragformance.generators.mic import MicGenerator, MicGeneratorConfig
    from ragformance.generators.ragas import RagasGenerator, RagasGeneratorConfig
    from ragformance.generators.structural_generator import (
        StructuralGenerator,
        StructuralGeneratorConfig,
    )
    from ragformance.generators.tokenburner import (
        TokenBurnerGenerator,
        TokenBurnerGeneratorConfig,
    )
    from ragformance.generators.tokenburner_gpt_2 import (
        TokenBurnerGPT2Generator,
        TokenBurnerGPT2GeneratorConfig,
    )

    generator = config.get("generation", {})
    generator_type = generator.get("type", None)
    data_path = generator.get("source", {}).get("path", None)
    output_path = generator.get("output", {}).get("path", None)
    llms = config.get("LLMs", None)
    default_api_key = llms[0].get("api_key", None) if llms else None
    default_model_name = llms[0].get("model", None) if llms else None
    default_base_url = llms[0].get("base_url", None) if llms else None

    generator_class_map = {
        "alpha": (AlphaGenerator, AlphaGeneratorConfig),
        "aida": (AidaGenerator, AidaGeneratorConfig),
        "based_llm_and_summary": (
            BasedLLMSummaryGenerator,
            BasedLLMSummaryGeneratorConfig,
        ),
        "error_code": (ErrorCodeGenerator, ErrorCodeGeneratorConfig),
        "llm_prompt": (LLMPromptGenerator, LLMPromptGeneratorConfig),
        "mic": (MicGenerator, MicGeneratorConfig),
        "ragas": (RagasGenerator, RagasGeneratorConfig),
        "structural_generator": (StructuralGenerator, StructuralGeneratorConfig),
        "tokenburner": (TokenBurnerGenerator, TokenBurnerGeneratorConfig),
        "tokenburner_gpt_2": (TokenBurnerGPT2Generator, TokenBurnerGPT2GeneratorConfig),
    }

    gen_run_config: Dict[str, Any] = {
        "data_path": data_path,
        "output_path": output_path,
        "llm_api_key": default_api_key,
        "llm_base_url": default_base_url,
        "llm_model_name": default_model_name,
    }
    if "params" in generator:
        gen_run_config.update(generator.get("params", {}))

    # Specifics for certain generators
    if generator_type == "aida":
        aida_specific_params = config.get("aida_generator_config", {})
        gen_run_config.update(aida_specific_params)
        if "seed_questions_path" not in gen_run_config:
            gen_run_config["seed_questions_path"] = os.path.join(
                data_path, "seed_questions.json"
            )
        if "data_dir" not in gen_run_config:
            gen_run_config["data_dir"] = data_path
        if "capella_xml_path" not in gen_run_config:
            gen_run_config["capella_xml_path"] = os.path.join(data_path, "data.capella")
        if llms and len(llms) > 1 and "entity_model_name" not in gen_run_config:
            gen_run_config["entity_model_name"] = llms[1].get(
                "model", default_model_name
            )
        else:
            gen_run_config.setdefault("entity_model_name", default_model_name)
        gen_run_config.setdefault("qa_model_name", default_model_name)
        embeddings_list = config.get("embeddings", [{}])
        if embeddings_list and "hf_embed_model" not in gen_run_config:
            gen_run_config["hf_embed_model"] = embeddings_list[0].get("model")

    elif generator_type == "ragas":
        ragas_specific_params = config.get("ragas_generator_config", {})
        gen_run_config.update(ragas_specific_params)
        if "llm_config" not in gen_run_config:
            gen_run_config["llm_config"] = llms[0] if llms else {}
        if "embedding_config" not in gen_run_config:
            gen_run_config["embedding_config"] = (
                config.get("embeddings", [{}])[0] if config.get("embeddings") else {}
            )
        critique_llm_index = ragas_specific_params.get("critique_llm_index")
        if (
            critique_llm_index is not None
            and llms
            and 0 <= critique_llm_index < len(llms)
        ):
            gen_run_config["critique_llm_config"] = llms[critique_llm_index]
        elif "critique_llm_config" not in gen_run_config:
            gen_run_config["critique_llm_config"] = gen_run_config["llm_config"]

    if generator_type == "tokenburner_gpt_2" and "pdf_path" not in gen_run_config:
        gen_run_config["pdf_path"] = data_path

    # Selection of generator and Pydantic config
    if generator_type in generator_class_map:
        GeneratorClass, GeneratorConfigClass = generator_class_map[generator_type]
        # Convert dict to Pydantic object if class exists
        if GeneratorConfigClass is not None:
            try:
                pydantic_config = GeneratorConfigClass(**gen_run_config)
                config_for_run = pydantic_config
            except Exception as e:
                logging.error(
                    f"Validation error in Pydantic config for {generator_type}: {e}"
                )
                raise
        else:
            config_for_run = gen_run_config
        generator_instance = GeneratorClass()
        print(f"[Generator] Running {generator_type} with config: {gen_run_config}")
        corpus, queries = generator_instance.run(config_for_run)
        logging.info(f"Data generation complete using {generator_type}.")
        return corpus, queries
    else:
        logging.error(f"Unknown or unsupported generator type: {generator_type}")
        raise ValueError(f"Unknown or unsupported generator type: {generator_type}")


def run_pipeline(config_path="config.json"):
    """
    Run the full or partial pipeline according to the steps enabled in the config.
    """
    config = load_config(config_path)

    log_path = config.get("log_path", "logs")
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    setup_logging(log_path + "/ragformance.log")

    maybe_enable_phoenix_tracing(config)

    steps = config.get("steps", {})

    corpus: List[DocModel] = []
    queries: List[AnnotatedQueryModel] = []
    answers: List[AnswerModel] = []
    metrics_data = []  # TODO define model for metrics data

    ta = TypeAdapter(List[DocModel])
    taq = TypeAdapter(List[AnnotatedQueryModel])

    # TODO : optionaly start a local LLM server, update config

    # Question generation
    if steps.get("generation", False):
        logging.info("[STEP] Question generation.")
        corpus, queries = run_question_generation(config)

    # Upload to HuggingFace
    if steps.get("upload_hf", False):
        logging.info("[STEP] HuggingFace upload.")
        from ragformance.dataloaders import push_to_hub

        hf_path = config.get("hf", {}).get("hf_path", None)
        data_path = config.get("generation", {}).get("output", {}).get("path", None)
        hf_token = config.get("hf", {}).get("hf_token", None)
        if hf_path and data_path:
            push_to_hub(
                hf_path, data_path, hf_token
            )  # Note : we could wrap other parameters from config, but we focus on the main ones to have uniform pipelines
            logging.info("[UPLOAD] Upload complete.")
        else:
            logging.info("[UPLOAD] hf.hf_path or generation.output.path not set.")

    # Load dataset from source
    if steps.get("load_dataset", False):
        logging.info("[STEP] Loading dataset from source enabled.")
        if len(corpus) > 0 or len(queries) > 0:
            logging.warning(
                "[Warning] Dataset already loaded from generation. Loading will replace the current dataset."
            )

        source_type = config.get("dataset", {}).get("source_type", "jsonl")
        source_path = config.get("dataset", {}).get("path", "")
        data_path = config.get("data_path", "data")

        if source_type == "jsonl":
            with open(os.path.join(source_path, "corpus.jsonl")) as f:
                corpus = ta.validate_python([json.loads(line) for line in f])
            with open(os.path.join(source_path, "queries.jsonl")) as f:
                queries = taq.validate_python([json.loads(line) for line in f])

        elif source_type == "huggingface":
            from datasets import load_dataset

            corpus = ta.validate_python(
                load_dataset(source_path, "corpus", split="train")
            )
            queries = taq.validate_python(
                load_dataset(source_path, "queries", split="train")
            )
        elif source_type == "beir":
            from ragformance.dataloaders import load_beir_dataset

            filter_corpus = config.get("dataset", {}).get("filter_corpus", False)
            corpus, queries = load_beir_dataset(
                dataset=source_path, folder_path=data_path, filter_corpus=filter_corpus
            )

    # RAG evaluation
    if steps.get("evaluation", False):
        logging.info("[STEP] RAG evaluation enabled.")
        if len(corpus) <= 0 or len(queries) <= 0:
            logging.error("Dataset not loaded, skipping evaluation")

        else:
            answers = run_pipeline_evaluation(corpus, queries, config)

    # Metrics computation
    if steps.get("metrics", False):
        logging.info("[STEP] Metrics computation enabled.")
        metrics_data = compute_metrics(corpus, answers, config)

    # Visualization
    display_widget = None
    if steps.get("visualization", False):
        logging.info("[STEP] Visualization enabled.")
        display_widget = run_visualization(corpus, answers, metrics_data, config)

    # TODO Save answers and metrics

    return corpus, queries, answers, metrics_data, display_widget


def maybe_enable_phoenix_tracing(config):
    """
    Enable Phoenix Arize tracing if enabled in config and the phoenix module is installed.
    """
    phoenix_cfg = config.get("phoenix", {})
    phoenix_enabled = phoenix_cfg.get("enable", False)
    phoenix_endpoint = phoenix_cfg.get("endpoint", "http://localhost:6006")
    project_name = phoenix_cfg.get("project_name", "ragformance")
    auto_instrument = phoenix_cfg.get("auto_instrument", True)
    if phoenix_enabled:
        try:
            import importlib

            phoenix_spec = importlib.util.find_spec("phoenix")
            if phoenix_spec is not None:
                import os

                os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = phoenix_endpoint
                from phoenix.otel import register

                # Configure the Phoenix tracer
                register(project_name=project_name, auto_instrument=auto_instrument)
                print(
                    f"[Phoenix] Tracing enabled via Arize Phoenix at {phoenix_endpoint} (project: {project_name})."
                )
            else:
                print(
                    "[Phoenix] The 'phoenix' module is not installed. Tracing is disabled."
                )
        except Exception as e:
            print(f"[Phoenix] Error while enabling Phoenix tracing: {e}")


def main():
    parser = argparse.ArgumentParser(description="RAGformance End-to-End Runner")
    parser.add_argument(
        "--config", type=str, required=True, help="Path to config JSON file"
    )
    args = parser.parse_args()

    config_path = args.config
    run_pipeline(config_path)


def get_rag_class(
    main_config: Dict[str, Any],
):
    rag_type = main_config.get("rag", {}).get("rag_type", "naive")

    params_for_rag_config = main_config.get("rag", {}).get("params", main_config)

    # Ensure all keys in params_for_rag_config are UPPER_CASE
    # Pydantic model_validate expects a dict.
    upper_case_params = {k.upper(): v for k, v in params_for_rag_config.items()}

    try:
        if rag_type == "naive":
            from ragformance.rag.naive_rag import NaiveRag

            # Ensure all required fields for NaiveRagConfig are in upper_case_params
            # or have defaults.
            pydantic_config = NaiveRagConfig(**upper_case_params)
            return NaiveRag(config=pydantic_config)
        elif rag_type == "openwebui":
            from ragformance.rag.openwebui_rag import OpenwebuiRag

            pydantic_config = OpenWebUIRagConfig(**upper_case_params)
            return OpenwebuiRag(config=pydantic_config)
        elif rag_type == "haystack":  # Added Haystack
            from ragformance.rag.haystack_rag import HaystackRAG

            pydantic_config = HaystackRagConfig(**upper_case_params)
            return HaystackRAG(config=pydantic_config)
        elif rag_type == "multi_embedding_llm":  # Added MultiEmbeddingLLM
            from ragformance.rag.multi_embedding_llm import MultiEmbeddingLLM

            # MultiEmbeddingLLM typically loads from its own JSON.
            # If multi_rag_configuration_path is in main_config:
            multi_config_path = main_config.get(
                "multi_embedding_llm_config_path",
                "ragformance/rag/config/multi_rag_configuration.json",
            )
            if os.path.exists(multi_config_path):
                with open(multi_config_path) as f:
                    json_data = json.load(f)
                # Transform keys to UPPER_CASE for Pydantic model
                upper_case_json_data = {k.upper(): v for k, v in json_data.items()}
                pydantic_config = MultiEmbeddingLLMRagConfig(**upper_case_json_data)
            else:
                # Fallback to params from main config if file not found or path not specified
                logging.warning(
                    f"MultiEmbeddingLLM config file not found at {multi_config_path}. Trying to use params from main config."
                )
                pydantic_config = MultiEmbeddingLLMRagConfig(
                    **upper_case_params
                )  # Uses general params
            return MultiEmbeddingLLM(config=pydantic_config)
        else:
            raise ValueError(f"Unknown rag_type: {rag_type}")
    except ValidationError as e:
        logging.error(f"Configuration validation error for {rag_type}: {e}")
        raise  # Re-raise the validation error to stop execution if config is bad


def run_pipeline_evaluation(
    corpus: List[DocModel],
    queries: List[AnnotatedQueryModel],
    main_config: Dict[str, Any],
):
    logging.info("[EVALUATION] Starting RAG evaluation...")
    rag = get_rag_class(main_config)

    rag.upload_corpus(corpus)
    answers = rag.ask_queries(queries)
    logging.info("[EVALUATION] RAG evaluation complete.")
    return answers


def compute_metrics(corpus, answers, config):
    logging.info("[METRICS] Computing metrics...")

    from ragformance.eval import trec_eval_metrics

    metrics_data = trec_eval_metrics(answers)

    logging.info("[METRICS] Metrics computation complete.")

    return metrics_data


def run_visualization(corpus, answers, metrics_data, config):
    logging.info("[VISUALIZATION] Generating visualizations...")

    from ragformance.eval import visualize_semantic_F1, display_semantic_quadrants

    quadrants = visualize_semantic_F1(
        corpus, answers, embedding_config={"model": "all-MiniLM-L6-v2"}
    )

    display_widget = display_semantic_quadrants(quadrants)

    logging.info("[VISUALIZATION] Visualization complete.")

    return display_widget


if __name__ == "__main__":
    main()
