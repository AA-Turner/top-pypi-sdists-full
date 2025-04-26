
import sphinx.cmd.build

def test_build(tmpdir):
    sphinx.cmd.build.main([
        "-W",
        "-b", "linkcheck",
        "-d", str(tmpdir / "doctrees"),
        "doc",
        str(tmpdir / "html"),
    ])
