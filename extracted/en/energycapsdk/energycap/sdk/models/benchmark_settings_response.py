# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BenchmarkSettingsResponse(Model):
    """BenchmarkSettingsResponse.

    :param benchmark1:
    :type benchmark1: ~energycap.sdk.models.BenchmarkWithUsedCountResponse
    :param benchmark2:
    :type benchmark2: ~energycap.sdk.models.BenchmarkWithUsedCountResponse
    :param benchmark3:
    :type benchmark3: ~energycap.sdk.models.BenchmarkWithUsedCountResponse
    """

    _attribute_map = {
        'benchmark1': {'key': 'benchmark1', 'type': 'BenchmarkWithUsedCountResponse'},
        'benchmark2': {'key': 'benchmark2', 'type': 'BenchmarkWithUsedCountResponse'},
        'benchmark3': {'key': 'benchmark3', 'type': 'BenchmarkWithUsedCountResponse'},
    }

    def __init__(self, **kwargs):
        super(BenchmarkSettingsResponse, self).__init__(**kwargs)
        self.benchmark1 = kwargs.get('benchmark1', None)
        self.benchmark2 = kwargs.get('benchmark2', None)
        self.benchmark3 = kwargs.get('benchmark3', None)
