import os
import asyncio
from jinja2 import Environment, FileSystemLoader


env = Environment(
    loader=FileSystemLoader(os.path.dirname(__file__)),
    enable_async=True,
)

_template_cache = {}


async def init_templates():
    template_files = ['spreadsheet_act_sysetm_prompt']
    for template_name in template_files:
        _template_cache[template_name] = env.get_template(f"{template_name}.md")


async def get_rendered_template(prompt_name: str, args: dict = {}) -> str:
    try:
        template = _template_cache.get(prompt_name)
        if not template:
            template = await asyncio.to_thread(env.get_template, f"{prompt_name}.md")
        prompt = await template.render_async(args)
        return prompt
    except Exception as e:
        raise ValueError(f"Error in applying prompt template {prompt_name}: {e}")
