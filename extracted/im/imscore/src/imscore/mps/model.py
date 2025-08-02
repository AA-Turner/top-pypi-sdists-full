

import torch
from torch import nn, einsum
import torchvision
from dataclasses import dataclass
from transformers import CLIPModel as HFCLIPModel
from transformers import AutoTokenizer
from huggingface_hub import PyTorchModelHubMixin

from transformers import CLIPConfig
from typing import Optional
from .cross import CrossModel
from pathlib import Path


@dataclass
class BaseModelConfig:
    pass


class XCLIPModel(HFCLIPModel):
    def __init__(self, config: CLIPConfig):
        super().__init__(config)
    
    def get_text_features(
        self,
        input_ids: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.Tensor] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
    ) -> torch.FloatTensor:

        # Use CLIP model's config for some fields (if specified) instead of those of vision & text components.
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        text_outputs = self.text_model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        last_hidden_state = text_outputs[0]
        text_features = self.text_projection(last_hidden_state)

        pooled_output = text_outputs[1]
        text_features_eos = self.text_projection(pooled_output)

        return text_features, text_features_eos

    def get_image_features(
        self,
        pixel_values: Optional[torch.FloatTensor] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
    ) -> torch.FloatTensor:
        
        # Use CLIP model's config for some fields (if specified) instead of those of vision & text components.
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        vision_outputs = self.vision_model(
            pixel_values=pixel_values,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        last_hidden_state = vision_outputs[0]
        image_features = self.visual_projection(last_hidden_state)

        return image_features


class CLIPModel(nn.Module):
    def __init__(self, model:str = "laion/CLIP-ViT-H-14-laion2B-s32B-b79K"):
        super().__init__()
        self.model = XCLIPModel.from_pretrained(model)
        self.cross_model = CrossModel(dim=1024, layer_num=4, heads=16)
    
    def get_text_features(self, *args, **kwargs):
        return self.model.get_text_features(*args, **kwargs)

    def get_image_features(self, *args, **kwargs):
        return self.model.get_image_features(*args, **kwargs)

    def forward(self, text_inputs=None, image_inputs=None, condition_inputs=None):
        outputs = ()

        text_f, text_eos = self.model.get_text_features(text_inputs) # B*77*1024
        outputs += text_eos,

        image_f = self.model.get_image_features(image_inputs.half()) # B*257*1024
        condition_f, _ = self.model.get_text_features(condition_inputs) # B*5*1024

        sim_text_condition = einsum('b i d, b j d -> b j i', text_f, condition_f)
        sim_text_condition = torch.max(sim_text_condition, dim=1, keepdim=True)[0]
        sim_text_condition = sim_text_condition / sim_text_condition.max()
        mask = torch.where(sim_text_condition > 0.01, 0, float('-inf')) # B*1*77

        mask = mask.repeat(1, image_f.shape[1], 1) # B*257*77
        sim = self.cross_model(image_f, text_f, mask.half())
        outputs += sim[:,0,:],

        return outputs

    @property
    def logit_scale(self):
        return self.model.logit_scale

    def save(self, path):
        self.model.save_pretrained(path)


class MPS(
        nn.Module,
        PyTorchModelHubMixin,
        library_name="imscore",
        repo_url="https://github.com/RE-N-Y/imscore"
    ):

    def __init__(self):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained("laion/CLIP-ViT-H-14-laion2B-s32B-b79K", trust_remote_code=True)
        self.condition = "light, color, clarity, tone, style, ambiance, artistry, shape, face, hair, hands, limbs, structure, instance, texture, quantity, attributes, position, number, location, word, things." 
        
        mps = CLIPModel("laion/CLIP-ViT-H-14-laion2B-s32B-b79K")
        mps.model.text_model.eos_token_id = 2
        mps.model.text_model.requires_grad_(False)
        mps.model.vision_model.requires_grad_(True)

        self.mps = mps
        self.resize = torchvision.transforms.Resize(224, interpolation=3)
        self.crop = torchvision.transforms.CenterCrop(224)
        self.normalize = torchvision.transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073], std=[0.26862954, 0.26130258, 0.27577711])


    
    def _process(self, x):
        # assumes x is between 0 and 1
        dtype = x.dtype
        x = self.resize(x)
        x = self.crop(x)
        x = self.normalize(x)
        x = x.to(dtype=dtype)

        return x

    def _tokenize(self, captions:list[str]):
        inputs = self.tokenizer(captions, max_length=self.tokenizer.model_max_length, padding="max_length", truncation=True, return_tensors="pt")
        return inputs.input_ids


    def forward(self, *args, **kwargs):
        tfeat, ifeat, score = self.mps(*args, **kwargs) # text pixels conds
        ifeat = ifeat / ifeat.norm(dim=-1, keepdim=True)
        tfeat = tfeat / tfeat.norm(dim=-1, keepdim=True)
        logits = self.mps.logit_scale.exp() * torch.diagonal(torch.einsum('bd,cd->bc', tfeat, ifeat))

        return logits

    def score(self, pixels, prompts:list[str]):
        b, c, h, w = pixels.shape
        pixels = self._process(pixels)
        texts = self._tokenize(prompts).to(pixels.device)
        conds = self._tokenize(self.condition).to(pixels.device)
        
        tfeats, ifeats = self.mps(texts, pixels, conds.repeat(b, 1))
        ifeats = ifeats / ifeats.norm(dim=-1, keepdim=True)
        tfeats = tfeats / tfeats.norm(dim=-1, keepdim=True)

        scores = self.mps.logit_scale.exp() * torch.diagonal(torch.einsum('bd,cd->bc', tfeats, ifeats))

        return scores
        
        
