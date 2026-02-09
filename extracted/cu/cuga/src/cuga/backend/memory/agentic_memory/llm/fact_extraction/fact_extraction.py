import datetime
import json
from cuga.backend.memory.agentic_memory.utils.logging import Logging
from cuga.backend.memory.agentic_memory.utils.utils import get_chat_model, clean_llm_response
from cuga.backend.memory.agentic_memory.config import milvus_config
from cuga.backend.memory.agentic_memory.schema import Message
from langchain_core.prompts import PromptTemplate
from pathlib import Path
from pydantic import BaseModel

messages_tracker = {}
logger = Logging.get_logger()


class ExtractedFacts(BaseModel):
    facts: list[str]


async def extract_facts_from_messages(messages: list[Message]) -> list[str]:
    llm = get_chat_model(milvus_config.fact_extraction)

    filtered_messages = [m.content for m in messages if m.role == 'user']
    messages_str = ""
    for one_msg in filtered_messages:
        messages_str += one_msg
        messages_str += "\n"

    prompt_input = {"datetime": datetime.datetime.now(), "user_messages": messages_str}
    prompt_file = Path(__file__).parent / "prompts/fact_extraction.jinja2"
    failure_analysis_prompt = PromptTemplate.from_file(
        prompt_file, template_format="jinja2", encoding='utf-8'
    )
    formatted_prompt = failure_analysis_prompt.format(**prompt_input)
    response = (await llm.ainvoke(formatted_prompt)).content
    response = clean_llm_response(response)

    caught = None
    for attempt in range(3):
        try:
            extracted_facts = ExtractedFacts.model_validate(json.loads(response))
            return extracted_facts.facts
        except Exception as e:
            caught = e
            continue
    raise caught
