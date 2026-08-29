"""VIDEO GEN (2026-08-28) — registry seat for the studio spine.

Covers the two-vocabulary bridge (registry model keys -> studio zoo ids), the
transport schema, and — the actual regression guard — that the
text-to-video / image-to-video pairs resolve in both registries so
validate_registry stops flagging the Wan rows. Rendering itself is the studio
spine's and exercised on dev.

    ./venv/bin/pytest tests/test_video_gen_runner.py -q
"""
import importlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

VG = importlib.import_module("abstract_hugpy_dev.managers.video_gen")


def test_studio_model_id_bridges_the_two_vocabularies():
    # The four Wan rows registered on this fleet, as discovered.
    assert VG.studio_model_id("Wan2.1-T2V-1.3B") == "wan2.1-t2v-1.3b"
    assert VG.studio_model_id("Wan-AI~Wan2.1-VACE-1.3B") == "wan2.1-vace-1.3b"
    assert VG.studio_model_id("Wan2.1-VACE-1.3B-diffusers") == "wan2.1-vace-1.3b"
    # No match in the studio zoo -> passed through for the router to refuse
    # as err-as-data, never silently rewritten to a different model.
    assert VG.studio_model_id("VACE-Wan2.1-1.3B-Preview") == \
        "vace-wan2.1-1.3b-preview"


def test_request_defaults_are_the_wan_reference_geometry():
    req = VG.VideoGenRequest(request_id="r", model_key="m", prompt="p")
    assert (req.width, req.height, req.fps) == (832, 480, 16)
    assert req.requested_frames is None      # None = bound model's default (81)
    assert req.vram_budget_gb is None        # None = AUTOFIT, not a low guess
    with pytest.raises(Exception):
        VG.VideoGenRequest(request_id="r", model_key="m", prompt="p",
                           steps=101)


def test_registry_pairs_resolve():
    fw = importlib.import_module(
        "abstract_hugpy_dev.managers.resolvers.categories.frameworks")
    bl = importlib.import_module(
        "abstract_hugpy_dev.managers.resolvers.categories.builders")
    for task in ("text-to-video", "image-to-video"):
        assert ("transformers", task) in fw.FRAMEWORK_RUNNERS
        assert ("transformers", task) in bl.MODEL_REQUEST_BUILDERS
        assert task in fw.KNOWN_TASKS_REGISTRY
    assert fw.FRAMEWORK_RUNNERS[("transformers", "text-to-video")] \
        is VG.StudioVideoRunner


def test_builder_refuses_an_unconditioned_ask():
    bl = importlib.import_module(
        "abstract_hugpy_dev.managers.resolvers.categories.builders")
    build = bl.MODEL_REQUEST_BUILDERS[("transformers", "text-to-video")]
    with pytest.raises(ValueError):
        build({}, "Wan2.1-T2V-1.3B")
    req = build({"prompt": "a hillside at dawn", "requested_frames": 81},
                "Wan2.1-T2V-1.3B")
    assert req.model_key == "Wan2.1-T2V-1.3B"
    assert req.requested_frames == 81
