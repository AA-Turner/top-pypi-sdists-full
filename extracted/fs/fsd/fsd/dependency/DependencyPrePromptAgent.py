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

class DependencyPrePromptAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_prePrompt_plan(self, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        all_file_contents = self.repo.print_tree()
        messages = [
            {
                "role": "system", 
                "content": (
                    "You are a DevOps expert specializing in dependency management. Analyze the project files and user request, then provide a concise JSON response. Follow these rules:\n\n"
                    "install_plan: Provide detailed dependency installation steps in markdown format. For example:\n"
                    "```bash\n"
                    "# Install required dependencies\n" 
                    "npm install package-name\n"
                    "pip install package-name\n"
                    "```\n"
                    "Translate non-English requests. For pipeline 2, specify the tool (e.g., CocoaPods, npm, pip).\n\n"
                    "pipeline: Choose 0 (do nothing), 1 (need expert help), or 2 (can use CLI).\n"
                    "explainer: For pipeline 1, explain why automatic installation won't work. For pipeline 2, list dependencies, versions, and CLI tool. Use user's language.\n"
                    "JSON format:\n"
                    "{\n"
                    '    "install_plan": "Installation steps with bash commands",\n'
                    '    "pipeline": "0, 1, or 2",\n'
                    '    "explainer": ""\n'
                    "}\n\n"
                    "Ensure proper JSON formatting without extra text. Focus on dependency management."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Project info:\n{all_file_contents}\n\n"
                    f"User request:\n{user_prompt}\n"
                )
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
            logger.error(f"  `SnowX` encountered an error\n Error: {e}")
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
        plan = await self.get_prePrompt_plan(user_prompt)
        return plan
