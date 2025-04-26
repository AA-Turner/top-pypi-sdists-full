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


__all__ = ["SplitStatus", "SplitStatusSchema"]
__pdoc__ = {
    "SplitStatusSchema.resource": False,
    "SplitStatusSchema.opts": False,
}


class SplitStatusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SplitStatus object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the split_status."""

    pending_splits = Size(
        data_key="pending_splits",
        allow_none=True,
    )
    r""" Specifies the number of pending file clone split operations in the volume."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the split_status."""

    unsplit_size = Size(
        data_key="unsplit_size",
        allow_none=True,
    )
    r""" Specifies the space occupied by unsplit file clones in the volume."""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the split_status."""

    @property
    def resource(self):
        return SplitStatus

    gettable_fields = [
        "links",
        "pending_splits",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "unsplit_size",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,pending_splits,svm.links,svm.name,svm.uuid,unsplit_size,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class SplitStatus(Resource):
    """Allows interaction with SplitStatus objects on the host"""

    _schema = SplitStatusSchema
    _path = "/api/storage/file/clone/split-status"
    _keys = ["volume.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves file clone split status of all volumes in the node.
### Learn More
* [`DOC /storage/file/clone`]
```
# The API:
/api/storage/file/clone/split-status
# The call:
curl -X GET "https://<mgmt_ip>/api/storage/file/clone/split-status" -H "accept: application/hal+json"
# The response:
{
  "records": [
    {
      "volume": {
        "uuid": "ac559964-57a3-40cf-b5cb-f3cb99151a7d",
        "name": "vol1",
        "_links": {
          "self": {
            "href": "/api/storage/volumes/ac559964-57a3-40cf-b5cb-f3cb99151a7d"
          }
        }
      },
      "svm": {
        "uuid": "9fcb44bf-4305-11e8-b8d5-00a09887594b",
        "name": "vs1"
        "_links": {
          "self": {
            "href": "/api/svm/svms/9fcb44bf-4305-11e8-b8d5-00a09887594b"
          }
        }
      },
      "pending_splits": 0,
      "unsplit_size": 0,
      "_links": {
        "self": {
          "href": "/api/storage/file/clone/split-status/ac559964-57a3-40cf-b5cb-f3cb99151a7d"
        }
      }
    },
    {
      "volume": {
        "uuid": "32d95d48-d8b7-11eb-a41d-005056bb3837",
        "name": "vs1_root",
        "_links": {
          "self": {
            "href": "/api/storage/volumes/32d95d48-d8b7-11eb-a41d-005056bb3837"
          }
        }
      },
      "svm": {
        "name": "vs1"
        "_links": {
          "self": {
            "href": "/api/svm/svms/9fcb44bf-4305-11e8-b8d5-00a09887594b"
          }
        }
      },
      "pending_splits": 0,
      "unsplit_size": 0,
      "_links": {
        "self": {
          "href": "/api/storage/file/clone/split-status/32d95d48-d8b7-11eb-a41d-005056bb3837"
        }
      }
    }
  ],
  "num_records": 2,
  "_links": {
    "self": {
      "href": "/api/storage/file/clone/split-status"
    }
  }
}
```
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
        """Returns a count of all SplitStatus resources that match the provided query"""
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
        """Returns a list of RawResources that represent SplitStatus resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves file clone split status of all volumes in the node.
### Learn More
* [`DOC /storage/file/clone`]
```
# The API:
/api/storage/file/clone/split-status
# The call:
curl -X GET "https://<mgmt_ip>/api/storage/file/clone/split-status" -H "accept: application/hal+json"
# The response:
{
  "records": [
    {
      "volume": {
        "uuid": "ac559964-57a3-40cf-b5cb-f3cb99151a7d",
        "name": "vol1",
        "_links": {
          "self": {
            "href": "/api/storage/volumes/ac559964-57a3-40cf-b5cb-f3cb99151a7d"
          }
        }
      },
      "svm": {
        "uuid": "9fcb44bf-4305-11e8-b8d5-00a09887594b",
        "name": "vs1"
        "_links": {
          "self": {
            "href": "/api/svm/svms/9fcb44bf-4305-11e8-b8d5-00a09887594b"
          }
        }
      },
      "pending_splits": 0,
      "unsplit_size": 0,
      "_links": {
        "self": {
          "href": "/api/storage/file/clone/split-status/ac559964-57a3-40cf-b5cb-f3cb99151a7d"
        }
      }
    },
    {
      "volume": {
        "uuid": "32d95d48-d8b7-11eb-a41d-005056bb3837",
        "name": "vs1_root",
        "_links": {
          "self": {
            "href": "/api/storage/volumes/32d95d48-d8b7-11eb-a41d-005056bb3837"
          }
        }
      },
      "svm": {
        "name": "vs1"
        "_links": {
          "self": {
            "href": "/api/svm/svms/9fcb44bf-4305-11e8-b8d5-00a09887594b"
          }
        }
      },
      "pending_splits": 0,
      "unsplit_size": 0,
      "_links": {
        "self": {
          "href": "/api/storage/file/clone/split-status/32d95d48-d8b7-11eb-a41d-005056bb3837"
        }
      }
    }
  ],
  "num_records": 2,
  "_links": {
    "self": {
      "href": "/api/storage/file/clone/split-status"
    }
  }
}
```
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves file clone split status of all volumes in the node.
### Related Ontap commands
* `volume file clone split status`
### Learn More
* [`DOC /storage/file/clone`]
### Retrieves the information of split status.
The GET operation retrieves information about split processes in the volume.
`pending-clone-splits` is the number of files for which file clone split is not yet completed.
`unsplit-size` is the sum of all sizes in the volume that is not split, in bytes.
```
# The API:
/api/storage/file/clone/split-status/{volume.uuid}
# The call:
curl -X GET "https://<mgmt_ip>/api/storage/file/clone/split-status/ac559964-57a3-40cf-b5cb-f3cb99151a7d" -H "accept: application/hal+json"
# The response:
{
  "volume": {
    "uuid": "ac559964-57a3-40cf-b5cb-f3cb99151a7d",
    "name": "vol1",
    "_links": {
      "self": {
        "href": "/api/storage/volumes/ac559964-57a3-40cf-b5cb-f3cb99151a7d"
      }
    }
  },
  "svm": {
    "name": "vs1"
  },
  "pending_splits": 0,
  "unsplit_size": 0,
  "_links": {
    "self": {
      "href": "/api/storage/file/clone/split-status/ac559964-57a3-40cf-b5cb-f3cb99151a7d"
    }
  }
}
```
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





