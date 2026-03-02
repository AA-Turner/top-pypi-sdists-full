import argparse,fnmatch,os,shutil
from pathlib import Path
import yaml
from localstack_obfuscator.obfuscate import Obfuscator
CONFIG_FILE_NAME='obfuscator.yml'
def root_code_dir():return Path(__file__).resolve().parent
def mkdir(path):path.mkdir(parents=True,exist_ok=True)
def run(cmd):os.system(cmd)
def copy_target_code(src_dir,build_dir,target_dir_name,remove=None):
	D=remove;C=build_dir;A=src_dir;print(f"Copying target code from {A} to {C} while excluding patterns: {D}");B=C/target_dir_name;mkdir(B);G=[A.replace('\\','').replace('/*','')for A in D]or[]
	def E(current_dir,names):
		E=Path(current_dir);F=E.relative_to(A);D=[]
		for B in names:
			if E==A and B==C.name:D.append(B);continue
			H=(F/B).as_posix()if F.parts else B
			if any(fnmatch.fnmatch(H,A)for A in G):D.append(B);continue
		return D
	print(f"Copying {A} to {B} with Python copy");shutil.copytree(A,B,dirs_exist_ok=True,ignore=E);return B
def load_config(config_path):
	try:
		with config_path.open('r')as A:return yaml.safe_load(A)
	except FileNotFoundError:print(f"No {CONFIG_FILE_NAME} file found in target directory");return{}
def obfuscate(src_dir,config_file):
	F=False;B=src_dir;B=B.resolve();A=load_config(config_file);G=A.get('modify_in_place',F);H=B/A.get('build_dir','build');I=A.get('target_dir',B.name);J=A.get('minify',{});K=A.get('exclude',[]);L=A.get('remove',[])
	if G:C=B
	else:C=copy_target_code(B,H,I,remove=L)
	print(f"Starting obfuscation in {C}...");M=A.get('custom_patches',F);N=Obfuscator(M,J)
	for(O,Q,P)in os.walk(C):
		for D in P:
			if D in K or not D.endswith('.py'):continue
			E=Path(O)/D;print(f"Obfuscating {E}");N.obfuscate_file(E)
	print('Done!')
def main():A=argparse.ArgumentParser(description='Obfuscate LocalStack proprietary code base');A.add_argument('src_dir',type=str,help='Source directory to obfuscate');A.add_argument('--config',type=str,default=CONFIG_FILE_NAME,help='Configuration file');B=A.parse_args();obfuscate(Path(B.src_dir),Path(B.config))
if __name__=='__main__':main()