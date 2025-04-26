r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsEventActionParameters", "EmsEventActionParametersSchema"]
__pdoc__ = {
    "EmsEventActionParametersSchema.resource": False,
    "EmsEventActionParametersSchema.opts": False,
    "EmsEventActionParameters": False,
}


class EmsEventActionParametersSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsEventActionParameters object"""

    description = marshmallow_fields.Nested("netapp_ontap.models.ems_ui_message.EmsUiMessageSchema", unknown=EXCLUDE, data_key="description", allow_none=True)
    r""" Information to be displayed to the user. """

    enum = marshmallow_fields.List(marshmallow_fields.Str, data_key="enum", allow_none=True)
    r""" Specifies the possible values of the parameter.

Example: ["value-1","value-2"] """

    exclusive_maximum = marshmallow_fields.Boolean(data_key="exclusiveMaximum", allow_none=True)
    r""" Specifies whether the "maximum" value is excluded in the parameter value range. """

    exclusive_minimum = marshmallow_fields.Boolean(data_key="exclusiveMinimum", allow_none=True)
    r""" Specifies whether the "minimum" value is excluded in the parameter value range. """

    format = marshmallow_fields.Str(data_key="format", allow_none=True)
    r""" An optional modifier that serves as a hint at the content and format of the parameter.

Example: date-time """

    help = marshmallow_fields.Nested("netapp_ontap.models.ems_ui_message.EmsUiMessageSchema", unknown=EXCLUDE, data_key="help", allow_none=True)
    r""" Information to be displayed to the user. """

    in_ = marshmallow_fields.Str(data_key="in", allow_none=True)
    r""" Specifies where the parameter is placed when invoking the action.

Valid choices:

* body
* query """

    items = marshmallow_fields.Dict(data_key="items", allow_none=True)
    r""" If the type of the parameter is an array, this specifies the type of items in the form of a JSON object where other properties applicable to that type can be included.

Example: {"format":"date-time","type":"string"} """

    max_items = Size(data_key="maxItems", allow_none=True)
    r""" Specifies the maximum length of an array type parameter. """

    max_length = Size(data_key="maxLength", allow_none=True)
    r""" Specifies the maximum length of a string type parameter. """

    maximum = Size(data_key="maximum", allow_none=True)
    r""" Specifies the maximum value of the parameter. """

    min_items = Size(data_key="minItems", allow_none=True)
    r""" Specifies the minimum length of an array type parameter. """

    min_length = Size(data_key="minLength", allow_none=True)
    r""" Specifies the minimum length of a string type parameter. """

    minimum = Size(data_key="minimum", allow_none=True)
    r""" Specifies the minimum value of the parameter. """

    multiple_of = marshmallow_fields.Number(data_key="multipleOf", allow_none=True)
    r""" Specifies that a number type parameter must be the multiple of this number. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Parameter name.

Example: schedule-at """

    optional = marshmallow_fields.List(marshmallow_fields.Str, data_key="optional", allow_none=True)
    r""" By default, all properties of an object type parameter are mandatory. This property specifies the list of optional properties.

Example: ["end-time"] """

    pattern = marshmallow_fields.Str(data_key="pattern", allow_none=True)
    r""" Specifies a regular expression template for a string type parameter. """

    properties = marshmallow_fields.Dict(data_key="properties", allow_none=True)
    r""" If the type of the parameter is an object, this specifies what properties make up the object in the form of a JSON array where multiple parameters can be embedded within a single parameter. It is primarily used as a schema for an array type parameter.

Example: [{"format":"date-time","name":"start-date","type":"string"},{"format":"date-time","name":"end-date","type":"string"}] """

    title = marshmallow_fields.Nested("netapp_ontap.models.ems_ui_message.EmsUiMessageSchema", unknown=EXCLUDE, data_key="title", allow_none=True)
    r""" Information to be displayed to the user. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Parameter type.

Valid choices:

* string
* number
* integer
* boolean
* array
* object """

    unique_items = marshmallow_fields.Boolean(data_key="uniqueItems", allow_none=True)
    r""" Specifies whether the "maximum" value is excluded in the parameter value range. """

    validation_error_message = marshmallow_fields.Nested("netapp_ontap.models.ems_ui_message.EmsUiMessageSchema", unknown=EXCLUDE, data_key="validation_error_message", allow_none=True)
    r""" Information to be displayed to the user. """

    value = marshmallow_fields.Dict(data_key="value", allow_none=True)
    r""" Specifies the current value(s) for the parameter encoded in the appropriate JSON type. """

    @property
    def resource(self):
        return EmsEventActionParameters

    gettable_fields = [
        "description",
        "enum",
        "exclusive_maximum",
        "exclusive_minimum",
        "format",
        "help",
        "in_",
        "items",
        "max_items",
        "max_length",
        "maximum",
        "min_items",
        "min_length",
        "minimum",
        "multiple_of",
        "name",
        "optional",
        "pattern",
        "properties",
        "title",
        "type",
        "unique_items",
        "validation_error_message",
        "value",
    ]
    """description,enum,exclusive_maximum,exclusive_minimum,format,help,in_,items,max_items,max_length,maximum,min_items,min_length,minimum,multiple_of,name,optional,pattern,properties,title,type,unique_items,validation_error_message,value,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class EmsEventActionParameters(Resource):

    _schema = EmsEventActionParametersSchema
