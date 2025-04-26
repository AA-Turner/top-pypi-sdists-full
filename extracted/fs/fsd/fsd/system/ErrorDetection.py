import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class ErrorDetection:
    """
    A class to plan and manage tasks using AI-powered assistance, including error handling and suggestions.
    """

    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self):
        """
        Initialize the conversation with a system prompt and user context.
        """

        system_prompt = (
            "You're a DevOps expert analyzing errors. Determine if it's:\n"
            "1. Code issue (type 1)\n"
            "2. Configuration/dependency issue (type 2)\n" 
            "3. Ambiguous requiring human confirmation (type 3)\n\n"
            "Return JSON:\n"
            "{\n"
            "  'error_type': <1, 2, or 3>,\n"
            "  'error_message': <error info>\n"
            "}\n\n"
            "Type 1 (Code):\n"
            "- Syntax, logic, type errors\n"
            "- Undefined variables/functions\n"
            "- Project-level import errors\n"
            "- Runtime errors\n\n"
            "Type 2 (Config/Dependency):\n"
            "- Missing external dependencies\n"
            "- System configuration issues\n"
            "- Permission/file access errors\n"
            "- Network/database errors\n\n"
            "Type 3 (Ambiguous):\n"
            "- Unclear root cause\n"
            "- Multiple potential causes\n"
            "- Needs more investigation\n\n"
            "Examples:\n"
            "{'error_type': 1, 'error_message': 'SyntaxError: invalid syntax'}\n"
            "{'error_type': 2, 'error_message': 'ImportError: No module named \"requests\"'}\n"
            "{'error_type': 3, 'error_message': 'FileNotFoundError: config.json not found'}"
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
    

    async def get_task_plan(self, error):
        """
        Get a dependency installation plan based on the error, config context, and OS architecture using AI.

        Args:
            error (str): The error message encountered during dependency installation.

        Returns:
            dict: Dependency installation plan or error reason.
        """

        prompt = (
             f"Analyze the following error and determine if it's a code error or a dependency error. Provide a comprehensive explanation and suggested action.\n\n"
             f"Error: {error}\n"
             "Return your analysis in a JSON format with the following structure:\n"
             "{\n"
             "  'error_type': <1, 2, or 3 as an integer (3 if unsure/ambiguous)>,\n"
             "  'error_message': <combined error information as a string>\n"
             "}\n"
             "Provide only the JSON response without additional text or Markdown symbols.\n"
             "Use error_type 3 if:\n"
             "- The error could be either code or dependency related\n"
             "- You are unsure about the root cause\n"
             "- Human investigation is needed to determine the exact issue"
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.prompt(self.conversation_history, 4096, 0.2, 0.1)
            self.remove_latest_conversation()
            res = json.loads(response.choices[0].message.content)
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"ErrorDetection failed to get task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, error):
        """
        Get development plans based on the error, config context, and OS architecture.

        Args:
            error (str): The error message encountered during dependency installation.
            config_context (str): The configuration context of the project.
            os_architecture (str): The operating system and architecture of the target environment.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug(f" #### `ErrorDetection` agent is analyzing the error and generating a task plan")
        plan = await self.get_task_plan(error)
        logger.debug(f" #### `ErrorDetection` agent has completed the error analysis and produced a plan")
        return plan
