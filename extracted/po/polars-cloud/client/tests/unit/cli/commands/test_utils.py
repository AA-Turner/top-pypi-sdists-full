import pytest
from polars_cloud.cli.commands._utils import handle_errors


def test_handle_errors() -> None:
    msg = "nope"

    with pytest.raises(SystemExit, match="ERROR: nope"):  # noqa: SIM117
        with handle_errors():
            raise ValueError(msg)
