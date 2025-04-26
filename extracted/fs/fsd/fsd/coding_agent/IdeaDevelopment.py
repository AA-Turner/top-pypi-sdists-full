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

class IdeaDevelopment:
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

    def initial_setup(self, role, crawl_logs, context, file_attachments, assets_link):
        """
        Initialize the conversation with a system prompt and user context.
        """
        logger.debug("Initializing conversation with system prompt and user context")

        all_file_contents = self.repo.print_tree()

        system_prompt = (
            f"You are a senior {role} architect. Analyze the project files and develop a production-ready implementation plan that balances scalability with maintainability. Your plan must be clear, specific, and build a foundation for future growth. Follow these guidelines:\n\n"
            
            "ARCHITECTURAL PRINCIPLES:\n"
            "- Modularity: Break down systems into small, focused components with single responsibilities\n"
            "- Granularity: Create many small files rather than few large ones\n"
            "- Decoupling: Ensure minimal dependencies between components\n"
            "- Scalability: Design small, independent services that can scale individually\n"
            "- Maintainability: Favor many simple files over complex monolithic structures\n"
            "- Testability: Small components are easier to test in isolation\n"
            "- Reusability: Smaller components promote code reuse across the application\n"
            "- UI/UX: Always prioritize intuitive user interfaces and seamless user experiences\n\n"
            
            "EXTERNAL RESOURCES INTEGRATION:\n"
            "- When Zinley crawler data is provided, design robust interfaces for data consumption\n"
            "- Implement proper error handling and data validation\n"
            "- Consider caching strategies and fallback mechanisms\n"
            "- Example: 'The DataService in src/services/DataService.js will handle crawler data with retry logic and validation'\n\n"
            
            "COMPONENT BREAKDOWN:\n"
            "IMPORTANT: Only include sections that are relevant to the current task. Do not include all sections if they are not appropriate for the task at hand.\n\n"
            
            "1.GOAL:\n"
            "- Define the goal overview what need to be implemented in 2-3 sentences\n"

            "2. EXISTING FILES MODIFICATIONS:\n"
            "- List only files that need to be modified:\n"
            "  * MANDATORY: Specify EXACTLY which files need to be updated\n"
            "  * MANDATORY: For each file, briefly describe what changes are needed\n"
            "  * MANDATORY: Focus only on high-level architectural changes required\n"
            "3. NEW COMPONENTS AND FILES:\n\n"
            
            "DIRECTORY STRUCTURE (CRITICAL):\n"
            "- MANDATORY: Provide a tree structure showing ONLY:\n"
            "  2. Files being moved (showing source and destination)\n"
            "- DO NOT include unchanged existing files\n"
            "- Example:\n"
            "```plaintext\n"
            "project_main_folder/\n"
            "├── src/\n"
            "│   ├── components/\n"
            "│   │   └── LoginForm.js       # New component\n"
            "│   ├── services/\n"
            "│   │   └── ApiService.js      # New API client\n"
            "│   └── utils/\n"
            "│       └── validators.js      # Moved from: helpers/validation.js\n"
            "```\n\n"
            
            "COMPONENT DESIGN:\n"
            "- For each new component/module:\n"
            "  * Purpose and responsibilities\n"
            "  * Integration with other components\n"
            "- MANDATORY: Ensure component structure promotes modularity with clear separation of concerns\n"
            "- MANDATORY: Define interfaces between components to minimize coupling\n"
            "- MANDATORY: Specify reusable components that can be shared across features\n\n"
            
            "4. IMPLEMENTATION ORDER:\n"
            "- Organize implementation in a logical sequence to maximize context awareness:\n"
            "  * Start with core utilities and services that other components will depend on\n"
            "  * Then build main components in dependency order (implement providers before consumers)\n"
            "  * Finally integrate everything together with proper context flow\n"
            "- For each step, list files in implementation order with dependencies clearly marked\n"
            "- MANDATORY: Ensure files that provide context are implemented before files that consume that context\n"
            "- MANDATORY: Group related files together to maintain contextual understanding\n\n"
            
            "5. FEATURES TO IMPLEMENT (CRITICAL):\n"
            "- List all core features that must be implemented in this iteration inlude UI/UX if any\n"
            "- Example: 'User Authentication (Critical): Allow users to register and login. Requirements: Email/password registration, secure password storage, session management. Acceptance: User can register, login, and access protected routes'\n\n"
            
            "6. CORE UI/UX FLOW DESCRIPTION:\n"
            "- Outline the sequence of logical steps including:\n"
            "  * User actions (clicks, form submissions, etc.)\n"
            "  * System responses and screen transitions\n"
            "  * Key decision points in the flow\n"
            "- MANDATORY: Focus only on the core journey without detailing edge cases or error flows\n"
            "- MANDATORY: Ensure the flow is logical and addresses the main user goal\n"
            "- MANDATORY: Keep the flow description concise and focused on critical interactions\n"
            "- MANDATORY: Include only the steps necessary to complete the primary user goal\n"
            
            "7. DEPENDENCIES AND TECHNICAL STACK:\n"
            "- List only NEW dependencies required for this feature (marked as [REQUIRED])\n"
            "- Purpose of each new dependency within the architecture\n"
            "- NEVER request to modify package.json, package-lock.json, yarn.lock, or similar dependency files directly\n"
            "- All dependencies will be installed through the dependency installation process\n"
            "- Installation commands for new dependencies only\n"
            "- DO NOT include version numbers (like x.x.x) unless you are absolutely certain about the specific version needed\n"
            "- When listing required dependencies, only include the package name and installation command without version numbers\n"
            "- NEVER suggest installing linting tools, testing frameworks, or other development dependencies unless explicitly requested by the user\n"
            "- For dependency issues, clearly mark as [FIX REQUIRED] and specify the action needed:\n"
            "  * For removal: '[FIX REQUIRED] package-name: Remove conflicting/unused dependency. Action: pnpm remove package-name'\n"
            "  * For reinstallation: '[FIX REQUIRED] package-name: Reinstall to fix version conflicts. Action: pnpm remove package-name && pnpm add package-name'\n"
            "  * For buggy dependencies: '[FIX REQUIRED] package-name: Replace with alternative due to known bugs. Action: pnpm remove package-name && pnpm add alternative-package'\n"
            "- Example: '[REQUIRED] react-router-dom: Client-side routing library. Purpose: Navigate between pages. Install: pnpm add react-router-dom'\n\n"
            
            "8. API INTEGRATION:\n"
            "- For each API endpoint:\n"
            "  * Endpoint URL\n"
            "  * Basic request/response information\n"
            "- Example:\n"
            "  - API: https://api.example.com/data\n"
            "  - Purpose: Fetch user data\n"
            "  - Request: GET with user ID parameter\n\n"
            
            "9. DOCUMENTATION:\n"
            "- ALWAYS include a task to update the existing md file or create a new one if it doesn't exist to document the implementation\n"
            "- Create/Update snowx.md file for internal AI memory about the project and codebase:\n"
            "  * Keep this file concise but include all important implementation details\n"
            "  * Document key architecture decisions and code patterns for future reference\n"
            "  * Always replace outdated information with new knowledge\n"
            "  * This internal memory file helps improve future code generation and understanding\n"
            "  * Focus on documenting only what will be helpful for future AI assistance\n"
            "- Update official documentation for users:\n"
            "  * Update README.md or other existing documentation files\n"
            "  * Create new documentation files only if necessary\n"
            "- Split user documentation into multiple .md files if the content is extensive:\n"
            "  * setup.md: Installation and configuration instructions\n"
            "  * usage.md: Usage examples and API documentation\n"
            "  * architecture.md: System architecture and component relationships\n"
            "- Clearly specify which files to update and what content to modify\n"
            "- Ensure all documentation is clear, concise, and follows a consistent format\n"
            
            "CRITICAL INSTRUCTION: Only include sections that are relevant to the current task. Do not include all sections by default. Focus only on what needs to be done for this specific implementation.\n\n"
            
            "DO NOT INCLUDE:\n"
            "- Future enhancements or improvements\n"
            "- Focus only on what needs to be done now\n"
            "- Any code - only describe what needs to be implemented\n\n"
            
            "IMPORTANT NOTES:\n"
            "- When encountering empty existing files, treat them as placeholders to be filled\n"
            "- For empty projects, establish a viable structure\n"
            "- For existing projects, make targeted additions that align with current structure\n"
            "- NEVER suggest deleting existing files\n"
            f"- Reference the project root path {self.repo.get_repo_path()}:\n{all_file_contents}\n\n"
            
            "CODE FILE SIZE LIMIT:\n"
            "- Keep files concise and focused on specific functionality\n\n"
            
            "IMAGE FORMAT RULES:\n"
            "- For icons, buttons, and UI elements, ALWAYS prefer SVG format for better scalability and performance\n"
            "- Only consider PNG, JPG, JPEG, or ICO formats for complex images that cannot be represented as vectors\n"
            "- SVG is the recommended format for all icons, logos, and simple graphics\n"
            "- Only flag image generation if the architecture explicitly requires photos or complex raster images\n\n"
            
            "UI/UX DESIGN PRINCIPLES:\n"
            "- If building a web app/ mobile app from scratch, prioritize a beautiful and modern UI with best UX practices\n"
            "- Design responsive layouts that work across all device sizes (mobile, tablet, desktop)\n"
            "- Use consistent color schemes, typography, and spacing throughout the application\n"
            "- Implement intuitive navigation patterns and clear visual hierarchies\n"
            "- Ensure accessibility compliance (WCAG standards) for all UI components\n"
            "- Design for progressive enhancement and graceful degradation\n"
            "- Include loading states, error handling, and empty states in the UI\n"
            "- Prioritize performance optimization for fast page loads and smooth interactions\n\n"
            
            "SPECIAL ENDING RULES:\n"
            "- If plan includes BOTH dependencies AND new eligible images: End with #### DONE: *** - D*** I**\n" 
            "- If ONLY dependencies needed: End with #### DONE: *** - D***\n"
            "- If ONLY new eligible images needed: End with #### DONE: *** - I**\n"
            "- If NO dependencies AND NO eligible images: No special ending"
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})

        if crawl_logs:
            crawl_logs_prompt = f"This is data from the website the user mentioned. You don't need to crawl again: {crawl_logs}"
            self.conversation_history.append({"role": "user", "content": crawl_logs_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Understood. Using provided data only."})

            utilization_prompt = (
                "Specify which file(s) should access this crawl data. "
                "Do not provide steps for crawling or API calls. "
                "The data is already available. "
                "Follow the original development plan guidelines strictly, "
                "ensuring adherence to all specified requirements and best practices."
            )
            self.conversation_history.append({"role": "user", "content": utilization_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Will specify files for data access, following original implementation guidelines strictly. No additional crawling or API calls needed."})

        if context:
            working_files = [file for file in context.get('working_files', []) if not file.lower().endswith(('.mp4', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.wav', '.mp3', '.ogg'))]

            all_working_files_contents = ""

            if working_files:
                for file_path in working_files:
                    # Skip large lock files
                    if os.path.basename(file_path) in ["pnpm-lock.yaml", "package-lock.json", "yarn.lock", "Gemfile.lock", "Cargo.lock", "poetry.lock"]:
                        all_working_files_contents += f"\n\nFile: {file_path}:\n[Lock file content omitted due to size]"
                        continue
                        
                    file_content = read_file_content(file_path)
                    if file_content:
                        all_working_files_contents += f"\n\nFile: {file_path}: {file_content}"
                    else:
                        all_working_files_contents += f"\n\nFile: {file_path}: EXISTING EMPTY FILE -  NO NEW CREATION NEED PLEAS, ONLY MODIFIED IF NEED"


            if all_working_files_contents:
                self.conversation_history.append({"role": "user", "content": f"This is the most picked relevant file that may related for this task, analysizing and use it properly. \n{all_working_files_contents}"})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})
            else:
                self.conversation_history.append({"role": "user", "content": "There are no existing files yet that I can find for this task."})
                self.conversation_history.append({"role": "assistant", "content": "Understood."})


        all_attachment_file_contents = ""

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
            self.conversation_history.append({"role": "user", "content": f"User has attached files for you, use them appropriately: {all_attachment_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Understood."})

        message_content = [{"type": "text", "text": "User has attached these images. Use them correctly, follow the user prompt, and use these images as support!"}]

        # Add image files to the user content
        for base64_image in image_files:
            message_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"{base64_image}"
                }
            })

        if assets_link:
            for image_url in assets_link:
                message_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                })

        self.conversation_history.append({"role": "user", "content": message_content})
        self.conversation_history.append({"role": "assistant", "content": "Understood."})

        if assets_link or image_files:
            image_detail_prompt = (
                "Analyze each image in detail according to user requirements.\n\n"
                "For each image, describe visual elements (shapes, colors, layout), "
                "content (text, fonts, icons), implementation details (dimensions, structure), "
                "and purpose (replica vs inspiration). Description should enable "
                "implementation without the original image."
            )
            self.conversation_history.append({"role": "user", "content": image_detail_prompt})
            self.conversation_history.append({"role": "assistant", "content": "I will analyze each image with extreme detail, providing comprehensive specifications for all visual elements, content, measurements, and implementation requirements. My descriptions will be precise enough to enable perfect reproduction based on the user's needs for either exact replication or inspiration."})

    async def get_idea_plan(self, user_prompt):
        logger.debug("Generating idea plan based on user prompt")
        prompt = (
            f"Create a focused implementation plan for:\n\n{user_prompt}\n\n"
            f"Operating System: {platform.system()}\n"
            f"Use correct OS-specific paths and separators.\n\n"
            "Focus on essential elements only:\n"
            "- Be brief and concise\n"
            "- Mark requirements clearly\n"
            "- Avoid content repetition\n"
            "- Prioritize immediate needs\n\n"
            "Determine exactly what to do for the current implementation plan, without conditionals since you are the one deciding what to do and other agents will do exactly what you say. Don't mention anything about future plans.\n\n"
            "SPECIAL ENDING RULES:\n"
            "- If plan includes BOTH dependencies management AND new eligible images: End with #### DONE: *** - D*** I**\n" 
            "- If ONLY dependencies management needed: End with #### DONE: *** - D***\n"
            "- If ONLY new eligible images needed: End with #### DONE: *** - I**\n"
            "- If NO dependencies AND NO eligible images: No special ending"
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.arch_stream_prompt(self.conversation_history, 4096, 0.2, 0.1)
            return response
        except Exception as e:
            logger.error(f"`IdeaDevelopment` agent encountered an error: {e}")
            return {
                "reason": str(e)
            }

    async def get_idea_plans(self, user_prompt):
        logger.debug("Initiating idea plan generation process")
        return await self.get_idea_plan(user_prompt)
