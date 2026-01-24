_A=None
import dataclasses,pytest
from _pytest.config import Config
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from localstack.aws.chain import Handler
from localstack.services.plugins import SERVICE_PLUGINS,ServiceManager
from localstack.state import StateContainer,StateVisitor,pickle
from localstack.utils.objects import singleton_factory
from pluggy import Result
from pytest import Item
class StoreSerializationCheckerPlugin:
	@pytest.hookimpl()
	def pytest_configure(self,config:Config):from localstack.aws.handlers import serve_custom_service_request_handlers as A;from localstack.pro.core.persistence.pickling import reducers as B;B.register();A.append(get_dirty_marker_handler());config.addinivalue_line('markers','skip_store_check(reason=None): skip the store serialization check')
	@pytest.hookimpl(hookwrapper=True)
	def pytest_runtest_call(self,item:Item)->_A:
		C:CallInfo=(yield)
		if C.excinfo:return
		if item.get_closest_marker('skip_store_check'):return
		D=PicklingErrorCollector(SERVICE_PLUGINS);A=get_dirty_marker_handler();B=D.try_pickle_state_containers(A.dirty);A.clear()
		if B.errors:raise PicklingTestException(B)
	@pytest.hookimpl(hookwrapper=True)
	def pytest_runtest_makereport(self,item:Item,call:CallInfo[_A])->TestReport|_A:
		A=call;C:Result=(yield);B:TestReport=C.get_result()
		if A.excinfo is not _A and isinstance(A.excinfo.value,PicklingTestException):D:PicklingTestException=A.excinfo.value;B.longrepr='\n'.join([str(A)for A in D.result.errors])
		return B
@singleton_factory
def get_dirty_marker_handler():return DirtyMarkerHandler()
@dataclasses.dataclass
class PicklingError:service:str;state_container:StateContainer;exception:Exception
class PicklingTestResult:
	errors:list[PicklingError]
	def __init__(A):A.errors=[]
class PicklingTestException(Exception):
	result:PicklingTestResult
	def __init__(A,result:PicklingTestResult):super().__init__();A.result=result
class DirtyMarkerHandler(Handler):
	dirty:set[str]
	def __init__(A):A.dirty=set()
	def __call__(B,chain,context,response):
		A=context
		if not A.service:return
		B.dirty.add(A.service.service_name)
	def clear(A):A.dirty.clear()
class PicklingVisitor(StateVisitor):
	errors:list[PicklingError]
	def __init__(A,service:str):A.errors=[];A.service=service
	def visit(A,state_container:StateContainer):
		B=state_container
		try:pickle.dumps(B)
		except Exception as C:A.errors.append(PicklingError(A.service,B,C))
class PicklingErrorCollector:
	def __init__(A,service_manager:ServiceManager):A.service_manager=service_manager
	def try_pickle_state_containers(E,services:set[str])->PicklingTestResult:
		A=PicklingTestResult()
		for B in services.copy():
			C=E.service_manager.get_service(B)
			if not C:continue
			D=PicklingVisitor(B);C.accept_state_visitor(D);A.errors.extend(D.errors)
		return A