import pytest

from novita_sandbox.core import AsyncSandbox

@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_clone_returns_instances(template):
    src = await AsyncSandbox.create(template, timeout=300)
    try:
        clones = await AsyncSandbox.clone(src.sandbox_id, 2, strict=True, timeout=300)
        print("\nsnapshot:", clones.snapshot_template_id)
        assert len(clones) == 2
        for sbx in clones:
            assert isinstance(sbx, AsyncSandbox)
            assert sbx.sandbox_id
            assert await sbx.is_running() is True
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




