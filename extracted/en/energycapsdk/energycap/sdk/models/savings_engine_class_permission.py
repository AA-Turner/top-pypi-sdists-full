# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SavingsEngineClassPermission(Model):
    """SavingsEngineClassPermission.

    :param run:
    :type run: bool
    """

    _attribute_map = {
        'run': {'key': 'run', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(SavingsEngineClassPermission, self).__init__(**kwargs)
        self.run = kwargs.get('run', None)
