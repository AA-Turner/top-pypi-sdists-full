# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AdjustedCostTypeResponse(Model):
    """AdjustedCostTypeResponse.

    :param adjusted_cost_type_id: Adjusted Cost Type identifier
    :type adjusted_cost_type_id: int
    :param adjusted_cost_type_code: Adjusted Cost Type code
    :type adjusted_cost_type_code: str
    :param adjusted_cost_type_info: Adjusted Cost Type name
    :type adjusted_cost_type_info: str
    """

    _attribute_map = {
        'adjusted_cost_type_id': {'key': 'adjustedCostTypeId', 'type': 'int'},
        'adjusted_cost_type_code': {'key': 'adjustedCostTypeCode', 'type': 'str'},
        'adjusted_cost_type_info': {'key': 'adjustedCostTypeInfo', 'type': 'str'},
    }

    def __init__(self, *, adjusted_cost_type_id: int=None, adjusted_cost_type_code: str=None, adjusted_cost_type_info: str=None, **kwargs) -> None:
        super(AdjustedCostTypeResponse, self).__init__(**kwargs)
        self.adjusted_cost_type_id = adjusted_cost_type_id
        self.adjusted_cost_type_code = adjusted_cost_type_code
        self.adjusted_cost_type_info = adjusted_cost_type_info
