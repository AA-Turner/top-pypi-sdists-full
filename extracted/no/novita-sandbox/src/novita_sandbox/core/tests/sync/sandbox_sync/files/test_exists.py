from novita_sandbox.core import Sandbox


def test_exists(sandbox: Sandbox):
    filename = "test_exists.txt"

    sandbox.files.write(filename, "test")
    assert sandbox.files.exists(filename)


def test_does_not_exist(sandbox: Sandbox):
    assert not sandbox.files.exists("/nonexistent/path")
