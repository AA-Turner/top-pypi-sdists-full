
import torch
import torch.nn as nn
import torchvision.transforms as T
from torchvision.transforms import InterpolationMode
from huggingface_hub import PyTorchModelHubMixin
from .blip import BLIP

class MLP(nn.Module):
    def __init__(self, hiddens):
        super().__init__()
        self.hiddens = hiddens
        self.layers = nn.Sequential(
            nn.Linear(hiddens, 1024),
            nn.GELU(),
            nn.Linear(1024, 128),
            nn.GELU(),
            nn.Linear(128, 64),
            nn.GELU(),
            nn.Linear(64, 16),
            nn.GELU(),
            nn.Linear(16, 1)
        )
        
    def forward(self, input):
        return self.layers(input)


class CycleReward(
        nn.Module,
        PyTorchModelHubMixin,
        library_name="imscore",
        repo_url="https://github.com/RE-N-Y/imscore"
    ):

    def __init__(self):
        super().__init__()
        
        self.blip = BLIP(image_size=224)
        self.preprocess = T.Compose([
            T.Resize(224, interpolation=InterpolationMode.BICUBIC),
            T.CenterCrop(224),
            T.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)),
        ])

        self.mlp = MLP(768)
    
    def score(self, opixels, prompts:list[str]):
        pixels = self.preprocess(opixels)
        texts = self.blip.tokenizer(prompts, padding='max_length', truncation=True, max_length=128, return_tensors="pt")
        embeds = self.blip.visual_encoder(pixels)

        b, t, d = embeds.shape
        mask = torch.ones(b, t, device=embeds.device, dtype=torch.bool)
        texts = texts.to(embeds.device)
        
        text_output = self.blip.text_encoder(
            texts.input_ids,
            attention_mask = texts.attention_mask,
            encoder_hidden_states = embeds,
            encoder_attention_mask = mask,
        )

        txt_features = text_output[:,0,:]
        rewards = self.mlp(txt_features)
        
        return rewards