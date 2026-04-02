"""Another simple class wrapper for interacting with Discord webhooks."""

from .client import UserAgent, Webhook, WebhookResponse
from .embed import Author, Embed, Field, Footer, Image, Thumbnail

__version__ = "1.1.0"

__all__ = [
    "UserAgent",
    "Webhook",
    "WebhookResponse",
    "Author",
    "Embed",
    "Field",
    "Footer",
    "Image",
    "Thumbnail",
]
