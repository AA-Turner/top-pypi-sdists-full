import os
import aiohttp
import json
import sys
import platform

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.util.utils import read_file_content
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class DependencyTaskPlanner:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_task_plan(self, instruction, dependency_files, os_architecture):
        """
        Get a dependency installation plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for dependency installation planning.
            dependency_files (list): List of dependency-related files in the project to determine tech stack.
            os_architecture (str): The operating system and architecture of the target environment.

        Returns:
            dict: Dependency installation plan or error reason.
        """
        logger.debug("\n #### `DependencyTaskPlanner` is initiating the task planning process")

        all_file_contents = ""
        if dependency_files:
            for file_path in dependency_files:
                # Skip large lock files
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
                    f"Create a JSON step-by-step dependency installation plan for '{self.repo.get_repo_path()}' focusing ONLY on installing the specific dependencies requested by the user.\n"
                    f"User OS: {platform.system()}\n"
                    "Rules:\n"
                    f"1. Start with 'cd' to the appropriate project subdirectory containing package.json or other build configuration files, not just the root directory. For {platform.system()}, " + 
                    ("use backslashes and enclose paths with spaces in double quotes (e.g. cd \"C:\\Program Files\\MyApp\\frontend\")\n" if platform.system() == "Windows" else 
                    "use forward slashes and enclose paths with spaces in single quotes (e.g. cd '/Users/name/My App/frontend')\n") +
                    "2. Analyze dependency files to determine the correct package manager (npm, pnpm, pip, etc.) already in use.\n"
                    "3. DO NOT introduce new package managers not already configured in the project.\n"
                    "4. For all echo commands or similar configuration instructions, use the 'update' method and provide a detailed prompt specifying exactly what content needs to be added, modified, or removed in the file.\n" 
                    "5. All 'cd' commands must always be in separate steps, DO NOT combine with other commands.\n"
                    "6. Include only essential steps for installing the EXACT dependencies specified in the user's instruction.\n"
                    "7. Only Set is_localhost_command to '1' only for commands that start a local development server or build process that needs to stay running (e.g. npm run dev, tauri dev). Set to '0' for all other commands including installations.\n"
                    "8. Generate a commit message for specific work. The commit message must use the imperative tense and be structured as follows: <type>: <description>. Use these for <type>: bugfix, feature, optimize, update, config, document, format, restructure, enhance, verify. The commit message should be a single line.\n"
                    "9. STRICTLY focus on installing only the exact dependencies requested by user - nothing more, nothing less.\n"
                    "10. NEVER include ambiguous version numbers like x.x.x in dependency specifications.\n"
                    "11. If the user specifies version requirements (e.g., 'react@18.2.0' or 'lodash latest version'), follow those requirements exactly.\n"
                    "12. Keep commands simple and direct - avoid unnecessary complexity or overkill commands.\n"
                    "Format:\n"
                    "{\n"
                    '    "steps": [\n'
                    '        {\n'
                    '            "file_name": "N/A or full path",\n'
                    '            "prompt": "Detailed description of exact content to be updated, including specific lines, configurations, or dependencies to be added, modified, or removed.",\n'
                    '            "method": "update or bash",\n'
                    '            "command": "Exact command (for bash only, omit for update method)",\n'
                    '            "is_localhost_command": "0 or 1 (1 only for local dev server commands that need to stay running)"\n'
                    '        }\n'
                    '    ],\n'
                    '    "commits": ""\n'
                    "}\n\n"
                    f"Provide only valid JSON. No additional text or Markdown. Include only essential steps. All commands must be compatible with {platform.system()} - do not provide commands for other operating systems. For paths with spaces use " +
                    ("double quotes and backslashes (e.g. \"C:\\Program Files\\App\")" if platform.system() == "Windows" else 
                    "single quotes and forward slashes (e.g. '/path/to/my app')")
                )
            },
            {
                "role": "user",
                "content": f"Create dependency installation plan for ONLY the specific dependencies mentioned in my instructions. OS: {os_architecture}. Project structure:'{self.repo.get_repo_path()}'\n{tree}\n\nDependency files:\n{all_file_contents}\n\nFollow dependency installation plan strictly:\n{instruction}"
            }
        ]

        try:
            logger.debug("\n #### `DependencyTaskPlanner` is dispatching a request to the AI for task planning")
            response = await self.ai.arch_prompt(messages, 4096, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### `DependencyTaskPlanner` has successfully obtained and parsed the AI response")
            return res
        except json.JSONDecodeError:
            logger.debug("\n #### `DependencyTaskPlanner` encountered a JSON decoding error and is attempting to repair it")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"  `DependencyTaskPlanner` encountered an error while retrieving the task plan:\n Error: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction):
        logger.debug("\n #### `DependencyTaskPlanner` is commencing the retrieval of task plans")
        plan = await self.get_task_plan(instruction, [], platform.system())
        logger.debug("\n #### `DependencyTaskPlanner` has finalized the retrieval of task plans")
        return plan
