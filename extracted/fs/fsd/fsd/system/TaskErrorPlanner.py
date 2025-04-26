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

class TaskErrorPlanner:
    """
    A class to plan and manage tasks using AI-powered assistance, including error handling and suggestions.
    """

    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_task_plan(self, error, config_context, os_architecture, compile_files):
        """
        Get a dependency installation plan based on the error, config context, and OS architecture using AI.

        Args:
            error (str): The error message encountered during dependency installation.
            config_context (str): The configuration context of the project, including what is being built.
            os_architecture (str): The operating system and architecture of the target environment.
            compile_files (list): List of files to be checked for configuration issues.

        Returns:
            dict: Dependency installation plan or error reason.
        """

        all_file_contents = ""

        files_paths = compile_files

        if files_paths:
            for file_path in files_paths:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}:\n{file_content}"
        else:
            all_file_contents = "No related files found."


        tree = self.repo.print_tree()

        messages = [
            {
                "role": "system", 
                "content": (
                    "As an EXPERT DevOps engineer, create a concise, step-by-step dependency installation/build configuration plan to fix the error. Follow these guidelines:\n\n"
                    f"User OS: {platform.system()}\n"
                    "1. Analyze the error and suggest fixes, but DO NOT include the failed command that caused the error.\n"
                    "2. Organize steps logically, starting with foundational components.\n" 
                    "3. Provide detailed, executable commands ONLY for " + platform.system() + ".\n"
                    "4. Check configuration files for issues.\n"
                    "5. All 'cd' commands must always be in separate steps, DO NOT combine with other commands.\n"
                    "6. For paths with spaces: " + 
                    ("Use backslashes and enclose in double quotes (e.g. cd \"C:\\Program Files\\App\")" if platform.system() == "Windows" else
                    "Use forward slashes and enclose in single quotes (e.g. cd '/path/to/my app')") + "\n"
                    "7. For commands requiring elevated privileges: " +
                    ("Run Command Prompt/PowerShell as Administrator" if platform.system() == "Windows" else
                    "Use sudo before the command") + "\n\n"
                    "For each task, include:\n"
                    f"- file_name: Full path of the config file or 'N/A' for bash commands.\n"
                    "- error_resolution: Specific instruction for the task.\n"
                    "- method: 'update' for file modifications or 'bash' for terminal commands.\n"
                    "- command: Exact command to execute (for 'bash' method only).\n"
                    "Respond with a valid JSON in this format without additional text or symbols or MARKDOWN:\n"
                    "{\n"
                    '    "steps": [\n'
                    '        {\n'
                    '            "file_name": "",\n'
                    '            "method": "",\n'
                    '            "command": "",\n'
                    '            "error_resolution": ""\n'
                    '        }\n'
                    '    ]\n'
                    "}\n\n"
                    "Provide only the JSON response. Do not include the failed command that caused the error - it will NOT be retried automatically after fixes. "
                    "Instead, provide alternative commands that will achieve the same goal as the failed command.\n"
                    f"CRITICAL: All commands MUST be valid and executable on {platform.system()} - do not provide commands for any other OS.\n"
                    "CRITICAL: Each step in the plan must serve a unique purpose - do not include duplicate or similar steps that accomplish the same goal."
                )
            },
            {
                "role": "user",
                "content": f"Create a focused plan to resolve this error:\n\n"
                           f"This is the current project structure:\n{self.repo.get_repo_path()}\n{self.repo.print_summarize_with_tree()}, need to use full path to files in file_name\n"
                           f"1. Config Context: {config_context}\n" 
                           f"2. Error: {error}\n"
                           f"3. OS Architecture: {os_architecture}\n"
                           f"4. Configuration Files:\n{all_file_contents}\n\n"
                           f"Provide specific commands to fix the error AND achieve the original goal. The failed command will NOT be run again, "
                           f"so your plan must include alternative commands that accomplish the same objective.\n"
                           f"Include direct actions like:\n"
                           f"- Add specific missing configurations (e.g. add build script to package.json)\n"
                           f"- Install specific missing dependencies (e.g. npm install package@version)\n"
                           f"- Fix specific configuration issues (e.g. update vite.config.js base path)\n"
                           f"- Provide alternative commands to achieve the original goal\n"
                           f"Each step must serve a unique purpose - do not include duplicate or similar steps.\n"
                           f"Remember, all 'cd' commands must be in separate steps and not combined with other commands.\n"
                           f"All commands MUST be valid for {platform.system()} OS.\n"
                           f"For paths with spaces, " +
                           ("use backslashes and double quotes" if platform.system() == "Windows" else "use forward slashes and single quotes") + ".\n"
                           f"For commands requiring elevated privileges, " +
                           ("run Command Prompt/PowerShell as Administrator" if platform.system() == "Windows" else "use sudo before the command") + ".\n"
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
            logger.error(f"  `TaskErrorPlanner` agent encountered an error:\n Failed to get task plan\n Error: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, error, config_context, os_architecture, compile_files):
        """
        Get development plans based on the error, config context, and OS architecture.

        Args:
            error (str): The error message encountered during dependency installation.
            config_context (str): The configuration context of the project.
            os_architecture (str): The operating system and architecture of the target environment.

        Returns:
            dict: Development plan or error reason.
        """
        plan = await self.get_task_plan(error, config_context, os_architecture, compile_files)
        return plan
