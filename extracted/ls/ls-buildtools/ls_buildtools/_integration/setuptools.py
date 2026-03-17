import shutil
from pathlib import Path
from ls_buildtools.protect import Protector
from ls_buildtools._integration import BUILDTOOLS_CONFIG_FILE
from ls_buildtools.protector_config import ProtectorConfig
from ls_buildtools.utilities import read_protector_config
try:
	from setuptools.command.sdist import sdist
	class ProtectionCommand(sdist):
		def make_release_tree(E,base_dir,files):
			A=base_dir;super().make_release_tree(A,files);print('Protecting files with LocalStack BuildTools protection...');A=Path(A);F=A/'setup.py';F.unlink();G:ProtectorConfig=read_protector_config(A/'..'/BUILDTOOLS_CONFIG_FILE);H=A/BUILDTOOLS_CONFIG_FILE;H.unlink(missing_ok=True);I=[A for A in A.rglob('*')if A.is_file()];J=[(A,A)for A in I];K=E.distribution.get_version();L=Protector.protect_files_parallel(J,K,G)
			for(C,M,B,D)in L:
				if D is not None:
					if B.absolute()!=C.absolute():C.unlink()
					if D.absolute()!=B.absolute():shutil.move(str(B.absolute()),str(D.absolute()))
				else:C.unlink();B.unlink(missing_ok=True)
except ImportError:pass