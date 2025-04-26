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
from fsd.util.utils import process_image_files
logger = get_logger(__name__)

class ContextPrepareAgent:
    def __init__(self, repo):
        """
        Initialize the ContextPrepareAgent with the repository.

        Args:
            repo: The repository object containing project information.
        """
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_file_planning(self, idea, file_attachments, focused_files, assets_link):

        """
        Request file planning from AI for a given idea and project structure.

        Args:
            idea (str): The user's task or development plan.
            file_attachments (list): List of attached files.
            focused_files (list): List of files the user is focusing on.
            assets_link (list): List of asset links.

        Returns:
            dict: JSON response with the plan including working files and context files.
        """
        logger.debug("\n #### Context prepare agent is initiating file planning process")
        prompt = (
            "Based on the provided development plan and project structure, create a JSON response with a 'working_files' list containing the most relevant files needed for this task. "
            "The response should be valid JSON without any additional text or formatting. "
            "'working_files' should include full paths for up to 10 most relevant existing files that are directly related to this task. "
            "Include all files that are necessary for comprehensive context awareness before coding. "
            "\nFiles MUST be prioritized in this exact order: "
            "1. Files explicitly mentioned in user attachments or focused files "
            "2. README.md and ALL other documentation files (.md, .txt, etc.) that explain project structure, rules, or guidelines "
            "3. Configuration files relevant to the task (package.json, package-lock.json, npm-shrinkwrap.json, yarn.lock, pnpm-lock.yaml, tsconfig.json, .eslintrc, pom.xml, requirements.txt, Gemfile.lock, Cargo.lock, etc.) "
            "4. Route definition files (routes.js, urls.py, web.php, etc.) based on the tech stack "
            "5. Model/schema definitions related to the task "
            "6. Service/controller/component files that implement related functionality "
            "7. Test files for components being modified "
            "8. Utility files referenced by the above files "
            "\nTech stack specific guidelines: "
            "- For JavaScript/TypeScript projects: Include package.json, package-lock.json/yarn.lock/pnpm-lock.yaml, tsconfig.json, relevant webpack/babel configs "
            "- For React/Vue/Angular: Include component definitions and their related context/store files "
            "- For Node.js: Include route definitions, middleware, and controller files "
            "- For Python: Include requirements.txt, Pipfile.lock, settings.py, urls.py, models.py, and views.py "
            "- For Java/Spring: Include pom.xml, gradle.lock, application.properties, controller and service classes "
            "- For PHP/Laravel: Include composer.json, composer.lock, web.php, controllers, and models "
            "- For .NET: Include .csproj files, packages.lock.json, Startup.cs, Program.cs, and relevant controllers "
            "- For Ruby/Rails: Include Gemfile, Gemfile.lock, routes.rb, controllers, and models "
            "- For Rust: Include Cargo.toml, Cargo.lock, and relevant module files "
            "\nImportant guidelines: "
            "- Include complete file paths from project root, matching exactly as they appear in the structure "
            "- Only include files that actually exist in the project "
            "- ALWAYS include ALL .md files including README.md and other documentation files that might contain project rules or guidelines "
            "- Exclude third-party libraries, generated folders, and dependency files (node_modules/, build/, etc.) "
            "- Always include configuration files relevant to the task (package.json, tsconfig.json, etc.) "
            "- Always include lock files (package-lock.json, yarn.lock, pnpm-lock.yaml, etc.) to understand exact dependency versions "
            "- Always include route definition files when modifying endpoints or API functionality "
            "- Always include model/schema definitions when working with data structures "
            "- Exclude all image and media files (.png, .jpg, .mp4, etc.) "
            "- Return an empty list if no relevant files are found "
            "\nExamples of when to include specific files: "
            "- When modifying a React component: Include the component file, its CSS, related context providers, and parent components "
            "- When fixing a bug in an API endpoint: Include the route definition, controller, service, and related model files "
            "- When implementing a new feature: Include similar existing implementations, configuration files, and affected components "
            "- When refactoring code: Include all files in the refactoring scope plus configuration files "
            "\nCRITICAL PATH REQUIREMENTS:"
            "- ALWAYS use the COMPLETE directory structure when specifying file paths. NEVER skip intermediate directories."
            "- CORRECT: \"{self.repo.get_repo_path()}/projectfolder/src/components/Button/index.js\""
            "- INCORRECT: \"{self.repo.get_repo_path()}/index.js\" (when the file is actually nested in subdirectories)"
            "- Always traverse through ALL subdirectories when specifying paths. Never connect the root directory directly to a deeply nested file."
            "\nUse this JSON format:"
            "{\n"
            "    \"working_files\": [\"/absolute/path/to/project/root/folder1/subfolder/file1.extension\", \"/absolute/path/to/project/root/folder2/file2.extension\"],\n"
            "}\n\n"
            "If the list is empty, return:"
            "{\n"
            "    \"working_files\": [],\n"
            "}\n\n"
            f"The current project path is \"{self.repo.get_repo_path()}\". Ensure all file paths start with this project path and EXACTLY match the paths in the provided project structure.\n"
            "Return only valid JSON without Markdown symbols or invalid escapes."
        )

        all_focused_files_contents = ""
        all_attachment_file_contents = ""

        if focused_files:
            for file_path in focused_files:
                file_content = read_file_content(file_path)
                if file_content:
                    all_focused_files_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if all_focused_files_contents:
            prompt += f"\nUser has focused on files in the current project, MUST include those files in working_files and find relevant context files related to those attached: {all_focused_files_contents}"

        # Process image files
        image_files = process_image_files(file_attachments)
        
        # Remove image files from file_attachments
        file_attachments = [f for f in file_attachments if not f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]

        if file_attachments:
            for file_path in file_attachments:
                file_content = read_file_content(file_path)
                if file_content:
                    all_attachment_file_contents += f"\n\nFile: {os.path.relpath(file_path)}:\n{file_content}"

        if all_attachment_file_contents:
            prompt += f"\nUser has attached files for you, use them appropriately: {all_attachment_file_contents}"

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
                
        messages = [
            {
                "role": "system",
                "content": user_content
            },
            {
                "role": "user",
                "content": f"This is the user's request to do:\n{idea}\nThis is the current project structure:\n{self.repo.get_repo_path()}\n{self.repo.print_summarize_with_tree()}\n"
            }
        ]

        try:
            logger.debug("\n #### Context prepare agent is sending request to AI for file planning")
            response = await self.ai.arch_prompt(messages, 4096, 0.2, 0.1)
            logger.debug("\n #### Context prepare agent has received response from AI")
            plan_json = json.loads(response.choices[0].message.content)
            
            # Ensure working_files list exists and contains only unique elements
            plan_json["working_files"] = list(set(plan_json.get("working_files", [])))
            
            return plan_json
        except json.JSONDecodeError:
            logger.debug("\n #### Context prepare agent encountered JSON decode error, attempting repair")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"  Context prepare agent encountered an error: `{e}`")
            return {
                "working_files": [],
                "reason": str(e)
            }

    async def get_file_plannings(self, idea, focused_files):
        logger.debug("\n #### Context prepare agent is starting file planning process")
        return await self.get_file_planning(idea, focused_files)
