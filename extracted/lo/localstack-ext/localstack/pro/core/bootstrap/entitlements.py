_A=None
import fnmatch
from collections.abc import Iterable,Iterator
from typing import Any,TypedDict
from localstack.utils.numbers import to_number
class ProductInfo(TypedDict):name:str;version:str;metadata:dict[str,Any]|_A
class ProductEntitlements:
	def __init__(A,products:Iterable[ProductInfo],allow_all:bool=False):A._products=list(products);A._allow_all=allow_all
	def __contains__(A,entitlement:str)->bool:return A.has_entitlement(entitlement)
	def __iter__(A)->Iterator[ProductInfo]:return iter(A._products)
	def has_entitlement(A,entitlement:str)->bool:
		if A._allow_all:return True
		return A._get_product_info(entitlement,pattern_matching=True)is not _A
	def get_entitlement_limit(C,entitlement:str,default:int|float|_A=_A)->int|float|_A:
		A=default;D=C._get_product_info(entitlement)
		if not D:return A
		E=C._get_metadata(D)
		if E is _A:return A
		F=E.get('limit')
		if F is _A:return A
		try:B=to_number(F)
		except Exception:return A
		if B is _A or isinstance(B,bool):return A
		return B
	def _get_product_info(D,entitlement:str,pattern_matching:bool=False)->ProductInfo|_A:
		C=entitlement
		for B in D._products:
			A=B.get('name')
			if not A:continue
			A=str(A)
			if'*'in A and pattern_matching:
				if fnmatch.fnmatch(C,A):return B
			elif A==C:return B
	def _get_metadata(B,product:ProductInfo)->dict[str,Any]|_A:
		A=product.get('metadata')
		if A is _A or not isinstance(A,dict):return
		return A