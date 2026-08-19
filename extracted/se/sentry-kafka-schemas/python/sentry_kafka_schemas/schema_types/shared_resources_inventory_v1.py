from typing import Required, Union, Literal, TypedDict


class SharedResourcesInventory(TypedDict, total=False):
    """ shared_resources_inventory. """

    shared_resource_id: Required[str]
    """
    Identifies the shared resource this record belongs to. Matches the shared_resource_id label on the billed GCP resource.

    Required property
    """

    app_feature: Required[str]
    """
    The product feature this record is attributed to.

    Required property
    """

    op_type: Required["_SharedResourcesInventoryOpType"]
    """
    WRITE creates or replaces a record. UPDATE mutates fields of an existing record without changing its stored size (to, for example, extend an expiration deadline). DELETE removes it.

    Required property
    """

    record_id: Required[str]
    """
    Opaque stable identifier for the stored record, unique within a shared_resource_id. It is recommended that producers use a hash (e.g. BLAKE3) of some app-level ID. Once decided, it shouldn't be changed.

    Required property
    """

    timestamp: Required[int]
    """
    Unix epoch microseconds at which the operation occurred. NOTE: this differs from shared-resources-usage, which uses epoch seconds. Microsecond resolution keeps same-instant collisions rare enough that ordering per record_id can be resolved by timestamp plus a fixed op_type precedence.

    Required property
    """

    sample_rate: Required[Union[int, float]]
    """
    Proportion of records the producer is emitting for this shared_resource_id. Producers that emit every record set this to 1. Consumers/pipelines may use `1 / sample_rate` as a weight when computing rollups to keep the rollup proportionally stable even when sample_rate changes.

    exclusiveMinimum: 0
    maximum: 1

    Required property
    """

    size: Union[int, None]
    """ Stored size in bytes. Required for op_type=WRITE. Omitted for DELETE, and for UPDATE when the size is unchanged. """

    expiration_time: Union[int, None]
    """ Unix epoch microseconds at which the record is expected to be reclaimed by the backend, if known. Backends that expire records without notifying the producer rely on this for downstream removal. """

    organization_id: Union[int, None]
    """ Sentry organization ID the record is attributed to, if known. """

    project_id: Union[int, None]
    """ Sentry project ID the record is attributed to, if known. """



_SharedResourcesInventoryOpType = Union[Literal['WRITE'], Literal['UPDATE'], Literal['DELETE']]
""" WRITE creates or replaces a record. UPDATE mutates fields of an existing record without changing its stored size (to, for example, extend an expiration deadline). DELETE removes it. """
_SHAREDRESOURCESINVENTORYOPTYPE_WRITE: Literal['WRITE'] = "WRITE"
"""The values for the 'WRITE creates or replaces a record. UPDATE mutates fields of an existing record without changing its stored size (to, for example, extend an expiration deadline). DELETE removes it' enum"""
_SHAREDRESOURCESINVENTORYOPTYPE_UPDATE: Literal['UPDATE'] = "UPDATE"
"""The values for the 'WRITE creates or replaces a record. UPDATE mutates fields of an existing record without changing its stored size (to, for example, extend an expiration deadline). DELETE removes it' enum"""
_SHAREDRESOURCESINVENTORYOPTYPE_DELETE: Literal['DELETE'] = "DELETE"
"""The values for the 'WRITE creates or replaces a record. UPDATE mutates fields of an existing record without changing its stored size (to, for example, extend an expiration deadline). DELETE removes it' enum"""

