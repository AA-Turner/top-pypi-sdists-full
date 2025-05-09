# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CalculatedBillDemandRequest(Model):
    """CalculatedBillDemandRequest.

    :param readings_channel_id: Use channel data readings to calculate bill
     demand <span class='property-internal'>Required (defined)</span>
    :type readings_channel_id: int
    :param fixed_demand:
    :type fixed_demand: ~energycap.sdk.models.FixedDemandRequest
    :param use_wattics_data_point: Use SmartAnalytics (Wattics) data readings
     to calculate bill demand <span class='property-internal'>Required
     (defined)</span>
    :type use_wattics_data_point: bool
    """

    _attribute_map = {
        'readings_channel_id': {'key': 'readingsChannelId', 'type': 'int'},
        'fixed_demand': {'key': 'fixedDemand', 'type': 'FixedDemandRequest'},
        'use_wattics_data_point': {'key': 'useWatticsDataPoint', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(CalculatedBillDemandRequest, self).__init__(**kwargs)
        self.readings_channel_id = kwargs.get('readings_channel_id', None)
        self.fixed_demand = kwargs.get('fixed_demand', None)
        self.use_wattics_data_point = kwargs.get('use_wattics_data_point', None)
