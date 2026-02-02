_A=None
from pathlib import Path
from typing import Tuple
from._protections.encryption import Encryption
from._protections.global_filter import GlobalFilter
from.exceptions import ProtectionException
from.protector_config import ProtectorConfig
from._protections import Protection
from._protections.obfuscation import Obfuscation
class Protector:
	def __init__(A):A.PROTECTIONS=_A
	def initialize(B,version:str,config:ProtectorConfig|_A=_A):A=config;C=A.get('global_filter')if A else _A;D=A.get('obfuscation')if A else _A;E=A.get('encryption')if A else _A;(B.PROTECTIONS):list[Protection]=[GlobalFilter(config=C),Obfuscation(config=D),Encryption(version,config=E)]
	def protect_file(C,source_path:Path,distribution_path:Path)->Tuple[Path,Path]:
		B=source_path;A=distribution_path
		if not C.PROTECTIONS:raise ProtectionException('Protections not yet initialized.')
		for D in C.PROTECTIONS:
			if D.should_protect(B,A):
				B,A=D.protect_file(B,A)
				if A is _A:break
		return B,A
	def finalize(A):
		for B in A.PROTECTIONS:B.finalize()