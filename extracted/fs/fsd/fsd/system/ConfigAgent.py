import os
import sys
import asyncio
from datetime import datetime
import aiohttp
import json
import re
from json_repair import repair_json
from log.logger_config import get_logger

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class ConfigAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    def get_current_time_formatted(self):
        """Return the current time formatted as mm/dd/yy."""
        current_time = datetime.now()
        formatted_time = current_time.strftime("%m/%d/%y")
        return formatted_time

    async def get_config_request(self, instruction, main_path):
        """
        Get coding response for the given instruction and context from AI.

        Args:
            instruction (str): The instruction for the config change.
            main_path (str): Path to the file to work on.

        Returns:
            str: The config response or error reason.
        """
        if main_path:
            context = read_file_content(main_path)
        else:
            context = "Empty File context"

        system_prompt = f"""You are an expert software engineer specializing in devops. Follow these guidelines strictly when responding to instructions:

                **Response Guidelines:**
                1. Use ONLY the following SEARCH/REPLACE block format for ALL code changes, additions, or deletions:

                   <<<<<<< SEARCH
                   [Existing code to be replaced, if any]
                   =======
                   [New or modified code]
                   >>>>>>> REPLACE

                2. For new code additions, use an empty SEARCH section:

                   <<<<<<< SEARCH
                   =======
                   [New code to be added]
                   >>>>>>> REPLACE

                3. CRITICAL: The SEARCH section MUST match the existing code with EXACT precision - every character, whitespace, indentation, newline, and comment must be identical.
                   - If the file contains code or other data wrapped/escaped in json/xml/quotes or other containers, you need to propose edits to the literal contents of the file, including the container markup.

                4. For large files, focus on relevant sections. Use comments to indicate skipped portions:
                   // ... existing code ...

                5. MUST break complex changes or large files into multiple SEARCH/REPLACE blocks.
                   - Keep SEARCH/REPLACE blocks concise
                   - Break large changes into a series of smaller blocks that each change a small portion of the file
                   - Include just the changing lines, and a few surrounding lines if needed for uniqueness
                   - Do not include long runs of unchanging lines

                6. CRITICAL: NEVER provide code snippets, suggestions, or examples outside of SEARCH/REPLACE blocks. ALL code must be within these blocks.

                7. Do not provide explanations, ask questions, or engage in discussions. Only return SEARCH/REPLACE blocks.

                8. If a request cannot be addressed solely through SEARCH/REPLACE blocks, do not respond.

                9. CRITICAL: Never include code markdown formatting, syntax highlighting, or any other decorative elements. Code must be provided in its raw form.

                10. STRICTLY FORBIDDEN: Do not hallucinate, invent, or make assumptions about code. Only provide concrete, verified code changes based on the actual codebase.

                11. MANDATORY: Code must be completely plain without any formatting, annotations, explanations or embellishments. Only pure code is allowed.

                12. SEARCH/REPLACE blocks will only replace the first match occurrence. Include multiple unique blocks if needed.

                13. Only create SEARCH/REPLACE blocks for files that have been added to the chat.

                14. To move code within a file, use 2 SEARCH/REPLACE blocks:
                    - One to delete it from its current location
                    - One to insert it in the new location

                Remember: Your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed.

        """

        user_prompt = (
            f"File context: {context}. "
            f"Your config must be well-organized, with a senior-level design approach.\n"
            "Remember, your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed.\n\n"
            f"Instruction: {instruction}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            logger.debug(f" #### `SnowX` is initiating a request to the AI for configuration changes")
            response = await self.ai.coding_prompt(messages, 4096, 0.2, 0.1)
            logger.debug(f" #### `SnowX` has successfully received a response from the AI")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"  `SnowX` encountered an error: Failed to get config request: {e}")
            return str(e)

    async def get_config_requests(self, instruction, main_path):
        """
        Get config response for the given file and instruction.

        Args:
            file_name (str): Name of the file to work on.
            instruction (str): The instruction for the config change.

        Returns:
            str: The config response or error reason.
        """
        logger.debug(f" #### `SnowX` is beginning to process the configuration request for {main_path}")
        result = await self.get_config_request(instruction, main_path)
        logger.debug(f" #### `SnowX` has completed processing the configuration request for {main_path}")
        return result
