import base64
import io
import os
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from abstra_internals.controllers.main import (
    READ_DOCUMENT_MAX_IMAGE_DIMENSION,
    MainController,
)


class TestReadDocumentImageFidelity(unittest.TestCase):
    def setUp(self):
        # The image helpers only touch `self` + the file path, so bypass the
        # heavy MainController.__init__ (migrations, fs setup, etc.).
        self.controller = object.__new__(MainController)
        self.tempdir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def _photo_png(self, size=(2400, 1600), name="image.png") -> Path:
        # Noisy RGB content, like a phone photo: stored large as PNG.
        img = Image.frombytes("RGB", size, os.urandom(size[0] * size[1] * 3))
        p = self.tmp / name
        img.save(p, format="PNG")
        return p

    def test_large_photo_is_downscaled_and_jpeg_encoded(self):
        p = self._photo_png(size=(2400, 1600))
        raw_bytes = p.stat().st_size

        result = self.controller._read_image_file(p)

        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result["mimeType"], "image/jpeg")
        self.assertTrue(result["dataUri"].startswith("data:image/jpeg;base64,"))

        out = base64.b64decode(result["dataUri"].split(",", 1)[1])
        self.assertLess(len(out), raw_bytes)  # smaller than the original upload
        with Image.open(io.BytesIO(out)) as got:
            self.assertEqual(got.format, "JPEG")
            self.assertLessEqual(max(got.size), READ_DOCUMENT_MAX_IMAGE_DIMENSION)

    def test_rgba_png_is_flattened_to_jpeg(self):
        p = self.tmp / "logo.png"
        Image.new("RGBA", (300, 300), (255, 0, 0, 128)).save(p, format="PNG")

        result = self.controller._read_image_file(p)

        assert result is not None
        self.assertEqual(result["mimeType"], "image/jpeg")

    def test_unreadable_file_falls_back_to_raw_passthrough(self):
        p = self.tmp / "broken.png"
        p.write_bytes(b"not really a png")

        result = self.controller._read_image_file(p)

        # PIL can't decode it → keep prior behavior (raw bytes, ext-based mime)
        assert result is not None
        self.assertEqual(result["mimeType"], "image/png")
        out = base64.b64decode(result["dataUri"].split(",", 1)[1])
        self.assertEqual(out, b"not really a png")


if __name__ == "__main__":
    unittest.main()
