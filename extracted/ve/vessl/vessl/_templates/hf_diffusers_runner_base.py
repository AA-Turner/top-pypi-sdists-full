import io
from typing import Dict, List, Optional, Union

import torch
from diffusers import DiffusionPipeline
from PIL import Image
from pydantic import BaseModel

from vessl.service import RunnerBase

MODEL_NAME_OR_PATH = "{MODEL_NAME_OR_PATH}"


class InputType(BaseModel):
    prompt: Union[str, List[str]]
    height: Optional[int] = None
    width: Optional[int] = None
    num_inference_steps: Optional[int] = 50
    guidance_scale: Optional[float] = 7.5
    negative_prompt: Optional[Union[str, List[str]]] = None


class OutputType(BaseModel):
    result: bytes


def get_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


class HfDiffuserRunner(RunnerBase[InputType, OutputType]):
    @staticmethod
    def load_model(
        props: Union[Dict[str, str], None], artifacts: Dict[str, str]
    ) -> DiffusionPipeline:
        pipeline = DiffusionPipeline.from_pretrained(
            MODEL_NAME_OR_PATH, torch_dtype=torch.float16, variant="fp16"
        )

        device = get_device()
        pipeline = pipeline.to(device)

        return pipeline

    @staticmethod
    def preprocess_data(data: InputType) -> InputType:
        return data

    @staticmethod
    def predict(model: DiffusionPipeline, data: InputType) -> Image.Image:
        inputs = data.model_dump()
        outputs = model(**inputs)
        return outputs.images[0]

    @staticmethod
    def postprocess_data(data: Image.Image):
        fp = io.BytesIO()
        data.save(fp, format="PNG")
        byte_array = fp.getvalue()

        return {"result": byte_array}


if __name__ == "__main__":
    inputs = InputType(prompt="white cat")

    model = HfDiffuserRunner.load_model(None, None)
    data = HfDiffuserRunner.preprocess_data(inputs)
    result = HfDiffuserRunner.predict(model, data)
    output = HfDiffuserRunner.postprocess_data(result)
