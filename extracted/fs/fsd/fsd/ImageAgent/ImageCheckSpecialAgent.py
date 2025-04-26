import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.portkey import AIGateway
from json_repair import repair_json
from log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class ImageCheckSpecialAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_image_check_plan(self, user_prompt):
        """
        Get an image check plan from Azure OpenAI based on the user prompt.

        Args:
            user_prompt (str): The user's prompt.

        Returns:
            dict: Image check plan or error reason.
        """
        messages = [
            {
                "role": "system", 
                "content": (
                    f"ONLY RETURN MARKDOWN TABLES FOR PNG, png, JPG, jpg, JPEG, jpeg, or .ico IMAGES. NO OTHER FORMATS OR FILE TYPES ARE ALLOWED OR SHOULD BE MENTIONED.\n\n"
                    "Table format for each new image:\n\n"
                    "| Aspect | Detail description |\n"
                    "|--------|-------------|\n"
                    "| Image Name | [Exact name from development plan] |\n"
                    f"| File Path | [Full path starting with {self.repo.get_repo_path()} and STRICTLY using the EXACT relative path from development plan, INCLUDING ANY PROJECT FOLDER NAMES] |\n"
                    "| Description | [Detailed and clear description for this new image, including specific style, purpose of use, and any relevant context. The description should be comprehensive enough to ensure the correct image is generated for the intended use case.] |\n"
                    "| Format | [STRICTLY ONLY: PNG, JPG, JPEG, or ICO - NO OTHER FORMATS] |\n"
                    "| Dimensions | [Width x Height in pixels] |\n\n"
                    "STRICT RULES:\n"
                    "- ONLY ALLOWED FORMATS: PNG, JPG, JPEG, ICO\n"
                    "- Only return markdown tables, no other text\n"
                    "- One table per image\n"
                    "- Separate tables with -------------------\n"
                    "- Only include NEW images explicitly requested\n"
                    f"- Use absolute paths starting with {self.repo.get_repo_path()}\n"
                    "- MUST include project folder names in paths\n"
                    "- NEVER modify or guess paths\n"
                    "- STRICTLY follow development plan paths\n"
                    "- REJECT AND DO NOT INCLUDE ANY OTHER IMAGE FORMATS\n"
                    "- No explanatory text or analysis\n"
                    "- Tables must be properly formatted markdown\n"
                    "- Ensure the description is clear, detailed, and relevant to the image's purpose\n"
                )
            },
            {
                "role": "user",
                "content": f"Extract ONLY images in PNG, JPG, JPEG, or ICO format to be generated from this development plan. NO OTHER FORMATS ARE ALLOWED. Provide clear and detailed descriptions for each image. Return ONLY markdown tables: {user_prompt}"
            }
        ]

        response = await self.ai.arch_stream_prompt(messages, 4096, 0.2, 0.1)
        return response

    async def get_image_check_plans(self, user_prompt):
        """
        Get image check plans based on the user prompt.

        Args:
            user_prompt (str): The user's prompt.

        Returns:
            dict: Image check plan or error reason.
        """
        logger.debug(f" #### `SnowX` is initiating the image check plan generation\n User prompt: {user_prompt}")
        plan = await self.get_image_check_plan(user_prompt)
        logger.debug(f" #### `SnowX` has completed generating the image check plan")
        return plan
