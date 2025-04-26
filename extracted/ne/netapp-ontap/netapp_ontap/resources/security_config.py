r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API for various cluster-wide security-related operations.
## "onboard_key_manager_configurable_status" object
Use this API to retrieve details of whether or not the Onboard Key Manager can be configured on the cluster.

* GET    /api/security
* GET    /api/security?fields=onboard_key_manager_configurable_status
## "software_data_encryption" object
Contains software data encryption related information.<br/>
  The following APIs can be used to enable or disable and obtain default software data at rest encryption values:

  * PATCH  /api/security -d '{ "software_data_encryption.disabled_by_default" : true }'
  * PATCH  /api/security -d '{ "software_data_encryption.disabled_by_default" : false }'
  * GET    /api/security
  * GET    /api/security?fields=software_data_encryption <br/>
### Platform Specifics
### Unified ONTAP
A PATCH request on this API using the parameter "software_data_encryption.conversion_enabled" triggers the  conversion of all non-encrypted metadata volumes to encrypted metadata volumes and all non-NAE aggregates to NAE aggregates. For the conversion to start, the cluster must have either Onboard Key Manager or an external key manager set up and the aggregates should either be empty or have only metadata volumes. No data volumes should be present in any of the aggregates. For MetroCluster configurations, the PATCH request will fail if the cluster is in the switchover state.<br/>
### ASA r2
A PATCH request on this API using the parameter "software_data_encryption.conversion_enabled" triggers the  conversion of all non-encrypted volumes and LUNs to encrypted volumes and LUNs. For the conversion to start, the cluster must have either Onboard Key Manager or an external key manager set up. Newly created volumes and LUNs are encrypted by default after this PATCH request.
A PATCH request on this API using the parameter "software_data_encryption.rekey" triggers the rekey of all encrypted volumes and LUNs.<br/>
The following API can be used to initiate software data encryption conversion.

* PATCH  /api/security -d '{ "software_data_encryption.conversion_enabled" : true }'<br/>
The following API can be used to initiate software data encryption rekey on ASA r2 platforms.

* PATCH  /api/security -d '{ "software_data_encryption.rekey" : true }'
## "fips" object
Contains FIPS mode information.<br/>
A PATCH request on this API using the parameter "fips.enabled" switches the system from using the default cryptographic module software implementations to validated ones or vice versa, where applicable. If the value of the parameter is "true" and unapproved algorithms are configured as permitted in relevant subsystems, those algorithms will be disabled in the relevant subsystem configurations. If "false", there will be no implied change to the relevant subsystem configurations.

* GET    /api/security
* GET    /api/security?fields=fips
* PATCH  /api/security -d '{ "fips.enabled" : true }'
* PATCH  /api/security -d '{ "fips.enabled" : false }'
## "tls" object
Contains TLS configuration information.<br/>
A PATCH request on this API using the parameter "tls.cipher_suites" and/or "tls.protocol_versions" configures the permissible cipher suites and/or protocol versions for all TLS-enabled applications in the system. All protocol versions at or above the lowest version level specified are enabled, including those that are not explicitly specified.

* GET    /api/security
* GET    /api/security?fields=tls
* PATCH  /api/security -d '{ "tls" : { "protocol_versions" : ["TLSv1.3", "TLSv1.2"], "cipher_suites" : ["TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384", "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"] } }'
## "management_protocols" object
Contains Security Protocols information.<br/>
This security protocols endpoint is used to retrieve and configure security protocols.

* GET    /api/security
* GET    /api/security?fields=management_protocols
* PATCH  /api/security -d '{ "management_protocols" : { "rsh_enabled" : true } }'
* PATCH  /api/security -d '{ "management_protocols" : { "rsh_enabled" : false } }'
* PATCH  /api/security -d '{ "management_protocols" : { "telnet_enabled" : true } }'
* PATCH  /api/security -d '{ "management_protocols" : { "telnet_enabled" : false } }'
* PATCH  /api/security -d '{ "management_protocols" : { "rsh_enabled" : true, "telnet_enabled" : true } }'
## GET Examples
### Retrieving information about the security configured on the cluster
The following example shows how to retrieve the configuration of the cluster.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityConfig()
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
SecurityConfig(
    {
        "onboard_key_manager_configurable_status": {
            "message": "Onboard Key Manager cannot be configured on the cluster. There are no self-encrypting disks in the cluster, and the following nodes do not support volume granular encryption: ntap-vsim2.",
            "code": 65537300,
            "supported": False,
        },
        "tls": {
            "protocol_versions": ["TLSv1.3", "TLSv1.2"],
            "cipher_suites": [
                "TLS_RSA_WITH_AES_128_CCM",
                "TLS_RSA_WITH_AES_128_CCM_8",
                "TLS_RSA_WITH_AES_128_GCM_SHA256",
                "TLS_RSA_WITH_AES_128_CBC_SHA",
                "TLS_RSA_WITH_AES_128_CBC_SHA256",
                "TLS_RSA_WITH_AES_256_CCM",
                "TLS_RSA_WITH_AES_256_CCM_8",
                "TLS_RSA_WITH_AES_256_GCM_SHA384",
                "TLS_RSA_WITH_AES_256_CBC_SHA",
                "TLS_RSA_WITH_AES_256_CBC_SHA256",
                "TLS_RSA_WITH_ARIA_128_GCM_SHA256",
                "TLS_RSA_WITH_ARIA_256_GCM_SHA384",
                "TLS_RSA_WITH_CAMELLIA_128_CBC_SHA",
                "TLS_RSA_WITH_CAMELLIA_128_CBC_SHA256",
                "TLS_RSA_WITH_CAMELLIA_256_CBC_SHA",
                "TLS_RSA_WITH_CAMELLIA_256_CBC_SHA256",
                "TLS_DHE_DSS_WITH_AES_128_GCM_SHA256",
                "TLS_DHE_DSS_WITH_AES_128_CBC_SHA",
                "TLS_DHE_DSS_WITH_AES_128_CBC_SHA256",
                "TLS_DHE_DSS_WITH_AES_256_GCM_SHA384",
                "TLS_DHE_DSS_WITH_AES_256_CBC_SHA",
                "TLS_DHE_DSS_WITH_AES_256_CBC_SHA256",
                "TLS_DHE_DSS_WITH_ARIA_128_GCM_SHA256",
                "TLS_DHE_DSS_WITH_ARIA_256_GCM_SHA384",
                "TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA",
                "TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA256",
                "TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA",
                "TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA256",
                "TLS_DHE_PSK_WITH_AES_128_CBC_SHA",
                "TLS_DHE_PSK_WITH_AES_128_CBC_SHA256",
                "TLS_DHE_PSK_WITH_AES_128_CCM",
                "TLS_PSK_DHE_WITH_AES_128_CCM_8",
                "TLS_DHE_PSK_WITH_AES_128_GCM_SHA256",
                "TLS_DHE_PSK_WITH_AES_256_CBC_SHA",
                "TLS_DHE_PSK_WITH_AES_256_CBC_SHA384",
                "TLS_DHE_PSK_WITH_AES_256_CCM",
                "TLS_PSK_DHE_WITH_AES_256_CCM_8",
                "TLS_DHE_PSK_WITH_AES_256_GCM_SHA384",
                "TLS_DHE_PSK_WITH_ARIA_128_GCM_SHA256",
                "TLS_DHE_PSK_WITH_ARIA_256_GCM_SHA384",
                "TLS_DHE_PSK_WITH_CAMELLIA_128_CBC_SHA256",
                "TLS_DHE_PSK_WITH_CAMELLIA_256_CBC_SHA384",
                "TLS_DHE_PSK_WITH_CHACHA20_POLY1305_SHA256",
                "TLS_DHE_RSA_WITH_AES_128_CCM",
                "TLS_DHE_RSA_WITH_AES_128_CCM_8",
                "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256",
                "TLS_DHE_RSA_WITH_AES_128_CBC_SHA",
                "TLS_DHE_RSA_WITH_AES_128_CBC_SHA256",
                "TLS_DHE_RSA_WITH_AES_256_CCM",
                "TLS_DHE_RSA_WITH_AES_256_CCM_8",
                "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384",
                "TLS_DHE_RSA_WITH_AES_256_CBC_SHA",
                "TLS_DHE_RSA_WITH_AES_256_CBC_SHA256",
                "TLS_DHE_RSA_WITH_ARIA_128_GCM_SHA256",
                "TLS_DHE_RSA_WITH_ARIA_256_GCM_SHA384",
                "TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA",
                "TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA256",
                "TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA",
                "TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA256",
                "TLS_DHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
                "TLS_ECDHE_RSA_WITH_ARIA_128_GCM_SHA256",
                "TLS_ECDHE_RSA_WITH_ARIA_256_GCM_SHA384",
                "TLS_ECDHE_ECDSA_WITH_AES_128_CCM",
                "TLS_ECDHE_ECDSA_WITH_AES_128_CCM_8",
                "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
                "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
                "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
                "TLS_ECDHE_ECDSA_WITH_AES_256_CCM",
                "TLS_ECDHE_ECDSA_WITH_AES_256_CCM_8",
                "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
                "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
                "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
                "TLS_ECDHE_ECDSA_WITH_ARIA_128_GCM_SHA256",
                "TLS_ECDHE_ECDSA_WITH_ARIA_256_GCM_SHA384",
                "TLS_ECDHE_ECDSA_WITH_CAMELLIA_128_CBC_SHA256",
                "TLS_ECDHE_ECDSA_WITH_CAMELLIA_256_CBC_SHA384",
                "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
                "TLS_ECDHE_PSK_WITH_AES_128_CBC_SHA",
                "TLS_ECDHE_PSK_WITH_AES_128_CBC_SHA256",
                "TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA",
                "TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA384",
                "TLS_ECDHE_PSK_WITH_CAMELLIA_128_CBC_SHA256",
                "TLS_ECDHE_PSK_WITH_CAMELLIA_256_CBC_SHA384",
                "TLS_ECDHE_PSK_WITH_CHACHA20_POLY1305_SHA256",
                "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
                "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA",
                "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
                "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
                "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
                "TLS_ECDHE_RSA_WITH_CAMELLIA_128_CBC_SHA256",
                "TLS_ECDHE_RSA_WITH_CAMELLIA_256_CBC_SHA384",
                "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
                "TLS_PSK_WITH_AES_128_CBC_SHA",
                "TLS_PSK_WITH_AES_128_CBC_SHA256",
                "TLS_PSK_WITH_AES_128_CCM",
                "TLS_PSK_WITH_AES_128_CCM_8",
                "TLS_PSK_WITH_AES_128_GCM_SHA256",
                "TLS_PSK_WITH_AES_256_CBC_SHA",
                "TLS_PSK_WITH_AES_256_CBC_SHA384",
                "TLS_PSK_WITH_AES_256_CCM",
                "TLS_PSK_WITH_AES_256_CCM_8",
                "TLS_PSK_WITH_AES_256_GCM_SHA384",
                "TLS_PSK_WITH_ARIA_128_GCM_SHA256",
                "TLS_PSK_WITH_ARIA_256_GCM_SHA384",
                "TLS_PSK_WITH_CAMELLIA_128_CBC_SHA256",
                "TLS_PSK_WITH_CAMELLIA_256_CBC_SHA384",
                "TLS_PSK_WITH_CHACHA20_POLY1305_SHA256",
                "TLS_RSA_PSK_WITH_AES_128_CBC_SHA",
                "TLS_RSA_PSK_WITH_AES_128_CBC_SHA256",
                "TLS_RSA_PSK_WITH_AES_128_GCM_SHA256",
                "TLS_RSA_PSK_WITH_AES_256_CBC_SHA",
                "TLS_RSA_PSK_WITH_AES_256_CBC_SHA384",
                "TLS_RSA_PSK_WITH_AES_256_GCM_SHA384",
                "TLS_RSA_PSK_WITH_ARIA_128_GCM_SHA256",
                "TLS_RSA_PSK_WITH_ARIA_256_GCM_SHA384",
                "TLS_RSA_PSK_WITH_CAMELLIA_128_CBC_SHA256",
                "TLS_RSA_PSK_WITH_CAMELLIA_256_CBC_SHA384",
                "TLS_RSA_PSK_WITH_CHACHA20_POLY1305_SHA256",
                "TLS_SRP_SHA_WITH_AES_128_CBC_SHA",
                "TLS_SRP_SHA_WITH_AES_256_CBC_SHA",
                "TLS_SRP_SHA_DSS_WITH_AES_128_CBC_SHA",
                "TLS_SRP_SHA_DSS_WITH_AES_256_CBC_SHA",
                "TLS_SRP_SHA_RSA_WITH_AES_128_CBC_SHA",
                "TLS_SRP_SHA_RSA_WITH_AES_256_CBC_SHA",
                "TLS_AES_128_GCM_SHA256",
                "TLS_AES_256_GCM_SHA384",
                "TLS_CHACHA20_POLY1305_SHA256",
            ],
        },
        "fips": {"enabled": False},
        "software_data_encryption": {
            "encryption_state": "unencrypted",
            "conversion_enabled": False,
            "disabled_by_default": False,
        },
        "management_protocols": {"telnet_enabled": False, "rsh_enabled": False},
    }
)

```
</div>
</div>

---
```
---
## PATCH Examples
### Enabling software encryption conversion in the cluster
The following example shows how to enable software encryption conversion in the cluster.
# The API:
PATCH /api/security
# The call
curl -X PATCH "https://<mgmt_ip>/api/security" -d '{ "software_data_encryption.conversion_enabled" : true }'
# The response:
{
   "job": {
       "uuid": "ebcbd82d-1cd4-11ea-8f75-005056ac4adc",
       "_links": {
           "self": {
               "href": "/api/cluster/jobs/ebcbd82d-1cd4-11ea-8f75-005056ac4adc"
           }
       }
   }
}
This returns a job UUID. A subsequent GET for this job UUID returns details of the job.
# The call
curl -X GET "https://<mgmt_ip>/api/cluster/jobs/ebcbd82d-1cd4-11ea-8f75-005056ac4adc"
# The response:
{
  "uuid": "ebcbd82d-1cd4-11ea-8f75-005056ac4adc",
  "description": "PATCH /api/security",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2019-12-12T06:45:40-05:00",
  "end_time": "2019-12-12T06:45:40-05:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/ebcbd82d-1cd4-11ea-8f75-005056ac4adc"
    }
  }
}
### Triggering software encryption rekey in the cluster
### Platform Specifics

* **ASA r2**:
The following example shows how to trigger software encryption rekey in the cluster.
# The API:
PATCH /api/security
# The call
curl -X PATCH "https://<mgmt_ip>/api/security" -d '{ "software_data_encryption.rekey" : true }'
# The response:
{
   "job": {
       "uuid": "ebcbd82d-1cd4-11ea-8f75-005056ac4adc",
       "_links": {
           "self": {
               "href": "/api/cluster/jobs/ebcbd82d-1cd4-11ea-8f75-005056ac4adc"
           }
       }
   }
}
This returns a job UUID. A subsequent GET for this job UUID returns details of the job.
# The call
curl -X GET "https://<mgmt_ip>/api/cluster/jobs/ebcbd82d-1cd4-11ea-8f75-005056ac4adc"
# The response:
{
  "uuid": "ebcbd82d-1cd4-11ea-8f75-005056ac4adc",
  "description": "PATCH /api/security",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2019-12-12T06:45:40-05:00",
  "end_time": "2019-12-12T06:45:40-05:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/ebcbd82d-1cd4-11ea-8f75-005056ac4adc"
    }
  }
}
### Enabling FIPS mode in the cluster
The following example shows how to enable FIPS mode in the cluster.
# The API:
PATCH /api/security
# The call
curl -X PATCH "https://<mgmt_ip>/api/security" -d '{ "fips.enabled" : true }'
# The response:
{
   "job": {
       "uuid": "8e7f59ee-a9c4-4faa-9513-bef689bbf2c2",
       "_links": {
           "self": {
               "href": "/api/cluster/jobs/8e7f59ee-a9c4-4faa-9513-bef689bbf2c2"
           }
       }
   }
}
This returns a job UUID. A subsequent GET for this job UUID returns details of the job.
# The call
curl -X GET "https://<mgmt_ip>/api/cluster/jobs/8e7f59ee-a9c4-4faa-9513-bef689bbf2c2"
# The response:
{
  "uuid": "8e7f59ee-a9c4-4faa-9513-bef689bbf2c2",
  "description": "PATCH /api/security",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2020-04-28T06:55:40-05:00",
  "end_time": "2020-04-28T06:55:41-05:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/8e7f59ee-a9c4-4faa-9513-bef689bbf2c2"
    }
  }
}
### Configuring permissible TLS protocols and cipher suites in the cluster
The following example shows how to configure the cluster to only allow TLSv1.3 & TLSv1.2 with selected cipher suites.
# The API:
PATCH /api/security
# The call
curl -X PATCH "https://<mgmt_ip>/api/security" -d '{ "tls" : { "protocol_versions" : ["TLSv1.3", TLSv1.2"], "cipher_suites" : ["TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384", "TLS_AES_256_GCM_SHA384"] } }'
# The response:
{
   "job": {
       "uuid": "b45b6290-f4f2-442a-aa0e-4d3ffefe5e0d",
       "_links": {
           "self": {
               "href": "/api/cluster/jobs/b45b6290-f4f2-442a-aa0e-4d3ffefe5e0d"
           }
       }
   }
}
This returns a job UUID. A subsequent GET for this job UUID returns details of the job.
# The call
curl -X GET "https://<mgmt_ip>/api/cluster/jobs/b45b6290-f4f2-442a-aa0e-4d3ffefe5e0d"
# The response:
{
  "uuid": "b45b6290-f4f2-442a-aa0e-4d3ffefe5e0d",
  "description": "PATCH /api/security",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2021-03-22T08:52:50-05:00",
  "end_time": "2021-03-22T08:52:51-05:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/b45b6290-f4f2-442a-aa0e-4d3ffefe5e0d"
    }
  }
}
### Enabling security protocols in the cluster
The following example shows how to enable the security protocol rsh in the cluster.
# The API:
PATCH /api/security
# The call
curl -X PATCH "https://<mgmt_ip>/api/security" -d '{ "management_protocols" : { "rsh_enabled" : true } }'
# The response
{
  "job": {
  "uuid": "2980ba28-adab-11eb-8fa3-005056bbfa84",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/2980ba28-adab-11eb-8fa3-005056bbfa84"
    }
   }
 }
}
# The call:
curl -H "accept: application/hal+json" -X GET "https://<mgmt-ip>/api/security/?fields=management_protocols"
# The response:
{
  "management_protocols": {
    "rsh_enabled": false,
    "telnet_enabled": false
  },
  "_links": {
    "self": {
      "href": "/api/security"
    }
  }
}
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


__all__ = ["SecurityConfig", "SecurityConfigSchema"]
__pdoc__ = {
    "SecurityConfigSchema.resource": False,
    "SecurityConfigSchema.opts": False,
}


class SecurityConfigSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityConfig object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the security_config."""

    fips = marshmallow_fields.Nested("netapp_ontap.models.fips.FipsSchema", data_key="fips", unknown=EXCLUDE, allow_none=True)
    r""" Cluster-wide Federal Information Processing Standards (FIPS) mode information."""

    management_protocols = marshmallow_fields.Nested("netapp_ontap.models.management_protocols.ManagementProtocolsSchema", data_key="management_protocols", unknown=EXCLUDE, allow_none=True)
    r""" Cluster-wide security protocols related information."""

    onboard_key_manager_configurable_status = marshmallow_fields.Nested("netapp_ontap.models.onboard_key_manager_configurable_status.OnboardKeyManagerConfigurableStatusSchema", data_key="onboard_key_manager_configurable_status", unknown=EXCLUDE, allow_none=True)
    r""" Indicates whether the Onboard Key Manager can be configured in the cluster."""

    software_data_encryption = marshmallow_fields.Nested("netapp_ontap.models.software_data_encryption.SoftwareDataEncryptionSchema", data_key="software_data_encryption", unknown=EXCLUDE, allow_none=True)
    r""" Cluster-wide software data encryption related information."""

    tls = marshmallow_fields.Nested("netapp_ontap.models.tls.TlsSchema", data_key="tls", unknown=EXCLUDE, allow_none=True)
    r""" Cluster-wide Transport Layer Security (TLS) configuration information"""

    @property
    def resource(self):
        return SecurityConfig

    gettable_fields = [
        "links",
        "fips",
        "management_protocols",
        "onboard_key_manager_configurable_status",
        "software_data_encryption",
        "tls",
    ]
    """links,fips,management_protocols,onboard_key_manager_configurable_status,software_data_encryption,tls,"""

    patchable_fields = [
        "fips",
        "management_protocols",
        "software_data_encryption",
        "tls",
    ]
    """fips,management_protocols,software_data_encryption,tls,"""

    postable_fields = [
        "fips",
        "management_protocols",
        "software_data_encryption",
        "tls",
    ]
    """fips,management_protocols,software_data_encryption,tls,"""

class SecurityConfig(Resource):
    """Allows interaction with SecurityConfig objects on the host"""

    _schema = SecurityConfigSchema
    _path = "/api/security"
    _action_form_data_parameters = { 'file':'file', }






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves information about the security configured on the cluster.
### Related ONTAP commands
* `security config show`

### Learn more
* [`DOC /security`](#docs-security-security)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)


    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the software FIPS mode or modifies software data encryption.
## Platform Specifics
### Unified ONTAP
The PATCH request can be used to enable conversion of non-encrypted metadata volumes to encrypted metadata volumes and non-NAE aggregates to NAE aggregates.
### ASA r2
The PATCH request can be used to enable conversion of all non-encrypted volumes and LUNs to encrypted volumes and LUNs.
The PATCH request can also be used to start the rekey of all encrypted volumes and LUNs.
### Related ONTAP commands
* `security config modify`

### Learn more
* [`DOC /security`](#docs-security-security)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)


    def certificate_signing_request(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""This API generates a Certificate Signing Request(CSR) and a private key pair. A CSR is a message sent securely to a certificate authority (CA) via any electronic media to apply for a digital identity certificate. This is a general utility API for users to generate a CSR.
### Required properties
* `subject_name` - Subject details of the certificate, including but not limited to the common name. Can be omitted if subject_alternatives is specified.
* `subject_alternatives` - Subject Alternate Name (SAN) extensions. Only required if a common name is not specified using subject_name.
### Recommended optional properties
* `security_strength` - Key size of the certificate, in bits. Specifying a stronger security strength in bits is recommended when creating a certificate. A value of at least 128 is necessary when using EC algorithm if the certificate is to be used in the context of TLSv1.3.
* `hash_function` -  Hashing function.
* `algorithm` - Asymmetric algorithm. Algorithm used to generate a public/private key pair when creating a certificate.
### Default property values
If not specified in POST, the following default property values are assigned:
* `security_strength` - _112_
* `hash_function` - _sha256_
* `algorithm` - _rsa_
### Related ONTAP commands
* `security certificate generate-csr`
"""
        return super()._action(
            "certificate-signing-request", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    certificate_signing_request.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)

