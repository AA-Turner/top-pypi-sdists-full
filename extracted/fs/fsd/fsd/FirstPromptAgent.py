import os
import sys
import json
from json_repair import repair_json
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = get_logger(__name__)

class FirstPromptAgent:
    def __init__(self, repo):
        self.repo = repo
        self.ai = AIGateway()

    async def get_prePrompt_plans(self, user_prompt):
        """
        Get development plans based on the user prompt.

        Args:
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        try:
            logger.info("#### Hi there! `SnowX` is processing your request.")
            messages = self._create_messages(user_prompt)
            response = await self.ai.prompt(messages, 4096, 0.2, 0.1)
            return self._parse_response(response)
        except Exception as e:
            logger.error(f" `SnowX` encountered an error during pre-prompt planning:\n{str(e)}")
            return {"reason": str(e)}

    def _create_messages(self, user_prompt):
        logger.debug("#### `SnowX` is constructing messages for the AI gateway")
        system_content = (
            "You are a senior developer and prompt engineering specialist. "
            "Analyze the user's prompt and respond in JSON format. Follow these guidelines strictly:\n\n"
            "pipeline: Choose the most appropriate pipeline based on the user's prompt. "
            "Respond with a number (1, 2, or 3) for the specific pipeline:\n\n"
            "1. Talkable: Use this for general conversation and non-code related requests.\n"
            "Examples:\n"
            "- 'Explain how React hooks work'\n"
            "- 'What's the difference between REST and GraphQL?'\n"
            "- 'Show me the project structure'\n"
            "- 'Find bugs in this code'\n"
            "- 'Compare these two files'\n"
            "- 'Hello, how are you?'\n"
            "- 'Tell me about Python's history'\n"
            "- 'What are best practices for microservices?'\n\n"
            "2. Actionable: Use this for requests that require actual code changes or project modifications.\n"
            "Examples:\n"
            "- 'Fix the login page error'\n"
            "- 'Create a new API endpoint for user registration'\n"
            "- 'Add authentication to the application'\n"
            "- 'Build a CI/CD pipeline'\n"
            "- 'Implement a caching system'\n"
            "- 'Deploy the application to production'\n"
            "- 'Install and configure Redis'\n"
            "- 'Generate a new logo for the project'\n"
            "- 'Move the authentication logic to a separate service'\n\n"
            "3. Ambiguous: Use this when the request could be interpreted as either talkable or actionable.\n"
            "Examples:\n"
            "- 'Help me with this bug' (needs clarification: discuss or fix?)\n"
            "- 'I need help with the database' (needs clarification: explain or implement?)\n"
            "- 'The API is slow' (needs clarification: analyze or optimize?)\n\n"
            "Key Indicators:\n"
            "Choose '2' (Actionable) if the request contains:\n"
            "- Direct commands: 'fix', 'create', 'add', 'move', 'install', 'run', 'deploy'\n"
            "- Technical implementation details\n"
            "- Specific project modifications\n"
            "- Build or deployment instructions\n"
            "- Code generation requests\n\n"
            "Choose '1' (Talkable) if the request:\n"
            "- Is conversational\n"
            "- Seeks explanations\n"
            "- Requests information\n"
            "- Asks for analysis without changes\n"
            "- Is general discussion\n\n"
            "Choose '3' (Ambiguous) when:\n"
            "- The intent is unclear\n"
            "- Both discussion and action are possible\n"
            "- Human clarification is needed\n\n"
            "Example JSON response:\n"
            '{"pipeline": "1"}\n'
            "Return only a valid JSON response without additional text, symbols, or MARKDOWN."
        )
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"User original prompt:\n{user_prompt}. Return only a valid PLAIN JSON response STRICTLY without additional text, symbols, or MARKDOWN."}
        ]

    def _parse_response(self, response):
        logger.debug("#### `SnowX` is parsing the AI gateway response")
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.error(f" `SnowX` encountered an error and is attempting to repai itself.")
            logger.debug(f"DAMAGE RESPOND: {response.choices[0].message.content}")
            repaired_json = repair_json(response.choices[0].message.content)
            return json.loads(repaired_json)
