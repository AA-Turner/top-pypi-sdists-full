r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API displays security certificate information and manages the certificates in ONTAP.
## Installing certificates in ONTAP
The security certificates GET request retrieves all of the certificates in the cluster.
## Examples
### Retrieving all certificates installed in the cluster with their common-names
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SecurityCertificate.get_collection(fields="common_name")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    SecurityCertificate(
        {
            "_links": {
                "self": {
                    "href": "/api/security/certificates/dad2363b-8ac0-11e8-9058-005056b482fc"
                }
            },
            "common_name": "vs0",
            "uuid": "dad2363b-8ac0-11e8-9058-005056b482fc",
            "svm": {"name": "vs0"},
        }
    ),
    SecurityCertificate(
        {
            "_links": {
                "self": {
                    "href": "/api/security/certificates/1941e048-8ac1-11e8-9058-005056b482fc"
                }
            },
            "common_name": "ROOT",
            "uuid": "1941e048-8ac1-11e8-9058-005056b482fc",
        }
    ),
    SecurityCertificate(
        {
            "_links": {
                "self": {
                    "href": "/api/security/certificates/5a3a77a8-892d-11e8-b7da-005056b482fc"
                }
            },
            "common_name": "cert_name",
            "uuid": "5a3a77a8-892d-11e8-b7da-005056b482fc",
        }
    ),
]

```
</div>
</div>

---
### Retrieving all certificates installed at cluster-scope with their common-names
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(SecurityCertificate.get_collection(scope="cluster", fields="common_name"))
    )

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    SecurityCertificate(
        {
            "_links": {
                "self": {
                    "href": "/api/security/certificates/1941e048-8ac1-11e8-9058-005056b482fc"
                }
            },
            "common_name": "ROOT",
            "uuid": "1941e048-8ac1-11e8-9058-005056b482fc",
            "scope": "cluster",
        }
    ),
    SecurityCertificate(
        {
            "_links": {
                "self": {
                    "href": "/api/security/certificates/5a3a77a8-892d-11e8-b7da-005056b482fc"
                }
            },
            "common_name": "cert_name",
            "uuid": "5a3a77a8-892d-11e8-b7da-005056b482fc",
            "scope": "cluster",
        }
    ),
]

```
</div>
</div>

---
### Retrieving all certificates installed on a specific SVM with their common-names
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            SecurityCertificate.get_collection(
                fields="common_name", **{"svm.name": "vs0"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    SecurityCertificate(
        {
            "_links": {
                "self": {
                    "href": "/api/security/certificates/dad2363b-8ac0-11e8-9058-005056b482fc"
                }
            },
            "common_name": "vs0",
            "uuid": "dad2363b-8ac0-11e8-9058-005056b482fc",
            "svm": {"name": "vs0"},
        }
    )
]

```
</div>
</div>

---
### Retrieving a certificate using its UUID for all fields
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityCertificate(uuid="dad2363b-8ac0-11e8-9058-005056b482fc")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
SecurityCertificate(
    {
        "serial_number": "15428D45CF81CF56",
        "key_size": 2048,
        "_links": {
            "self": {
                "href": "/api/security/certificates/dad2363b-8ac0-11e8-9058-005056b482fc"
            }
        },
        "expiry_time": "2019-07-18T15:29:14-04:00",
        "common_name": "vs0",
        "hash_function": "sha256",
        "uuid": "dad2363b-8ac0-11e8-9058-005056b482fc",
        "type": "server",
        "ca": "vs0",
        "public_certificate": "<CERTIFICATE-CONTENT>",
        "scope": "svm",
        "svm": {"name": "vs0", "uuid": "d817293c-8ac0-11e8-9058-005056b482fc"},
    }
)

```
</div>
</div>

### Creating a certificate in a cluster
These certificates can be used to help administrators enable certificate-based authentication and to enable SSL-based communication to the cluster.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityCertificate()
    resource.common_name = "TEST-SERVER"
    resource.type = "server"
    resource.post(hydrate=True)
    print(resource)

```

### Installing a certificate in a cluster
These certificates can be used to help administrators enable certificate-based authentication and to enable-SSL based communication to the cluster.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityCertificate()
    resource.type = "server_ca"
    resource.public_certificate = "<CERTIFICATE-CONTENT>"
    resource.post(hydrate=True)
    print(resource)

```

---
### Installing a certificate on a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityCertificate()
    resource.svm = {"name": "vs0"}
    resource.type = "server_ca"
    resource.public_certificate = "<CERTIFICATE-CONTENT>"
    resource.post(hydrate=True)
    print(resource)

```

---
### Installing a CA-signed certificate on a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityCertificate()
    resource.svm = {"name": "vs0"}
    resource.type = "server"
    resource.public_certificate = "<CERTIFICATE-CONTENT>"
    resource.intermediate_certificates = [
        "<CERTIFICATE-CONTENT>",
        "<CERTIFICATE-CONTENT>",
    ]
    resource.post(hydrate=True)
    print(resource)

```

---
### Deleting a certificate using its UUID
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityCertificate(uuid="dad2363b-8ac0-11e8-9058-005056b482fc")
    resource.delete(fields="*")

```

### Signing a new certificate signing request using an existing CA certificate UUID
Once you have created a certificate of type "root_ca", you can use that certificate to act as a local Certificate Authority to sign new certificate signing requests. The following example signs a new certificate signing request using an existing CA certificate UUID. If successful, the API returns a signed certificate.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityCertificate(uuid="253add53-8ac9-11e8-9058-005056b482fc")
    resource.sign(
        body={"signing_request": "<CERTIFICATE-CONTENT>", "hash_function": "sha256"}
    )

```
<div class="try_it_out">
<input id="example9_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example9_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example9_result" class="try_it_out_content">
```
SecurityCertificate({"public_certificate": "<CERTIFICATE-CONTENT>"})

```
</div>
</div>

### Generate a new Certificate Signing Request (CSR)
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityConfig()
    resource.certificate_signing_request(
        body={
            "algorithm": "rsa",
            "extended_key_usage": ["serverauth"],
            "hash_function": "sha256",
            "key_usage": ["digitalsignature"],
            "security_strength": "112",
            "subject_alternatives": {
                "dns": ["*.example.com", "*.example1.com"],
                "email": ["abc@example.com", "abc@example1.com"],
                "ip": ["10.225.34.223", "10.225.34.224"],
                "uri": ["http://example.com", "http://example1.com"],
            },
            "subject_name": "C=US,O=NTAP,CN=test.domain.com",
        }
    )

```

---
```
### Download and install a certificate from the Azure Key Vault.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityCertificate()
    resource.svm = {"name": "vs0"}
    resource.name = "vs0-client-cert"
    resource.type = "client"
    resource.azure = {
        "key_vault": "https://example.vault.azure.net",
        "client_id": "12345678-abcd-1234-12ad-dfasdffgfdaaa",
        "tenant_id": "12345678-abcd-abcd-test-720ef604b100",
        "client_secret": "clientSecretString",
        "verify_host": False,
    }
    resource.post(hydrate=True)
    print(resource)

```

---
```
### Creating a root-ca certificate in a cluster when DCN cluster is configured.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityCertificate()
    resource.common_name = "TEST-ROOT-CA"
    resource.type = "root_ca"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example12_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example12_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example12_result" class="try_it_out_content">
```
SecurityCertificate({"common_name": "TEST-ROOT-CA", "type": "root_ca"})

```
</div>
</div>

---
### Deleting a CA certificate using its UUID when DCN cluster is configured.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityCertificate(uuid="dad2363b-8ac0-11e8-9058-005056b482fc")
    resource.delete(fields="*")

```

---"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union
from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["SecurityCertificate", "SecurityCertificateSchema"]
__pdoc__ = {
    "SecurityCertificateSchema.resource": False,
    "SecurityCertificateSchema.opts": False,
}

class SecurityCertificateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityCertificate object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the security_certificate."""

    authority_key_identifier = marshmallow_fields.Str(
        data_key="authority_key_identifier",
        allow_none=True,
    )
    r""" Provides the key identifier of the issuing CA certificate that signed the SSL certificate.

Example: 26:1F:C5:53:5B:D7:9E:E2:37:74:F4:F4:06:09:03:3D:EB:41:75:D7"""

    azure = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.security_azure", "SecurityAzureSchema"),
                data_key="azure",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The azure field of the security_certificate."""

    ca = marshmallow_fields.Str(
        data_key="ca",
        validate=len_validation(minimum=1, maximum=256),
        allow_none=True,
    )
    r""" Certificate authority"""

    common_name = marshmallow_fields.Str(
        data_key="common_name",
        allow_none=True,
    )
    r""" FQDN or custom common name. Provide on POST when creating a self-signed certificate.

Example: test.domain.com"""

    expiry_time = marshmallow_fields.Str(
        data_key="expiry_time",
        allow_none=True,
    )
    r""" Certificate expiration time, in ISO 8601 duration format or date and time format. Can be provided on POST if creating self-signed certificate. The expiration time range is between 1 day to 10 years.

Example: 2030-01-25T11:20:13.000+0000"""

    hash_function = marshmallow_fields.Str(
        data_key="hash_function",
        validate=enum_validation(['sha1', 'sha256', 'md5', 'sha224', 'sha384', 'sha512']),
        allow_none=True,
    )
    r""" Hashing function. Can be provided on POST when creating a self-signed certificate. Hash functions md5 and sha1 are not allowed on POST.

Valid choices:

* sha1
* sha256
* md5
* sha224
* sha384
* sha512"""

    intermediate_certificates = marshmallow_fields.List(marshmallow_fields.Str, data_key="intermediate_certificates", allow_none=True)
    r""" Chain of intermediate Certificates in PEM format. Only valid in POST when installing a certificate."""

    key_size = Size(
        data_key="key_size",
        allow_none=True,
    )
    r""" Key size of requested Certificate in bits. One of 512, 1024, 1536, 2048, 3072. Can be provided on POST if creating self-signed certificate with a minimum permissible value of 2048."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Certificate name or name of the certificate to be downloaded from the Azure Key Vault (AKV). If not provided in POST, a unique name specific to the SVM is automatically generated."""

    private_key = marshmallow_fields.Str(
        data_key="private_key",
        allow_none=True,
    )
    r""" Private key Certificate in PEM format. Only valid for create when installing a CA-signed certificate. This is not audited.

Example: (private_key)\n"""

    public_certificate = marshmallow_fields.Str(
        data_key="public_certificate",
        allow_none=True,
    )
    r""" Public key Certificate in PEM format. If this is not provided in POST, a self-signed certificate is created.

Example: <CERTIFICATE-CONTENT>"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        allow_none=True,
    )
    r""" The scope field of the security_certificate."""

    serial_number = marshmallow_fields.Str(
        data_key="serial_number",
        validate=len_validation(minimum=1, maximum=40),
        allow_none=True,
    )
    r""" Serial number of certificate."""

    subject_alternatives = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.subject_alternate_name", "SubjectAlternateNameSchema"),
                data_key="subject_alternatives",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The subject_alternatives field of the security_certificate."""

    subject_key_identifier = marshmallow_fields.Str(
        data_key="subject_key_identifier",
        allow_none=True,
    )
    r""" Provides the key identifier used to identify the public key in the SSL certificate.

Example: 26:1F:C5:53:5B:D7:9E:E2:37:74:F4:F4:06:09:03:3D:EB:41:75:D8"""

    svm = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.svm", "SvmSchema"),
                data_key="svm",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The svm field of the security_certificate."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['client', 'server', 'client_ca', 'server_ca', 'root_ca']),
        allow_none=True,
    )
    r""" Type of Certificate. The following types are supported:

* client - a certificate and its private key used by an SSL client in ONTAP.
* server - a certificate and its private key used by an SSL server in ONTAP.
* client_ca - a Certificate Authority certificate used by an SSL server in ONTAP to verify an SSL client certificate.
* server_ca - a Certificate Authority certificate used by an SSL client in ONTAP to verify an SSL server certificate.
* root_ca - a self-signed certificate used by ONTAP to sign other certificates by acting as a Certificate Authority.


Valid choices:

* client
* server
* client_ca
* server_ca
* root_ca"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique ID that identifies a certificate."""

    @property
    def resource(self):
        return SecurityCertificate

    gettable_fields = [
        "links",
        "authority_key_identifier",
        "azure",
        "ca",
        "common_name",
        "expiry_time",
        "hash_function",
        "key_size",
        "name",
        "public_certificate",
        "scope",
        "serial_number",
        "subject_alternatives",
        "subject_key_identifier",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "uuid",
    ]
    """links,authority_key_identifier,azure,ca,common_name,expiry_time,hash_function,key_size,name,public_certificate,scope,serial_number,subject_alternatives,subject_key_identifier,svm.links,svm.name,svm.uuid,type,uuid,"""

    patchable_fields = [
        "azure",
        "common_name",
        "expiry_time",
        "hash_function",
        "key_size",
        "name",
        "public_certificate",
        "scope",
        "svm.name",
        "svm.uuid",
        "type",
    ]
    """azure,common_name,expiry_time,hash_function,key_size,name,public_certificate,scope,svm.name,svm.uuid,type,"""

    postable_fields = [
        "azure",
        "common_name",
        "expiry_time",
        "hash_function",
        "intermediate_certificates",
        "key_size",
        "name",
        "private_key",
        "public_certificate",
        "scope",
        "subject_alternatives",
        "svm.name",
        "svm.uuid",
        "type",
    ]
    """azure,common_name,expiry_time,hash_function,intermediate_certificates,key_size,name,private_key,public_certificate,scope,subject_alternatives,svm.name,svm.uuid,type,"""

class SecurityCertificate(Resource):
    """Allows interaction with SecurityCertificate objects on the host"""

    _schema = SecurityCertificateSchema
    _path = "/api/security/certificates"
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
        r"""Retrieves security certificates.
### Related ONTAP commands
* `security certificate show`

### Learn more
* [`DOC /security/certificates`](#docs-security-security_certificates)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SecurityCertificate resources that match the provided query"""
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
        """Returns a list of RawResources that represent SecurityCertificate resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["SecurityCertificate"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SecurityCertificate"], NetAppResponse]:
        r"""Creates or installs a certificate or downloads a certificate from Azure Key Vault (AKV) and installs it on the ONTAP cluster.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create or install the certificate.
* `common_name` - Common name of the certificate. Required when creating a certificate.
* `type` - Type of certificate.
* `public_certificate` - Public key certificate in PEM format. Required when installing a certificate.
* `private_key` - Private key certificate in PEM format. Required when installing a CA-signed certificate.
### Recommended optional properties
* `expiry_time` - Certificate expiration time. Specifying an expiration time is recommended when creating a certificate.
* `key_size` - Key size of the certificate in bits. Specifying a strong key size is recommended when creating a certificate.
* `name` - Unique certificate name per SVM or the name of the certificate in AKV, required for downloading AKV certificates. If one is not provided, it is automatically generated.
### AKV required properties for downloading a certificate
* `azure.key_vault` - URI of the Azure Key Vault.
* `azure.client_id` - Application (client) ID of the deployed Azure application with appropriate access to an AKV.
* `azure.tenant_id` - Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.
* `azure.client_secret` - Secret used by the application to prove its identity to AKV.
* `azure.client_certificate` - PKCS12 certificate used by the application to prove its identity to AKV.
### AKV optional properties for downloading a certificate
* `azure.oauth_host` - Open authorization server host name.
* `azure.proxy.type` - Type of proxy (http, https etc.) if proxy configuration is used.
* `azure.proxy.host` - Proxy hostname if proxy configuration is used.
* `azure.proxy.port` - Proxy port number if proxy configuration is used.
* `azure.proxy.username` - Proxy username if proxy configuration is used.
* `azure.proxy.password` - Proxy password if proxy configuration is used.
* `azure.timeout` - AKV connection timeout in seconds.
* `azure.verify_host` - Verify the identity of the AKV host name.
### Default property values
If not specified in POST, the following default property values are assigned:
* `key_size` - _2048_
* `expiry_time` - _P365DT_
* `hash_function` - _sha256_
### Related ONTAP commands
* `security certificate create`
* `security certificate install`
* `security certificate azure-install`

### Learn more
* [`DOC /security/certificates`](#docs-security-security_certificates)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["SecurityCertificate"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a security certificate.
### Related ONTAP commands
* `security certificate delete`

### Learn more
* [`DOC /security/certificates`](#docs-security-security_certificates)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves security certificates.
### Related ONTAP commands
* `security certificate show`

### Learn more
* [`DOC /security/certificates`](#docs-security-security_certificates)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves security certificates.
### Related ONTAP commands
* `security certificate show`

### Learn more
* [`DOC /security/certificates`](#docs-security-security_certificates)"""
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
        r"""Creates or installs a certificate or downloads a certificate from Azure Key Vault (AKV) and installs it on the ONTAP cluster.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create or install the certificate.
* `common_name` - Common name of the certificate. Required when creating a certificate.
* `type` - Type of certificate.
* `public_certificate` - Public key certificate in PEM format. Required when installing a certificate.
* `private_key` - Private key certificate in PEM format. Required when installing a CA-signed certificate.
### Recommended optional properties
* `expiry_time` - Certificate expiration time. Specifying an expiration time is recommended when creating a certificate.
* `key_size` - Key size of the certificate in bits. Specifying a strong key size is recommended when creating a certificate.
* `name` - Unique certificate name per SVM or the name of the certificate in AKV, required for downloading AKV certificates. If one is not provided, it is automatically generated.
### AKV required properties for downloading a certificate
* `azure.key_vault` - URI of the Azure Key Vault.
* `azure.client_id` - Application (client) ID of the deployed Azure application with appropriate access to an AKV.
* `azure.tenant_id` - Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.
* `azure.client_secret` - Secret used by the application to prove its identity to AKV.
* `azure.client_certificate` - PKCS12 certificate used by the application to prove its identity to AKV.
### AKV optional properties for downloading a certificate
* `azure.oauth_host` - Open authorization server host name.
* `azure.proxy.type` - Type of proxy (http, https etc.) if proxy configuration is used.
* `azure.proxy.host` - Proxy hostname if proxy configuration is used.
* `azure.proxy.port` - Proxy port number if proxy configuration is used.
* `azure.proxy.username` - Proxy username if proxy configuration is used.
* `azure.proxy.password` - Proxy password if proxy configuration is used.
* `azure.timeout` - AKV connection timeout in seconds.
* `azure.verify_host` - Verify the identity of the AKV host name.
### Default property values
If not specified in POST, the following default property values are assigned:
* `key_size` - _2048_
* `expiry_time` - _P365DT_
* `hash_function` - _sha256_
### Related ONTAP commands
* `security certificate create`
* `security certificate install`
* `security certificate azure-install`

### Learn more
* [`DOC /security/certificates`](#docs-security-security_certificates)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)


    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a security certificate.
### Related ONTAP commands
* `security certificate delete`

### Learn more
* [`DOC /security/certificates`](#docs-security-security_certificates)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    def sign(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Signs a certificate.
### Required properties
* `signing_request` - Certificate signing request to be signed by the given certificate authority.
### Recommended optional properties
* `expiry_time` - Certificate expiration time. Specifying an expiration time for a signed certificate is recommended.
* `hash_function` - Hashing function. Specifying a strong hashing function is recommended when signing a certificate.
### Default property values
If not specified in POST, the following default property values are assigned:
* `expiry_time` - _P365DT_
* `hash_function` - _sha256_
### Related ONTAP commands
* `security certificate sign`
This API is used to sign a certificate request using a pre-existing self-signed root certificate. The self-signed root certificate acts as a certificate authority within its scope and maintains the records of its signed certificates. <br/>
The root certificate can be created for a given SVM or for the cluster using [`POST security/certificates`].<br/>
"""
        return super()._action(
            "sign", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    sign.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)

