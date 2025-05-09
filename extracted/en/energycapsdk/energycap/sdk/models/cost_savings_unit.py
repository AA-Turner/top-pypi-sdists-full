# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CostSavingsUnit(Model):
    """CostSavingsUnit.

    :param cost_savings_unit_id: The cost savings unit identifier
    :type cost_savings_unit_id: int
    :param cost_savings_unit_code: The cost savings unit code
    :type cost_savings_unit_code: str
    :param cost_savings_unit_info: The cost savings unit information
    :type cost_savings_unit_info: str
    """

    _attribute_map = {
        'cost_savings_unit_id': {'key': 'costSavingsUnitId', 'type': 'int'},
        'cost_savings_unit_code': {'key': 'costSavingsUnitCode', 'type': 'str'},
        'cost_savings_unit_info': {'key': 'costSavingsUnitInfo', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(CostSavingsUnit, self).__init__(**kwargs)
        self.cost_savings_unit_id = kwargs.get('cost_savings_unit_id', None)
        self.cost_savings_unit_code = kwargs.get('cost_savings_unit_code', None)
        self.cost_savings_unit_info = kwargs.get('cost_savings_unit_info', None)
