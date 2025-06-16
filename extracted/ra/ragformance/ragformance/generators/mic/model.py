from typing import Optional

from transformers import AutoModelForCausalLM, AutoTokenizer


class LLM:
    def __init__(self, model_name: str, system_prompt: Optional[str] = None) -> None:
        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.system_prompt = system_prompt

    def set_system_prompt(self, system_prompt: str) -> None:
        self.system_prompt = system_prompt

    def generate(self, queries: list[str]) -> list[str]:
        sytem_prompts_message = (
            []
            if self.system_prompt is None
            else [{"role": "system", "content": self.system_prompt}]
        )
        batch_messages = [
            [{"role": "user", "content": query}] + sytem_prompts_message
            for query in queries
        ]

        batch_text = [
            self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            for messages in batch_messages
        ]

        model_inputs = self.tokenizer(batch_text, return_tensors="pt", padding=True).to(
            self.model.device
        )
        input_length = model_inputs["input_ids"].shape[1]
        generated_ids = self.model.generate(**model_inputs, max_new_tokens=512)

        responses = self.tokenizer.batch_decode(
            generated_ids[:, input_length:], skip_special_tokens=True
        )

        return responses
