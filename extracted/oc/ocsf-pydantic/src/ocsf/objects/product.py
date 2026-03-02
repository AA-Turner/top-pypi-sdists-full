from pydantic import AnyUrl

from .data_classification import DataClassification

from ._entity import Entity
from .feature import Feature

class Product(Entity, DataClassification):
    """
    The Product object describes characteristics of a software product.
    """

    vendor_name: str # The name of the vendor of the product.

    # Recommended:
    version: str | None = None # The version of the product, as defined by the event source. For
                               # example: `2013.1.3-beta`.

    # Optional:
    feature: Feature | None = None
    cpe_name: str | None = None
    lang: str | None = None
    name: str | None = None # The name of the product.
    path: str | None = None # The installation path of the product.
    uid: str | None = None # The unique identifier of the product.
    url_string: AnyUrl | None = None # The URL pointing towards the product.
