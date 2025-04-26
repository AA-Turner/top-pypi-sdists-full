import time

from contextlib import suppress

import pytest

from snowflake.core._common import CreateMode
from snowflake.core.exceptions import ConflictError, NotFoundError
from snowflake.core.stream import PointOfTimeOffset, Stream, StreamSourceStage, StreamSourceTable, StreamSourceView
from tests.utils import random_string


def create_stream(name, stream_source, streams):
    stream = Stream(name=name, stream_source=stream_source)

    created_stream = streams.create(stream)

    stream_handle = created_stream.fetch()
    assert stream_handle.name.upper() == name.upper()
    assert stream_handle.stream_source is not None
    assert type(stream_handle.stream_source) is type(stream_source)
    return stream_handle


@pytest.mark.min_sf_ver("8.35.0")
@pytest.mark.parametrize("pot", (None, PointOfTimeOffset(reference="before", offset="-1")))
def test_create_by_table(streams, src_temp_table, pot):
    stream_name = random_string(10, 'test_stream_by_table_')
    try:
        if pot is not None:
            time.sleep(1)
        create_stream(stream_name, StreamSourceTable(
            point_of_time = pot,
            name = src_temp_table.name,
            append_only = True,
            show_initial_rows = False,
            comment = "asdf"
        ), streams)
    finally:
        with suppress(NotFoundError):
            streams[stream_name].drop()


@pytest.mark.min_sf_ver("8.35.0")
@pytest.mark.parametrize("pot", (None, PointOfTimeOffset(reference="before", offset="-1")))
def test_create_by_view(streams, src_temp_view, pot):
    stream_name = random_string(10, 'test_stream_by_view_')

    try:
        if pot is not None:
            time.sleep(1)
        create_stream(stream_name, StreamSourceView(
            point_of_time = pot,
            name = src_temp_view.name,
        ), streams)
    finally:
        with suppress(NotFoundError):
            streams[stream_name].drop()


@pytest.mark.min_sf_ver("8.35.0")
@pytest.mark.parametrize("pot", (None, PointOfTimeOffset(reference="before", offset="-1")))
def test_create_by_directory_table(streams, temp_directory_table, pot):
    stream_name = random_string(10, 'test_stream_by_stage_')

    try:
        if pot is not None:
            time.sleep(1)
        create_stream(stream_name, StreamSourceStage(
            point_of_time = pot,
            name = temp_directory_table.name,
        ), streams)
    finally:
        with suppress(NotFoundError):
            streams[stream_name].drop()


@pytest.mark.min_sf_ver("8.35.0")
@pytest.mark.parametrize("pot", (None, PointOfTimeOffset(reference="before", offset="-1")))
def test_create_by_view_with_multiple_base_tables(
        streams, src_temp_view_with_multiple_base_tables, pot):
    stream_name = random_string(10, 'test_stream_by_view_with_multiple_base_tables_')

    view_handle, table_a_name, table_b_name = src_temp_view_with_multiple_base_tables
    try:
        if pot is not None:
            time.sleep(1)
        stream_handle = create_stream(stream_name, StreamSourceView(
            point_of_time = pot,
            name = view_handle.name,
        ), streams)

        assert isinstance(stream_handle.stream_source, StreamSourceView)
        assert sorted([i.split('.')[-1] for i in stream_handle.stream_source.base_tables]) \
            == sorted([table_a_name.upper(), table_b_name.upper()])
    finally:
        with suppress(NotFoundError):
            streams[stream_name].drop()


@pytest.mark.min_sf_ver("8.35.0")
def test_create_and_update(streams, src_temp_table):
    stream_name = random_string(10, 'test_stream_by_table_')

    try:
        stream_handle = streams.create(Stream(
            name=stream_name,
            stream_source=StreamSourceTable(
                name = src_temp_table.name,
            )
        ))

        streams.create(Stream(
            name=stream_name,
            stream_source=StreamSourceTable(
                name = src_temp_table.name,
                copy_grants = True,
            )
        ), mode = CreateMode.or_replace)

        with pytest.raises(
            ConflictError
        ):
            streams.create(Stream(
                name=stream_name,
                stream_source=StreamSourceTable(
                    name = src_temp_table.name,
                )
            ))

        streams.create(
            stream_handle.fetch(),
            mode = CreateMode.or_replace
        )
    finally:
        with suppress(NotFoundError):
            streams[stream_name].drop()
