import multiprocessing,os,sys
from pathlib import Path
import shutil
from ls_buildtools.protect import Protector
from ls_buildtools._integration import BUILDTOOLS_CONFIG_FILE
from ls_buildtools.protector_config import ProtectorConfig
from ls_buildtools.utilities import read_protector_config
def _protect_file_worker(args:tuple[ProtectorConfig,Path,str]):
	E,A,F=args;D=Protector();D.initialize(version=F,config=E);print(f"- Protecting file: {A}");sys.stdout.flush();B,C=D.protect_file(A,A)
	if C is not None:
		if B.absolute()!=A.absolute():A.unlink()
		if C.absolute()!=B.absolute():shutil.move(str(B.absolute()),str(C.absolute()))
	else:A.unlink();B.unlink(missing_ok=True)
try:
	from setuptools.command.sdist import sdist
	class ProtectionCommand(sdist):
		def make_release_tree(E,base_dir,files):
			A=base_dir;super().make_release_tree(A,files);print('Protecting files with LocalStack BuildTools protection...');A=Path(A);F=A/'setup.py';F.unlink();G:ProtectorConfig=read_protector_config(A/'..'/BUILDTOOLS_CONFIG_FILE);H=A/BUILDTOOLS_CONFIG_FILE;H.unlink(missing_ok=True);B=[A for A in A.rglob('*')if A.is_file()]
			try:C=multiprocessing.get_context('fork')
			except ValueError:C=multiprocessing.get_context()
			try:D=os.process_cpu_count()or 1
			except AttributeError:D=os.cpu_count()or 1
			I=min(D,len(B))or 1;J=E.distribution.get_version();K=[(G,A,J)for A in B]
			with C.Pool(processes=I)as L:L.map(_protect_file_worker,K)
except ImportError:pass