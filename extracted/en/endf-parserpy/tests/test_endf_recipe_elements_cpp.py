import pytest
from endf_parserpy import EndfParserCpp
from base_test_endf_recipe_elements import *


@pytest.fixture(scope="function")
def endf_parser():
    return EndfParserCpp(
        endf_format="test", ignore_send_records=True, ignore_missing_tpid=True
    )


def test_nested_indices_with_inconsistent_assignment(
    inconsistent_mf1_mt1_test_section, endf_parser
):
    with pytest.raises(RuntimeError):
        endf_dict = endf_parser.parse(inconsistent_mf1_mt1_test_section)
