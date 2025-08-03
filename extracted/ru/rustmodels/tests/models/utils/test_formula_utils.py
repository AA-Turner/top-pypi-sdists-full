import rustmodels
import pytest
from typing import Optional

@pytest.mark.parametrize("formula_str, expected_result_str, expected_error, error_message_pattern", [
    ('y~x1+x2', "y ~ 1 + x1 + x2", None, None),
    ('y~0 + x1+x2', "y ~ x1 + x2", None, None),
    ('y~-x2 + x1+x2', "y ~ 1 + x1", None, None),
    ('y~x1*x2', "y ~ 1 + x1 + x2 + x1:x2", None, None),
    ('y~x1:x2 + 0', "y ~ x1:x2", None, None),
    ('y~x1 + x2 + 5', "y ~ 1 + x1 + x2", None, None),
    ('y~0 + x1 + x1 + x1 + x3', "y ~ x1 + x3", None, None),
    ('y ~ -x1 + x2 + 5', "y ~ 1 + x2", None, None),
    
    # Error cases
    ('', None, ValueError, r"Formula cannot be empty"),
    ('y x1 + x2', None, ValueError, r"Formula must contain '~' to separate dependent and independent variables"),
    ('y ~~~~', None, ValueError, r"Formula cannot contain multiple '~' characters"),
    (' ~ x1 + x2', None, ValueError, r"Dependent variable cannot be empty"),
    ('y ~ ', None, ValueError, r"Independent variables cannot be empty"),
    ('y ~ x1*x2*x3', None, ValueError, r"Invalid term found in formula:")
])
def test_parse_formula(
    formula_str, 
    expected_result_str: Optional[str],
    expected_error: Optional[Exception],
    error_message_pattern: Optional[str]
):
    if expected_error and error_message_pattern:
        with pytest.raises(expected_error, match=error_message_pattern):
            rustmodels._parse_formula(formula_str)
        return

    parsed_formula = rustmodels._parse_formula(formula_str)
    assert str(parsed_formula) == expected_result_str


