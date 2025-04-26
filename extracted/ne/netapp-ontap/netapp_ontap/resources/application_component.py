r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["ApplicationComponent", "ApplicationComponentSchema"]
__pdoc__ = {
    "ApplicationComponentSchema.resource": False,
    "ApplicationComponentSchema.opts": False,
}


class ApplicationComponentSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationComponent object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the application_component."""

    application = marshmallow_fields.Nested("netapp_ontap.models.application_component_application.ApplicationComponentApplicationSchema", data_key="application", unknown=EXCLUDE, allow_none=True)
    r""" The application field of the application_component."""

    backing_storage = marshmallow_fields.Nested("netapp_ontap.models.application_backing_storage.ApplicationBackingStorageSchema", data_key="backing_storage", unknown=EXCLUDE, allow_none=True)
    r""" The backing_storage field of the application_component."""

    cifs_access = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_cifs_properties.ApplicationCifsPropertiesSchema", unknown=EXCLUDE, allow_none=True), data_key="cifs_access", allow_none=True)
    r""" The cifs_access field of the application_component."""

    file_system = marshmallow_fields.Str(
        data_key="file_system",
        validate=enum_validation(['m1fs', 'xfs', 'generic']),
        allow_none=True,
    )
    r""" Defines the type of file system that will be installed on this application component.

Valid choices:

* m1fs
* xfs
* generic"""

    host_management_url = marshmallow_fields.Str(
        data_key="host_management_url",
        allow_none=True,
    )
    r""" Host management URL"""

    host_name = marshmallow_fields.Str(
        data_key="host_name",
        allow_none=True,
    )
    r""" L2 Host FQDN"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Application component name"""

    nfs_access = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_nfs_properties.ApplicationNfsPropertiesSchema", unknown=EXCLUDE, allow_none=True), data_key="nfs_access", allow_none=True)
    r""" The nfs_access field of the application_component."""

    nvme_access = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_nvme_access.ApplicationNvmeAccessSchema", unknown=EXCLUDE, allow_none=True), data_key="nvme_access", allow_none=True)
    r""" Application NVME access"""

    protection_groups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_protection_groups.ApplicationProtectionGroupsSchema", unknown=EXCLUDE, allow_none=True), data_key="protection_groups", allow_none=True)
    r""" The protection_groups field of the application_component."""

    san_access = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_san_access.ApplicationSanAccessSchema", unknown=EXCLUDE, allow_none=True), data_key="san_access", allow_none=True)
    r""" The san_access field of the application_component."""

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.application_component_storage_service.ApplicationComponentStorageServiceSchema", data_key="storage_service", unknown=EXCLUDE, allow_none=True)
    r""" The storage_service field of the application_component."""

    svm = marshmallow_fields.Nested("netapp_ontap.models.application_component_svm.ApplicationComponentSvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the application_component."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The application component UUID. Valid in URL."""

    @property
    def resource(self):
        return ApplicationComponent

    gettable_fields = [
        "links",
        "application",
        "backing_storage",
        "cifs_access",
        "file_system",
        "host_management_url",
        "host_name",
        "name",
        "nfs_access",
        "nvme_access",
        "protection_groups",
        "san_access",
        "storage_service",
        "svm",
        "uuid",
    ]
    """links,application,backing_storage,cifs_access,file_system,host_management_url,host_name,name,nfs_access,nvme_access,protection_groups,san_access,storage_service,svm,uuid,"""

    patchable_fields = [
        "backing_storage",
        "cifs_access",
        "nfs_access",
        "nvme_access",
        "protection_groups",
        "san_access",
    ]
    """backing_storage,cifs_access,nfs_access,nvme_access,protection_groups,san_access,"""

    postable_fields = [
        "backing_storage",
        "cifs_access",
        "nfs_access",
        "nvme_access",
        "protection_groups",
        "san_access",
    ]
    """backing_storage,cifs_access,nfs_access,nvme_access,protection_groups,san_access,"""

class ApplicationComponent(Resource):
    r""" Application component """

    _schema = ApplicationComponentSchema
    _path = "/api/application/applications/{application[uuid]}/components"
    _keys = ["application.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves application components.
### Overview
The application component object exposes how to access an application. Most application interfaces abstract away the underlying ONTAP storage elements, but this interface exposes what is necessary to connect to and uses the storage that is provisioned for an application. See the application component model for a detailed description of each property.
### Query examples
Queries are limited on this API. Most of the details are nested under the `nfs_access`, `cifs_access`, or `san_access` properties, but those properties do not support queries, and properties nested under those properties cannot be requested individually in the current release.<br/>
The following query returns all application components with names beginning in _secondary_.<br/><br/>
```
GET /application/applications/{application.uuid}/components?name=secondary*
```
<br/>The following query returns all application components at the _extreme_ storage service.<br/><br/>
```
GET /application/applications/{application.uuid}/components?storage_service.name=extreme
```
### Learn more
* [`DOC /application`](#docs-application-overview)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all ApplicationComponent resources that match the provided query"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)


    @classmethod
    def fast_get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["RawResource"]:
        """Returns a list of RawResources that represent ApplicationComponent resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves application components.
### Overview
The application component object exposes how to access an application. Most application interfaces abstract away the underlying ONTAP storage elements, but this interface exposes what is necessary to connect to and uses the storage that is provisioned for an application. See the application component model for a detailed description of each property.
### Query examples
Queries are limited on this API. Most of the details are nested under the `nfs_access`, `cifs_access`, or `san_access` properties, but those properties do not support queries, and properties nested under those properties cannot be requested individually in the current release.<br/>
The following query returns all application components with names beginning in _secondary_.<br/><br/>
```
GET /application/applications/{application.uuid}/components?name=secondary*
```
<br/>The following query returns all application components at the _extreme_ storage service.<br/><br/>
```
GET /application/applications/{application.uuid}/components?storage_service.name=extreme
```
### Learn more
* [`DOC /application`](#docs-application-overview)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an application component.
### Overview
The application component object exposes how to access an application. Most application interfaces abstract away the underlying ONTAP storage elements, but this interface exposes what is necessary to connect to and uses the storage that is provisioned for an application. See the application component model for a detailed description of each property.
### Access
Each application component can be accessed via NFS, CIFS, or SAN. NFS and CIFS access can be enabled simultaneously. Each access section includes a `backing_storage` property. This property is used to correlate the storage elements with the access elements of the application. The `backing_storage` portion of the access section provides the `type` and `uuid` of the backing storage. There is another `backing_storage` property at the same level as the access properties which contains lists of backing storage elements corresponding to the types listed in the access section.
### Learn more
* [`DOC /application`](#docs-application-overview)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





