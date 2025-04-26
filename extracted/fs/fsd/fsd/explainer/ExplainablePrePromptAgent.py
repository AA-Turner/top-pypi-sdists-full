import os
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)
class ExplainablePrePromptAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_prePrompt_plan(self, user_prompt, file_attachments, focused_files):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            user_prompt (str): The user's prompt.
            file_attachments (list): List of file paths attached by the user.
            focused_files (list): List of files the user is currently focused on.

        Returns:
            dict: Development plan or error reason.
        """

        tree = self.repo.print_tree()
    
        messages = [
            {
                "role": "system",
                "content": (
                    "Analyze the user's question, project files, and any attached files meticulously. Provide an answer in this exact JSON format:\n\n"
                    "2. processed_prompt: \n"
                    "   - If not in English, translate to English.\n"
                    "   - Ensure clarity and conciseness while preserving the core message.\n"
                    "   - If the question is ambiguous, request clarification.\n\n"
                    "3. pipeline: \n"
                    "   - Select '1' ONLY if ALL of these conditions are met:\n"
                    "     * The question directly relates to specific files or structures in the current project\n"
                    "     * It requires analysis of the current project's code or architecture\n"
                    "     * You are 100% certain it cannot be answered without referencing the project structure\n"
                    "   - Select '2' for ALL other cases, including but not limited to:\n"
                    "     * Any ambiguous or unclear questions\n"
                    "     * General inquiries not specific to the current project\n"
                    "     * Questions about attached files or images that don't require project context\n"
                    "     * References to 'this image', 'that file', etc., indicating attachments\n"
                    "     * Theoretical questions not directly about the project\n"
                    "     * General life questions, greetings, or casual conversation\n"
                    "     * Generated questions or friendly chat\n"
                    "     * Ambiguous prompts without clear actions\n"
                    "     * Random inputs (numbers, words, etc.)\n"
                    "     * ANY uncertainty about the relevance to the current project structure\n\n"
                    "4. role: \n"
                    "   - Specify the most appropriate expert to address the question.\n"
                    "   - Examples: 'Senior C++ Engineer', 'iOS Development Expert', 'AI Ethics Specialist', etc.\n"
                    "   - Be precise and tailor the role to the question's nature.\n"
                    "   - For multiple experts, list the primary one first.\n"
                    "   - Use 'Conversational AI' or a relevant general expert for broad queries or chat.\n\n"
                    "Adhere strictly to this JSON format:\n"
                    "{\n"
                    '    "role": "Specific Expert Title",\n'
                    '    "pipeline": "1 or 2",\n'
                    "}\n\n"
                    "Ensure JSON correctness. Do not include any text outside the JSON structure."
                )
            },
            {
                "role": "user",
                "content": f"User prompt:\n{user_prompt}\n\Project structure:\n{tree}"
            }
        ]

        if file_attachments:
            messages[-1]["content"] += f"\n\nAttached files:\n{file_attachments}"

        if focused_files:
            messages[-1]["content"] += f"\n\nFocused files:\n{focused_files}"

        try:
            logger.debug("\n #### `SnowX` is initiating:\n A request to the AI for pre-prompt planning")
            response = await self.ai.prompt(messages, 4096, 0, 0)
            logger.debug("\n #### `SnowX` has successfully:\n Received the AI response for pre-prompt planning")
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.debug("\n #### `SnowX` is attempting:\n To repair a JSON decoding error in the AI response")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"  `SnowX` encountered an error:\n While getting the pre-prompt plan\n Error: {e}")
            return {
                "reason": str(e)
            }

    async def get_prePrompt_plans(self, user_prompt, file_attachments, focused_files):
        """
        Get development plans for a list of txt files from Azure OpenAI based on the user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### `SnowX` is beginning:\n The pre-prompt planning process")
        plan = await self.get_prePrompt_plan(user_prompt, file_attachments, focused_files)
        logger.debug("\n #### `SnowX` has finished:\n The pre-prompt planning process")
        return plan
