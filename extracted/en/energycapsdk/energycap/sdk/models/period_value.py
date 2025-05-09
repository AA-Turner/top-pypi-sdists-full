# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PeriodValue(Model):
    """General purpose period value DTO.

    :param period: The period
    :type period: int
    :param value: The value within the period
    :type value: float
    :param formatted_value: The formatted value within the period
    :type formatted_value: str
    """

    _attribute_map = {
        'period': {'key': 'period', 'type': 'int'},
        'value': {'key': 'value', 'type': 'float'},
        'formatted_value': {'key': 'formattedValue', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(PeriodValue, self).__init__(**kwargs)
        self.period = kwargs.get('period', None)
        self.value = kwargs.get('value', None)
        self.formatted_value = kwargs.get('formatted_value', None)
