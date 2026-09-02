from matrx_utils import clear_terminal, vcprint

from matrx_ai._ext import get_ext
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.providers import UnifiedAIClient

create_test_execution_context = get_ext("create_test_execution_context")


async def test_translation(settings_to_use):
    client = UnifiedAIClient()
    request = AIMatrixRequest.from_dict(settings_to_use)
    formatted_request = await client.translate_request(request)
    vcprint(formatted_request, "Formatted Request", color="blue")


async def test_execution(settings_to_use):
    client = UnifiedAIClient()
    request = AIMatrixRequest.from_dict(settings_to_use)
    response = await client.execute(request)
    vcprint(response, "Response", color="blue")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    import asyncio

    initialize_for_tools = False

    if initialize_for_tools:
        initialize = get_ext("initialize")

        initialize()

    _ctx_token = create_test_execution_context(is_admin=False)

    clear_terminal()

    model_1 = "gpt-5"
    model_2 = "gemini-3-flash-preview"
    model_3 = "548126f2-714a-4562-9001-0c31cbeea375"
    model_4 = "gemini-3-pro-image-preview"
    model_5 = "gpt-5-mini"

    minimal_settings = {
        "ai_model_id": model_2,
        "conversation_id": "12345678-1234-1234-1234-123456789012",
        "user_id": "12345678-1234-1234-1234-123456789012",
        "debug": True,
        "config": {
            "max_output_tokens": 4444,
            "reasoning_effort": "high",
            "reasoning_summary": "always",
            "tools": [
                # "get_location",
                # "get_weather",
                # "get_restaurants",
                # "get_activities",
                # "get_events",
                # "create_summary",
            ],
            "tool_choice": "auto",
            "messages": [
                {
                    "role": "system",
                    "content": "You're a helpful assistant. Think through your response step by step and use the many tools you have available to you.",
                },
                {
                    "role": "user",
                    "content": "Hello! Can you give me some recommendations for today?",
                },
            ],
        },
    }

    complex_settings = {
        "ai_model_id": model_2,
        "conversation_id": "12345678-1234-1234-1234-123456789012",
        "user_id": "12345678-1234-1234-1234-123456789012",
        "debug": True,
        "config": {
            "system_instruction": "You're a helpful assistant.",
            "messages": [
                {
                    "role": "system",
                    "content": "SYSTEM MESSAGE - You're a helpful assistant. Think through your response step by step before proceeding with a response. Always search the web to ensure you include recent and relevant facts in your response. You can check the user's location with a tool and provide whatever they need.",
                },
                {
                    "role": "developer",
                    "content": "DEVELOPER MESSAGE - This should not get through",
                },
                {
                    "role": "user",
                    "content": "Hello! Can you help me? What is the latest us news?",
                },
            ],
            "temperature": 1,
            "max_output_tokens": 5555,
            "top_p": 1,
            "top_k": 50,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stream": True,
            "response_format": "text",
            "store": True,
            "stop_sequences": ["STOP"],
            "tools": [
                # "get_location",
                # "get_weather",
                # "get_restaurants",
                # "get_activities",
                # "get_events",
                # "create_summary",
            ],
            "tool_choice": "auto",
            "parallel_tool_calls": False,
            "image_urls": False,
            "file_urls": False,
            "internal_web_search": True,
            "youtube_videos": False,
            "size": "1024x1024",
            "quality": "standard",
            "count": 1,
            "tts_voice": "alloy",
            "audio_format": "mp3",
            "reasoning_effort": "low",
            "verbosity": "medium",
            "reasoning_summary": "auto",
            "modalities": {},
            "preset_name": "default",
            "system_message_override": None,
            "reasoning": {},
        },
    }

    settings_to_use = complex_settings

    asyncio.run(test_translation(settings_to_use))
