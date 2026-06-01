_A='exclude'
from pathlib import Path
from typing import Any
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from hatchling.plugin import hookimpl
from.import BUILDTOOLS_CONFIG_FILE
from..protect import Protector
from..protector_config import ProtectorConfig
from..utilities import read_protector_config
@hookimpl
def hatch_register_build_hook():return HatchlingProtectionHook
class HatchlingProtectionHook(BuildHookInterface):
	PLUGIN_NAME='ls_buildtools'
	def __init__(A,*B:Any,**C:Any)->None:super().__init__(*B,**C);A.builder_config=A.build_config;A.builder=A.builder_config.builder;A.protector=Protector();A.rename={}
	def _get_exclude_config(A)->dict[str,Any]:
		if _A in A.builder_config.target_config:return A.builder_config.target_config
		return A.builder.build_config
	def initialize(A,version:str,build_data:dict[str,Any])->None:
		A.app.display_info('Protecting files with LocalStack BuildTools protection...');F:ProtectorConfig=read_protector_config(Path(A.builder_config.root)/BUILDTOOLS_CONFIG_FILE);G=A.builder.metadata.version;A.protector.initialize(version=G,config=F);H=[]
		for C in A.builder.recurse_included_files():
			if not C.distribution_path:continue
			if C.distribution_path==BUILDTOOLS_CONFIG_FILE:
				B=A._get_exclude_config()
				if _A not in B:B[_A]=[]
				B[_A].append(f"**/{BUILDTOOLS_CONFIG_FILE}");continue
			I=Path(C.path);D=Path(C.distribution_path);H.append((I,D))
		J=Protector.protect_files_parallel(H,G,F)
		for(I,D,K,E)in J:
			if E is not None:build_data['force_include'][K]=E
			if D!=E:
				B=A._get_exclude_config()
				if _A not in B:B[_A]=[]
				B[_A].append(f"**/{str(D)}")
		if hasattr(A.builder_config,'exclude_spec'):del A.builder_config.exclude_spec