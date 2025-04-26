import os
import aiohttp
import json
import sys
from typing import List, Dict, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.openai import OpenAIClient
from json_repair import repair_json
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content

logger = get_logger(__name__)

class MainBuilderAgent:
    def __init__(self, repo):
        self.repo = repo

    async def get_pipeline_plan(self, files: str, tree: str) -> Dict:
        """Get a development plan for all txt files from Azure OpenAI based on the user prompt."""
        logger.debug("\n #### `SnowX` is initiating the process to obtain a pipeline plan")
        openai_client = OpenAIClient()
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a builder agent tasked with checking for any compile errors. "
                    "Analyze the provided context to determine the appropriate pipeline to use and respond in JSON format. "
                    "Follow these guidelines:\n\n"
                    "1. Use pipeline 1 if the project needs to be built with Apple Xcode.\n"
                    "2. Use pipeline 2 if the project can be built without Apple Xcode.\n"
                    "The JSON response must follow this format:\n\n"
                    '{\n    "pipeline": "1 or 2"\n}\n\n'
                    "Return only a valid JSON response without additional text or Markdown symbols."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Here are the file changes that need to be built to verify:\n{files}\n"
                    f"Here is the tree structure of the build project:\n{tree}\n"
                )
            }
        ]


        try:
            logger.debug("\n #### `SnowX` is sending a request to OpenAI for completion")
            plan = await openai_client.complete(messages, 0.2)
            if "choices" in plan and len(plan["choices"]) > 0:
                message_content = plan["choices"][0]["message"]["content"]
                plan_json = json.loads(message_content)
                logger.debug("\n #### `SnowX` has successfully received and parsed the pipeline plan")
                return plan_json
        except json.JSONDecodeError:
            logger.debug("\n #### `SnowX` encountered a JSON decoding error, attempting to repair")
            good_json_string = repair_json(message_content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### `SnowX` has successfully repaired and parsed the JSON")
            return plan_json 
        except Exception as e:
            error_message = plan.get("error", {}).get(
                "message", "Unknown error"
            )
            logger.error(f"  `SnowX` encountered an error:\n{error_message}")
            return {"reason": error_message}

    async def get_pipeline_plans(self, files: List[str]) -> Dict:
        """Get development plans for a list of txt files from Azure OpenAI based on the user prompt."""
        logger.debug("\n #### `SnowX` is preparing to retrieve pipeline plans for multiple files")
        all_file_contents = self.repo.print_tree()
        logger.debug("\n #### `SnowX` is calling get_pipeline_plan with the prepared data")
        return await self.get_pipeline_plan(files, all_file_contents)