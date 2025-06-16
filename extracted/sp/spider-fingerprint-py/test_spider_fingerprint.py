from spider_fingerprint_py import (
    PyViewport, PyTier, PyFingerprintMode, generate_emulation_script, spoof_ua
)

def test_generate_script_basic():
    user_agent = spoof_ua()
    viewport = PyViewport(width=1280, height=720)
    script = generate_emulation_script(
        user_agent=user_agent,
        tier=PyTier.Basic,
        fingerprint_mode=PyFingerprintMode.Basic,
        dismiss_dialogs=True,
        viewport=viewport,
        eval_script=None,
    )
    
    assert script is not None, "Generated script should not be None"
    assert len(script) > 0, "Generated script cannot be empty"
    print(script)

def test_generate_script_none():
    user_agent = spoof_ua()
    
    script = generate_emulation_script(
        user_agent=user_agent,
        tier=PyTier.NoSpoof,
        fingerprint_mode=PyFingerprintMode.NoSpoof,
        dismiss_dialogs=False
    )

    assert script is None, "Script should be None when no spoofing is selected."