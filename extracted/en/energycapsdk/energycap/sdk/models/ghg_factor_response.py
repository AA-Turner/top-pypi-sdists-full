# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GHGFactorResponse(Model):
    """GHGFactorResponse.

    :param factor_id: The factor identifier
    :type factor_id: int
    :param factor_code: The factor code
    :type factor_code: str
    :param factor_info: The factor info
    :type factor_info: str
    :param factor_description: The factor description
    :type factor_description: str
    :param source_organization: The source organization
    :type source_organization: str
    :param model: The model
    :type model: str
    :param factor_category:
    :type factor_category: ~energycap.sdk.models.GHGFactorCategory
    :param from_unit:
    :type from_unit: ~energycap.sdk.models.UnitChild
    :param factor_region:
    :type factor_region: ~energycap.sdk.models.GHGFactorRegion
    """

    _attribute_map = {
        'factor_id': {'key': 'factorId', 'type': 'int'},
        'factor_code': {'key': 'factorCode', 'type': 'str'},
        'factor_info': {'key': 'factorInfo', 'type': 'str'},
        'factor_description': {'key': 'factorDescription', 'type': 'str'},
        'source_organization': {'key': 'sourceOrganization', 'type': 'str'},
        'model': {'key': 'model', 'type': 'str'},
        'factor_category': {'key': 'factorCategory', 'type': 'GHGFactorCategory'},
        'from_unit': {'key': 'fromUnit', 'type': 'UnitChild'},
        'factor_region': {'key': 'factorRegion', 'type': 'GHGFactorRegion'},
    }

    def __init__(self, **kwargs):
        super(GHGFactorResponse, self).__init__(**kwargs)
        self.factor_id = kwargs.get('factor_id', None)
        self.factor_code = kwargs.get('factor_code', None)
        self.factor_info = kwargs.get('factor_info', None)
        self.factor_description = kwargs.get('factor_description', None)
        self.source_organization = kwargs.get('source_organization', None)
        self.model = kwargs.get('model', None)
        self.factor_category = kwargs.get('factor_category', None)
        self.from_unit = kwargs.get('from_unit', None)
        self.factor_region = kwargs.get('factor_region', None)
