from ipywidgets import (
    Widget, DOMWidget, widget_serialization, register
)
from ipywidgets.widgets.trait_types import TypedTuple
from traitlets import (
    Unicode, Int, CInt, Instance, ForwardDeclaredInstance, This, Enum,
    Tuple, List, Dict, Float, CFloat, Bool, Union, Any,
)

from .._base.Three import ThreeWidget
from .._base.uniforms import uniforms_serialization
from ..enums import *
from ..traits import *

from .Material import Material

from ..textures.Texture_autogen import Texture

@register
class MeshMatcapMaterial(Material):
    """MeshMatcapMaterial

    Autogenerated by generate-wrappers.js
    See https://threejs.org/docs/#api/materials/MeshMatcapMaterial
    """

    _model_name = Unicode('MeshMatcapMaterialModel').tag(sync=True)

    alphaMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    bumpMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    bumpScale = IEEEFloat(1, allow_none=False).tag(sync=True)

    color = Color("#ffffff", allow_none=False).tag(sync=True)

    displacementMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    displacementScale = IEEEFloat(1, allow_none=False).tag(sync=True)

    displacementBias = IEEEFloat(0, allow_none=False).tag(sync=True)

    lights = Bool(False, allow_none=False).tag(sync=True)

    map = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    matcap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    morphNormals = Bool(False, allow_none=False).tag(sync=True)

    morphTargets = Bool(False, allow_none=False).tag(sync=True)

    normalMap = Instance(Texture, allow_none=True).tag(sync=True, **widget_serialization)

    normalScale = Vector2(default_value=[1, 1]).tag(sync=True)

    skinning = Bool(False, allow_none=False).tag(sync=True)

    type = Unicode("MeshMatcapMaterial", allow_none=False).tag(sync=True)


import inspect
# Include explicit signature since the metaclass screws it up
MeshMatcapMaterial.__signature__ = inspect.signature(MeshMatcapMaterial.__init__)
