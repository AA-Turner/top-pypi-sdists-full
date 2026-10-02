"""ChatCompletionObject class.
"""
from databricks_genai_inference.api.abstract.foundation_model_object import FoundationModelObject


class ChatCompletionObject(FoundationModelObject):
    """
    A class representing a chat completion response object.
    """

    @property
    def message(self):
        """
        Returns the message content from the chat completion API response.

        Returns:
            str: The message content.
        """
        return self.response['choices'][0]['message']['content']
