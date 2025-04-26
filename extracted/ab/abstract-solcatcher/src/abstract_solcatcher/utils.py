import asyncio,httpx,logging,json
from abstract_utilities import eatAll,get_any_value
from abstract_security import get_env_value
from abstract_apis import get_headers,get_response
import requests
solana_rpc_url="http://api.mainnet-beta.solana.com"
fall_back_rpc = get_env_value('solana_fallback_rpc_url')
def getSolcatcherUrl(endpoint=None):
  return getEndpointUrl(endpoint=endpoint,url='https://solcatcher.io')
def getSolcatcherPairCatchUrl(endpoint=None):
  return getEndpointUrl(endpoint=endpoint,url='https://solcatcher.io/pairCatch')
def getSolcatcherTsUrl(endpoint=None):
  return getEndpointUrl(endpoint=endpoint,url='https://solcatcher.io/ts')
def getSolcatcherDbCalls(endpoint=None):
  return getEndpointUrl(endpoint=endpoint,url="https://solcatcher.io/dbCalls")
def get_response(response):
    if isinstance(response,requests.Response) or isinstance(response,httpx.Response):
      try:
        response = response.json()
      except:
        try:
          response = response.text
        except:
          pass
      return response
def get_result(response,key='result'):
    response = get_response(response)
    if isinstance(response,dict):
        result = get_any_value(response,key)
        return result
    return response
def get_socatcherSettings(getResult = None,getResponse=None):
    return {"getResult":getResult or True,"getResponse":getResponse or True}
def get_db_header(headers=None, api_key=None):
    # Start with existing or default headers
    header = {}
    # Retrieve the key from environment or config
    key = api_key or get_env_value('SOLCATCHER_DB_API_KEY')
       # If key is not None, add the header; otherwise skip it
    if key:
        header["X-API-KEY"] = str(key) if key else ""
    # else do not set "X-API-KEY" at all
    header.update(headers or get_headers())
    return header
def post_request(endpoint, **kwargs):
    url = getSolcatcherDbCalls(endpoint=endpoint)
    response = requests.post(url=url, data=json.dumps(kwargs), headers=get_db_header())
    return get_response(response)
def getEndpointUrl(endpoint=None,url=None):
  if endpoint:
    url = eatAll(url,['/'])
    endpoint = eatAll(endpoint,['/'])
    url= f"{url}/{endpoint}"
  return url
def try_json_dumps(data):
  if isinstance(data,dict):
    try:
      data = json.dumps(data)
    except:
      pass
    return data
def get_url(url=None):
    if isinstance(url,dict):
      url = url.get('url',url)
    return url
def getCallArgs(endpoint):
  return {'getMetaData': ['signature'], 'getPoolData': ['signature'], 'getTransactionData': ['signature'], 'getPoolInfo': ['signature'], 'getMarketInfo': ['signature'], 'getKeyInfo': ['signature'], 'getLpKeys': ['signature'], 'process': ['signature']}.get(get_endpoint(endpoint))
def ifListGetSection(listObj,section=0):
  if isinstance(listObj,list):
      if len(listObj)>section:
          return listObj[section]
  return listObj
def updateData(data,**kwargs):
  data.update(kwargs)
  return data
def get_method(method=None):
  return method or 'default_method'
def get_resp(response=None):
  response = response or {}
  if isinstance(response,dict):
    response = {"response":response}
  return response
def get_payload(*args,**kwargs):
    payload = args
    if args and kwargs:
        payload.append(kwargs)
    else:
        payload = kwargs
    return payload
defaultSolcatcherSettings = get_socatcherSettings()
