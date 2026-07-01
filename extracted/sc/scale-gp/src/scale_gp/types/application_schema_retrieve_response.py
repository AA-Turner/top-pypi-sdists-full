# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict
from typing_extensions import TypeAlias

from .application_node_schema_registry_record import ApplicationNodeSchemaRegistryRecord

__all__ = ["ApplicationSchemaRetrieveResponse"]

ApplicationSchemaRetrieveResponse: TypeAlias = Dict[str, ApplicationNodeSchemaRegistryRecord]
