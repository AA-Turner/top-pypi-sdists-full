import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class BugTaskPlanner:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        """
        Initialize the TaskPlanner with necessary configurations.

        Args:
            directory_path (str): Path to the project directory.
            api_key (str): API key for authentication.
            endpoint (str): API endpoint URL.
            deployment_id (str): Deployment ID for the AI model.
            max_tokens (int): Maximum number of tokens for AI responses.
        """
        self.max_tokens = 4096
        self.repo = repo
        self.ai = AIGateway()

    async def get_task_plan(self, instruction, file_list):
        """
        Get a development plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for task planning.
            file_list (list): List of available files.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### `TaskPlanner` is initiating the process to generate a task plan")
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a principal engineer specializing in bug fixing and code quality. Generate an ordered list of tasks for implementing bug fixes based on the user's instruction and provided file list.\n\n"
                    "Guidelines:\n"
                    "1. MUST Only include files from the provided 'file_list' for all task, no exception.\n"
                    "2. Follow dependency order:\n"
                    "   - Utility/Helper functions first\n" 
                    "   - Base components second\n"
                    "   - Services and middleware third\n"
                    "   - Main application components last\n"
                    "3. Fix bugs in priority order:\n"
                    "   - Critical system crashes\n"
                    "   - Security vulnerabilities\n" 
                    "   - Data integrity issues\n"
                    "   - Performance issues\n"
                    "   - UI/UX defects\n"
                    "4. Follow dependency chain:\n"
                    "   - Fix foundational bugs before dependent ones\n"
                    "   - Fix shared components before specific ones\n"
                    "5. Each file appears only once in the entire plan\n"
                    "6. Provide `file_name` (full path) for each task\n"
                    "7. Generate a commit message using format: bugfix(scope): <description>\n"
                    "Response Format:\n"
                    "{\n"
                    '    "steps": [\n'
                    '        {\n'
                    '            "file_name": "/full/path/to/file",\n'
                    '        }\n'
                    '    ],\n'
                    '    "commits": ""\n'
                    "}\n\n"
                    "Return only valid JSON without additional text or formatting."
                )
            },
            {
                "role": "user",
                "content": f"Create an ordered list of tasks for bug fixing. Only select files from this list:\n{file_list} - MUST Only include files from the provided 'file_list' for all task in correct path, no exception.\n\nInclude `file_name` (full path from {self.repo.get_repo_path()}) for each task in JSON format. Ensure correct paths. Follow the implementation order from the original instruction strictly. Original instruction: {instruction}\n\n"
            }
        ]

        try:
            response = await self.ai.arch_prompt(messages, 4096, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### `TaskPlanner` has successfully generated the task plan")
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### `TaskPlanner` has repaired and processed the JSON response")
            return plan_json
        except Exception as e:
            logger.error(f"  `TaskPlanner` encountered an error while generating the task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction, file_lists):
        """
        Get development plans based on the user's instruction.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### `TaskPlanner` is generating task plans")
        plan = await self.get_task_plan(instruction, file_lists)
        logger.debug("\n #### `TaskPlanner` has completed generating the task plans")
        return plan