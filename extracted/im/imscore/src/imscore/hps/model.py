import torch
import torch.nn as nn
import torchvision
from pathlib import Path

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms.functional as TF
from torchvision.transforms import InterpolationMode
from open_clip import create_model_and_transforms, get_tokenizer
from huggingface_hub import PyTorchModelHubMixin


class ResizeMaxSize(nn.Module):
    def __init__(self, size, interpolation=InterpolationMode.BICUBIC, fill=0):
        super().__init__()
        self.size = size
        self.interpolation = interpolation
        self.fill = fill

    def forward(self, img):
        if isinstance(img, torch.Tensor):
            height, width = img.shape[-2:]
        else:
            width, height = img.size
        scale = self.size / float(max(height, width))
        if scale != 1.0:
            _size = tuple(round(dim * scale) for dim in (height, width))
            img = TF.resize(img, _size, self.interpolation)
            hpad = self.size - _size[0]
            wpad = self.size - _size[1]
            img = TF.pad(img, padding=[wpad // 2, hpad // 2, wpad - wpad // 2, hpad - hpad // 2], fill=self.fill)
        return img

class HPSv2(
        nn.Module,
        PyTorchModelHubMixin,
        library_name="imscore",
        repo_url="https://github.com/RE-N-Y/imscore"
    ):

    def __init__(self):
        super().__init__()
        self.model, _, self.processor = create_model_and_transforms(
            "ViT-H-14",
            'laion2B-s32B-b79K',
            output_dict=True,
        )    
    
        self.tokenizer = get_tokenizer("ViT-H-14")
        self.resize = ResizeMaxSize(224)
        self.normalize = torchvision.transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073], std=[0.26862954, 0.26130258, 0.27577711])

    
    def _process(self, x):
        # assumes x is between 0 and 1
        dtype = x.dtype
        x = self.resize(x)
        x = self.normalize(x)
        x = x.to(dtype=dtype)

        return x
    
    def score(self, opixels, prompts:list[str]):
        b, c, h, w = opixels.shape
        pixels = self._process(opixels)
        captions = self.tokenizer(prompts)
        captions = captions.to(pixels.device)
        outputs = self.model(pixels, captions)
        image_features, text_features = outputs["image_features"], outputs["text_features"]
        logits = image_features @ text_features.T
        scores = torch.diagonal(logits)

        return scores
    
    def forward(self, *args, **kwargs):
        outputs = self.model(*args, **kwargs) # open clip model args
        image_features, text_features = outputs["image_features"], outputs["text_features"]
        logits = image_features @ text_features.T

        return logits