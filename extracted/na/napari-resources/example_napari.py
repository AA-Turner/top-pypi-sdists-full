# /// script
# dependencies = [
#   "napari[all]",
#   "imageio",
#   "cairosvg",
#   "napari-resources",
# ]
#
# [tool.uv.sources]
# napari_resources = { path = "./" }
# ///

"""Show all napari logo variants as image layers (cairosvg + imageio)."""

import cairosvg
import imageio.v3 as iio
import napari

import napari_resources

viewer = napari.Viewer()

for name in napari_resources.logo_variants():
    svg_path = napari_resources.logo_path(f"{name}-plain-dark.svg")
    png = cairosvg.svg2png(url=str(svg_path))
    viewer.add_image(iio.imread(png), name=name)

viewer.grid.enabled = True
viewer.fit_to_view()

napari.run()
