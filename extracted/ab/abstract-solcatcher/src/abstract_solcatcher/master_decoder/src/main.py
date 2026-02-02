
from .managers import get_decoder_env

from .imports.utils.save_data import (
    update_sample_payloads,
    update_none_payloads,
)
from abstract_utilities import *
class payloadDatas(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.sample_payloads={}
            self.none_payloads={}
    def update_json_data(self,data,discriminator,event,kwargs):
        if discriminator not in data:
            data[discriminator] = {}
        if event not in data[discriminator]:
            data[discriminator][event] =  kwargs
        return data
            
    def updateSamplePayloads(self,discriminator, event, payload):
        data = self.update_json_data(self.sample_payloads,discriminator,event,payload)
        self.sample_payloads=data
    def updateNonePayloads(self,discriminator, event, payload):
        data = self.update_json_data(self.none_payloads,discriminator,event,payload)
        self.none_payloads=data
def get_payload_datas():
    return payloadDatas()   

def save_decoded(discriminator, event, payload):
    get_payload_datas().updateSamplePayloads(discriminator, event, payload)
def save_failed(discriminator, event, payload):
   get_payload_datas().updateNonePayloads(discriminator, event, payload)
def get_none_payloads():
    return get_payload_datas().none_payloads
def get_sample_payloads():
    return get_payload_datas().sample_payloads
def return_all_datas():
    none_payloads = get_none_payloads()
    sample_payloads = get_sample_payloads()
    return {"sample":sample_payloads,"none":none_payloads}
def get_idl_json_data():
    return safe_read_from_json('events.json')
ENV = get_decoder_env()
def decode_record_data(**kwargs):

    result = ENV.decode(
        kwargs.get("b64"),
        signature=kwargs.get("signature"),
        program_id=kwargs.get("program_id"),
    )
    print(result)
    payload = {
        "data": kwargs.get("b64"),
        "signature": kwargs.get("signature"),
        "program_id": kwargs.get("program_id"),
        "result": result,
    }

    if result is None:
        save_failed(
            discriminator=kwargs.get("discriminator"),
            event=kwargs.get("event"),
            payload=payload,
        )
    else:
        save_decoded(
            discriminator=kwargs.get("discriminator"),
            event=kwargs.get("event"),
            payload=payload,
        )

##for log in logs:
##    b64 = log.get('b64')
##    event_name = log.get("event")
##    signature = log.get('signature')
##    program_id = log.get('program_id')
##    result = env.decode(b64, signature=signature, program_id=program_id)
##    print(result)
