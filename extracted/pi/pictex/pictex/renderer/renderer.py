import skia
from ..models import FontSmoothing
from ..models import CropMode
from .image_processor import ImageProcessor
from .vector_image_processor import VectorImageProcessor
from ..models import RenderProps
from ..bitmap_image import BitmapImage
from ..vector_image import VectorImage
from ..nodes import Node
from ..layout import LayoutEngine

class Renderer:

    def __init__(self):
        self._layout_engine = LayoutEngine()

    def render_as_bitmap(self, root: Node, crop_mode: CropMode, font_smoothing: FontSmoothing, scale_factor: float = 1.0) -> BitmapImage:
        """Renders the nodes with the given builders, generating a bitmap image."""
        self._prepare_tree_for_rendering(root, RenderProps(False, crop_mode, font_smoothing))

        canvas_bounds = root.paint_bounds
        render_width = int(canvas_bounds.width() * scale_factor)
        render_height = int(canvas_bounds.height() * scale_factor)
        if render_width <= 0 or render_height <= 0:
            raise Exception(f"Invalid render dimensions: {render_width}x{render_height}. Use size() to set a valid size, or include at least one node with content.")
        
        # We're using by default:
        # - kUnknown_PixelGeometry as pixel geometry
        # - kPremul_AlphaType alpha type
        # This is the valid approach for our case
        surface = skia.Surface.MakeRasterN32Premul(render_width, render_height)
        if surface is None:
            raise Exception("Failed to create surface")
        
        canvas = surface.getCanvas()
        canvas.clear(skia.ColorTRANSPARENT)
        
        canvas.scale(scale_factor, scale_factor)
        canvas.translate(-canvas_bounds.left(), -canvas_bounds.top())

        root.paint(canvas)
        del canvas
        final_image = surface.makeImageSnapshot()
        return ImageProcessor().process(root, final_image, crop_mode)
    
    def render_as_svg(self, root: Node, embed_fonts: bool) -> VectorImage:
        """Renders the text with the given builders, generating a vector image."""
        # If support shadows in the near future, we should use CropMode.NONE.
        self._prepare_tree_for_rendering(root, RenderProps(True, CropMode.CONTENT_BOX, FontSmoothing.SUBPIXEL))

        canvas_bounds = root.paint_bounds
        stream = skia.DynamicMemoryWStream()
        canvas = skia.SVGCanvas.Make(canvas_bounds, stream)
        canvas.clear(skia.ColorTRANSPARENT)
        canvas.translate(-canvas_bounds.left(), -canvas_bounds.top())

        root.paint(canvas)
        del canvas
        return VectorImageProcessor().process(stream, embed_fonts, root)

    def _prepare_tree_for_rendering(self, root: Node, render_props: RenderProps) -> None:
        """Prepare the tree for rendering."""
        root.clear()
        root.init_render_dependencies(render_props)
        self._layout_engine.compute_layout(root)