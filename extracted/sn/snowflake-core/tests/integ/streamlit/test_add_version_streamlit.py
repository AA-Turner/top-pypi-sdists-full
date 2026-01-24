import pytest

from tests.integ.utils import random_string

from snowflake.core.streamlit import (
    AddVersionStreamlitRequest,
    AddVersionStreamlitRequestVersion,
    Streamlit,
)


@pytest.mark.min_sf_ver("9.38.0")
def test_add_version_streamlit(streamlits, streamlit_stage_with_file, warehouse, streamlit_main_file):
    name = random_string(8, "test_add_version_streamlit_")

    st = Streamlit(
        name=name,
        query_warehouse=warehouse.name,
        source_location=f"@{streamlit_stage_with_file.name}",
        main_file=streamlit_main_file,
    )

    ref = streamlits.create(st)
    try:
        version_name = random_string(8, "version_")
        version = AddVersionStreamlitRequestVersion(
            name=version_name,
            comment="Test version for integration testing",
            if_not_exists=True,
        )

        add_version_request = AddVersionStreamlitRequest(
            source_location=f"@{streamlit_stage_with_file.name}",
            version=version,
        )

        ref.add_version(add_version_request)

        fetched = ref.fetch()
        assert fetched.name.upper() == name.upper()
        assert fetched.last_version_details is not None
        assert fetched.last_version_details.name is not None
        assert fetched.last_version_details.alias.upper() == version_name.upper()
        assert fetched.last_version_details.source_location_uri.upper() == f"@{streamlit_stage_with_file.name}".upper()

    finally:
        ref.drop()
