import asyncio
from matrx_utils import clear_terminal
from matrx_ai.instructions.core import SystemInstruction

clear_terminal()


async def main():
    system_instruction_with_blocks = SystemInstruction(
        intro="You are 'AI MATRX Assistant'. The most advanced & intelligent assistant in the universe.",
        outro="Always think about the user's request carefully and identify what they really want and then think through the best possible response.",
        base_instruction="Test system instruction",
        content_blocks=[
            "flashcards",
            "f5513cf7-e676-4ca7-95c6-0ad38baf580f",
        ],
        tools_list=[
            "get_weather",
            "get_news",
            "get_stock_price",
        ],
    )
    await system_instruction_with_blocks.load_content_blocks()
    print("\n" + "=" * 100 + "\n")
    print(system_instruction_with_blocks)

    # ai_matrix_system_instruction = SystemInstruction.for_ai_matrix()
    # print("\n" + "=" * 100 + "\n")
    # print(ai_matrix_system_instruction)

    # instruction_dict = {
    #     "intro": "You are 'AI MATRX Assistant'. The most advanced & intelligent assistant in the universe.",
    #     "outro": "Always think about the user's request carefully and identify what they really want and then think through the best possible response.",
    #     "base_instruction": "Test system instruction",
    #     "content_blocks": [
    #         "flashcards",
    #         "f5513cf7-e676-4ca7-95c6-0ad38baf580f",
    #     ],
    #     "tools_list": [
    #         "get_weather",
    #         "get_news",
    #         "get_stock_price",
    #         "search_the_web",
    #     ],
    # }
    # system_instruction_from_dict = await SystemInstruction.from_dict(instruction_dict)
    # print("\n" + "=" * 100 + "\n")
    # print(system_instruction_from_dict)

    # instruction_dict = {
    #     "base_instruction": "Test system instruction",
    # }
    # system_instruction_from_dict = await SystemInstruction.from_dict(instruction_dict)
    # print("\n" + "=" * 100 + "\n")
    # print(system_instruction_from_dict)

    instruction_dict = {
        "role": "system",
        "content": "You're a helpful assistant.",
    }
    system_instruction_from_dict = await SystemInstruction.from_dict(instruction_dict)
    print("\n" + "=" * 100)
    print(system_instruction_from_dict)
    print("=" * 100)


if __name__ == "__main__":
    asyncio.run(main())
