from abc import ABC
import asyncio
from google.cloud import language_v1
from google.auth.exceptions import GoogleAuthError
from .GoogleClient import GoogleClient
from ..exceptions import ComponentError


class GoogleLanguage(GoogleClient, ABC):
    """
    Google Cloud Natural Language Client for analyzing text for 
    sentiment, entities, syntax, and content classification.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = None

    async def get_client(self):
        """Get the Natural Language client, with caching."""
        if not self._client:
            try:
                self._client = await asyncio.to_thread(language_v1.LanguageServiceClient, credentials=self.credentials)
            except GoogleAuthError as e:
                raise ComponentError(f"Google Natural Language API authentication error: {e}")
        return self._client

    async def analyze_sentiment(self, text: str):
        """
        Analyze the sentiment of the provided text.

        Args:
            text (str): The text to analyze.

        Returns:
            dict: Sentiment score and magnitude.
        """
        client = await self.get_client()
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = await asyncio.to_thread(client.analyze_sentiment, document=document)
        sentiment = response.document_sentiment
        return {"score": sentiment.score, "magnitude": sentiment.magnitude}

    async def analyze_entities(self, text: str):
        """
        Analyze entities in the provided text.

        Args:
            text (str): The text to analyze.

        Returns:
            list: A list of entities with their types and salience scores.
        """
        client = await self.get_client()
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = await asyncio.to_thread(client.analyze_entities, document=document)
        
        entities = []
        for entity in response.entities:
            entities.append({
                "name": entity.name,
                "type": language_v1.Entity.Type(entity.type_).name,
                "salience": entity.salience,
                "metadata": entity.metadata,
            })
        return entities

    async def analyze_syntax(self, text: str):
        """
        Analyze syntax of the provided text.

        Args:
            text (str): The text to analyze.

        Returns:
            list: A list of tokens with their parts of speech and dependency relationships.
        """
        client = await self.get_client()
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = await asyncio.to_thread(client.analyze_syntax, document=document)
        
        tokens = []
        for token in response.tokens:
            tokens.append({
                "text": token.text.content,
                "part_of_speech": language_v1.PartOfSpeech.Tag(token.part_of_speech.tag).name,
                "dependency_edge": {
                    "head_token_index": token.dependency_edge.head_token_index,
                    "label": language_v1.DependencyEdge.Label(token.dependency_edge.label).name,
                }
            })
        return tokens

    async def classify_text(self, text: str):
        """
        Classify the content of the provided text into categories.

        Args:
            text (str): The text to classify.

        Returns:
            list: A list of categories with confidence scores.
        """
        client = await self.get_client()
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = await asyncio.to_thread(client.classify_text, document=document)

        categories = []
        for category in response.categories:
            categories.append({
                "name": category.name,
                "confidence": category.confidence,
            })
        return categories
