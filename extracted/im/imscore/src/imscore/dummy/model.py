import torch
import torch.nn as nn
import torchvision
from pathlib import Path
from einops import reduce

class DummyReward(nn.Module):

    def __init__(self):
        super().__init__()

    def forward(self, pixels, prompts=None):
        return self.score(pixels, prompts)

    def score(self, pixels, prompts:list[str]):
        return reduce(pixels, 'b c h w -> b', 'mean')
    
