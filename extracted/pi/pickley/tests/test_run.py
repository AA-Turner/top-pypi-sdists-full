from pickley import bstrap
from pickley.cli import RunSetup


def test_run(cli):
    cli.run("run --help")
    assert cli.succeeded
    assert "Run a python CLI (auto-install it if needed)" in cli.logged

    cli.run("-nv run mgit:mgit==1.3.0 -f")
    assert cli.succeeded
    assert "install mgit==1.3.0" in cli.logged
    assert "mgit -f" in cli.logged

    if bstrap.USE_UV:
        cli.run("-nv run pip-compile==6.14.0 foo")
        assert cli.succeeded
        assert "install pip-tools==6.14.0" in cli.logged
        assert "pip-compile foo" in cli.logged

        cli.run("-nv run aws==1.31.13 foo -bar")
        assert cli.succeeded
        assert "install awscli==1.31.13" in cli.logged
        assert "aws foo -bar" in cli.logged


def test_run_setup():
    rs = RunSetup.cmd_pip_compile()
    assert str(rs) == "pip-tools:pip-compile"

    rs = RunSetup.from_cli("foo:bar==1.0")
    assert str(rs) == "foo==1.0:bar"
    assert rs.command == "bar"
    assert rs.package == "foo"
    assert rs.pinned == "1.0"
    assert rs.specced == "foo==1.0"
