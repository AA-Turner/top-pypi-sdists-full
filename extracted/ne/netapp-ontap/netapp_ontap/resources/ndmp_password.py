r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

Generates and retrieves the password for a given NDMP user in the SVM context.
### Examples
<br/>
```
GET "/api/protocols/ndmp/svms/ca8e29e0-e116-11ea-876c-0050568ea754/passwords/ndmpuser"
```
<br/>"""

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


__all__ = ["NdmpPassword", "NdmpPasswordSchema"]
__pdoc__ = {
    "NdmpPasswordSchema.resource": False,
    "NdmpPasswordSchema.opts": False,
}


class NdmpPasswordSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NdmpPassword object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ndmp_password."""

    password = marshmallow_fields.Str(
        data_key="password",
        allow_none=True,
    )
    r""" NDMP Password"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the ndmp_password."""

    user = marshmallow_fields.Str(
        data_key="user",
        allow_none=True,
    )
    r""" NDMP user"""

    @property
    def resource(self):
        return NdmpPassword

    gettable_fields = [
        "links",
        "password",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "user",
    ]
    """links,password,svm.links,svm.name,svm.uuid,user,"""

    patchable_fields = [
        "password",
        "svm.name",
        "svm.uuid",
        "user",
    ]
    """password,svm.name,svm.uuid,user,"""

    postable_fields = [
        "password",
        "svm.name",
        "svm.uuid",
        "user",
    ]
    """password,svm.name,svm.uuid,user,"""

class NdmpPassword(Resource):
    """Allows interaction with NdmpPassword objects on the host"""

    _schema = NdmpPasswordSchema
    _path = "/api/protocols/ndmp/svms/{svm[uuid]}/passwords"
    _keys = ["svm.uuid", "user"]






    def get(self, **kwargs) -> NetAppResponse:
        r"""Generates and retrieves the password for the specified NDMP user.
### Related ONTAP commands
* `vserver services ndmp generate-password`
### Learn more
* [`DOC /protocols/ndmp/svms/{svm.uuid}/passwords/{user}`](#docs-ndmp-protocols_ndmp_svms_{svm.uuid}_passwords_{user})
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





