import asyncio

from matrx_utils import cleanup_async_resources, clear_terminal, vcprint

from matrx_ai._ext import get_ext
from matrx_ai.agents.definition import Agent

create_test_execution_context = get_ext("create_test_app_context")
initialize = get_ext("initialize")

initialize()
_ctx_token = create_test_execution_context(is_admin=False)


async def direct_news_agent_test():
    """Test: Direct news agent execution"""

    news_agent = await Agent.from_prompt("35461e07-bbd1-46cc-81a7-910850815703")
    news_agent.set_variable("topic", "This news article")

    result = await news_agent.execute(
        user_input=[
            {"type": "input_text", "text": "Here is the article..."},
            {
                "type": "input_image",
                "image_url": "https://cdn.matrxserver.com/test-assets/chat-attachments/sample.png",
            },
        ]
    )

    output = result.output
    print(output)

    return news_agent


async def test_1_basic_execution():
    """Test 1: Basic agent execution"""

    news_agent = await Agent.from_prompt("35461e07-bbd1-46cc-81a7-910850815703")
    news_agent.set_variable("topic", "Recent advances in AI")

    result = await news_agent.execute(
        user_input="Make this extremely concise and to the point",
    )

    output = result.output
    print(output)

    return news_agent


async def test_1B_basic_execution_with_parent_conversation():
    """Test 1B: Basic agent execution with parent conversation tracking."""
    import uuid

    from matrx_ai.context.app_context import (
        clear_app_context,
        get_app_context,
        set_app_context,
    )

    parent_conversation_id = "89dc2516-0598-4fe0-a5a6-6cc9c8274831"

    news_agent = await Agent.from_prompt("35461e07-bbd1-46cc-81a7-910850815703")

    # Fork a child context with parent tracking
    child_ctx = get_app_context().fork_for_child_agent(str(uuid.uuid4()))
    child_ctx = child_ctx.with_overrides(parent_conversation_id=parent_conversation_id)
    child_token = set_app_context(child_ctx)

    try:
        news_agent.set_variable("topic", "Recent advances in AI")
        result = await news_agent.execute(
            user_input="Make this extremely concise and to the point",
        )
    finally:
        clear_app_context(child_token)

    output = result.output
    print(output)

    return news_agent


async def test_2_with_second_message():
    """Test 2: Basic agent execution"""

    news_agent = await Agent.from_prompt("35461e07-bbd1-46cc-81a7-910850815703")
    news_agent.set_variable("topic", "Recent advances in AI")

    result = await news_agent.execute(
        user_input="Make this extremely concise and to the point",
    )

    output = result.output
    print(output)

    print("=" * 50)

    next_result = await news_agent.execute(
        user_input="Can you give me a concise summary of what I absolutely need to know?",
    )
    vcprint(news_agent, "News Agent", color="green")

    output = next_result.output
    print(output)

    return news_agent


async def test_3_with_config_overrides():
    """Test 3: With config overrides"""

    news_agent = await Agent.from_prompt("35461e07-bbd1-46cc-81a7-910850815703")
    news_agent.set_variable("topic", "Recent advances in AI")
    news_agent.apply_config_overrides(
        model="gpt-4.1-mini-2025-04-14",
    )

    result = await news_agent.execute(
        user_input="Make this extremely concise and to the point",
    )

    output = result.output
    print(output)

    print("=" * 50)

    next_result = await news_agent.execute(
        user_input="Can you give me a concise summary of what I absolutely need to know?",
    )
    vcprint(news_agent, "News Agent", color="green")

    output = next_result.output
    print(output)

    return news_agent


async def test_4_clone_with_different_models():
    """Test 4: Clone agent mid-conversation and use different models for parallel branches"""

    print("=" * 80)
    print("TEST 4: Clone Agent with Different Models")
    print("=" * 80)
    print()

    news_agent = await Agent.from_prompt("35461e07-bbd1-46cc-81a7-910850815703")
    news_agent.set_variable("topic", "Recent advances in AI")

    print(f"Original model: {news_agent.config.model}")
    print()

    print("=" * 80)
    print("STEP 1: First call with ORIGINAL model")
    print("=" * 80)
    response_1 = await news_agent.execute(
        user_input="Make this extremely concise and to the point",
    )
    print(f"Model used: {news_agent.config.model}")
    print(response_1.output)
    print()

    print("Cloning agent...")
    news_agent_clone = news_agent.clone()
    news_agent_clone.apply_config_overrides(model="gpt-4.1-mini-2025-04-14")
    print(f"Clone model changed to: {news_agent_clone.config.model}")
    print()

    print("=" * 80)
    print("STEP 2: Second call on ORIGINAL agent (same model)")
    print("=" * 80)
    response_2_original = await news_agent.execute(
        user_input="What are the top 3 things I should know? Very concsise please.",
    )
    print(f"Model used: {news_agent.config.model}")
    print(response_2_original.output)
    print()

    print("=" * 80)
    print("STEP 3: Second call on CLONED agent (different model)")
    print("=" * 80)
    response_2_clone = await news_agent_clone.execute(
        user_input="What are the top 3 things I should know? Very concsise please.",
    )
    print(f"Model used: {news_agent_clone.config.model}")
    print(response_2_clone.output)
    print()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Original agent model: {news_agent.config.model}")
    print(f"Original agent messages: {len(news_agent.config.messages._messages)}")
    print()
    print(f"Cloned agent model: {news_agent_clone.config.model}")
    print(f"Cloned agent messages: {len(news_agent_clone.config.messages._messages)}")
    print()
    print("No spillover - each agent maintains independent state!")

    return {
        "original": news_agent,
        "clone": news_agent_clone,
        "responses": {
            "first": response_1,
            "original_second": response_2_original,
            "clone_second": response_2_clone,
        },
    }


if __name__ == "__main__":
    clear_terminal()
    results = asyncio.run(test_1B_basic_execution_with_parent_conversation())
    vcprint(results, "Results", color="green")

    cleanup_async_resources()
