# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import PostFxEffect
from ._mask import MaskData

from typing import TYPE_CHECKING, ClassVar, Type

if TYPE_CHECKING:
    from ..._rendering import Pipeline
    from .. import PostFxRenderer

# ======================================== ABSTRACT CLASS ========================================
class SpecializedPostFxRenderer:
    """Classe abstraite des renderers d'effets post-processing spécialisés"""
    __slots__ = tuple()

    _HANDLES: ClassVar[frozenset[Type[PostFxEffect]]]

    _POSTFX_RENDERER: Type[PostFxRenderer] = None

    @classmethod
    def _get_postfx_renderer(cls) -> Type[PostFxRenderer]:
        """Renvoie le ``PostFxRenderer``"""
        if cls._POSTFX_RENDERER is None:
            from ._renderer import PostFxRenderer
            cls._POSTFX_RENDERER = PostFxRenderer
        return cls._POSTFX_RENDERER

    def __init_subclass__(cls, **kwargs: object) -> None:
        """S'enregistre en tant que renderer spécialisé"""
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "_HANDLES"):
            cls._get_postfx_renderer()._register(cls)

    # ======================================== CONTRACT ========================================
    @classmethod
    def clear_shader_cache(cls) -> None:
        """Libère les ``ShaderProgram`` mis en cache"""

    def apply(self, pipeline: Pipeline, effect: PostFxEffect, mask: MaskData) -> None:
        """Applique l'effet sur le framebuffer courant
    
        Args:
            pipeline: ``Pipeline`` de rendu courant
            effect: paramètres de l'effet
            mask: données de masque spatial (position, forme, blend) en coordonnées
                  framebuffer ; utiliser ``MASK_FULL`` pour un effet plein écran
        """

# ======================================== EXPORTS ========================================
__all__ = [
    "SpecializedPostFxRenderer",
]