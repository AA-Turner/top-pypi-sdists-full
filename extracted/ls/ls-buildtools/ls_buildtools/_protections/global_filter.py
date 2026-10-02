_A=None
import re
from pathlib import Path
from typing import Tuple
from..protector_config import GlobalFilterConfig
from.._protections import Protection
class GlobalFilter(Protection):
	def __init__(A,config:GlobalFilterConfig|_A=_A):A.config=config or GlobalFilterConfig();A.remove_regexes=[re.compile(A)for A in A.config.get('remove_regexes',[])]
	def should_protect(A,source_path:Path,distribution_path:Path)->bool:return True
	def protect_file(B,source_path:Path,distribution_path:Path)->Tuple[Path,Path|_A]:
		A=source_path
		if B.remove_regexes and any(B.search(str(A))for B in B.remove_regexes):return A,_A
		return A,distribution_path