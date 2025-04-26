import os
import aiohttp
import json
import sys
import platform

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content

logger = get_logger(__name__)

class CompileTaskPlanner:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        """
        Initialize the TaskPlanner with necessary configurations.

        Args:
            api_key (str): API key for authentication.
            endpoint (str): API endpoint URL.
            deployment_id (str): Deployment ID for the AI model.
            max_tokens (int): Maximum number of tokens for AI responses.
        """
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_task_plan(self, instruction, dependency_files, os_architecture):
        """
        Get a compilation plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for compilation installation planning.
            dependency_files (list): List of dependency-related files in the project.
            os_architecture (str): The operating system and architecture of the target environment.

        Returns:
            dict: compilation installation plan or error reason.
        """
        logger.debug("\n #### `CompileTaskPlanner` is initiating the task planning process")

        all_file_contents = ""
        if dependency_files:
            for file_path in dependency_files:
                if os.path.basename(file_path) in ["pnpm-lock.yaml", "package-lock.json", "yarn.lock", "Gemfile.lock", "Cargo.lock", "poetry.lock"]:
                    all_file_contents += f"\n\nFile: {file_path}:\n[Lock file content omitted due to size]"
                    continue
                
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}:\n{file_content}"


        tree = self.repo.print_tree()
        messages = [
            {
                "role": "system", 
                "content": (
                    f"Create a JSON step-by-step compilation plan for '{self.repo.get_repo_path()}' following pyramid architecture from provided plan.\n"
                    f"User OS: {platform.system()}\n"
                    "Rules:\n"
                    f"1. Start with 'cd' to the appropriate project subdirectory containing package.json or other build configuration files, not just the root directory. For {platform.system()}, " + 
                    ("use backslashes and enclose paths with spaces in double quotes (e.g. cd \"C:\\Program Files\\MyApp\\frontend\")\n" if platform.system() == "Windows" else 
                    "use forward slashes and enclose paths with spaces in single quotes (e.g. cd '/Users/name/My App/frontend')\n") +
                    "2. For all echo commands or similar configuration instructions, use the 'update' method and provide a detailed prompt specifying exactly what content needs to be added, modified, or removed in the file.\n"
                    "3. All 'cd' commands must always be in separate steps, DO NOT combine with other commands.\n"
                    "4. Include only essential steps - no verification or double-checking steps.\n"
                    "Format:\n"
                    "{\n"
                    '    "steps": [\n'
                    '        {\n'
                    '            "file_name": "N/A or full path",\n'
                    f'            "prompt": "Detailed description of exact content to be updated, including specific lines, configurations, or dependencies to be added, modified, or removed.",\n'
                    '            "method": "update or bash",\n'
                    '            "command": "Exact command (for bash only, omit for update method)",\n'
                    '            "is_localhost_command": "0 or 1 (1 for localhost run commands like tauri dev/build, npm run dev, pnpm run that need to stay alive)"\n'
                    '        }\n'
                    '    ]\n'
                    "}\n\n"
                    f"Provide only valid JSON. Include only essential steps needed for compilation. All commands must be compatible with {platform.system()}.\n"
                    "For is_localhost_command: Set to '1' only for commands that run a local development server or build process requiring localhost access (e.g. tauri dev, npm run dev, pnpm run dev).\n"
                    "Set to '0' for all other commands including installation steps.\n"
                    f"CRITICAL: Ensure all paths and commands strictly follow {platform.system()} conventions and syntax. Do not provide commands for other operating systems."
                )
            },
            {
                "role": "user",
                "content": f"Create focused compilation plan with only necessary steps. OS: {os_architecture}. Project tree:\n\n{tree}\n\nDependency files:\n{all_file_contents}\n\nFollow this plan strictly:\n{instruction}\n\n"
            }
        ]

        try:
            logger.debug("Sending request to AI for compilation plan generation")
            response = await self.ai.arch_prompt(messages, 4096, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("Successfully received and parsed AI-generated compilation plan")
            return res
        except json.JSONDecodeError:
            logger.debug("Attempting to repair malformed JSON from AI response")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("Successfully repaired and parsed JSON compilation plan")
            return plan_json
        except Exception as e:
            logger.error(f"Error generating task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction):
        """
        Get development plans based on the user's instruction.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("Beginning task plan retrieval")
        plan = await self.get_task_plan(instruction)
        logger.debug("Successfully retrieved task plan")
        return plan
