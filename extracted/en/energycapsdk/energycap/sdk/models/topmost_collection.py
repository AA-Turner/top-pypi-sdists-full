# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class TopmostCollection(Model):
    """TopmostCollection.

    :param is_multi_topmost_collection: User's topmost combines multiple
     collections
    :type is_multi_topmost_collection: bool
    :param multi_topmost_collections:
    :type multi_topmost_collections:
     list[~energycap.sdk.models.CollectionChild]
    :param collection_id: The collection identifier
    :type collection_id: int
    :param collection_code: The collection code
    :type collection_code: str
    :param collection_info: The collection info
    :type collection_info: str
    :param collection_icon:
    :type collection_icon: ~energycap.sdk.models.Icon
    """

    _attribute_map = {
        'is_multi_topmost_collection': {'key': 'isMultiTopmostCollection', 'type': 'bool'},
        'multi_topmost_collections': {'key': 'multiTopmostCollections', 'type': '[CollectionChild]'},
        'collection_id': {'key': 'collectionId', 'type': 'int'},
        'collection_code': {'key': 'collectionCode', 'type': 'str'},
        'collection_info': {'key': 'collectionInfo', 'type': 'str'},
        'collection_icon': {'key': 'collectionIcon', 'type': 'Icon'},
    }

    def __init__(self, **kwargs):
        super(TopmostCollection, self).__init__(**kwargs)
        self.is_multi_topmost_collection = kwargs.get('is_multi_topmost_collection', None)
        self.multi_topmost_collections = kwargs.get('multi_topmost_collections', None)
        self.collection_id = kwargs.get('collection_id', None)
        self.collection_code = kwargs.get('collection_code', None)
        self.collection_info = kwargs.get('collection_info', None)
        self.collection_icon = kwargs.get('collection_icon', None)
