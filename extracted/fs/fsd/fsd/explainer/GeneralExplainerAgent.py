import os
import sys
import datetime
from typing import List, Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
from fsd.util.utils import process_image_files
logger = get_logger(__name__)

class GeneralExplainerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    async def get_normal_answer_plan(self, conversation_history, user_prompt, role, file_attachments, focused_files, assets_link, crawl_logs=""):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            conversation_history (list): The conversation history.
            user_prompt (str): The user's prompt.
            role (str): The role of the AI assistant.
            file_attachments (list): List of attached file paths.
            focused_files (list): List of focused file paths.
            assets_link (list): List of image URLs.
            crawl_logs (str): Crawl logs string (default empty).

        Returns:
            list: Updated conversation history.
        """
        logger.debug("\n #### `SnowX` is preparing to generate a response plan")

        prompt = ""
        all_attachment_file_contents = ""
        all_focused_files_contents = ""

        # Process image files
        image_files = process_image_files(file_attachments)
        
        # Remove image files from file_attachments
        file_attachments = [f for f in file_attachments if not f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]

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
            prompt += f"\nUser has focused on files in the current project, pay special attention to them according to user prompt: {all_focused_files_contents}"

        prompt += (
            f"Current time, only use if need: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo}"
            f"User prompt:\n{user_prompt}\n"
            "FOR ALL LINKS, YOU MUST USE MARKDOWN FORMAT. EXAMPLE: [Link text](https://www.example.com)\n"
        )

        message_content = [{"type": "text", "text": prompt}]

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

        conversation_history.append({"role": "user", "content": message_content})

        try:
            logger.info(f" #### `{role}` is in charge.\n")
            res = await self.ai.explainer_stream_prompt(conversation_history, 4096, 0.2, 0.1)
            conversation_history.append({"role": "assistant", "content": res})
            
            # Keep conversation history no longer than 30 pairs, excluding the system prompt
            if len(conversation_history) > 61:  # 1 system + 30 user/assistant pairs
                conversation_history = conversation_history[:1] + conversation_history[-60:]
            
            return conversation_history
        except Exception as e:
            logger.error(f"  `{role}` encountered some errors: {str(e)}")
            # Remove the last user prompt from history in case of error
            if len(conversation_history) > 1 and conversation_history[-1]["role"] == "user":
                conversation_history.pop()
            return conversation_history

    async def get_normal_answer_plans(self, conversation_history, user_prompt, role, file_attachments, focused_files, assets_link, crawl_logs=""):
        logger.debug("\n #### `SnowX` is commencing the process of obtaining normal answer plans")
        plan = await self.get_normal_answer_plan(conversation_history, user_prompt, role, file_attachments, focused_files, assets_link, "")
        logger.debug("\n #### `SnowX` has successfully retrieved the normal answer plan")
        return plan
