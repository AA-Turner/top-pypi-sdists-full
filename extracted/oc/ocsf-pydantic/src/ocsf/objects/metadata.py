from datetime import datetime

from ocsf import OCSF_VERSION

from .data_classification import DataClassification

from .product import Product
from .logger import Logger
from .extension import SchemaExtension

class Metadata(DataClassification):
    """
    The Metadata object describes the metadata associated with the event
    """

    product: Product
    version: str = OCSF_VERSION # The version of the OCSF schema, using Semantic Versioning
                                # Specification (https://semver.org)
                                # For example: 1.0.0. Event consumers use the version to determine
                                # the available event attributes.

    # Recommended:
    log_name: str | None = None
    log_provider: str | None = None
    original_time: str | None = None
    tenant_uid: str | None = None

    # Optional:
    correlation_uid: str | None = None
    event_code: str | None = None
    extension: SchemaExtension | None = None
    extensions: list[SchemaExtension] | None = None
    labels: list[str] | None = None # The list of category labels attached to the event or specific
                                    # attributes. Labels are user defined tags or aliases added at
                                    # normalization time
                                    # For example: `["network", "connection.ip:destination", "device.ip:source"]`
    log_level: str | None = None
    log_version: str | None = None
    logged_time: datetime | None = None
    modified_time: datetime | None = None # The time when the event was last modified or enriched.
    loggers: list[Logger] | None = None
    processed_time: datetime | None = None
    profiles: list[str] | None = None
    sequence: int | None = None
    uid: str | None = None # The logging system-assigned unique identifier of an event instance.
