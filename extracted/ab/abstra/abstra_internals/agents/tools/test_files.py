import tempfile
from pathlib import Path

from abstra_internals.agents.tools.files import path_in_glob


class TestPathInGlob:
    def test_accepts_str_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "foo.csv").write_text("")
            assert path_in_glob(
                str(Path(tmpdir) / "*.csv"), str(Path(tmpdir) / "foo.csv")
            )

    def test_accepts_path_object(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "foo.csv").write_text("")
            assert path_in_glob(str(Path(tmpdir) / "*.csv"), Path(tmpdir) / "foo.csv")

    def test_rejects_unmatched_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "foo.csv").write_text("")
            assert not path_in_glob(
                str(Path(tmpdir) / "*.csv"), Path(tmpdir) / "foo.txt"
            )
