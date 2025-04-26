import os
import aiohttp
import asyncio
import json
import sys
import platform

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
logger = get_logger(__name__)

class CompileProjectAnalysAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        logger.debug("Conversation history cleared by CompileProjectAnalysAgent")

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()
            logger.debug("Latest conversation entry removed by CompileProjectAnalysAgent")

    def initial_setup(self, dependency_files, OS_architecture):
        """
        Initialize the conversation with a system prompt and user context.
        """
        logger.debug("CompileProjectAnalysAgent initializing conversation setup")

        tree_contents = self.repo.print_tree()

        dependency_files_path = dependency_files

        all_file_contents = ""
        if dependency_files_path:
            for file_path in dependency_files_path:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}:\n{file_content}"
        else:
            all_file_contents = "No dependency files found."

        system_prompt = (
            f"You are an EXPERT DevOps engineer. Analyze the project structure and develop a concise plan for setting up and compiling the project for local development using CLI commands. Follow these guidelines:\n\n"
            f"User OS: {platform.system()}\n"
            "- Respect and use existing conventions, libraries, etc. that are already present in the code base.\n"
            f"Working directory: {self.repo.get_repo_path()}\n"
            "1. Provide a SHORT TITLE for the setup process.\n"
            "2. ANALYZE the project structure.\n"
            "3. For empty/incomplete projects:\n"
               "   a. Create necessary directories/files.\n"
               "   b. Provide CLI commands for file creation.\n"
            "4. For existing projects:\n"
               "   a. Analyze the structure for config files, build scripts, etc.\n"
               "   b. Don't assume existence of files not shown.\n"
            "5. Focus on local development setup only.\n"
            f"6. Always navigate to the right path in {self.repo.get_repo_path()} and the right relative path from the provided instruction.\n"
            "7. Explain steps concisely, referencing specific file names/paths.\n"
            "8. Provide CLI commands for setup, file creation, dependency installation, and compilation.\n"
            "9. For new files, provide exact CLI commands to create and populate.\n"
            "10. Navigate back to working directory before major operations.\n"
            "11. Provide each task as a separate, logical step.\n"
            "12. Follow best practices for dependency management (e.g., venv for Python, npm for Node.js).\n"
            "13. Create dependency config files if missing.\n"
            "14. Check project structure before suggesting file operations.\n"
            "15. Include compilation steps for compiled languages.\n"
            "16. Provide steps for multiple scenarios if project type is unclear.\n"
            "17. Don't specify dependency versions unless requested.\n"
            "18. If no dependency files are found or provided, initialize appropriate ones based on the project type.\n"
            "19. Only if need to initializing package.json if doesn't need yet and need to init for one:\n"
                "   - Must include scripts for build and dev environments\n"
                "   - Add 'build' script for production builds\n"
                "   - Add 'dev' script for development\n"
                "   - Add 'start' script to run production build\n"
                "   - Configure all necessary build tools and dependencies\n"
            "20. Use nice format in bash markdown for all commands.\n" +
            (f"   For Windows: Use backslashes and enclose paths with spaces in double quotes (e.g. cd \"{self.repo.get_repo_path()}\")\n" if platform.system() == "Windows" else
            f"   For Unix/Linux/macOS: Use forward slashes and enclose paths with spaces in single quotes (e.g. cd '{self.repo.get_repo_path()}')\n") +
            "21. Include a profile example for commands to show execution time.\n\n"
            "22. CRITICAL - Package Manager Usage:\n"
                "   - NEVER assume or switch package managers\n"
                "   - For Node.js projects, check package-lock.json for npm, yarn.lock for yarn, pnpm-lock.yaml for pnpm\n"
                "   - STRICTLY use ONLY the package manager that's already configured in the project\n"
                "   - If no package manager is set up yet, ASK USER which one they prefer\n"
                "   - DO NOT automatically default to any specific package manager\n"
                "   - Verify lock files and project structure before suggesting ANY package manager commands\n\n"
            "23. CRITICAL - Elevated Privileges:\n"
                "   - For Windows: Prefix commands requiring admin rights with 'Run as Administrator'\n"
                "   - For Unix/Linux/macOS: Use 'sudo' for commands requiring root privileges\n"
                "   - Warn users when elevated privileges are needed\n"
                "   - Explain why elevated privileges are required for specific commands\n\n"

            "Response structure:\n"
            "- Title: [Short setup process title]\n"
            "- Explanation: [Brief process overview]\n"
            "- Steps: [Numbered list of concise steps with CLI commands]\n\n"

            f"CRITICAL: Limit to local development setup. Start with 'cd {self.repo.get_repo_path()}' and end with final compilation/run command. Use exact file names/paths. Provide each CLI command as a separate step. If no dependency files exist, create appropriate ones. Focus solely on dependency setup and ignore tasks related to creating or modifying code files. Ensure all commands are formatted in nice markdown. Include a profile example for commands to show execution time. ONLY PROVIDE COMMANDS THAT WORK ON {platform.system()}."
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current dependency files: {all_file_contents}\n\nProject structure: {tree_contents}\n\nOS Architecture: {OS_architecture}"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})
        logger.debug("CompileProjectAnalysAgent completed initial conversation setup")

    async def get_idea_plan(self, user_prompt, file_attachments, focused_files, assets_link):
        """
        Get development plan for all txt files from Azure OpenAI based on user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("CompileProjectAnalysAgent generating idea plan based on user prompt")
        prompt = (
             f"Here is the user's request:\n{user_prompt} - make it simple and straight forward, no extra step please\n\n"
             f"User OS: {platform.system()}\n"
             "For paths with spaces, preserve the original spaces without escaping or encoding.\n"
             f"CRITICAL: All commands and paths MUST be compatible with {platform.system()} OS - do not provide commands for other operating systems.\n"
             "Important: Follow the existing project setup and focus only on completing the specific task requested. Do not introduce new tools or approaches unless explicitly needed.\n"
             "CRITICAL: For any dependency management or build/run commands:\n"
             "- Strictly use ONLY package managers and tools that are ALREADY set up in the project\n" 
             "- Do NOT assume or suggest installing new package managers (npm, pnpm, yarn etc)\n"
             "- Check and respect the existing project structure and configuration files\n"
             "- If no package manager is currently set up, choose one that best matches the project type\n"
             "- Verify presence of package.json, pnpm-lock.yaml etc before suggesting related commands\n"
             "- Base all suggestions on actual project files, not assumptions\n"
             "CRITICAL EXECUTION RULES:\n"
             "- If user mentions 'run this project' or similar without specifying build - ONLY provide development/run commands (e.g. npm run dev)\n"
             "- If user specifically requests build - ONLY provide build commands (e.g. npm run build)\n" 
             "- Never mix build and dev commands unless explicitly requested\n"
             "- Provide ONLY the exact commands needed - no extra steps or explanations\n"
             "- Keep responses focused on: 1) Directory navigation 2) The specific run/build command\n"
             "- Do not suggest any additional setup or configuration unless absolutely required for the requested operation"
        )

        image_files = process_image_files(file_attachments)

        file_attachments = [f for f in file_attachments if not f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]

        all_attachment_file_contents = ""
        all_focused_files_contents = ""

        if file_attachments:
            for file_path in file_attachments:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if focused_files:
            for file_path in focused_files:
                file_content = read_file_content(file_path)
                if file_content:
                    all_focused_files_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if all_attachment_file_contents:
            prompt += f"\nUser has attached files for you, use them appropriately: {all_attachment_file_contents}"

        if all_focused_files_contents:
            prompt += f"\nUser has focused on files in the current project, pay special attention to them according if need: {all_focused_files_contents}"

        user_content = [{"type": "text", "text": prompt}]

        # Add image files to the user content
        for base64_image in image_files:
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"{base64_image}"
                }
            })

        if assets_link:
            for image_url in assets_link:
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                })

        self.conversation_history.append({"role": "user", "content": user_content})

        try:
            response = await self.ai.arch_stream_prompt(self.conversation_history, 4096, 0.2, 0.1)
            return response
        except Exception as e:
            logger.error(f"AIGateway encountered an error while generating idea plan: {e}")
            return {
                "reason": str(e)
            }


    async def get_idea_plans(self, user_prompt, file_attachments, focused_files, assets_link):
        """
        Get development plans for a list of txt files from Azure OpenAI based on user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        plan = await self.get_idea_plan(user_prompt, file_attachments, focused_files, assets_link)
        return plan
