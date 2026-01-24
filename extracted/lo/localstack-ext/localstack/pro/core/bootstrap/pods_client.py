_L='versions'
_K='Retrieving state from the container'
_J='Content-Length'
_I='services'
_H='status'
_G='service'
_F='message'
_E='version'
_D='event'
_C=True
_B=False
_A=None
import builtins,io,json,logging,os,zipfile
from abc import ABC,abstractmethod
from functools import singledispatch
from pathlib import Path
from typing import IO,Any,Optional,TypedDict
from urllib import parse
from urllib.parse import urlparse
import click,requests,yaml
from click import ClickException
from localstack import config,constants
from localstack.cli import console
from localstack.constants import APPLICATION_JSON,HEADER_CONTENT_TYPE,LOCALHOST_HOSTNAME
from localstack.pro.core.bootstrap import auth
from localstack.pro.core.bootstrap.auth import get_platform_auth_headers
from localstack.pro.core.bootstrap.pods.constants import INTERNAL_REQUEST_PARAMS_HEADER
from localstack.pro.core.bootstrap.pods.remotes.api import CloudPodsRemotesClient
from localstack.pro.core.bootstrap.pods.remotes.configs import DEFAULT_REMOTE_SCHEME,RemoteConfig,RemoteConfigParams
from localstack.pro.core.bootstrap.pods.remotes.params import get_remote_params_callable
from localstack.pro.core.config import CLI_INJECT_POD_IDENTITY,POD_LOAD_CLI_TIMEOUT
from localstack.pro.core.constants import API_PATH_PODS,CLOUDPODS_METADATA_FILE,HEADER_POD_SECRET
from localstack.utils.bootstrap import in_ci
from localstack.utils.http import safe_requests
from localstack.utils.strings import to_str
from packaging import version
from requests.structures import CaseInsensitiveDict
from rich.progress import Progress
LOG=logging.getLogger(__name__)
HEADER_LS_API_KEY='ls-api-key'
HEADER_LS_VERSION='ls-version'
HEADER_AUTHORIZATION='Authorization'
DiffResult=dict[str,list[dict[str,Any]]]
class CloudPodNotFound(Exception):
	def __init__(A,pod_name:str)->_A:super().__init__(f"Cloud pod '{pod_name}' not found")
class PodInfo(TypedDict,total=_B):name:str;pod_id:str;version:int;services:list[str];description:str;size:int;remote:str;localstack_version:str;encrypted:bool
def fetch_state_response_from_instance(services:list[str]|_A=_A)->tuple[requests.Response,PodInfo]:
	B=services;C=f"{get_runtime_pods_endpoint()}/state";D=','.join(B)if B else'';E={INTERNAL_REQUEST_PARAMS_HEADER:'{}'};F:bool=in_ci();A=requests.get(C,params={_I:D},headers=E,stream=not F)
	if not A.ok:raise Exception(f"An error occurred while retrieving the LocalStack state (code {A.status_code})")
	G=PodInfo(services=A.headers.get('x-localstack-pod-services','').split(','),size=int(A.headers.get('x-localstack-pod-size',0)));return A,G
def write_state_zip_to_file(open_file:IO[bytes],services:list[str]|_A=_A,chunk_size:int=100000)->PodInfo:
	A,D=fetch_state_response_from_instance(services);E=int(A.headers.get(_J,0))
	with Progress()as B:
		F=B.add_task(_K,total=E)
		for C in A.iter_content(chunk_size=chunk_size):open_file.write(C);B.update(F,advance=len(C))
	return D
def get_state_zip_from_instance(services:list[str]|_A=_A)->tuple[bytes,PodInfo]:
	A,E=fetch_state_response_from_instance(services);F=int(A.headers.get(_J,0));G:bool=in_ci();B=A.content if G else b''
	with Progress()as C:
		H=C.add_task(_K,total=F)
		for D in A.iter_content(chunk_size=100000):B+=D;C.update(H,advance=len(D))
	return B,E
class CloudPodRemoteAttributes(TypedDict,total=_B):is_public:bool;description:str|_A;services:list[str]|_A
class PodSaveRequest(TypedDict,total=_B):remote:dict[str,str|dict]|_A;attributes:CloudPodRemoteAttributes|_A
class CloudPodsService(ABC):
	@abstractmethod
	def save(self,pod_name:str,attributes:CloudPodRemoteAttributes|_A=_A,remote:RemoteConfigParams|_A=_A,local:bool=_B,version:int|_A=_A,secret:str|_A=_A)->PodInfo:0
	@abstractmethod
	def delete(self,pod_name:str,remote:RemoteConfigParams|_A=_A,delete_from_remote:bool=_C)->_A:0
	@abstractmethod
	def load(self,pod_name:str,remote:RemoteConfigParams|_A=_A,version:int|_A=_A,merge_strategy:str|_A=_A,ignore_version_mismatches:bool=_C,secret:str|_A=_A)->_A:0
	@abstractmethod
	def list(self,remote:RemoteConfigParams|_A=_A)->list:0
	@abstractmethod
	def get_versions(self,pod_name:str,remote:RemoteConfigParams|_A=_A)->builtins.list:0
	def diff(A,pod_name:str,remote:RemoteConfigParams|_A=_A,version:int|_A=_A)->DiffResult:0
	def _get_cloud_pods_info(C,pod_name:str)->dict:
		B=pod_name;A=requests.get(create_platform_url(B),headers=get_platform_auth_headers())
		if A.status_code==404:raise CloudPodNotFound(B)
		if not A.ok:_raise_exception_with_formatted_message(f"Unable to get info for pod: {B}",A)
		return json.loads(A.content)
	def _get_localstack_pod_version(H,pod_name:str,cloud_pods_dict:dict,version:int|_A=_A)->str|_A:
		B=cloud_pods_dict;A=version;C:list[dict]=B[_L];D=int(B['max_version'])
		if A and A>D:raise Exception(f"Unable to load pod {pod_name} with version {A}. The maximum version available in the remote storage is {D}")
		E=list(filter(lambda v:v[_E]==A,C));F=E[0]if E else C[-1];G:str|_A=F['localstack_version'];return G
	def get_state_data(B)->dict:
		A=requests.get(url=f"{get_runtime_pods_endpoint()}/state/metamodel",headers=_get_headers())
		if not A.ok:_raise_exception_with_formatted_message('Unable to get state data from the LocalStack instance',A)
		return json.loads(A.content)
	def set_remote_attributes(G,pod_name:str,attributes:CloudPodRemoteAttributes,remote:RemoteConfigParams|_A=_A)->_A:
		D='is_public';C=remote;B=pod_name
		if C:LOG.debug("Trying to set attributes for remote '%s'. Currently we support attributes only for the default remote",C);return
		E=create_platform_url(B);F=auth.get_platform_auth_headers();A=safe_requests.patch(E,headers=F,json={D:attributes[D]})
		if not A.ok:raise Exception(f"Error setting remote attributes for Cloud Pod {B} (code {A.status_code}): {A.text}")
def _get_headers()->dict[str,str]:
	A={HEADER_CONTENT_TYPE:APPLICATION_JSON}
	if CLI_INJECT_POD_IDENTITY:A.update(CaseInsensitiveDict(auth.get_platform_auth_headers()))
	return A
def _raise_exception_with_formatted_message(message:str,response:requests.Response):raise Exception(f"{message}: {response.text}")
def _get_remote_params_payload(remote:RemoteConfigParams|_A)->PodSaveRequest:
	A=remote
	if not A:return{}
	C=_get_remote_configuration(A,render_params=_B);B=get_remote_params_callable(C.remote_url)
	if not B:return{}
	A.remote_params=B();return{'remote':A.to_dict()}
class CloudPodsClient(CloudPodsService):
	def __init__(A,interactive:bool=_B)->_A:A.interactive=interactive
	def _process_response(J,response,message:str):
		F='operation';C=message;B=console.status(C);B.start()
		for G in response.iter_lines():
			A=json.loads(G)
			if A[_D]=='log':B.update(A[_F])
			if A[_D]==_G:D,H,E=A[_G],A[_H],A[F];C=f"{D}: {E} succeeded"if H=='ok'else f"{D}: {E} failed";B.update(C)
			elif A[_D]=='completion':
				B.stop()
				if A[_H]=='error':raise Exception(A.get(_F))
				if A[F]=='save':I=PodInfo(**A['info']);return I
		B.stop()
	def save(C,pod_name:str,attributes:CloudPodRemoteAttributes|_A=_A,remote:RemoteConfigParams|_A=_A,local:bool=_B,version:int|_A=_A,secret:str|_A=_A)->PodInfo:
		H=version;E=secret;D=pod_name;F=f"{get_runtime_pods_endpoint(E)}/{D}?"
		if local:F+='&local=true'
		if H:F+=f"&version={H}"
		I:PodSaveRequest=_get_remote_params_payload(remote);I.update({'attributes':attributes});J=_get_headers()
		if E:J[HEADER_POD_SECRET]=E
		B=requests.post(url=F,json=I,headers=J,stream=C.interactive)
		if not B.ok:_raise_exception_with_formatted_message(f"Unable to save pod {D}",B)
		G={}
		if C.interactive:G=C._process_response(B,message=f"Saving Cloud Pod {D}")
		else:
			for A in B.iter_lines():
				A=json.loads(A)
				if A[_D]=='pod_info':G=PodInfo(**A['extra'])
				elif A[_D]=='exception':raise Exception(A[_F])
		return G
	def delete(E,pod_name:str,remote:RemoteConfigParams|_A=_A,delete_from_remote:bool=_C):
		A=pod_name;B=f"{get_runtime_pods_endpoint()}/{A}"
		if not delete_from_remote:B+='?local=true'
		D=_get_remote_params_payload(remote);C=requests.delete(url=B,json=D,headers=_get_headers())
		if not C.ok:_raise_exception_with_formatted_message(f"Unable to delete Cloud Pod '{A}'",C)
	def load(A,pod_name:str,remote:RemoteConfigParams|_A=_A,version:int|_A=_A,merge_strategy:str|_A=_A,ignore_version_mismatches:bool=_B,secret:str|_A=_A)->_A:
		I=secret;H=ignore_version_mismatches;G=merge_strategy;E=version;D=remote;B=pod_name
		if in_ci():H=_C
		J=_get_remote_configuration(D,render_params=_B)if D else _A;O=J and J.scheme!=DEFAULT_REMOTE_SCHEME
		if not O and not H:
			P=A._get_cloud_pods_info(B);K:str=A._get_localstack_pod_version(pod_name=B,version=E,cloud_pods_dict=P);L:str=get_ls_version_from_health()
			if not is_compatible_version(K,L)and not click.confirm(f"This Cloud Pod was created with LocalStack {K} but you are running LocalStack {L}. Cloud Pods might be incompatible across different LocalStack versions.\nLoading a Cloud Pod with mismatching version might lead to a corrupted state of the emulator. Do you want to continue?"):raise click.Abort('LocalStack version mismatch')
		M=f"{get_runtime_pods_endpoint()}/{B}";C={}
		if E:C[_E]=E
		if G:C['merge']=G
		if C:M+=f"?{parse.urlencode(C)}"
		Q=_get_remote_params_payload(D);N=_get_headers()
		if I:N[HEADER_POD_SECRET]=I
		F=requests.put(url=M,json=Q,headers=N,stream=A.interactive)
		if not F.ok:_raise_exception_with_formatted_message(f"Unable to load pod {B}",F)
		if A.interactive:A._process_response(F,message=f"Loading Cloud Pod {B}")
	def list(E,remote:RemoteConfigParams|_A=_A,creator:str|_A=_A)->list:
		B=creator;D=_get_remote_params_payload(remote);C=get_runtime_pods_endpoint()
		if B:C+=f"?creator={B}"
		A=requests.get(C,json=D,headers=_get_headers())
		if not A.ok:_raise_exception_with_formatted_message('Unable to list Cloud Pods',A)
		return json.loads(A.content).get('cloudpods',[])
	def get_versions(D,pod_name:str,remote:RemoteConfigParams|_A=_A)->builtins.list:
		B=pod_name;C=_get_remote_params_payload(remote);A=requests.get(url=f"{get_runtime_pods_endpoint()}/{B}/versions",json=C,headers=_get_headers())
		if A.status_code==404:raise Exception(f"Cloud Pod {B} not found")
		if not A.ok:_raise_exception_with_formatted_message(f"Unable to get versions for pod {B}",A)
		return json.loads(A.content).get(_L,[])
	def diff(G,pod_name:str,remote:RemoteConfigParams|_A=_A,version:int|_A=_A)->DiffResult:
		C=version;B=pod_name;D=f"{get_runtime_pods_endpoint()}/{B}/diff";E={}
		if C:E[_E]=C;D+=f"?{parse.urlencode(E)}"
		F=_get_remote_params_payload(remote);A=requests.get(url=D,json=F,headers=_get_headers())
		if not A.ok:_raise_exception_with_formatted_message(f"Unable to get diff for pod {B}",A)
		return json.loads(A.content)
def _get_remote_configuration(params:RemoteConfigParams,render_params:bool=_C)->RemoteConfig:
	A=params;D=CloudPodsRemotesClient()
	try:C=D.get_remote(name=A.remote_name)
	except Exception as E:raise ClickException(f"Error getting configuration for the remote {A.remote_name}")from E
	B=C['remote_url']
	if render_params:B=A.render_url(B)
	LOG.debug('Remote configuration: %s',C);return RemoteConfig(remote_url=B)
def get_runtime_pods_endpoint(passphrase:str|_A=_A)->str:
	if not passphrase:return f"{config.external_service_url()}{API_PATH_PODS}"
	A=config.external_service_url(protocol='https')
	if LOCALHOST_HOSTNAME not in A:LOG.warning('LocalStack is not running locally and we are sending the encryption passphrase to a different host!')
	return f"{A}{API_PATH_PODS}"
class StateService:
	def export_pod(I,target:str,services:Optional[list[str]]=_A)->PodInfo:
		C=target;D=urlparse(C);A:str=os.path.abspath(os.path.join(D.netloc,D.path));E=Path(A).parent.absolute()
		if not os.path.exists(E):raise Exception(f"{E} is not a valid path")
		with open(A,'wb')as G:F=write_state_zip_to_file(G,services)
		B:dict=get_environment_metadata();B['name']=os.path.basename(C);B.update(F)
		with zipfile.ZipFile(file=A,mode='a')as H:H.writestr(CLOUDPODS_METADATA_FILE,yaml.dump(B))
		return F
	def import_pod(I,source:str,show_progress:bool=_C)->_A:
		E='pro';C=urlparse(source);A=os.path.abspath(os.path.join(C.netloc,C.path))
		if not os.path.exists(A):raise Exception(f"Path {A} does not exist")
		if not os.path.isfile(A):raise Exception(f"Path {A} is not a file")
		with open(A,mode='rb')as B:
			with zipfile.ZipFile(B,'r')as F:D=read_metadata_from_pod(F)or{}
			G=D.get(_I,[]);H:bool=get_environment_metadata().get(E)
			if D.get(E,_B)and not H:console.print('Warning: You are trying to load a Cloud Pod generated with a Pro license.The loaded state might be incomplete.')
			B.seek(0);load_local_state_from_open_zipfile(file=B,number_services=len(G),show_progress=show_progress)
def list_public_pods()->list[str]:
	B=create_platform_url('public');C=auth.get_platform_auth_headers();A=safe_requests.get(B,headers=C)
	if not A.ok:raise Exception(to_str(A.content))
	D=json.loads(A.content);return[A['pod_name']for A in D]
@singledispatch
def read_metadata_from_pod(zip_file:zipfile.ZipFile)->dict|_A:
	try:A=yaml.safe_load(zip_file.read(CLOUDPODS_METADATA_FILE));return A
	except KeyError:LOG.debug('No %s file in the archive',CLOUDPODS_METADATA_FILE)
@read_metadata_from_pod.register(bytes)
def _(zip_file:bytes)->dict|_A:A=zip_file;A=zipfile.ZipFile(io.BytesIO(A),'r');return read_metadata_from_pod(A)
@read_metadata_from_pod.register(str)
def _(zip_file:str)->dict|_A:
	with zipfile.ZipFile(zip_file)as A:return read_metadata_from_pod(A)
def call_post_load_endpoint(content:bytes|IO[bytes],stream:bool)->requests.Response:
	B=stream;C=get_runtime_pods_endpoint()
	try:
		A=requests.post(C,data=content,timeout=POD_LOAD_CLI_TIMEOUT,stream=B)
		if not B:LOG.debug('Loaded services from local state file: %s',A.content)
	except requests.exceptions.Timeout as D:raise Exception('Timeout exceed for the pod load operation. To avoid this issue, try to increase thevalue of the POD_LOAD_CLI_TIMEOUT configuration variable.')from D
	if not A.ok:raise Exception(f"Unable to load LocalStack state via {C}")
	return A
def load_state_with_progress_bar(content:bytes|IO[bytes],number_services:int=0)->_A:
	A=content;D=call_post_load_endpoint(A,stream=_C);C=0
	with Progress()as B:
		E=B.add_task('Loading state',total=number_services)
		for F in D.iter_lines():A=json.loads(F);LOG.debug('Loaded service: %s',A);G,H=A[_G],'✅'if A[_H]else'❌';B.log(f"{G}: {H}");C+=1;B.update(E,completed=C)
def load_local_state(content:bytes,number_services:int=0,show_progress:bool=_C)->_A:
	A=content
	if show_progress:load_state_with_progress_bar(content=A,number_services=number_services)
	else:call_post_load_endpoint(content=A,stream=_B)
def load_local_state_from_open_zipfile(file:IO[bytes],number_services:int=0,show_progress:bool=_B)->_A:
	if show_progress:load_state_with_progress_bar(content=file,number_services=number_services)
	else:call_post_load_endpoint(content=file,stream=_B)
def get_environment_metadata()->dict:
	C=get_runtime_pods_endpoint();A=f"{C}/environment";B=requests.get(A)
	if not B.ok:raise Exception(f"Unable to retrieve environment metadata from {A}")
	return json.loads(B.content)
def reset_state(services:list=_A)->_A:
	B=services
	def C(_url:str)->_A:
		A=requests.post(_url)
		if not A.ok:LOG.debug('Reset call to %s failed: status code %s',_url,A.status_code);raise Exception('Failed to reset LocalStack')
	if not B:A=f"{config.external_service_url()}/_localstack/state/reset";C(A);return
	for D in B:A=f"{config.external_service_url()}/_localstack/state/{D}/reset";C(A)
def get_ls_version_from_health()->str:
	try:A=f"{config.external_service_url()}/_localstack/health";B=requests.get(A).json();return B[_E]
	except Exception:return''
def create_platform_url(path:str|_A=_A,api_endpoint:str|_A=_A)->str:
	B=api_endpoint;A=path;B=B or constants.API_ENDPOINT;C=f"{B}/cloudpods"
	if not A:return C
	A=A if A.startswith('/')else f"/{A}";return f"{C}{A}"
def is_compatible_version(version_one:str|_A,version_two:str|_A)->bool:
	B=version_two;A=version_one
	if not A or not B:return _B
	C=version.parse(A);D=version.parse(B);return C.base_version==D.base_version