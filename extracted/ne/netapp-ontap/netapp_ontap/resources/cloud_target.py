r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Retrieving a collection of cloud targets
The cloud targets GET API retrieves all cloud targets defined in the cluster.
## Creating cloud targets
The cluster administrator tells ONTAP how to connect to a cloud target. The following pre-requisites must be met before creating an object store configuration in ONTAP.
A valid data bucket or container must be created with the object store provider. This assumes that the user has valid account credentials with the object store provider to access the data bucket.
The ONTAP node must be able to connect to the object store. </br>
This includes:
  - Fast, reliable connectivity to the object store.
  - An inter-cluster LIF (logical interface) must be configured on the cluster. ONTAP verifies connectivity prior to saving this configuration information.
  - If SSL/TLS authentication is required, then valid certificates must be installed.
  - FabricPool license (required for all object stores except SGWS).
## Deleting cloud targets
If a cloud target is used by an aggregate, then the aggregate must be deleted before the cloud target can be deleted."""

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


__all__ = ["CloudTarget", "CloudTargetSchema"]
__pdoc__ = {
    "CloudTargetSchema.resource": False,
    "CloudTargetSchema.opts": False,
}


class CloudTargetSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CloudTarget object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the cloud_target."""

    access_key = marshmallow_fields.Str(
        data_key="access_key",
        allow_none=True,
    )
    r""" Access key ID for AWS_S3 and other S3 compatible provider types."""

    authentication_type = marshmallow_fields.Str(
        data_key="authentication_type",
        validate=enum_validation(['key', 'cap', 'ec2_iam', 'gcp_sa', 'azure_msi']),
        allow_none=True,
    )
    r""" Authentication used to access the target. SnapMirror does not yet support CAP. Required in POST.

Valid choices:

* key
* cap
* ec2_iam
* gcp_sa
* azure_msi"""

    azure_account = marshmallow_fields.Str(
        data_key="azure_account",
        allow_none=True,
    )
    r""" Azure account"""

    azure_msi_token = marshmallow_fields.Str(
        data_key="azure_msi_token",
        allow_none=True,
    )
    r""" Managed Service Identity (MSI) token required to authenticate to the Azure object store. This form of authentication is only supported on Azure NetApp Files."""

    azure_private_key = marshmallow_fields.Str(
        data_key="azure_private_key",
        allow_none=True,
    )
    r""" Azure access key"""

    azure_sas_token = marshmallow_fields.Str(
        data_key="azure_sas_token",
        allow_none=True,
    )
    r""" Shared access signature token to access Azure containers and blobs."""

    cap_url = marshmallow_fields.Str(
        data_key="cap_url",
        allow_none=True,
    )
    r""" This parameter is available only when auth-type is CAP. It specifies a full URL of the request to a CAP server for retrieving temporary credentials (access-key, secret-password, and session token) for accessing the object store.

Example: https://123.45.67.89:1234/CAP/api/v1/credentials?agency=myagency&mission=mymission&role=myrole"""

    certificate_validation_enabled = marshmallow_fields.Boolean(
        data_key="certificate_validation_enabled",
        allow_none=True,
    )
    r""" Is SSL/TLS certificate validation enabled? The default value is true. This can only be modified for SGWS, IBM_COS, and ONTAP_S3 provider types."""

    cluster = marshmallow_fields.Nested("netapp_ontap.models.cloud_target_cluster.CloudTargetClusterSchema", data_key="cluster", unknown=EXCLUDE, allow_none=True)
    r""" The cluster field of the cloud_target."""

    container = marshmallow_fields.Str(
        data_key="container",
        allow_none=True,
    )
    r""" Data bucket/container name. For FabricLink, a wildcard character "*" can also be specified to indicate that all the buckets in an SVM can use the same target information. However, for containers other than ONTAP, an exact name should be specified.

Example: bucket1"""

    ipspace = marshmallow_fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", data_key="ipspace", unknown=EXCLUDE, allow_none=True)
    r""" The ipspace field of the cloud_target."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Cloud target name"""

    owner = marshmallow_fields.Str(
        data_key="owner",
        validate=enum_validation(['fabricpool', 'snapmirror', 's3_snapmirror']),
        allow_none=True,
    )
    r""" Owner of the target. Allowed values are FabricPool, SnapMirror or S3_SnapMirror. A target can be used by only one feature.

Valid choices:

* fabricpool
* snapmirror
* s3_snapmirror"""

    port = Size(
        data_key="port",
        allow_none=True,
    )
    r""" Port number of the object store that ONTAP uses when establishing a connection. Required in POST."""

    provider_type = marshmallow_fields.Str(
        data_key="provider_type",
        allow_none=True,
    )
    r""" Type of cloud provider. Allowed values depend on owner type. For FabricPool, AliCloud, AWS_S3, Azure_Cloud, GoogleCloud, IBM_COS, SGWS, and ONTAP_S3 are allowed. For SnapMirror, the valid values are AWS_S3 or SGWS. For FabricLink, AWS_S3, SGWS, S3_Compatible, S3EMU, LOOPBACK and ONTAP_S3 are allowed."""

    read_latency_warning_threshold = Size(
        data_key="read_latency_warning_threshold",
        allow_none=True,
    )
    r""" The warning threshold for read latency that is used to determine when an alert ems for a read operation from an object store should be issued."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['cluster', 'svm']),
        allow_none=True,
    )
    r""" If the cloud target is owned by a data SVM, then the scope is set to svm. Otherwise it will be set to cluster.

Valid choices:

* cluster
* svm"""

    secret_password = marshmallow_fields.Str(
        data_key="secret_password",
        allow_none=True,
    )
    r""" Secret access key for AWS_S3 and other S3 compatible provider types."""

    server = marshmallow_fields.Str(
        data_key="server",
        allow_none=True,
    )
    r""" Fully qualified domain name of the object store server. Required on POST.  For Amazon S3, server name must be an AWS regional endpoint in the format s3.amazonaws.com or s3-<region>.amazonaws.com, for example, s3-us-west-2.amazonaws.com. The region of the server and the bucket must match. For Azure, if the server is a "blob.core.windows.net" or a "blob.core.usgovcloudapi.net", then a value of azure-account followed by a period is added in front of the server."""

    server_side_encryption = marshmallow_fields.Str(
        data_key="server_side_encryption",
        validate=enum_validation(['none', 'sse_s3', 'sse_kms', 'dsse_kms']),
        allow_none=True,
    )
    r""" Encryption of data at rest by the object store server for AWS_S3 and other S3 compatible provider types. In most cases it is best not to change default value of "sse_s3" for object store servers which support SSE-S3 encryption. The encryption is in addition to any encryption done by ONTAP at a volume or at an aggregate level. Note that changing this option does not change encryption of data which already exist in the object store.

Valid choices:

* none
* sse_s3
* sse_kms
* dsse_kms"""

    snapmirror_use = marshmallow_fields.Str(
        data_key="snapmirror_use",
        validate=enum_validation(['data', 'metadata']),
        allow_none=True,
    )
    r""" Use of the cloud target by SnapMirror.

Valid choices:

* data
* metadata"""

    ssl_enabled = marshmallow_fields.Boolean(
        data_key="ssl_enabled",
        allow_none=True,
    )
    r""" SSL/HTTPS enabled or not"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the cloud_target."""

    url_style = marshmallow_fields.Str(
        data_key="url_style",
        validate=enum_validation(['path_style', 'virtual_hosted_style']),
        allow_none=True,
    )
    r""" URL style used to access S3 bucket.

Valid choices:

* path_style
* virtual_hosted_style"""

    use_http_proxy = marshmallow_fields.Boolean(
        data_key="use_http_proxy",
        allow_none=True,
    )
    r""" Use HTTP proxy when connecting to the object store."""

    used = Size(
        data_key="used",
        allow_none=True,
    )
    r""" The amount of cloud space used by all the aggregates attached to the target, in bytes. This field is only populated for FabricPool targets. The value is recalculated once every 5 minutes."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Cloud target UUID"""

    @property
    def resource(self):
        return CloudTarget

    gettable_fields = [
        "links",
        "access_key",
        "authentication_type",
        "azure_account",
        "cap_url",
        "certificate_validation_enabled",
        "cluster",
        "container",
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
        "name",
        "owner",
        "port",
        "provider_type",
        "read_latency_warning_threshold",
        "scope",
        "server",
        "server_side_encryption",
        "snapmirror_use",
        "ssl_enabled",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "url_style",
        "use_http_proxy",
        "used",
        "uuid",
    ]
    """links,access_key,authentication_type,azure_account,cap_url,certificate_validation_enabled,cluster,container,ipspace.links,ipspace.name,ipspace.uuid,name,owner,port,provider_type,read_latency_warning_threshold,scope,server,server_side_encryption,snapmirror_use,ssl_enabled,svm.links,svm.name,svm.uuid,url_style,use_http_proxy,used,uuid,"""

    patchable_fields = [
        "access_key",
        "authentication_type",
        "azure_account",
        "azure_msi_token",
        "azure_private_key",
        "azure_sas_token",
        "cap_url",
        "certificate_validation_enabled",
        "cluster",
        "name",
        "port",
        "read_latency_warning_threshold",
        "secret_password",
        "server",
        "server_side_encryption",
        "snapmirror_use",
        "ssl_enabled",
        "svm.name",
        "svm.uuid",
        "url_style",
        "use_http_proxy",
    ]
    """access_key,authentication_type,azure_account,azure_msi_token,azure_private_key,azure_sas_token,cap_url,certificate_validation_enabled,cluster,name,port,read_latency_warning_threshold,secret_password,server,server_side_encryption,snapmirror_use,ssl_enabled,svm.name,svm.uuid,url_style,use_http_proxy,"""

    postable_fields = [
        "access_key",
        "authentication_type",
        "azure_account",
        "azure_msi_token",
        "azure_private_key",
        "azure_sas_token",
        "cap_url",
        "certificate_validation_enabled",
        "cluster",
        "container",
        "ipspace.name",
        "ipspace.uuid",
        "name",
        "owner",
        "port",
        "provider_type",
        "read_latency_warning_threshold",
        "secret_password",
        "server",
        "server_side_encryption",
        "snapmirror_use",
        "ssl_enabled",
        "svm.name",
        "svm.uuid",
        "url_style",
        "use_http_proxy",
    ]
    """access_key,authentication_type,azure_account,azure_msi_token,azure_private_key,azure_sas_token,cap_url,certificate_validation_enabled,cluster,container,ipspace.name,ipspace.uuid,name,owner,port,provider_type,read_latency_warning_threshold,secret_password,server,server_side_encryption,snapmirror_use,ssl_enabled,svm.name,svm.uuid,url_style,use_http_proxy,"""

class CloudTarget(Resource):
    """Allows interaction with CloudTarget objects on the host"""

    _schema = CloudTargetSchema
    _path = "/api/cloud/targets"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the collection of cloud targets in the cluster.
### Related ONTAP commands
* `storage aggregate object-store config show`
* `snapmirror object-store config show`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all CloudTarget resources that match the provided query"""
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
        """Returns a list of RawResources that represent CloudTarget resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["CloudTarget"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the cloud target specified by the UUID with the fields in the body. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store config modify`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["CloudTarget"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["CloudTarget"], NetAppResponse]:
        r"""Creates a cloud target.
### Required properties
* `name` - Name for the cloud target.
* `owner` - Owner of the target: _fabricpool_, _snapmirror_.
* `provider_type` - Type of cloud provider: _AWS_S3_, _Azure_Cloud_, _SGWS_, _IBM_COS_, _AliCloud_, _GoogleCloud_, _ONTAP_S3_.
* `server` - Fully qualified domain name of the object store server. Required when `provider_type` is one of the following: _SGWS_, _IBM_COS_, _AliCloud_.
* `container` - Data bucket/container name.
* `access_key` - Access key ID if `provider_type` is not _Azure_Cloud_ and `authentication_type` is _key_.
* `secret_password` - Secret access key if `provider_type` is not _Azure_Cloud_ and `authentication_type` is _key_.
* `azure_account` - Azure account if `provider_type` is _Azure_Cloud_.
* `azure_private_key` - Azure access key if `provider_type` is _Azure_Cloud_.
* `cap_url` - Full URL of the request to a CAP server for retrieving temporary credentials if `authentication_type` is _cap_.
* `snapmirror_use` - Use of the cloud target if `owner` is _snapmirror_: data, metadata.
* `azure_msi_token` - Azure Managed Service Identity (MSI) token if `owner` is _fabricpool_ or _snapmirror_, `provider_type` is _Azure_Cloud_,  `authentication_type` if specified must be  _azure_msi_ and platform is Azure Netapp Files.
### Recommended optional properties
* `authentication_type` - Authentication used to access the target: _key_, _cap_, _ec2_iam_, _gcp_sa_, _azure_msi_.
* `ssl_enabled` - SSL/HTTPS enabled or disabled.
* `port` - Port number of the object store that ONTAP uses when establishing a connection.
* `ipspace` - IPspace to use in order to reach the cloud target.
* `use_http_proxy` - Use the HTTP proxy when connecting to the object store server.
* `azure_sas_token` - Shared access signature to grant limited access to Azure storage account resources.
* `svm.name` or `svm.uuid` - Name or UUID of SVM if `owner` is _snapmirror_.
* `read_latency_warning_threshold` - Latency threshold to determine when to issue a warning alert EMS for a GET request.
### Default property values
* `authentication_type`
  - _ec2_iam_ - if running in Cloud Volumes ONTAP in AWS
  - _gcp_sa_ - if running in Cloud Volumes ONTAP in GCP
  - _azure_msi_ - if running in Cloud Volumes ONTAP in Azure or if running on Azure NetApp Files platform with a Managed Service Identity (MSI) token.
  - _key_  - in all other cases.
* `server`
  - _s3.amazonaws.com_ - if `provider_type` is _AWS_S3_
  - _blob.core.windows.net_ - if `provider_type` is _Azure_Cloud_
  - _storage.googleapis.com_ - if `provider_type` is _GoogleCloud_
* `ssl_enabled` - _true_
* `port`
  - _443_ if `ssl_enabled` is _true_
  - _80_ if `ssl_enabled` is _false_ and `provider_type` is not _SGWS_
  - _8084_ if `ssl_enabled` is _false_ and `provider_type` is _SGWS_
* `ipspace` - _Default_
* `certificate_validation_enabled` - _true_
* `ignore_warnings` - _false_
* `check_only` - _false_
* `use_http_proxy` - _false_
* `server_side_encryption`
  - _none_ - if `provider_type` is _ONTAP_S3_
  - _sse_s3_ - if `provider_type` is not _ONTAP_S3_
* `url_style`
  - _path_style_ - if `provider_type` is neither _AWS_S3_ nor _AliCloud_
  - _virtual_hosted_style_ - if `provider_type` is either _AWS_S3 or _AliCloud__
### Related ONTAP commands
* `storage aggregate object-store config create`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["CloudTarget"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the cloud target specified by the UUID. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store config delete`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the collection of cloud targets in the cluster.
### Related ONTAP commands
* `storage aggregate object-store config show`
* `snapmirror object-store config show`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the cloud target specified by the UUID.
### Related ONTAP commands
* `storage aggregate object-store config show`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Creates a cloud target.
### Required properties
* `name` - Name for the cloud target.
* `owner` - Owner of the target: _fabricpool_, _snapmirror_.
* `provider_type` - Type of cloud provider: _AWS_S3_, _Azure_Cloud_, _SGWS_, _IBM_COS_, _AliCloud_, _GoogleCloud_, _ONTAP_S3_.
* `server` - Fully qualified domain name of the object store server. Required when `provider_type` is one of the following: _SGWS_, _IBM_COS_, _AliCloud_.
* `container` - Data bucket/container name.
* `access_key` - Access key ID if `provider_type` is not _Azure_Cloud_ and `authentication_type` is _key_.
* `secret_password` - Secret access key if `provider_type` is not _Azure_Cloud_ and `authentication_type` is _key_.
* `azure_account` - Azure account if `provider_type` is _Azure_Cloud_.
* `azure_private_key` - Azure access key if `provider_type` is _Azure_Cloud_.
* `cap_url` - Full URL of the request to a CAP server for retrieving temporary credentials if `authentication_type` is _cap_.
* `snapmirror_use` - Use of the cloud target if `owner` is _snapmirror_: data, metadata.
* `azure_msi_token` - Azure Managed Service Identity (MSI) token if `owner` is _fabricpool_ or _snapmirror_, `provider_type` is _Azure_Cloud_,  `authentication_type` if specified must be  _azure_msi_ and platform is Azure Netapp Files.
### Recommended optional properties
* `authentication_type` - Authentication used to access the target: _key_, _cap_, _ec2_iam_, _gcp_sa_, _azure_msi_.
* `ssl_enabled` - SSL/HTTPS enabled or disabled.
* `port` - Port number of the object store that ONTAP uses when establishing a connection.
* `ipspace` - IPspace to use in order to reach the cloud target.
* `use_http_proxy` - Use the HTTP proxy when connecting to the object store server.
* `azure_sas_token` - Shared access signature to grant limited access to Azure storage account resources.
* `svm.name` or `svm.uuid` - Name or UUID of SVM if `owner` is _snapmirror_.
* `read_latency_warning_threshold` - Latency threshold to determine when to issue a warning alert EMS for a GET request.
### Default property values
* `authentication_type`
  - _ec2_iam_ - if running in Cloud Volumes ONTAP in AWS
  - _gcp_sa_ - if running in Cloud Volumes ONTAP in GCP
  - _azure_msi_ - if running in Cloud Volumes ONTAP in Azure or if running on Azure NetApp Files platform with a Managed Service Identity (MSI) token.
  - _key_  - in all other cases.
* `server`
  - _s3.amazonaws.com_ - if `provider_type` is _AWS_S3_
  - _blob.core.windows.net_ - if `provider_type` is _Azure_Cloud_
  - _storage.googleapis.com_ - if `provider_type` is _GoogleCloud_
* `ssl_enabled` - _true_
* `port`
  - _443_ if `ssl_enabled` is _true_
  - _80_ if `ssl_enabled` is _false_ and `provider_type` is not _SGWS_
  - _8084_ if `ssl_enabled` is _false_ and `provider_type` is _SGWS_
* `ipspace` - _Default_
* `certificate_validation_enabled` - _true_
* `ignore_warnings` - _false_
* `check_only` - _false_
* `use_http_proxy` - _false_
* `server_side_encryption`
  - _none_ - if `provider_type` is _ONTAP_S3_
  - _sse_s3_ - if `provider_type` is not _ONTAP_S3_
* `url_style`
  - _path_style_ - if `provider_type` is neither _AWS_S3_ nor _AliCloud_
  - _virtual_hosted_style_ - if `provider_type` is either _AWS_S3 or _AliCloud__
### Related ONTAP commands
* `storage aggregate object-store config create`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the cloud target specified by the UUID with the fields in the body. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store config modify`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the cloud target specified by the UUID. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store config delete`

### Learn more
* [`DOC /cloud/targets`](#docs-cloud-cloud_targets)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


