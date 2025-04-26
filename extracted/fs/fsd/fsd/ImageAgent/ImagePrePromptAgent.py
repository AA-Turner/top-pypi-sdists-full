import os
import aiohttp
import asyncio
import json
import sys

from json_repair import repair_json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class CompilePrePromptAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_prePrompt_plan(self, all_file_contents, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You're an image generation specialist. Process requests for PNG, JPG, JPEG, png, jpg, jpeg formats only, excluding SVG. Respond in JSON:\n\n"
                    "processed_prompt: For supported formats, extract:\n"
                    "- Save path\n"
                    "- Name\n"
                    "- Dimension\n"
                    "- Description\n"
                    "Combine all image details into one string, separated by newlines. Translate non-English prompts. NO YAPPING OR UNNECESSARY EXPLANATIONS.\n"
                    "pipeline: \"0\" for unsupported/no request, \"1\" for supported.\n\n"
                    "JSON structure:\n"
                    "{\n"
                    '    "processed_prompt": "Path: [path], Name: [name], Dimension: [WxH], Description: [desc]\n..." (only if pipeline is "1", otherwise ""),\n'
                    '    "pipeline": "0" or "1"\n'
                    "}\n\n"
                    "Strict JSON only. Any unsupported format (including SVG) mention results in pipeline \"0\" and empty processed_prompt. STRICTLY ENFORCE no yapping in the response."
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{all_file_contents}\n\nDirective:\n{user_prompt}\n"
            }
        ]

        try:
            response = await self.ai.prompt(messages, 4096, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"  `SnowX` encountered an error: `{e}`")
            return {
                "reason": str(e)
            }

    async def get_prePrompt_plans(self, user_prompt):
        """
        Get development plans for a list of txt files from Azure OpenAI based on the user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### `SnowX` is initiating the pre-prompt planning process")
        all_file_contents = self.repo.print_tree()
        plan = await self.get_prePrompt_plan(all_file_contents, user_prompt)
        logger.debug(f" #### `SnowX` has completed the pre-prompt planning: `{plan}`")
        return plan
