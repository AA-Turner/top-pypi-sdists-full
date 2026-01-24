from localstack.aws.protocol import service_router as localstack_service_router
from localstack.aws.spec import ServiceModelIdentifier
from localstack.utils.patch import patch
def patch_service_router():
	from collections.abc import Callable as A
	@patch(localstack_service_router.custom_signing_name_rules)
	def B(fn:A,signing_name:str,path:str,**C)->ServiceModelIdentifier|None:
		B='rds';A=signing_name
		if A in[B,'docdb','neptune']:return ServiceModelIdentifier(B)
		return fn(A,path,**C)
	@patch(localstack_service_router.custom_host_addressing_rules)
	def C(fn:A,host:str,**A)->ServiceModelIdentifier|None:
		if'mediastore-'in host:return ServiceModelIdentifier('mediastore-data')
		return fn(host,**A)