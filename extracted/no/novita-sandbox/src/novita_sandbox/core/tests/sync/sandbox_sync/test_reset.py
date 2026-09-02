import pytest

from novita_sandbox.core import Sandbox


@pytest.mark.skip_debug()
def test_reset_returns_instances(template):
    # Create a short-lived sandbox to clone
    sbx = Sandbox.create(template, timeout=300)
    try:
        sbx.reset(resume=True, timeout=150)
        assert sbx.is_running() is True
    finally:
        # Cleanup
        print("\n\n")
        print("src.sandbox_id", sbx.sandbox_id)
        sbx.kill()


@pytest.mark.skip_debug()
def test_reset_static_returns_instances(template):
    # Create a short-lived sandbox to clone
    sbx = Sandbox.create(template, timeout=300)
    try:
        Sandbox.reset(sbx.sandbox_id, resume=True, timeout=150)
        assert sbx.is_running() is True
    finally:
        # Cleanup
        print("\n\n")
        print("src.sandbox_id", sbx.sandbox_id)
        sbx.kill()



