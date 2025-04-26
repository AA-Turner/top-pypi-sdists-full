r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Amazon Web Services Key Management Services (AWS KMS) is a cloud key
management service (KMS) that provides a secure store for secrets. This
feature allows ONTAP to securely store its encryption keys using AWS KMS.
In order to use AWS KMS with ONTAP, you must first create a
Customer Master Key (CMK) in AWS KMS and provide an Access Key ID and
Secret Access Key for a user that has appropriate access to the newly
created CMK in the AWS KMS."
## Examples
### Enabling AWS KMS for an SVM
The following example shows how to enable AWS KMS at the SVM-scope. Note the <i>return_records=true</i> query parameter is used to obtain the newly created key manager configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AwsKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AwsKms()
    resource.svm = {"uuid": "f36ff553-e713-11ea-bd56-005056bb4222"}
    resource.region = "us-east-1"
    resource.key_id = "kmip-aws"
    resource.access_key_id = "(token)"
    resource.secret_access_key = "Ahrut-#ghty5-881Ht"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
AwsKms(
    {
        "_links": {
            "self": {
                "href": "/api/security/aws-kms/f72098a2-e908-11ea-bd56-005056bb4222"
            }
        },
        "svm": {"name": "vs0", "uuid": "f36ff553-e713-11ea-bd56-005056bb4222"},
        "access_key_id": "(token)",
        "uuid": "f72098a2-e908-11ea-bd56-005056bb4222",
        "region": "us-east-1",
        "key_id": "kmip-aws",
    }
)

```
</div>
</div>

---
### Retrieving all AWS KMS configurations
The following example shows how to retrieve all AWS KMS configurations.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AwsKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(AwsKms.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    AwsKms(
        {
            "_links": {
                "self": {
                    "href": "/api/security/aws-kms/f72098a2-e908-11ea-bd56-005056bb4222"
                }
            },
            "svm": {"name": "vs0", "uuid": "f36ff553-e713-11ea-bd56-005056bb4222"},
            "service": "KMS",
            "timeout": 10,
            "access_key_id": "(token)",
            "uuid": "f72098a2-e908-11ea-bd56-005056bb4222",
            "region": "us-east-1",
            "scope": "svm",
            "polling_period": 60,
            "default_domain": "amazonaws.com",
            "key_id": "kmip-aws",
        }
    )
]

```
</div>
</div>

---
### Retrieving a specific AWS KMS configuration
The following example shows how to retrieve information for a specific AWS KMS configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AwsKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AwsKms(uuid="f72098a2-e908-11ea-bd56-005056bb4222")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
AwsKms(
    {
        "_links": {
            "self": {
                "href": "/api/security/aws-kms/f72098a2-e908-11ea-bd56-005056bb4222"
            }
        },
        "svm": {"name": "vs0", "uuid": "f36ff553-e713-11ea-bd56-005056bb4222"},
        "service": "KMS",
        "timeout": 10,
        "access_key_id": "(token)",
        "uuid": "f72098a2-e908-11ea-bd56-005056bb4222",
        "region": "us-east-1",
        "scope": "svm",
        "polling_period": 60,
        "default_domain": "amazonaws.com",
        "key_id": "kmip-aws",
    }
)

```
</div>
</div>

---
### Retrieving the advanced properties of an AWS configured for a specific SVM
These values are not retrieved by default with the 'fields=*' option.
The following example retrieves the advanced properties of a configured AWS for a specific SVM; there is an added computational cost in retrieving their values. The properties are not populated for either a collection GET or an instance GET unless they are explicitly requested using the `fields` query parameter or GET for all advanced properties is enabled.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AwsKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AwsKms(uuid="7052c6c0-a503-11ec-a68f-005056ac75a0")
    resource.get(fields="state,amazon_reachability,ekmip_reachability")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
AwsKms(
    {
        "_links": {
            "self": {
                "href": "/api/security/aws-kms/d70efc34-aa13-11ec-a059-005056ac7c32"
            }
        },
        "amazon_reachability": {"message": "", "reachable": True, "code": "0"},
        "uuid": "d70efc34-aa13-11ec-a059-005056ac7c32",
        "state": {"message": "", "code": "0", "cluster_state": True},
        "ekmip_reachability": [
            {
                "message": "",
                "reachable": True,
                "code": "0",
                "node": {
                    "name": "node1",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/817f544f-a98d-11ec-ae20-005056ac7c32"
                        }
                    },
                    "uuid": "817f544f-a98d-11ec-ae20-005056ac7c32",
                },
            },
            {
                "message": "",
                "reachable": True,
                "code": "0",
                "node": {
                    "name": "node2",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/84b3f5f3-a98d-11ec-9ff4-005056acfbfe"
                        }
                    },
                    "uuid": "84b3f5f3-a98d-11ec-9ff4-005056acfbfe",
                },
            },
        ],
    }
)

```
</div>
</div>

---
### Updating the "access_key_id" of a specific AWS KMS configuration
The following example shows how to update the "access_key_id" for a specific AWS KMS configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AwsKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AwsKms(uuid="f72098a2-e908-11ea-bd56-005056bb4222")
    resource.access_key_id = "(token)"
    resource.secret_access_key = "Ahrut-#ghty5-881Ht"
    resource.patch()

```

---
### Updating a specific AWS KMS configuration to allow it to use a proxy.
The following example shows how to update a specific AWS KMS configuration to allow the AWS KMS instance to use a proxy.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AwsKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AwsKms(uuid="f72098a2-e908-11ea-bd56-005056bb4222")
    resource.default_domain = "216.9"
    resource.host = "172.20.216.9"
    resource.port = 8000
    resource.service = "10"
    resource.verify_host = False
    resource.verify_ip = False
    resource.patch()

```

---
### Deleting a specific AWS KMS configuration
The following example shows how to delete a specific AWS KMS configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AwsKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AwsKms(uuid="f72098a2-e908-11ea-bd56-005056bb4222")
    resource.delete()

```

---
### Restoring keys from a KMIP server
The following example shows how to restore keys for a AWS KMS configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AwsKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AwsKms(uuid="33820b57-ec90-11ea-875e-005056bbf3f0")
    resource.restore()

```

---"""

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


__all__ = ["AwsKms", "AwsKmsSchema"]
__pdoc__ = {
    "AwsKmsSchema.resource": False,
    "AwsKmsSchema.opts": False,
}


class AwsKmsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AwsKms object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the aws_kms."""

    access_key_id = marshmallow_fields.Str(
        data_key="access_key_id",
        allow_none=True,
    )
    r""" AWS Access Key ID of the user that has appropriate access to AWS KMS.

Example: (token)"""

    amazon_reachability = marshmallow_fields.Nested("netapp_ontap.models.aws_connectivity.AwsConnectivitySchema", data_key="amazon_reachability", unknown=EXCLUDE, allow_none=True)
    r""" Indicates whether or not the Amazon KMS is reachable from all nodes in the cluster.
This is an advanced property; there is an added computational cost to retrieving its value. The property is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter or GET for all advanced properties is enabled."""

    default_domain = marshmallow_fields.Str(
        data_key="default_domain",
        allow_none=True,
    )
    r""" AWS KMS default domain.

Example: domainName"""

    ekmip_reachability = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ekmip_server_connectivity.EkmipServerConnectivitySchema", unknown=EXCLUDE, allow_none=True), data_key="ekmip_reachability", allow_none=True)
    r""" Provides the connectivity status for the given SVM on the given node to all EKMIP servers configured on all nodes of the cluster.
This is an advanced property; there is an added computational cost to retrieving its value. The property is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter or GET for all advanced properties is enabled."""

    encryption_context = marshmallow_fields.Str(
        data_key="encryption_context",
        allow_none=True,
    )
    r""" Additional layer of authentication and logging.

Example: aws:fsx:fs-id=fs-0785c8beceb895999"""

    host = marshmallow_fields.Str(
        data_key="host",
        allow_none=True,
    )
    r""" AWS KMS host's hostname.

Example: aws-host.host.com"""

    key_id = marshmallow_fields.Str(
        data_key="key_id",
        allow_none=True,
    )
    r""" AWS Key ID.

Example: kmip-aws"""

    polling_period = Size(
        data_key="polling_period",
        allow_none=True,
    )
    r""" Polling period in minutes.

Example: 55"""

    port = Size(
        data_key="port",
        allow_none=True,
    )
    r""" AWS KMS port.

Example: 443"""

    proxy_host = marshmallow_fields.Str(
        data_key="proxy_host",
        allow_none=True,
    )
    r""" Proxy host.

Example: proxy.eng.com"""

    proxy_password = marshmallow_fields.Str(
        data_key="proxy_password",
        allow_none=True,
    )
    r""" Proxy password. Password is not audited.

Example: awskze-Jwjje2-WJJPer"""

    proxy_port = Size(
        data_key="proxy_port",
        allow_none=True,
    )
    r""" Proxy port.

Example: 1234"""

    proxy_type = marshmallow_fields.Str(
        data_key="proxy_type",
        validate=enum_validation(['http', 'https']),
        allow_none=True,
    )
    r""" Proxy type.

Valid choices:

* http
* https"""

    proxy_username = marshmallow_fields.Str(
        data_key="proxy_username",
        allow_none=True,
    )
    r""" Proxy username.

Example: proxyuser"""

    region = marshmallow_fields.Str(
        data_key="region",
        allow_none=True,
    )
    r""" AWS region of the AWS KMS.

Example: us-east-1"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['svm', 'cluster']),
        allow_none=True,
    )
    r""" Set to "svm" for interfaces owned by an SVM. Otherwise, set to "cluster".

Valid choices:

* svm
* cluster"""

    secret_access_key = marshmallow_fields.Str(
        data_key="secret_access_key",
        allow_none=True,
    )
    r""" AWS Secret Access Key for the provided access key ID.

Example: tyb1kA/bSr5654LncZNwNcvAOR7hu1vPo0nPrtoG"""

    service = marshmallow_fields.Str(
        data_key="service",
        allow_none=True,
    )
    r""" AWS service type.

Example: dynamodb.*.amazonaws.com"""

    skip_verify = marshmallow_fields.Boolean(
        data_key="skip_verify",
        allow_none=True,
    )
    r""" Set to true to bypass verification of the user provided access_key_id
and secret_access_key. An error will be returned if 'skip_verify' is
provided but 'access_key_id' is not.


Example: false"""

    state = marshmallow_fields.Nested("netapp_ontap.models.aws_kms_state.AwsKmsStateSchema", data_key="state", unknown=EXCLUDE, allow_none=True)
    r""" Indicates whether or not the Amazon Web Services Key Management Service (AWS KMS) key protection is available cluster-wide."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the aws_kms."""

    timeout = Size(
        data_key="timeout",
        allow_none=True,
    )
    r""" AWS Connection timeout, in seconds.

Example: 20"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" A unique identifier for the AWS KMS.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    verify = marshmallow_fields.Boolean(
        data_key="verify",
        allow_none=True,
    )
    r""" Set to true to verify the AWS KMS host.

Example: false"""

    verify_host = marshmallow_fields.Boolean(
        data_key="verify_host",
        allow_none=True,
    )
    r""" Set to true to verify the AWS KMS host's hostname.

Example: true"""

    verify_ip = marshmallow_fields.Boolean(
        data_key="verify_ip",
        allow_none=True,
    )
    r""" Set to true to verify the AWS KMS host's IP address.

Example: false"""

    @property
    def resource(self):
        return AwsKms

    gettable_fields = [
        "links",
        "access_key_id",
        "amazon_reachability",
        "default_domain",
        "ekmip_reachability",
        "encryption_context",
        "host",
        "key_id",
        "polling_period",
        "port",
        "proxy_host",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "region",
        "scope",
        "service",
        "skip_verify",
        "state",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "timeout",
        "uuid",
        "verify",
        "verify_host",
        "verify_ip",
    ]
    """links,access_key_id,amazon_reachability,default_domain,ekmip_reachability,encryption_context,host,key_id,polling_period,port,proxy_host,proxy_port,proxy_type,proxy_username,region,scope,service,skip_verify,state,svm.links,svm.name,svm.uuid,timeout,uuid,verify,verify_host,verify_ip,"""

    patchable_fields = [
        "access_key_id",
        "default_domain",
        "encryption_context",
        "host",
        "polling_period",
        "port",
        "proxy_host",
        "proxy_password",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "region",
        "secret_access_key",
        "service",
        "skip_verify",
        "timeout",
        "verify",
        "verify_host",
        "verify_ip",
    ]
    """access_key_id,default_domain,encryption_context,host,polling_period,port,proxy_host,proxy_password,proxy_port,proxy_type,proxy_username,region,secret_access_key,service,skip_verify,timeout,verify,verify_host,verify_ip,"""

    postable_fields = [
        "access_key_id",
        "default_domain",
        "encryption_context",
        "host",
        "key_id",
        "polling_period",
        "port",
        "proxy_host",
        "proxy_password",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "region",
        "secret_access_key",
        "service",
        "svm.name",
        "svm.uuid",
    ]
    """access_key_id,default_domain,encryption_context,host,key_id,polling_period,port,proxy_host,proxy_password,proxy_port,proxy_type,proxy_username,region,secret_access_key,service,svm.name,svm.uuid,"""

class AwsKms(Resource):
    """Allows interaction with AwsKms objects on the host"""

    _schema = AwsKmsSchema
    _path = "/api/security/aws-kms"
    _keys = ["uuid"]
    _action_form_data_parameters = { 'file':'file', }

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all AWS KMS instances configured for all clusters and SVMs.
### Related ONTAP commands
* `security key-manager external aws show`
* `security key-manager external aws check`

### Learn more
* [`DOC /security/aws-kms`](#docs-security-security_aws-kms)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all AwsKms resources that match the provided query"""
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
        """Returns a list of RawResources that represent AwsKms resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["AwsKms"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the AWS KMS configuration.
### Optional properties
* `region` - AWS region of the AWS KMS.
* `service` - AWS service type.
* `default_domain` - AWS KMS default domain.
* `port` - AWS KMS port.
* `proxy_type` - Type of proxy (http, https, etc.), if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `polling_period` - Polling period in minutes.
* `timeout` - AWS Connection timeout, in seconds.
* `verify` - Set to true to verify the AWS KMS host.
* `verify_host` - Set to true to verify the AWS KMS host's hostname.
* `verify_ip` - Set to true to verify the AWS KMS host's IP address.
* `host` - AWS KMS host's hostname.
* `secret_access_key` - AWS secret access key for the access key ID provided.
* `access_key_id` - AWS access key ID of the user with the appropriate access to AWS KMS.
* `skip_verify` - Set to true to bypass verification of the user provided access_key_id and secret_access_key.
* `encryption_context` - Additional layer of authentication and logging.
### Related ONTAP commands
* `security key-manager external aws update-config`
* `security key-manager external aws update-credentials`

### Learn more
* [`DOC /security/aws-kms`](#docs-security-security_aws-kms)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["AwsKms"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["AwsKms"], NetAppResponse]:
        r"""Configures the AWS KMS configuration for the specified SVM.
### Required properties
* `access_key_id` - AWS access key ID of the user who has the appropriate access to AWS KMS.
* `secret_access_key` - AWS secret access key for the access key ID provided.
* `svm.uuid` or `svm.name` - Existing SVM in which to create an AWS KMS.
* `region` - AWS region of the AWS KMS.
* `key_id` - AWS Key ID
### Optional properties
* `service` - AWS service type.
* `default_domain` - AWS KMS default domain.
* `host` - AWS KMS host's hostname.
* `port` - AWS KMS port.
* `proxy_type` - Type of proxy (http, https, etc.), if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `polling_period` - Polling period in minutes.
* `encryption_context` - Additional layer of authentication and logging.
### Related ONTAP commands
* `security key-manager external aws enable`

### Learn more
* [`DOC /security/aws-kms`](#docs-security-security_aws-kms)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["AwsKms"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an AWS KMS configuration.
### Related ONTAP commands
* `security key-manager external aws disable`

### Learn more
* [`DOC /security/aws-kms`](#docs-security-security_aws-kms)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all AWS KMS instances configured for all clusters and SVMs.
### Related ONTAP commands
* `security key-manager external aws show`
* `security key-manager external aws check`

### Learn more
* [`DOC /security/aws-kms`](#docs-security-security_aws-kms)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the AWS KMS configuration for the SVM specified by the UUID.
### Related ONTAP commands
* `security key-manager external aws show`
* `security key-manager external aws check`

### Learn more
* [`DOC /security/aws-kms`](#docs-security-security_aws-kms)"""
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
        r"""Configures the AWS KMS configuration for the specified SVM.
### Required properties
* `access_key_id` - AWS access key ID of the user who has the appropriate access to AWS KMS.
* `secret_access_key` - AWS secret access key for the access key ID provided.
* `svm.uuid` or `svm.name` - Existing SVM in which to create an AWS KMS.
* `region` - AWS region of the AWS KMS.
* `key_id` - AWS Key ID
### Optional properties
* `service` - AWS service type.
* `default_domain` - AWS KMS default domain.
* `host` - AWS KMS host's hostname.
* `port` - AWS KMS port.
* `proxy_type` - Type of proxy (http, https, etc.), if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `polling_period` - Polling period in minutes.
* `encryption_context` - Additional layer of authentication and logging.
### Related ONTAP commands
* `security key-manager external aws enable`

### Learn more
* [`DOC /security/aws-kms`](#docs-security-security_aws-kms)"""
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
        r"""Updates the AWS KMS configuration.
### Optional properties
* `region` - AWS region of the AWS KMS.
* `service` - AWS service type.
* `default_domain` - AWS KMS default domain.
* `port` - AWS KMS port.
* `proxy_type` - Type of proxy (http, https, etc.), if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `polling_period` - Polling period in minutes.
* `timeout` - AWS Connection timeout, in seconds.
* `verify` - Set to true to verify the AWS KMS host.
* `verify_host` - Set to true to verify the AWS KMS host's hostname.
* `verify_ip` - Set to true to verify the AWS KMS host's IP address.
* `host` - AWS KMS host's hostname.
* `secret_access_key` - AWS secret access key for the access key ID provided.
* `access_key_id` - AWS access key ID of the user with the appropriate access to AWS KMS.
* `skip_verify` - Set to true to bypass verification of the user provided access_key_id and secret_access_key.
* `encryption_context` - Additional layer of authentication and logging.
### Related ONTAP commands
* `security key-manager external aws update-config`
* `security key-manager external aws update-credentials`

### Learn more
* [`DOC /security/aws-kms`](#docs-security-security_aws-kms)"""
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
        r"""Deletes an AWS KMS configuration.
### Related ONTAP commands
* `security key-manager external aws disable`

### Learn more
* [`DOC /security/aws-kms`](#docs-security-security_aws-kms)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    def rekey_external(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Rekeys or re-versions the AWS KMS Key Encryption Key (KEK) for the given AWS KMS.
### Related ONTAP commands
* `security key-manager external aws rekey-external`
"""
        return super()._action(
            "rekey-external", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    rekey_external.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)
    def rekey_internal(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Rekeys SVM KEK for the given AWS KMS.
### Related ONTAP commands
* `security key-manager external aws rekey-internal`
"""
        return super()._action(
            "rekey-internal", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    rekey_internal.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)
    def restore(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Restores the keys for an SVM from a configured AWS KMS.
### Related ONTAP commands
* `security key-manager external AWS restore`
"""
        return super()._action(
            "restore", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    restore.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)

