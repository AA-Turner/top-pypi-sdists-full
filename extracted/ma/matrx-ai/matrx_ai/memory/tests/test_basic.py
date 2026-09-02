import asyncio
from datetime import datetime

from matrx_ai.memory import (
    Message,
    MessageRole,
    InMemoryStorage,
    ObservationalMemory,
    ObservationalMemoryConfig,
    ObservationConfig,
    ReflectionConfig,
)

async def dummy_llm_call(model, messages, temperature, max_tokens):
    """A dummy LLM that just returns a fixed XML structure."""
    if "Extract observations" in messages[-1]["content"]:
        return """
<observations>
Date: Dec 4, 2025
* 🔴 (14:30) User stated they prefer Python
* ✅ Completed basic test
</observations>
<current-task>
Testing the python OM port
</current-task>
<suggested-response>
Say hello to the user
</suggested-response>
"""
    else:
        # Reflector
        return """
<observations>
Date: Dec 4, 2025
* 🔴 User prefers Python
* ✅ Basic test done
</observations>
"""

def count_tokens(text: str) -> int:
    return len(text) // 4  # Rough approximation

async def test_om():
    storage = InMemoryStorage()
    
    config = ObservationalMemoryConfig(
        observation=ObservationConfig(token_threshold=50), # small threshold for testing
        reflection=ReflectionConfig(token_threshold=100)
    )
    
    om = ObservationalMemory(
        config=config,
        storage=storage,
        count_tokens_fn=count_tokens,
        llm_call_fn=dummy_llm_call
    )
    
    thread_id = "test-thread"
    resource_id = "test-user"
    
    # 1. Create some messages
    messages = [
        Message(
            id="1", 
            thread_id=thread_id, 
            resource_id=resource_id, 
            role=MessageRole.USER, 
            content="Hello, I prefer Python.",
            created_at=datetime.utcnow()
        ),
        Message(
            id="2", 
            thread_id=thread_id, 
            resource_id=resource_id, 
            role=MessageRole.ASSISTANT, 
            content="Great! I will remember that. " * 10, # Make it long enough to trigger threshold
            created_at=datetime.utcnow()
        )
    ]
    
    # 2. process_output_step (should trigger observer)
    await om.process_output_step(messages, thread_id, resource_id)
    
    # Check storage
    record = await storage.get_record(resource_id, thread_id, config.scope)
    assert record is not None
    assert "User stated they prefer Python" in record.active_observations
    assert record.current_task == "Testing the python OM port"
    
    print("Test passed! Observer was triggered and storage updated.")
    
    # 3. Next turn, process_input_step should inject the OM context
    new_messages = [
        Message(
            id="3", 
            thread_id=thread_id, 
            resource_id=resource_id, 
            role=MessageRole.USER, 
            content="What language do I prefer?",
            created_at=datetime.utcnow()
        )
    ]
    
    injected_messages = await om.process_input_step(new_messages, thread_id, resource_id)
    
    assert len(injected_messages) == 2
    assert injected_messages[0].role == MessageRole.SYSTEM
    print(f"Injected context:\\n{injected_messages[0].content}")
    assert "User stated they prefer Python" in injected_messages[0].content
    
    print("Test passed! Context was properly injected into the prompt.")

if __name__ == "__main__":
    asyncio.run(test_om())
