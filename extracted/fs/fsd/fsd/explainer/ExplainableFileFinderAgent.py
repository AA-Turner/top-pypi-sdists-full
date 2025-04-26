import os
import json
import sys
import platform
from json_repair import repair_json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)
class ExplainableFileFinderAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_file_planning(self, idea, file_attachments, focused_files):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.

        Returns:
            dict: JSON response with the plan or an empty array if no files are found.
        """

        all_attachment_file_contents = ""

        file_attachments_path = file_attachments

        if file_attachments_path:
            for file_path in file_attachments_path:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {file_path}:\n{file_content}"

        all_focused_files_contents = ""

        all_focused_path = focused_files

        if all_focused_path:
            for file_path in all_focused_path:
                file_content = read_file_content(file_path)
                if file_content:
                    all_focused_files_contents += f"\n\nFile: {file_path}:\n{file_content}"

        all_file_contents = self.repo.print_tree()
        directory_path = self.repo.get_repo_path()
        prompt = (
            f"Analyze the user prompt and project structure to identify ONLY THE MOST CRITICAL files (MAXIMUM 7) needed to answer the user's request. "
            f"Build a JSON response listing files. Include only files that are DIRECTLY related to the user's query and are NOT already in the focused files. "
            f"Provide only a JSON response without any additional text. "
            f"Current working project is {directory_path}. "
            f"User OS: {platform.system()}\n"
            f"Based on the OS above, ensure all file paths use the correct separator:\n"
            f"For {platform.system()}: " + (
                "C:\\Users\\name\\project\\file.txt" if platform.system() == "Windows" 
                else "/Users/name/project/file.txt"
            ) + "\n\n"
            f"Use this JSON format:"
            "{\n"
            f"    \"working_files\": [\"{directory_path}/path/to/relevant_file1.ext\", \"{directory_path}/path/to/relevant_file2.ext\"]\n" 
            "}\n\n"
            "CRITICAL REQUIREMENTS:\n"
            "1. RETURN NO MORE THAN 7 FILES TOTAL - only the most essential ones\n"
            "2. Each file path MUST be a complete absolute path starting with the project directory\n"
            "3. ONLY include files that ACTUALLY EXIST in the given project structure\n"
            "4. NEVER include files already in the focused files list\n"
            "5. EXCLUDE ALL:\n"
            "   - Lock files (package-lock.json, yarn.lock, Podfile.lock, etc)\n"
            "   - Generated folders (node_modules/, build/, dist/, etc)\n"
            "   - Third-party library code files\n"
            "   - Cache directories\n"
            "   - Any files generated after dependency installation\n"
            "6. For dependencies, ONLY include primary manifest files like:\n"
            "   - package.json (NOT package-lock.json)\n"
            "   - Podfile (NOT Podfile.lock)\n"
            "   - requirements.txt\n"
            "   - pom.xml\n"
            "7. ALWAYS include snowx.md in the working_files if it exists in the project\n"
            "8. If the user prompt is not related to the project or code in any meaningful way, return an empty working_files array except for snowx.md:\n"
            "{\n"
            f"    \"working_files\": [\"{directory_path}/snowx.md\"]\n"
            "}\n"
            "9. IMPORTANT: Always use the COMPLETE directory structure when specifying file paths. NEVER skip intermediate directories.\n"
            "   - CORRECT: \"{directory_path}/projectfolder/src/components/Button/index.js\"\n"
            "   - INCORRECT: \"{directory_path}/projectfolder/index.js\"\n"
            "10. Always traverse through ALL subdirectories when specifying paths. Never connect the root directory directly to a deeply nested file.\n"
            "If you don't understand the request or are unsure about file relevance or if the user prompt is not related to the project or code in any meaningful way, return:"
            "{\n"
            f"    \"working_files\": [""]\n"
            "}\n"
        )

        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"This is user request to do:\n{idea}\nThis is the current project context:\n{all_file_contents}"
            }
        ]

        if all_attachment_file_contents:
            messages[-1]["content"] += f"\nUser has attached files for you, from user request and this file, find something the most relevant files from provided tree to answer their question: {all_attachment_file_contents}"

        if all_focused_files_contents:
            messages[-1]["content"] += f"\nFocused files: User has focused on files inside the current project. No need to re-mention files since we already have them: {all_focused_files_contents}"

        try:
            response = await self.ai.prompt(messages, 4096, 0.2, 0.1)
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            return {
                "reason": str(e)
            }

    async def get_file_plannings(self, idea, file_attachments, focused_files):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.
            files (list): List of file paths representing the project structure.

        Returns:
            dict: JSON response with the plan.
        """
        logger.info(f" #### `SnowX` is looking for any relevant context.")
        logger.info("-------------------------------------------------")
        plan = await self.get_file_planning(idea,file_attachments, focused_files)
        logger.debug(f" #### `SnowX`: Successfully completed the search for relevant files")
        return plan
