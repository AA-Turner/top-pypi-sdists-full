"""No gateway offered with late tools on is a once-only yellow notice, never red (feedback 0154af1e)."""
from unittest.mock import patch

from matrx_ai.providers import late_tools


def test_announce_once_is_yellow_and_once() -> None:
    late_tools._ANNOUNCED.discard("t")
    with patch.object(late_tools, "vcprint") as vc:
        late_tools._announce_once("t", "x")
        late_tools._announce_once("t", "x")
    assert vc.call_count == 1
    assert vc.call_args.kwargs["color"] == "yellow"
