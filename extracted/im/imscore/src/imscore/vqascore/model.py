import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from transformers import T5ForConditionalGeneration, T5Tokenizer, CLIPVisionModel, CLIPVisionModelWithProjection, CLIPImageProcessor
import textwrap
from huggingface_hub import PyTorchModelHubMixin

class VQAScore(
        nn.Module,
        PyTorchModelHubMixin,
        library_name="preferences",
        repo_url="https://github.com/RE-N-Y/imscore"
    ):

    def __init__(self):
        super().__init__()
        self.t5 = T5ForConditionalGeneration.from_pretrained('google/flan-t5-xxl')
        self.t5.resize_token_embeddings(32100)
        
        self.tokenizer = T5Tokenizer.from_pretrained('google/flan-t5-xxl')
        self.v = CLIPVisionModel.from_pretrained('openai/clip-vit-large-patch14-336')
        self.processor = CLIPImageProcessor.from_pretrained('openai/clip-vit-large-patch14-336')
        self.normalize = torchvision.transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073], std=[0.26862954, 0.26130258, 0.27577711])
        self.resize = torchvision.transforms.Resize((336, 336), interpolation=3)
        self.mm_projector = nn.Sequential(
            nn.Linear(1024, 4 * 1024),
            nn.GELU(),
            nn.Linear(4 * 1024, 4 * 1024)
        )

        self.v.to(dtype=torch.bfloat16, device="cpu")
        self.mm_projector.to(dtype=torch.bfloat16, device="cpu")

    def imgprocess(self, pixels:torch.Tensor, device):
        # 1. pads with image mean, 
        # 2. crop/resize to 336x336 
        # 3. normalise

        # for simplicity, we first normalise, pad with 0s and resize to 336x336
        b, c, h, w = pixels.shape
        pixels = self.normalize(pixels)
        
        if h > w:
            pixels = F.pad(pixels, (0, 0, (h-w)//2, (h-w)//2), mode='constant', value=0)
        elif h < w:
            pixels = F.pad(pixels, ((w-h)//2, (w-h)//2, 0, 0), mode='constant', value=0)

        pixels = self.resize(pixels)

        return pixels



    def format(self, prompt:str):
        return textwrap.dedent(
            f"""A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: <image>
            Does this figure show "{prompt}"? Please answer yes or no. ASSISTANT: """
        )
    
    def get_input_ids(self, prompt):
        chunks = [self.tokenizer(chunk).input_ids for chunk in prompt.split('<image>')]

        def insert(x, sep):
            return [ele for sublist in zip(x, [sep] * len(x)) for ele in sublist][:-1]

        input_ids = []
        for x in insert(chunks, [-200]):
            input_ids.extend(x)

        return input_ids
        

    def txtprocess(self, prompts:list[str], device):
        questions = [self.format(prompt) for prompt in prompts]
        answers = ["Yes"] * len(prompts)
        input_ids = [self.get_input_ids(qs) for qs in questions]
        labels = [self.get_input_ids(ans) for ans in answers]


        input_ids = [torch.tensor(ids, device=device) for ids in input_ids]
        labels = [torch.tensor(ids, device=device) for ids in labels]

        input_ids = torch.nn.utils.rnn.pad_sequence(input_ids, batch_first=True, padding_value=self.tokenizer.pad_token_id)
        labels = torch.nn.utils.rnn.pad_sequence(labels, batch_first=True, padding_value=-100)
        input_ids = input_ids[:, :self.tokenizer.model_max_length]
        labels = labels[:, :self.tokenizer.model_max_length]

        attention_mask = input_ids.ne(self.tokenizer.pad_token_id)
        decoder_attention_mask = labels.ne(-100)

        return input_ids, attention_mask, decoder_attention_mask, labels


    def score(self, pixels, prompts:list[str]):
        SHIFT = 1

        pixels = self.imgprocess(pixels, device=pixels.device)
        vision_features = self.v(pixels, output_hidden_states=True).hidden_states[-2]
        vision_features = self.mm_projector(vision_features)
        
        # for testing        
        input_ids, attention_mask, decoder_attention_mask, labels = self.txtprocess(prompts, device=pixels.device)

        idx = 0
        embeds = []

        for ids in input_ids:
            _embeds = []

            (start,) = torch.where(ids == -200)
            features = vision_features[idx]
            
            _embeds.append(self.t5.encoder.embed_tokens(ids[:start]))
            _embeds.append(features)
            _embeds.append(self.t5.encoder.embed_tokens(ids[start+SHIFT:]))
            _embeds = torch.cat(_embeds)

            embeds.append(_embeds)


        embeds = torch.stack(embeds)

        padding = torch.full((len(attention_mask), embeds.shape[1] - attention_mask.shape[1]), True, dtype=attention_mask.dtype, device=attention_mask.device)
        attention_mask = torch.cat([padding, attention_mask], dim=1)
        outputs = self.t5(
            inputs_embeds=embeds, 
            attention_mask=attention_mask, 
            decoder_attention_mask=decoder_attention_mask, 
            labels=labels
        )

        return torch.exp(-outputs.loss)