import json

from cuga.backend.memory.agentic_memory.config import milvus_config
from cuga.backend.memory.agentic_memory.llm.conflict_resolution.schema import SimpleMemory, MemoryEvent
from cuga.backend.memory.agentic_memory.schema import RecordedFact
from cuga.backend.memory.agentic_memory.utils.utils import get_chat_model, clean_llm_response
from langchain_core.prompts import PromptTemplate
from pathlib import Path


def resolve_conflicts(
    old_facts: list[RecordedFact],
    new_facts: list[RecordedFact],
    custom_update_memory_prompt: str | None = None,
) -> list[MemoryEvent]:
    simplified_old_facts = SimpleMemory.from_recorded_facts(old_facts)
    simplified_new_facts = SimpleMemory.from_recorded_facts(new_facts)
    new_facts_by_id = {fact.id: fact for fact in new_facts}

    prompt = get_update_memory_messages(
        simplified_old_facts, simplified_new_facts, custom_update_memory_prompt
    )
    llm = get_chat_model(milvus_config.step_processing)

    caught = None
    for attempt in range(3):
        try:
            response: str = llm.invoke(input=[{"role": "user", "content": prompt}]).content
            response = clean_llm_response(response)
            parsed = json.loads(response)
            memory_events = [MemoryEvent.model_validate(event) for event in parsed['memory']]
            for event in memory_events:
                if event.event == 'ADD':
                    event.metadata = new_facts_by_id[event.id].metadata
            return memory_events
        except Exception as e:
            caught = e
            continue
    raise caught


def get_update_memory_messages(
    old_facts: list['SimpleMemory'],
    new_facts: list['SimpleMemory'],
    custom_update_memory_prompt: str | None = None,
) -> str:
    if custom_update_memory_prompt is None:
        prompt_file = Path(__file__).parent / "prompts/default_conflict_resolution.jinja2"
        failure_analysis_prompt = PromptTemplate.from_file(
            prompt_file, template_format="jinja2", encoding='utf-8'
        )
        custom_update_memory_prompt = failure_analysis_prompt.format()

    prompt_input = {
        "custom_update_memory_prompt": custom_update_memory_prompt,
        "old_facts": json.dumps([fact.model_dump(mode='json') for fact in old_facts], indent=4),
        "new_facts": json.dumps([fact.model_dump(mode='json') for fact in new_facts], indent=4),
    }
    prompt_file = Path(__file__).parent / "prompts/conflict_resolution.jinja2"
    conflict_resolution_prompt = PromptTemplate.from_file(
        prompt_file, template_format="jinja2", encoding='utf-8'
    )
    return conflict_resolution_prompt.format(**prompt_input)
