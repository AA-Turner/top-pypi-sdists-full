import os
import aiohttp
import asyncio
import json
import sys

from json_repair import repair_json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class CompilePrePromptAgent:
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
                    "You're an expert in project compilation and local development. Analyze the files and prompt, then respond in JSON format:\n\n"
                    "compile_plan: Refine the user's prompt, focusing on local setup and execution. Translate if needed. Enhance with project-specific insights. NO YAPPING OR UNNECESSARY EXPLANATIONS. Exclude any mentions or questions about AI models.\n"
                    "pipeline: Choose the best action (0, 1, or 2):\n"
                    "0. No setup needed (empty project or no executable code)\n"
                    "1. CLI setup possible (e.g., `npm start`, `python manage.py runserver`)\n"
                    "Respond in this JSON structure:\n"
                    "{\n"
                    '    "compile_plan": "Enhanced directive focusing on local setup",\n'
                    '    "pipeline": "0, 1"\n'
                    "}\n"
                    "Provide only valid JSON without additional text or symbols or MARKDOWN. Prioritize local development unless deployment is explicitly requested. STRICTLY ENFORCE no yapping in the response. Use markdown code blocks with 'bash' syntax highlighting for ALL bash commands in the compile_plan, e.g.:\n"
                    "```bash\n"
                    "npm install\n"
                    "npm start\n"
                    "```"
                )
            },
            {
                "role": "user",
                "content": (
                    f"Project structure:\n{all_file_contents}\n\n"
                    f"User directive:\n{user_prompt}\n"
                )
            }
        ]

        try:
            logger.debug("Sending request to AI for plan generation")
            response = await self.ai.prompt(messages, 4096, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("AI response received and parsed successfully")
            return res
        except json.JSONDecodeError:
            logger.debug("JSON decoding error encountered, attempting to repair response")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("JSON response repaired and parsed successfully")
            return plan_json
        except Exception as e:
            logger.error(f"Error encountered during plan generation: {e}")
            return {
                "reason": str(e)
            }

    async def get_prePrompt_plans(self, user_prompt):
        plan = await self.get_prePrompt_plan(user_prompt)
        logger.debug("Pre-prompt plans retrieved successfully")
        return plan
