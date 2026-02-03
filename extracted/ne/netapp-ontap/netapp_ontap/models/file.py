r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use the ONTAP DCN cluster software upload API to upload the DCN software image from the local system to the ONTAP cluster.
### Uploading a software package
The following example shows how to upload a DCN software package.
<br/>
```
# The API:
/api/dcn/cluster/software/upload
# The call:
curl -ku username:password -F "file=@auDev__aidp_dcn_image.tgz__2c9ca354-0ff6-4041-aa71-df76eadaba9e.tgz" -X POST "https://<mgmt-ip>/api/dcn/cluster/software/upload"
# The response:
HTTP/1.1 100 Continue
HTTP/1.1 200 OK
{
      "uuid": "f0ce5ac2-3347-4fa9-9335-ff8f2212bdad",
      "state": "processing",
      "create_time": "2025-07-09T13:27:09-04:00"
}
```
---"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["File", "FileSchema"]
__pdoc__ = {
    "FileSchema.resource": False,
    "FileSchema.opts": False,
    "File": False,
}

class FileSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the File object"""

    path = marshmallow_fields.Str(data_key="path", allow_none=True)
    r""" Path of the file or directory. """

    svm = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.svm", "SvmSchema"),
                unknown=EXCLUDE,
                data_key="svm",
                allow_none=True
            )
    r""" The svm field of the file. """

    volume = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.volume", "VolumeSchema"),
                unknown=EXCLUDE,
                data_key="volume",
                allow_none=True
            )
    r""" The volume field of the file. """

    @property
    def resource(self):
        return File

    gettable_fields = [
        "path",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """path,svm.links,svm.name,svm.uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "path",
        "svm.name",
        "svm.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """path,svm.name,svm.uuid,volume.name,volume.uuid,"""

    postable_fields = [
        "path",
        "svm.name",
        "svm.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """path,svm.name,svm.uuid,volume.name,volume.uuid,"""


class File(Resource):

    _schema = FileSchema
