from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Union

import torch
from pydantic import BaseModel
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
)

from vessl.service import RunnerBase

MODEL_NAME_OR_PATH = "{MODEL_NAME_OR_PATH}"


@dataclass
class HfLanguageModel:
    tokenizer: PreTrainedTokenizer
    model: PreTrainedModel


class InputType(BaseModel):
    text: str
    max_length: Optional[int] = 20
    max_new_tokens: Optional[int] = None
    do_sample: Optional[bool] = False
    temperature: Optional[float] = 1.0
    top_k: Optional[int] = 50
    top_p: Optional[float] = 1.0
    num_beams: Optional[int] = 1
    num_beam_groups: Optional[int] = 1


class OutputType(BaseModel):
    result: str


def get_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


class HfTransformerRunner(RunnerBase[InputType, OutputType]):
    @staticmethod
    def load_model(
        props: Union[Dict[str, str], None], artifacts: Dict[str, str]
    ) -> Tuple[PreTrainedModel, PreTrainedTokenizer]:
        # TODO: transformer has a lot of models including causal LM
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME_OR_PATH)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME_OR_PATH)

        device = get_device()
        model = model.to(device)

        return HfLanguageModel(tokenizer, model)

    @staticmethod
    def preprocess_data(data: InputType) -> str:
        return data

    @staticmethod
    def predict(model: HfLanguageModel, data: InputType) -> str:
        tokenizer = model.tokenizer
        model = model.model

        inputs = tokenizer(data.text, return_tensors="pt").to(model.device)
        configs = data.model_dump(exclude={"text"})
        outputs = model.generate(**inputs, **configs)
        output_text = tokenizer.decode(outputs[0])

        return output_text

    @staticmethod
    def postprocess_data(data: str):
        return OutputType(result=data)


if __name__ == "__main__":
    inputs = InputType(text="Hello!")

    model = HfTransformerRunner.load_model(None, None)
    data = HfTransformerRunner.preprocess_data(inputs)
    result = HfTransformerRunner.predict(model, data)
    output = HfTransformerRunner.postprocess_data(result)
