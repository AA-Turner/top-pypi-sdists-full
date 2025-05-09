# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class UDFSelectValueCreate(Model):
    """UDFSelectValueCreate.

    All required parameters must be populated in order to send to Azure.

    :param value: Required. The UDF select option's value <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 255 characters</span>
    :type value: str
    :param display_order: Required. The UDF select option's display order
     <span class='property-internal'>Required</span>
    :type display_order: int
    """

    _validation = {
        'value': {'required': True, 'max_length': 255, 'min_length': 0},
        'display_order': {'required': True},
    }

    _attribute_map = {
        'value': {'key': 'value', 'type': 'str'},
        'display_order': {'key': 'displayOrder', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(UDFSelectValueCreate, self).__init__(**kwargs)
        self.value = kwargs.get('value', None)
        self.display_order = kwargs.get('display_order', None)
