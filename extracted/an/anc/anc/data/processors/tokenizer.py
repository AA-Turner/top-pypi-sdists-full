from transformers import AutoTokenizer
from typing import List
import logging

class HFPretrainedTokenizer():
    def __init__(self, opt):
        self.opt = opt
        logging.info(f"Loading vocab from huggingface {opt.hf_model_name}")
        # if getattr(self.opt, 'model_type') == 'llama':
        #     from transformers.models.llama.tokenization_llama import LlamaTokenizer
        #     self.hf_tokenizer = LlamaTokenizer.from_pretrained(
        #         opt.hf_model_name, 
        #         trust_remote_code=True,
        #         bos_token='<s>',
        #         eos_token='</s>',
        #         unk_token='<unk>',
        #     )
        # else:
        self.hf_tokenizer = AutoTokenizer.from_pretrained(opt.hf_model_name, trust_remote_code=True)

        # Add special tokens
        self.override_special_tokens()
        self.vocab_size = len(self.hf_tokenizer.get_vocab())
        logging.info(f'Special tokens: {self.hf_tokenizer.special_tokens_map},\nwhere {list(zip(self.hf_tokenizer.all_special_tokens, self.hf_tokenizer.all_special_ids))}')
        
    @property
    def gmask_token(self):
        return self.hf_tokenizer.gmask_token
    
    @property
    def gmask_token_id(self):
        return self.hf_tokenizer.gmask_token_id
    
    @property
    def null_token(self):
        if self.hf_tokenizer.pad_token != None:
            return self.hf_tokenizer.pad_token
        elif self.hf_tokenizer.unk_token != None:
            return self.hf_tokenizer.unk_token
        else:
            raise ValueError('Missing pad token')
    
    @property
    def end_token(self):
        return self.hf_tokenizer.eos_token
    
    @property
    def unk_token(self):
        return self.hf_tokenizer.unk_token
    
    @property
    def start_token(self):
        return self.hf_tokenizer.bos_token

    @property
    def cls_token(self):
        return self.hf_tokenizer.cls_token
    
    @property
    def null_token_id(self):
        if self.hf_tokenizer.pad_token_id != None:
            return self.hf_tokenizer.pad_token_id
        elif self.hf_tokenizer.unk_token_id != None:
            return self.hf_tokenizer.unk_token_id
        else:
            raise ValueError('Missing pad token')
    
    @property
    def end_token_id(self):
        return self.hf_tokenizer.eos_token_id
    
    @property
    def unk_token_id(self):
        return self.hf_tokenizer.unk_token_id
    
    @property
    def start_token_id(self):
        return self.hf_tokenizer.bos_token_id

    @property
    def cls_token_id(self):
        return self.hf_tokenizer.cls_token_id
    
    
    def override_special_tokens(self):
        pass
        
    def txt2vec(self, text: str, add_special=False):
        # return [token for token in self.hf_tokenizer.encode(text, add_special_tokens=False) if token != self.unk_token_id]
        # text = self.detokenizer.detokenize(text.split())
        return self.hf_tokenizer.encode(text, add_special_tokens=add_special)

    def vec2txt(self, vector: List[int], skip_special=False):
        text = self.hf_tokenizer.decode(vector, skip_special_tokens=skip_special)
        return text

    def add_special_tokens(self, special_tokens):
        self.hf_tokenizer.add_tokens(special_tokens)

    def added_tokens_decoder(self):
        return self.hf_tokenizer.added_tokens_decoder

    def __len__(self):
        return len(self.hf_tokenizer)