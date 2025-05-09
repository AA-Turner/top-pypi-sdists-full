# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ReportingSettingResponse(Model):
    """ReportingSettingResponse.

    :param energy_unit:
    :type energy_unit: ~energycap.sdk.models.UnitChild
    :param cost_unit:
    :type cost_unit: ~energycap.sdk.models.UnitChild
    :param floor_area_unit:
    :type floor_area_unit: ~energycap.sdk.models.UnitChild
    :param months_to_exclude_from_charts: Months to exclude from charts,
     including the current month.
     Ex. If the current month is October,
     A value of 0 will not exclude any months,
     A value of 1 will exclude the month of October,
     A value of 2 will exclude October and September,
     A value of 3 will exclude October, September, and August,
     A value of 13 will exclude October and the last full year of data.
    :type months_to_exclude_from_charts: int
    """

    _attribute_map = {
        'energy_unit': {'key': 'energyUnit', 'type': 'UnitChild'},
        'cost_unit': {'key': 'costUnit', 'type': 'UnitChild'},
        'floor_area_unit': {'key': 'floorAreaUnit', 'type': 'UnitChild'},
        'months_to_exclude_from_charts': {'key': 'monthsToExcludeFromCharts', 'type': 'int'},
    }

    def __init__(self, *, energy_unit=None, cost_unit=None, floor_area_unit=None, months_to_exclude_from_charts: int=None, **kwargs) -> None:
        super(ReportingSettingResponse, self).__init__(**kwargs)
        self.energy_unit = energy_unit
        self.cost_unit = cost_unit
        self.floor_area_unit = floor_area_unit
        self.months_to_exclude_from_charts = months_to_exclude_from_charts
