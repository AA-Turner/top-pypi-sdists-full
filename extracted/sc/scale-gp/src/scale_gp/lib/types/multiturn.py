from typing import Any, Dict, List, Union, Optional

from scale_gp import BaseModel
from scale_gp.types.evaluation_datasets import FlexibleMessageParam


class MultiturnTestCaseSchema(BaseModel):
    messages: List[FlexibleMessageParam]
    turns: Optional[List[int]] = None
    expected_messages: Optional[List[FlexibleMessageParam]] = None
    other_inputs: Optional[Union[str, float, Dict[str, Any]]] = None
    other_expected: Optional[Union[str, float, Dict[str, Any]]] = None
