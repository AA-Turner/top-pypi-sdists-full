from typing import Union, Dict, List, Any


Any = Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]
"""
any.

Topic without validation (e.g. DLQs)
"""

