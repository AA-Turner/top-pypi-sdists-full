# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class UDFSelectValueEntityResponse(Model):
    """UDFSelectValueEntityResponse.

    :param udf_select_value_id:  <span class='property-internal'>Required
     (defined)</span>
    :type udf_select_value_id: int
    :param value:  <span class='property-internal'>Required (defined)</span>
    :type value: str
    :param display_order:  <span class='property-internal'>Required
     (defined)</span>
    :type display_order: int
    """

    _attribute_map = {
        'udf_select_value_id': {'key': 'udfSelectValueId', 'type': 'int'},
        'value': {'key': 'value', 'type': 'str'},
        'display_order': {'key': 'displayOrder', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(UDFSelectValueEntityResponse, self).__init__(**kwargs)
        self.udf_select_value_id = kwargs.get('udf_select_value_id', None)
        self.value = kwargs.get('value', None)
        self.display_order = kwargs.get('display_order', None)
