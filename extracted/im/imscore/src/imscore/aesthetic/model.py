import torch
import torch.nn as nn
import torchvision
from torchvision.transforms.functional import InterpolationMode
from transformers import AutoModel, AutoProcessor, AutoImageProcessor
from transformers import SiglipVisionModel, Dinov2Model, CLIPVisionModelWithProjection, ViTForImageClassification
from huggingface_hub import PyTorchModelHubMixin
from ..utils import get_image_transform


class ShadowAesthetic(
        nn.Module,
        PyTorchModelHubMixin,
        library_name="imscore",
        repo_url="https://github.com/RE-N-Y/imscore"
    ):
    def __init__(self):
        super().__init__()
        self.model = ViTForImageClassification.from_pretrained("RE-N-Y/aesthetic-shadow-v2")
        self.resize = torchvision.transforms.Resize((1024, 1024), interpolation=2)
        self.normalize = torchvision.transforms.Normalize(mean=[0.65463551, 0.60715182, 0.61108185], std=[0.32903292, 0.32726001, 0.31909652])

    def forward(self, pixels, prompts=None):
        return self.score(pixels, prompts)
    
    def score(self, pixels, prompts=None):
        # assume pixels is between 0 and 1
        dtype = pixels.dtype
        pixels = self.resize(pixels)
        pixels = self.normalize(pixels)
        pixels = pixels.to(dtype=dtype)

        outputs = self.model(pixels)
        return outputs.logits.squeeze()
    
class CLIPAestheticScorer(
        nn.Module, 
        PyTorchModelHubMixin,
        library_name="imscore",
        repo_url="https://github.com/RE-N-Y/imscore"
    ):
    def __init__(self, tag:str, expansion:int = 4, layers:int = 3, freeze:int = -1, dropout:float = 0.1):
        super().__init__()

        model = AutoModel.from_pretrained(tag)
        self.model = model.vision_model
        self.processor = AutoProcessor.from_pretrained(tag)
        
        nlayers = len(self.model.encoder.layers)
        for name, param in self.model.named_parameters():
            if name.startswith("encoder.layers"):
                _, _, lidx, *_ = name.split(".")
                if int(lidx) < nlayers + freeze:
                    param.requires_grad = False

        self.tform = get_image_transform(self.processor.image_processor)

        hiddens = self.model.config.hidden_size
        self.head = nn.Sequential(
            nn.Linear(hiddens, hiddens * expansion), nn.Dropout(p=dropout),
            *[nn.Linear(hiddens * expansion, hiddens * expansion), nn.ReLU(), nn.Dropout(p=dropout)] * layers,
            nn.Linear(hiddens * expansion, hiddens),
            nn.Linear(hiddens, hiddens // 2),
            nn.Linear(hiddens // 2, 1)
        )

    def forward(self, *args, **kwargs):
        outputs = self.model(*args, **kwargs).last_hidden_state
        scores = self.head(outputs[:, 0, :])
        return scores.squeeze()
    
    def score(self, pixels, prompts=None):
        # assume pixels is between 0 and 1
        pixels = self.tform(pixels)
        outputs = self.model(pixel_values=pixels).last_hidden_state
        scores = self.head(outputs[:, 0, :])

        return scores.squeeze()
    

class SiglipAestheticScorer(
        nn.Module,
        PyTorchModelHubMixin,
        library_name="imscore",
        repo_url="https://github.com/RE-N-Y/imscore"
    ):
    def __init__(self, tag:str, expansion:int = 4, layers:int = 3, freeze:int = -1, dropout:float = 0.1):
        super().__init__()

        self.model = SiglipVisionModel.from_pretrained(tag)
        self.processor = AutoProcessor.from_pretrained(tag)
        nlayers = len(self.model.vision_model.encoder.layers)

        self.tform = get_image_transform(self.processor.image_processor)

        for name, param in self.model.named_parameters():
            if name.startswith("vision_model.encoder.layers"):
                _, _, _, lidx, *_ = name.split(".")
                if int(lidx) < nlayers + freeze:
                    param.requires_grad = False

        hiddens = self.model.config.hidden_size
        self.head = nn.Sequential(
            nn.Linear(hiddens, hiddens * expansion), nn.Dropout(p=dropout),
            *[nn.Linear(hiddens * expansion, hiddens * expansion), nn.ReLU(), nn.Dropout(p=dropout)] * layers,
            nn.Linear(hiddens * expansion, hiddens),
            nn.Linear(hiddens, hiddens // 2),
            nn.Linear(hiddens // 2, 1)
        )

    def forward(self, *args, **kwargs):
        hiddens = self.model(*args, **kwargs).last_hidden_state
        hiddens = torch.mean(hiddens, dim=1)

        return self.head(hiddens).squeeze()
    
    def score(self, pixels, prompts=None):
        # assume pixels is between 0 and 1
        pixels = self.tform(pixels)
        hiddens = self.model(pixel_values=pixels).last_hidden_state
        hiddens = torch.mean(hiddens, dim=1)

        return self.head(hiddens).squeeze()

class Dinov2AestheticScorer(
        nn.Module,
        PyTorchModelHubMixin,
        library_name="imscore",
        repo_url="https://github.com/RE-N-Y/imscore"
    ):
    def __init__(self, tag:str, expansion:int = 4, layers:int = 3, freeze:int = -1, dropout:float = 0.1):
        super().__init__()

        self.model = Dinov2Model.from_pretrained(tag)
        self.processor = AutoImageProcessor.from_pretrained(tag)
        nlayers = len(self.model.encoder.layer)
        for name, param in self.model.named_parameters():
            if name.startswith("encoder.layer"):
                _, _, lidx, *_ = name.split(".")
                if int(lidx) < nlayers + freeze:
                    param.requires_grad = False

        self.tform = get_image_transform(self.processor)

        hiddens = 2 * self.model.config.hidden_size
        self.head = nn.Sequential(
            nn.Linear(hiddens, hiddens * expansion), nn.Dropout(p=dropout),
            *[nn.Linear(hiddens * expansion, hiddens * expansion), nn.ReLU(), nn.Dropout(p=dropout)] * layers,
            nn.Linear(hiddens * expansion, hiddens),
            nn.Linear(hiddens, hiddens // 2),
            nn.Linear(hiddens // 2, hiddens // 4),
            nn.Linear(hiddens // 4, 1)
        )
    
    def forward(self, *args, **kwargs):
        hiddens = self.model(*args, **kwargs).last_hidden_state
        cls_token = hiddens[:, 0]
        patch_tokens = hiddens[:, 1:]
        
        hiddens = torch.cat([cls_token, patch_tokens.mean(dim=1)], dim=1)

        return self.head(hiddens).squeeze()
    
    def score(self, pixels, prompts=None):
        # assume pixels is between 0 and 1
        pixels = self.tform(pixels)
        hiddens = self.model(pixel_values=pixels).last_hidden_state
        cls_token = hiddens[:, 0]
        patch_tokens = hiddens[:, 1:]

        hiddens = torch.cat([cls_token, patch_tokens.mean(dim=1)], dim=1)

        return self.head(hiddens).squeeze()
    
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(768, 1024),
            nn.Dropout(0.2),
            nn.Linear(1024, 128),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.Dropout(0.1),
            nn.Linear(64, 16),
            nn.Linear(16, 1),
        )


    def forward(self, embed):
        return self.layers(embed)

class LAIONAestheticScorer(
        nn.Module,
        PyTorchModelHubMixin,
        library_name="imscore",
        repo_url="https://github.com/RE-N-Y/imscore"
    ):
    def __init__(self):
        super().__init__()
        
        self.clip = CLIPVisionModelWithProjection.from_pretrained("openai/clip-vit-large-patch14")
        self.mlp = MLP()
        self.resize = torchvision.transforms.Resize(224, interpolation=InterpolationMode.BICUBIC)
        self.crop = torchvision.transforms.CenterCrop(224)
        self.normalize = torchvision.transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073], std=[0.26862954, 0.26130258, 0.27577711])

    def forward(self, *args, **kwargs):
        embeds = self.clip(*args, **kwargs).image_embeds
        embeds = embeds / torch.linalg.vector_norm(embeds, dim=-1, keepdim=True)
        scores = self.mlp(embeds)

        return scores.squeeze(-1)

    def score(self, pixels, prompts=None):
        # assume pixels is between 0 and 1
        pixels = self.resize(pixels)
        pixels = self.crop(pixels)
        pixels = self.normalize(pixels)
        embed = self.clip(pixel_values=pixels).image_embeds
        embed = embed / torch.linalg.vector_norm(embed, dim=-1, keepdim=True)
        scores = self.mlp(embed)

        return scores.squeeze(-1)


