from abc import ABC, abstractmethod
import torch
from langchain_huggingface import (
    HuggingFaceEmbeddings
)
from langchain_community.embeddings import (
    HuggingFaceBgeEmbeddings
)
from navconfig.logging import logging
from ...conf import (
    MAX_BATCH_SIZE,
    EMBEDDING_DEVICE,
    EMBEDDING_DEFAULT_MODEL
)

class AbstractStore(ABC):
    """AbstractStore class.

    Args:
        embedding_model (dict): Embeddings.
    """
    def __init__(self, *args, **kwargs):
        self.embedding_model: dict = kwargs.pop(
            'embedding_model',
            self._default_embedding_model()
        )
        self.logger = logging.getLogger(__name__)
        self._metric_type: str = kwargs.pop("metric_type", self._default_metric())
        self._index_type: str = kwargs.pop("index_type", self._default_index())
        self._dimension: int = kwargs.pop('dimension', 768)
        self.vector_field: str = kwargs.pop('vector_field', 'vector')
        self.text_field: str = kwargs.pop('text_field', 'text')
        self.database: str = kwargs.pop('database', 'default')
        super().__init__(*args, **kwargs)
        # Embedding Model
        self._embed_ = None
        self._connection = None

    def _default_metric(self) -> str:
        return 'COSINE'

    def _default_index(self) -> str:
        return 'IVF_FLAT'

    def _default_embedding_model(self) -> dict:
        return {
            "model_name": "sentence-transformers/paraphrase-MiniLM-L6-v2",
            "model_type": "transformers"
        }

    def _get_device(self, device_type: str = None, cuda_number: int = 0):
        """Get Default device for Torch and transformers.

        """
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        if device_type:
            return torch.device(device_type)
        if device_type == 'cpu' or EMBEDDING_DEVICE == 'cpu':
            return torch.device('cpu')
        if torch.cuda.is_available():
            # Use CUDA GPU if available
            return torch.device(f'cuda:{cuda_number}')
        if torch.backends.mps.is_available():
            # Use CUDA Multi-Processing Service if available
            return torch.device("mps")
        if EMBEDDING_DEVICE == 'cuda':
            return torch.device(f'cuda:{cuda_number}')
        else:
            return torch.device(EMBEDDING_DEVICE)

    def create_embedding(
        self,
        embedding_model: dict
    ):
        encode_kwargs: str = {
            'normalize_embeddings': True,
            "batch_size": MAX_BATCH_SIZE
        }
        device = self._get_device()
        model_kwargs: str = {'device': device}
        model_name = embedding_model.get('model_name', EMBEDDING_DEFAULT_MODEL)
        model_type = embedding_model.get('model_type', 'transformers')
        if model_type == 'bge':
            return HuggingFaceBgeEmbeddings(
                model_name=model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs
            )
        else:
            return HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs
            )

    def get_default_embedding(
        self,
        model_name: str = EMBEDDING_DEFAULT_MODEL
    ):
        return self.create_embedding(model_name=model_name)

    @abstractmethod
    async def load_documents(
        self,
        documents: list,
        collection: str = None
    ):
        pass

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    async def __aenter__(self):
        if self._embed_ is None:
            self._embed_ = self.create_embedding(
                self.embedding_model
            )
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        # closing Embedding
        self._embed_ = None
        try:
            await self.disconnect()
        except RuntimeError:
            pass
