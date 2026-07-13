"""A wrapper for sending messages to Discord webhooks."""

from dhooks_lite.client import UserAgent, Webhook, WebhookResponse
from dhooks_lite.embed import Author, Embed, Field, Footer, Image, Thumbnail

__version__ = "2.0.0"
__title__ = "dhooks_lite"
__url__ = "https://github.com/AllianceAuth-Apps/dhooks-lite"

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
