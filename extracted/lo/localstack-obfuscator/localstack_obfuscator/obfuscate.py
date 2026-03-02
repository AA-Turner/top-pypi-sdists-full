from pathlib import Path
import python_minifier
from localstack_obfuscator.custom_patches import patch
class Obfuscator:
	def __init__(A,custom_patches,minify_config):
		A.minify_config=minify_config
		if custom_patches:A._apply_custom_patches()
	def _apply_custom_patches(E):
		D=True;import ast as A;from python_minifier.ast_annotation import get_parent as C;from python_minifier.transforms.remove_annotations import RemoveAnnotations as B
		if not hasattr(B.visit_AnnAssign,'_ls_patched'):
			def F(node):
				F=False;E=node
				if not isinstance(C(E),A.ClassDef):return F
				if len(C(E).bases)==0:return F
				G=['NamedTuple','TypedDict','BaseModel']
				for B in C(E).bases:
					if isinstance(B,A.Name)and B.id in G:return D
					elif isinstance(B,A.Attribute)and B.attr in G:return D
				return F
			@patch(B.visit_AnnAssign)
			def G(fn,self,node):
				E='annotation';B=node
				if F(B):return B
				if isinstance(B,A.AnnAssign):
					D=getattr(B,E,None);C=fn(self,B);G=getattr(C,E,None)
					if isinstance(G,A.Constant)and isinstance(D,A.Subscript|A.Name|A.BinOp):C.annotation=D
					return C
				return fn(self,B)
			B.visit_AnnAssign._ls_patched=D
	def obfuscate_file(A,src_file_path,target_file_path=None):B=src_file_path;C=python_minifier.minify(Obfuscator.load_file(B),**A.minify_config);A.save_file(target_file_path or B,C)
	@staticmethod
	def load_file(path):
		with path.open('r')as A:return A.read()
	@staticmethod
	def save_file(path,content):
		with path.open('w')as A:return A.write(content)