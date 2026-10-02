import json,os
from pathlib import Path
from.exceptions import ProtectionException
from.protector_config import ProtectorConfig
def load_file(file_path:Path)->bytes:
	with file_path.absolute().open(mode='rb')as A:return A.read()
def save_file(path:Path,content:str)->int:
	with path.absolute().open(mode='w')as A:return A.write(content)
def get_encryption_keys_config(keys_file:str|None)->dict[str,str]:
	A=keys_file
	if A and os.path.exists(A):B=load_file(Path(A));return json.loads(B)
	if(C:=os.environ.get('LOCALSTACK_ENCRYPTION_KEYS')):return json.loads(C)
	D=f"in either file={A} or "if A else'';raise ProtectionException(f"Unable to find encryption keys {D}using env var 'LOCALSTACK_ENCRYPTION_KEYS'")
def get_encryption_key(version:str,keys_file:str|None=None)->bytes:
	C='.';A=version;D=get_encryption_keys_config(keys_file)
	if len(A.split(C))>3:A=C.join(A.split(C)[0:3])
	B=D.get(A)
	if B:return B.encode()
	E=C.join(A.split(C)[0:2]);B=D.get(E)
	if B:return B.encode()
	raise ProtectionException(f"Unable to find encryption key for version={A}")
def read_protector_config(toml_path:Path)->ProtectorConfig:
	try:import tomllib as A
	except ModuleNotFoundError:import tomli as A
	with toml_path.open(mode='rb')as B:return A.load(B)