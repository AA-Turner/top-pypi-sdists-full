_A=None
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
	def __init__(A,*B:Any,**C:Any)->_A:super().__init__(*B,**C);A.builder_config=A.build_config;A.builder=A.builder_config.builder;A.protector=Protector();A.rename={}
	def initialize(A,version:str,build_data:dict[str,Any])->_A:
		B='exclude';A.app.display_info('Protecting files with LocalStack BuildTools protection...');G:ProtectorConfig=read_protector_config(Path(A.builder_config.root)/BUILDTOOLS_CONFIG_FILE);A.protector.initialize(A.builder.metadata.version,G)
		for C in A.builder.recurse_included_files():
			if not C.distribution_path:continue
			if C.distribution_path==BUILDTOOLS_CONFIG_FILE:
				if B not in A.builder.build_config:A.builder.build_config[B]=[]
				A.builder.build_config[B].append(f"**/{BUILDTOOLS_CONFIG_FILE}");continue
			F=Path(C.path);D=Path(C.distribution_path);A.app.display_info(f"- Protecting file: {F}");H,E=A.protector.protect_file(F,D)
			if E is not _A:build_data['force_include'][H]=E
			if D!=E:
				if B not in A.builder.build_config:A.builder.build_config[B]=[]
				A.builder.build_config[B].append(f"**/{str(D)}")
			del A.builder_config.exclude_spec
	def finalize(A,version:str,build_data:dict[str,Any],artifact_path:str)->_A:A.protector.finalize()