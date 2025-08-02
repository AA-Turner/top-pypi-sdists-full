import urllib.parse
from typing import Optional

import requests

from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.feedback_manager import FeedbackManager


class LLMException(Exception):
    pass


class LLM:
    def __init__(
        self,
        host: str,
        user_token: str,
    ):
        self.host = host
        self.user_token = user_token

    def ask(self, system_prompt: str, prompt: str, feature: Optional[str] = None, model: Optional[str] = None) -> str:
        """
        Calls the model with the given prompt and returns the response.

        Args:
            system_prompt (str): The system prompt to send to the model.
            prompt (str): The user prompt to send to the model.
            feature (Optional[str]): The feature to send to the model.
            model (Optional[str]): The model to use.

        Returns:
            str: The response from the language model.
        """

        data = {"system": system_prompt, "prompt": prompt}
        params = {"origin": "cli"}
        if feature:
            params["feature"] = feature
        if model:
            params["model"] = model
        cli_config = CLIConfig.get_project_config()
        workspace_id = cli_config.get("id")
        params_str = urllib.parse.urlencode(params)
        if workspace_id:
            llm_url = f"{self.host}/v0/llm/{workspace_id}?{params_str}"
        else:
            llm_url = f"{self.host}/v0/llm?{params_str}"
        response = requests.post(
            llm_url,
            headers={"Authorization": f"Bearer {self.user_token}"},
            data=data,
        )

        if not response.ok:
            raise LLMException(FeedbackManager.error(message=response.text))

        return response.json().get("result", "")
