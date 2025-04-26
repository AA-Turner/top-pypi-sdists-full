import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.stream import Stream, StreamSourceTable
from tests.utils import random_string


@pytest.mark.min_sf_ver("8.35.0")
def test_drop(streams, src_temp_table):
    stream_name = random_string(10, 'test_stream_')

    stream_handle = streams.create(Stream(
        name=stream_name,
        stream_source=StreamSourceTable(
            name = src_temp_table.name,
        ),
        comment="ThIs iS a ComMeNT"
    ))


    stream_handle.drop()

    with pytest.raises(
        NotFoundError
    ):
        stream_handle.drop()

    stream_handle.drop(if_exists=True)
