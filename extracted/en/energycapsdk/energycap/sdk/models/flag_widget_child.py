# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class FlagWidgetChild(Model):
    """FlagWidgetChild.

    :param item_id: Identifier for the item could be meterId, placeId,
     accountId
    :type item_id: int
    :param item_display: Item display (name or code)
    :type item_display: str
    :param item_type: If item is a meter, this will be commodityCode
     If item is a building, this will say BUILDING
     If item is a account, this will say ACCOUNT
    :type item_type: str
    :param parent_id: Identifier for the parent of the item could be placeId,
     costCenterId
    :type parent_id: int
    :param parent_display: Parent display (name or code)
    :type parent_display: str
    :param parent_item_type: If parent is a building, this will say BUILDING
     For all other types, it will say ORGANIZATION
     If parent is a costcenter, this will say COSTCENTER
    :type parent_item_type: str
    :param split_parent: If the view is by Account or Meter, true indicates
     the account or meter is a master for a "Bill split"
    :type split_parent: bool
    :param split_child: If the view is by Account or Meter, true indicates the
     account or meter is a recipient of a "Bill split"
    :type split_child: bool
    :param calculated: If the view is by Account or Meter, true indicates the
     account or meter is part of a "Bill calculation"
    :type calculated: bool
    :param active: If the view is by Account or Meter, true indicates the
     account or meter is active
    :type active: bool
    :param cost: Total cost of all the bills that have flags for this item
    :type cost: float
    :param cost_recovery: Total cost recovery for bill flags for this item
    :type cost_recovery: float
    :param flag_count: Total number of bill flags for this item
    :type flag_count: int
    """

    _attribute_map = {
        'item_id': {'key': 'itemId', 'type': 'int'},
        'item_display': {'key': 'itemDisplay', 'type': 'str'},
        'item_type': {'key': 'itemType', 'type': 'str'},
        'parent_id': {'key': 'parentId', 'type': 'int'},
        'parent_display': {'key': 'parentDisplay', 'type': 'str'},
        'parent_item_type': {'key': 'parentItemType', 'type': 'str'},
        'split_parent': {'key': 'splitParent', 'type': 'bool'},
        'split_child': {'key': 'splitChild', 'type': 'bool'},
        'calculated': {'key': 'calculated', 'type': 'bool'},
        'active': {'key': 'active', 'type': 'bool'},
        'cost': {'key': 'cost', 'type': 'float'},
        'cost_recovery': {'key': 'costRecovery', 'type': 'float'},
        'flag_count': {'key': 'flagCount', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(FlagWidgetChild, self).__init__(**kwargs)
        self.item_id = kwargs.get('item_id', None)
        self.item_display = kwargs.get('item_display', None)
        self.item_type = kwargs.get('item_type', None)
        self.parent_id = kwargs.get('parent_id', None)
        self.parent_display = kwargs.get('parent_display', None)
        self.parent_item_type = kwargs.get('parent_item_type', None)
        self.split_parent = kwargs.get('split_parent', None)
        self.split_child = kwargs.get('split_child', None)
        self.calculated = kwargs.get('calculated', None)
        self.active = kwargs.get('active', None)
        self.cost = kwargs.get('cost', None)
        self.cost_recovery = kwargs.get('cost_recovery', None)
        self.flag_count = kwargs.get('flag_count', None)
