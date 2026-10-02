"""EmbeddingObject class.
"""
from databricks_genai_inference.api.abstract.foundation_model_object import FoundationModelObject


class EmbeddingObject(FoundationModelObject):
    """
    A class representing an embedding response object.
    """

    @property
    def embeddings(self):
        """
        Returns the embedding content from the chat completion API response.

        Returns:
            List: The embedding content.
        """
        return [data['embedding'] for data in self.response['data']]
