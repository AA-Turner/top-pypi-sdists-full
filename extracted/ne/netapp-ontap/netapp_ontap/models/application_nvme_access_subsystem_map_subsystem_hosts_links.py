r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ApplicationNvmeAccessSubsystemMapSubsystemHostsLinks", "ApplicationNvmeAccessSubsystemMapSubsystemHostsLinksSchema"]
__pdoc__ = {
    "ApplicationNvmeAccessSubsystemMapSubsystemHostsLinksSchema.resource": False,
    "ApplicationNvmeAccessSubsystemMapSubsystemHostsLinksSchema.opts": False,
    "ApplicationNvmeAccessSubsystemMapSubsystemHostsLinks": False,
}

class ApplicationNvmeAccessSubsystemMapSubsystemHostsLinksSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationNvmeAccessSubsystemMapSubsystemHostsLinks object"""

    self_ = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                unknown=EXCLUDE,
                data_key="self",
                allow_none=True
            )
    r""" The self_ field of the application_nvme_access_subsystem_map_subsystem_hosts_links. """

    @property
    def resource(self):
        return ApplicationNvmeAccessSubsystemMapSubsystemHostsLinks

    gettable_fields = [
        "self_",
    ]
    """self_,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationNvmeAccessSubsystemMapSubsystemHostsLinks(Resource):

    _schema = ApplicationNvmeAccessSubsystemMapSubsystemHostsLinksSchema
