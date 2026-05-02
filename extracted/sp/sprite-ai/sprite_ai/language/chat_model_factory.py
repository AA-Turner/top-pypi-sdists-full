from langchain.llms.base import LLM
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq


class ChatModelFactory:
    def build(
        self,
        model_name: str,
        context_size: int,
        temperature: float = 0.7,
        url: str = '',
        stop_strings: list[str] | None = None,
        api_key: str = '',
    ) -> LLM:
        if stop_strings is None:
            stop_strings = []

        try:
            prefix_end_position = model_name.index('/')
        except ValueError as e:
            raise ValueError('Missing model backend in model name', e)
        model_name_start_position = prefix_end_position + 1
        model_prefix = model_name[:prefix_end_position]
        model_name = model_name[model_name_start_position:]

        if model_prefix == 'ollama':
            llm = ChatOllama(
                model=model_name,
                num_ctx=context_size,
                temperature=temperature,
                base_url=url,
                stop=stop_strings,
            )
        elif model_prefix == 'openai':
            url = url if url else None
            llm = ChatOpenAI(
                model=model_name,
                max_tokens=context_size,
                temperature=temperature,
                openai_api_key=api_key,
                openai_api_base=url,
            )
        elif model_prefix == 'groq':
            llm = ChatGroq(
                model=model_name,
                max_tokens=context_size,
                temperature=temperature,
                api_key=api_key,
                base_url=url,
            )
        else:
            raise ValueError('Unsuported model type')

        return llm
