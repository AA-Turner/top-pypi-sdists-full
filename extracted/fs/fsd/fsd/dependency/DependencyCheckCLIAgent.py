import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.portkey import AIGateway
from json_repair import repair_json
from fsd.util.utils import read_file_content
from log.logger_config import get_logger
logger = get_logger(__name__)

class DependencyCheckCLIAgent:
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
                    "Analyze the user's request for dependency installation. If the request can be fulfilled using CLI commands, respond with 'Got it!'. If the request requires IDE manipulation or cannot be done through CLI, must always respond with 'Hi, I am sorry about...' followed by a brief explanation."
                )
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        response = await self.ai.stream_prompt(messages, 4096, 0.2, 0.1)
        return response

    async def get_dependency_check_plans(self, user_prompt):
        """
        Get development plans for a list of txt files from Azure OpenAI based on the user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug(f" #### `SnowX` is initiating the dependency check plan generation\n User prompt: {user_prompt}")
        plan = await self.get_dependency_check_plan(user_prompt)
        logger.debug(f" #### `SnowX` has completed generating the dependency check plan")
        return plan
