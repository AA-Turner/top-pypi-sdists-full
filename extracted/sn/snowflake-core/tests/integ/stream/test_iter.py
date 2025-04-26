from contextlib import suppress

import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.stream import Stream, StreamSourceTable
from tests.utils import random_string

from ...utils import ensure_snowflake_version


@pytest.fixture(scope='module')
def streams_extended(streams, src_temp_table, snowflake_version):
    ensure_snowflake_version(snowflake_version, "8.35.0")

    name_list = []
    for _ in range(5):
        name_list.append(random_string(10, 'test_stream_iter_a_'))
    for _ in range(7):
        name_list.append(random_string(10, 'test_stream_iter_b_'))
    for _ in range(3):
        name_list.append(random_string(10, 'test_stream_iter_c_'))

    for stream_name in name_list:
        streams.create(Stream(
            name=stream_name,
            stream_source=StreamSourceTable(
                name = src_temp_table.name,
            ),
            comment="ThIs iS a ComMeNT"
        ))

    try:
        yield streams
    finally:
        for stream_name in name_list:
            with suppress(NotFoundError):
                streams[stream_name].drop()

def test_iter_raw(streams_extended):
    assert len(list(streams_extended.iter())) >= 15


def test_iter_like(streams_extended):
    assert len(list(streams_extended.iter(like="test_stream_iter_"))) == 0
    assert len(list(streams_extended.iter(like="test_stream_iter_a_%%"))) == 5
    assert len(list(streams_extended.iter(like="test_stream_iter_b_%%"))) == 7
    assert len(list(streams_extended.iter(like="test_stream_iter_c_%%"))) == 3


def test_iter_show_limit(streams_extended):
    assert len(list(streams_extended.iter(like="test_stream_iter_a_%%"))) == 5
    assert len(list(streams_extended.iter(like="test_stream_iter_a_%%", show_limit=2))) == 2
    assert len(list(streams_extended.iter(show_limit=2))) == 2


def test_iter_starts_with(streams_extended):
    assert len(list(streams_extended.iter(starts_with="test_stream_iter_a_".upper()))) == 5


def test_iter_from_name(streams_extended):
    assert len(list(streams_extended.iter(from_name='test_stream_iter_b_'.upper(), show_limit=10000))) >= 10
    assert len(list(streams_extended.iter(from_name='test_stream_iter_b_'.upper(), show_limit=5))) <= 5

    # This should return all streams
    assert len(list(streams_extended.iter(from_name='test_stream_iter_b_'.upper()))) >= 15
    assert len(list(streams_extended.iter(from_name='test_stream_iter_b_', show_limit=10000))) == 0
