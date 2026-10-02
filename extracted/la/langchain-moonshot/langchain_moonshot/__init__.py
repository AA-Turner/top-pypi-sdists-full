"""LangChain Moonshot integration."""

from importlib import metadata

from langchain_moonshot.chat_models import ChatMoonshot

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    __version__ = ""
del metadata

__all__ = [
    "ChatMoonshot",
    "__version__",
]
