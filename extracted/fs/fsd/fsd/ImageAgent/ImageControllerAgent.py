import os
import sys
import json
import subprocess
import asyncio
import re

from .ImagePrePromptAgent import CompilePrePromptAgent
from .ImageTaskPlanner import ImageTaskPlanner
from .ImageAnalysAgent import ImageAnalysAgent
from .ImageGenAgent import ImageGenAgent
from .ImageCheckSpecialAgent import ImageCheckSpecialAgent

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.utils import parse_payload
from fsd.log.logger_config import get_logger
from fsd.PromptImageUrlAgent.PromptImageUrlAgent import PromptImageUrlAgent
logger = get_logger(__name__)

class ImageControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.preprompt = CompilePrePromptAgent(repo)
        self.analysAgent = ImageAnalysAgent(repo)
        self.taskPlanner = ImageTaskPlanner(repo)
        self.imageGenAgent = ImageGenAgent(repo)
        self.imageCheckSpecialAgent = ImageCheckSpecialAgent(repo)
        self.imageAgent = PromptImageUrlAgent(repo)

    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)


    async def start_image_process(self, tier, instruction):
        logger.info(f" #### `SnowX` is organizing and preparing the task. ")
        task = await self.taskPlanner.get_task_plan(instruction)
        await self.imageGenAgent.generate_images(task, tier)
        commits = task.get('commits', "")
        self.repo.add_all_files(f"{commits}")
        logger.info(f" #### Image generation process completed.")


    async def get_started(self, tier, instruction, file_attachments, focused_files):
        """Start the processing of the user prompt."""
        
        logger.info(" #### `SnowX` is finding relevant style content.")

        style_files = []

        all_files = set(style_files)
        if file_attachments:
            all_files.update(file_attachments)
        if focused_files:
            all_files.update(focused_files)

        if all_files:
            files_list = "\n".join([f"- {file}" for file in all_files])
            logger.info(f" #### `SnowX` is reading files:\n{files_list}")

        image_result = await self.imageAgent.process_image_links(instruction)
        assets_link = image_result.get('assets_link', []) if isinstance(image_result, dict) else []

        logger.info(f" #### `Image Task Planner` is organizing and preparing the task. ")
        task = await self.taskPlanner.get_task_plan(instruction)
        await self.imageGenAgent.generate_images(task, tier)
        commits = task.get('commits', "")
        self.repo.add_all_files(f"{commits}")
        logger.info(f" #### Image generation process completed.")


    async def get_started_image_generation(self, tier, user_prompt):
        """Start the processing of the user prompt."""
        
        logger.debug(" #### Image generation agent initialized and ready to process image requests")

        if "#### DONE: *** - D*** I**" in user_prompt or "#### DONE: *** - I**" in user_prompt:
            await self.start_image_process(tier, user_prompt)
        else:
            logger.info(" #### `SnowX` has determined that no additional images need to be generated")

        logger.debug(f" #### Image generation process completed!")
