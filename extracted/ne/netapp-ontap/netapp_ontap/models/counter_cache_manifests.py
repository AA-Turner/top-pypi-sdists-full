r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["CounterCacheManifests", "CounterCacheManifestsSchema"]
__pdoc__ = {
    "CounterCacheManifestsSchema.resource": False,
    "CounterCacheManifestsSchema.opts": False,
    "CounterCacheManifests": False,
}

class CounterCacheManifestsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CounterCacheManifests object"""

    preset = marshmallow_fields.Str(data_key="preset", allow_none=True)
    r""" The name of the preset.

Example: _cm2_workload_overview """

    preset_details = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.counter_cache_preset_detail", "CounterCachePresetDetailSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="preset_details",
                allow_none=True
                )
    r""" The collection of retrieved cached metrics manifests. """

    @property
    def resource(self):
        return CounterCacheManifests

    gettable_fields = [
        "preset",
        "preset_details",
    ]
    """preset,preset_details,"""

    patchable_fields = [
        "preset",
        "preset_details",
    ]
    """preset,preset_details,"""

    postable_fields = [
        "preset",
        "preset_details",
    ]
    """preset,preset_details,"""


class CounterCacheManifests(Resource):

    _schema = CounterCacheManifestsSchema
