
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as T
from transformers import BertTokenizer, BertConfig
from .bert import BertModel
from .vit import VisionTransformer


class BLIP(nn.Module):
    def __init__(
        self,                 
        image_size = 224,
        vision_width = 1024,              
        embed_dim = 256,     
    ):
        super().__init__()
        
        self.visual_encoder = VisionTransformer(img_size=image_size, patch_size=16, embed_dim=vision_width, depth=24, num_heads=16)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.tokenizer.add_special_tokens({'bos_token':'[DEC]'})
        self.tokenizer.add_special_tokens({'additional_special_tokens':['[ENC]']})       
        self.tokenizer.enc_token_id = self.tokenizer.additional_special_tokens_ids[0]

        config = {
            "architectures": [
                "BertModel"
            ],
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
            "vocab_size": 30524,
            "encoder_width": 768,
            "add_cross_attention": True
        }

        encoder_config = BertConfig.from_dict(config)
        encoder_config.encoder_width = vision_width
        self.text_encoder = BertModel(config=encoder_config)

        text_width = self.text_encoder.config.hidden_size
        self.vision_proj = nn.Linear(vision_width, embed_dim)
        self.text_proj = nn.Linear(text_width, embed_dim)


class MLP(nn.Module):
    def __init__(self, hiddens):
        super().__init__()
        self.hiddens = hiddens
        self.layers = nn.Sequential(
            nn.Linear(self.hiddens, 1024),
            nn.Dropout(0.2),
            nn.Linear(1024, 128),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.Dropout(0.1),
            nn.Linear(64, 16),
            nn.Linear(16, 1)
        )
        
    def forward(self, input):
        return self.layers(input)