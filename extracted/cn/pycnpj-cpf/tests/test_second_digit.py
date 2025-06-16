import pytest

from pycnpj_cpf.core import (
    second_digit_cnpj_checker_is_valid,
    second_digit_cpf_checker_is_valid,
)


@pytest.mark.unit
@pytest.mark.high
@pytest.mark.parametrize(
    'value',
    [
        '98803280278',
        '71858204054',
        '06982641007',
        '89219560003',
        '53683761032',
    ],
)
def test_positive_second_digit_cpf(value):
    """Test positive for function second_digit_cpf_checker_is_valid."""
    assert second_digit_cpf_checker_is_valid(value)


@pytest.mark.unit
@pytest.mark.high
@pytest.mark.parametrize(
    'value',
    [
        '97744421000169',
        '89420356000198',
        '50629870000100',
        '88506571000143',
        '35868665000104',
        '12.ABC.345/01DE-35',
        '12.2HI.345/01DE-40',
        'AB2YW3Z501DE69',
    ],
)
def test_positive_second_digit_cnpj(value):
    """Test positive for function second_digit_cnpj_checker_is_valid."""
    assert second_digit_cnpj_checker_is_valid(value)
