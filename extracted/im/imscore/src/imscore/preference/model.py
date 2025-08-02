import torch
import torch.nn as nn
import torchvision
from transformers import AutoModel, AutoProcessor
from transformers import SiglipModel
from huggingface_hub import PyTorchModelHubMixin
from ..utils import get_image_transform


class SiglipPreferenceScorer(
        nn.Module,
        PyTorchModelHubMixin,
        library_name="preferences",
        repo_url="https://github.com/RE-N-Y/imscore"
    ):

    def __init__(self, tag:str):
        super().__init__()
        self.tag = tag
        self.model = SiglipModel.from_pretrained(tag)
        self.processor = AutoProcessor.from_pretrained(tag)
        self.tform = get_image_transform(self.processor.image_processor) 


    def forward(self, *args, **kwargs):
        outputs = self.model(*args, **kwargs)
        return outputs.logits_per_image
    
    def _process(self, pixels):
        dtype = pixels.dtype
        pixels = self.tform(pixels)
        pixels = pixels.to(dtype=dtype)

        return pixels
    
    def score(self, pixels, prompts:list[str]):
        texts = self.processor(text=prompts, padding='max_length', truncation=True, return_tensors="pt").to(pixels.device)
        pixels = self._process(pixels)
        outputs = self.model(pixel_values=pixels, **texts)
        return outputs.logits_per_image.diagonal()

class CLIPPreferenceScorer(
        nn.Module,
        PyTorchModelHubMixin,
        library_name="preferences",
        repo_url="https://github.com/RE-N-Y/imscore"
    ):

    def __init__(self, tag:str):
        super().__init__()
        self.model = AutoModel.from_pretrained(tag)
        self.processor = AutoProcessor.from_pretrained(tag)
        self.tform = get_image_transform(self.processor.image_processor)

    def forward(self, *args, **kwargs):
        outputs = self.model(*args, **kwargs)
        return outputs.logits_per_image
    
    def _process(self, pixels):
        dtype = pixels.dtype
        pixels = self.tform(pixels)
        pixels = pixels.to(dtype=dtype)

        return pixels
    
    def score(self, pixels, prompts:list[str]):
        texts = self.processor(text=prompts, padding='max_length', truncation=True, return_tensors="pt").to(pixels.device)
        pixels = self._process(pixels)
        outputs = self.model(pixel_values=pixels, **texts)
        return outputs.logits_per_image.diagonal()
    

class CLIPScore(
    nn.Module,
    PyTorchModelHubMixin,
    library_name="imscore",
    repo_url="https://github.com/RE-N-Y/imscore"
):
    def __init__(self, tag:str):
        super().__init__()
        self.model = AutoModel.from_pretrained(tag)
        self.processor = AutoProcessor.from_pretrained(tag)
        self.tform = get_image_transform(self.processor.image_processor)

    def forward(self, *args, **kwargs):
        outputs = self.model(*args, **kwargs)
        return outputs.logits_per_image
    
    def _process(self, pixels):
        dtype = pixels.dtype
        pixels = self.tform(pixels)
        pixels = pixels.to(dtype=dtype)

        return pixels
    
    def score(self, pixels, prompts:list[str]):
        texts = self.processor(text=prompts, padding='max_length', truncation=True, return_tensors="pt").to(pixels.device)
        pixels = self._process(pixels)
        outputs = self.model(pixel_values=pixels, **texts)
        return outputs.logits_per_image.diagonal()