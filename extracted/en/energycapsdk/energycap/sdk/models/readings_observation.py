# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ReadingsObservation(Model):
    """ReadingsObservation.

    :param observation_id: The unique ID for the reading <span
     class='property-internal'>Required (defined)</span>
    :type observation_id: long
    :param time: The date and time of the reading <span
     class='property-internal'>Required (defined)</span>
    :type time: datetime
    :param value: The raw or computed value of the reading <span
     class='property-internal'>Required (defined)</span>
    :type value: float
    :param raw_value: The raw value of the reading (before multiplier or delta
     are applied) <span class='property-internal'>Required (defined)</span>
    :type raw_value: float
    :param estimated: Indicates if the reading is estimated <span
     class='property-internal'>Required (defined)</span>
    :type estimated: bool
    :param note: A note pertaining to the reading <span
     class='property-internal'>Required (defined)</span>
    :type note: str
    """

    _attribute_map = {
        'observation_id': {'key': 'observationId', 'type': 'long'},
        'time': {'key': 'time', 'type': 'iso-8601'},
        'value': {'key': 'value', 'type': 'float'},
        'raw_value': {'key': 'rawValue', 'type': 'float'},
        'estimated': {'key': 'estimated', 'type': 'bool'},
        'note': {'key': 'note', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(ReadingsObservation, self).__init__(**kwargs)
        self.observation_id = kwargs.get('observation_id', None)
        self.time = kwargs.get('time', None)
        self.value = kwargs.get('value', None)
        self.raw_value = kwargs.get('raw_value', None)
        self.estimated = kwargs.get('estimated', None)
        self.note = kwargs.get('note', None)
