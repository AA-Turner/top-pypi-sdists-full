# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SearchEmissionSourceChild(Model):
    """SearchEmissionSourceChild.

    :param result:
    :type result:
     ~energycap.sdk.models.SearchEmissionSourceChildSearchEmissionSource
    """

    _attribute_map = {
        'result': {'key': 'result', 'type': 'SearchEmissionSourceChildSearchEmissionSource'},
    }

    def __init__(self, *, result=None, **kwargs) -> None:
        super(SearchEmissionSourceChild, self).__init__(**kwargs)
        self.result = result
