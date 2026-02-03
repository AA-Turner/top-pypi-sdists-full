r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineGovernancePoliciesClassifier", "DataEngineGovernancePoliciesClassifierSchema"]
__pdoc__ = {
    "DataEngineGovernancePoliciesClassifierSchema.resource": False,
    "DataEngineGovernancePoliciesClassifierSchema.opts": False,
    "DataEngineGovernancePoliciesClassifier": False,
}

class DataEngineGovernancePoliciesClassifierSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernancePoliciesClassifier object"""

    create_time = ImpreciseDateTime(data_key="create_time", allow_none=True)
    r""" The timestamp indicating when the classifier was created.

Example: 2018-06-04T19:00:00.000+0000 """

    custom = marshmallow_fields.Boolean(data_key="custom", allow_none=True)
    r""" Indicates if the classifier is custom or predefined.

Example: false """

    description = marshmallow_fields.Str(data_key="description", allow_none=True)
    r""" Description of the classifier.

Example: classifier for data subjects(i.e., person names) """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the classifier.

Example: data subjects classifier """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" State of the classifier. Possible values are:

* <i>enabled</i>: Classifier is enabled.
* <i>disabled</i>: Classifier is disabled.
* <i>simulate</i>: Classifier is in simulation mode.


Valid choices:

* enabled
* disabled
* simulate """

    tag = marshmallow_fields.Str(data_key="tag", allow_none=True)
    r""" Tag associated with the classifier.

Example: CLS_ENTD00000 """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Specifies the type of classifier. Possible values are:

* <i>data</i>: Classifier for data entities.
* <i>document</i>: Classifier for document entities.


Valid choices:

* data
* document """

    update_time = ImpreciseDateTime(data_key="update_time", allow_none=True)
    r""" The timestamp indicating when the classifier was last updated.

Example: 2018-06-04T19:00:00.000+0000 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Unique identifier of the classifier.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return DataEngineGovernancePoliciesClassifier

    gettable_fields = [
        "create_time",
        "custom",
        "description",
        "name",
        "state",
        "tag",
        "type",
        "update_time",
        "uuid",
    ]
    """create_time,custom,description,name,state,tag,type,update_time,uuid,"""

    patchable_fields = [
        "custom",
        "description",
        "name",
        "state",
        "tag",
        "type",
    ]
    """custom,description,name,state,tag,type,"""

    postable_fields = [
        "custom",
        "description",
        "name",
        "state",
        "tag",
        "type",
    ]
    """custom,description,name,state,tag,type,"""


class DataEngineGovernancePoliciesClassifier(Resource):

    _schema = DataEngineGovernancePoliciesClassifierSchema
