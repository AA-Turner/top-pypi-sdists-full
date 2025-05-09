# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class EmissionRecordType(Model):
    """EmissionRecordType.

    :param emission_record_type_id: Id of the emission record type
    :type emission_record_type_id: int
    :param emission_record_type_info: Name of the emission record type
    :type emission_record_type_info: str
    """

    _attribute_map = {
        'emission_record_type_id': {'key': 'emissionRecordTypeId', 'type': 'int'},
        'emission_record_type_info': {'key': 'emissionRecordTypeInfo', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(EmissionRecordType, self).__init__(**kwargs)
        self.emission_record_type_id = kwargs.get('emission_record_type_id', None)
        self.emission_record_type_info = kwargs.get('emission_record_type_info', None)
