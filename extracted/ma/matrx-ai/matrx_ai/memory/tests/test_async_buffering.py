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
from matrx_ai.memory.buffering_coordinator import BufferingCoordinator

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

async def test_buffering():
    storage = InMemoryStorage()
    
    config = ObservationalMemoryConfig(
        observation=ObservationConfig(
            token_threshold=100, 
            buffer_tokens=20 # Buffer when we hit 20 unobserved tokens
        ),
        reflection=ReflectionConfig(
            token_threshold=200,
            buffer_activation=0.5 # Buffer when we hit 100 observation tokens
        )
    )
    
    om = ObservationalMemory(
        config=config,
        storage=storage,
        count_tokens_fn=count_tokens,
        llm_call_fn=dummy_llm_call
    )
    
    thread_id = "test-buffer-thread"
    resource_id = "test-user"
    
    # 1. Create messages that hit buffer_tokens but NOT token_threshold
    messages = [
        Message(
            id="1", 
            thread_id=thread_id, 
            resource_id=resource_id, 
            role=MessageRole.USER, 
            content="Hello, this message is long enough to trigger background buffering but not long enough to trigger full sync observation. Let's see if we get a background task created.",
            created_at=datetime.utcnow()
        )
    ]
    
    # Process output
    await om.process_output_step(messages, thread_id, resource_id)
    
    # Verify that a background task was created
    lock_key = om.buffering.get_lock_key(thread_id, resource_id)
    obs_key = om.buffering.get_observation_buffer_key(lock_key)
    
    # wait a bit for async tasks to run if they are pending
    await asyncio.sleep(0.1)
    
    # We should have buffered chunks in DB
    record = await storage.get_record(resource_id, thread_id, config.scope)
    assert record is not None
    assert len(record.buffered_observations) == 1
    assert "User stated they prefer Python" in record.buffered_observations[0].observations
    
    # And active observations should still be empty
    assert not record.active_observations
    
    print("Test passed! Background task ran and created buffered chunks.")
    
    # Now let's trigger a sync observation by passing the threshold
    messages.append(
        Message(
            id="2", 
            thread_id=thread_id, 
            resource_id=resource_id, 
            role=MessageRole.ASSISTANT, 
            content="Long response " * 100,
            created_at=datetime.utcnow()
        )
    )
    
    await om.process_output_step(messages, thread_id, resource_id)
    
    # Wait for tasks
    await asyncio.sleep(0.1)
    
    record = await storage.get_record(resource_id, thread_id, config.scope)
    
    # Buffered should have been merged and cleared
    assert len(record.buffered_observations) == 0
    assert "User stated they prefer Python" in record.active_observations
    
    print("Test passed! Buffered chunks were activated into active_observations.")

if __name__ == "__main__":
    asyncio.run(test_buffering())
