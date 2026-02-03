r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ContainerResponseRecords", "ContainerResponseRecordsSchema"]
__pdoc__ = {
    "ContainerResponseRecordsSchema.resource": False,
    "ContainerResponseRecordsSchema.opts": False,
    "ContainerResponseRecords": False,
}

class ContainerResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerResponseRecords object"""

    provisioning_options = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.container_provisioning_options", "ContainerProvisioningOptionsSchema"),
                unknown=EXCLUDE,
                data_key="provisioning_options",
                allow_none=True
            )
    r""" Options that are applied to the operation. """

    svm = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.svm", "SvmSchema"),
                unknown=EXCLUDE,
                data_key="svm",
                allow_none=True
            )
    r""" The svm field of the container_response_records. """

    use_mirrored_aggregates = marshmallow_fields.Boolean(data_key="use_mirrored_aggregates", allow_none=True)
    r""" Specifies whether mirrored aggregates are selected when provisioning the volume. Only mirrored aggregates are used if this parameter is set to _true_ and only unmirrored aggregates are used if this parameter is set to _false_. The default value is _true_ for a MetroCluster configuration and is _false_ for a non-MetroCluster configuration. """

    volumes = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.container_volume", "ContainerVolumeSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="volumes",
                allow_none=True
                )
    r""" A list of NAS volumes to provision.<br/> """

    @property
    def resource(self):
        return ContainerResponseRecords

    gettable_fields = [
        "volumes",
    ]
    """volumes,"""

    patchable_fields = [
        "volumes",
    ]
    """volumes,"""

    postable_fields = [
        "provisioning_options",
        "svm.name",
        "svm.uuid",
        "use_mirrored_aggregates",
        "volumes",
    ]
    """provisioning_options,svm.name,svm.uuid,use_mirrored_aggregates,volumes,"""


class ContainerResponseRecords(Resource):

    _schema = ContainerResponseRecordsSchema
