r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataCollectionMetricsCountsByState", "DataCollectionMetricsCountsByStateSchema"]
__pdoc__ = {
    "DataCollectionMetricsCountsByStateSchema.resource": False,
    "DataCollectionMetricsCountsByStateSchema.opts": False,
    "DataCollectionMetricsCountsByState": False,
}

class DataCollectionMetricsCountsByStateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataCollectionMetricsCountsByState object"""

    count = Size(data_key="count", allow_none=True)
    r""" The number of data collections in the given state.

Example: 50 """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" State of the data collection:

* <i>draft</i> - The data collection is in draft.
* <i>processing</i> - The data collection is being processed.
* <i>published</i> - The data collection is published.
* <i>failed</i> - The data collection has a failure.
* <i>outdated</i> - The data collection is outdated.
* <i>deleted</i> - The data collection has been marked for deletion.


Valid choices:

* draft
* processing
* published
* failed
* outdated
* deleted """

    @property
    def resource(self):
        return DataCollectionMetricsCountsByState

    gettable_fields = [
        "count",
        "state",
    ]
    """count,state,"""

    patchable_fields = [
        "count",
        "state",
    ]
    """count,state,"""

    postable_fields = [
        "count",
        "state",
    ]
    """count,state,"""


class DataCollectionMetricsCountsByState(Resource):

    _schema = DataCollectionMetricsCountsByStateSchema
