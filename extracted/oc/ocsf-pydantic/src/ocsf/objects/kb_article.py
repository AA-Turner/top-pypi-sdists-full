from datetime import datetime
from pydantic import BaseModel, AnyUrl

from .os import OperatingSystem
from .product import Product


class KBArticle(BaseModel):
    """
    The KB Article object contains metadata that describes the patch or update.
    """

    uid: str # The unique identifier for the kb article.

    # Recommended:
    title: str | None = None # The title of the kb article.
    os: OperatingSystem | None = None # The operating system the kb article applies.
    severity: str | None = None # The severity of the kb article.

    # Optional:
    bulletin: str | None = None # The kb article bulletin identifier.
    product: Product | None = None # The product details the kb article applies.
    is_superseded: bool | None = None # The kb article has been replaced by another.
    created_time: datetime | None = None # The date the kb article was released by the vendor.
    size: int | None = None # The size in bytes for the kb article.
    src_url: AnyUrl | None = None # The kb article link from the source vendor.
    classification: str | None = None # The vendors classification of the kb article.
