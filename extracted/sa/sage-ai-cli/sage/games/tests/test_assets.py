"""Asset-generator end-to-end coverage.

The asset layer is the one subsystem that runs every build, regardless
of engine. It must keep moving even when its primary backends (Imagen,
Blender, Replicate, ffmpeg) are unavailable — so we explicitly test the
fallback paths, since those are what hit in CI / on a stock developer
machine that hasn't set up cloud creds.

Each test asserts the *file* on disk is structurally valid, not just
that some bytes got written: a corrupt PNG that ships into a Godot or
Unity build is worse than no PNG at all (it crashes the importer at
load time instead of giving a clear "missing asset" error at scaffold).
"""

from __future__ import annotations

import shutil
import struct
import zipfile
from pathlib import Path

import pytest

from sage.games.assets import (
    AssetManifest,
    AudioGenerator,
    AudioResult,
    MeshGenerator,
    MeshResult,
    SpriteGenerator,
    SpriteResult,
)


# ───────────────────────── helpers ────────────────────────────────────


_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _read_png_ihdr(path: Path) -> tuple[int, int, int, int]:
    """Parse the IHDR chunk of a PNG. Raises if the file isn't a real PNG.

    Returns (width, height, bit_depth, color_type). Mirrors what the Godot
    and Unity texture importers do on first read — if this passes, those
    importers will too."""
    blob = path.read_bytes()
    assert blob.startswith(_PNG_MAGIC), f"missing PNG magic in {path}"
    # 8 bytes magic + 4 bytes length + 4 bytes type "IHDR" + 13 bytes data
    ihdr_len = struct.unpack(">I", blob[8:12])[0]
    assert blob[12:16] == b"IHDR", "first chunk must be IHDR"
    assert ihdr_len == 13, f"IHDR length must be 13, got {ihdr_len}"
    width, height = struct.unpack(">II", blob[16:24])
    bit_depth, color_type = blob[24], blob[25]
    # Tail must contain IEND to be a complete file.
    assert blob.endswith(b"IEND\xae\x42\x60\x82"), "missing IEND chunk"
    return width, height, bit_depth, color_type


# ───────────────────────── SpriteGenerator ────────────────────────────


def test_sprite_generator_produces_valid_placeholder_png(tmp_path):
    """No cloud creds in CI → placeholder path must produce a real PNG."""
    gen = SpriteGenerator(tmp_path / "sprites", style="pixel")
    result = gen.generate("player", "blue cube hero", size=(64, 48))

    assert isinstance(result, SpriteResult)
    assert result.role == "player"
    assert result.backend == "placeholder"  # no creds in test env
    assert result.path.is_file()
    assert result.path.suffix == ".png"

    width, height, bit_depth, color_type = _read_png_ihdr(result.path)
    assert (width, height) == (64, 48)
    assert bit_depth == 8 and color_type == 2  # 8-bit RGB


def test_sprite_generator_uses_deterministic_color_per_role(tmp_path):
    """Same role → same placeholder color. Different roles → different colors.

    We don't pin the actual RGB tuple (hash() randomization makes that
    flaky across processes), we just assert two roles produce two distinct
    images and that re-generating one role produces an identical file."""
    gen = SpriteGenerator(tmp_path / "sprites")
    a1 = gen.generate("alpha", "any prompt", size=(8, 8))
    a2 = gen.generate("alpha", "any prompt", size=(8, 8))
    b1 = gen.generate("beta", "any prompt", size=(8, 8))

    assert a1.path.read_bytes() == a2.path.read_bytes()
    assert a1.path.read_bytes() != b1.path.read_bytes()


def test_sprite_generator_falls_back_when_imagen_raises(tmp_path, monkeypatch):
    """Force the Imagen path to look available, then make it raise. We must
    fall through to the placeholder and NOT propagate the exception — a
    single failing sprite shouldn't sink the whole build."""
    from sage.games.assets import sprites as s
    monkeypatch.setattr(s, "_vertex_available", lambda: True)

    def boom(*args, **kwargs):
        raise RuntimeError("imagen quota exceeded")
    monkeypatch.setattr(s, "_imagen_generate", boom)

    gen = SpriteGenerator(tmp_path / "sprites")
    result = gen.generate("hero", "any prompt", size=(16, 16))
    assert result.backend == "placeholder"
    width, height, *_ = _read_png_ihdr(result.path)
    assert (width, height) == (16, 16)


def test_sprite_generator_uses_imagen_when_path_succeeds(tmp_path, monkeypatch):
    """Path coverage: when both `_vertex_available` and `_imagen_generate`
    succeed, the result reports backend=imagen and the size we asked for."""
    from sage.games.assets import sprites as s
    monkeypatch.setattr(s, "_vertex_available", lambda: True)

    def fake_imagen(prompt, size, out_path, *, style):
        # Write a valid 4×4 PNG so _read_png_ihdr stays clean.
        out_path.write_bytes(_one_pixel_red_png(size))
    monkeypatch.setattr(s, "_imagen_generate", fake_imagen)

    gen = SpriteGenerator(tmp_path / "sprites", style="cartoon")
    result = gen.generate("villain", "evil sorcerer", size=(32, 32))
    assert result.backend == "imagen"
    assert result.path.is_file()
    width, height, *_ = _read_png_ihdr(result.path)
    assert (width, height) == (32, 32)


def _one_pixel_red_png(size: tuple[int, int]) -> bytes:
    """Build a real RGB PNG of `size` filled with red. Used in tests where
    we need to mock Imagen with a valid file the rest of the pipeline can
    consume."""
    from sage.games.assets.sprites import _write_placeholder_png  # type: ignore
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
        _write_placeholder_png(Path(tf.name), size, (255, 0, 0))
        return Path(tf.name).read_bytes()


# ───────────────────────── MeshGenerator ──────────────────────────────


_GLB_MAGIC = b"glTF"


def test_mesh_generator_falls_back_to_placeholder_glb(tmp_path):
    """No Blender on PATH → placeholder GLB. Must start with `glTF` magic
    so a Godot/Unity glTF importer doesn't reject it outright."""
    gen = MeshGenerator(tmp_path / "meshes")
    result = gen.generate("world", "open level")

    assert isinstance(result, MeshResult)
    assert result.backend == "placeholder"
    assert result.path.is_file()
    assert result.path.read_bytes().startswith(_GLB_MAGIC)


@pytest.mark.parametrize("prompt,expected_prim", [
    ("a player character",       "capsule"),
    ("a stone pillar",            "cylinder"),
    ("a brick block",             "cube"),
    ("a planet orb",              "sphere"),
    ("a flat ground plane",       "plane"),
    ("a pine tree",               "cone"),
    ("something nondescript",     "cube"),
])
def test_mesh_primitive_classifier(prompt, expected_prim):
    """_pick_primitive is the only deterministic heuristic in the mesh
    layer — wrong classification means wrong primitive at build time."""
    from sage.games.assets.meshes import _pick_primitive
    assert _pick_primitive(prompt) == expected_prim


def test_mesh_generator_when_blender_fails_writes_placeholder(tmp_path, monkeypatch):
    """If Blender is found but `_blender_export` raises mid-run, the
    generator must still emit a placeholder so the manifest stays
    consistent for the engine adapter that consumes it."""
    from sage.games.assets import meshes as m
    monkeypatch.setattr(m, "_find_blender", lambda: Path("/fake/blender"))

    def boom(blender, prim, out_path):
        raise RuntimeError("blender crashed")
    monkeypatch.setattr(m, "_blender_export", boom)

    gen = MeshGenerator(tmp_path / "meshes")
    result = gen.generate("enemy", "robot")
    assert result.backend == "placeholder"
    assert result.path.read_bytes().startswith(_GLB_MAGIC)


# ───────────────────────── AudioGenerator ─────────────────────────────


def test_audio_silent_wav_is_valid_riff(tmp_path, monkeypatch):
    """Force the silent fallback (no Replicate token, no ffmpeg). The WAV
    we write must be a valid RIFF that audio decoders can open."""
    from sage.games.assets import audio as a
    monkeypatch.delenv("REPLICATE_API_TOKEN", raising=False)
    monkeypatch.setattr(a, "_ffmpeg_available", lambda: False)

    gen = AudioGenerator(tmp_path / "audio")
    sfx = gen.generate_sfx("jump", "jump sound")

    assert isinstance(sfx, AudioResult)
    assert sfx.backend == "silent"
    assert sfx.path.suffix == ".wav"
    blob = sfx.path.read_bytes()
    assert blob.startswith(b"RIFF")
    # WAVE format chunk + data chunk are required for any decoder to read.
    assert b"WAVE" in blob[:12]
    assert b"fmt " in blob
    assert b"data" in blob


def test_audio_music_silent_ogg_when_nothing_available(tmp_path, monkeypatch):
    """Same idea for music — when no backend is available, we emit an empty
    .ogg. Empty is intentional (downstream engines treat it as "no track"),
    but the file MUST exist and the result must report backend=silent so
    the report is accurate."""
    from sage.games.assets import audio as a
    monkeypatch.delenv("REPLICATE_API_TOKEN", raising=False)
    monkeypatch.setattr(a, "_ffmpeg_available", lambda: False)

    gen = AudioGenerator(tmp_path / "audio")
    music = gen.generate_music("theme", "epic battle music", seconds=5)
    assert music.backend == "silent"
    assert music.path.suffix == ".ogg"
    assert music.path.is_file()


def test_audio_uses_ffmpeg_when_available(tmp_path, monkeypatch):
    """When ffmpeg IS available (mocked), the SFX path must invoke it and
    report backend=ffmpeg. We mock subprocess.run so the test doesn't need
    a real ffmpeg binary in CI."""
    from sage.games.assets import audio as a
    monkeypatch.delenv("REPLICATE_API_TOKEN", raising=False)
    monkeypatch.setattr(a, "_ffmpeg_available", lambda: True)

    def fake_ffmpeg_sfx(prompt, out_path):
        # ffmpeg "writes" a stub file via our mock
        out_path.write_bytes(b"RIFFmockWAVEfmt mockdatamock")
    monkeypatch.setattr(a, "_ffmpeg_sfx", fake_ffmpeg_sfx)

    gen = AudioGenerator(tmp_path / "audio")
    res = gen.generate_sfx("explode", "explosion sound")
    assert res.backend == "ffmpeg"
    assert res.path.read_bytes().startswith(b"RIFF")


# ───────────────────────── AssetManifest ──────────────────────────────


def test_asset_manifest_total_count(tmp_path):
    m = AssetManifest(
        sprites={"a": tmp_path / "a", "b": tmp_path / "b"},
        meshes={"c": tmp_path / "c"},
        audio={"d": tmp_path / "d", "e": tmp_path / "e"},
    )
    assert m.total_count() == 5


def test_asset_manifest_starts_empty():
    m = AssetManifest()
    assert m.total_count() == 0
    assert m.sprites == {} and m.meshes == {} and m.audio == {}
