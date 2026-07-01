"""Embeddings generation for vector search."""

import os
import logging
from typing import List, Optional, Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)


# Default embedding models per provider
DEFAULT_EMBEDDING_MODELS = {
    "openai": "text-embedding-3-small",  # 1536 dimensions
    "cohere": "embed-english-v3.0",      # 1024 dimensions
    "huggingface": "all-MiniLM-L6-v2",  # 384 dimensions
}


class EmbeddingProvider(str, Enum):
    """Supported embedding providers."""
    OPENAI = "openai"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    

class EmbeddingService:
    """Service for generating embeddings from text."""
    
    def __init__(self, provider: EmbeddingProvider = EmbeddingProvider.OPENAI):
        """Initialize embedding service.
        
        Args:
            provider: Which embedding provider to use
        """
        self.provider = provider
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the embedding client based on provider."""
        if self.provider == EmbeddingProvider.OPENAI:
            try:
                import openai
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    logger.warning("OPENAI_API_KEY not set. Embedding generation will fail.")
                self._client = openai.OpenAI(api_key=api_key)
            except ImportError:
                logger.error("OpenAI package not installed. Run: uv add openai")
                raise
        elif self.provider == EmbeddingProvider.COHERE:
            try:
                import cohere
                api_key = os.getenv("COHERE_API_KEY")
                if not api_key:
                    logger.warning("COHERE_API_KEY not set. Embedding generation will fail.")
                self._client = cohere.Client(api_key)
            except ImportError:
                logger.error("Cohere package not installed. Run: uv add cohere")
                raise
        else:
            raise NotImplementedError(f"Provider {self.provider} not yet implemented")
    
    def get_default_model(self) -> str:
        """Get the default embedding model for the current provider.
        
        Returns:
            Default model name for the provider
        """
        return DEFAULT_EMBEDDING_MODELS.get(self.provider.value, "")
    
    async def generate_embedding(self, text: str, model: Optional[str] = None) -> List[float]:
        """Generate embedding for a single text.
        
        Args:
            text: Text to embed
            model: Optional model override
            
        Returns:
            List of floats representing the embedding vector
        """
        if not text:
            return []
            
        if self.provider == EmbeddingProvider.OPENAI:
            model = model or DEFAULT_EMBEDDING_MODELS[self.provider.value]
            try:
                response = self._client.embeddings.create(
                    model=model,
                    input=text
                )
                return response.data[0].embedding
            except Exception as e:
                logger.error(f"Failed to generate OpenAI embedding: {e}")
                raise
                
        elif self.provider == EmbeddingProvider.COHERE:
            model = model or DEFAULT_EMBEDDING_MODELS[self.provider.value]
            try:
                response = self._client.embed(
                    texts=[text],
                    model=model,
                    input_type="search_document"
                )
                return response.embeddings[0]
            except Exception as e:
                logger.error(f"Failed to generate Cohere embedding: {e}")
                raise
        
        else:
            raise NotImplementedError(f"Provider {self.provider} not yet implemented")
    
    async def generate_embeddings(self, texts: List[str], model: Optional[str] = None) -> List[List[float]]:
        """Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            model: Optional model override
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
            
        if self.provider == EmbeddingProvider.OPENAI:
            model = model or DEFAULT_EMBEDDING_MODELS[self.provider.value]
            try:
                response = self._client.embeddings.create(
                    model=model,
                    input=texts
                )
                return [item.embedding for item in response.data]
            except Exception as e:
                logger.error(f"Failed to generate OpenAI embeddings: {e}")
                raise
                
        elif self.provider == EmbeddingProvider.COHERE:
            model = model or DEFAULT_EMBEDDING_MODELS[self.provider.value]
            try:
                response = self._client.embed(
                    texts=texts,
                    model=model,
                    input_type="search_document"
                )
                return response.embeddings
            except Exception as e:
                logger.error(f"Failed to generate Cohere embeddings: {e}")
                raise
        
        else:
            raise NotImplementedError(f"Provider {self.provider} not yet implemented")
    
    async def generate_query_embedding(self, query: str, model: Optional[str] = None) -> List[float]:
        """Generate embedding for a search query.
        
        Some providers have different handling for queries vs documents.
        
        Args:
            query: Search query text
            model: Optional model override
            
        Returns:
            Embedding vector for the query
        """
        if self.provider == EmbeddingProvider.COHERE:
            model = model or DEFAULT_EMBEDDING_MODELS[self.provider.value]
            try:
                response = self._client.embed(
                    texts=[query],
                    model=model,
                    input_type="search_query"  # Different from documents
                )
                return response.embeddings[0]
            except Exception as e:
                logger.error(f"Failed to generate Cohere query embedding: {e}")
                raise
        else:
            # For other providers, queries and documents are handled the same
            return await self.generate_embedding(query, model)


# Singleton instance
_embedding_service = None


def get_embedding_service(provider: Optional[EmbeddingProvider] = None) -> EmbeddingService:
    """Get or create the embedding service singleton.
    
    Args:
        provider: Optional provider override
        
    Returns:
        EmbeddingService instance
    """
    global _embedding_service
    
    if _embedding_service is None or (provider and provider != _embedding_service.provider):
        provider = provider or EmbeddingProvider.OPENAI
        _embedding_service = EmbeddingService(provider)
    
    return _embedding_service


if __name__ == "__main__":
    import asyncio
    
    async def test_embeddings():
        """Test embedding generation functionality."""
        print("=== Embedding Service Test ===\n")
        
        # Check environment
        provider = os.getenv("EMBEDDING_PROVIDER", "openai").lower()
        print(f"Provider: {provider}")
        print(f"Default model: {DEFAULT_EMBEDDING_MODELS.get(provider, 'N/A')}")
        
        # Check API keys
        if provider == "openai" and not os.getenv("OPENAI_API_KEY"):
            print("\nERROR: OPENAI_API_KEY not set. Please set it to test embeddings.")
            print("Example: export OPENAI_API_KEY=your-api-key")
            return
        elif provider == "cohere" and not os.getenv("COHERE_API_KEY"):
            print("\nERROR: COHERE_API_KEY not set. Please set it to test embeddings.")
            print("Example: export COHERE_API_KEY=your-api-key")
            return
        
        try:
            # Initialize service
            print("\n--- Initializing Embedding Service ---")
            service = get_embedding_service()
            print(f"✓ Service initialized with provider: {service.provider}")
            print(f"✓ Default model: {service.get_default_model()}")
            
            # Test single embedding
            print("\n--- Testing Single Text Embedding ---")
            test_text = "Weather forecasting API with real-time data"
            embedding = await service.generate_embedding(test_text)
            print(f"Input text: '{test_text}'")
            print(f"✓ Embedding dimensions: {len(embedding)}")
            print(f"✓ First 5 values: {embedding[:5]}")
            
            # Test multiple embeddings
            print("\n--- Testing Multiple Text Embeddings ---")
            test_texts = [
                "Machine learning for data analysis",
                "API integration tools",
                "Real-time weather monitoring"
            ]
            embeddings = await service.generate_embeddings(test_texts)
            print(f"Input texts: {len(test_texts)} texts")
            for i, text in enumerate(test_texts):
                print(f"  {i+1}. '{text}' -> {len(embeddings[i])} dimensions")
            
            # Test query embedding
            print("\n--- Testing Query Embedding ---")
            query = "climate prediction services"
            query_embedding = await service.generate_query_embedding(query)
            print(f"Query: '{query}'")
            print(f"✓ Query embedding dimensions: {len(query_embedding)}")
            
            # Test similarity (cosine similarity between doc and query)
            print("\n--- Testing Semantic Similarity ---")
            import numpy as np
            
            # Calculate cosine similarity
            def cosine_similarity(a, b):
                return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
            
            # Compare query with test texts
            print(f"Query: '{query}'")
            for i, (text, emb) in enumerate(zip(test_texts, embeddings)):
                similarity = cosine_similarity(query_embedding, emb)
                print(f"  vs '{text}': {similarity:.3f}")
            
            print("\n✓ All tests passed!")
            
        except ImportError as e:
            print(f"\n✗ Import error: {e}")
            print("Please install the required package:")
            if "openai" in str(e):
                print("  uv add openai")
            elif "cohere" in str(e):
                print("  uv add cohere")
            elif "numpy" in str(e):
                print("  uv add numpy")
                
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Run the test
    print("Testing embedding service...")
    print(f"ENABLE_EMBEDDINGS: {os.getenv('ENABLE_EMBEDDINGS', 'false')}")
    print(f"EMBEDDING_PROVIDER: {os.getenv('EMBEDDING_PROVIDER', 'openai')}")
    print()
    
    asyncio.run(test_embeddings()) 