_B=True
_A=False
import os,re,shutil
from pathlib import Path
from tempfile import mkdtemp,tempdir
from typing import Tuple
from localstack_obfuscator.obfuscate import Obfuscator
from.import Protection
from..protector_config import ObfuscationConfig
class Obfuscation(Protection):
	def __init__(A,config:ObfuscationConfig|None=None):A.config=config or ObfuscationConfig(custom_patches=_A,remove_annotations=_B,remove_literal_statements=_B);A.exclude=[re.compile(A)for A in A.config.get('exclude_regexes',[])];A.minified_directory=Path(mkdtemp(dir=tempdir));B=A.config.get('custom_patches',_A);C={B:A.config.get(B,None)for B in('remove_annotations','remove_literal_statements')};A.obfuscator=Obfuscator(B,C)
	def should_protect(A,source_path:Path,distribution_path:Path)->bool:
		B=source_path
		if os.environ.get('LS_SKIP_OBFUSCATION','0')=='1':print(f"--- ! OBFUSCATION HAS EXPLICITLY BEEN DISABLED: {distribution_path} is NOT being obfuscated! ! ---");return _A
		if A.exclude and any(A.search(str(B))for A in A.exclude):return _A
		if B.suffix!='.py':return _A
		return _B
	def protect_file(B,source_path:Path,distribution_path:Path)->Tuple[Path,Path]:C=distribution_path;A=Path(B.minified_directory)/C;A.parent.mkdir(parents=_B,exist_ok=_B);B.obfuscator.obfuscate_file(source_path,A);return A,C
	def finalize(A):shutil.rmtree(A.minified_directory)