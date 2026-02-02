_A=True
import os,re,shutil
from functools import cached_property
from pathlib import Path
from tempfile import mkdtemp,tempdir
from typing import Tuple
from..protector_config import EncryptionConfig
from.._protections import Protection
from..utilities import get_encryption_key
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
class Encryption(Protection):
	def __init__(A,version:str,config:EncryptionConfig|None=None):A.config=config or EncryptionConfig();A.version=version;A.encrypted_directory=Path(mkdtemp(dir=tempdir));A.AES_BLOCK_SIZE=16;A.exclude=[re.compile(A)for A in A.config.get('exclude_regexes',[])]
	def should_protect(A,source_path:Path,distribution_path:Path)->bool:
		C=source_path;B=False
		if not A.config.get('enabled',_A)or os.environ.get('LS_SKIP_ENCRYPTION','0')=='1':print(f"--- ! ENCRYPTION HAS EXPLICITLY BEEN DISABLED: {distribution_path} is NOT being encrypted! ! ---");return B
		if A.exclude and any(A.search(str(C))for A in A.exclude):return B
		if C.suffix!='.py':return B
		return _A
	@cached_property
	def cipher(self):A=get_encryption_key(self.version,keys_file=self.config.get('encryption_keys_file'));B=b'\x00'*16;return Cipher(algorithms.AES(A),modes.CBC(B))
	def protect_file(A,source_path:Path,distribution_path:Path)->Tuple[Path,Path]:
		B=distribution_path;C=A.encrypted_directory/B.with_name(f"{B.name}.enc");C.parent.mkdir(parents=_A,exist_ok=_A)
		with open(source_path,'rb')as G:D=G.read()
		D+=b'\x00'*(A.AES_BLOCK_SIZE-len(D)%A.AES_BLOCK_SIZE);E=A.cipher.encryptor();H=E.update(D)+E.finalize()
		with open(C,'w+b')as F:F.write(H);F.flush()
		I=B.with_name(f"{B.name}.enc");return C,I
	def finalize(A):shutil.rmtree(A.encrypted_directory)