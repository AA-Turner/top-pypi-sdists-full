
from . import _VDAPIService, _VDDuplicateableResponse

class _SupplyTagAPI(_VDAPIService):

    __RESPONSE_OBJECT__ = _VDDuplicateableResponse
    __API__ = "supply_tags"


class _SupplyPartnerAPI(_VDAPIService):

    __API__ = "supply_partners"

class _SupplyLabelAPI(_VDAPIService):

    __API__ = "supply_labels"

class _ConnectedSupplyAPI(_VDAPIService):

    __API__ = "connected_supply"

class _SupplyRouterAPI(_VDAPIService):

    __API__ = "supply_routers"




