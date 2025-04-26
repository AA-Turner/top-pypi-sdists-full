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


__all__ = ["ApplicationTemplate", "ApplicationTemplateSchema"]
__pdoc__ = {
    "ApplicationTemplateSchema.resource": False,
    "ApplicationTemplateSchema.opts": False,
}


class ApplicationTemplateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationTemplate object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the application_template."""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" Description."""

    missing_prerequisites = marshmallow_fields.Str(
        data_key="missing_prerequisites",
        allow_none=True,
    )
    r""" Missing prerequisites."""

    mongo_db_on_san = marshmallow_fields.Nested("netapp_ontap.models.mongo_db_on_san.MongoDbOnSanSchema", data_key="mongo_db_on_san", unknown=EXCLUDE, allow_none=True)
    r""" MongoDB using SAN."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Template name."""

    nas = marshmallow_fields.Nested("netapp_ontap.models.nas.NasSchema", data_key="nas", unknown=EXCLUDE, allow_none=True)
    r""" A generic NAS application."""

    nvme = marshmallow_fields.Nested("netapp_ontap.models.zapp_nvme.ZappNvmeSchema", data_key="nvme", unknown=EXCLUDE, allow_none=True)
    r""" An NVME application."""

    oracle_on_nfs = marshmallow_fields.Nested("netapp_ontap.models.oracle_on_nfs.OracleOnNfsSchema", data_key="oracle_on_nfs", unknown=EXCLUDE, allow_none=True)
    r""" Oracle using NFS."""

    oracle_on_san = marshmallow_fields.Nested("netapp_ontap.models.oracle_on_san.OracleOnSanSchema", data_key="oracle_on_san", unknown=EXCLUDE, allow_none=True)
    r""" Oracle using SAN."""

    oracle_rac_on_nfs = marshmallow_fields.Nested("netapp_ontap.models.oracle_rac_on_nfs.OracleRacOnNfsSchema", data_key="oracle_rac_on_nfs", unknown=EXCLUDE, allow_none=True)
    r""" Oracle RAC using NFS."""

    oracle_rac_on_san = marshmallow_fields.Nested("netapp_ontap.models.oracle_rac_on_san.OracleRacOnSanSchema", data_key="oracle_rac_on_san", unknown=EXCLUDE, allow_none=True)
    r""" Oracle RAC using SAN."""

    protocol = marshmallow_fields.Str(
        data_key="protocol",
        validate=enum_validation(['nas', 'nvme', 's3', 'san']),
        allow_none=True,
    )
    r""" Access protocol.

Valid choices:

* nas
* nvme
* s3
* san"""

    s3_bucket = marshmallow_fields.Nested("netapp_ontap.models.zapp_s3_bucket.ZappS3BucketSchema", data_key="s3_bucket", unknown=EXCLUDE, allow_none=True)
    r""" A generic S3 bucket application."""

    san = marshmallow_fields.Nested("netapp_ontap.models.san.SanSchema", data_key="san", unknown=EXCLUDE, allow_none=True)
    r""" A generic SAN application."""

    sql_on_san = marshmallow_fields.Nested("netapp_ontap.models.sql_on_san.SqlOnSanSchema", data_key="sql_on_san", unknown=EXCLUDE, allow_none=True)
    r""" Microsoft SQL using SAN."""

    sql_on_smb = marshmallow_fields.Nested("netapp_ontap.models.sql_on_smb.SqlOnSmbSchema", data_key="sql_on_smb", unknown=EXCLUDE, allow_none=True)
    r""" Microsoft SQL using SMB."""

    vdi_on_nas = marshmallow_fields.Nested("netapp_ontap.models.vdi_on_nas.VdiOnNasSchema", data_key="vdi_on_nas", unknown=EXCLUDE, allow_none=True)
    r""" A VDI application using NAS."""

    vdi_on_san = marshmallow_fields.Nested("netapp_ontap.models.vdi_on_san.VdiOnSanSchema", data_key="vdi_on_san", unknown=EXCLUDE, allow_none=True)
    r""" A VDI application using SAN."""

    vsi_on_nas = marshmallow_fields.Nested("netapp_ontap.models.vsi_on_nas.VsiOnNasSchema", data_key="vsi_on_nas", unknown=EXCLUDE, allow_none=True)
    r""" A VSI application using NAS."""

    vsi_on_san = marshmallow_fields.Nested("netapp_ontap.models.vsi_on_san.VsiOnSanSchema", data_key="vsi_on_san", unknown=EXCLUDE, allow_none=True)
    r""" A VSI application using SAN."""

    @property
    def resource(self):
        return ApplicationTemplate

    gettable_fields = [
        "links",
        "description",
        "missing_prerequisites",
        "mongo_db_on_san",
        "name",
        "nas",
        "nvme",
        "oracle_on_nfs",
        "oracle_on_san",
        "oracle_rac_on_nfs",
        "oracle_rac_on_san",
        "protocol",
        "s3_bucket",
        "san",
        "sql_on_san",
        "sql_on_smb",
        "vdi_on_nas",
        "vdi_on_san",
        "vsi_on_nas",
        "vsi_on_san",
    ]
    """links,description,missing_prerequisites,mongo_db_on_san,name,nas,nvme,oracle_on_nfs,oracle_on_san,oracle_rac_on_nfs,oracle_rac_on_san,protocol,s3_bucket,san,sql_on_san,sql_on_smb,vdi_on_nas,vdi_on_san,vsi_on_nas,vsi_on_san,"""

    patchable_fields = [
        "mongo_db_on_san",
        "nas",
        "nvme",
        "oracle_on_nfs",
        "oracle_on_san",
        "oracle_rac_on_nfs",
        "oracle_rac_on_san",
        "s3_bucket",
        "san",
        "sql_on_san",
        "sql_on_smb",
        "vdi_on_nas",
        "vdi_on_san",
        "vsi_on_nas",
        "vsi_on_san",
    ]
    """mongo_db_on_san,nas,nvme,oracle_on_nfs,oracle_on_san,oracle_rac_on_nfs,oracle_rac_on_san,s3_bucket,san,sql_on_san,sql_on_smb,vdi_on_nas,vdi_on_san,vsi_on_nas,vsi_on_san,"""

    postable_fields = [
        "mongo_db_on_san",
        "nas",
        "nvme",
        "oracle_on_nfs",
        "oracle_on_san",
        "oracle_rac_on_nfs",
        "oracle_rac_on_san",
        "s3_bucket",
        "san",
        "sql_on_san",
        "sql_on_smb",
        "vdi_on_nas",
        "vdi_on_san",
        "vsi_on_nas",
        "vsi_on_san",
    ]
    """mongo_db_on_san,nas,nvme,oracle_on_nfs,oracle_on_san,oracle_rac_on_nfs,oracle_rac_on_san,s3_bucket,san,sql_on_san,sql_on_smb,vdi_on_nas,vdi_on_san,vsi_on_nas,vsi_on_san,"""

class ApplicationTemplate(Resource):
    r""" Application templates """

    _schema = ApplicationTemplateSchema
    _path = "/api/application/templates"
    _keys = ["name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves application templates.
### Query examples
The most useful queries on this API allows searches by name or protocol access. The following query returns all templates that are used to provision an Oracle application.<br/><br/>
```
GET /application/templates?name=ora*
```
<br/>Similarly, the following query returns all templates that support SAN access.<br/><br/>
```
GET /application/templates?protocol=san
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
        """Returns a count of all ApplicationTemplate resources that match the provided query"""
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
        """Returns a list of RawResources that represent ApplicationTemplate resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves application templates.
### Query examples
The most useful queries on this API allows searches by name or protocol access. The following query returns all templates that are used to provision an Oracle application.<br/><br/>
```
GET /application/templates?name=ora*
```
<br/>Similarly, the following query returns all templates that support SAN access.<br/><br/>
```
GET /application/templates?protocol=san
```
### Learn more
* [`DOC /application`](#docs-application-overview)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an application template.
### Template properties
Each application template has a set of properties. These properties are always nested under a property with the same name as the template. For example, when using the `mongo_db_on_san` template, the properties are found nested inside the `mongo_db_on_san` property. The properties nested under the template property are all specific to the template. The model for the application template object includes all the available templates, but only the object that corresponds to the template's name is returned, and only one is provided in any application API.<br/>
The model of each template includes a description of each property and its allowed values or usage. Default values are also indicated when available. The template properties returned by this API include an example value for each property.
### Template prerequisites
Each template has a set of prerequisites required for its use. If any of these prerequisites are not met, the `missing_prerequisites` property indicates which prerequisite is missing.
### Learn more
* [`DOC /application`](#docs-application-overview)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





