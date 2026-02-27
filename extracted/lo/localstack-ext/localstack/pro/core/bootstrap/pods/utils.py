def get_pod_name_and_version(pod_name:str)->tuple[str,int|None]:
	A=pod_name
	if':'not in A:return A,None
	C,D,B=A.rpartition(':')
	if B.isdigit():return C,int(B)
	return A,None