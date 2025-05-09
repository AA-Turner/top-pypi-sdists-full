# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ChannelVersionResponse(Model):
    """ChannelVersionResponse.

    :param channel_version_id: The channel version identifier
    :type channel_version_id: int
    :param multiplier: The channel multiplier
    :type multiplier: float
    :param unit:
    :type unit: ~energycap.sdk.models.UnitChild
    :param observation_rule:
    :type observation_rule: ~energycap.sdk.models.ObservationRule
    :param maximum_reading: The channel's max reading
    :type maximum_reading: float
    :param begin_date: Date this channel version started to be used
    :type begin_date: datetime
    :param end_date: Date this channel version stopped being used
    :type end_date: datetime
    :param udfs: List of user defined/custom fields and values for this
     version
    :type udfs: list[~energycap.sdk.models.UDFFieldChild]
    """

    _attribute_map = {
        'channel_version_id': {'key': 'channelVersionId', 'type': 'int'},
        'multiplier': {'key': 'multiplier', 'type': 'float'},
        'unit': {'key': 'unit', 'type': 'UnitChild'},
        'observation_rule': {'key': 'observationRule', 'type': 'ObservationRule'},
        'maximum_reading': {'key': 'maximumReading', 'type': 'float'},
        'begin_date': {'key': 'beginDate', 'type': 'iso-8601'},
        'end_date': {'key': 'endDate', 'type': 'iso-8601'},
        'udfs': {'key': 'udfs', 'type': '[UDFFieldChild]'},
    }

    def __init__(self, *, channel_version_id: int=None, multiplier: float=None, unit=None, observation_rule=None, maximum_reading: float=None, begin_date=None, end_date=None, udfs=None, **kwargs) -> None:
        super(ChannelVersionResponse, self).__init__(**kwargs)
        self.channel_version_id = channel_version_id
        self.multiplier = multiplier
        self.unit = unit
        self.observation_rule = observation_rule
        self.maximum_reading = maximum_reading
        self.begin_date = begin_date
        self.end_date = end_date
        self.udfs = udfs
