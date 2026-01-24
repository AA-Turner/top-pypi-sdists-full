import pytest

from tests.integ.utils import random_string

from snowflake.core.exceptions import NotFoundError
from snowflake.core.streamlit import Streamlit


@pytest.mark.min_sf_ver("9.38.0")
def test_undrop_streamlit(streamlits, streamlit_stage_with_file, warehouse, streamlit_main_file):
    name = random_string(8, "test_undrop_streamlit_")

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

    try:
        ref.undrop()

        fetched = ref.fetch()
        assert fetched.name.upper() == name.upper()
        assert fetched.last_version_details is not None
        assert fetched.last_version_details.source_location_uri.upper() == f"@{streamlit_stage_with_file.name}".upper()
        assert fetched.main_file.upper() == streamlit_main_file.upper()
        assert fetched.query_warehouse.upper() == warehouse.name.upper()

    finally:
        try:
            ref.drop()
        except Exception:
            pass
