"""Forcing-function tests for ``read_image_metadata``.

Every fixture here is a REAL image file, encoded by Pillow in-test with known
EXIF written into it, then decoded by the production reader from the resulting
bytes. Nothing about the reader is stubbed: if the IFD walk, the GPS sign
convention or the datetime parse breaks, these fail. The assertions are against
values the test PUT IN the file, so a reader that silently returns ``None`` for
everything — the exact way this class of code rots — cannot pass.
"""

from __future__ import annotations

import io

import pytest
from PIL import Image
from PIL.TiffImagePlugin import IFDRational as R

from matrx_files.specific_handlers.image_ops import read_image_metadata

MAKE = "Matrx Test Camera Co"
MODEL = "MX-1000"
SOFTWARE = "MatrxTestHarness 1.0"
LENS = "MX 24mm f/1.4"
CAPTURED = "2026:03:04 05:06:07"


def _jpeg_with_exif(
    *, lat_ref: str = "N", lon_ref: str = "W", size: tuple[int, int] = (64, 48)
) -> bytes:
    """A real JPEG carrying known IFD0, Exif-IFD and GPS-IFD tags.

    San Francisco when (N, W): 37°46'29.88" N, 122°24'31.32" W.
    """
    image = Image.new("RGB", size, (10, 120, 60))
    exif = image.getexif()
    exif[0x010F] = MAKE
    exif[0x0110] = MODEL
    exif[0x0131] = SOFTWARE
    exif[0x0112] = 1
    exif_ifd = exif.get_ifd(0x8769)
    exif_ifd[0x9003] = CAPTURED
    exif_ifd[0x9004] = "2026:03:04 05:06:08"
    exif_ifd[0xA434] = LENS
    gps = exif.get_ifd(0x8825)
    gps[1] = lat_ref
    gps[2] = (R(37, 1), R(46, 1), R(2988, 100))
    gps[3] = lon_ref
    gps[4] = (R(122, 1), R(24, 1), R(3132, 100))
    gps[5] = 0
    gps[6] = R(152, 1)
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", exif=exif)
    return buffer.getvalue()


def _jpeg_stripped() -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (64, 48), (1, 2, 3)).save(buffer, format="JPEG")
    return buffer.getvalue()


def _png() -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (10, 10), (9, 9, 9)).save(buffer, format="PNG")
    return buffer.getvalue()


class TestKnownExif:
    def test_camera_software_and_lens_come_back(self):
        report = read_image_metadata(_jpeg_with_exif())
        assert report["camera_make"] == MAKE
        assert report["camera_model"] == MODEL
        assert report["software"] == SOFTWARE
        assert report["lens_model"] == LENS, "LensModel lives in the Exif IFD, not IFD0"
        assert report["orientation"] == 1

    def test_capture_time_is_parsed_and_the_raw_string_is_kept(self):
        report = read_image_metadata(_jpeg_with_exif())
        assert report["datetime_original"] == "2026-03-04T05:06:07"
        assert report["datetime_original_text"] == CAPTURED
        assert report["datetime_digitized"] == "2026-03-04T05:06:08"

    def test_dimensions_and_format(self):
        report = read_image_metadata(_jpeg_with_exif(size=(120, 90)))
        assert (report["width"], report["height"]) == (120, 90)
        assert report["format"] == "JPEG"
        assert report["mime_type"] == "image/jpeg"
        assert report["color_mode"] == "RGB"

    def test_raw_tag_table_is_populated_and_named(self):
        report = read_image_metadata(_jpeg_with_exif())
        assert report["tag_count"] >= 10
        assert report["raw_tags"]["Make"] == MAKE
        # GPSTAGS names already carry the GPS prefix — never "GPSGPSLatitude".
        assert "GPSLatitude" in report["raw_tags"]
        assert not any(key.startswith("GPSGPS") for key in report["raw_tags"])

    def test_report_is_json_serialisable(self):
        import json

        json.dumps(read_image_metadata(_jpeg_with_exif()))


class TestGps:
    def test_north_west_is_positive_latitude_negative_longitude(self):
        report = read_image_metadata(_jpeg_with_exif(lat_ref="N", lon_ref="W"))
        assert report["gps_latitude"] == pytest.approx(37.7749667, abs=1e-6)
        assert report["gps_longitude"] == pytest.approx(-122.4087, abs=1e-6)
        assert report["gps_altitude_m"] == pytest.approx(152.0)

    def test_south_east_flips_both_signs(self):
        """The hemisphere letter is the whole ballgame: ignore it and every
        southern-hemisphere photo lands in the wrong half of the planet."""
        report = read_image_metadata(_jpeg_with_exif(lat_ref="S", lon_ref="E"))
        assert report["gps_latitude"] == pytest.approx(-37.7749667, abs=1e-6)
        assert report["gps_longitude"] == pytest.approx(122.4087, abs=1e-6)


class TestStrippedSignal:
    def test_exif_present_is_not_stripped(self):
        report = read_image_metadata(_jpeg_with_exif())
        assert report["has_exif"] is True
        assert report["metadata_stripped"] is False
        assert report["containers"]["exif"] is True

    def test_jpeg_without_exif_is_reported_stripped(self):
        report = read_image_metadata(_jpeg_stripped())
        assert report["has_exif"] is False
        assert report["metadata_stripped"] is True
        assert "normally carries it" in report["stripped_note"]
        assert "not a verdict" in report["stripped_note"]

    def test_png_absence_is_null_not_false_and_not_true(self):
        """PNG does not normally carry EXIF, so neither True nor False would be
        true — the reader must decline to answer rather than pick one."""
        report = read_image_metadata(_png())
        assert report["has_exif"] is False
        assert report["metadata_stripped"] is None
        assert "says nothing either way" in report["stripped_note"]


class TestFailures:
    def test_non_image_bytes_raise_rather_than_return_an_empty_report(self):
        with pytest.raises(ValueError, match="could not decode"):
            read_image_metadata(b"<!doctype html><html>not an image</html>")

    def test_empty_bytes_raise(self):
        with pytest.raises(ValueError, match="empty byte string"):
            read_image_metadata(b"")
