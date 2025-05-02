import unittest
from transformers import BertTokenizer, BertModel, T5Tokenizer, T5Model, AutoTokenizer, AutoModelForCausalLM
from config import *
class TestModelLoading(unittest.TestCase):
    def test_load_model(self):

        params = get_prompt_fine_tuning()
        model_name = params["model-name"]
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.assertTrue(tokenizer)
        self.assertTrue(model)