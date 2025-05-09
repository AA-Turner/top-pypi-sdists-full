# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GHGScopeResponse(Model):
    """GHGScopeResponse.

    :param scope_id: The Scope Identifier
    :type scope_id: int
    :param scope_info: The Scope Info
    :type scope_info: str
    :param scope_categories: The list of Scope Categories under this scope
    :type scope_categories: list[~energycap.sdk.models.GHGScopeCategoryChild]
    """

    _attribute_map = {
        'scope_id': {'key': 'scopeId', 'type': 'int'},
        'scope_info': {'key': 'scopeInfo', 'type': 'str'},
        'scope_categories': {'key': 'scopeCategories', 'type': '[GHGScopeCategoryChild]'},
    }

    def __init__(self, **kwargs):
        super(GHGScopeResponse, self).__init__(**kwargs)
        self.scope_id = kwargs.get('scope_id', None)
        self.scope_info = kwargs.get('scope_info', None)
        self.scope_categories = kwargs.get('scope_categories', None)
