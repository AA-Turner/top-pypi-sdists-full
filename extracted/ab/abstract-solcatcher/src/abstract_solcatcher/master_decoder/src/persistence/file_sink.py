from .sink import DecodeSink
from ..imports.utils.save_data import (
    update_sample_payloads,
    update_none_payloads,
)
from abstract_utilities import SingletonMeta
class payloadDatas(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.sample_payloads={}
            self.none_payloads={}
    def update_json_data(path,discriminator,event,**kwargs):
        data = get_json_data(path)
        if discriminator not in data:
            data[discriminator] = []
        if event not in data[discriminator]:
            data[discriminator][event] =  kwargs
            safe_json_save_data(data,path)
            
    def updateSamplePayloads(self,discriminator, event, **payload):
        data = self.update_json_data(self.sample_payloads,discriminator,event,**payload)
        self.sample_payloads=data
    def updateNonePayloads(self,discriminator, event, **payload):
        data = self.update_json_data(self.none_payloads,discriminator,event,**payload)
        self.none_payloads=data
def get_payload_datas():
    return payloadDatas()   

def save_decoded(self, *, discriminator, event, payload):
    get_payload_datas().updateSamplePayloads(discriminator, event, **payload)
def save_failed(self, *, discriminator, event, payload):
   get_payload_datas().updateNonePayloads(discriminator, event, **payload)
def get_none_payloads():
    return get_payload_datas().none_payloads
def get_sample_payloads():
    return get_payload_datas().sample_payloads
def return_all_datas():
    none_payloads = get_none_payloads()
    sample_payloads = get_sample_payloads()
    return {"sample":sample_payloads,"none":none_payloads}
