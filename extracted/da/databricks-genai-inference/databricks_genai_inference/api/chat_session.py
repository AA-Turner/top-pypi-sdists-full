""" ChatSession class for multi-turn chat completion management.
"""
import copy

from databricks_genai_inference.api.chat_completion import ChatCompletion


class ChatSession():
    """
    A class representing a chat session with a chat completion model.

    Methods:
        reply(message: str) -> ChatCompletion: Sends a message to the chat model and returns its response.
        system_message() -> str: Returns the system message.
        last() -> str: Returns the last assistant message in the chat history.
        history() -> List: Returns the entire chat history.
        pretty_history() -> str: Returns a formatted string representing the chat history.
        count() -> int: Returns the number of chat rounds conducted so far
    """

    def __init__(self, model: str, system_message=None, **kwargs):
        """Args:
            model (str): The model name.
            system_message (str): The system message to guide the conversation. e.g. "You are a helpful assistant."
            **kwargs: Additional model parameters to pass to the chat completion API.
        """
        self.model = model
        self.parameters = kwargs
        self.chat_history = []
        self.system_message = system_message
        if self.parameters.get("stream", False):
            raise NotImplementedError(
                "You are setting stream=True, but streaming is not supported for ChatSession() yet.")
        if system_message is not None:
            self.chat_history = [{"role": "system", "content": system_message}]

    def reply(self, message: str):
        """
        Sends a message to the chat model and returns its response.

        Args:
            message (str): The message to send to the chat model.

        Returns:
            ChatCompletionObject: An object representing the response from the chat model.
        """
        self.chat_history.append({"role": "user", "content": message})
        response = ChatCompletion.create(model=self.model, messages=copy.deepcopy(self.chat_history), **self.parameters)
        self.chat_history.append({"role": "assistant", "content": response.message})
        return response

    @property
    def last(self):
        """
        Returns the last assistant message in the chat history.

        Returns:
            str: The last assistant message in the chat history.
        """
        if len(self.chat_history) <= 1:
            return ""
        return self.chat_history[-1]["content"]

    @property
    def history(self):
        """
        Returns the entire chat history.

        Returns:
            List: The entire chat history.
        """
        return self.chat_history

    @property
    def pretty_history(self):
        """
        Returns a formatted string representing the chat history.

        Returns:
            str: A formatted string representing the chat history.
        """
        return '\n' + '\n'.join([
            f'{self.chat_history[i]["role"]}: {self.chat_history[i]["content"]}' for i in range(len(self.chat_history))
        ])

    @property
    def count(self):
        """
        Returns the number of chat rounds conducted so far.

        Returns:
            int: The number of chat rounds conducted so far.
        """
        return int(len(self.chat_history) / 2)
