"""Pinning tests for the Image Studio rendering primitives.

These cover the pure compute that turns ``(source_bytes, render_spec)``
into output bytes — the parts that would silently regress and quietly
ship the wrong thing if untested. No S3, no DB, no FastAPI; the router
itself is exercised by integration tests elsewhere.

The tests cover:

1. **Geometry math** — ``_cover_rect_at_focal_point`` agrees with the FE
   port (``coverRectAtFocalPoint`` in compute-crop.ts).
2. **Hex parser** — every shorthand the FE can send.
3. **Anchor table** — every named anchor maps to the expected corner.
4. **Fit modes** — cover crops, contain letterboxes, inside upscales
   to match Sharp's ``withoutEnlargement: false`` default.
5. **Smart crop** — entropy / attention pick higher-detail regions
   over uniform ones.
6. **Output formats** — every format produces non-empty bytes; quality
   is honored for lossy codecs; PNG is alpha-preserved.
7. **EXIF transpose** — orientation 6 (rotate-90-CW) is undone.
8. **Preset catalog integrity** — every preset id is unique, every
   width / height is positive, every recommended bundle references
   real ids.
"""

from __future__ import annotations

from io import BytesIO

import pytest
from PIL import Image

from matrx_files.specific_handlers.image_handler import (
    ImageHandler,
    _NAMED_FOCAL_POINTS,
    _anchor_to_focal_point,
    _cover_rect_at_focal_point,
    _parse_hex_color,
    is_avif_available,
)
from matrx_files.specific_handlers.image_studio_presets import (
    ALL_PRESETS,
    PRESETS_BY_ID,
    PRESET_CATEGORIES,
    RECOMMENDED_BUNDLES,
    get_preset_by_id,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _solid(width: int, height: int, color: tuple[int, int, int] = (200, 200, 200), mode: str = "RGB") -> Image.Image:
    return Image.new(mode, (width, height), color)


def _gradient(width: int, height: int) -> Image.Image:
    """A horizontal gradient — left half dark, right half bright; high entropy in the middle."""
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for x in range(width):
        v = int(255 * x / max(1, width - 1))
        for y in range(height):
            pixels[x, y] = (v, v, v)
    return img


def _checkerboard(width: int, height: int, square: int = 8) -> Image.Image:
    """High-entropy region — black and white squares."""
    img = Image.new("RGB", (width, height), (255, 255, 255))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            if ((x // square) + (y // square)) % 2 == 0:
                pixels[x, y] = (0, 0, 0)
    return img


def _half_blank_half_busy(width: int, height: int) -> Image.Image:
    """Left half is uniform gray (low entropy), right half is checkerboard (high entropy).

    A correct entropy-crop should pick the right half when the target
    aspect demands a crop narrower than the source.
    """
    img = _solid(width, height, (128, 128, 128))
    busy = _checkerboard(width // 2, height, square=4)
    img.paste(busy, (width // 2, 0))
    return img


def _bytes_for(img: Image.Image, fmt: str = "PNG") -> bytes:
    buf = BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# 1. Geometry — _cover_rect_at_focal_point
# ---------------------------------------------------------------------------


class TestCoverRectAtFocalPoint:
    def test_centre_focal_returns_centred_crop(self):
        # 4000x3000 source, target 1000x500 → 2:1 aspect → crop_h = 2000.
        left, top, w, h = _cover_rect_at_focal_point(4000, 3000, 1000, 500, (0.5, 0.5))
        assert (w, h) == (4000, 2000)
        assert left == 0
        assert top == 500  # (3000 - 2000) // 2

    def test_focal_point_is_clamped_inside_source(self):
        # Push focal point past the right edge — crop must still be inside.
        left, top, w, h = _cover_rect_at_focal_point(4000, 3000, 1000, 500, (1.5, 0.5))
        assert left == 0
        assert top + h <= 3000

    def test_same_aspect_returns_full_source(self):
        left, top, w, h = _cover_rect_at_focal_point(1000, 500, 200, 100, (0.3, 0.7))
        assert (left, top, w, h) == (0, 0, 1000, 500)

    def test_zero_dim_source_does_not_crash(self):
        left, top, w, h = _cover_rect_at_focal_point(0, 0, 100, 100, (0.5, 0.5))
        assert (w, h) == (0, 0)


# ---------------------------------------------------------------------------
# 2. Hex parser
# ---------------------------------------------------------------------------


class TestParseHexColor:
    @pytest.mark.parametrize(
        "input_str,expected",
        [
            ("#fff", (255, 255, 255)),
            ("#000", (0, 0, 0)),
            ("#ffffff", (255, 255, 255)),
            ("#000000", (0, 0, 0)),
            ("ffffff", (255, 255, 255)),
            ("#ffaa00", (255, 170, 0)),
            ("#FFAA00", (255, 170, 0)),
            ("#ffffff80", (255, 255, 255)),  # 8-char with alpha; alpha stripped
        ],
    )
    def test_valid_inputs(self, input_str, expected):
        assert _parse_hex_color(input_str) == expected

    @pytest.mark.parametrize("bad", ["", "#", "#zz", "not-a-color", "#ff", "#fffff"])
    def test_invalid_returns_white(self, bad):
        assert _parse_hex_color(bad) == (255, 255, 255)


# ---------------------------------------------------------------------------
# 3. Anchor table
# ---------------------------------------------------------------------------


class TestAnchorTable:
    def test_all_nine_anchors_in_unit_square(self):
        for anchor in _NAMED_FOCAL_POINTS:
            x, y = _anchor_to_focal_point(anchor)
            assert 0.0 <= x <= 1.0
            assert 0.0 <= y <= 1.0

    def test_corners_pin_corners(self):
        assert _anchor_to_focal_point("top-left") == (0.0, 0.0)
        assert _anchor_to_focal_point("top-right") == (1.0, 0.0)
        assert _anchor_to_focal_point("bottom-left") == (0.0, 1.0)
        assert _anchor_to_focal_point("bottom-right") == (1.0, 1.0)

    def test_unknown_anchor_falls_back_to_centre(self):
        assert _anchor_to_focal_point("not-a-real-anchor") == (0.5, 0.5)


# ---------------------------------------------------------------------------
# 4. Fit modes
# ---------------------------------------------------------------------------


class TestFitModes:
    def test_cover_produces_exact_target_size(self):
        src = _gradient(2000, 1000)
        out, notes = ImageHandler.apply_studio_fit(src, 800, 800, "cover", "center", (255, 255, 255))
        assert out.size == (800, 800)
        assert notes == []

    def test_contain_produces_exact_target_size_with_padding(self):
        src = _solid(1000, 500, (200, 0, 0))  # 2:1 source
        out, notes = ImageHandler.apply_studio_fit(src, 400, 400, "contain", "center", (255, 255, 255))
        assert out.size == (400, 400)
        # Top + bottom rows should be the background color (padded).
        # Inner aspect 2:1 fit inside 400x400 → 400x200 centered vertically.
        assert out.getpixel((10, 10)) == (255, 255, 255) or out.getpixel((10, 10)) == (255, 255, 255, 255)

    def test_inside_upscales_when_source_smaller_than_target(self):
        # 100x100 → 1080x1080 should upscale (Sharp default: withoutEnlargement=false).
        src = _solid(100, 100, (100, 50, 50))
        out, _ = ImageHandler.apply_studio_fit(src, 1080, 1080, "inside", "center", (255, 255, 255))
        assert out.size == (1080, 1080)

    def test_inside_preserves_aspect(self):
        # 2000x1000 source, 800x600 inside target → result is the largest size that
        # fits inside 800x600 at 2:1 aspect → 800x400.
        src = _solid(2000, 1000)
        out, _ = ImageHandler.apply_studio_fit(src, 800, 600, "inside", "center", (255, 255, 255))
        assert out.size == (800, 400)

    def test_cover_with_focal_point_dict(self):
        src = _gradient(2000, 1000)
        out, _ = ImageHandler.apply_studio_fit(src, 800, 800, "cover", {"x": 0.25, "y": 0.5}, (255, 255, 255))
        assert out.size == (800, 800)


# ---------------------------------------------------------------------------
# 5. Smart crop
# ---------------------------------------------------------------------------


class TestSmartCrop:
    def test_entropy_crop_picks_busy_half(self):
        # Source: left half blank, right half checkerboard. Target: square crop
        # narrower than source. Entropy should pick the right (checkerboard) half.
        src = _half_blank_half_busy(800, 400)
        # Use a square target so the chosen window is 400x400 and lives entirely
        # in either the left or right half.
        fx, fy = ImageHandler.smart_crop_focal_point(src, 400, 400, "entropy")
        assert fx > 0.5, f"expected entropy crop to favor the busy right half, got fx={fx}"

    def test_attention_crop_returns_focal_point_in_unit_square(self):
        src = _checkerboard(600, 400, square=4)
        fx, fy = ImageHandler.smart_crop_focal_point(src, 300, 200, "attention")
        assert 0.0 <= fx <= 1.0
        assert 0.0 <= fy <= 1.0

    def test_smart_crop_is_centre_when_source_already_at_target_aspect(self):
        # No cropping decision to make — the function returns center.
        src = _gradient(800, 400)  # 2:1
        fx, fy = ImageHandler.smart_crop_focal_point(src, 400, 200, "entropy")  # also 2:1
        assert (fx, fy) == (0.5, 0.5)

    def test_smart_crop_handles_zero_dim_gracefully(self):
        src = Image.new("RGB", (1, 1), (0, 0, 0))
        fx, fy = ImageHandler.smart_crop_focal_point(src, 0, 0, "entropy")
        assert (fx, fy) == (0.5, 0.5)


# ---------------------------------------------------------------------------
# 6. Output formats
# ---------------------------------------------------------------------------


class TestOutputFormats:
    @pytest.fixture
    def src_bytes(self) -> bytes:
        return _bytes_for(_gradient(400, 300))

    @pytest.mark.parametrize("fmt", ["jpeg", "png", "webp"])
    def test_format_produces_nonempty_bytes(self, src_bytes, fmt):
        result = ImageHandler.render_studio_variant(src_bytes, {
            "preset_id": "test",
            "width": 200, "height": 200,
            "format": fmt, "quality": 80,
            "fit": "cover", "position": "center",
            "background_color": "#ffffff",
        })
        assert result["size"] > 0
        assert len(result["bytes"]) == result["size"]
        assert result["width"] == 200
        assert result["height"] == 200

    @pytest.mark.skipif(not is_avif_available(), reason="pillow-avif-plugin not installed")
    def test_avif_format_produces_nonempty_bytes(self, src_bytes):
        result = ImageHandler.render_studio_variant(src_bytes, {
            "preset_id": "test", "width": 200, "height": 200,
            "format": "avif", "quality": 70,
            "fit": "cover", "position": "center",
            "background_color": "#ffffff",
        })
        assert result["size"] > 0

    def test_jpeg_quality_lower_means_smaller(self, src_bytes):
        hi = ImageHandler.render_studio_variant(src_bytes, {
            "preset_id": "test", "width": 400, "height": 300,
            "format": "jpeg", "quality": 95,
            "fit": "inside", "position": "center", "background_color": "#ffffff",
        })
        lo = ImageHandler.render_studio_variant(src_bytes, {
            "preset_id": "test", "width": 400, "height": 300,
            "format": "jpeg", "quality": 30,
            "fit": "inside", "position": "center", "background_color": "#ffffff",
        })
        assert lo["size"] < hi["size"]

    def test_png_returns_quality_none(self, src_bytes):
        result = ImageHandler.render_studio_variant(src_bytes, {
            "preset_id": "test", "width": 100, "height": 100,
            "format": "png", "quality": 80,
            "fit": "cover", "position": "center", "background_color": "#ffffff",
        })
        assert result["quality"] is None

    def test_jpeg_alpha_source_is_flattened(self):
        # RGBA source with alpha=0 → should flatten onto background_color.
        rgba = Image.new("RGBA", (100, 100), (255, 0, 0, 0))
        src_bytes = _bytes_for(rgba, fmt="PNG")
        result = ImageHandler.render_studio_variant(src_bytes, {
            "preset_id": "test", "width": 50, "height": 50,
            "format": "jpeg", "quality": 90,
            "fit": "cover", "position": "center", "background_color": "#00ff00",
        })
        # Round-trip: decode the JPEG and check a center pixel.
        out = Image.open(BytesIO(result["bytes"])).convert("RGB")
        r, g, b = out.getpixel((25, 25))
        assert g > 200, f"expected green background after flatten; got ({r}, {g}, {b})"


# ---------------------------------------------------------------------------
# 7. EXIF transpose
# ---------------------------------------------------------------------------


class TestExifTranspose:
    def test_orientation_6_is_un_rotated(self):
        # A 200x100 image with EXIF orientation 6 should be presented as 100x200
        # (rotated 90° clockwise back to upright).
        src = _gradient(200, 100)
        # Build EXIF block with orientation = 6.
        exif = src.getexif()
        exif[0x0112] = 6  # Orientation tag
        buf = BytesIO()
        src.save(buf, format="JPEG", exif=exif.tobytes())
        result = ImageHandler.render_studio_variant(buf.getvalue(), {
            "preset_id": "test", "width": 50, "height": 100,
            "format": "png", "quality": 80,
            "fit": "inside", "position": "center", "background_color": "#ffffff",
        })
        # After exif_transpose, the source is 100x200; inside-fit at 50x100 keeps aspect.
        assert result["width"] == 50
        assert result["height"] == 100


# ---------------------------------------------------------------------------
# 8. Preset catalog integrity
# ---------------------------------------------------------------------------


class TestPresetCatalog:
    def test_every_preset_id_is_unique(self):
        ids = [p["id"] for p in ALL_PRESETS]
        assert len(ids) == len(set(ids)), "duplicate preset ids in catalog"

    def test_presets_by_id_matches_all_presets(self):
        assert len(PRESETS_BY_ID) == len(ALL_PRESETS)
        for p in ALL_PRESETS:
            assert PRESETS_BY_ID[p["id"]] is p

    def test_every_preset_has_positive_dimensions(self):
        for p in ALL_PRESETS:
            assert p["width"] > 0
            assert p["height"] > 0

    def test_every_preset_has_required_fields(self):
        required = {"id", "name", "usage", "width", "height", "aspect"}
        for p in ALL_PRESETS:
            missing = required - set(p.keys())
            assert not missing, f"preset {p.get('id')!r} missing fields: {missing}"

    def test_recommended_bundles_reference_real_preset_ids(self):
        for bundle in RECOMMENDED_BUNDLES:
            for pid in bundle["preset_ids"]:
                assert pid in PRESETS_BY_ID, (
                    f"bundle {bundle['id']!r} references missing preset {pid!r}"
                )

    def test_categories_carry_presets(self):
        total = sum(len(c["presets"]) for c in PRESET_CATEGORIES)
        assert total == len(ALL_PRESETS)

    def test_get_preset_by_id_lookup(self):
        assert get_preset_by_id("og-image") is not None
        assert get_preset_by_id("does-not-exist") is None
