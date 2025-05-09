# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AggregatedResponseGHGBuildingRank(Model):
    """AggregatedResponseGHGBuildingRank.

    :param period:
    :type period: ~energycap.sdk.models.PeriodRange
    :param total:
    :type total: ~energycap.sdk.models.GHGBuildingRank
    :param data_details: The data details
    :type data_details: list[~energycap.sdk.models.GHGBuildingRank]
    """

    _attribute_map = {
        'period': {'key': 'period', 'type': 'PeriodRange'},
        'total': {'key': 'total', 'type': 'GHGBuildingRank'},
        'data_details': {'key': 'dataDetails', 'type': '[GHGBuildingRank]'},
    }

    def __init__(self, *, period=None, total=None, data_details=None, **kwargs) -> None:
        super(AggregatedResponseGHGBuildingRank, self).__init__(**kwargs)
        self.period = period
        self.total = total
        self.data_details = data_details
