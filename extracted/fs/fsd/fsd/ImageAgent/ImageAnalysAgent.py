import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)
from fsd.util.utils import process_image_files

class ImageAnalysAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.project_path = self.repo.get_repo_path()
        self.ai = AIGateway()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self, style_files):
        """
        Initialize the conversation with a system prompt and user context.
        """

        all_file_contents = ""
        tree_contents = self.repo.print_tree()

        style_files_path = style_files

        if style_files:
            for file_path in style_files_path:
                file_content = read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}:\n{file_content}"
        else:
            all_file_contents = "No dependency files found."

        system_prompt = (
            f"UI/UX designer for image analysis. Analyze files, describe images. FOLLOW:\n\n"
            "2. Analyze style files\n"
            "3. Extract theme elements and color scheme\n"
            "4. Determine image sizes\n"
            "5. Identify backgrounds and textures\n"
            "6. Analyze existing images\n"
            "7. Describe images matching style, including detailed descriptions of most fitting elements\n"
            "8. Adapt to theme, color scheme, and sizes (1024x1024, 1792x1024, 1024x1792)\n"
            f"9. MUST ALWAYS provide FULL PATH within `{self.repo.get_repo_path()}` to save each image\n"
            "10. Support PNG, JPG, JPEG only\n"
            "11. Specify style that fits the overall design theme\n\n"
            "Focus on detailed analysis and description. No code changes.\n\n"
            "Use exact paths. Follow requirements strictly.\n\n"
            "Provide comprehensive color scheme analysis.\n\n"
            "Offer detailed descriptions of elements that best fit the design.\n\n"
            "Clearly articulate the overall style that aligns with the design theme.\n\n"
            "Organize with clear headings (max ####) and spacing."
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current dependency files: {all_file_contents}\n\nProject structure: {tree_contents}\n"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})


    async def get_idea_plan(self, user_prompt, file_attachments, focused_files, assets_link):
        prompt = (
             f"User image generation request:\n{user_prompt}\n\n"
            f"ONLY RETURN IN MARKDOWN TABLES FOR NEW IMAGES TO BE GENERATED. NO OTHER TEXT OR FORMATS.\n\n"
            f"Required table format for each new image:\n\n"
            f"| Aspect | Description |\n"
            f"|--------|-------------|\n"
            f"| Image Name | [Exact name from request] |\n" 
            f"| Description | [Clear and detailed description relevant to the use case] |\n"
            f"| Size | [Width x Height in pixels] |\n"
            f"| Style | [Style description] |\n"
            f"| Colors | [Color scheme] |\n"
            f"| File Path | [Full absolute path starting from {self.repo.get_repo_path()}] |\n"
            f"| Format | [PNG/png, JPG/jpg, JPEG/jpeg, or ICO/ico only] |\n\n"
            f"Rules:\n"
            f"- Only return markdown tables, no other text\n"
            f"- One table per image\n"
            f"- Separate tables with -------------------\n"
            f"- Only include NEW images explicitly requested\n"
            f"- Use absolute paths starting from {self.repo.get_repo_path()}\n"
            f"- NEVER modify or guess paths\n"
            f"- STRICTLY ONLY support PNG/png, JPG/jpg, JPEG/jpeg, ICO/ico formats\n"
            f"- IMMEDIATELY REJECT any other image formats including SVG\n"
            f"- Ignore all other formats and existing images\n"
            f"- No explanatory text or analysis\n"
            f"- Tables must be properly formatted markdown\n"
            f"- Ensure the description is clear and relevant to the use case\n"
            f"- DO NOT process or include any SVG or other unsupported formats\n"
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
            logger.debug("\n #### `SnowX` is initiating the AI prompt for idea generation")
            response = await self.ai.arch_stream_prompt(self.conversation_history, 4096, 0.2, 0.1)
            logger.debug("\n #### `SnowX` has successfully received the AI response")
            return response
        except Exception as e:
            logger.error(f"  `SnowX` encountered an error during idea generation\n Error: {e}")
            return {
                "reason": str(e)
            }


    async def get_idea_plans(self, user_prompt, file_attachments, focused_files, assets_link):
        logger.debug("\n #### `SnowX` is beginning the process of generating idea plans")
        plan = await self.get_idea_plan(user_prompt, file_attachments, focused_files, assets_link)
        logger.debug("\n #### `SnowX` has completed generating idea plans")
        return plan
