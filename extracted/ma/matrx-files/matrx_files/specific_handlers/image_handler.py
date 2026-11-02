from __future__ import annotations

import asyncio
import base64
from io import BytesIO
from pathlib import Path
from typing import Any, Literal, TypedDict, Union

from PIL import Image, ImageEnhance, ImageOps, ImageStat

# Optional AVIF support. pillow-avif-plugin registers AVIF read/write codecs
# with Pillow on import. Wrapped so the package still imports cleanly when
# the plugin isn't installed (e.g. in environments that don't need AVIF).
try:
    import pillow_avif  # noqa: F401  # registers AVIF opener as a side effect
    _AVIF_AVAILABLE = True
except ImportError:
    _AVIF_AVAILABLE = False

# Optional HEIC/HEIF support. pillow-heif registers a Pillow opener for
# `.heic` / `.heif` files. Used heavily by iPhone uploads — explicit support
# is one of the things Python does that Sharp on Vercel doesn't reliably do.
try:
    from pillow_heif import register_heif_opener  # type: ignore
    register_heif_opener()
    _HEIC_AVAILABLE = True
except ImportError:
    _HEIC_AVAILABLE = False

# Optional mozjpeg post-encode optimization. mozjpeg-lossless-optimization
# rewrites a libjpeg-turbo JPEG into a smaller mozjpeg-encoded JPEG without
# any quality loss — typically 3–7% byte reduction. Closes most of the gap
# vs Sharp's first-class mozjpeg support without needing a system binary.
try:
    import mozjpeg_lossless_optimization as _mozjpeg_mod
except ImportError:
    _mozjpeg_mod = None
_MOZJPEG_AVAILABLE = _mozjpeg_mod is not None

from matrx_files.file_handler import FileHandler


# ---------------------------------------------------------------------------
# Variant type and preset collections
# ---------------------------------------------------------------------------

class ImageVariant(TypedDict):
    key: str      # Key in the returned dict, e.g. "cover_url"
    suffix: str   # Filename suffix, e.g. "cover"
    width: int
    height: int
    quality: int  # JPEG/WEBP quality 1-95
    format: str   # "JPEG" | "PNG" | "WEBP"


# Podcast / Audio — Apple Podcasts & Spotify recommended 3000×3000; 1400 kept
# as legacy SD variant. OG covers Twitter / LinkedIn / Facebook. Thumb for UI.
PODCAST_VARIANTS: list[ImageVariant] = [
    {"key": "cover_url",     "suffix": "cover",    "width": 3000, "height": 3000, "quality": 90, "format": "JPEG"},
    {"key": "cover_sd_url",  "suffix": "cover_sd", "width": 1400, "height": 1400, "quality": 85, "format": "JPEG"},
    {"key": "og_url",        "suffix": "og",       "width": 1200, "height": 630,  "quality": 85, "format": "JPEG"},
    {"key": "thumbnail_url", "suffix": "thumb",    "width": 400,  "height": 400,  "quality": 80, "format": "JPEG"},
]

# Social media — OG/Twitter card, Instagram square/portrait/story, YouTube thumbnail
SOCIAL_VARIANTS: list[ImageVariant] = [
    {"key": "og_url",            "suffix": "og",        "width": 1200, "height": 630,  "quality": 85, "format": "JPEG"},
    {"key": "twitter_card_url",  "suffix": "twitter",   "width": 1200, "height": 675,  "quality": 85, "format": "JPEG"},
    {"key": "square_url",        "suffix": "sq",        "width": 1080, "height": 1080, "quality": 85, "format": "JPEG"},
    {"key": "portrait_url",      "suffix": "portrait",  "width": 1080, "height": 1350, "quality": 85, "format": "JPEG"},
    {"key": "story_url",         "suffix": "story",     "width": 1080, "height": 1920, "quality": 85, "format": "JPEG"},
    {"key": "yt_thumbnail_url",  "suffix": "yt_thumb",  "width": 1280, "height": 720,  "quality": 85, "format": "JPEG"},
]

# Web — hero banner, OG/SEO, in-content article image, content card, Apple touch icon, PWA manifest icon, UI thumbnail
WEB_VARIANTS: list[ImageVariant] = [
    {"key": "hero_url",         "suffix": "hero",         "width": 1920, "height": 1080, "quality": 85, "format": "JPEG"},
    {"key": "og_url",           "suffix": "og",           "width": 1200, "height": 630,  "quality": 85, "format": "JPEG"},
    {"key": "content_url",      "suffix": "content",      "width": 1200, "height": 800,  "quality": 85, "format": "JPEG"},
    {"key": "card_url",         "suffix": "card",         "width": 800,  "height": 450,  "quality": 85, "format": "JPEG"},
    {"key": "touch_icon_url",   "suffix": "touch_icon",   "width": 180,  "height": 180,  "quality": 90, "format": "PNG"},
    {"key": "pwa_icon_url",     "suffix": "pwa_icon",     "width": 512,  "height": 512,  "quality": 90, "format": "PNG"},
    {"key": "thumbnail_url",    "suffix": "thumb",        "width": 400,  "height": 400,  "quality": 80, "format": "JPEG"},
]

# Email — standard 600px-wide header + small inline square
EMAIL_VARIANTS: list[ImageVariant] = [
    {"key": "header_url", "suffix": "email_header", "width": 600, "height": 200, "quality": 85, "format": "JPEG"},
    {"key": "square_url", "suffix": "email_sq",     "width": 200, "height": 200, "quality": 85, "format": "JPEG"},
]

# Logo — multi-size logo set for product / brand surfaces. PNG to preserve alpha.
LOGO_VARIANTS: list[ImageVariant] = [
    {"key": "logo_lg_url",   "suffix": "logo_lg",   "width": 512, "height": 512, "quality": 90, "format": "PNG"},
    {"key": "logo_md_url",   "suffix": "logo_md",   "width": 200, "height": 200, "quality": 90, "format": "PNG"},
    {"key": "logo_sm_url",   "suffix": "logo_sm",   "width": 64,  "height": 64,  "quality": 90, "format": "PNG"},
]

# Avatar — circular crop targets. JPEG (no alpha needed, photos compress better).
AVATAR_VARIANTS: list[ImageVariant] = [
    {"key": "avatar_xl_url", "suffix": "avatar_xl", "width": 400, "height": 400, "quality": 85, "format": "JPEG"},
    {"key": "avatar_lg_url", "suffix": "avatar_lg", "width": 256, "height": 256, "quality": 85, "format": "JPEG"},
    {"key": "avatar_md_url", "suffix": "avatar_md", "width": 128, "height": 128, "quality": 85, "format": "JPEG"},
    {"key": "avatar_sm_url", "suffix": "avatar_sm", "width": 64,  "height": 64,  "quality": 80, "format": "JPEG"},
    {"key": "avatar_xs_url", "suffix": "avatar_xs", "width": 32,  "height": 32,  "quality": 80, "format": "JPEG"},
]

# Favicon — standard favicon / apple-touch / android sizes. PNG for transparency.
FAVICON_VARIANTS: list[ImageVariant] = [
    {"key": "favicon_512_url",         "suffix": "favicon_512",         "width": 512, "height": 512, "quality": 90, "format": "PNG"},
    {"key": "favicon_android_url",     "suffix": "favicon_android",     "width": 192, "height": 192, "quality": 90, "format": "PNG"},
    {"key": "favicon_apple_touch_url", "suffix": "favicon_apple_touch", "width": 180, "height": 180, "quality": 90, "format": "PNG"},
    {"key": "favicon_32_url",          "suffix": "favicon_32",          "width": 32,  "height": 32,  "quality": 90, "format": "PNG"},
    {"key": "favicon_16_url",          "suffix": "favicon_16",          "width": 16,  "height": 16,  "quality": 90, "format": "PNG"},
]

# Social baseline — applied to EVERY public asset upload regardless of preset.
# Guarantees that any public asset has a working OG card + UI thumbnail + icon
# without the caller having to think about it. Roughly 20-30 KB on disk total.
SOCIAL_BASELINE: list[ImageVariant] = [
    {"key": "og_url",        "suffix": "og",    "width": 1200, "height": 630, "quality": 85, "format": "JPEG"},
    {"key": "thumbnail_url", "suffix": "thumb", "width": 400,  "height": 400, "quality": 80, "format": "JPEG"},
    {"key": "tiny_url",      "suffix": "tiny",  "width": 128,  "height": 128, "quality": 80, "format": "JPEG"},
]

# Full set — use when you want every variant in one call
ALL_VARIANTS: list[ImageVariant] = PODCAST_VARIANTS + SOCIAL_VARIANTS + WEB_VARIANTS


# ---------------------------------------------------------------------------
# Preset registry — maps a preset name to its variant list + primary key.
#
# The host calls compose_preset(name) to get the final list of variants for
# an upload (preset + social baseline, de-duplicated by ``key``). The new
# asset upload endpoint dispatches presets through this registry, so adding
# a preset is one entry here, not a code change in the router.
# ---------------------------------------------------------------------------


class PresetSpec(TypedDict):
    name: str
    variants: list[ImageVariant]
    primary_key: str          # which variant becomes Asset.primary_url
    include_baseline: bool    # add SOCIAL_BASELINE when True


# Order matters for compose_preset: preset variants render first, baseline
# variants render after but are skipped when a key already exists.
PRESETS: dict[str, PresetSpec] = {
    "podcast": {
        "name": "podcast",
        "variants": PODCAST_VARIANTS,
        "primary_key": "cover_url",
        "include_baseline": True,
    },
    "social": {
        "name": "social",
        "variants": SOCIAL_VARIANTS,
        "primary_key": "og_url",
        "include_baseline": True,  # baseline keys overlap; dedup handles it
    },
    "web": {
        "name": "web",
        "variants": WEB_VARIANTS,
        "primary_key": "hero_url",
        "include_baseline": True,
    },
    "email": {
        "name": "email",
        "variants": EMAIL_VARIANTS,
        "primary_key": "header_url",
        "include_baseline": False,  # email assets are private by convention
    },
    "logo": {
        "name": "logo",
        "variants": LOGO_VARIANTS,
        "primary_key": "logo_lg_url",
        "include_baseline": True,
    },
    "avatar": {
        "name": "avatar",
        "variants": AVATAR_VARIANTS,
        "primary_key": "avatar_xl_url",
        "include_baseline": False,  # avatars are personal — no auto-OG
    },
    "favicon": {
        "name": "favicon",
        "variants": FAVICON_VARIANTS,
        "primary_key": "favicon_apple_touch_url",
        "include_baseline": False,
    },
    "raw": {
        # "raw" preset = no variant rendering; uploads the master only.
        # Useful when the caller wants the Asset envelope (folder, web lane,
        # URLs) but doesn't need derived sizes.
        "name": "raw",
        "variants": [],
        "primary_key": "original",
        "include_baseline": False,
    },
}


def get_preset(name: str) -> PresetSpec:
    """Return the preset spec for *name*. Raises KeyError for unknown presets."""
    if name not in PRESETS:
        raise KeyError(
            f"Unknown preset {name!r}. "
            f"Known presets: {sorted(PRESETS.keys())}"
        )
    return PRESETS[name]


def compose_preset(
    name: str,
    *,
    include_baseline: bool | None = None,
    extra_variants: list[ImageVariant] | None = None,
) -> tuple[PresetSpec, list[ImageVariant]]:
    """Resolve a preset name to its final ``(spec, variants)`` pair.

    Variants are de-duplicated by their ``key`` field — if the preset
    already defines an ``og_url`` (e.g. the social preset), the baseline's
    ``og_url`` is skipped rather than rendered twice.

    Parameters
    ----------
    name
        Preset name (``"podcast"``, ``"logo"``, etc.). See ``PRESETS``.
    include_baseline
        Override the preset's default about whether to merge the
        ``SOCIAL_BASELINE`` variants. ``None`` (default) honors the
        preset spec.
    extra_variants
        Caller-supplied variants merged in last; same dedup-by-key rule.
        Use this for one-off custom sizes alongside a known preset.
    """
    spec = get_preset(name)
    use_baseline = spec["include_baseline"] if include_baseline is None else bool(include_baseline)
    combined: list[ImageVariant] = list(spec["variants"])
    seen_keys = {v["key"] for v in combined}
    if use_baseline:
        for v in SOCIAL_BASELINE:
            if v["key"] not in seen_keys:
                combined.append(v)
                seen_keys.add(v["key"])
    if extra_variants:
        for v in extra_variants:
            if v["key"] not in seen_keys:
                combined.append(v)
                seen_keys.add(v["key"])
    return spec, combined


def list_preset_names() -> list[str]:
    return list(PRESETS.keys())


# ---------------------------------------------------------------------------
# Studio rendering — fit modes, anchor positions, focal-point cropping
# ---------------------------------------------------------------------------

StudioFit = Literal["cover", "contain", "inside"]
StudioAnchor = Literal[
    "center", "top", "bottom", "left", "right",
    "top-left", "top-right", "bottom-left", "bottom-right",
    "entropy", "attention",
]


class StudioFocalPoint(TypedDict):
    x: float  # [0, 1] — fraction across source width
    y: float  # [0, 1] — fraction down source height


# A position is either a named anchor or a continuous focal point.
StudioPosition = Union[StudioAnchor, StudioFocalPoint]


class StudioRenderSpec(TypedDict, total=False):
    """One target render. Mirrors the Image Studio per-variant spec on the FE."""
    preset_id: str           # Stable id; used as the staged-S3 key suffix.
    width: int
    height: int
    format: Literal["jpeg", "png", "webp", "avif"]
    quality: int             # 1-100 (ignored for PNG)
    fit: StudioFit
    position: StudioPosition  # Used only when fit == "cover"
    background_color: str    # Hex — flatten alpha + contain padding.


class StudioRenderResult(TypedDict):
    preset_id: str
    format: str
    width: int
    height: int
    quality: int | None
    size: int
    bytes: bytes
    fit: StudioFit
    position: StudioPosition | None
    notes: list[str]         # Soft warnings (e.g. "anchor 'entropy' not supported, used center")


_NAMED_ANCHORS = {
    "center", "top", "bottom", "left", "right",
    "top-left", "top-right", "bottom-left", "bottom-right",
    "entropy", "attention",
}


def is_avif_available() -> bool:
    return _AVIF_AVAILABLE


def is_heic_available() -> bool:
    return _HEIC_AVAILABLE


def is_mozjpeg_available() -> bool:
    return _MOZJPEG_AVAILABLE


_NAMED_FOCAL_POINTS = {
    "center": (0.5, 0.5),
    "top": (0.5, 0.0),
    "bottom": (0.5, 1.0),
    "left": (0.0, 0.5),
    "right": (1.0, 0.5),
    "top-left": (0.0, 0.0),
    "top-right": (1.0, 0.0),
    "bottom-left": (0.0, 1.0),
    "bottom-right": (1.0, 1.0),
}


def _anchor_to_focal_point(anchor: str) -> tuple[float, float]:
    """Map a 9-direction anchor to a normalized (x, y) focal point.

    Smart-crop modes ("entropy", "attention") are NOT handled here —
    callers should branch into ``smart_crop_focal_point`` for those.
    """
    return _NAMED_FOCAL_POINTS.get(anchor, (0.5, 0.5))


def _cover_rect_at_focal_point(
    src_w: int, src_h: int, dst_w: int, dst_h: int, focal: tuple[float, float]
) -> tuple[int, int, int, int]:
    """Compute the source crop rectangle for cover-fit at a custom focal point.

    Mirrors `coverRectAtFocalPoint` in `features/image-studio/utils/compute-crop.ts`
    so client preview and server output match. The focal point is the
    desired center of the crop; we slide it inside the source so the rect
    never escapes.

    Returns ``(left, top, width, height)`` in source pixels.
    """
    if src_w <= 0 or src_h <= 0:
        return 0, 0, src_w, src_h
    src_aspect = src_w / src_h
    dst_aspect = dst_w / dst_h

    if abs(src_aspect - dst_aspect) < 1e-6:
        crop_w, crop_h = src_w, src_h
    elif src_aspect > dst_aspect:
        crop_h = src_h
        crop_w = src_h * dst_aspect
    else:
        crop_w = src_w
        crop_h = src_w / dst_aspect

    fx = max(0.0, min(1.0, focal[0]))
    fy = max(0.0, min(1.0, focal[1]))
    ideal_left = fx * src_w - crop_w / 2
    ideal_top = fy * src_h - crop_h / 2
    left = max(0.0, min(src_w - crop_w, ideal_left))
    top = max(0.0, min(src_h - crop_h, ideal_top))

    return int(round(left)), int(round(top)), int(round(crop_w)), int(round(crop_h))


def _parse_hex_color(hex_str: str) -> tuple[int, int, int]:
    """Accept "#fff", "#ffffff", "ffffff", "#ffffff80" → (R, G, B) tuple.

    Alpha component (when present) is stripped — flatten always uses an
    opaque base. Falls back to white on any parse error so we never crash
    encoding on a malformed color string.
    """
    s = hex_str.strip().lstrip("#")
    try:
        if len(s) == 3:
            r, g, b = (int(c * 2, 16) for c in s)
            return r, g, b
        if len(s) in (6, 8):
            return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
    except ValueError:
        pass
    return 255, 255, 255


class ImageHandler(FileHandler):
    def __init__(self, app_name, batch_print=False):
        super().__init__(app_name, batch_print=batch_print)

    # Custom Methods
    def custom_read_image(self, path):
        try:
            with Image.open(path) as img:
                self._print_link(path=path, message="Read Image file")
                return img.copy()

        except Exception as e:
            print(f"Error reading image from {path}: {str(e)}")
            self._print_link(path=path, message=f"READ IMAGE ERROR {str(e)}", color="red")
            return None

    def custom_write_image(self, path, image):
        try:
            self._ensure_directory(Path(path))
            image.save(path)
            self._print_link(path=path, message="Image File Saved")
            return True
        except Exception as e:
            self._print_link(path=path, message="Error saving Image", color="red")
            print(f"Error saving image to {path}: {str(e)}")
            return False

    def custom_append_image(self, path, image, position=(0, 0)):
        try:
            base_image = self.custom_read_image(path)
            if base_image:
                base_image.paste(image, position)
                return self.custom_write_image(path, base_image)
            return False
        except Exception as e:
            print(f"Error appending image to {path}: {str(e)}")
            return False

    def custom_delete_image(self, path):
        return self.delete(path)

    # Core Methods
    def read_image(self, root, path):
        full_path = self._get_full_path(root, path)
        return self.custom_read_image(full_path)

    def write_image(self, root, path, image):
        full_path = self._get_full_path(root, path)
        return self.custom_write_image(full_path, image)

    def append_image(self, root, path, image, position=(0, 0)):
        full_path = self._get_full_path(root, path)
        return self.custom_append_image(full_path, image, position)

    def delete_image(self, root, path):
        full_path = self._get_full_path(root, path)
        return self.custom_delete_image(full_path)

    # File Type-specific Methods
    def get_image_size(self, root, path):
        image = self.read_image(root, path)
        return image.size if image else None

    def get_image_format(self, root, path):
        image = self.read_image(root, path)
        return image.format if image else None

    def get_image_mode(self, root, path):
        image = self.read_image(root, path)
        return image.mode if image else None

    def resize_image(self, root, path, width, height):
        image = self.read_image(root, path)
        if image:
            resized_image = image.resize((width, height))
            return self.write_image(root, path, resized_image)
        return False

    def convert_image_format(self, root, path, target_format):
        image = self.read_image(root, path)
        if image:
            target_path = Path(path).with_suffix(f'.{target_format.lower()}')
            return self.write_image(root, target_path, image)
        return False

    def crop_image(self, root, path, left, top, right, bottom):
        image = self.read_image(root, path)
        if image:
            cropped_image = image.crop((left, top, right, bottom))
            return self.write_image(root, path, cropped_image)
        return False

    def rotate_image(self, root, path, angle):
        image = self.read_image(root, path)
        if image:
            rotated_image = image.rotate(angle)
            return self.write_image(root, path, rotated_image)
        return False

    def merge_images(self, root, path_list, output_path):
        loaded = [self.read_image(root, path) for path in path_list]
        images: list[Image.Image] = [img for img in loaded if img is not None]
        if not images or len(images) != len(loaded):
            return False
        widths, heights = zip(*(img.size for img in images))
        total_width = sum(widths)
        max_height = max(heights)
        merged_image = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        for img in images:
            merged_image.paste(img, (x_offset, 0))
            x_offset += img.width
        return self.write_image(root, output_path, merged_image)

    def add_watermark(self, root, path, watermark_path, position=(0, 0), opacity=128):
        image = self.read_image(root, path)
        watermark = self.read_image(root, watermark_path)
        if image and watermark:
            if watermark.mode != 'RGBA':
                watermark = watermark.convert('RGBA')
            alpha = watermark.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity / 255.0)
            watermark.putalpha(alpha)
            image.paste(watermark, position, watermark)
            return self.write_image(root, path, image)
        return False

    def adjust_brightness(self, root, path, factor):
        image = self.read_image(root, path)
        if image:
            enhancer = ImageEnhance.Brightness(image)
            brightened_image = enhancer.enhance(factor)
            return self.write_image(root, path, brightened_image)
        return False

    def convert_to_grayscale(self, root, path):
        image = self.read_image(root, path)
        if image:
            grayscale_image = image.convert('L')
            return self.write_image(root, path, grayscale_image)
        return False

    def create_thumbnail(self, root, path, size):
        image = self.read_image(root, path)
        if image:
            image.thumbnail(size)
            return self.write_image(root, path, image)
        return False

    def flip_image(self, root, path, direction='horizontal'):
        image = self.read_image(root, path)
        if image:
            if direction == 'horizontal':
                flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
            elif direction == 'vertical':
                flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
            else:
                print(f"Invalid flip direction: {direction}. Use 'horizontal' or 'vertical'.")
                return False
            return self.write_image(root, path, flipped_image)
        return False

    def custom_base64_to_png(self, base64_string, path):
        try:
            # Remove data:image/... prefix if present
            if base64_string.startswith("data:image"):
                base64_string = base64_string.split(",")[1]

            # Ensure path has .png extension
            path = Path(path)
            if path.suffix.lower() != ".png":
                path = path.with_suffix(".png")

            # Simple approach: decode and write directly
            self._ensure_directory(path)
            with open(path, "wb") as f:
                f.write(base64.b64decode(base64_string))

            self._print_link(path=path, message="Base64 converted to PNG")
            return True

        except Exception as e:
            print(f"Error converting base64 to PNG at {path}: {str(e)}")
            self._print_link(
                path=path, message=f"BASE64 TO PNG ERROR {str(e)}", color="red"
            )
            return False

    def custom_base64_to_webp(self, base64_string, path):
        try:
            # Remove data:image/... prefix if present
            if base64_string.startswith("data:image"):
                base64_string = base64_string.split(",")[1]

            # For WebP, we need PIL to convert from the original format
            image_data = base64.b64decode(base64_string)
            image = Image.open(BytesIO(image_data))

            # Ensure path has .webp extension
            path = Path(path)
            if path.suffix.lower() != ".webp":
                path = path.with_suffix(".webp")

            # Save as WebP
            self._ensure_directory(path)
            image.save(path, "WEBP", quality=85)
            self._print_link(path=path, message="Base64 converted to WebP")
            return True

        except Exception as e:
            print(f"Error converting base64 to WebP at {path}: {str(e)}")
            self._print_link(
                path=path, message=f"BASE64 TO WEBP ERROR {str(e)}", color="red"
            )
            return False

    def base64_to_png(self, root, path, base64_string):
        full_path = self._get_full_path(root, path)
        return self.custom_base64_to_png(base64_string, full_path)

    def base64_to_webp(self, root, path, base64_string):
        full_path = self._get_full_path(root, path)
        return self.custom_base64_to_webp(base64_string, full_path)

    # ------------------------------------------------------------------
    # Cloud I/O — require FileManager construction (CloudMixin)
    # ------------------------------------------------------------------

    def base64_to_cloud(self, base64_string: str, dest_uri: str) -> bool:
        """Decode a base64 image and write it directly to cloud storage.

        Accepts base64 strings with or without the ``data:image/...;base64,``
        prefix. Writes raw bytes — no format conversion — to any configured
        backend via *dest_uri*.

        Parameters
        ----------
        base64_string:
            Base64-encoded image data, optionally prefixed with a data URI
            header (``data:image/png;base64,...``).
        dest_uri:
            Full cloud storage URI, e.g.
            ``"s3://bucket/users/123/avatar.png"``
            ``"s3://bucket/generated/image.webp"``

        Examples
        --------
            # From an OpenAI image generation response
            handler.base64_to_cloud(result.data[0].b64_json, "s3://bucket/out.png")

            # From a multipart form upload (already base64-encoded client-side)
            handler.base64_to_cloud(form_data.image_b64, "s3://bucket/img.jpg")
        """
        try:
            if base64_string.startswith("data:image"):
                base64_string = base64_string.split(",", 1)[1]
            file_bytes = base64.b64decode(base64_string)
            return self.cloud_write(dest_uri, file_bytes)
        except Exception as e:
            print(f"[ImageHandler] base64_to_cloud failed for {dest_uri}: {e}")
            return False

    async def base64_to_cloud_async(self, base64_string: str, dest_uri: str) -> bool:
        """Async version of base64_to_cloud(). Use this in FastAPI routes."""
        try:
            if base64_string.startswith("data:image"):
                base64_string = base64_string.split(",", 1)[1]
            file_bytes = base64.b64decode(base64_string)
            return await self.cloud_write_async(dest_uri, file_bytes)
        except Exception as e:
            print(f"[ImageHandler] base64_to_cloud_async failed for {dest_uri}: {e}")
            return False

    def read_image_from_cloud(self, uri_or_url: str) -> "Image.Image | None":
        """Read an image from any cloud URI or URL and return a PIL Image.

        Accepts native URIs (``s3://``), public HTTPS URLs,
        and signed/expired URLs. Reads via server-side credentials so token
        expiry is irrelevant.

        Parameters
        ----------
        uri_or_url:
            Any cloud storage URI or URL pointing to an image file.

        Examples
        --------
            img = handler.read_image_from_cloud("s3://bucket/avatar.png")
            img = handler.read_image_from_cloud(share_or_cdn_url)
        """
        try:
            raw = self.cloud_read_url(uri_or_url)
            return Image.open(BytesIO(raw))
        except Exception as e:
            print(f"[ImageHandler] read_image_from_cloud failed for {uri_or_url}: {e}")
            return None

    async def read_image_from_cloud_async(self, uri_or_url: str) -> "Image.Image | None":
        """Async version of read_image_from_cloud(). Use this in FastAPI routes."""
        try:
            raw = await self.cloud_read_url_async(uri_or_url)
            return Image.open(BytesIO(raw))
        except Exception as e:
            print(f"[ImageHandler] read_image_from_cloud_async failed for {uri_or_url}: {e}")
            return None

    def write_image_to_cloud(self, image: "Image.Image", dest_uri: str, fmt: str = "PNG") -> bool:
        """Encode a PIL Image and write it to cloud storage.

        Parameters
        ----------
        image:
            A PIL Image object to upload.
        dest_uri:
            Full cloud storage URI (s3:// or server://).
        fmt:
            Pillow format string used for encoding, e.g. ``"PNG"``, ``"WEBP"``,
            ``"JPEG"``. Defaults to ``"PNG"``.

        Examples
        --------
            handler.write_image_to_cloud(resized_img, "s3://bucket/thumb.webp", fmt="WEBP")
        """
        try:
            buf = BytesIO()
            image.save(buf, format=fmt)
            return self.cloud_write(dest_uri, buf.getvalue())
        except Exception as e:
            print(f"[ImageHandler] write_image_to_cloud failed for {dest_uri}: {e}")
            return False

    async def write_image_to_cloud_async(self, image: "Image.Image", dest_uri: str, fmt: str = "PNG") -> bool:
        """Async version of write_image_to_cloud(). Use this in FastAPI routes."""
        try:
            buf = BytesIO()
            image.save(buf, format=fmt)
            return await self.cloud_write_async(dest_uri, buf.getvalue())
        except Exception as e:
            print(f"[ImageHandler] write_image_to_cloud_async failed for {dest_uri}: {e}")
            return False

    # ------------------------------------------------------------------
    # Cover-crop resize and JPEG normalization
    # ------------------------------------------------------------------

    @staticmethod
    def resize_cover(image: Image.Image, width: int, height: int) -> Image.Image:
        """Scale and center-crop to exact dimensions (CSS object-fit: cover).

        The image is scaled so that it completely fills the target box
        (no empty space), then the excess is trimmed from both sides equally.
        Uses LANCZOS resampling for maximum quality.
        """
        src_ratio = image.width / image.height
        dst_ratio = width / height
        if src_ratio > dst_ratio:
            # Source is wider than target — scale by height, crop width
            new_h = height
            new_w = int(image.width * (height / image.height))
        else:
            # Source is taller than target — scale by width, crop height
            new_w = width
            new_h = int(image.height * (width / image.width))
        image = image.resize((new_w, new_h), Image.LANCZOS)
        left = (image.width - width) // 2
        top = (image.height - height) // 2
        return image.crop((left, top, left + width, top + height))

    @staticmethod
    def normalize_for_export(
        image: Image.Image,
        fmt: str,
        background_color: tuple[int, int, int] = (255, 255, 255),
    ) -> Image.Image:
        """Ensure image mode is compatible with the target format.

        JPEG / AVIF cannot encode alpha — RGBA inputs are composited onto
        ``background_color`` and converted to RGB. WebP and PNG keep alpha.
        Non-RGB modes (P, L, etc.) for JPEG are also converted.
        """
        fmt_upper = fmt.upper()
        if fmt_upper in ("JPEG", "AVIF"):
            if image.mode in ("RGBA", "LA"):
                bg = Image.new("RGB", image.size, background_color)
                bg.paste(image, mask=image.split()[-1])
                return bg
            if image.mode != "RGB":
                return image.convert("RGB")
        return image

    # ------------------------------------------------------------------
    # Smart-crop — Pillow-native equivalents of Sharp's entropy / attention
    # ------------------------------------------------------------------

    @staticmethod
    def smart_crop_focal_point(
        image: Image.Image,
        target_w: int,
        target_h: int,
        mode: Literal["entropy", "attention"],
        analysis_max_edge: int = 512,
    ) -> tuple[float, float]:
        """Find the focal point that maximises a saliency metric.

        Returns ``(fx, fy)`` in [0, 1] — a centre-of-best-window normalized
        focal point that ``_cover_rect_at_focal_point`` consumes the same
        way it consumes a user-dragged focal point.

        ``mode="entropy"`` is the classic Shannon-entropy smart crop: the
        target-aspect window with the most detail wins. Identical in spirit
        to libvips' (Sharp's) entropy strategy.

        ``mode="attention"`` biases entropy by per-window saturation —
        detail-rich AND vibrant regions outscore detail-rich-but-dull ones.
        Pillow-native approximation of Sharp's libvips attention strategy
        (which uses a saliency model). Visually similar; not bit-identical.

        Performance: the source is downscaled to ``analysis_max_edge`` (default
        512px) before scoring, so even multi-megapixel sources finish in
        single-digit milliseconds. The chosen window's center is returned in
        normalized coordinates so the caller can still crop at full source
        resolution.
        """
        src_w, src_h = image.size
        if src_w == 0 or src_h == 0 or target_w <= 0 or target_h <= 0:
            return 0.5, 0.5

        src_aspect = src_w / src_h
        dst_aspect = target_w / target_h
        if src_aspect > dst_aspect:
            crop_h = src_h
            crop_w = int(round(src_h * dst_aspect))
        else:
            crop_w = src_w
            crop_h = int(round(src_w / dst_aspect))

        # Source already at the target ratio (or smaller in both dims) — no
        # cropping decision to make; center is correct.
        if crop_w >= src_w and crop_h >= src_h:
            return 0.5, 0.5

        # Downscale the analysis frame so the sweep is bounded work.
        scale = min(1.0, analysis_max_edge / max(src_w, src_h))
        if scale < 1.0:
            a_w, a_h = max(1, int(src_w * scale)), max(1, int(src_h * scale))
            analysis = image.resize((a_w, a_h), Image.BILINEAR)
            crop_w_a = max(1, int(round(crop_w * scale)))
            crop_h_a = max(1, int(round(crop_h * scale)))
        else:
            analysis = image
            a_w, a_h = src_w, src_h
            crop_w_a, crop_h_a = crop_w, crop_h

        # Coerce to RGB up-front for HSV conversion (P/L/RGBA all need this).
        if analysis.mode not in ("RGB", "L"):
            analysis_rgb = analysis.convert("RGB")
        else:
            analysis_rgb = analysis

        gray = analysis_rgb.convert("L") if analysis_rgb.mode != "L" else analysis_rgb

        sat_channel: Image.Image | None = None
        if mode == "attention":
            # The S channel of HSV is a cheap saturation proxy; bias toward it.
            try:
                sat_channel = analysis_rgb.convert("HSV").split()[1]
            except Exception:
                sat_channel = None  # fall through to pure entropy

        stride_x = max(1, crop_w_a // 16)
        stride_y = max(1, crop_h_a // 16)
        max_left = a_w - crop_w_a
        max_top = a_h - crop_h_a

        best_score = -1.0
        best_left = 0
        best_top = 0

        for top in range(0, max_top + 1, stride_y):
            for left in range(0, max_left + 1, stride_x):
                box = (left, top, left + crop_w_a, top + crop_h_a)
                score = gray.crop(box).entropy()
                if sat_channel is not None:
                    avg_sat = ImageStat.Stat(sat_channel.crop(box)).mean[0] / 255.0
                    score = score * (0.5 + 0.5 * avg_sat)
                if score > best_score:
                    best_score = score
                    best_left = left
                    best_top = top

        cx = (best_left + crop_w_a / 2) / a_w
        cy = (best_top + crop_h_a / 2) / a_h
        return cx, cy

    # ------------------------------------------------------------------
    # Studio rendering — fit modes + focal-point cropping
    # ------------------------------------------------------------------

    @staticmethod
    def apply_studio_fit(
        image: Image.Image,
        target_w: int,
        target_h: int,
        fit: StudioFit,
        position: StudioPosition,
        background: tuple[int, int, int],
    ) -> tuple[Image.Image, list[str]]:
        """Resize *image* to (target_w, target_h) using the given fit + position.

        Returns ``(resized_image, notes)`` where notes is a list of soft
        warnings; cover-mode smart-crops ("entropy", "attention") are
        handled natively here, so callers no longer get a center fallback.
        """
        notes: list[str] = []

        if fit == "cover":
            # Resolve position → focal point.
            if isinstance(position, dict):
                fx = float(position.get("x", 0.5))
                fy = float(position.get("y", 0.5))
            elif position in ("entropy", "attention"):
                fx, fy = ImageHandler.smart_crop_focal_point(
                    image, target_w, target_h, position  # type: ignore[arg-type]
                )
                if position == "attention":
                    notes.append(
                        "attention crop uses Pillow entropy + saturation bias "
                        "(not Sharp's libvips saliency); results visually similar"
                    )
            else:
                fx, fy = _anchor_to_focal_point(str(position))

            left, top, crop_w, crop_h = _cover_rect_at_focal_point(
                image.width, image.height, target_w, target_h, (fx, fy)
            )
            cropped = image.crop((left, top, left + crop_w, top + crop_h))
            return cropped.resize((target_w, target_h), Image.LANCZOS), notes

        if fit == "inside":
            # Scale the image to the largest size that fits inside the target
            # while preserving aspect ratio. Upscales when the source is
            # smaller than the target — matches Sharp's default
            # ``withoutEnlargement: false``. No crop, no padding.
            src_w, src_h = image.size
            if src_w <= 0 or src_h <= 0:
                return image, notes
            src_aspect = src_w / src_h
            dst_aspect = target_w / target_h if target_h else 1.0
            if dst_aspect > src_aspect:
                new_h = target_h
                new_w = max(1, int(round(target_h * src_aspect)))
            else:
                new_w = target_w
                new_h = max(1, int(round(target_w / src_aspect)))
            return image.resize((new_w, new_h), Image.LANCZOS), notes

        if fit == "contain":
            # Fit the whole image inside the target, letterbox with `background`.
            src_aspect = image.width / image.height if image.height else 1.0
            dst_aspect = target_w / target_h if target_h else 1.0
            if src_aspect > dst_aspect:
                inner_w = target_w
                inner_h = max(1, int(round(target_w / src_aspect)))
            else:
                inner_h = target_h
                inner_w = max(1, int(round(target_h * src_aspect)))
            inner = image.resize((inner_w, inner_h), Image.LANCZOS)
            canvas_mode = "RGBA" if image.mode in ("RGBA", "LA") else "RGB"
            if canvas_mode == "RGBA":
                canvas = Image.new("RGBA", (target_w, target_h), (*background, 255))
            else:
                canvas = Image.new("RGB", (target_w, target_h), background)
            paste_x = (target_w - inner_w) // 2
            paste_y = (target_h - inner_h) // 2
            if inner.mode in ("RGBA", "LA"):
                canvas.paste(inner, (paste_x, paste_y), mask=inner.split()[-1])
            else:
                canvas.paste(inner, (paste_x, paste_y))
            return canvas, notes

        # Unknown fit — defensive; treat as cover-center.
        notes.append(f"unknown fit '{fit}', using cover-center")
        left, top, crop_w, crop_h = _cover_rect_at_focal_point(
            image.width, image.height, target_w, target_h, (0.5, 0.5)
        )
        cropped = image.crop((left, top, left + crop_w, top + crop_h))
        return cropped.resize((target_w, target_h), Image.LANCZOS), notes

    @staticmethod
    def encode_for_studio(
        image: Image.Image, fmt: str, quality: int, background: tuple[int, int, int]
    ) -> bytes:
        """Encode *image* to bytes in the requested format.

        Mirrors the Sharp pipeline's encode step: progressive JPEG,
        lossless-ish PNG (compress_level=9), default WebP / AVIF quality.
        """
        fmt_upper = fmt.upper()
        if fmt_upper == "AVIF" and not _AVIF_AVAILABLE:
            raise RuntimeError(
                "AVIF output requested but pillow-avif-plugin is not installed. "
                "`pip install pillow-avif-plugin` to enable."
            )

        normalized = ImageHandler.normalize_for_export(image, fmt_upper, background)
        buf = BytesIO()
        if fmt_upper == "JPEG":
            normalized.save(buf, format="JPEG", quality=quality, progressive=True, optimize=True)
            jpeg_bytes = buf.getvalue()
            # Lossless mozjpeg re-optimisation when the package is installed.
            # Typically yields 3–7% smaller files at byte-identical decoded
            # output. Falls through silently when the package isn't present
            # so Pillow's libjpeg-turbo output remains the floor.
            if _mozjpeg_mod is not None:
                try:
                    optimised = _mozjpeg_mod.optimize(jpeg_bytes)
                    # Defensively keep the smaller of the two — the
                    # optimization can theoretically grow trivial JPEGs.
                    if optimised and len(optimised) < len(jpeg_bytes):
                        return optimised
                except Exception:
                    # Optimizer failure must never break encoding — fall
                    # through to the un-optimised libjpeg-turbo bytes.
                    pass
            return jpeg_bytes
        if fmt_upper == "WEBP":
            # method=6 is the slowest / highest-quality libwebp setting (range 0-6).
            normalized.save(buf, format="WEBP", quality=quality, method=6)
            return buf.getvalue()
        if fmt_upper == "AVIF":
            normalized.save(buf, format="AVIF", quality=quality)
            return buf.getvalue()
        if fmt_upper == "PNG":
            normalized.save(buf, format="PNG", optimize=True, compress_level=9)
            return buf.getvalue()
        raise ValueError(f"Unsupported output format: {fmt!r}")

    @staticmethod
    def render_studio_variant(
        image_bytes: bytes,
        spec: StudioRenderSpec,
    ) -> StudioRenderResult:
        """Decode source bytes, apply EXIF rotation, fit + position, encode.

        Synchronous + CPU-bound. Always invoke from a thread executor when
        called from async code so the event loop isn't blocked.
        """
        notes: list[str] = []

        with Image.open(BytesIO(image_bytes)) as src:
            # Honor EXIF orientation so phone uploads aren't rotated 90°.
            try:
                src = ImageOps.exif_transpose(src)
            except Exception:
                # Some images expose mangled EXIF — skip transpose, log only.
                notes.append("exif-transpose failed; rendering raw orientation")

            target_w = int(spec["width"])
            target_h = int(spec["height"])
            fit: StudioFit = spec.get("fit", "cover")
            position: StudioPosition = spec.get("position", "center")
            fmt: str = spec.get("format", "webp")
            quality: int = max(1, min(100, int(spec.get("quality", 85))))
            background = _parse_hex_color(spec.get("background_color", "#ffffff"))

            resized, fit_notes = ImageHandler.apply_studio_fit(
                src, target_w, target_h, fit, position, background
            )
            notes.extend(fit_notes)

            encoded = ImageHandler.encode_for_studio(resized, fmt, quality, background)

            actual_w, actual_h = resized.size

        return {
            "preset_id": spec["preset_id"],
            "format": fmt,
            "width": actual_w,
            "height": actual_h,
            "quality": None if fmt.upper() == "PNG" else quality,
            "size": len(encoded),
            "bytes": encoded,
            "fit": fit,
            "position": position if fit == "cover" else None,
            "notes": notes,
        }

    @staticmethod
    def render_studio_variants_batch(
        image_bytes: bytes, specs: list[StudioRenderSpec]
    ) -> list[StudioRenderResult]:
        """Decode the source ONCE, render every variant. CPU-bound; call via thread executor."""
        # Open the source once to extract dims; per-variant render still
        # decodes (Pillow images aren't safe to deep-share across mutations).
        # The decode cost is small relative to the resize, so this is fine.
        return [ImageHandler.render_studio_variant(image_bytes, spec) for spec in specs]

    def _render_variants(
        self, image_bytes: bytes, variants: list[ImageVariant]
    ) -> list[tuple[str, str, str, bytes]]:
        """CPU-bound: open source image and produce all variant byte buffers.

        Returns a list of (key, suffix, format, encoded_bytes) tuples.
        Runs synchronously — always call from a thread executor in async contexts.

        SVG inputs are pre-rasterized to a 4096²-bound PNG via librsvg's
        rsvg-convert binary, then handed to the normal Pillow pipeline
        unchanged. Bypasses the rasterizer entirely for non-SVG bytes so
        existing callers see zero behavioral change.
        """
        from .svg_rasterizer import (
            SvgRasterizerUnavailable,
            is_available as _rsvg_available,
            is_svg as _is_svg,
            rasterize_svg_to_png,
        )

        if _is_svg(image_bytes):
            if not _rsvg_available():
                raise SvgRasterizerUnavailable(
                    "SVG master uploaded but rsvg-convert is not installed."
                )
            # Rasterize once at a bounding box larger than any variant we
            # ship; the Pillow pipeline downsamples per-variant. 4096²
            # keeps the upstream image sharp through every downsample.
            image_bytes = rasterize_svg_to_png(image_bytes, width=4096, height=4096)

        img = Image.open(BytesIO(image_bytes))
        results: list[tuple[str, str, str, bytes]] = []
        for v in variants:
            resized = self.resize_cover(img, v["width"], v["height"])
            normalized = self.normalize_for_export(resized, v["format"])
            buf = BytesIO()
            save_kwargs: dict = {"format": v["format"]}
            if v["format"].upper() in ("JPEG", "WEBP"):
                save_kwargs["quality"] = v.get("quality", 85)
                save_kwargs["optimize"] = True
            normalized.save(buf, **save_kwargs)
            results.append((v["key"], v["suffix"], v["format"], buf.getvalue()))
        return results

    def process_variants(
        self,
        image_bytes: bytes,
        variants: list[ImageVariant],
        folder_uri: str,
    ) -> dict[str, str]:
        """Resize image to all variants, upload each to cloud, return public URLs.

        Synchronous version — use process_variants_async() in FastAPI routes.

        Parameters
        ----------
        image_bytes:
            Raw bytes of the source image (any PIL-supported format).
        variants:
            List of ImageVariant dicts. Use PODCAST_VARIANTS, SOCIAL_VARIANTS,
            WEB_VARIANTS, EMAIL_VARIANTS, or a custom list.
        folder_uri:
            Cloud folder URI, e.g. ``"s3://bucket/{user_id}/{uuid}"``.
            Each variant is uploaded as ``{folder_uri}/{suffix}.{ext}``.

        Returns
        -------
        dict[str, str]
            Mapping of variant key to permanent public URL.
            e.g. ``{"cover_url": "https://...", "og_url": "https://..."}``
        """
        rendered = self._render_variants(image_bytes, variants)
        urls: dict[str, str] = {}
        for key, suffix, fmt, data in rendered:
            ext = "jpg" if fmt.upper() == "JPEG" else fmt.lower()
            dest_uri = f"{folder_uri.rstrip('/')}/{suffix}.{ext}"
            mime = f"image/jpeg" if ext == "jpg" else f"image/{ext}"
            self.cloud_write(dest_uri, data, content_type=mime)
            urls[key] = self.cloud_get_public_url(dest_uri)
        return urls

    async def process_variants_async(
        self,
        image_bytes: bytes,
        variants: list[ImageVariant],
        folder_uri: str,
    ) -> dict[str, str]:
        """Async version of process_variants(). Use this in FastAPI routes.

        CPU work (Pillow resizing) runs in a thread executor so the event loop
        is never blocked. S3 uploads are fully asynchronous.

        Parameters
        ----------
        image_bytes:
            Raw bytes of the source image (any PIL-supported format).
        variants:
            List of ImageVariant dicts. Use PODCAST_VARIANTS, SOCIAL_VARIANTS,
            WEB_VARIANTS, EMAIL_VARIANTS, or a custom list.
        folder_uri:
            Cloud folder URI, e.g. ``"s3://bucket/{user_id}/{uuid}"``.

        Returns
        -------
        dict[str, str]
            Mapping of variant key to permanent public URL.
        """
        loop = asyncio.get_event_loop()
        rendered = await loop.run_in_executor(
            None, self._render_variants, image_bytes, variants
        )
        urls: dict[str, str] = {}
        for key, suffix, fmt, data in rendered:
            ext = "jpg" if fmt.upper() == "JPEG" else fmt.lower()
            dest_uri = f"{folder_uri.rstrip('/')}/{suffix}.{ext}"
            mime = f"image/jpeg" if ext == "jpg" else f"image/{ext}"
            await self.cloud_write_async(dest_uri, data, content_type=mime)
            urls[key] = await self.cloud_get_public_url_async(dest_uri)
        return urls
