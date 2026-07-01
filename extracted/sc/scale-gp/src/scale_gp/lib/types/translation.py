from typing import Any, Dict, Union, Optional

from scale_gp import BaseModel


class TranslationTestCaseSchema(BaseModel):
    original_text: str
    language: Optional[str] = None
    expected_translation: Optional[str] = None
    other_inputs: Optional[Union[str, float, Dict[str, Any]]] = None
    other_expected: Optional[Union[str, float, Dict[str, Any]]] = None
