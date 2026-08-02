# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Cover the cross-process env-install path of the fault library.

``install_all_from_env`` and the ``GENEVA_FAULT_*`` spec parsers are how a real-Ray
worker installs faults it cannot receive via an in-process ``set_X`` (the propagated
env var is read in the worker). These are fast unit tests -- they install the ``Flaky*``
into the process-global indirections, assert the right type landed, and a fixture
restores the defaults so no fault leaks into other tests.
"""

import os
import pathlib
import sys
from collections.abc import Iterator

import pytest

from geneva.checkpoint import get_checkpoint_store_wrap, set_checkpoint_store_wrap
from geneva.committer import get_committer, set_committer
from geneva.field_metadata_writer import (
    get_field_metadata_writer,
    set_field_metadata_writer,
)
from geneva.fragment_writer import get_fragment_file_writer, set_fragment_file_writer
from geneva.table_writer import get_table_writer, set_table_writer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from geneva_faults import (  # noqa: E402
    FlakyCommitter,
    FlakyFieldMetadataWriter,
    FlakyFragmentFileWriter,
    FlakyTableWriter,
    _parse_committer_fault,
    install_all_from_env,
    install_committer_fault_from_env,
)

_ENV_VARS = (
    "GENEVA_FAULT_COMMITTER",
    "GENEVA_FAULT_TABLE_WRITER",
    "GENEVA_FAULT_FRAGMENT_WRITER",
    "GENEVA_FAULT_FIELD_METADATA",
    "GENEVA_FAULT_CHECKPOINT",
)


@pytest.fixture
def restore_globals() -> Iterator[None]:
    """Snapshot the five process-global indirections + env, restore on teardown so an
    installed fault never leaks into another test in the same process."""
    saved = (
        get_committer(),
        get_table_writer(),
        get_fragment_file_writer(),
        get_field_metadata_writer(),
        get_checkpoint_store_wrap(),
    )
    saved_env = {k: os.environ.get(k) for k in _ENV_VARS}
    try:
        yield
    finally:
        set_committer(saved[0])
        set_table_writer(saved[1])
        set_fragment_file_writer(saved[2])
        set_field_metadata_writer(saved[3])
        set_checkpoint_store_wrap(saved[4])
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def test_install_all_from_env_installs_every_surface(restore_globals) -> None:
    default_wrap = get_checkpoint_store_wrap()
    os.environ["GENEVA_FAULT_COMMITTER"] = "DataReplacement:drop:1"
    os.environ["GENEVA_FAULT_TABLE_WRITER"] = "delete:drop:1"
    os.environ["GENEVA_FAULT_FRAGMENT_WRITER"] = "raise:1"
    os.environ["GENEVA_FAULT_FIELD_METADATA"] = "drop:1"
    os.environ["GENEVA_FAULT_CHECKPOINT"] = "set:drop:1"

    install_all_from_env()

    assert isinstance(get_committer(), FlakyCommitter)
    assert isinstance(get_table_writer(), FlakyTableWriter)
    assert isinstance(get_fragment_file_writer(), FlakyFragmentFileWriter)
    assert isinstance(get_field_metadata_writer(), FlakyFieldMetadataWriter)
    assert get_checkpoint_store_wrap() is not default_wrap  # a flaky wrap was installed


def test_install_all_from_env_is_noop_when_unset(restore_globals) -> None:
    for k in _ENV_VARS:
        os.environ.pop(k, None)
    before = (get_committer(), get_table_writer(), get_checkpoint_store_wrap())

    install_all_from_env()

    assert (get_committer(), get_table_writer(), get_checkpoint_store_wrap()) == before


def test_install_swallows_malformed_spec(restore_globals) -> None:
    before = get_committer()
    os.environ["GENEVA_FAULT_COMMITTER"] = "not-a-valid-spec"

    # A malformed spec must not raise (it would break a worker's import); it is ignored.
    assert install_committer_fault_from_env() is None
    assert get_committer() is before


def test_parse_committer_fault_rejects_malformed() -> None:
    with pytest.raises(ValueError, match="expected"):
        _parse_committer_fault("missing-fields")
    parsed = _parse_committer_fault("DataReplacement:drop:1,2")
    assert isinstance(parsed, FlakyCommitter)
