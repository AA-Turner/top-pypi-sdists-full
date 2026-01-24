_L='Summary'
_K='--disable-pip-version-check'
_J='--no-color'
_I='--no-input'
_H='extension'
_G='name'
_F='pip'
_E=None
_D='log'
_C='status'
_B='message'
_A='event'
import inspect,logging,os,subprocess
from collections.abc import Generator
from pathlib import Path
from typing import Any,Literal,TypedDict
from localstack import config,constants
from localstack.utils.objects import singleton_factory
from localstack.utils.venv import VirtualEnvironment
from plux import PluginManager
LOG=logging.getLogger(__name__)
LOCALSTACK_VENV=VirtualEnvironment(constants.LOCALSTACK_VENV_FOLDER)
VENV_DIRECTORY='extensions/python_venv'
def get_extensions_venv()->VirtualEnvironment:return VirtualEnvironment(os.path.join(config.dirs.var_libs,VENV_DIRECTORY))
@singleton_factory
def get_extension_repository()->'ExtensionsRepository':return ExtensionsRepository(init_extension_venv())
def init_extension_venv()->VirtualEnvironment:
	A=get_extensions_venv()
	if not A.exists:LOG.info('initializing extension environment at %s',A.venv_dir);A.create();LOG.debug('adding localstack venv path %s to %s',LOCALSTACK_VENV,A.venv_dir);A.add_pth('localstack-venv',LOCALSTACK_VENV)
	return A
def list_extension_metadata()->list[dict]:from localstack.extensions.api import Extension as A;return list_plugin_distribution_data(PluginManager(A.namespace))
def list_plugin_distribution_data(plugin_manager:PluginManager)->list[dict]:
	C=[]
	for A in plugin_manager.list_containers():
		try:D=A.distribution
		except ValueError:continue
		except Exception as F:LOG.error('Error while resolving distribution for plugin %s: %s. This probably means that the package was removed or otherwise changed after the plugin was loaded. Restarting LocalStack should fix the issue.',A.name,F);continue
		if not D:continue
		E=A.plugin_spec;B=inspect.getmodule(A.plugin_spec.factory);G={'namespace':E.namespace,_G:A.name,'factory':{'module':str(B.__name__),'code':f"{B.__name__}.{E.factory.__name__}",'file':str(B.__file__)},'distribution':D.metadata.json};C.append(G)
	return C
class InstallerEvent(TypedDict,total=False):event:Literal[_C,_D,'error','exception',_F,_H];message:str;extra:dict[str,Any]|_E
class ExtensionsRepository:
	venv:VirtualEnvironment
	def __init__(A,venv:VirtualEnvironment=_E):A.venv=venv or get_extensions_venv();A.venv.inject_to_sys_path()
	@property
	def pip(self)->Path:
		A=self.venv.venv_dir/'bin'/_F
		if not A.exists():raise FileNotFoundError(f"pip is not available at {self.pip}")
		return A
	def pip_show(A,package:str)->dict|_E:
		B=[A.pip,'show',package]
		try:C=subprocess.check_output(B,stderr=subprocess.STDOUT,text=True);return dict(A.split(': ',maxsplit=1)for A in C.splitlines())
		except subprocess.CalledProcessError as D:
			if'not found'in D.output:return
			raise
	def run_install(C,name_or_url:str)->Generator[InstallerEvent,_E,_E]:
		B=name_or_url;G=[C.pip,_I,_J,_K,'install',B];yield{_A:_C,_B:'Checking installed extensions'};A=C.pip_show(B)
		if A:H=A['Name'];I=A[_L];J=A['Author'];yield{_A:_D,_B:f"Extension {H} ({I} by {J}) already installed"};return
		_clear_plugin_cache();K={A[_G]:A for A in list_extension_metadata()};yield{_A:_C,_B:'Installing extension'};D=False
		try:
			with SubprocessLineStream.open(G)as L:
				for E in L:
					yield{_A:_F,_B:E}
					if'No matching distribution found for'in E:D=True;yield{_A:'error',_B:f"Could not resolve package {B}, please check the URL or that the package exists in pypi."}
		except subprocess.CalledProcessError:
			if D:return
			raise
		_clear_plugin_cache();M={A[_G]:A for A in list_extension_metadata()};F=[B for(A,B)in M.items()if A not in K]
		if F:
			yield{_A:_D,_B:'Extension successfully installed'}
			for N in F:yield{_A:_H,_B:'','extra':N}
		else:yield{_A:_D,_B:'No change'}
		yield{_A:_C,_B:'Extension installation completed'}
	def run_uninstall(C,package:str)->Generator[InstallerEvent,_E,_E]:
		A=package;D=[C.pip,_I,_J,_K,'uninstall','-y',A];yield{_A:_C,_B:'Checking extensions'};B=C.pip_show(A)
		if not B:yield{_A:_D,_B:f"Extension {A} is not installed"};return
		E=B['Name'];F=B[_L];yield{_A:_D,_B:f"Uninstalling extension {E} ({F})"};yield{_A:_C,_B:'Uninstalling extension'}
		with SubprocessLineStream.open(D)as G:
			for H in G:yield{_A:_F,_B:H}
		yield{_A:_D,_B:'Extension successfully uninstalled'};_clear_plugin_cache();yield{_A:_C,_B:'Extension uninstall completed'}
class SubprocessLineStream:
	default_timeout:int=5
	def __init__(A,process:subprocess.Popen):A.process=process
	def __iter__(A):return A._gen()
	def _gen(A):
		C=A.process.stdout
		if A.process.text_mode:B='\r\n'
		else:B=b'\r\n'
		for D in C:yield D.rstrip(B)
		if A.process.wait(A.default_timeout)!=0:raise subprocess.CalledProcessError(returncode=A.process.returncode,cmd=A.process.args)
	def __enter__(A):return A
	def __exit__(A,exc_type,exc_val,exc_tb):A.close()
	def close(A):A.process.terminate()
	@classmethod
	def open(A,cmd,*B,**C):return A(subprocess.Popen(cmd,*B,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,**C))
def _clear_plugin_cache():
	from plux.runtime.cache import EntryPointsCache as B;from plux.runtime.metadata import packages_distributions as C;A=B.instance()
	with A._lock:A._cache.clear()
	C.cache_clear()