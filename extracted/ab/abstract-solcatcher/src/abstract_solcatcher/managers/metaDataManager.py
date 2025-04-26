from abstract_utilities import get_any_value,SingletonMeta
import logging,os,json
from abstract_pandas import pd
from abstract_apis import getRequest
from PIL import Image
import io
import requests
from ..imageUtils import *
from ..dbConfig import get_meta_data_by_mint
def get_image_vars(uri):
    response = getRequest(url=uri,data={})
    return response
def get_image_data(image_url):
    try:
        response = getRequest(url=uri,data={},result='content')
        image = Image.open(io.BytesIO(response.content))
        image.thumbnail((200, 200))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        return bio.getvalue()
    except:
        pass
metaDataLowerKeys = {
    'image': 'image',
    'uri': 'uri',
    'supply': 'supply',
    'symbol': 'symbol',
    'mintauthority': 'mintAuthority',
    'freezeauthority': 'freezeAuthority',
    'twitter': 'twitter',
    'website': 'website',
    'ismutable': 'isMutable',
    'creators': 'creators',
    'updateauthority': 'updateAuthority',
    'createdon': 'createdOn',
    'primarysalehappened': 'createdOn',
    'description': 'description'
}
metaDataTypeKeys = {
    'image': str,
    'uri': str,
    'supply': int,
    'name':str,
    'symbol': str,
    'mintAuthority': str,
    'freezeAuthority': str,
    'twitter': str,
    'website': str,
    'isMutable': bool,
    'creators': str,
    'updateAuthority': str,
    'createdOn': int,
    'primarySaleHappened': bool,
    'description': str
}
metaDataCheckKeys = {
    'image': True,
    'uri': True,
    'supply': True,
    'symbol': True,
    'name':True,
    'mintAuthority': True,
    'freezeAuthority': True,
    'twitter': True,
    'website': True,
    'isMutable': True,
    'creators': True,
    'updateAuthority': True,
    'createdOn': True,
    'primarySaleHappened': True,
    'description': True
}
metaKeys = list(metaDataTypeKeys.keys())

def make_insert(key):
    key = key.replace(' ', '_').upper()
    return f"-{key}-"
def make_insert_bool(key):
    key = key.replace(' ', '_').upper()
    return f"-{key}_BOOL-"
def make_check_bool(key):
    key = key.replace(' ', '_').upper()
    return f"-{key}_CHECK-"
def deKeyKey(key):
    return key.lower()[1:-1].replace('_',' ')
def getBool(key, value):
    return isinstance(value, metaDataTypeKeys.get(key))
class metaDataManager(metaclass=SingletonMeta):
    def __init__(self):
        self.allMetaData = {}
        self.metaDataCheckKeys=metaDataCheckKeys
        self.metaDataTypeKeys = metaDataTypeKeys
    def changeTally(self,event,values):
        lower_key = deKeyKey(event)
        regularMetakey = metaDataLowerKeys.get(lower_key)
        self.metaDataCheckKeys[regularMetakey] = values[event]
    def processMetaData(self,mint,imageData=True):
        if not self.allMetaData.get(mint):
            metaData = get_meta_data_by_mint(mint)
            self.get_meta_vars(metaData,imageData)
            self.allMetaData[mint] = {"processed":self.datas_js,'bools':self.bool_js}
        return self.allMetaData[mint]
    def filter_meta_data(self,mint,filterMetaChecks={}):
        metaData_js = self.processMetaData(mint)
        bools = metaData_js['bools']
        self.allMetaData[mint]['filtered']=True
        for key,check in self.metaDataCheckKeys.items():
            if check and not bools.get(key):
                self.allMetaData[mint]['filtered']=False
                break
        return self.allMetaData[mint]['filtered']
    def get_meta_vars(self,metaData,imageData=True):
        self.datas_js = {}
        self.bool_js = {}
        self.metaData = self.get_uri(metaData,imageData)
        for key in metaKeys:
            self.get_from_any_meta(key,metaData)
    def get_from_any_meta(self,key,metaData):
        values = get_any_value(metaData, key) or None
        value = values[0] if values and isinstance(values, list) else values
        self.bool_js[key] =getBool(key, value)
        self.datas_js[key] = value
        return value
    def get_uri(self,metaData,imageData=True):
        key = 'uri'
        self.get_from_any_meta(key,metaData)
        
        if self.bool_js[key] and imageData:
           try:
                metaData[0].update(get_image_vars(self.datas_js[key]) or {})
           except:
                pass
        return metaData
            

