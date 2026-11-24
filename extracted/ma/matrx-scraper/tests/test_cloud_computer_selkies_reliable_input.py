"""The Cloud Computer's key, mouse and clipboard channel never drops a message (2026-11-19).

Selkies 1.6.2 opens its input data channel ordered with ``max-retransmits`` 0:
a message lost on the network is never sent again. Over a relayed connection
that loses packets, a lost key-down is a key never typed and a lost key-up is a
key held down on the machine (auto-repeated, or a stuck Control). The owner's
correct authenticator code was refused and his shortcuts did nothing while the
picture lagged. The image build removes the limit, which makes the channel
reliable. This applies the build's own edit to the upstream lines.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

PATCH = Path(__file__).resolve().parents[1] / "docker" / "cloud-computer" / "patch-selkies-web.py"

# Selkies 1.6.2 selkies_gstreamer/gstwebrtc_app.py, start_pipeline, verbatim.
UPSTREAM = '''        if not audio_only:
            # Create the data channel, this has to be done after the pipeline is PLAYING.
            options = Gst.Structure("application/data-channel")
            options.set_value("ordered", True)
            options.set_value("priority", "high")
            options.set_value("max-retransmits", 0)
            self.data_channel = self.webrtcbin.emit(
                'create-data-channel', "input", options)
'''


def _patch_module():
    spec = importlib.util.spec_from_file_location("patch_selkies_web", PATCH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_input_channel_is_reliable_and_still_ordered() -> None:
    patch = _patch_module()
    patched = patch.patch_text("gstwebrtc_app.py", UPSTREAM, patch.PACKAGE_EDITS["gstwebrtc_app.py"])
    # No retransmit limit and no lifetime limit = a reliable channel.
    assert 'set_value("max-retransmits"' not in patched
    assert 'set_value("max-packet-lifetime"' not in patched
    assert 'options.set_value("ordered", True)' in patched
    assert "'create-data-channel', \"input\", options)" in patched
    compile(patched.replace("        if not audio_only:", "if True:", 1).replace("\n            ", "\n    "), "patched", "exec")


def test_a_changed_upstream_fails_the_build_instead_of_shipping_unpatched() -> None:
    patch = _patch_module()
    assert "gstwebrtc_app.py" in patch.PACKAGE_UPSTREAM_SHA256
    with pytest.raises(SystemExit):
        patch.patch_text("gstwebrtc_app.py", UPSTREAM.replace('"max-retransmits", 0', '"max-retransmits", 2'),
                         patch.PACKAGE_EDITS["gstwebrtc_app.py"])
