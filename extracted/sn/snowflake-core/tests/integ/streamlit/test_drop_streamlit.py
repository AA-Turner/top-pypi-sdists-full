import pytest

from tests.integ.utils import random_string

from snowflake.core.exceptions import NotFoundError
from snowflake.core.streamlit import Streamlit


@pytest.mark.min_sf_ver("9.38.0")
def test_drop(streamlits, streamlit_stage_with_file, warehouse, streamlit_main_file):
    name = random_string(8, "test_streamlit_")
    st = Streamlit(
        name=name,
        query_warehouse=warehouse.name,
        source_location=f"@{streamlit_stage_with_file.name}",
        main_file=streamlit_main_file,
    )

    ref = streamlits.create(st)
    ref.drop()

    with pytest.raises(NotFoundError):
        streamlits[name].fetch()

    # drop if exists shouldn't error
    streamlits[name].drop(if_exists=True)
