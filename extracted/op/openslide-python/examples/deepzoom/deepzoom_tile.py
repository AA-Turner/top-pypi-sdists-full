#!/usr/bin/env python
#
# deepzoom_tile - Convert whole-slide images to Deep Zoom format
#
# Copyright (c) 2010-2015 Carnegie Mellon University
# Copyright (c) 2022-2024 Benjamin Gilbert
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

"""An example program to generate a Deep Zoom directory tree from a slide."""

from __future__ import annotations

from argparse import ArgumentParser
import base64
from collections.abc import Callable
from io import BytesIO
import json
from multiprocessing import JoinableQueue, Process
import multiprocessing.queues
import os
from pathlib import Path
import re
import shutil
import sys
from typing import TYPE_CHECKING, Literal
from unicodedata import normalize
import zlib

from PIL import Image, ImageCms

if TYPE_CHECKING:
    # Python 3.10+
    from typing import TypeAlias

if os.name == 'nt':
    _dll_path = os.getenv('OPENSLIDE_PATH')
    if _dll_path is not None:
        with os.add_dll_directory(_dll_path):  # type: ignore[attr-defined,unused-ignore]  # noqa: E501
            import openslide
    else:
        import openslide
else:
    import openslide

from openslide import AbstractSlide, ImageSlide, open_slide
from openslide.deepzoom import DeepZoomGenerator

VIEWER_SLIDE_NAME = 'slide'

# Optimized sRGB v2 profile, CC0-1.0 license
# https://github.com/saucecontrol/Compact-ICC-Profiles/blob/bdd84663/profiles/sRGB-v2-micro.icc
# ImageCms.createProfile() generates a v4 profile and Firefox has problems
# with those: https://littlecms.com/blog/2020/09/09/browser-check/
SRGB_PROFILE_BYTES = zlib.decompress(
    base64.b64decode(
        'eNpjYGA8kZOcW8wkwMCQm1dSFOTupBARGaXA/oiBmUGEgZOBj0E2Mbm4wDfYLYQBCIoT'
        'y4uTS4pyGFDAt2sMjCD6sm5GYl7K3IkMtg4NG2wdSnQa5y1V6mPADzhTUouTgfQHII5P'
        'LigqYWBg5AGyecpLCkBsCSBbpAjoKCBbB8ROh7AdQOwkCDsErCYkyBnIzgCyE9KR2ElI'
        'bKhdIMBaCvQsskNKUitKQLSzswEDKAwgop9DwH5jFDuJEMtfwMBg8YmBgbkfIZY0jYFh'
        'eycDg8QthJgKUB1/KwPDtiPJpUVlUGu0gLiG4QfjHKZS5maWk2x+HEJcEjxJfF8Ez4t8'
        'k8iS0VNwVlmjmaVXZ/zacrP9NbdwX7OQshjxFNmcttKwut4OnUlmc1Yv79l0e9/MU8ev'
        'pz4p//jz/38AR4Nk5Q=='
    )
)
SRGB_PROFILE = ImageCms.getOpenProfile(BytesIO(SRGB_PROFILE_BYTES))

if TYPE_CHECKING:
    ColorMode: TypeAlias = Literal[
        'default',
        'absolute-colorimetric',
        'perceptual',
        'relative-colorimetric',
        'saturation',
        'embed',
        'ignore',
    ]
    TileQueue: TypeAlias = multiprocessing.queues.JoinableQueue[
        tuple[str | None, int, tuple[int, int], Path] | None
    ]
    Transform: TypeAlias = Callable[[Image.Image], None]


class TileWorker(Process):
    """A child process that generates and writes tiles."""

    def __init__(
        self,
        queue: TileQueue,
        slidepath: Path,
        tile_size: int,
        overlap: int,
        limit_bounds: bool,
        quality: int,
        color_mode: ColorMode,
    ):
        Process.__init__(self, name='TileWorker')
        self.daemon = True
        self._queue = queue
        self._slidepath = slidepath
        self._tile_size = tile_size
        self._overlap = overlap
        self._limit_bounds = limit_bounds
        self._quality = quality
        self._color_mode = color_mode
        self._slide: AbstractSlide | None = None

    def run(self) -> None:
        self._slide = open_slide(self._slidepath)
        last_associated = None
        dz, transform = self._get_dz_and_transform()
        while True:
            data = self._queue.get()
            if data is None:
                self._queue.task_done()
                break
            associated, level, address, outfile = data
            if last_associated != associated:
                dz, transform = self._get_dz_and_transform(associated)
                last_associated = associated
            tile = dz.get_tile(level, address)
            transform(tile)
            tile.save(
                outfile, quality=self._quality, icc_profile=tile.info.get('icc_profile')
            )
            self._queue.task_done()

    def _get_dz_and_transform(
        self, associated: str | None = None
    ) -> tuple[DeepZoomGenerator, Transform]:
        assert self._slide is not None
        if associated is not None:
            image: AbstractSlide = ImageSlide(self._slide.associated_images[associated])
        else:
            image = self._slide
        dz = DeepZoomGenerator(
            image, self._tile_size, self._overlap, limit_bounds=self._limit_bounds
        )
        return dz, self._get_transform(image)

    def _get_transform(self, image: AbstractSlide) -> Transform:
        if image.color_profile is None:
            return lambda img: None
        mode = self._color_mode
        if mode == 'ignore':
            # drop ICC profile from tiles
            return lambda img: img.info.pop('icc_profile')
        elif mode == 'embed':
            # embed ICC profile in tiles
            return lambda img: None
        elif mode == 'default':
            intent = ImageCms.Intent(ImageCms.getDefaultIntent(image.color_profile))
        elif mode == 'absolute-colorimetric':
            intent = ImageCms.Intent.ABSOLUTE_COLORIMETRIC
        elif mode == 'relative-colorimetric':
            intent = ImageCms.Intent.RELATIVE_COLORIMETRIC
        elif mode == 'perceptual':
            intent = ImageCms.Intent.PERCEPTUAL
        elif mode == 'saturation':
            intent = ImageCms.Intent.SATURATION
        else:
            raise ValueError(f'Unknown color mode {mode}')
        transform = ImageCms.buildTransform(
            image.color_profile,
            SRGB_PROFILE,
            'RGB',
            'RGB',
            intent,
            ImageCms.Flags(0),
        )

        def xfrm(img: Image.Image) -> None:
            ImageCms.applyTransform(img, transform, True)
            # Some browsers assume we intend the display's color space if we
            # don't embed the profile.  Pillow's serialization is larger, so
            # use ours.
            img.info['icc_profile'] = SRGB_PROFILE_BYTES

        return xfrm


class DeepZoomImageTiler:
    """Handles generation of tiles and metadata for a single image."""

    def __init__(
        self,
        dz: DeepZoomGenerator,
        basename: Path,
        format: str,
        associated: str | None,
        queue: TileQueue,
    ):
        self._dz = dz
        self._basename = basename
        self._format = format
        self._associated = associated
        self._queue = queue
        self._processed = 0

    def run(self) -> None:
        self._write_tiles()
        self._write_dzi()

    def _write_tiles(self) -> None:
        for level in range(self._dz.level_count):
            tiledir = self._basename.with_name(self._basename.name + '_files') / str(
                level
            )
            tiledir.mkdir(parents=True, exist_ok=True)
            cols, rows = self._dz.level_tiles[level]
            for row in range(rows):
                for col in range(cols):
                    tilename = tiledir / f'{col}_{row}.{self._format}'
                    if not tilename.exists():
                        self._queue.put((self._associated, level, (col, row), tilename))
                    self._tile_done()

    def _tile_done(self) -> None:
        self._processed += 1
        count, total = self._processed, self._dz.tile_count
        if count % 100 == 0 or count == total:
            print(
                "Tiling %s: wrote %d/%d tiles"
                % (self._associated or 'slide', count, total),
                end='\r',
                file=sys.stderr,
            )
            if count == total:
                print(file=sys.stderr)

    def _write_dzi(self) -> None:
        with self._basename.with_name(self._basename.name + '.dzi').open('w') as fh:
            fh.write(self.get_dzi())

    def get_dzi(self) -> str:
        return self._dz.get_dzi(self._format)


class DeepZoomStaticTiler:
    """Handles generation of tiles and metadata for all images in a slide."""

    def __init__(
        self,
        slidepath: Path,
        basename: Path,
        format: str,
        tile_size: int,
        overlap: int,
        limit_bounds: bool,
        quality: int,
        color_mode: ColorMode,
        workers: int,
        with_viewer: bool,
    ):
        if with_viewer:
            # Check extra dependency before doing a bunch of work
            import jinja2  # noqa: F401  module-imported-but-unused
        self._slide = open_slide(slidepath)
        self._basename = basename
        self._format = format
        self._tile_size = tile_size
        self._overlap = overlap
        self._limit_bounds = limit_bounds
        self._queue: TileQueue = JoinableQueue(2 * workers)
        self._workers = workers
        self._color_mode = color_mode
        self._with_viewer = with_viewer
        self._dzi_data: dict[str, str] = {}
        for _i in range(workers):
            TileWorker(
                self._queue,
                slidepath,
                tile_size,
                overlap,
                limit_bounds,
                quality,
                color_mode,
            ).start()

    def run(self) -> None:
        self._run_image()
        if self._with_viewer:
            for name in self._slide.associated_images:
                self._run_image(name)
            self._write_html()
            self._write_static()
        self._shutdown()

    def _run_image(self, associated: str | None = None) -> None:
        """Run a single image from self._slide."""
        if associated is None:
            image = self._slide
            if self._with_viewer:
                basename = self._basename / VIEWER_SLIDE_NAME
            else:
                basename = self._basename
        else:
            image = ImageSlide(self._slide.associated_images[associated])
            basename = self._basename / self._slugify(associated)
        dz = DeepZoomGenerator(
            image, self._tile_size, self._overlap, limit_bounds=self._limit_bounds
        )
        tiler = DeepZoomImageTiler(dz, basename, self._format, associated, self._queue)
        tiler.run()
        self._dzi_data[self._url_for(associated)] = tiler.get_dzi()

    def _url_for(self, associated: str | None) -> str:
        if associated is None:
            base = VIEWER_SLIDE_NAME
        else:
            base = self._slugify(associated)
        return '%s.dzi' % base

    def _write_html(self) -> None:
        import jinja2

        # https://docs.python.org/3/reference/import.html#main-spec
        if __spec__ is not None:
            # We're running from a module (e.g. "python -m deepzoom_tile")
            # so load templates from the containing package.
            loader = jinja2.PackageLoader('__main__')
        else:
            # We're not running from a module (e.g. "python deepzoom_tile.py")
            # so PackageLoader('__main__') doesn't work in jinja2 3.x.
            # Load templates directly from the filesystem.
            loader = jinja2.FileSystemLoader([Path(__file__).parent / 'templates'])
        env = jinja2.Environment(loader=loader, autoescape=True)
        template = env.get_template('slide-multipane.html')
        associated_urls = {n: self._url_for(n) for n in self._slide.associated_images}
        try:
            mpp_x = self._slide.properties[openslide.PROPERTY_NAME_MPP_X]
            mpp_y = self._slide.properties[openslide.PROPERTY_NAME_MPP_Y]
            mpp = (float(mpp_x) + float(mpp_y)) / 2
        except (KeyError, ValueError):
            mpp = 0
        # Embed the dzi metadata in the HTML to work around Chrome's
        # refusal to allow XmlHttpRequest from file:///, even when
        # the originating page is also a file:///
        data = template.render(
            slide_url=self._url_for(None),
            slide_mpp=mpp,
            associated=associated_urls,
            properties=self._slide.properties,
            dzi_data=json.dumps(self._dzi_data),
        )
        with open(self._basename / 'index.html', 'w') as fh:
            fh.write(data)

    def _write_static(self) -> None:
        basesrc = Path(__file__).absolute().parent / 'static'
        basedst = self._basename / 'static'
        self._copydir(basesrc, basedst)
        self._copydir(basesrc / 'images', basedst / 'images')

    def _copydir(self, src: Path, dest: Path) -> None:
        dest.mkdir(parents=True, exist_ok=True)
        for srcpath in src.iterdir():
            if srcpath.is_file():
                shutil.copy(srcpath, dest / srcpath.name)

    @classmethod
    def _slugify(cls, text: str) -> str:
        text = normalize('NFKD', text.lower()).encode('ascii', 'ignore').decode()
        return re.sub('[^a-z0-9]+', '_', text)

    def _shutdown(self) -> None:
        for _i in range(self._workers):
            self._queue.put(None)
        self._queue.join()


if __name__ == '__main__':
    try:
        # Python 3.13+
        available_cpus = os.process_cpu_count()  # type: ignore[attr-defined]
    except AttributeError:
        try:
            # Linux
            available_cpus = len(
                os.sched_getaffinity(0)  # type: ignore[attr-defined,unused-ignore]
            )
        except AttributeError:
            # default
            available_cpus = 4

    parser = ArgumentParser(usage='%(prog)s [options] <SLIDE>')
    parser.add_argument(
        '-B',
        '--ignore-bounds',
        dest='limit_bounds',
        default=True,
        action='store_false',
        help='display entire scan area',
    )
    parser.add_argument(
        '--color-mode',
        dest='color_mode',
        choices=[
            'default',
            'absolute-colorimetric',
            'perceptual',
            'relative-colorimetric',
            'saturation',
            'embed',
            'ignore',
        ],
        default='default',
        help=(
            'convert tiles to sRGB using default rendering intent of ICC '
            'profile, or specified rendering intent; or embed original '
            'ICC profile; or ignore ICC profile (compat) [default]'
        ),
    )
    parser.add_argument(
        '-e',
        '--overlap',
        metavar='PIXELS',
        dest='overlap',
        type=int,
        default=1,
        help='overlap of adjacent tiles [1]',
    )
    parser.add_argument(
        '-f',
        '--format',
        dest='format',
        default='jpeg',
        choices=['jpeg', 'png'],
        help='image format for tiles [jpeg]',
    )
    parser.add_argument(
        '-j',
        '--jobs',
        metavar='COUNT',
        dest='workers',
        type=int,
        default=available_cpus,
        help=f'number of worker processes to start [{available_cpus}]',
    )
    parser.add_argument(
        '-o',
        '--output',
        metavar='NAME',
        type=Path,
        dest='basename',
        help='base name of output file',
    )
    parser.add_argument(
        '-Q',
        '--quality',
        metavar='QUALITY',
        dest='quality',
        type=int,
        default=90,
        help='JPEG compression quality [90]',
    )
    parser.add_argument(
        '-r',
        '--viewer',
        dest='with_viewer',
        action='store_true',
        help='generate directory tree with HTML viewer',
    )
    parser.add_argument(
        '-s',
        '--size',
        metavar='PIXELS',
        dest='tile_size',
        type=int,
        default=254,
        help='tile size [254]',
    )
    parser.add_argument(
        'slidepath',
        metavar='SLIDE',
        type=Path,
        help='slide file',
    )

    args = parser.parse_args()
    if args.basename is None:
        args.basename = Path(args.slidepath.stem)

    DeepZoomStaticTiler(
        args.slidepath,
        args.basename,
        args.format,
        args.tile_size,
        args.overlap,
        args.limit_bounds,
        args.quality,
        args.color_mode,
        args.workers,
        args.with_viewer,
    ).run()
