# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from unittest.mock import MagicMock

import pytest

import geneva.runners.ray.pipeline as pipeline_mod
from geneva.runners.ray.pipeline import FragmentWriterSession


def test_start_writer_requires_initialized_ray(monkeypatch) -> None:
    """Reject missing lifecycle ownership before Queue can auto-initialize Ray."""
    queue = MagicMock(side_effect=AssertionError("Queue must not be constructed"))
    monkeypatch.setattr(pipeline_mod.ray, "is_initialized", lambda: False)
    monkeypatch.setattr(pipeline_mod.ray.util.queue, "Queue", queue)
    session = FragmentWriterSession(
        frag_id=0,
        ds_uri="memory://table",
        output_columns=["out"],
        checkpoint_store=MagicMock(),
        where=None,
    )

    with pytest.raises(RuntimeError, match="before Ray is initialized"):
        session._start_writer()

    queue.assert_not_called()
