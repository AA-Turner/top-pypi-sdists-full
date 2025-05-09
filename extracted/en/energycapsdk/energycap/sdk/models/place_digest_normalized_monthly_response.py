# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PlaceDigestNormalizedMonthlyResponse(Model):
    """PlaceDigestNormalizedMonthlyResponse.

    :param place_code: The place code
    :type place_code: str
    :param place_info: The place info
    :type place_info: str
    :param place_id: The place identifier
    :type place_id: int
    :param target_comparison:
    :type target_comparison:
     ~energycap.sdk.models.PlaceDigestNormalizedTargetComparisonMonthly
    :param updated: The date and time the data was updated
    :type updated: datetime
    :param global_use_unit:
    :type global_use_unit: ~energycap.sdk.models.UnitChild
    :param commodities: An array of monthly data per commodity
    :type commodities:
     list[~energycap.sdk.models.PlaceDigestNormalizedMonthlyResponseCommodityData]
    :param results: An array of monthly data
    :type results:
     list[~energycap.sdk.models.PlaceDigestNormalizedMonthlyResponseResults]
    """

    _attribute_map = {
        'place_code': {'key': 'placeCode', 'type': 'str'},
        'place_info': {'key': 'placeInfo', 'type': 'str'},
        'place_id': {'key': 'placeId', 'type': 'int'},
        'target_comparison': {'key': 'targetComparison', 'type': 'PlaceDigestNormalizedTargetComparisonMonthly'},
        'updated': {'key': 'updated', 'type': 'iso-8601'},
        'global_use_unit': {'key': 'globalUseUnit', 'type': 'UnitChild'},
        'commodities': {'key': 'commodities', 'type': '[PlaceDigestNormalizedMonthlyResponseCommodityData]'},
        'results': {'key': 'results', 'type': '[PlaceDigestNormalizedMonthlyResponseResults]'},
    }

    def __init__(self, **kwargs):
        super(PlaceDigestNormalizedMonthlyResponse, self).__init__(**kwargs)
        self.place_code = kwargs.get('place_code', None)
        self.place_info = kwargs.get('place_info', None)
        self.place_id = kwargs.get('place_id', None)
        self.target_comparison = kwargs.get('target_comparison', None)
        self.updated = kwargs.get('updated', None)
        self.global_use_unit = kwargs.get('global_use_unit', None)
        self.commodities = kwargs.get('commodities', None)
        self.results = kwargs.get('results', None)
