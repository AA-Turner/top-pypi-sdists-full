# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class RollingComparisonResponse(Model):
    """RollingComparisonResponse.

    :param data_displayed: Indicates the type of the data displayed. Eg:
     Actual, Calendarized or Normalized.
    :type data_displayed: str
    :param unit: The values unit
    :type unit: str
    :param period_range:
    :type period_range: ~energycap.sdk.models.PeriodRange
    :param data_details: The data details
    :type data_details: list[~energycap.sdk.models.RollingComparisonDetail]
    """

    _attribute_map = {
        'data_displayed': {'key': 'dataDisplayed', 'type': 'str'},
        'unit': {'key': 'unit', 'type': 'str'},
        'period_range': {'key': 'periodRange', 'type': 'PeriodRange'},
        'data_details': {'key': 'dataDetails', 'type': '[RollingComparisonDetail]'},
    }

    def __init__(self, **kwargs):
        super(RollingComparisonResponse, self).__init__(**kwargs)
        self.data_displayed = kwargs.get('data_displayed', None)
        self.unit = kwargs.get('unit', None)
        self.period_range = kwargs.get('period_range', None)
        self.data_details = kwargs.get('data_details', None)
