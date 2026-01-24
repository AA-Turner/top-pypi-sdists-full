from contextlib import suppress

import pytest

from tests.integ.utils import random_string

from snowflake.core.exceptions import NotFoundError
from snowflake.core.streamlit import (
    AddLiveVersionStreamlitRequest,
    CommitStreamlitRequest,
    Streamlit,
)


@pytest.mark.min_sf_ver("9.38.0")
def test_live_and_commit(streamlits, streamlit_stage_with_file, warehouse, streamlit_main_file):
    name = random_string(8, "test_streamlit_")
    st = Streamlit(
        name=name,
        query_warehouse=warehouse.name,
        source_location=f"@{streamlit_stage_with_file.name}",
        main_file=streamlit_main_file,
    )

    ref = streamlits.create(st)
    try:
        assert ref.fetch().live_version_location_uri is None
        ref.add_live_version(from_last=True, add_live_version_streamlit_request=AddLiveVersionStreamlitRequest())
        assert ref.fetch().live_version_location_uri is not None
        ref.commit(commit_streamlit_request=CommitStreamlitRequest())
        assert ref.fetch().live_version_location_uri is None
    finally:
        with suppress(NotFoundError):
            ref.drop()
