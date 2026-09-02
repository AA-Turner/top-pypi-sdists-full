import asyncio

from matrx_utils import clear_terminal, vcprint

from matrx_ai.agents.DEPRECATED_prompts_manager import pm


async def load_prompt_by_id(prompt_id: str):
    prompt = await pm.load_prompt(prompt_id)
    return prompt


async def load_prompt_by_name(prompt_name: str):
    prompts = await pm.find_prompts(name=prompt_name)
    return prompts[0] if prompts else None


async def load_prompt_by_user_id(user_id: str):
    return await pm.find_prompts(user_id=user_id)


if __name__ == "__main__":
    clear_terminal()
    prompt_id = "7817c1bc-297c-4a3d-b294-8887ca396749"
    prompt = asyncio.run(load_prompt_by_id(prompt_id))
    vcprint(prompt, "Prompt", color="green")

    defaults = prompt.variable_defaults
    for default in defaults:
        name = default["name"]
        default_value = default["defaultValue"]
        vcprint("\n\n", color="yellow")
        vcprint(f"Variable Name: {name}", color="yellow")
        print(default_value)
