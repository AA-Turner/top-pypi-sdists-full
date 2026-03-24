_C='pickle'
_B=True
_A=None
import dataclasses,os,traceback,typing as t
from contextlib import contextmanager
from functools import singledispatchmethod
import pytest
from _pytest.config import Config
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from localstack.aws.chain import Handler
from localstack.constants import ENV_PRO_ACTIVATED
from localstack.pro.core.persistence.avro.codec import AvroEncoder
from localstack.pro.core.persistence.utils.avro import supports_avro
from localstack.services.plugins import SERVICE_PLUGINS,ServiceManager
from localstack.services.stores import AccountRegionBundle,BaseStore
from localstack.state import StateContainer,StateVisitor
from localstack.state.pickle import PickleEncoder
from localstack.utils.objects import singleton_factory
from moto.core.base_backend import BackendDict,BaseBackend
from pluggy import Result
from pytest import Item
class StoreSerializationCheckerPlugin:
	def __init__(A,with_pickle:bool=_B):A.pickle_enabled=with_pickle
	@pytest.hookimpl()
	def pytest_configure(self,config:Config):
		from localstack.aws.handlers import serve_custom_service_request_handlers as A;from localstack.pro.core.persistence.avro import reducers as B;from localstack.pro.core.persistence.avro.aws.plugins import register_aws_avro_plugins as C;C();B.register()
		if self.pickle_enabled:from localstack.pro.core.persistence.pickling import reducers as D;D.register()
		A.append(get_dirty_marker_handler());config.addinivalue_line('markers','skip_store_check(reason=None): skip the store serialization check')
	@pytest.hookimpl(hookwrapper=_B)
	def pytest_runtest_call(self,item:Item)->_A:
		C:CallInfo=(yield)
		if C.excinfo:return
		if item.get_closest_marker('skip_store_check'):return
		D=StateSerializationErrorCollector(SERVICE_PLUGINS,with_pickle=self.pickle_enabled);A=get_dirty_marker_handler();B=D.try_serialize_state_containers(A.dirty);A.clear()
		if B.errors:raise StateSerializationTestException(B)
	@pytest.hookimpl(hookwrapper=_B)
	def pytest_runtest_makereport(self,item:Item,call:CallInfo[_A])->TestReport|_A:
		A=call;C:Result=(yield);B:TestReport=C.get_result()
		if A.excinfo is not _A and isinstance(A.excinfo.value,StateSerializationTestException):D:StateSerializationTestException=A.excinfo.value;B.longrepr=D.result.render_errors()
		return B
@singleton_factory
def get_dirty_marker_handler():return DirtyMarkerHandler()
@dataclasses.dataclass
class StateSerializationError:service:str;state_container:StateContainer;exception:Exception;serialization_backend:t.Literal[_C,'avro'];account_id:str|_A=_A;region:str|_A=_A
class StateSerializationTestResult:
	errors:list[StateSerializationError]
	def __init__(A):A.errors=[]
	def render_errors(A)->str:return'\n'.join([A.render_error(B)for B in A.errors])
	@staticmethod
	def render_error(error:StateSerializationError)->str:
		A=error;C=A.exception;B=f"Store {A.serialization_backend} serialization Error: {A.service}\n";B+=f"\t current stores: {A.state_container}\n"
		if A.account_id:B+=f"\t failing store: {A.account_id}:{A.region}\n"
		B+=f"\t error: {C}\n";B+='\t\t'.join(traceback.format_exception(C));return B
class StateSerializationTestException(Exception):
	result:StateSerializationTestResult
	def __init__(A,result:StateSerializationTestResult):super().__init__();A.result=result
class DirtyMarkerHandler(Handler):
	dirty:set[str]
	def __init__(A):A.dirty=set()
	def __call__(B,chain,context,response):
		A=context
		if not A.service:return
		B.dirty.add(A.service.service_name)
	def clear(A):A.dirty.clear()
class PicklingVisitor(StateVisitor):
	errors:list[StateSerializationError]
	def __init__(A,service_name:str):A.errors=[];A.service_name=service_name;A.pickle_encoder=PickleEncoder()
	def visit(A,state_container:StateContainer):
		B=state_container
		try:A.pickle_encoder.encodes(B)
		except Exception as C:D=StateSerializationError(service=A.service_name,state_container=B,exception=C,serialization_backend=_C);A.errors.append(D)
class AvroPicklingVisitor(StateVisitor):
	errors:list[StateSerializationError]
	def __init__(A,service_name:str,with_pickle:bool=_B):A.errors=[];A.service_name=service_name;A.avro_encoder=AvroEncoder();A.pickle_encoder=PickleEncoder()if with_pickle else _A
	@singledispatchmethod
	def visit(self,state_container:StateContainer):0
	@visit.register(AccountRegionBundle)
	def _(self,state_container:AccountRegionBundle):
		B=state_container;A=self
		for(C,D,E)in B.iter_stores():
			try:A.avro_encoder.encodes(E)
			except Exception as F:G=StateSerializationError(service=A.service_name,state_container=B,exception=F,serialization_backend='avro',account_id=C,region=D);A.errors.append(G)
	@visit.register(BackendDict)
	def _(self,state_container:BackendDict):
		B=state_container;A=self
		if not A.pickle_encoder:return
		try:A.pickle_encoder.encodes(B)
		except Exception as C:D=StateSerializationError(service=A.service_name,state_container=B,exception=C,serialization_backend=_C);A.errors.append(D)
class StateSerializationErrorCollector:
	def __init__(A,service_manager:ServiceManager,with_pickle:bool=_B):A.service_manager=service_manager;A.pickle_enabled=with_pickle
	def try_serialize_state_containers(B,services:set[str])->StateSerializationTestResult:
		C=StateSerializationTestResult()
		for A in services.copy():
			E=B.service_manager.get_service(A)
			if not E:continue
			if supports_avro(A):D=AvroPicklingVisitor(A,with_pickle=B.pickle_enabled)
			elif B.pickle_enabled:D=PicklingVisitor(A)
			else:return C
			E.accept_state_visitor(D);C.errors.extend(D.errors)
		return C
class LocalstackStateContainerCollector(StateVisitor):
	stores:dict[str,type[BaseStore]];backends:dict[str,type[BaseBackend]]
	def __init__(A)->_A:A._stores={};A._backends={}
	@staticmethod
	def get_collector()->'LocalstackStateContainerCollector':return LocalstackStateContainerCollector()
	@contextmanager
	def _activate_pro(self):
		from localstack.pro.core import config as A;B=os.environ.get(ENV_PRO_ACTIVATED);C=A.ENABLE_DMS;os.environ[ENV_PRO_ACTIVATED]='1';A.ENABLE_DMS=_B
		try:yield
		finally:
			A.ENABLE_DMS=C
			if B:os.environ[ENV_PRO_ACTIVATED]=B
	def _collect_service(B,service_name:str,providers:list[str]):
		A=service_name
		if A in B._stores or A in B._backends:return
		if'pro'in providers:C=f"{A}:pro"
		else:C=f"{A}:default"
		D=SERVICE_PLUGINS.plugin_manager.load(C);D.service.accept_state_visitor(B);D.service.stop()
	def _collect_all_state_containers(A):
		with A._activate_pro():
			for(B,C)in sorted(SERVICE_PLUGINS.api_provider_specs.items()):A._collect_service(B,C)
	@singledispatchmethod
	def visit(self,state_container:t.Any):0
	@visit.register(AccountRegionBundle)
	def _(self,state_container:AccountRegionBundle):
		A=state_container
		if A is not _A:self._stores[A.service_name]=A.store
	@visit.register(BackendDict)
	def _(self,state_container:BackendDict):
		A=state_container
		if A is not _A:self._backends[A.service_name]=A.backend
	@staticmethod
	def collect_stores()->dict[str,type[BaseStore]]:
		A=LocalstackStateContainerCollector.get_collector()
		if not A._stores:A._collect_all_state_containers()
		return A._stores
	@staticmethod
	def collect_backends()->dict[str,type[BaseBackend]]:
		A=LocalstackStateContainerCollector.get_collector()
		if not A._backends:A._collect_all_state_containers()
		return A._backends
	@staticmethod
	def get_store_for_service(service_name:str)->type[BaseStore]|_A:
		A=service_name;B=LocalstackStateContainerCollector.get_collector()
		if B._stores and A in B._stores:return B._stores[A]
		if A not in SERVICE_PLUGINS.api_provider_specs:raise Exception(f"{A} is not a recognized and supported service")
		C=SERVICE_PLUGINS.api_provider_specs[A]
		with B._activate_pro():B._collect_service(A,C)
		return B._stores.get(A)