"""Leaving the folder step must preserve Back versus quitting the installer."""

import pytest

from probe.cli import backfill, backfill_run, tui


@pytest.mark.parametrize("picked", [tui.BACK, None], ids=["back", "quit"])
def test_folder_picker_exit_stops_before_any_import_work(monkeypatch, tmp_path, picked):
    monkeypatch.setattr(backfill, "choose_directory", lambda start: picked)

    def forbidden(*args, **kwargs):
        pytest.fail("leaving the folder picker must not start import work")

    monkeypatch.setattr(backfill, "resolve_agent", forbidden)
    monkeypatch.setattr(backfill_run, "execute", forbidden)

    def run():
        return backfill.run(client_factory=forbidden, start=tmp_path, interactive=True)

    if picked is None:
        with pytest.raises(KeyboardInterrupt):
            run()
    else:
        assert run() is None
