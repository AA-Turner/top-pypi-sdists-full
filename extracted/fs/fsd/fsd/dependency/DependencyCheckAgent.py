import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.portkey import AIGateway
from json_repair import repair_json
from log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class DependencyCheckAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_dependency_check_plan(self, user_prompt):
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
                    "Check if the user mentions needing to install any dependencies through CLI tools like npm, pod, pip, pnpm, or similar package managers. Return '0' if no CLI-based dependency installations are mentioned or if it's just code configuration. Return '1' only if CLI-based dependency installations are explicitly mentioned. Respond in this exact JSON format:\n"
                    "{\n"
                    '    "result": "0" or "1"\n'
                    "}"
                )
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        try:
            logger.debug("\n #### `SnowX` is initiating a request to the AI Gateway")
            response = await self.ai.prompt(messages, 4096, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### `SnowX` has successfully parsed the AI response")
            return res
        except json.JSONDecodeError:
            logger.debug("\n #### `SnowX` encountered a JSON decoding error and is attempting to repair it")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### `SnowX` has successfully repaired and parsed the JSON")
            return plan_json
        except Exception as e:
            logger.error(f"  `SnowX` encountered an error during the process: `{e}`")
            return {
                "reason": str(e)
            }

    async def get_dependency_check_plans(self, user_prompt):
        """
        Get development plans for a list of txt files from Azure OpenAI based on the user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### `SnowX` is beginning to retrieve dependency check plans")
        plan = await self.get_dependency_check_plan(user_prompt)
        logger.debug("\n #### `SnowX` has successfully retrieved dependency check plans")
        return plan
