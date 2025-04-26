import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
import platform
logger = get_logger(__name__)

class DependencyProjectAnalysAgent:
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

    def initial_setup(self, dependency_files, OS_architecture):
        """
        Initialize the conversation with a system prompt and user context.
        """

        all_file_contents = ""
        tree_contents = self.repo.print_tree()

        logger.debug(f" #### `SnowX`: Initializing analysis with repository path\n{self.repo.get_repo_path()}")

        dependency_files_path = dependency_files

        if dependency_files_path:
            for file_path in dependency_files_path:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}:\n{file_content}"
        else:
            all_file_contents = "No dependency files found."
        system_prompt = (
            f"You are an EXPERT DevOps engineer. Create a simple CLI-only dependency installation plan. Follow these rules:\n\n"
            f"User OS: {platform.system()}\n"
            "- Respect and use existing conventions, libraries, etc. that are already present in the code base.\n"
            "1. Navigate to the project directory\n"
            "2. Carefully examine the project tree to identify existing configuration files\n"
            "3. If configuration files (e.g., package.json, Podfile, requirements.txt) are missing, create them first\n"
            "4. Initialize configuration files with basic structure before proceeding with installations\n"
            "5. Only if need to initializing package.json if need for this project but missing:\n"
            "   - Must include scripts for build and dev environments\n" 
            "   - Add 'build' script for production builds\n"
            "   - Add 'dev' script for development\n"
            "   - Add 'start' script to run production build\n"
            "   - Configure all necessary build tools and dependencies\n"
            "6. Identify and install dependencies using appropriate package managers (e.g., pip, npm, yarn)\n"
            "7. Set up a virtual environment if necessary (e.g., venv for Python)\n"
            "8. Provide concise CLI commands for each step, using nice formatting in bash markdown, like this:\n"
            "   ```bash\n" +
            ("   # Windows commands:\n"
             "   # Use 'Run as Administrator' for commands requiring elevated privileges\n"
             "   cd C:\\path\\to\\project\n"
             "   # For admin privileges, open PowerShell as Administrator and run:\n"
             "   npm install --global package-name\n" if platform.system() == "Windows" else
             "   # Unix commands:\n"
             "   cd /path/to/project\n"
             "   # Use sudo for commands requiring elevated privileges\n"
             "   sudo npm install --global package-name\n") +
            "   ```\n"
            "9. Focus only on essential dependency setup and configuration\n"
            "10. Ensure the setup allows for easy project execution later\n"
            "11. For any file modifications, specify the file path and content to be changed\n"
            "12. Prioritize simplicity and avoid potential conflicts in the installation process\n"
            "13. Configure build/run files to make project execution as simple as possible\n" +
            (f"14. If appropriate, create a simple run.bat script with clear instructions\n" if platform.system() == "Windows" else
             f"14. If appropriate, create a simple run.sh script with clear instructions\n") +
            "15. For compiled languages, include compilation steps and create executable files if needed\n"
            "16. For other project types, ensure similar configuration files are properly set up (e.g., Gemfile for Ruby, pom.xml for Java)\n"
            "17. Double-check all configuration files for completeness and correctness\n"
            "18. For commands requiring elevated privileges:\n" +
            ("    - On Windows: Run PowerShell/CMD as Administrator\n"
             "    - Indicate which commands need Administrator privileges\n" if platform.system() == "Windows" else
             "    - Use 'sudo' prefix for commands requiring root access\n"
             "    - Indicate which commands need sudo privileges\n") +
            "19. Never introduce mismatched or additional dependencies not included as required from original prompt, don't make up a new one\n" +
            "Do not create or modify any code files beyond basic configuration and build/run scripts. Match the OS architecture provided."
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current dependency files: {all_file_contents}\n\nProject tree: {tree_contents}\n\nOS Architecture: {OS_architecture}"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})

    async def get_idea_plan(self, user_prompt, file_attachments, focused_files, assets_link):
        prompt = (
            f"Analyze the current project setup and install only the specific dependencies requested by the user:\n\n"
            f"{user_prompt} - make it simple and straight forward, no extra step please\n\n"
            "- CRITICAL: Strictly respect and use ONLY package managers and build tools that are already configured in the project\n"
            "- DO NOT assume or add new package managers (npm, pnpm, pip, etc) that aren't already set up\n"
            "- If no package manager exists, carefully analyze project type and files to determine most appropriate one\n"
            "- Use existing configuration files if present\n"
            "- Only add requested dependencies, no extra packages\n"
            "- FOCUS ONLY on installing dependencies - do not include steps for running, building, compiling, testing etc\n"
            "- Do not include version verification or validation steps\n"
            "- Keep installation commands minimal and direct - no extra configuration\n"
            "- Provide direct installation commands with clear formatting\n"
            "- For paths with spaces, preserve the original spaces without escaping or encoding\n"
            f"- All commands MUST be compatible with {platform.system()} OS only\n"
            f"- Do not provide commands for other operating systems besides {platform.system()}\n"
            "- Before suggesting ANY package manager commands, verify that manager is actually installed and configured\n"
            "- If suggesting a new package manager, clearly state it needs to be installed first\n"
            "- STRICTLY focus on installing only the exact dependencies requested by user - nothing more\n"
            "- NEVER include ambiguous version numbers like x.x.x in dependency specifications\n"
            "- Only specify exact version numbers if you are absolutely confident about the correct version\n"
            "- If you're not confident about the exact version number, omit version specifications entirely\n"
            "- Do not use version ranges with carets (^) or tildes (~) unless explicitly requested\n\n"
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
            logger.error(f"  `SnowX`: Error occurred while generating idea plan\n{e}")
            return {
                "reason": str(e)
            }


    async def get_idea_plans(self, user_prompt, file_attachments, focused_files, assets_link):
        plan = await self.get_idea_plan(user_prompt, file_attachments, focused_files, assets_link)
        return plan
