"""A client says which reply shapes it draws (``client.reads``), and the run carries it (PF-1 P3b, L13).

The ``message_blocks`` event goes only to a client that reads ``blocks-v1``; this pins the half that carries the
client's word from the request envelope to the run's context. Lane: common-docs/systems/chat/projects/chat-ground-up/cgu-m3-lanes/L13-blocks.md.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.capabilities import ClientContext
from matrx_ai.processing.blocks.saved_blocks import BLOCKS_V1_READ, client_reads, metadata_with_client_reads


def test_the_envelope_takes_reads_and_the_run_carries_them() -> None:
    client = ClientContext.model_validate({"surface": "matrx-user/chat", "reads": ["blocks-v1"]})
    metadata = metadata_with_client_reads({"x": 1}, client)
    assert metadata == {"x": 1, "client_reads": ["blocks-v1"]}
    assert client_reads(SimpleNamespace(metadata=metadata), BLOCKS_V1_READ) is True


def test_a_client_that_names_nothing_reads_nothing() -> None:
    plain = {"x": 1}
    assert metadata_with_client_reads(plain, ClientContext()) is plain
    assert metadata_with_client_reads(plain, None) is plain
    assert client_reads(SimpleNamespace(metadata=plain), BLOCKS_V1_READ) is False
    assert client_reads(None, BLOCKS_V1_READ) is False
