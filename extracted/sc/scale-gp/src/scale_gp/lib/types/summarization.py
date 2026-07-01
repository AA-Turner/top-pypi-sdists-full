from typing import Any, Dict, Union, Optional

from scale_gp import BaseModel


class SummarizationTestCaseSchema(BaseModel):
    document: str
    expected_summary: Optional[str]
    other_inputs: Optional[Union[str, float, Dict[str, Any]]] = None
    other_expected: Optional[Union[str, float, Dict[str, Any]]] = None
