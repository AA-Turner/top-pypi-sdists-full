import torch
import torch.nn as nn
import torchvision.transforms as T
from torchvision.transforms import InterpolationMode
from huggingface_hub import PyTorchModelHubMixin
from einops import rearrange, reduce
from transformers import BertTokenizer, BertConfig
from .bert import BertLMHeadModel
from .vit import VisionTransformer

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(768, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )
        
    def forward(self, input):
        return self.layers(input)


class EvalMuse(
        nn.Module,
        PyTorchModelHubMixin,
        library_name="imscore",
        repo_url="https://github.com/RE-N-Y/imscore"
    ):
    def __init__(self):
        super().__init__()

        config = {
            "attention_probs_dropout_prob": 0.1,
            "hidden_act": "gelu",
            "hidden_dropout_prob": 0.1,
            "hidden_size": 768,
            "initializer_range": 0.02,
            "intermediate_size": 3072,
            "layer_norm_eps": 1e-12,
            "max_position_embeddings": 512,
            "model_type": "bert",
            "num_attention_heads": 12,
            "num_hidden_layers": 12,
            "pad_token_id": 0,
            "type_vocab_size": 2,
            "vocab_size": 30523,
            "encoder_width": 1408,
            "add_cross_attention": True
        }
        config = BertConfig.from_dict(config)

        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.visual_encoder = VisionTransformer(img_size=364, patch_size=14, in_chans=3, embed_dim=1408, depth=39, num_heads=16, mlp_ratio=4.364)
        self.ln_vision = nn.LayerNorm((1408,))
        self.Qformer = BertLMHeadModel(config)
        self.vision_proj = nn.Linear(in_features=768, out_features=256, bias=True)
        self.text_proj = nn.Linear(in_features=768, out_features=256, bias=True)
        self.itm_head = nn.Linear(in_features=768, out_features=2, bias=True)
        self.query_tokens = nn.Parameter(torch.randn(1, 32, 768))
        self.mask_proj = MLP()

        self.preprocess = T.Compose([
            T.Resize((364, 364), interpolation=InterpolationMode.BICUBIC),
            T.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)),
        ])


    def score(self, opixels, prompts:list[str]):
        pixels = self.preprocess(opixels)
        texts = self.tokenizer(prompts, padding='max_length', return_tensors="pt", max_length=32, truncation=True)
        texts = texts.to(opixels.device)
        
        # print("text input ids", texts.input_ids.shape)
        embeds = self.ln_vision(self.visual_encoder(pixels))
        embeds = embeds.float()
        query_tokens = self.query_tokens.expand(len(prompts), -1, -1)

        bq, tq, dq = query_tokens.shape
        be, te, de = embeds.shape
        query_attention_mask = torch.ones(bq, tq, device=embeds.device)
        embeds_attention_mask = torch.ones(be, te, device=embeds.device)
        attention_mask = torch.cat([query_attention_mask, texts.attention_mask], dim=1)
        
        output = self.Qformer.bert(
            texts.input_ids,
            query_embeds=query_tokens,
            attention_mask=attention_mask,
            encoder_hidden_states=embeds,
            encoder_attention_mask=embeds_attention_mask,
        )
        embeddings = output[:, :, :]
        logit = self.itm_head(embeddings)
        scores = torch.nn.functional.softmax(logit, dim=2)
        scores = reduce(scores[:, :tq, 1], 'b t -> b', 'mean')

        return scores * 4 + 1