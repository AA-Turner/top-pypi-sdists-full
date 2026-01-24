import pytest

from tests.integ.utils import random_string

from snowflake.core.exceptions import NotFoundError
from snowflake.core.streamlit import Streamlit


pytestmark = [pytest.mark.min_sf_ver("9.38.0")]


def test_rename(streamlits, streamlit_stage_with_file, warehouse, streamlit_main_file):
    original_name = random_string(10, "test_original_streamlit_")
    new_name = random_string(10, "test_renamed_streamlit_")

    st = Streamlit(
        name=original_name,
        query_warehouse=warehouse.name,
        source_location=f"@{streamlit_stage_with_file.name}",
        main_file=streamlit_main_file,
    )

    streamlit_handle = streamlits.create(st)
    try:
        fetched_streamlit = streamlit_handle.fetch()
        assert fetched_streamlit.name.upper() == original_name.upper()

        streamlit_handle.rename(new_name)

        fetched_after_rename = streamlits[new_name].fetch()
        assert fetched_after_rename.name.upper() == new_name.upper()
        assert fetched_after_rename.database_name.upper() == streamlits.database.name.upper()
        assert fetched_after_rename.schema_name.upper() == streamlits.schema.name.upper()

        with pytest.raises(NotFoundError):
            streamlits[original_name].fetch()
    finally:
        streamlits[new_name].drop(if_exists=True)


def test_rename_nonexistent_streamlit(streamlits):
    """Test renaming a non-existent streamlit raises NotFoundError."""
    nonexistent_name = random_string(10, "test_nonexistent_streamlit_")
    new_name = random_string(10, "test_new_name_streamlit_")

    with pytest.raises(NotFoundError):
        streamlits[nonexistent_name].rename(new_name)

    streamlits[nonexistent_name].rename(new_name, if_exists=True)


def test_rename_streamlit_cross_schema(
    streamlits, streamlit_stage_with_file, warehouse, streamlit_main_file, temp_schema
):
    """Test renaming streamlit across schemas."""
    original_name = random_string(10, "test_cross_schema_streamlit_")
    new_name = random_string(10, "test_renamed_cross_schema_streamlit_")

    st = Streamlit(
        name=original_name,
        query_warehouse=warehouse.name,
        source_location=f"@{streamlit_stage_with_file.database.name}.{streamlit_stage_with_file.schema.name}.{streamlit_stage_with_file.name}",
        main_file=streamlit_main_file,
    )

    streamlit_handle = streamlits.create(st)
    original_db_name = streamlit_handle.database.name
    try:
        streamlit_handle.rename(
            new_name,
            target_schema=temp_schema.name,
            target_database=original_db_name,
        )

        fetched_streamlit = streamlit_handle.fetch()
        assert fetched_streamlit.name.upper() == new_name.upper()
        assert fetched_streamlit.schema_name.upper() == temp_schema.name.upper()
        assert fetched_streamlit.database_name.upper() == original_db_name.upper()

        with pytest.raises(NotFoundError):
            streamlits[original_name].fetch()
    finally:
        streamlit_handle.drop(if_exists=True)
