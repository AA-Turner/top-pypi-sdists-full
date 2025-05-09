#
# openslide-python - Python bindings for the OpenSlide library
#
# Copyright (c) 2016-2024 Benjamin Gilbert
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of version 2.1 of the GNU Lesser General Public License
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library.  If not, see <https://www.gnu.org/licenses/>.
#

from __future__ import annotations

import sys
import unittest

from PIL import Image
from common import file_path

from openslide import ImageSlide, OpenSlideCache, OpenSlideError, lowlevel


class TestImageWithoutOpening(unittest.TestCase):
    def test_detect_format(self) -> None:
        self.assertTrue(ImageSlide.detect_format(file_path('__missing_file')) is None)
        self.assertTrue(ImageSlide.detect_format(file_path('../setup.py')) is None)
        self.assertEqual(ImageSlide.detect_format(file_path('boxes.png')), 'PNG')

    def test_open(self) -> None:
        self.assertRaises(OSError, lambda: ImageSlide(file_path('__does_not_exist')))
        self.assertRaises(OSError, lambda: ImageSlide(file_path('../setup.py')))

    def test_open_image(self) -> None:
        # passing PIL.Image to ImageSlide
        with Image.open(file_path('boxes.png')) as img:
            with ImageSlide(img) as osr:
                self.assertEqual(osr.dimensions, (300, 250))
                self.assertEqual(repr(osr), 'ImageSlide(%r)' % img)

    @unittest.skipUnless(
        sys.getfilesystemencoding() == 'utf-8',
        'Python filesystem encoding is not UTF-8',
    )
    def test_unicode_path(self) -> None:
        path = file_path('😐.png')
        for arg in path, str(path):
            self.assertEqual(ImageSlide.detect_format(arg), 'PNG')
            self.assertEqual(ImageSlide(arg).dimensions, (300, 250))

    def test_unicode_path_bytes(self) -> None:
        arg = str(file_path('😐.png')).encode('UTF-8')
        self.assertEqual(ImageSlide.detect_format(arg), 'PNG')
        self.assertEqual(ImageSlide(arg).dimensions, (300, 250))

    def test_operations_on_closed_handle(self) -> None:
        with Image.open(file_path('boxes.png')) as img:
            osr = ImageSlide(img)
            osr.close()
            self.assertRaises(
                ValueError, lambda: osr.read_region((0, 0), 0, (100, 100))
            )
            self.assertRaises(ValueError, lambda: osr.level_dimensions)
            # If an Image is passed to the constructor, ImageSlide.close()
            # shouldn't close it
            self.assertEqual(img.getpixel((0, 0)), 3)

    def test_context_manager(self) -> None:
        osr = ImageSlide(file_path('boxes.png'))
        with osr:
            pass
        self.assertRaises(ValueError, lambda: osr.read_region((0, 0), 0, (100, 100)))
        self.assertRaises(ValueError, lambda: osr.level_dimensions)


class _Abstract:
    # nested class to prevent the test runner from finding it
    class SlideTest(unittest.TestCase):
        FILENAME: str | None = None

        def setUp(self) -> None:
            assert self.FILENAME is not None
            self.osr = ImageSlide(file_path(self.FILENAME))

        def tearDown(self) -> None:
            self.osr.close()


class TestImage(_Abstract.SlideTest):
    FILENAME = 'boxes.png'

    def test_repr(self) -> None:
        self.assertEqual(repr(self.osr), 'ImageSlide(%r)' % file_path('boxes.png'))

    def test_metadata(self) -> None:
        self.assertEqual(self.osr.level_count, 1)
        self.assertEqual(self.osr.level_dimensions, ((300, 250),))
        self.assertEqual(self.osr.dimensions, (300, 250))
        self.assertEqual(self.osr.level_downsamples, (1.0,))

        self.assertEqual(self.osr.get_best_level_for_downsample(0.5), 0)
        self.assertEqual(self.osr.get_best_level_for_downsample(3), 0)

        self.assertEqual(self.osr.properties, {})
        self.assertEqual(self.osr.associated_images, {})

    def test_color_profile(self) -> None:
        assert self.osr.color_profile is not None  # for type inference
        self.assertEqual(self.osr.color_profile.profile.device_class, 'mntr')
        self.assertEqual(
            len(self.osr.read_region((0, 0), 0, (100, 100)).info['icc_profile']), 588
        )
        self.assertEqual(
            len(self.osr.get_thumbnail((100, 100)).info['icc_profile']), 588
        )

    def test_read_region(self) -> None:
        self.assertEqual(
            self.osr.read_region((-10, -10), 0, (400, 400)).size, (400, 400)
        )

    def test_read_region_size_dimension_zero(self) -> None:
        self.assertEqual(self.osr.read_region((0, 0), 0, (400, 0)).size, (400, 0))

    def test_read_region_bad_level(self) -> None:
        self.assertRaises(
            OpenSlideError, lambda: self.osr.read_region((0, 0), 1, (100, 100))
        )

    def test_read_region_bad_size(self) -> None:
        self.assertRaises(
            OpenSlideError, lambda: self.osr.read_region((0, 0), 0, (400, -5))
        )

    def test_thumbnail(self) -> None:
        self.assertEqual(self.osr.get_thumbnail((100, 100)).size, (100, 83))

    @unittest.skipUnless(lowlevel.cache_create.available, "requires OpenSlide 4.0.0")
    def test_set_cache(self) -> None:
        self.osr.set_cache(OpenSlideCache(64 << 10))
        self.assertEqual(self.osr.read_region((0, 0), 0, (400, 400)).size, (400, 400))


class TestNoIccImage(_Abstract.SlideTest):
    FILENAME = 'boxes-no-icc.png'

    def test_color_profile(self) -> None:
        self.assertIsNone(self.osr.color_profile)
        self.assertNotIn(
            'icc_profile', self.osr.read_region((0, 0), 0, (100, 100)).info
        )
        self.assertNotIn('icc_profile', self.osr.get_thumbnail((100, 100)).info)
