"""CompletionObject class.
"""
from databricks_genai_inference.api.abstract.foundation_model_object import FoundationModelObject


class CompletionObject(FoundationModelObject):
    """
    A class representing a completion response object.
    """

    @property
    def text(self):
        """
        Returns the text content from the chat completion API response.

        Returns:
            List[str]: The text content.
        """
        return [data['text'] for data in self.response['choices']]
