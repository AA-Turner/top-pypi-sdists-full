import pytest

from tests.integ.utils import random_string

from snowflake.core.streamlit import Streamlit


pytestmark = [pytest.mark.min_sf_ver("9.38.0")]


@pytest.fixture(scope="module")
def streamlits_extended(streamlits, streamlit_stage_with_file, warehouse, streamlit_main_file):
    names_list = []

    for _ in range(5):
        names_list.append(random_string(10, "test_streamlit_iter_a_"))

    for _ in range(7):
        names_list.append(random_string(10, "test_streamlit_iter_b_"))

    for _ in range(3):
        names_list.append(random_string(10, "test_streamlit_iter_c_"))

    try:
        for name in names_list:
            st = Streamlit(
                name=name,
                query_warehouse=warehouse.name,
                source_location=f"@{streamlit_stage_with_file.name}",
                main_file=streamlit_main_file,
            )
            streamlits.create(st)

        yield streamlits
    finally:
        for name in names_list:
            streamlits[name].drop(if_exists=True)


def test_iter_raw(streamlits_extended):
    assert len(list(streamlits_extended.iter())) >= 15


def test_iter_like(streamlits_extended):
    assert len(list(streamlits_extended.iter(like="test_streamlit_iter_a_%"))) == 5
    assert len(list(streamlits_extended.iter(like="test_streamlit_iter_b_%"))) == 7
    assert len(list(streamlits_extended.iter(like="test_streamlit_iter_c_%"))) == 3
    assert len(list(streamlits_extended.iter(like="TEST_STREAMLIT_ITER_C_%"))) == 3
    assert len(list(streamlits_extended.iter(like="nonexistent_pattern_%"))) == 0


def test_iter_limit(streamlits_extended):
    assert len(list(streamlits_extended.iter(limit=2))) == 2


def test_iter_starts_with(streamlits_extended):
    assert len(list(streamlits_extended.iter(starts_with="test_streamlit_iter_a_".upper()))) == 5
    assert len(list(streamlits_extended.iter(starts_with="test_streamlit_iter_a_"))) == 0
    assert len(list(streamlits_extended.iter(starts_with="test_streamlit_iter_d_".upper()))) == 0


def test_iter_from_name(streamlits_extended):
    streamlits_from_b = list(streamlits_extended.iter(limit=20, from_name="TEST_STREAMLIT_ITER_B_"))
    assert len(streamlits_from_b) == 10
