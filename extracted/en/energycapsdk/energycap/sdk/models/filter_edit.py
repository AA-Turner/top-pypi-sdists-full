# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class FilterEdit(Model):
    """FilterEdit.

    All required parameters must be populated in order to send to Azure.

    :param field_id: Required. Data field ID for the filter <span
     class='property-internal'>Required</span>
    :type field_id: int
    :param operator: Required. Filter operator expressed as a string (e.g.
     "equals") <span class='property-internal'>Required</span>
    :type operator: str
    :param value: Filter value
    :type value: str
    """

    _validation = {
        'field_id': {'required': True},
        'operator': {'required': True},
    }

    _attribute_map = {
        'field_id': {'key': 'fieldId', 'type': 'int'},
        'operator': {'key': 'operator', 'type': 'str'},
        'value': {'key': 'value', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(FilterEdit, self).__init__(**kwargs)
        self.field_id = kwargs.get('field_id', None)
        self.operator = kwargs.get('operator', None)
        self.value = kwargs.get('value', None)
