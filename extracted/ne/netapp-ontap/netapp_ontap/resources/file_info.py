r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to read a file, write to a file, retrieve a list of files and directories, and retrieve or modify certain properties of files and directories. The path field is used to specify the path to the directory or file to be acted on. The path field requires using "%2E" to represent "." and "%2F" to represent "/" for the path provided.
## File data
Read and write data from/to a named file. To read a file, the Accept request HTTP header must be specified as multipart/form-data, and a value for the `length` query property, which represents the number of bytes to be read, must be specified. The API will fail if the length of data being read/written exceeds 1 MB. This API should only be used on normal files or streams associated with files. The results for other file types, such as LUNs is undefined.<br/>
To write to an existing file or create a new file, the user must specify Content-Type as “multipart/form-data”. The “application/json” Content-Type is supported for the files endpoint for file metadata operations. POST, PATCH and GET operations with “application/json” can be used to create a directory, modify metadata fields on a file, and get directory or file metadata information. POST and PATCH operations created with the Content-Type set to 'application/json' are not supported for use with the _data_ field.
The following APIs are used to read or write data to a file:

* GET     /api/storage/volumes/{volume.uuid}/files/{path}?byte_offset=0&length=40 -H "Accept: multipart/form-data"
* POST    /api/storage/volumes/{volume.uuid}/files/{path} -H "Content-Type: multipart/form-data" --form "file=the data to be written to the new file"
* PATCH   /api/storage/volumes/{volume.uuid}/files/{path}?byte_offset=10 -H "Content-Type: multipart/form-data" --form "file=the new data to be written or overwritten to the existing file starting at byte_offset"
## Listing directories and files
A list of files and directories and their properties can be retrieved for a specified path.<br/>
The following APIs are used to view a list of files and directories:

* GET       /api/storage/volumes/{volume.uuid}/files
* GET       /api/storage/volumes/{volume.uuid}/files/{path}
* GET       /api/storage/volumes/{volume.uuid}/files/{path}?fields=*
## File information
The metadata and detailed information about a single directory or file can be retrieved by setting the `return_metadata` query property to `true`. The information returned includes type, creation_time, modified_time, changed_time, accessed_time, unix_permissions, owner_id, group_id, size, hard_links_count, inode_number, is_empty, bytes_used, unique_bytes, inode_generation, is_vm_aligned, is_junction, links, and analytics (if requested).<br/>
The following API is used to view the properties of a single file or directory:

* GET       /api/storage/volumes/{volume.uuid}/files/{path}?return_metadata=true
## File usage
Custom details about the usage of a file can be retrieved by specifying a value for the `byte_offset` and `length` query properties.<br/>
The following API is used to view the unique bytes, and bytes used, by a file based on the range defined by `byte_offset` and `length`:

* GET       /api/storage/volumes/{volume.uuid}/files/{path}?return_metadata=true&byte_offset={int}&length={int}
## Create a directory
The following API is used to create a directory:

* POST    /api/storage/volumes/{volume.uuid}/files/{path} -d '{ "type" : "directory", "unix-permissions" : "644"}'
## Delete an entire directory
A directory can be deleted. The behavior of this call is equivalent to rm -rf.<br/>
The following API is used to delete an entire directory:

* DELETE    /api/storage/volumes/{volume.uuid}/files/{path}?recurse=true
## Delete a file or an empty directory
The following API is used to delete a file or an empty directory:

* DELETE    /api/storage/volumes/{volume.uuid}/files/{path}
* DELETE    /api/storage/volumes/{volume.uuid}/files/{path}?recurse=false
## File system analytics
File system analytics provide a quick method for obtaining information summarizing properties of all files within any directory tree of a volume. When file system analytics are enabled on a volume, `analytics.*` fields may be requested, and will be populated in the response records corresponding to directories. The API does not support file system analytics for requests that are made beyond the boundary of the specified `volume.uuid`.<br/>
The following APIs are used to obtain analytics information for a directory:

* GET    /api/storage/volumes/{volume.uuid}/files/{path}?fields=analytics
* GET    /api/storage/volumes/{volume.uuid}/files/{path}?fields=**
## QoS
QoS policies and settings enforce Service Level Objectives (SLO) on a file. A pre-created QoS policy can be used by specifying the `qos.name` or `qos.uuid` properties.</br>
The following APIs are used to assign a QoS policy to a file:

* PATCH   /api/storage/volumes/{volume.uuid}/files/{path} -d '{ "qos_policy.name" : "policy" }'
* PATCH   /api/storage/volumes/{volume.uuid}/files/{path} -d '{ "qos_policy.uuid" : "b89bc5dd-94a3-11e8-a7a3-0050568edf84" }'
## Symlinks
The following APIs are used to create a symlink and read the contents of a symlink:

* POST   /api/storage/volumes/{volume.uuid}/files/{path}  -d '{ "target" : "directory2/file1" }'
* GET    /api/storage/volumes/{volume.uuid}/files/{path}?return_metadata=true&fields=target
## Rename a file or a directory
The following API can be used to rename a file or a directory. Note that you need to provide the path relative to the root of the volume in the `path` body parameter.

* PATCH   /api/storage/volumes/{volume.uuid}/files/{path} -d '{ "path" : "directory1/directory2" }'
* PATCH   /api/storage/volumes/{volume.uuid}/files/{path} -d '{ "path" : "directory1/directory2/file1" }'
## Examples
### Writing to a new file
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection(
    "<mgmt-ip>",
    username="admin",
    password="password",
    verify=False,
    headers={"Accept": "multipart/form-data"},
):
    resource = FileInfo("54c06ce2-5430-11ea-90f9-005056a73aff", "aNewFile")
    resource.post(hydrate=True, data="the data to be written to the new file")
    print(resource)

```

### Writing to an existing file
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection(
    "<mgmt-ip>",
    username="admin",
    password="password",
    verify=False,
    headers={"Accept": "multipart/form-data"},
):
    resource = FileInfo("54c06ce2-5430-11ea-90f9-005056a73aff", "aNewFile")
    resource.patch(hydrate=True, data="*here is a little more data", byte_offset=39)

```

### Reading a file
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection(
    "<mgmt-ip>",
    username="admin",
    password="password",
    verify=False,
    headers={"Accept": "multipart/form-data"},
):
    resource = FileInfo("54c06ce2-5430-11ea-90f9-005056a73aff", "aNewFile")
    resource.get(byte_offset=0, length=100)
    print(resource)

```

###  Creating a directory
You can use the POST request to create a directory.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo("cb6b1b39-8d21-11e9-b926-05056aca658", "dir1")
    resource.type = "directory"
    resource.unix_permissions = "644"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
FileInfo({"path": "dir1", "unix_permissions": 644, "type": "directory"})

```
</div>
</div>

### Creating a stream on a file
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection(
    "<mgmt-ip>",
    username="admin",
    password="password",
    verify=False,
    headers={"Accept": "multipart/form-data"},
):
    resource = FileInfo("54c06ce2-5430-11ea-90f9-005056a73aff", "aNewFile")
    resource.post(
        hydrate=True,
        data="the data to be written to the new file",
        overwrite=True,
        byte_offset=-1,
        stream_name="someStream",
    )
    print(resource)

```

###  Retrieving the list of files in a directory
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo("cb6b1b39-8d21-11e9-b926-05056aca658", path="d1/d2/d3")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
[
    FileInfo(
        {
            "name": ".",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cb6b1b39-8d21-11e9-b926-005056aca658/files/d1%2Fd2%2Fd3%2F%2E"
                },
                "metadata": {
                    "href": "/api/storage/volumes/e8274d79-3bba-11ea-b780-005056a7d72a/files/d1%2Fd2%2Fd3%2F%2E?return_metadata=true"
                },
            },
            "path": "d1/d2/d3",
            "type": "directory",
        }
    ),
    FileInfo(
        {
            "name": "..",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cb6b1b39-8d21-11e9-b926-005056aca658/files/d1%2Fd2%2Fd3%2F%2E%2E"
                },
                "metadata": {
                    "href": "/api/storage/volumes/e8274d79-3bba-11ea-b780-005056a7d72a/files/d1%2Fd2%2Fd3%2F%2E%2E?return_metadata=true"
                },
            },
            "path": "d1/d2/d3",
            "type": "directory",
        }
    ),
    FileInfo(
        {
            "name": "f1",
            "_links": {
                "metadata": {
                    "href": "/api/storage/volumes/e8274d79-3bba-11ea-b780-005056a7d72a/files/d1%2Fd2%2Fd3%2File1?return_metadata=true"
                }
            },
            "path": "d1/d2/d3",
            "type": "file",
        }
    ),
    FileInfo(
        {
            "name": "d5",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cb6b1b39-8d21-11e9-b926-005056aca658/files/d1%2Fd2%2Fd3%2Fd5"
                },
                "metadata": {
                    "href": "/api/storage/volumes/e8274d79-3bba-11ea-b780-005056a7d72a/files/d1%2Fd2%2Fd3%2Fd5?return_metadata=true"
                },
            },
            "path": "d1/d2/d3",
            "type": "directory",
        }
    ),
]

```
</div>
</div>

###  Retrieving a list of files based on file type
You can filter the list of files you retrieve based on multiple file types by including a query parameter in the following format type="file|symlink"
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo("cb6b1b39-8d21-11e9-b926-05056aca658", path="d1/d2/d3")
    resource.get(type="file|directory")
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
[
    FileInfo(
        {
            "name": ".",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cb6b1b39-8d21-11e9-b926-005056aca658/files/d1%2Fd2%2Fd3%2F%2E"
                },
                "metadata": {
                    "href": "/api/storage/volumes/e8274d79-3bba-11ea-b780-005056a7d72a/files/d1%2Fd2%2Fd3%2F%2E?return_metadata=true"
                },
            },
            "path": "d1/d2/d3",
            "type": "directory",
        }
    ),
    FileInfo(
        {
            "name": "..",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cb6b1b39-8d21-11e9-b926-005056aca658/files/d1%2Fd2%2Fd3%2F%2E%2E"
                },
                "metadata": {
                    "href": "/api/storage/volumes/e8274d79-3bba-11ea-b780-005056a7d72a/files/d1%2Fd2%2Fd3%2F%2E%2E?return_metadata=true"
                },
            },
            "path": "d1/d2/d3",
            "type": "directory",
        }
    ),
    FileInfo(
        {
            "name": "f1",
            "_links": {
                "metadata": {
                    "href": "/api/storage/volumes/e8274d79-3bba-11ea-b780-005056a7d72a/files/d1%2Fd2%2Fd3%2File1?return_metadata=true"
                }
            },
            "path": "d1/d2/d3",
            "type": "file",
        }
    ),
    FileInfo(
        {
            "name": "d5",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cb6b1b39-8d21-11e9-b926-005056aca658/files/d1%2Fd2%2Fd3%2Fd5"
                },
                "metadata": {
                    "href": "/api/storage/volumes/e8274d79-3bba-11ea-b780-005056a7d72a/files/d1%2Fd2%2Fd3%2Fd5?return_metadata=true"
                },
            },
            "path": "d1/d2/d3",
            "type": "directory",
        }
    ),
]

```
</div>
</div>

###  Retrieving the properties of a directory or a file
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo("cb6b1b39-8d21-11e9-b926-05056aca658", path="d1/d2/d3/f1")
    resource.get(return_metadata=True)
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
[
    FileInfo(
        {
            "unique_bytes": 4096,
            "creation_time": "2019-06-12T21:27:28-04:00",
            "name": "",
            "bytes_used": 4096,
            "path": "d1/d2/d3/f1",
            "inode_generation": 214488325,
            "modified_time": "2019-06-12T21:27:28-04:00",
            "owner_id": 54738,
            "group_id": 30,
            "changed_time": "2019-06-12T21:27:28-04:00",
            "hard_links_count": 1,
            "inode_number": 1233,
            "unix_permissions": 644,
            "size": 200,
            "is_vm_aligned": False,
            "accessed_time": "2019-06-12T21:27:28-04:00",
            "type": "file",
            "is_junction": False,
        }
    )
]

```
</div>
</div>

###  Creating a symlink to a relative path
You can use the POST request to create a symlink.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo("cb6b1b39-8d21-11e9-b926-05056aca658", "symlink1")
    resource.target = "d1/f1"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
FileInfo({"path": "symlink1", "target": "d1/f1"})

```
</div>
</div>

###  Retrieving the target of a symlink
You can use the GET request to view the target of a symlink.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo("cb6b1b39-8d21-11e9-b926-05056aca658", "symlink1")
    resource.get(return_metadata=True, fields="target")
    print(resource)

```
<div class="try_it_out">
<input id="example9_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example9_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example9_result" class="try_it_out_content">
```
[FileInfo({"path": "symlink1", "target": "d1/f1"})]

```
</div>
</div>

###  Retrieving the usage information for a file
You can use the GET request to retrieve the unique bytes held in a file with or without specifying the offset.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo("cb6b1b39-8d21-11e9-b926-05056aca658", "f1")
    resource.get(return_metadata=True, byte_offset=100, length=200)
    print(resource)

```
<div class="try_it_out">
<input id="example10_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example10_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example10_result" class="try_it_out_content">
```
[
    FileInfo(
        {
            "unique_bytes": 4096,
            "creation_time": "2019-06-12T21:27:28-04:00",
            "bytes_used": 4096,
            "path": "d1/d2/d3/f1",
            "inode_generation": 214488325,
            "modified_time": "2019-06-12T21:27:28-04:00",
            "owner_id": 54738,
            "group_id": 30,
            "changed_time": "2019-06-12T21:27:28-04:00",
            "hard_links_count": 1,
            "inode_number": 1233,
            "unix_permissions": 644,
            "size": 200,
            "is_vm_aligned": False,
            "accessed_time": "2019-06-12T21:27:28-04:00",
            "type": "file",
            "is_junction": False,
        }
    )
]

```
</div>
</div>

###  Retrieving all information (including analytics) for a directory
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo("1ef5d1b2-f9d7-11e9-8043-00505682f860", "d1")
    resource.get(return_metadata=True, fields="**")
    print(resource)

```
<div class="try_it_out">
<input id="example11_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example11_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example11_result" class="try_it_out_content">
```
[
    FileInfo(
        {
            "creation_time": "2019-10-28T23:04:13+00:00",
            "bytes_used": 4096,
            "analytics": {
                "bytes_used": 209657856,
                "by_modified_time": {
                    "bytes_used": {
                        "values": [
                            0,
                            0,
                            0,
                            0,
                            3112960,
                            0,
                            14041088,
                            20545536,
                            0,
                            57933824,
                            61947904,
                            68804608,
                            188686336,
                            0,
                            0,
                            0,
                            20971520,
                            0,
                        ],
                        "labels": [
                            "2019-W42",
                            "2019-W41",
                            "2019-W40",
                            "2019-W39",
                            "2019-W38",
                            "2019-10",
                            "2019-09",
                            "2019-08",
                            "2019-Q4",
                            "2019-Q3",
                            "2019-Q2",
                            "2019-Q1",
                            "2019",
                            "2018",
                            "2017",
                            "2016",
                            "--2015",
                            "unknown",
                        ],
                        "percentages": [
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            1.48,
                            0.0,
                            6.7,
                            9.8,
                            0.0,
                            27.63,
                            29.55,
                            32.82,
                            90.0,
                            0.0,
                            0.0,
                            0.0,
                            10.0,
                            0.0,
                        ],
                    }
                },
                "file_count": 668,
                "subdir_count": 18,
                "by_accessed_time": {
                    "bytes_used": {
                        "values": [
                            102760448,
                            1867776,
                            1245184,
                            2179072,
                            1556480,
                            105873408,
                            9027584,
                            8093696,
                            105873408,
                            23969792,
                            32382976,
                            26460160,
                            188686336,
                            0,
                            0,
                            0,
                            20971520,
                            0,
                        ],
                        "labels": [
                            "2019-W42",
                            "2019-W41",
                            "2019-W40",
                            "2019-W39",
                            "2019-W38",
                            "2019-10",
                            "2019-09",
                            "2019-08",
                            "2019-Q4",
                            "2019-Q3",
                            "2019-Q2",
                            "2019-Q1",
                            "2019",
                            "2018",
                            "2017",
                            "2016",
                            "--2015",
                            "unknown",
                        ],
                        "percentages": [
                            49.01,
                            0.89,
                            0.59,
                            1.04,
                            0.74,
                            50.5,
                            4.31,
                            3.86,
                            50.5,
                            11.43,
                            15.45,
                            12.62,
                            90.0,
                            0.0,
                            0.0,
                            0.0,
                            10.0,
                            0.0,
                        ],
                    }
                },
            },
            "path": "d1",
            "inode_generation": 214514951,
            "modified_time": "2019-10-28T23:10:30+00:00",
            "owner_id": 1002,
            "group_id": 65533,
            "changed_time": "2019-10-28T23:10:30+00:00",
            "hard_links_count": 5,
            "inode_number": 96,
            "unix_permissions": 755,
            "size": 4096,
            "volume": {
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/1ef5d1b2-f9d7-11e9-8043-00505682f860"
                    }
                },
                "uuid": "1ef5d1b2-f9d7-11e9-8043-00505682f860",
            },
            "is_vm_aligned": False,
            "accessed_time": "2019-10-28T23:10:38+00:00",
            "is_empty": False,
            "type": "directory",
            "is_junction": False,
        }
    )
]

```
</div>
</div>

### Retrieving file system analytics information for a set of histogram buckets
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            FileInfo.get_collection(
                "cb6b1b39-8d21-11e9-b926-05056aca658",
                "d3",
                type="directory",
                fields="analytics",
                **{
                    "analytics.histogram_by_time_labels": "2019-Q3,2019-Q2,2019-Q1,2018-Q4"
                }
            )
        )
    )

```
<div class="try_it_out">
<input id="example12_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example12_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example12_result" class="try_it_out_content">
```
[
    FileInfo(
        {
            "name": ".",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cb6b1b39-8d21-11e9-b926-005056aca658/files/d3%2F%2E"
                },
                "metadata": {
                    "href": "/api/storage/volumes/cb6b1b39-8d21-11e9-b926-005056aca658/files/d3%2F%2E?return_metadata=true"
                },
            },
            "analytics": {
                "bytes_used": 244240384,
                "by_modified_time": {
                    "bytes_used": {
                        "values": [57344, 29720576, 196141056, 57344],
                        "percentages": [0.02, 12.17, 80.31, 0.02],
                    }
                },
                "file_count": 44,
                "subdir_count": 14,
                "by_accessed_time": {
                    "bytes_used": {
                        "values": [69632, 244170752, 0, 0],
                        "percentages": [0.03, 99.97, 0.0, 0.0],
                    }
                },
            },
            "path": "d3",
            "type": "directory",
        }
    ),
    FileInfo(
        {
            "name": "..",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cb6b1b39-8d21-11e9-b926-005056aca658/files/d3%2F%2E%2E"
                },
                "metadata": {
                    "href": "/api/storage/volumes/cb6b1b39-8d21-11e9-b926-005056aca658/files/d3%2F%2E%2E?return_metadata=true"
                },
            },
            "analytics": {
                "bytes_used": 3034574848,
                "by_modified_time": {
                    "bytes_used": {
                        "values": [61440, 1756479488, 214622208, 1191936],
                        "percentages": [0.0, 57.88, 7.07, 0.04],
                    }
                },
                "file_count": 515,
                "subdir_count": 23,
                "by_accessed_time": {
                    "bytes_used": {
                        "values": [282624, 3034292224, 0, 0],
                        "percentages": [0.01, 99.99, 0.0, 0.0],
                    }
                },
            },
            "path": "d3",
            "type": "directory",
        }
    ),
    FileInfo(
        {
            "name": "d5",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/cb6b1b39-8d21-11e9-b926-005056aca658/files/d3%2Fd5"
                },
                "metadata": {
                    "href": "/api/storage/volumes/cb6b1b39-8d21-11e9-b926-005056aca658/files/d3%2Fd5?return_metadata=true"
                },
            },
            "analytics": {
                "bytes_used": 47648768,
                "by_modified_time": {
                    "bytes_used": {
                        "values": [0, 29638656, 0, 0],
                        "percentages": [0.0, 62.2, 0.0, 0.0],
                    }
                },
                "file_count": 10,
                "subdir_count": 4,
                "by_accessed_time": {
                    "bytes_used": {
                        "values": [0, 47648768, 0, 0],
                        "percentages": [0.0, 100.0, 0.0, 0.0],
                    }
                },
            },
            "path": "d3",
            "type": "directory",
        }
    ),
]

```
</div>
</div>

### Identifying the largest subdirectories
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            FileInfo.get_collection(
                "1ef5d1b2-f9d7-11e9-8043-00505682f860",
                "d1",
                fields="analytics.bytes_used",
                type="directory",
                order_by="analytics.bytes_used desc",
            )
        )
    )

```
<div class="try_it_out">
<input id="example13_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example13_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example13_result" class="try_it_out_content">
```
[
    FileInfo(
        {
            "name": "..",
            "analytics": {"bytes_used": 56623104},
            "path": "d1",
            "type": "directory",
        }
    ),
    FileInfo(
        {
            "name": ".",
            "analytics": {"bytes_used": 35651584},
            "path": "d1",
            "type": "directory",
        }
    ),
    FileInfo(
        {
            "name": "biggest",
            "analytics": {"bytes_used": 17825792},
            "path": "d1",
            "type": "directory",
        }
    ),
    FileInfo(
        {
            "name": "bigger",
            "analytics": {"bytes_used": 10485760},
            "path": "d1",
            "type": "directory",
        }
    ),
    FileInfo(
        {
            "name": "big",
            "analytics": {"bytes_used": 5242880},
            "path": "d1",
            "type": "directory",
        }
    ),
]

```
</div>
</div>

###  Assigning a QoS policy to a file
You can use the PATCH request to assign a QoS policy to a file.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo("cb6b1b39-8d21-11e9-b926-05056aca658", path="directory1/file1")
    resource.qos_policy = {"name": "policy"}
    resource.patch()

```

###  Retrieving QoS information for a file
You can use the GET request for all fields with return_metadata="true" to retrieve QoS information for the file.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo("cb6b1b39-8d21-11e9-b926-05056aca658", "file")
    resource.get(return_metadata=True, fields="**")
    print(resource)

```
<div class="try_it_out">
<input id="example15_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example15_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example15_result" class="try_it_out_content">
```
[
    FileInfo(
        {
            "creation_time": "2020-03-17T10:58:40-04:00",
            "bytes_used": 1056768,
            "path": "file",
            "inode_generation": 219748425,
            "modified_time": "2020-03-24T18:15:40-04:00",
            "owner_id": 0,
            "is_snapshot": False,
            "group_id": 0,
            "changed_time": "2020-03-24T18:15:40-04:00",
            "hard_links_count": 2,
            "qos_policy": {
                "name": "pg1",
                "uuid": "00725264-688f-11ea-8f10-005056a7b8ac",
            },
            "inode_number": 96,
            "unix_permissions": 644,
            "size": 1048576,
            "volume": {"uuid": "c05eb66a-685f-11ea-8508-005056a7b8ac"},
            "is_vm_aligned": False,
            "accessed_time": "2020-03-24T18:15:40-04:00",
            "type": "lun",
            "is_junction": False,
        }
    )
]

```
</div>
</div>

###  Deleting an entire directory
You can use the DELETE request to remove an entire directory recursively.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo(
        "cb6b1b39-8d21-11e9-b926-05056aca658", path="directory1/directory2"
    )
    resource.delete(recurse=True)

```

###  Deleting an entire directory with specified throttling threshold
You can specify the maximum number of directory delete operations per second when removing an entire directory recursively.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo(
        "cb6b1b39-8d21-11e9-b926-05056aca658", path="directory1/directory2"
    )
    resource.delete(recurse=True, throttle_deletion=100)

```

###  Deleting an empty directory
You can use the DELETE request to remove an empty directory.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo(
        "cb6b1b39-8d21-11e9-b926-05056aca658", path="directory1/directory2"
    )
    resource.delete()

```

###  Deleting a file
You can use the DELETE request to remove a file.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo("cb6b1b39-8d21-11e9-b926-05056aca658", path="directory1/file2")
    resource.delete()

```

###  Renaming a file
You can use the PATCH request to rename a file.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo(
        "cb6b1b39-8d21-11e9-b926-05056aca658", path="directory1/directory2/file1"
    )
    resource.path = "directory1/file2"
    resource.patch()

```

###  File truncating
You can use the PATCH request to change the size of a file.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo("cb6b1b39-8d21-11e9-b926-05056aca658", "abc.txt")
    resource.size = 100
    resource.patch()

```

###  Renaming a directory
You can use the PATCH request to rename a directory.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FileInfo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FileInfo(
        "cb6b1b39-8d21-11e9-b926-05056aca658", path="directory1/directory2"
    )
    resource.path = "d3/d4"
    resource.patch()

```
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


__all__ = ["FileInfo", "FileInfoSchema"]
__pdoc__ = {
    "FileInfoSchema.resource": False,
    "FileInfoSchema.opts": False,
}


class FileInfoSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FileInfo object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.file_info_links.FileInfoLinksSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the file_info."""

    accessed_time = ImpreciseDateTime(
        data_key="accessed_time",
        allow_none=True,
    )
    r""" Last access time of the file in date-time format.

Example: 2019-06-12T15:00:16.000+0000"""

    analytics = marshmallow_fields.Nested("netapp_ontap.models.analytics_info.AnalyticsInfoSchema", data_key="analytics", unknown=EXCLUDE, allow_none=True)
    r""" File system analytics information summarizing all descendants of a specific directory."""

    bytes_used = Size(
        data_key="bytes_used",
        allow_none=True,
    )
    r""" The actual number of bytes used on disk by this file. If byte_offset and length parameters are specified, this will return the bytes used by the file within the given range.

Example: 4096"""

    changed_time = ImpreciseDateTime(
        data_key="changed_time",
        allow_none=True,
    )
    r""" Last time data or attributes changed on the file in date-time format.

Example: 2019-06-12T15:00:16.000+0000"""

    constituent = marshmallow_fields.Nested("netapp_ontap.models.file_info_constituent.FileInfoConstituentSchema", data_key="constituent", unknown=EXCLUDE, allow_none=True)
    r""" The constituent field of the file_info."""

    creation_time = ImpreciseDateTime(
        data_key="creation_time",
        allow_none=True,
    )
    r""" Creation time of the file in date-time format.

Example: 2019-06-12T15:00:16.000+0000"""

    fill_enabled = marshmallow_fields.Boolean(
        data_key="fill_enabled",
        allow_none=True,
    )
    r""" Returns "true" if the space reservation is enabled. The field overwrite_enabled must also be set to the same value as this field."""

    group_id = Size(
        data_key="group_id",
        allow_none=True,
    )
    r""" The integer ID of the group of the file owner.

Example: 30"""

    hard_links_count = Size(
        data_key="hard_links_count",
        allow_none=True,
    )
    r""" The number of hard links to the file.

Example: 1"""

    inode_generation = Size(
        data_key="inode_generation",
        allow_none=True,
    )
    r""" Inode generation number.

Example: 214753547"""

    inode_number = Size(
        data_key="inode_number",
        allow_none=True,
    )
    r""" The file inode number.

Example: 1695"""

    is_empty = marshmallow_fields.Boolean(
        data_key="is_empty",
        allow_none=True,
    )
    r""" Specifies whether or not a directory is empty. A directory is considered empty if it only contains entries for "." and "..". This element is present if the file is a directory. In some special error cases, such as when the volume goes offline or when the directory is moved while retrieving this info, this field might not get set."""

    is_junction = marshmallow_fields.Boolean(
        data_key="is_junction",
        allow_none=True,
    )
    r""" Returns "true" if the directory is a junction.

Example: false"""

    is_snapshot = marshmallow_fields.Boolean(
        data_key="is_snapshot",
        allow_none=True,
    )
    r""" Returns "true" if the directory is a snapshot.

Example: false"""

    is_vm_aligned = marshmallow_fields.Boolean(
        data_key="is_vm_aligned",
        allow_none=True,
    )
    r""" Returns true if the file is vm-aligned. A vm-aligned file is a file that is initially padded with zero-filled data so that its actual data starts at an offset other than zero. The amount by which the start offset is adjusted depends on the vm-align setting of the hosting volume.

Example: false"""

    modified_time = ImpreciseDateTime(
        data_key="modified_time",
        allow_none=True,
    )
    r""" Last data modification time of the file in date-time format.

Example: 2019-06-12T15:00:16.000+0000"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the file."""

    overwrite_enabled = marshmallow_fields.Boolean(
        data_key="overwrite_enabled",
        allow_none=True,
    )
    r""" Returns "true" if the space reservation for overwrites is enabled. The field fill_enabled must also be set to the same value as this field."""

    owner_id = Size(
        data_key="owner_id",
        allow_none=True,
    )
    r""" The integer ID of the file owner.

Example: 54738"""

    path = marshmallow_fields.Str(
        data_key="path",
        allow_none=True,
    )
    r""" Path of the file."""

    qos_policy = marshmallow_fields.Nested("netapp_ontap.models.file_info_qos_policy.FileInfoQosPolicySchema", data_key="qos_policy", unknown=EXCLUDE, allow_none=True)
    r""" The QoS policy for the file. Both traditional and adaptive QoS policies are supported. If both `qos_policy.uuid` and `qos_policy.name` properties are specified in the same request, they must refer to the same QoS policy. To remove the file from a QoS policy, set the property `qos_policy.name` in a PATCH request to an empty string "" or "none". Note: Files which are in use as a LUN cannot be assigned to a QoS policy, instead use PATCH on /storage/luns to assign a QoS policy for such files. <br/>
Note that a QoS policy can be set on a file, or a file's volume, but not on both."""

    size = Size(
        data_key="size",
        allow_none=True,
    )
    r""" The size of the file, in bytes."""

    target = marshmallow_fields.Str(
        data_key="target",
        allow_none=True,
    )
    r""" The relative or absolute path contained in a symlink, in the form <some>/<path>."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['file', 'directory', 'blockdev', 'chardev', 'symlink', 'socket', 'fifo', 'stream', 'lun']),
        allow_none=True,
    )
    r""" Type of the file.

Valid choices:

* file
* directory
* blockdev
* chardev
* symlink
* socket
* fifo
* stream
* lun"""

    unique_bytes = Size(
        data_key="unique_bytes",
        allow_none=True,
    )
    r""" Number of bytes uniquely held by this file. If byte_offset and length parameters are specified, this will return bytes uniquely held by the file within the given range.

Example: 4096"""

    unix_permissions = Size(
        data_key="unix_permissions",
        allow_none=True,
    )
    r""" UNIX permissions to be viewed as an octal number. It consists of 4 digits derived by adding up bits 4 (read), 2 (write), and 1 (execute). The first digit selects the set user ID(4), set group ID (2), and sticky (1) attributes. The second digit selects permissions for the owner of the file; the third selects permissions for other users in the same group; the fourth selects permissions for other users not in the group."""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the file_info."""

    @property
    def resource(self):
        return FileInfo

    gettable_fields = [
        "links",
        "accessed_time",
        "analytics",
        "bytes_used",
        "changed_time",
        "constituent",
        "creation_time",
        "fill_enabled",
        "group_id",
        "hard_links_count",
        "inode_generation",
        "inode_number",
        "is_empty",
        "is_junction",
        "is_snapshot",
        "is_vm_aligned",
        "modified_time",
        "name",
        "overwrite_enabled",
        "owner_id",
        "path",
        "qos_policy",
        "size",
        "target",
        "type",
        "unique_bytes",
        "unix_permissions",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,accessed_time,analytics,bytes_used,changed_time,constituent,creation_time,fill_enabled,group_id,hard_links_count,inode_generation,inode_number,is_empty,is_junction,is_snapshot,is_vm_aligned,modified_time,name,overwrite_enabled,owner_id,path,qos_policy,size,target,type,unique_bytes,unix_permissions,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "constituent",
        "fill_enabled",
        "is_empty",
        "name",
        "overwrite_enabled",
        "path",
        "qos_policy",
        "size",
        "target",
        "unix_permissions",
    ]
    """constituent,fill_enabled,is_empty,name,overwrite_enabled,path,qos_policy,size,target,unix_permissions,"""

    postable_fields = [
        "constituent",
        "is_empty",
        "name",
        "path",
        "target",
        "type",
        "unix_permissions",
    ]
    """constituent,is_empty,name,path,target,type,unix_permissions,"""

class FileInfo(Resource):
    r""" Information about a single file. """

    _schema = FileInfoSchema
    _path = "/api/storage/volumes/{volume[uuid]}/files"
    _keys = ["volume.uuid", "path"]
    _post_form_data_parameters = { 'data':'string', }
    _patch_form_data_parameters = { 'data':'string', }

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of files and directories for a given directory or returns only the properties of a single given directory or file of a volume.
### Expensive properties
There is an added computational cost to retrieving values for these properties.  They are not included by default in GET results and must be explicitly requested using the `fields` query property. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
  * `analytics`
  * `qos_policy.name`
  * `qos_policy.uuid`

### Learn more
* [`DOC /storage/volumes/{volume.uuid}/files/{path}`](#docs-storage-storage_volumes_{volume.uuid}_files_{path})"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all FileInfo resources that match the provided query"""
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
        """Returns a list of RawResources that represent FileInfo resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["FileInfo"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Writes to an existing file with the supplied data or modifies the size, name, space reservation information, QoS policy, or hole range information of a file. Query-based PATCH operations are not supported.
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/files/{path}`](#docs-storage-storage_volumes_{volume.uuid}_files_{path})"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["FileInfo"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["FileInfo"], NetAppResponse]:
        r"""Creates a new file with the supplied data, a new directory or a new symlink.
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/files/{path}`](#docs-storage-storage_volumes_{volume.uuid}_files_{path})"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["FileInfo"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an existing file or directory. Query-based DELETE operations are not supported.
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/files/{path}`](#docs-storage-storage_volumes_{volume.uuid}_files_{path})"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of files and directories for a given directory or returns only the properties of a single given directory or file of a volume.
### Expensive properties
There is an added computational cost to retrieving values for these properties.  They are not included by default in GET results and must be explicitly requested using the `fields` query property. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
  * `analytics`
  * `qos_policy.name`
  * `qos_policy.uuid`

### Learn more
* [`DOC /storage/volumes/{volume.uuid}/files/{path}`](#docs-storage-storage_volumes_{volume.uuid}_files_{path})"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a list of files and directories for a given directory or returns only the properties of a single given directory or file of a volume.
### Expensive properties
There is an added computational cost to retrieving values for these properties.  They are not included by default in GET results and must be explicitly requested using the `fields` query property. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
  * `analytics`
  * `qos_policy.name`
  * `qos_policy.uuid`

### Learn more
* [`DOC /storage/volumes/{volume.uuid}/files/{path}`](#docs-storage-storage_volumes_{volume.uuid}_files_{path})"""
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
        r"""Creates a new file with the supplied data, a new directory or a new symlink.
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/files/{path}`](#docs-storage-storage_volumes_{volume.uuid}_files_{path})"""
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
        r"""Writes to an existing file with the supplied data or modifies the size, name, space reservation information, QoS policy, or hole range information of a file. Query-based PATCH operations are not supported.
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/files/{path}`](#docs-storage-storage_volumes_{volume.uuid}_files_{path})"""
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
        r"""Deletes an existing file or directory. Query-based DELETE operations are not supported.
### Learn more
* [`DOC /storage/volumes/{volume.uuid}/files/{path}`](#docs-storage-storage_volumes_{volume.uuid}_files_{path})"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


