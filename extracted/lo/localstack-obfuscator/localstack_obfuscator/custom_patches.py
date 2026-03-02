import functools,inspect,types
from collections.abc import Callable
from typing import Any
def get_defining_object(method):
	A=method
	if inspect.ismethod(A):return A.__self__
	if inspect.isfunction(A):
		C=A.__qualname__.split('.<locals>',1)[0].rsplit('.',1)[0]
		try:B=getattr(inspect.getmodule(A),C)
		except AttributeError:B=A.__globals__.get(C)
		if isinstance(B,type):return B
	return inspect.getmodule(A)
def create_patch_proxy(target,new):
	A=target
	@functools.wraps(A)
	def B(*B,**D):
		if C:B=B[1:]
		return new(A,*B,**D)
	C=inspect.ismethod(A)
	if C:B=types.MethodType(B,A.__self__)
	return B
class Patch:
	obj:0;name:0;new:0;old:0;is_applied:0
	def __init__(A,obj,name,new):super().__init__();A.obj=obj;A.name=name;A.old=getattr(A.obj,name);A.new=new;A.is_applied=False
	def apply(A):setattr(A.obj,A.name,A.new);A.is_applied=True
	def undo(A):setattr(A.obj,A.name,A.old);A.is_applied=False
	def __enter__(A):A.apply();return A
	def __exit__(A,exc_type,exc_val,exc_tb):A.undo();return A
	@staticmethod
	def function(target,fn,pass_target=True):
		C=target;A=fn;B=get_defining_object(C);D=C.__name__;F=not inspect.isclass(B)and not inspect.ismodule(B)
		if F:A.__name__=D;A=types.MethodType(A,B)
		if pass_target:E=create_patch_proxy(C,A)
		else:E=A
		return Patch(B,D,E)
def patch(target,pass_target=True):
	def A(fn):fn.patch=Patch.function(target,fn,pass_target=pass_target);fn.patch.apply();return fn
	return A