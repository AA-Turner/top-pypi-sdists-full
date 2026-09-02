import pytest

from novita_sandbox.core import Sandbox


@pytest.mark.skip_debug()
def test_snapshot(sandbox: Sandbox):
    assert sandbox.is_running()

    sandbox.beta_pause()
    assert not sandbox.is_running()

    resumed_sandbox = sandbox.connect()
    assert sandbox.is_running()
    assert resumed_sandbox.is_running()
    assert resumed_sandbox.sandbox_id == sandbox.sandbox_id

@pytest.mark.skip_debug()
def test_snapshot_with_sync(sandbox: Sandbox):
    assert sandbox.is_running()

    sandbox.beta_pause(sync=True)
    assert not sandbox.is_running()
