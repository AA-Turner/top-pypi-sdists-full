_A=None
import multiprocessing,os,sys
from pathlib import Path
from typing import Tuple
from._protections.encryption import Encryption
from._protections.global_filter import GlobalFilter
from.exceptions import ProtectionException
from.protector_config import ProtectorConfig
from._protections import Protection
from._protections.obfuscation import Obfuscation
def _protect_file_worker(args:tuple[ProtectorConfig,Path,Path,str])->Tuple[Path,Path,Path,Path]:
	E,A,B,F=args;C=os.environ.get('LS_BUILDTOOLS_TEST_PID_FILE')
	if C:
		try:
			with open(C,'a')as G:G.write(f"{os.getpid()}\n")
		except Exception:pass
	D=Protector();D.initialize(version=F,config=E);print(f"- Protecting file: {A}");sys.stdout.flush();H,I=D.protect_file(A,B);return A,B,H,I
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
	@staticmethod
	def protect_files_parallel(files:list[Tuple[Path,Path]],version:str,config:ProtectorConfig)->list[Tuple[Path,Path,Path,Path]]:
		A=files
		if not A:return[]
		try:B=multiprocessing.get_context('fork')
		except ValueError:B=multiprocessing.get_context()
		try:C=os.process_cpu_count()or 1
		except AttributeError:C=os.cpu_count()or 1
		D=min(C,len(A))or 1;print(f"Parallelizing file protections among {D} workers.");E=[(config,A,B,version)for(A,B)in A]
		with B.Pool(processes=D)as F:G=F.map(_protect_file_worker,E)
		return G