from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any, Optional, List

class AbstractModelManager(ABC):
    """Abstract base class for model management."""

    @abstractmethod
    def __init__(
        self,
        model_id: str,
        internal_server_type: str,
        internal_port: int,
        internal_host: str,
        action_tracker: Any,
        num_model_instances: int = 1,
    ):
        """Initialize the model manager.

        Args:
            model_id: ID of the model.
            internal_server_type: Type of internal server.
            internal_port: Internal port number.
            internal_host: Internal host address.
            action_tracker: Tracker for monitoring actions.
            num_model_instances: Number of model instances to create.
        """
        pass

    @abstractmethod
    def get_model(self) -> Any:
        """Get a model instance for inference."""
        pass

    @abstractmethod
    def inference(
        self,
        input1: Any,
        input2: Optional[Any] = None,
        extra_params: Optional[Dict[str, Any]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        input_hash: Optional[str] = None,
    ) -> Tuple[Any, bool]:
        """Perform single inference."""
        pass

    @abstractmethod
    def batch_inference(
        self,
        input1: List[Any],
        input2: Optional[List[Any]] = None,
        extra_params: Optional[Dict[str, Any]] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        input_hash: Optional[str] = None,
    ) -> Tuple[List[Any], bool]:
        """Perform batch inference."""
        pass