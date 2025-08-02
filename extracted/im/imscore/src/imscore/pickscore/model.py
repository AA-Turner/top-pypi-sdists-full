import torch
import torch.nn as nn
import torchvision
from transformers import AutoProcessor, CLIPModel
from huggingface_hub import PyTorchModelHubMixin

# TODO: fix mismatch in processing output
# score has an error of +-0.1

class PickScorer(
    nn.Module,
    PyTorchModelHubMixin,
    library_name="imscore",
    repo_url="https://github.com/RE-N-Y/imscore"
):
    def __init__(self, model:str = "yuvalkirstain/PickScore_v1"):
        super().__init__()
        self.processor = AutoProcessor.from_pretrained("laion/CLIP-ViT-H-14-laion2B-s32B-b79K")
        self.model = CLIPModel.from_pretrained(model)
        self.resize = torchvision.transforms.Resize(224, interpolation=3) # Resize to 224x224      
        self.crop = torchvision.transforms.CenterCrop(224) # Center crop to 224x224  
        self.normalize = torchvision.transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073], std=[0.26862954, 0.26130258, 0.27577711])

    def _process(self, pixels):
        dtype = pixels.dtype
        pixels = self.resize(pixels)
        pixels = self.crop(pixels)
        pixels = self.normalize(pixels)
        pixels = pixels.to(dtype=dtype)

        return pixels
        

    def score(self, pixels, prompts:list[str]):
        # pixels = self.processor(images=pixels, padding=True, truncation=True, max_length=77, return_tensors="pt").to(pixels.device)
        texts = self.processor(text=prompts, padding=True, truncation=True, max_length=77, return_tensors="pt").to(pixels.device)
        pixels = self._process(pixels)

        pixels = self.model.get_image_features(pixel_values=pixels)
        pixels = pixels / torch.norm(pixels, dim=-1, keepdim=True)

        texts = self.model.get_text_features(**texts)
        texts = texts / torch.norm(texts, dim=-1, keepdim=True)

        scores = self.model.logit_scale.exp() * (texts @ pixels.T)
        scores = torch.diagonal(scores)

        return scores
    
    def forward(self, *args, **kwargs):
        # NOTE: should double check if this is correct
        outputs = self.model(*args, **kwargs)
        return outputs.logits_per_image
