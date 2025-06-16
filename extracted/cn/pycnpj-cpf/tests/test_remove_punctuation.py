import pytest

from pycnpj_cpf.core import remove_punctuation


@pytest.mark.unit
@pytest.mark.high
def test_positive_remove_punctuation_cnpj():
    """Positive test for function remove_punctuation on a cnpj."""
    assert remove_punctuation('50.822.716/0001-42') == '50822716000142'


@pytest.mark.unit
@pytest.mark.high
def test_positive_remove_punctuation_cpf():
    """Positive test for function remove_punctuation on a cpf."""
    assert remove_punctuation('256.152.150-89') == '25615215089'
