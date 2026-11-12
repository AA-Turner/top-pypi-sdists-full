"""The Chat aggregate's store. The other asset services (`AssetService` and its subclasses) were retired (ENG-406): each module
builds its cached repository from its collection (`redis/`, `mongo/`)."""

from .chat_service import ChatAssetService

__all__ = ['ChatAssetService']
