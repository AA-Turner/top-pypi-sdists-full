r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A key manager is a key management solution (software or dedicated hardware) that enables other ONTAP client modules to securely and persistently store keys for various uses. For example, WAFL uses the key management framework to store and retrieve the volume encryption keys that it uses to encrypt/decrypt data on NVE volumes. A key manager can be configured at both cluster scope and SVM, with one key manager allowed per SVM. The key management framework in ONTAP supports two mutually exclusive modes for persisting keys: external and onboard.<p/>
When an SVM is configured with external key management, the keys are stored on up to four primary key servers that are external to the system.<p/>
Once external key management is enabled for an SVM, primary key servers can be added or removed using the <i>/api/security/key-managers/{uuid}/key-servers</i> endpoint. See [`POST /security/key-managers/{uuid}/key-servers`] and [`DELETE /security/key-managers/{uuid}/key-servers/{server}`] for more details.<p/>
Setting up external key management dictates that the required certificates for securely communicating with the key server are installed prior to configuring the key manager. To install the required client and server_ca certificates, use the <i>/api/security/certificates/</i> endpoint. <p/>
See [`POST /security/certificates`], [`GET /security/certificates/uuid`] and [`DELETE /security/certificates/{uuid}`] for more details.<p/>
When an SVM is configured with the Onboard Key Manager, the keys are stored in ONTAP in wrapped format using a key hierarchy created using the salted hash of the passphrase entered when configuring the Onboard Key Manager. This model fits well for customers who use ONTAP to store their own data. <p/>
## Examples
### Creating an external key manager with 1 primary key server for a cluster
The example key manager is configured at the cluster-scope with one primary key server. Note that the UUIDs of the certificates are those that are already installed at the cluster-scope. Note the <i>return_records=true</i> query parameter is used to obtain the newly created key manager configuration.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeyManager

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityKeyManager()
    resource.external = {
        "client_certificate": {"uuid": "5fb1701a-d922-11e8-bfe8-005056bb017d"},
        "server_ca_certificates": [{"uuid": "827d7d31-d6c8-11e8-b5bf-005056bb017d"}],
        "servers": [{"server": "10.225.89.33:5696"}],
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
SecurityKeyManager(
    {
        "uuid": "815e9462-dc57-11e8-9b2c-005056bb017d",
        "_links": {
            "self": {
                "href": "/api/security/key-managers/815e9462-dc57-11e8-9b2c-005056bb017d"
            }
        },
        "external": {
            "servers": [{"server": "10.225.89.33:5696"}],
            "server_ca_certificates": [
                {"uuid": "827d7d31-d6c8-11e8-b5bf-005056bb017d"}
            ],
            "client_certificate": {"uuid": "5fb1701a-d922-11e8-bfe8-005056bb017d"},
        },
    }
)

```
</div>
</div>

---
### Creating an external key manager with two primary key servers
The example key manager is configured at the cluster-scope with two primary key servers. Note that the UUIDs of the certificates are those that are already installed at the cluster-scope. Note the <i>return_records=true</i> query parameter is used to obtain the newly created key manager configuration.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeyManager

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityKeyManager()
    resource.external = {
        "client_certificate": {"uuid": "5fb1701a-d922-11e8-bfe8-005056bb017d"},
        "server_ca_certificates": [{"uuid": "827d7d31-d6c8-11e8-b5bf-005056bb017d"}],
        "servers": [{"server": "104.224.89.33:5696"}, {"server": "104.224.89.34:5696"}],
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
SecurityKeyManager(
    {
        "uuid": "815e9462-dc57-11e8-9b2c-005056bb017d",
        "_links": {
            "self": {
                "href": "/api/security/key-managers/815e9462-dc57-11e8-9b2c-005056bb017d"
            }
        },
        "external": {
            "servers": [
                {"server": "10.225.89.33:5696"},
                {"server": "10.225.89.34:5696"},
            ],
            "server_ca_certificates": [
                {"uuid": "827d7d31-d6c8-11e8-b5bf-005056bb017d"}
            ],
            "client_certificate": {"uuid": "5fb1701a-d922-11e8-bfe8-005056bb017d"},
        },
    }
)

```
</div>
</div>

---
### Creating an external key manager with 1 primary key server for an SVM
The example key manager is configured at the SVM-scope with one primary key server. Note that the UUIDs of the certificates are those that are already installed in that SVM. Note the <i>return_records=true</i> query parameter is used to obtain the newly created key manager configuration.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeyManager

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityKeyManager()
    resource.svm = {"uuid": "216e6c26-d6c6-11e8-b5bf-005056bb017d"}
    resource.external = {
        "client_certificate": {"uuid": "91dcaf7c-dbbd-11e8-9b2c-005056bb017d"},
        "server_ca_certificates": [{"uuid": "a4d4b8ba-dbbd-11e8-9b2c-005056bb017d"}],
        "servers": [{"server": "10.225.89.34:5696"}],
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
SecurityKeyManager(
    {
        "uuid": "80af63f2-dbbf-11e8-9b2c-005056bb017d",
        "_links": {
            "self": {
                "href": "/api/security/key-managers/80af63f2-dbbf-11e8-9b2c-005056bb017d"
            }
        },
        "svm": {"uuid": "216e6c26-d6c6-11e8-b5bf-005056bb017d"},
        "external": {
            "servers": [{"server": "10.225.89.34:5696"}],
            "server_ca_certificates": [
                {"uuid": "a4d4b8ba-dbbd-11e8-9b2c-005056bb017d"}
            ],
            "client_certificate": {"uuid": "91dcaf7c-dbbd-11e8-9b2c-005056bb017d"},
        },
    }
)

```
</div>
</div>

---
### Creating an onboard key manager for a cluster
The following example shows how to create an onboard key manager for a cluster with the onboard key manager configured at the cluster-scope.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeyManager

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityKeyManager()
    resource.onboard = {"passphrase": "passphrase"}
    resource.post(hydrate=True)
    print(resource)

```

---
### Retrieving the key manager configurations for all clusters and SVMs
The following example shows how to retrieve all configured key managers along with their configurations.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeyManager

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SecurityKeyManager.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
[
    SecurityKeyManager(
        {
            "configuration": {
                "name": "default",
                "uuid": "2345f09c-d6c9-11e8-b5bf-005056bb017d",
            },
            "uuid": "2345f09c-d6c9-11e8-b5bf-005056bb017d",
            "_links": {
                "self": {
                    "href": "/api/security/key-managers/2345f09c-d6c9-11e8-b5bf-005056bb017d"
                }
            },
            "svm": {"name": "vs0", "uuid": "0f22f8f3-d6c6-11e8-b5bf-005056bb017d"},
            "external": {
                "servers": [
                    {
                        "timeout": 25,
                        "username": "",
                        "_links": {
                            "self": {
                                "href": "/api/security/key-managers/2345f09c-d6c9-11e8-b5bf-005056bb017d/key-servers/10.2.30.4:5696/"
                            }
                        },
                        "server": "10.2.30.4:5696",
                    },
                    {
                        "timeout": 25,
                        "secondary_key_servers": "1.1.1.1, secondarykeyserver.com",
                        "username": "",
                        "_links": {
                            "self": {
                                "href": "/api/security/key-managers/2345f09c-d6c9-11e8-b5bf-005056bb017d/key-servers/vs0.local1:3678/"
                            }
                        },
                        "server": "vs0.local1:3678",
                    },
                ],
                "server_ca_certificates": [
                    {
                        "_links": {
                            "self": {
                                "href": "/api/security/certificates/8a17c858-d6c8-11e8-b5bf-005056bb017d/"
                            }
                        },
                        "uuid": "8a17c858-d6c8-11e8-b5bf-005056bb017d",
                    }
                ],
                "client_certificate": {
                    "_links": {
                        "self": {
                            "href": "/api/security/certificates/4cb15482-d6c8-11e8-b5bf-005056bb017d/"
                        }
                    },
                    "uuid": "4cb15482-d6c8-11e8-b5bf-005056bb017d",
                },
            },
            "scope": "svm",
        }
    ),
    SecurityKeyManager(
        {
            "configuration": {
                "name": "default",
                "uuid": "815e9462-dc57-11e8-9b2c-005056bb017d",
            },
            "uuid": "815e9462-dc57-11e8-9b2c-005056bb017d",
            "enabled": True,
            "_links": {
                "self": {
                    "href": "/api/security/key-managers/815e9462-dc57-11e8-9b2c-005056bb017d"
                }
            },
            "external": {
                "servers": [
                    {
                        "timeout": 25,
                        "username": "",
                        "_links": {
                            "self": {
                                "href": "/api/security/key-managers/815e9462-dc57-11e8-9b2c-005056bb017d/key-servers/10.225.89.33:5696/"
                            }
                        },
                        "server": "10.225.89.33:5696",
                    }
                ],
                "server_ca_certificates": [
                    {
                        "_links": {
                            "self": {
                                "href": "/api/security/certificates/827d7d31-d6c8-11e8-b5bf-005056bb017d/"
                            }
                        },
                        "uuid": "827d7d31-d6c8-11e8-b5bf-005056bb017d",
                    }
                ],
                "client_certificate": {
                    "_links": {
                        "self": {
                            "href": "/api/security/certificates/5fb1701a-d922-11e8-bfe8-005056bb017d/"
                        }
                    },
                    "uuid": "5fb1701a-d922-11e8-bfe8-005056bb017d",
                },
            },
            "scope": "cluster",
        }
    ),
]

```
</div>
</div>

---
### Retrieving the key manager configurations for all clusters and SVMs (showing Onboard Key Manager)
The following example shows how to retrieve all configured key managers along with their configurations.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeyManager

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SecurityKeyManager.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
[
    SecurityKeyManager(
        {
            "onboard": {
                "enabled": True,
                "key_backup": "--------------------------BEGIN BACKUP--------------------------\n <Backup Data> \n---------------------------END BACKUP---------------------------\n",
            },
            "configuration": {
                "name": "default",
                "uuid": "815e9462-dc57-11e8-9b2c-005056bb017d",
            },
            "is_default_data_at_rest_encryption_disabled": False,
            "uuid": "8ba52e0f-ae22-11e9-b747-005056bb7636",
            "enabled": True,
            "volume_encryption": {
                "message": "The following nodes do not support volume granular encryption: ntap-vsim2.",
                "code": 65536935,
                "supported": False,
            },
            "scope": "cluster",
        }
    )
]

```
</div>
</div>

---
### Retrieving expensive fields such as, status.code and status.message, associated with a key manager.
These values are not retrieved by default with the 'fields=*' option.
The following example shows how to retrieve the expensive objects associated with a key manager.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeyManager

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SecurityKeyManager.get_collection(fields="status.message,status.code")))

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
[
    SecurityKeyManager(
        {
            "status": {"message": "No action needed at this time.", "code": 65537200},
            "configuration": {
                "name": "default",
                "uuid": "ac305d46-aef4-11e9-ad3c-005056bb7636",
            },
            "uuid": "ac305d46-aef4-11e9-ad3c-005056bb7636",
            "enabled": True,
            "_links": {
                "self": {
                    "href": "/api/security/key-managers/ac305d46-aef4-11e9-ad3c-005056bb7636"
                }
            },
        }
    )
]

```
</div>
</div>

---
### Retrieving a specific key manager configuration
The following example shows how to retrieve a specific key manager configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeyManager

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityKeyManager(uuid="<uuid>")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
SecurityKeyManager(
    {
        "configuration": {
            "name": "default",
            "uuid": "2345f09c-d6c9-11e8-b5bf-005056bb017d",
        },
        "uuid": "2345f09c-d6c9-11e8-b5bf-005056bb017d",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/security/key-managers/2345f09c-d6c9-11e8-b5bf-005056bb017d"
            }
        },
        "svm": {"name": "vs0", "uuid": "0f22f8f3-d6c6-11e8-b5bf-005056bb017d"},
        "external": {
            "servers": [
                {
                    "timeout": 25,
                    "username": "",
                    "_links": {
                        "self": {
                            "href": "/api/security/key-managers/2345f09c-d6c9-11e8-b5bf-005056bb017d/key-servers/10.2.30.4:5696/"
                        }
                    },
                    "server": "10.2.30.4:5696",
                },
                {
                    "timeout": 25,
                    "username": "",
                    "_links": {
                        "self": {
                            "href": "/api/security/key-managers/2345f09c-d6c9-11e8-b5bf-005056bb017d/key-servers/vs0.local1:3678/"
                        }
                    },
                    "server": "vs0.local1:3678",
                },
            ],
            "server_ca_certificates": [
                {
                    "_links": {
                        "self": {
                            "href": "/api/security/certificates/8a17c858-d6c8-11e8-b5bf-005056bb017d/"
                        }
                    },
                    "uuid": "8a17c858-d6c8-11e8-b5bf-005056bb017d",
                }
            ],
            "client_certificate": {
                "_links": {
                    "self": {
                        "href": "/api/security/certificates/4cb15482-d6c8-11e8-b5bf-005056bb017d/"
                    }
                },
                "uuid": "4cb15482-d6c8-11e8-b5bf-005056bb017d",
            },
        },
        "scope": "svm",
    }
)

```
</div>
</div>

---
### Updating the configuration of an external key manager
The following example shows how to update the server_ca configuration of an external key manager.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeyManager

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityKeyManager(uuid="<uuid>")
    resource.external = {
        "server_ca_certificates": [{"uuid": "23b05c58-d790-11e8-b5bf-005056bb017d"}]
    }
    resource.patch()

```

---
### Updating the passphrase of an Onboard Key Manager
The following example shows how to update the passphrase of a given key manager.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeyManager

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityKeyManager(uuid="<uuid>")
    resource.onboard = {
        "existing_passphrase": "existing_passphrase",
        "passphrase": "new_passphrase",
    }
    resource.patch()

```

---
### Synchronizing the passphrase of the Onboard Key Manager on a cluster
The following example shows how to synchronize the passphrase on a cluster where the Onboard Key Manager is already configured.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeyManager

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityKeyManager(uuid="<uuid>")
    resource.onboard = {
        "existing_passphrase": "existing_passphrase",
        "synchronize": True,
    }
    resource.patch()

```

---
### Configuring the Onboard Key Manager on a cluster
The following example shows how to configure the Onboard Key Manager on a cluster where the Onboard Key Manager is not configured, but is configured on an MetroCluster partner cluster.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeyManager

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityKeyManager()
    resource.onboard = {"passphrase": "passphrase", "synchronize": True}
    resource.post(hydrate=True, return_records=False)
    print(resource)

```

---
### Deleting a configured key manager
The following example shows how to delete a key manager given its UUID.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityKeyManager

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityKeyManager(uuid="<uuid>")
    resource.delete()

```

---
### Adding a primary key server to an external key manager
The following example shows how to add a primary key server to an external key manager.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyServer("<uuid>")
    resource.server = "10.225.89.34:5696"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example13_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example13_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example13_result" class="try_it_out_content">
```
KeyServer(
    {
        "_links": {
            "self": {
                "href": "/api/security/key-managers/43e0c191-dc5c-11e8-9b2c-005056bb017d/key-servers/10.225.89.34%3A5696"
            }
        },
        "server": "10.225.89.34:5696",
    }
)

```
</div>
</div>

---
### Adding 2 primary key servers to an external key manager
The following example shows how to add 2 primary key servers to an external key manager. Note that the <i>records</i> property is used to add multiple primary key servers to the key manager in a single API call.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyServer("<uuid>")
    resource.records = [
        {"server": "10.225.89.34:5696"},
        {"server": "10.225.89.33:5696"},
    ]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example14_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example14_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example14_result" class="try_it_out_content">
```
KeyServer(
    {
        "_links": {
            "self": {
                "href": "/api/security/key-managers/43e0c191-dc5c-11e8-9b2c-005056bb017d/key-servers/"
            }
        }
    }
)

```
</div>
</div>

---
### Retrieving all the key servers configured in an external key manager
The following example shows how to retrieve all key servers configured in an external key manager.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(KeyServer.get_collection("<uuid>", fields="*")))

```
<div class="try_it_out">
<input id="example15_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example15_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example15_result" class="try_it_out_content">
```
[
    KeyServer(
        {
            "timeout": 25,
            "create_remove_timeout": 10,
            "secondary_key_servers": ["1.1.1.1", "secondarykeyserver.com"],
            "username": "",
            "_links": {
                "self": {
                    "href": "/api/security/key-managers/43e0c191-dc5c-11e8-9b2c-005056bb017d/key-servers/10.225.89.33%3A5696"
                }
            },
            "server": "10.225.89.33:5696",
        }
    ),
    KeyServer(
        {
            "timeout": 25,
            "create_remove_timeout": 10,
            "username": "",
            "_links": {
                "self": {
                    "href": "/api/security/key-managers/43e0c191-dc5c-11e8-9b2c-005056bb017d/key-servers/10.225.89.34%3A5696"
                }
            },
            "server": "10.225.89.34:5696",
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific primary key server (and any associated secondary key servers) configured in an external key manager
The following example shows how to retrieve a specific primary key server (and any associated secondary key servers) configured in an external key manager.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyServer("<uuid>", server="{server}")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example16_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example16_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example16_result" class="try_it_out_content">
```
KeyServer(
    {
        "timeout": 25,
        "create_remove_timeout": 10,
        "secondary_key_servers": ["1.1.1.1", "secondarykeyserver.com"],
        "username": "",
        "_links": {
            "self": {
                "href": "/api/security/key-managers/43e0c191-dc5c-11e8-9b2c-005056bb017d/key-servers/10.225.89.34:5696"
            }
        },
        "server": "10.225.89.34:5696",
    }
)

```
</div>
</div>

---
### Retrieving a specific primary key server (and any associated secondary key servers) (and connectivity, an expensive field) configured in an external key manager
The following example shows how to retrieve a specific primary key server (and any associated secondary key servers) configured in an external key manager.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyServer("<uuid>", server="{server}")
    resource.get(fields="**")
    print(resource)

```
<div class="try_it_out">
<input id="example17_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example17_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example17_result" class="try_it_out_content">
```
KeyServer(
    {
        "timeout": 25,
        "create_remove_timeout": 10,
        "secondary_key_servers": ["1.1.1.1", "secondarykeyserver.com"],
        "username": "",
        "connectivity": {
            "cluster_availability": True,
            "node_states": [
                {
                    "state": "available",
                    "node": {
                        "name": "sti65-vsim-ucs148i",
                        "uuid": "661843b3-a0e5-11ed-81ef-005056a7306b",
                    },
                },
                {
                    "state": "not_responding",
                    "node": {
                        "name": "sti65-vsim-ucs148j",
                        "uuid": "551843b3-a0e5-11ed-81ef-005056a7306b",
                    },
                },
            ],
        },
        "server": "10.225.89.34:5696",
    }
)

```
</div>
</div>

---
### Retrieving the connectivity status of a specific node for a specific primary key server configured in an external key manager
The following example shows how to retrieve the connectivity status for a specific node for a specific primary key server configured in an external key manager.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyServer(
        "43e0c191-dc5c-11e8-9b2c-005056bb017d", server="10.225.89.34:5696"
    )
    resource.get(
        fields="connectivity",
        return_unmatched_nested_array_objects=False,
        **{"connectivity.node_states.node.name": "sti65-vsim-ucs148i"}
    )
    print(resource)

```
<div class="try_it_out">
<input id="example18_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example18_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example18_result" class="try_it_out_content">
```
KeyServer(
    {
        "connectivity": {
            "cluster_availability": True,
            "node_states": [
                {
                    "state": "available",
                    "node": {
                        "name": "sti65-vsim-ucs148i",
                        "uuid": "661843b3-a0e5-11ed-81ef-005056a7306b",
                    },
                }
            ],
        },
        "server": "10.225.89.34:5696",
    }
)

```
</div>
</div>

---
### Updating a specific primary key server configuration configured in an external key manager
The following example shows how to update a specific primary key server configured in an external key manager.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyServer("<uuid>", server="{server}")
    resource.timeout = 45
    resource.patch()

```

---
### When the 'secondary_key_servers' field is populated in the PATCH API, the list of secondary key servers
### associated with the primary key servers is replaced by the list of secondary key servers specified in the
### 'secondary_key_servers' field.
The following example shows how to update the set of secondary key servers associated with a primary key server.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyServer("<uuid>", server="{server}")
    resource.secondary_key_servers = ["1.1.1.1", "secondarykeyserver.com"]
    resource.patch()

```

---
### Deleting a primary key server from an external key manager
The following example shows how to delete a primary key server from an external key manager.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyServer("<uuid>", server="{server}")
    resource.delete()

```

---
### Bypass the out of quorum checks when deleting a primary key server from an external key manager
The following example shows how to bypass the out of quorum checks when deleting a primary key server from an external key manager.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyServer("<uuid>", server="{server}")
    resource.delete(force=True)

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


__all__ = ["SecurityKeyManager", "SecurityKeyManagerSchema"]
__pdoc__ = {
    "SecurityKeyManagerSchema.resource": False,
    "SecurityKeyManagerSchema.opts": False,
}


class SecurityKeyManagerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityKeyManager object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the security_key_manager."""

    configuration = marshmallow_fields.Nested("netapp_ontap.models.security_keystore_configuration.SecurityKeystoreConfigurationSchema", data_key="configuration", unknown=EXCLUDE, allow_none=True)
    r""" Security keystore object reference."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates whether the configuration is enabled."""

    external = marshmallow_fields.Nested("netapp_ontap.models.security_key_manager_external.SecurityKeyManagerExternalSchema", data_key="external", unknown=EXCLUDE, allow_none=True)
    r""" Configures external key management"""

    is_default_data_at_rest_encryption_disabled = marshmallow_fields.Boolean(
        data_key="is_default_data_at_rest_encryption_disabled",
        allow_none=True,
    )
    r""" Indicates whether default data-at-rest encryption is disabled in the cluster. This field is deprecated in ONTAP 9.8 and later. Use the "software_data_encryption.disabled_by_default" of /api/security endpoint."""

    onboard = marshmallow_fields.Nested("netapp_ontap.models.security_key_manager_onboard.SecurityKeyManagerOnboardSchema", data_key="onboard", unknown=EXCLUDE, allow_none=True)
    r""" Configures onboard key management. After configuring onboard key management, save the encrypted configuration data in a safe location so that you can use it if you need to perform a manual recovery operation."""

    policy = marshmallow_fields.Str(
        data_key="policy",
        allow_none=True,
    )
    r""" Security policy associated with the key manager. This value is currently ignored if specified for the onboard key manager."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        allow_none=True,
    )
    r""" The scope field of the security_key_manager."""

    status = marshmallow_fields.Nested("netapp_ontap.models.key_manager_state.KeyManagerStateSchema", data_key="status", unknown=EXCLUDE, allow_none=True)
    r""" Optional status information on the current state of the key manager indicating if it is fully setup or requires more action."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the security_key_manager."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The uuid field of the security_key_manager."""

    volume_encryption = marshmallow_fields.Nested("netapp_ontap.models.volume_encryption_support.VolumeEncryptionSupportSchema", data_key="volume_encryption", unknown=EXCLUDE, allow_none=True)
    r""" Indicates whether volume encryption is supported in the cluster."""

    @property
    def resource(self):
        return SecurityKeyManager

    gettable_fields = [
        "links",
        "configuration",
        "enabled",
        "external",
        "is_default_data_at_rest_encryption_disabled",
        "onboard",
        "policy",
        "scope",
        "status",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
        "volume_encryption",
    ]
    """links,configuration,enabled,external,is_default_data_at_rest_encryption_disabled,onboard,policy,scope,status,svm.links,svm.name,svm.uuid,uuid,volume_encryption,"""

    patchable_fields = [
        "external",
        "is_default_data_at_rest_encryption_disabled",
        "onboard",
        "scope",
    ]
    """external,is_default_data_at_rest_encryption_disabled,onboard,scope,"""

    postable_fields = [
        "configuration",
        "external",
        "onboard",
        "policy",
        "scope",
        "svm.name",
        "svm.uuid",
    ]
    """configuration,external,onboard,policy,scope,svm.name,svm.uuid,"""

class SecurityKeyManager(Resource):
    """Allows interaction with SecurityKeyManager objects on the host"""

    _schema = SecurityKeyManagerSchema
    _path = "/api/security/key-managers"
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
        r"""Retrieves key managers.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity.cluster_availability`
* `connectivity.node_states.node.name`
* `connectivity.node_states.node.uuid`
* `connectivity.node_states.state`
* `status.message`
* `status.code`
### Related ONTAP commands
* `security key-manager show-key-store`
* `security key-manager external show`
* `security key-manager external show-status`
* `security key-manager onboard show-backup`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SecurityKeyManager resources that match the provided query"""
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
        """Returns a list of RawResources that represent SecurityKeyManager resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SecurityKeyManager"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a key manager.
NOTE: When validate_certificates is set, the API returns a 202 status code for successful creation of the job, otherwise an error is returned.
### Required properties (when patching the Onboard Key Manager)
* `onboard.existing_passphrase` - Cluster-wide passphrase. Required only when synchronizing the passphrase of the Onboard Key Manager.
* `synchronize` - Synchronizes missing Onboard Key Manager keys on any node in the cluster. Required only when synchronizing the Onboard Key Manager keys in a local cluster.
### Required properties (when patching an external key manager)
* `external.client_certificate` or `external.server_ca_certificates` - Client certificate or Server CA certificate. Required when modifying an external key manager.
### Optional parameters (when patching an external key manager):
* `validate_certificates` - Validate certificates by testing the connection to the KMIP server using them. This flag is set to "false" by default.
### Related ONTAP commands
* `security key-manager external modify`
* `security key-manager onboard sync`
* `security key-manager onboard update-passphrase`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SecurityKeyManager"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SecurityKeyManager"], NetAppResponse]:
        r"""Creates a key manager.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create a key manager.
* `external.client_certificate` - Client certificate. Required only when creating an external key manager.
* `external.server_ca_certificates` - Server CA certificates. Required only when creating an external key manager.
* `external.servers.server` - Primary Key servers. Required only when creating an external key manager.
* `onboard.passphrase` - Cluster-wide passphrase. Required only when creating an Onboard Key Manager.
* `synchronize` - Synchronizes missing onboard keys on any node in the cluster. Required only when creating an Onboard Key Manager at the partner site of a MetroCluster configuration.
### Optional parameters:
* `create_inactive` - Create a configuration without enabling it. This flag is set to "false" by default.
### Related ONTAP commands
* `security key-manager external enable`
* `security key-manager onboard enable`
* `security key-manager onboard sync`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["SecurityKeyManager"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a key manager.
### Related ONTAP commands
* `security key-manager external disable`
* `security key-manager onboard disable`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves key managers.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity.cluster_availability`
* `connectivity.node_states.node.name`
* `connectivity.node_states.node.uuid`
* `connectivity.node_states.state`
* `status.message`
* `status.code`
### Related ONTAP commands
* `security key-manager show-key-store`
* `security key-manager external show`
* `security key-manager external show-status`
* `security key-manager onboard show-backup`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves key managers.
### Examples:
- To retrieve basic information about a key server:
  ```
  GET /security/key-managers/{uuid}
  ```
- To retrieve specific fields, including expensive properties:
  ```
  GET /security/key-managers/{uuid}?fields=connectivity.cluster_availability,connectivity.node_states.node.name
  ```
### Note:
These fields are not available for inactive configurations due to the additional computational cost and the relevance of these fields is exclusive to active configurations.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity.cluster_availability`
* `connectivity.node_states.node.name`
* `connectivity.node_states.node.uuid`
* `connectivity.node_states.state`
* `status.message`
* `status.code`
### Related ONTAP commands
* `security key-manager show-key-store`
* `security key-manager external show`
* `security key-manager external show-status`
* `security key-manager onboard show-backup`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
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
        r"""Creates a key manager.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create a key manager.
* `external.client_certificate` - Client certificate. Required only when creating an external key manager.
* `external.server_ca_certificates` - Server CA certificates. Required only when creating an external key manager.
* `external.servers.server` - Primary Key servers. Required only when creating an external key manager.
* `onboard.passphrase` - Cluster-wide passphrase. Required only when creating an Onboard Key Manager.
* `synchronize` - Synchronizes missing onboard keys on any node in the cluster. Required only when creating an Onboard Key Manager at the partner site of a MetroCluster configuration.
### Optional parameters:
* `create_inactive` - Create a configuration without enabling it. This flag is set to "false" by default.
### Related ONTAP commands
* `security key-manager external enable`
* `security key-manager onboard enable`
* `security key-manager onboard sync`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
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
        r"""Updates a key manager.
NOTE: When validate_certificates is set, the API returns a 202 status code for successful creation of the job, otherwise an error is returned.
### Required properties (when patching the Onboard Key Manager)
* `onboard.existing_passphrase` - Cluster-wide passphrase. Required only when synchronizing the passphrase of the Onboard Key Manager.
* `synchronize` - Synchronizes missing Onboard Key Manager keys on any node in the cluster. Required only when synchronizing the Onboard Key Manager keys in a local cluster.
### Required properties (when patching an external key manager)
* `external.client_certificate` or `external.server_ca_certificates` - Client certificate or Server CA certificate. Required when modifying an external key manager.
### Optional parameters (when patching an external key manager):
* `validate_certificates` - Validate certificates by testing the connection to the KMIP server using them. This flag is set to "false" by default.
### Related ONTAP commands
* `security key-manager external modify`
* `security key-manager onboard sync`
* `security key-manager onboard update-passphrase`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
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
        r"""Deletes a key manager.
### Related ONTAP commands
* `security key-manager external disable`
* `security key-manager onboard disable`

### Learn more
* [`DOC /security/key-managers`](#docs-security-security_key-managers)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    def restore(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Retrieves and restores any current unrestored keys (associated with the storage controller) from the specified key management server.
### Required properties
* `security_key_manager.uuid` - UUID of the key management server.
The UUID of the external key manager can be retrieved using [`GET /api/security/key-managers`].
### Related ONTAP commands
* `security key-manager external restore`
"""
        return super()._action(
            "restore", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    restore.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)
    def migrate(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Migrates the keys belonging to an SVM between the cluster's key manager and the SVM's key manager. This operation can run for several minutes.
### Required properties
* `source.uuid` - UUID of the source key manager.
* `uuid` - UUID of the destination key manager.
The UUID of onboard and external KMIP key manager can be fetched using [`GET /api/security/key-managers`].
The UUID of Azure Key Vault key manager can be fetched using [`GET /api/security/azure-key-vaults`].
The UUID of Google Cloud key manager can be fetched using [`GET /api/security/gcp-kms`].
The UUID of Amazon Web Services key manager can be fetched using [`GET /api/security/aws-kms`].
### Related ONTAP commands
* `security key-manager key migrate`
"""
        return super()._action(
            "migrate", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    migrate.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)

