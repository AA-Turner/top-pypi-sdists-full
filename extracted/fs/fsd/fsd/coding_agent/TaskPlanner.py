import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class TaskPlanner:
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
        logger.debug("\n #### The `TaskPlanner` is initiating the process to generate a task plan")
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a principal engineer specializing in Pyramid architecture. Generate an ordered list of tasks for implementing a system based on the user's instruction and provided file list.\n\n"
                    "Guidelines:\n"
                    "1. MUST Only include files from the provided 'file_list' for all task, no exception.\n"
                    "2. Follow Pyramid architecture principles:\n"
                    "   - Foundation layers (data models, core utilities) must precede higher layers\n"
                    "   - Business logic layer depends on foundation layer\n"
                    "   - Presentation layer depends on business logic layer\n"
                    "   - Example: database schema → data models → services → controllers → views\n"
                    "3. Apply lead-follow principle across tech stacks:\n"
                    "   - Place lead file of each stack in its own early group to establish patterns\n" 
                    "   - Group follower files that can be executed concurrently\n"
                    "   - Example: Place 'UserModel.js' before 'ProductModel.js' and 'OrderModel.js'\n"
                    "4. Implement in the EXACT order specified in the original instruction. This takes precedence over architectural principles.\n"
                    "5. Omit configuration, dependencies, and non-essential files.\n"
                    "6. Each file appears only once in the entire plan\n"
                    "7. Provide `file_name` (full path) for each task\n"
                    "8. Generate a commit message using format: <type>: <description>\n"
                    "   Types: bugfix, feature, optimize, update, config, document, format, restructure, enhance, verify\n"
                    "   Example: 'feature: implement user authentication system'\n"
                    "9. Always implement smaller components first before main components:\n"
                    "   - Smaller, self-contained utilities and helpers should precede larger components\n"
                    "   - This makes integration easier and allows for incremental testing\n"
                    "   - Example: implement utility functions before the classes that use them\n"
                    "10. Exclude all image files except `.svg` and all audio asset files.\n"
                    "Response Format:\n"
                    "{\n"
                    '    "steps": [\n'
                    '        {\n'
                    '            "file_name": "/full/path/to/file",\n'
                    '        }\n'
                    '    ],\n'
                    '    "commits": ""\n'
                    "}\n\n"
                    f"Current working project is {self.repo.get_repo_path()}\n\n"
                    "Return only valid JSON without additional text or formatting."
                )
            },
            {
                "role": "user",
                "content": f"Create an ordered list of tasks following the EXACT order specified in the original instruction. Only select files from this list:\n{file_list} - MUST Only include files from the provided 'file_list' for all task, no exception.\n\nInclude `file_name` (full path) and `techStack` for each task in JSON format. Ensure correct paths. Follow the implementation order from the original instruction strictly. Original instruction: {instruction}\n\n"
            }
        ]

        try:
            response = await self.ai.arch_prompt(messages, 4096, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### The `TaskPlanner` has successfully generated the task plan")
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### The `TaskPlanner` has repaired and processed the JSON response")
            return plan_json
        except Exception as e:
            logger.error(f"  The `TaskPlanner` encountered an error while generating the task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction, file_lists):
        """
        Get development plans based on the user's instruction.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `TaskPlanner` is generating task plans")
        plan = await self.get_task_plan(instruction, file_lists)
        logger.debug("\n #### The `TaskPlanner` has completed generating the task plans")
        return plan