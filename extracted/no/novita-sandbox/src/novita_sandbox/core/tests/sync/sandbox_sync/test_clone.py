import pytest

from novita_sandbox.core import Sandbox


@pytest.mark.skip_debug()
def test_clone_returns_instances(template):
    # Create a short-lived sandbox to clone
    src = Sandbox.create(template, timeout=300)
    try:
        clones = Sandbox.clone(src.sandbox_id, 2, strict=True, timeout=300)
        print("\nsnapshot:", clones.snapshot_template_id)
        assert len(clones) == 2
        for sbx in clones:
            assert isinstance(sbx, Sandbox)
            assert sbx.sandbox_id
            # new instances should be reachable
            assert sbx.is_running() is True
    finally:
        # Cleanup
        print("\n\n")
        print("src.sandbox_id", src.sandbox_id)
        src.kill()
        for idx, sbx in enumerate(locals().get('clones', []) or []):
            try:
                print(f"clone.sandbox[{idx}]", sbx.sandbox_id)
                sbx.kill()
            except Exception:
                pass




