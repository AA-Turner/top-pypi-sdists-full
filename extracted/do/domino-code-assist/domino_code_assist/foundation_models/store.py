from dataclasses import asdict, dataclass
from typing import List, Optional

import solara

from domino_code_assist.util import to_float, to_int

curated_models = {
    "Natural Language Processing": {
        "Text Classification": {
            "models": [
                "bert-base-uncased",
                "bert-base-cased",
                "yiyanghkust/finbert-tone",
                "roberta-base",
                "xlm-roberta-base",
                "distilbert-base-uncased",
                "distilbert-base-cased",
            ],
            "description": "Text Classification is the task of assigning a label or class to a given text.",
            "input": "text",
            "output": "label",
        },
        "Text Generation": {
            "models": [
                "gpt2",
                "distilgpt2",
                "gpt2-medium",
                "bigscience/bloom-560m",
            ],
            "description": "Text Generation is the task of producing new text.",
            "input": "text",
        },
        "Token Classification": {
            "models": [
                "bert-base-uncased",
                "bert-base-cased",
                "roberta-base",
                "xlm-roberta-base",
                "distilbert-base-uncased",
                "distilbert-base-cased",
            ],
            "description": "Token classification is a natural language understanding task in which a label is assigned to some tokens in a text.",
            "input": "tokens",
            "output": "ner_tags",
        },
        "Conversational": {
            "models": [
                "microsoft/DialoGPT-small",
                "microsoft/DialoGPT-medium",
                "facebook/blenderbot_small-90M",
                "facebook/blenderbot-400M-distill",
            ],
            "description": "Conversational response modeling is the task of generating conversational text that is relevant, coherent and knowledgable given a prompt.",  # noqa: E501
        },
        "Summarization": {
            "models": [
                "t5-base",
                "t5-small",
                "facebook/bart-large-cnn",
                "google/pegasus-cnn_dailymail",
            ],
            "description": "Summarization is the task of producing a shorter version of a document while preserving its important information.",
            "input": "text",
            "output": "summary",
        },
    },
    "Computer Vision": {
        "Image Classification": {
            "models": [
                "google/vit-base-patch16-224",
                "microsoft/resnet-50",
            ],
            "description": "Image Classification is the task of assigning a label or class to an entire image.",
            "input": "img",
            "output": "label",
        },
        "Object Detection": {
            "models": [
                "facebook/detr-resnet-50",
                "hustvl/yolos-tiny",
            ],
            "description": "Object Detection models allow users to identify objects of certain defined classes.",
            "input": "image",
            "output": "objects",
        },
    },
}

config = {
    "Text Classification": {
        "input_col_name": "text",
        "output_col_name": "label",
        "config": {
            "max_iter": {
                "type": "int",
                "default": 20,
            }
        },
    },
    "Token Classification": {"input_col_name": "?", "output_col_name": "?", "config": {"?": {}}},
}


def categories():
    return list(curated_models.keys())


def tasks(category):
    return list(curated_models.get(category, {}).keys())


def models(category, task):
    return curated_models.get(category, {}).get(task, {}).get("models", [])


def description(category, task):
    return curated_models.get(category, {}).get(task, {}).get("description", "")


def is_recommended(category, task, model):
    model_list = models(category, task)
    return model_list and model == model_list[0]


@dataclass(frozen=True)
class TuneConfig:
    category: Optional[str] = None
    task: Optional[str] = None
    model_name: Optional[str] = None
    model_selected: bool = False
    df_var_name: Optional[str] = None
    input_col_name: Optional[str] = None
    output_col_name: Optional[str] = None
    experiment_name: Optional[str] = None
    use_huggingface_dataset: bool = True
    hf_dataset_name: Optional[str] = None
    hf_dataset_config_options: Optional[List[str]] = None
    hf_dataset_config: Optional[str] = None
    hf_dataset_error: bool = False
    epochs: Optional[str] = "3"
    output_dir: Optional[str] = "output"
    learning_rate: Optional[str] = "0.00001"
    evaluation_strategy: str = "epoch"
    per_device_train_batch_size: str = "4"
    per_device_eval_batch_size: str = "4"
    weight_decay: str = "0.01"
    metric_for_best_model: str = "accuracy"
    save_total_limit: str = "2"
    save_strategy: str = "epoch"

    # seq to seq specific
    max_input_length: Optional[str] = "1024"
    max_output_length: Optional[str] = "128"

    # Image Classification specific
    gradient_accumulation_steps: Optional[str] = "4"
    warmup_ratio: Optional[str] = "0.1"
    logging_steps: Optional[str] = "10"

    # Object Detection specific
    fp16: bool = True
    save_steps: Optional[str] = "200"
    label_key: Optional[str] = "category"


def get_column_name(tune_config: TuneConfig, name: str) -> str:
    return curated_models.get(tune_config.category, {}).get(tune_config.task, {}).get(name, name)  # type: ignore


def is_valid(config: TuneConfig):
    general_valid = bool(
        config.category
        and config.task
        and config.model_name
        and config.experiment_name
        and config.input_col_name
        and config.output_col_name
        and config.input_col_name != config.output_col_name
        and to_int(config.epochs) is not None
        and config.output_dir
        and to_float(config.learning_rate) is not None
        and (
            config.task not in ["Conversational", "Text Generation", "Summarization"]
            or (to_int(config.max_input_length) is not None and to_int(config.max_output_length) is not None)
        )
        and (
            config.task not in ["Image Classification"]
            or (
                to_int(config.gradient_accumulation_steps) is not None
                and to_float(config.warmup_ratio) is not None
                and to_int(config.logging_steps) is not None
            )
        )
        and (
            config.task not in ["Object Detection"] or (to_int(config.save_steps) is not None and to_int(config.logging_steps) is not None and config.label_key)
        )
    )

    if config.use_huggingface_dataset:
        if config.hf_dataset_config_options:
            hf_valid = bool(config.hf_dataset_name and config.hf_dataset_config)
        else:
            hf_valid = bool(config.hf_dataset_name)
        return general_valid and hf_valid
    else:
        df_valid = bool(config.df_var_name)
        return general_valid and df_valid


tune_config = solara.reactive(TuneConfig())


def to_json(obj: TuneConfig):
    if isinstance(obj, TuneConfig):
        return {"type_tune_config": asdict(obj)}


def from_json(dct):
    if "type_tune_config" in dct:
        return TuneConfig(**dct["type_tune_config"])
