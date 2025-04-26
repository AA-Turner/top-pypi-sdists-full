import os
import aiohttp
import asyncio
import json
import sys
from json_repair import repair_json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class ContextBugAgent:
    def __init__(self, repo):
        """
        Initialize the ContextBugAgent with the repository.

        Args:
            repo: The repository object containing project information.
        """
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_file_planning(self, bugs):
        """
        Request file planning from AI for fixing bugs.

        Args:
            bugs (str): The bug logs and error messages to analyze.

        Returns:
            dict: JSON response with the plan including working files needed to fix the bugs.
        """
        logger.debug("\n #### Context bug agent is initiating file planning process")
        prompt = (
            "Based on the provided bug logs and project structure, create a JSON response with a 'working_files' list containing the most relevant files needed to fix the bugs. "
            "The response should:"
            "1. Include only files that exist in the project structure and are directly related to fixing the bugs (max 5 files)"
            "2. Use complete file paths from the project root, matching exactly as they appear in the structure"
            "3. Exclude third-party libraries, generated files, and dependency folders (node_modules/, build/, etc.)"
            "4. Only include primary manifest files like package.json, pom.xml if directly relevant"
            "5. Prioritize files mentioned in error messages, containing bug-related code, or critically needed for fixes"
            "Return an empty list if no relevant files are found."
            "Use this JSON format:"
            "{\n"
            "    \"working_files\": [\"/absolute/path/to/project/root/folder1/subfolder/file1.extension\", \"/absolute/path/to/project/root/folder2/file2.extension\"],\n"
            "}\n\n"
            "If the list is empty, return:"
            "{\n"
            "    \"working_files\": [],\n"
            "}\n\n"
            "Return only valid JSON without Markdown symbols or invalid escapes."
        )

        messages = [
            {
                "role": "system", 
                "content": prompt
            },
            {
                "role": "user",
                "content": f"These are the bug logs to analyze:\n{bugs}\nThis is the current project structure:\n{self.repo.get_repo_path()}\n{self.repo.print_summarize_with_tree()}\n"
            }
        ]

        try:
            logger.debug("\n #### Context bug agent is sending request to AI for file planning")
            response = await self.ai.prompt(messages, 4096, 0.2, 0.1)
            logger.debug("\n #### Context bug agent has received response from AI")
            plan_json = json.loads(response.choices[0].message.content)
            
            # Ensure working_files list exists and contains only unique elements
            plan_json["working_files"] = list(set(plan_json.get("working_files", [])))
            
            return plan_json
        except json.JSONDecodeError:
            logger.debug("\n #### Context bug agent encountered JSON decode error, attempting repair")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"  Context bug agent encountered an error: `{e}`")
            return {
                "working_files": [],
                "reason": str(e)
            }

    async def get_file_plannings(self, bugs):
        logger.debug("\n #### Context bug agent is starting file planning process")
        return await self.get_file_planning(bugs)
