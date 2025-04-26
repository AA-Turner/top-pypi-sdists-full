r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A CIFS server is necessary to provide SMB clients with access to the Storage Virtual Machine (SVM). Before you begin, the following prerequisites must be in place:</br>

 * At least one SVM LIF must exist on the SVM.
 * The LIFs must be able to connect to the DNS servers configured on the SVM and to an Active Directory domain controller of the domain to which you want to join the CIFS server.
 * The DNS servers must contain the service location records that are needed to locate the Active Directory domain services.
 * The cluster time must be synchronized to within five minutes of the Active Directory domain controller.
## Performance monitoring
Performance of the SVM can be monitored by the `metric.*` and `statistics.*` properties. These show the performance of the SVM in terms of IOPS, latency and throughput. The `metric.*` properties denote an average whereas `statistics.*` properties denote a real-time monotonically increasing value aggregated across all nodes.
### Information on the CIFS server
 You must keep the following in mind when creating the CIFS server:

 * The CIFS server name might or might not be the same as the SVM name.
 * The CIFS server name can be up to 15 characters in length.
 * The following characters are not allowed: @ # * ( ) = + [ ] | ; : " , < > \ / ?
 * You must use the FQDN when specifying the domain.
 * The default is to add the CIFS server machine account to the Active Directory "CN=Computer" object.
 * You can choose to add the CIFS server to a different organizational unit (OU) by specifying the "organizational_unit" parameter. When specifying the OU, do not specify the domain portion of the distinguished name; only specify the OU or CN portion of the distinguished name. ONTAP appends the value provided for the required "-domain" parameter onto the value provided for the "-ou" parameter to create the Active Directory distinguished name, which is used when joining the Active Directory domain.
 * You can optionally choose to add a text comment of up to 256 characters about the CIFS server. If there is a space in the comment text, you must enclose the entire string in quotation marks.
 * You can optionally choose to add a comma-delimited list of one or more NetBIOS aliases for the CIFS server.
 * The initial administrative status of the CIFS server is "up".
 * The <i> large-mtu</i> and <i>multichannel</i> features are enabled for the new CIFS server.
 * If LDAP is configured with the <i>use_start_tls</i> and <i>session_security</i> features, the new CIFS server will also have this property set.
 * The security.kdc_encryption and security.advertised_kdc_encryptions fields are mutually exclusive. Use the advertised_kdc_encryptions field to specify the encryption types to be advertised to the Key Distribution Center (KDC) server in the Active Directory domain.
## Examples
### Creating a CIFS server
To create a CIFS server, use the following API. Note the <i>return_records=true</i> query parameter used to obtain the newly created entry in the response.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsService()
    resource.ad_domain = {
        "fqdn": "ontapavc.com",
        "organizational_unit": "CN=Computers",
        "password": "cifs*123",
        "user": "administrator",
    }
    resource.comment = "This CIFS Server Belongs to CS Department"
    resource.default_unix_user = "string"
    resource.enabled = True
    resource.name = "CIFS1"
    resource.netbios = {
        "aliases": ["ALIAS_1", "ALIAS_2", "ALIAS_3"],
        "enabled": False,
        "wins_servers": ["10.224.65.20", "10.224.65.21"],
    }
    resource.options = {
        "admin_to_root_mapping": True,
        "advanced_sparse_file": True,
        "copy_offload": True,
        "fake_open": True,
        "fsctl_trim": True,
        "junction_reparse": True,
        "large_mtu": True,
        "multichannel": True,
        "null_user_windows_name": "string",
        "path_component_cache": True,
        "referral": False,
        "smb_credits": 128,
        "widelink_reparse_versions": ["smb1"],
    }
    resource.security = {
        "encrypt_dc_connection": False,
        "kdc_encryption": False,
        "restrict_anonymous": "no_enumeration",
        "session_security": "none",
        "smb_encryption": False,
        "smb_signing": False,
        "use_ldaps": False,
        "use_start_tls": False,
    }
    resource.svm = {"name": "vs1", "uuid": "e0c20d9c-96cd-11eb-97da-0050568e684d"}
    resource.post(hydrate=True, return_timeout=10)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
CifsService(
    {
        "netbios": {
            "enabled": False,
            "aliases": ["ALIAS_1", "ALIAS_2", "ALIAS_3"],
            "wins_servers": ["10.224.65.20", "10.224.65.21"],
        },
        "name": "CIFS1",
        "enabled": True,
        "default_unix_user": "string",
        "svm": {"name": "vs1", "uuid": "e0c20d9c-96cd-11eb-97da-0050568e684d"},
        "security": {
            "aes_netlogon_enabled": False,
            "smb_encryption": False,
            "use_ldaps": False,
            "restrict_anonymous": "no_enumeration",
            "encrypt_dc_connection": False,
            "smb_signing": False,
            "lm_compatibility_level": "lm_ntlm_ntlmv2_krb",
            "session_security": "none",
            "kdc_encryption": False,
            "try_ldap_channel_binding": False,
            "use_start_tls": False,
        },
        "ad_domain": {"fqdn": "ONTAPAVC.COM", "organizational_unit": "CN=Computers"},
        "comment": "This CIFS Server Belongs to CS Department",
        "options": {
            "null_user_windows_name": "string",
            "junction_reparse": True,
            "advanced_sparse_file": True,
            "path_component_cache": True,
            "copy_offload": True,
            "admin_to_root_mapping": True,
            "fake_open": True,
            "large_mtu": True,
            "fsctl_trim": True,
            "widelink_reparse_versions": ["smb1"],
            "multichannel": True,
            "referral": False,
            "smb_credits": 128,
        },
    }
)

```
</div>
</div>

---
### Creating a CIFS server when using AKV
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsService()
    resource.key_vault_uri = "https://testkv.vault.azure.net"
    resource.client_secret = "_8E8Q~Qu866jtihUE3ia4Q5Y5IDEVC6UfskbZa6X"
    resource.authentication_method = "client_secret"
    resource.tenant_id = "c9f32fcb-4ab7-40fe-af1b-1850d46cfbbe"
    resource.client_id = "e959d1b5-5a63-4284-9268-851e30e3eceb"
    resource.ad_domain = {
        "fqdn": "ontapavc.com",
        "organizational_unit": "CN=Computers",
        "user": "administrator",
    }
    resource.comment = "This CIFS Server Belongs to CS Department"
    resource.default_unix_user = "string"
    resource.enabled = True
    resource.name = "CIFS1"
    resource.netbios = {
        "aliases": ["ALIAS_1", "ALIAS_2", "ALIAS_3"],
        "enabled": False,
        "wins_servers": ["10.224.65.20", "10.224.65.21"],
    }
    resource.options = {
        "admin_to_root_mapping": True,
        "advanced_sparse_file": True,
        "copy_offload": True,
        "fake_open": True,
        "fsctl_trim": True,
        "junction_reparse": True,
        "large_mtu": True,
        "multichannel": True,
        "null_user_windows_name": "string",
        "path_component_cache": True,
        "referral": False,
        "smb_credits": 128,
        "widelink_reparse_versions": ["smb1"],
    }
    resource.security = {
        "encrypt_dc_connection": False,
        "kdc_encryption": False,
        "restrict_anonymous": "no_enumeration",
        "session_security": "none",
        "smb_encryption": False,
        "smb_signing": False,
        "use_ldaps": False,
        "use_start_tls": False,
    }
    resource.svm = {"name": "vs1", "uuid": "e0c20d9c-96cd-11eb-97da-0050568e684d"}
    resource.post(hydrate=True, return_timeout=10)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
CifsService(
    {
        "netbios": {
            "enabled": False,
            "aliases": ["ALIAS_1", "ALIAS_2", "ALIAS_3"],
            "wins_servers": ["10.224.65.20", "10.224.65.21"],
        },
        "name": "CIFS1",
        "enabled": True,
        "default_unix_user": "string",
        "svm": {"name": "vs1", "uuid": "e0c20d9c-96cd-11eb-97da-0050568e684d"},
        "security": {
            "aes_netlogon_enabled": False,
            "smb_encryption": False,
            "use_ldaps": False,
            "restrict_anonymous": "no_enumeration",
            "encrypt_dc_connection": False,
            "smb_signing": False,
            "lm_compatibility_level": "lm_ntlm_ntlmv2_krb",
            "session_security": "none",
            "kdc_encryption": False,
            "try_ldap_channel_binding": False,
            "use_start_tls": False,
        },
        "ad_domain": {"fqdn": "ONTAPAVC.COM", "organizational_unit": "CN=Computers"},
        "comment": "This CIFS Server Belongs to CS Department",
        "options": {
            "null_user_windows_name": "string",
            "junction_reparse": True,
            "advanced_sparse_file": True,
            "path_component_cache": True,
            "copy_offload": True,
            "admin_to_root_mapping": True,
            "fake_open": True,
            "large_mtu": True,
            "fsctl_trim": True,
            "widelink_reparse_versions": ["smb1"],
            "multichannel": True,
            "referral": False,
            "smb_credits": 128,
        },
    }
)

```
</div>
</div>

---
### Creating a CIFS server for Hybrid user
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsService()
    resource.auth_user_type = "hybrid_user"
    resource.client_certificate = "certificate added to azure application"
    resource.authentication_method = "certificate"
    resource.tenant_id = "c9f32fcb-4ab7-40fe-af1b-1850d46cfbbe"
    resource.client_id = "e959d1b5-5a63-4284-9268-851e30e3eceb"
    resource.ad_domain = {"fqdn": "ontapavc.com", "organizational_unit": "CN=Computers"}
    resource.comment = "This CIFS Server Belongs to CS Department"
    resource.enabled = True
    resource.name = "CIFS1"
    resource.svm = {"name": "vs1", "uuid": "e0c20d9c-96cd-11eb-97da-0050568e684d"}
    resource.post(hydrate=True, return_timeout=10)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
CifsService(
    {
        "name": "CIFS1",
        "enabled": True,
        "svm": {"name": "vs1", "uuid": "e0c20d9c-96cd-11eb-97da-0050568e684d"},
        "ad_domain": {"fqdn": "ONTAPAVC.COM", "organizational_unit": "CN=Computers"},
        "comment": "This CIFS Server Belongs to CS Department",
    }
)

```
</div>
</div>

---
### Creating a CIFS server when using the security.advertised_kdc_encryptions field
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsService()
    resource.ad_domain = {
        "fqdn": "testdomain.com",
        "organizational_unit": "CN=Computers",
        "password": "cifs*123",
        "user": "administrator",
    }
    resource.enabled = True
    resource.name = "CIFS_server1"
    resource.security = {"advertised_kdc_encryptions": ["aes-128"]}
    resource.svm = {"name": "testvs", "uuid": "508375d4-fb16-11ee-a792-005056a75b5c"}
    resource.post(hydrate=True, return_timeout=120, force=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
CifsService(
    {
        "netbios": {"enabled": False, "wins_servers": []},
        "name": "CIFS_SERVER1",
        "enabled": True,
        "default_unix_user": "pcuser",
        "svm": {"name": "testvs", "uuid": "508375d4-fb16-11ee-a792-005056a75b5c"},
        "security": {
            "advertised_kdc_encryptions": ["aes_128"],
            "aes_netlogon_enabled": False,
            "smb_encryption": False,
            "use_ldaps": False,
            "restrict_anonymous": "no_enumeration",
            "encrypt_dc_connection": False,
            "smb_signing": False,
            "lm_compatibility_level": "lm_ntlm_ntlmv2_krb",
            "session_security": "none",
            "kdc_encryption": True,
            "try_ldap_channel_binding": True,
            "use_start_tls": False,
            "ldap_referral_enabled": False,
        },
        "group_policy_object_enabled": False,
        "statistics": {
            "status": "ok",
            "iops_raw": {"total": 0, "write": 0, "other": 0, "read": 0},
            "latency_raw": {"total": 0, "write": 0, "other": 0, "read": 0},
            "throughput_raw": {"total": 0, "write": 0, "read": 0},
            "timestamp": "2024-04-16T15:17:41+00:00",
        },
        "ad_domain": {
            "default_site": "",
            "fqdn": "TESTDOMAIN.COM",
            "organizational_unit": "CN=Computers",
        },
        "comment": "",
        "options": {
            "junction_reparse": True,
            "advanced_sparse_file": True,
            "path_component_cache": True,
            "copy_offload": True,
            "admin_to_root_mapping": True,
            "fake_open": True,
            "shadowcopy": True,
            "shadowcopy_dir_depth": 5,
            "export_policy_enabled": False,
            "large_mtu": True,
            "fsctl_trim": True,
            "widelink_reparse_versions": ["smb1"],
            "multichannel": True,
            "referral": False,
            "smb_credits": 512,
        },
    }
)

```
</div>
</div>

---
### Retrieving the full CIFS server configuration for all SVMs in the cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(CifsService.get_collection(fields="*", return_timeout=15)))

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
[
    CifsService(
        {
            "netbios": {
                "enabled": False,
                "aliases": ["ALIAS_1", "ALIAS_2", "ALIAS_3"],
                "wins_servers": ["10.224.65.20", "10.224.65.21"],
            },
            "name": "CIFS1",
            "enabled": True,
            "default_unix_user": "string",
            "svm": {"name": "vs1", "uuid": "e0c20d9c-96cd-11eb-97da-0050568e684d"},
            "security": {
                "aes_netlogon_enabled": False,
                "smb_encryption": False,
                "use_ldaps": False,
                "restrict_anonymous": "no_enumeration",
                "encrypt_dc_connection": False,
                "smb_signing": False,
                "lm_compatibility_level": "lm_ntlm_ntlmv2_krb",
                "session_security": "none",
                "kdc_encryption": False,
                "try_ldap_channel_binding": False,
                "use_start_tls": False,
            },
            "ad_domain": {
                "fqdn": "ONTAPAVC.COM",
                "organizational_unit": "CN=Computers",
            },
            "comment": "This CIFS Server Belongs to CS Department",
            "options": {
                "null_user_windows_name": "string",
                "junction_reparse": True,
                "advanced_sparse_file": True,
                "path_component_cache": True,
                "copy_offload": True,
                "admin_to_root_mapping": True,
                "fake_open": True,
                "large_mtu": True,
                "fsctl_trim": True,
                "widelink_reparse_versions": ["smb1"],
                "multichannel": True,
                "referral": False,
                "smb_credits": 128,
            },
        }
    )
]

```
</div>
</div>

---
### Retrieving CIFS server configuration details for a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsService(**{"svm.uuid": "e0c20d9c-96cd-11eb-97da-0050568e684d"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
CifsService(
    {
        "netbios": {
            "enabled": False,
            "aliases": ["ALIAS_1", "ALIAS_2", "ALIAS_3"],
            "wins_servers": ["10.224.65.20", "10.224.65.21"],
        },
        "name": "CIFS1",
        "enabled": True,
        "default_unix_user": "string",
        "svm": {"name": "vs1", "uuid": "e0c20d9c-96cd-11eb-97da-0050568e684d"},
        "security": {
            "aes_netlogon_enabled": False,
            "smb_encryption": False,
            "use_ldaps": False,
            "restrict_anonymous": "no_enumeration",
            "encrypt_dc_connection": False,
            "smb_signing": False,
            "lm_compatibility_level": "lm_ntlm_ntlmv2_krb",
            "session_security": "none",
            "kdc_encryption": False,
            "try_ldap_channel_binding": False,
            "use_start_tls": False,
        },
        "ad_domain": {"fqdn": "ONTAPAVC.COM", "organizational_unit": "CN=Computers"},
        "comment": "This CIFS Server Belongs to CS Department",
        "options": {
            "null_user_windows_name": "string",
            "junction_reparse": True,
            "advanced_sparse_file": True,
            "path_component_cache": True,
            "copy_offload": True,
            "admin_to_root_mapping": True,
            "fake_open": True,
            "large_mtu": True,
            "fsctl_trim": True,
            "widelink_reparse_versions": ["smb1"],
            "multichannel": True,
            "referral": False,
            "smb_credits": 128,
        },
    }
)

```
</div>
</div>

---
### Updating CIFS server properties for the specified SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsService(**{"svm.uuid": "e0c20d9c-96cd-11eb-97da-0050568e684d"})
    resource.comment = "CIFS SERVER MODIFICATION"
    resource.patch()

```

---
### Removing a CIFS server for a specific SVM
To delete a CIFS server, use the following API. This will delete the CIFS server along with other CIFS configurations such as CIFS share, share ACLs, homedir search-path, and so on.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsService(**{"svm.uuid": "e0c20d9c-96cd-11eb-97da-0050568e684d"})
    resource.delete(
        body={
            "ad_domain": {
                "fqdn": "ontapavc.com",
                "organizational_unit": "CN=Computers",
                "password": "cifs*123",
                "user": "administrator",
            },
            "force": True,
        }
    )

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


__all__ = ["CifsService", "CifsServiceSchema"]
__pdoc__ = {
    "CifsServiceSchema.resource": False,
    "CifsServiceSchema.opts": False,
}


class CifsServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsService object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the cifs_service."""

    ad_domain = marshmallow_fields.Nested("netapp_ontap.models.ad_domain.AdDomainSchema", data_key="ad_domain", unknown=EXCLUDE, allow_none=True)
    r""" The ad_domain field of the cifs_service."""

    auth_style = marshmallow_fields.Str(
        data_key="auth-style",
        validate=enum_validation(['domain', 'workgroup']),
        allow_none=True,
    )
    r""" Authentication type.

Valid choices:

* domain
* workgroup"""

    auth_user_type = marshmallow_fields.Str(
        data_key="auth_user_type",
        validate=enum_validation(['domain_user', 'hybrid_user']),
        allow_none=True,
    )
    r""" Specifies the type of user who can access the SMB Volume. The default is domain_user. In the case of a hybrid-user, ONTAP won't contact on-premise ADDS.


Valid choices:

* domain_user
* hybrid_user"""

    authentication_method = marshmallow_fields.Str(
        data_key="authentication_method",
        validate=enum_validation(['client_secret', 'certificate']),
        allow_none=True,
    )
    r""" Specifies the authentication method.
The available values are:

  * client_secret
  * certificate


Valid choices:

* client_secret
* certificate"""

    client_certificate = marshmallow_fields.Str(
        data_key="client_certificate",
        allow_none=True,
    )
    r""" PKCS12 certificate used by the application to prove its identity to AKV.

Example: PEM Cert"""

    client_id = marshmallow_fields.Str(
        data_key="client_id",
        allow_none=True,
    )
    r""" Application client ID of the deployed Azure application with appropriate access to an AKV or EntraId.

Example: e959d1b5-5a63-4284-9268-851e30e3eceb"""

    client_secret = marshmallow_fields.Str(
        data_key="client_secret",
        allow_none=True,
    )
    r""" Secret used by the application to prove its identity to AKV.

Example: _8E8Q~Qu866jtihUE3ia4Q5Y5IDEVC6UfskbZa6X"""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=256),
        allow_none=True,
    )
    r""" A descriptive text comment for the CIFS server. SMB clients can see the CIFS server comment when browsing servers on the network. If there is a space in the comment, you must enclose the entire string in quotation marks.

Example: This CIFS Server Belongs to CS Department"""

    default_unix_user = marshmallow_fields.Str(
        data_key="default_unix_user",
        allow_none=True,
    )
    r""" Specifies the UNIX user to which any authenticated CIFS user is mapped to, if the normal user mapping rules fails."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Specifies if the CIFS service is administratively enabled."""

    group_policy_object_enabled = marshmallow_fields.Boolean(
        data_key="group_policy_object_enabled",
        allow_none=True,
    )
    r""" If set to true, group policies will be applied to the SVM."""

    key_vault_uri = marshmallow_fields.Str(
        data_key="key_vault_uri",
        allow_none=True,
    )
    r""" URI of the deployed AKV that is used by ONTAP for storing keys.

Example: https://kmip-akv-keyvault.vault.azure.net/"""

    metric = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_svm.PerformanceMetricSvmSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" The metric field of the cifs_service."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=15),
        allow_none=True,
    )
    r""" The name of the CIFS server.

Example: CIFS1"""

    netbios = marshmallow_fields.Nested("netapp_ontap.models.cifs_netbios.CifsNetbiosSchema", data_key="netbios", unknown=EXCLUDE, allow_none=True)
    r""" The netbios field of the cifs_service."""

    oauth_host = marshmallow_fields.Str(
        data_key="oauth_host",
        allow_none=True,
    )
    r""" Open authorization server host name.

Example: login.microsoftonline.com"""

    options = marshmallow_fields.Nested("netapp_ontap.models.cifs_service_options.CifsServiceOptionsSchema", data_key="options", unknown=EXCLUDE, allow_none=True)
    r""" The options field of the cifs_service."""

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

Example: proxypassword"""

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

    security = marshmallow_fields.Nested("netapp_ontap.models.cifs_service_security.CifsServiceSecuritySchema", data_key="security", unknown=EXCLUDE, allow_none=True)
    r""" The security field of the cifs_service."""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_raw_svm.PerformanceMetricRawSvmSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" The statistics field of the cifs_service."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the cifs_service."""

    tenant_id = marshmallow_fields.Str(
        data_key="tenant_id",
        allow_none=True,
    )
    r""" Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV or EntraId.

Example: c9f32fcb-4ab7-40fe-af1b-1850d46cfbbe"""

    timeout = Size(
        data_key="timeout",
        allow_none=True,
    )
    r""" AKV connection timeout, in seconds. The allowed range is between 0 to 30 seconds.

Example: 25"""

    verify_host = marshmallow_fields.Boolean(
        data_key="verify_host",
        allow_none=True,
    )
    r""" Verify the identity of the AKV host name. By default, verify_host is set to true."""

    workgroup = marshmallow_fields.Str(
        data_key="workgroup",
        validate=len_validation(minimum=1, maximum=15),
        allow_none=True,
    )
    r""" The workgroup name.

Example: workgrp1"""

    @property
    def resource(self):
        return CifsService

    gettable_fields = [
        "links",
        "ad_domain",
        "auth_style",
        "auth_user_type",
        "authentication_method",
        "client_id",
        "comment",
        "default_unix_user",
        "enabled",
        "group_policy_object_enabled",
        "key_vault_uri",
        "metric.links",
        "metric.duration",
        "metric.iops",
        "metric.latency",
        "metric.status",
        "metric.throughput",
        "metric.timestamp",
        "name",
        "netbios",
        "oauth_host",
        "options",
        "proxy_host",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "security",
        "statistics.iops_raw",
        "statistics.latency_raw",
        "statistics.status",
        "statistics.throughput_raw",
        "statistics.timestamp",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "tenant_id",
        "timeout",
        "verify_host",
        "workgroup",
    ]
    """links,ad_domain,auth_style,auth_user_type,authentication_method,client_id,comment,default_unix_user,enabled,group_policy_object_enabled,key_vault_uri,metric.links,metric.duration,metric.iops,metric.latency,metric.status,metric.throughput,metric.timestamp,name,netbios,oauth_host,options,proxy_host,proxy_port,proxy_type,proxy_username,security,statistics.iops_raw,statistics.latency_raw,statistics.status,statistics.throughput_raw,statistics.timestamp,svm.links,svm.name,svm.uuid,tenant_id,timeout,verify_host,workgroup,"""

    patchable_fields = [
        "ad_domain",
        "auth_user_type",
        "authentication_method",
        "client_certificate",
        "client_id",
        "client_secret",
        "comment",
        "default_unix_user",
        "enabled",
        "group_policy_object_enabled",
        "key_vault_uri",
        "name",
        "netbios",
        "oauth_host",
        "options",
        "proxy_host",
        "proxy_password",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "security",
        "tenant_id",
        "timeout",
        "verify_host",
        "workgroup",
    ]
    """ad_domain,auth_user_type,authentication_method,client_certificate,client_id,client_secret,comment,default_unix_user,enabled,group_policy_object_enabled,key_vault_uri,name,netbios,oauth_host,options,proxy_host,proxy_password,proxy_port,proxy_type,proxy_username,security,tenant_id,timeout,verify_host,workgroup,"""

    postable_fields = [
        "ad_domain",
        "auth_user_type",
        "authentication_method",
        "client_certificate",
        "client_id",
        "client_secret",
        "comment",
        "default_unix_user",
        "enabled",
        "key_vault_uri",
        "name",
        "netbios",
        "oauth_host",
        "options",
        "proxy_host",
        "proxy_password",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "security",
        "svm.name",
        "svm.uuid",
        "tenant_id",
        "timeout",
        "verify_host",
        "workgroup",
    ]
    """ad_domain,auth_user_type,authentication_method,client_certificate,client_id,client_secret,comment,default_unix_user,enabled,key_vault_uri,name,netbios,oauth_host,options,proxy_host,proxy_password,proxy_port,proxy_type,proxy_username,security,svm.name,svm.uuid,tenant_id,timeout,verify_host,workgroup,"""

class CifsService(Resource):
    """Allows interaction with CifsService objects on the host"""

    _schema = CifsServiceSchema
    _path = "/api/protocols/cifs/services"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves CIFS servers.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `vserver cifs server show`
* `vserver cifs server options show`
* `vserver cifs server security show`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
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
        """Returns a count of all CifsService resources that match the provided query"""
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
        """Returns a list of RawResources that represent CifsService resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["CifsService"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates both the mandatory and optional parameters of the CIFS configuration. Ensure the CIFS server is administratively disabled when renaming the CIFS server or modifying the <i>ad_domain</i> properties.
### Related ONTAP commands
* `vserver cifs server modify`
* `vserver cifs server options modify`
* `vserver cifs security modify`
* `vserver cifs server add-netbios-aliases`
* `vserver cifs server remove-netbios-aliases`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["CifsService"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["CifsService"], NetAppResponse]:
        r"""Creates a CIFS server. Each SVM can have one CIFS server.</br>
### Important notes
- The CIFS server name might or might not be the same as the SVM name.
- The CIFS server name can contain up to 15 characters.
- The CIFS server name does not support the following characters: @ # * ( ) = + [ ] | ; : " , < >  / ?
### Required properties when creating CIFS server with Windows Active Directory domain
* `svm.uuid` or `svm.name` - Existing SVM in which to create the CIFS server.
* `name` -  Name of the CIFS server.
* `ad_domain.fqdn` - Fully qualified domain name of the Windows Active Directory to which this CIFS server belongs.
* `ad_domain.user` - User account with the access to add the CIFS server to the Active Directory.
* `ad_domain.password` - Account password used to add this CIFS server to the Active Directory.
### Required properties when creating CIFS server in Workgroup mode
* `svm.uuid` or `svm.name` - Existing SVM in which to create the CIFS server.
* `name` -  Name of the CIFS server.
* `workgroup` - Name of the workgroup to which this CIFS server belongs.
### Required properties when using AKV for authentication (ANF platform)
* `svm.uuid` or `svm.name` - Existing SVM in which to create the CIFS server.
* `name` -  Name of the CIFS server.
* `ad_domain.user` - User account with the access to add the CIFS server to the Active Directory.
* `ad_domain.fqdn` - Fully qualified domain name of the Windows Active Directory to which this CIFS server belongs.
* `client_id` - Application client ID of the deployed Azure application with appropriate access to an AKV or EntraId.
* `tenant_id` - Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV or EntraId.
* `key_vault_uri` - URI of the deployed AKV that is used by ONTAP for storing keys.
* `authentication_method` - Authentication method used by the application to prove its identity to AKV or EntraId. It can be either "client_secret" or "certificate".
* `auth_user_type` - Type of user who can access the SMB Volume. It can be either "domain_user" or "hybrid_user". The default is domain_user. In the case of a hybrid-user, ONTAP cannot access on-premise ADDS.
* `client_secret` - Secret used by the application to prove its identity to AKV.
* `client_certificate` - Base64 encoded PKCS12 certificate used by the application to prove its identity to AKV.
### Recommended optional properties
* `comment` - Add a text comment of up to 256 characters about the CIFS server.
* `netbios.aliases` - Add a comma-delimited list of one or more NetBIOS aliases for the CIFS server.
* `netbios.wins_servers` - Add a list of Windows Internet Name Server (WINS) addresses that manage and map the NetBIOS name of the CIFS server to their network IP addresses. The IP addresses must be IPv4 addresses.
### Default property values
If not specified in POST, the following default property values are assigned:
* `ad_domain.organizational_unit` - _CN=Computers_
* `enabled` - _true_
* `security.restrict_anonymous` - _no_enumeration_
* `security.smb_signing` - _false_
* `security.smb_encryption` - _false_
* `security.encrypt_dc_connection` - _false_
* `default_unix_user` - _pcuser_
* `netbios.enabled` - _false_ However, if either "netbios.wins-server" or "netbios.aliases" is set during POST and if `netbios.enabled` is not specified then `netbios.enabled` is set to true.
* `security.aes_netlogon_enabled` - _false_
* `security.try_ldap_channel_binding` - _true_
* `security.ldap_referral_enabled` - _false_
### Related ONTAP commands
* `vserver cifs server create`
* `vserver cifs server options modify`
* `vserver cifs security modify`
* `vserver cifs server add-netbios-aliases`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["CifsService"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a CIFS server and related CIFS configurations.<br/>
</br>Important notes:
* The default value for the "force" field is false.
* If the "force" field is set along with user login credentials, the local CIFS configuration will be deleted irrespective of any communication errors.
* If the "force" field alone is set without passing the user login credentials, the local CIFS configuration will be deleted by not making any request to Active Directory.
### Related ONTAP commands
* `vserver cifs server delete`
* `vserver cifs remove-netbios-aliases`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves CIFS servers.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `vserver cifs server show`
* `vserver cifs server options show`
* `vserver cifs server security show`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a CIFS server.
### Related ONTAP commands
* `vserver cifs server show`
* `vserver cifs server options show`
* `vserver cifs server security show`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
"""
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
        r"""Creates a CIFS server. Each SVM can have one CIFS server.</br>
### Important notes
- The CIFS server name might or might not be the same as the SVM name.
- The CIFS server name can contain up to 15 characters.
- The CIFS server name does not support the following characters: @ # * ( ) = + [ ] | ; : " , < >  / ?
### Required properties when creating CIFS server with Windows Active Directory domain
* `svm.uuid` or `svm.name` - Existing SVM in which to create the CIFS server.
* `name` -  Name of the CIFS server.
* `ad_domain.fqdn` - Fully qualified domain name of the Windows Active Directory to which this CIFS server belongs.
* `ad_domain.user` - User account with the access to add the CIFS server to the Active Directory.
* `ad_domain.password` - Account password used to add this CIFS server to the Active Directory.
### Required properties when creating CIFS server in Workgroup mode
* `svm.uuid` or `svm.name` - Existing SVM in which to create the CIFS server.
* `name` -  Name of the CIFS server.
* `workgroup` - Name of the workgroup to which this CIFS server belongs.
### Required properties when using AKV for authentication (ANF platform)
* `svm.uuid` or `svm.name` - Existing SVM in which to create the CIFS server.
* `name` -  Name of the CIFS server.
* `ad_domain.user` - User account with the access to add the CIFS server to the Active Directory.
* `ad_domain.fqdn` - Fully qualified domain name of the Windows Active Directory to which this CIFS server belongs.
* `client_id` - Application client ID of the deployed Azure application with appropriate access to an AKV or EntraId.
* `tenant_id` - Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV or EntraId.
* `key_vault_uri` - URI of the deployed AKV that is used by ONTAP for storing keys.
* `authentication_method` - Authentication method used by the application to prove its identity to AKV or EntraId. It can be either "client_secret" or "certificate".
* `auth_user_type` - Type of user who can access the SMB Volume. It can be either "domain_user" or "hybrid_user". The default is domain_user. In the case of a hybrid-user, ONTAP cannot access on-premise ADDS.
* `client_secret` - Secret used by the application to prove its identity to AKV.
* `client_certificate` - Base64 encoded PKCS12 certificate used by the application to prove its identity to AKV.
### Recommended optional properties
* `comment` - Add a text comment of up to 256 characters about the CIFS server.
* `netbios.aliases` - Add a comma-delimited list of one or more NetBIOS aliases for the CIFS server.
* `netbios.wins_servers` - Add a list of Windows Internet Name Server (WINS) addresses that manage and map the NetBIOS name of the CIFS server to their network IP addresses. The IP addresses must be IPv4 addresses.
### Default property values
If not specified in POST, the following default property values are assigned:
* `ad_domain.organizational_unit` - _CN=Computers_
* `enabled` - _true_
* `security.restrict_anonymous` - _no_enumeration_
* `security.smb_signing` - _false_
* `security.smb_encryption` - _false_
* `security.encrypt_dc_connection` - _false_
* `default_unix_user` - _pcuser_
* `netbios.enabled` - _false_ However, if either "netbios.wins-server" or "netbios.aliases" is set during POST and if `netbios.enabled` is not specified then `netbios.enabled` is set to true.
* `security.aes_netlogon_enabled` - _false_
* `security.try_ldap_channel_binding` - _true_
* `security.ldap_referral_enabled` - _false_
### Related ONTAP commands
* `vserver cifs server create`
* `vserver cifs server options modify`
* `vserver cifs security modify`
* `vserver cifs server add-netbios-aliases`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
"""
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
        r"""Updates both the mandatory and optional parameters of the CIFS configuration. Ensure the CIFS server is administratively disabled when renaming the CIFS server or modifying the <i>ad_domain</i> properties.
### Related ONTAP commands
* `vserver cifs server modify`
* `vserver cifs server options modify`
* `vserver cifs security modify`
* `vserver cifs server add-netbios-aliases`
* `vserver cifs server remove-netbios-aliases`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
"""
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
        r"""Deletes a CIFS server and related CIFS configurations.<br/>
</br>Important notes:
* The default value for the "force" field is false.
* If the "force" field is set along with user login credentials, the local CIFS configuration will be deleted irrespective of any communication errors.
* If the "force" field alone is set without passing the user login credentials, the local CIFS configuration will be deleted by not making any request to Active Directory.
### Related ONTAP commands
* `vserver cifs server delete`
* `vserver cifs remove-netbios-aliases`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


