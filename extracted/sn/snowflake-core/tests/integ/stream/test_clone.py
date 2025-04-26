
import pytest

from snowflake.core import Clone
from snowflake.core.schema import Schema
from snowflake.core.stream import Stream, StreamSourceTable
from tests.utils import random_string

from ...utils import ensure_snowflake_version


@pytest.fixture
def temp_stream(streams, src_temp_table, snowflake_version):
    ensure_snowflake_version(snowflake_version, "8.37.0")

    stream_name = random_string(10, 'test_stream_')
    stream_handle = streams.create(Stream(
        name=stream_name,
        stream_source=StreamSourceTable(
            name = src_temp_table.name,
        ),
        comment="ThIs iS a ComMeNT"
    ))

    try:
        yield stream_handle
    finally:
        streams[stream_name].drop()


def test_clone(streams, temp_stream):
    stream_name = random_string(10, 'test_stream_clone_')

    cloned_stream = streams.create(stream_name,
        clone_stream=temp_stream.name
    )

    try:
        cloned_handle = cloned_stream.fetch()
        assert isinstance(temp_stream.fetch().stream_source, type(cloned_handle.stream_source))
        assert temp_stream.fetch().stream_source.name == cloned_handle.stream_source.name
        assert cloned_handle.comment == "ThIs iS a ComMeNT"
    finally:
        streams[stream_name].drop()

def test_clone_with_point_of_time(streams, temp_stream):
    stream_name = random_string(10, 'test_stream_clone_pot_')
    cloned_stream = streams.create(stream_name,
        clone_stream=Clone(
            source=temp_stream.name
        )
    )

    try:
        cloned_handle = cloned_stream.fetch()
        assert isinstance(temp_stream.fetch().stream_source, type(cloned_handle.stream_source))
        assert temp_stream.fetch().stream_source.name == cloned_handle.stream_source.name
        assert cloned_handle.comment == "ThIs iS a ComMeNT"
    finally:
        streams[stream_name].drop()


def test_clone_across_schema(temp_stream, temp_schema):
    stream_name = random_string(10, "test_clone_stream_across_schema_")

    created_handle = temp_schema.streams.create(
        stream_name,
        clone_stream = f"{temp_stream.schema.name}.{temp_stream.name}"
    )

    try:
        assert isinstance(temp_stream.fetch().stream_source, type(created_handle.fetch().stream_source))
        assert temp_stream.fetch().stream_source.name == created_handle.fetch().stream_source.name
        assert created_handle.fetch().database_name.upper() == temp_schema.database.name.upper()
        assert created_handle.fetch().schema_name.upper() == temp_schema.name.upper()
        assert created_handle.fetch().comment == "ThIs iS a ComMeNT"
    finally:
        temp_schema.streams[stream_name].drop()


def test_clone_across_database(temp_stream, temp_db):
    schema_name = random_string(10, "test_create_clone_across_schema_")
    created_schema = temp_db.schemas.create(
        Schema(name=schema_name)
    )
    stream_name = random_string(10, "test_stream_clone_across_database_")

    try:
        created_handle = created_schema.streams.create(
            stream_name,
            clone_stream = f"{temp_stream.database.name}.{temp_stream.schema.name}.{temp_stream.name}"
        )

        assert isinstance(temp_stream.fetch().stream_source, type(created_handle.fetch().stream_source))
        assert temp_stream.fetch().stream_source.name == created_handle.fetch().stream_source.name
        assert created_handle.fetch().database_name.upper() == created_schema.database.name.upper()
        assert created_handle.fetch().schema_name.upper() == created_schema.name.upper()
        assert created_handle.fetch().comment == "ThIs iS a ComMeNT"
    finally:
        created_schema.drop()
