_A=None
import json
from abc import ABC,abstractmethod
import requests
from localstack import config
from localstack.pro.core.bootstrap.pods.constants import INTERNAL_REQUEST_PARAMS_HEADER
from localstack.pro.core.constants import API_PATH_PODS
class CloudPodsRemotesInterface(ABC):
	@abstractmethod
	def create_remote(self,name:str,protocols:list[str],remote_url:str|_A=_A)->_A:0
	@abstractmethod
	def delete_remote(self,name:str)->_A:0
	@abstractmethod
	def get_remote(self,name:str)->dict[str,str]:0
	@abstractmethod
	def get_remotes(self)->list[dict[str,str]]:0
class CloudPodsRemotesClient(CloudPodsRemotesInterface):
	@property
	def endpoint(self):return f"{config.external_service_url()}{API_PATH_PODS}/remotes"
	def create_remote(A,name:str,protocols:list[str],remote_url:str|_A=_A)->_A:
		C={'name':name,'protocols':protocols,'remote_url':remote_url};B=A._client.post(url=f"{A.endpoint}/{name}",data=json.dumps(C),headers={'Content-Type':'application/json'})
		if not B.ok:raise Exception(f"Failed to create remote: {B.content}")
	def delete_remote(A,name:str)->_A:
		B=A._client.delete(url=f"{A.endpoint}/{name}")
		if not B.ok:raise Exception(f"Failed to delete remote: {B.content}")
	def get_remotes(B)->list[dict[str,str]]:
		A=B._client.get(url=B.endpoint)
		if not A.ok:raise Exception(f"Failed to get list of remotes: {A.content}")
		C=json.loads(A.content);return C.get('remotes',[])
	def get_remote(B,name:str)->dict[str,str]:
		A=B._client.get(url=f"{B.endpoint}/{name}")
		if not A.ok:raise Exception(f"Failed to get remote: {A.content}")
		C=json.loads(A.content);return C
	@property
	def _client(self)->requests.Session:A=requests.Session();A.headers.update({INTERNAL_REQUEST_PARAMS_HEADER:'{}'});return A