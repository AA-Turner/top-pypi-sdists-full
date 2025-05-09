# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MapWidgetResponse(Model):
    """MapWidgetResponse.

    :param start_period: The start period for intensity data on places
    :type start_period: int
    :param end_period: The end period for intensity data on places
    :type end_period: int
    :param energy_use_intensity_unit:
    :type energy_use_intensity_unit: ~energycap.sdk.models.UnitChild
    :param energy_cost_intensity_unit:
    :type energy_cost_intensity_unit: ~energycap.sdk.models.UnitChild
    :param ghg_intensity_unit:
    :type ghg_intensity_unit: ~energycap.sdk.models.UnitChild
    :param floor_area_unit:
    :type floor_area_unit: ~energycap.sdk.models.UnitChild
    :param places: Place data to draw on the map
    :type places: list[~energycap.sdk.models.MapPlaceChild]
    """

    _attribute_map = {
        'start_period': {'key': 'startPeriod', 'type': 'int'},
        'end_period': {'key': 'endPeriod', 'type': 'int'},
        'energy_use_intensity_unit': {'key': 'energyUseIntensityUnit', 'type': 'UnitChild'},
        'energy_cost_intensity_unit': {'key': 'energyCostIntensityUnit', 'type': 'UnitChild'},
        'ghg_intensity_unit': {'key': 'ghgIntensityUnit', 'type': 'UnitChild'},
        'floor_area_unit': {'key': 'floorAreaUnit', 'type': 'UnitChild'},
        'places': {'key': 'places', 'type': '[MapPlaceChild]'},
    }

    def __init__(self, **kwargs):
        super(MapWidgetResponse, self).__init__(**kwargs)
        self.start_period = kwargs.get('start_period', None)
        self.end_period = kwargs.get('end_period', None)
        self.energy_use_intensity_unit = kwargs.get('energy_use_intensity_unit', None)
        self.energy_cost_intensity_unit = kwargs.get('energy_cost_intensity_unit', None)
        self.ghg_intensity_unit = kwargs.get('ghg_intensity_unit', None)
        self.floor_area_unit = kwargs.get('floor_area_unit', None)
        self.places = kwargs.get('places', None)
