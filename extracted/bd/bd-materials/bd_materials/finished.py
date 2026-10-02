"""The user-facing finished material -- the material as applied to a build123d part.

A ``FinishedMaterial`` bundles a range-based ``Material`` (the shared, immutable
typical-values table -- physics) with the **per-part choices**: ``color`` (a
selectable base color), ``thickness_mm`` (pane thickness), ``opacity`` (how
see-through this particular part is) and ``roughness`` (its surface gloss/frost) --
these three only meaningful when the material is ``transparent`` -- ``finish`` (an
``AppliedFinish`` or list of them), and ``process``. ``.material`` gives the physics;
``.pbr`` resolves the three.js look.

Color precedence (resolved in ``pbr``): a covering finish color > the selected
``color`` > the material's intrinsic look (derived from ``family``).

Threejs stays out of ``import bd_materials`` -- only ``.pbr`` pulls it in.
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Generic, TypeVar

from .finishes import AppliedFinish
from .core import Color, RangeMaterial
from .processes import AppliedProcess, Process, ProcessSpec

if TYPE_CHECKING:  # real types for checkers; never imported at runtime (viz-free)
    from threejs_materials import PbrProperties

# ``Color`` (the accepted per-part color input) is re-exported from ``core`` so the
# family functions can keep importing it from here; see ``core.Color`` for the shapes.

# finish input accepted by ``finish=`` (a single applied finish, a list, or none)
FinishSpec = AppliedFinish | list[AppliedFinish] | None

# the concrete material class a FinishedMaterial carries (MetalMaterial, ...), so
# ``.material`` keeps its category-specific physics fields for type checkers
MaterialT = TypeVar("MaterialT", bound=RangeMaterial)


def _normalize_process(process: ProcessSpec) -> AppliedProcess | None:
    """Coerce the ``process=`` input to an ``AppliedProcess``.

    A bare ``Process`` member reads as that route's defaults -- it carries no per-part
    geometry, which is why it is deprecated (see ``FinishedMaterial.__init__``).

    Args:
        process: ``None``, an ``AppliedProcess``, or a bare ``Process``.

    Returns:
        The applied process, or ``None``.
    """
    if process is None:
        return None
    if isinstance(process, Process):
        return AppliedProcess(process)
    return process


class FinishedMaterial(Generic[MaterialT]):
    """A range ``Material`` + per-part color / thickness / finish(es) / process.

    The material stays a pure typical-values table; everything chosen per part
    lives here. ``pbr=`` supplies a ready-made look and cannot be combined with
    ``finish`` / ``process`` / ``color`` / ``thickness_mm``.

    Generic over the material class: a family function returns e.g.
    ``FinishedMaterial[MetalMaterial]``, so ``.material`` keeps the category's
    physics fields (``.material.tensile_strength``) for type checkers.
    """

    def __init__(
        self,
        material: MaterialT,
        finish: FinishSpec = None,
        *,
        color: Color | None = None,
        thickness_mm: float | None = None,
        opacity: float | None = None,
        roughness: float | None = None,
        scale: tuple[float, float] = (1.0, 1.0),
        rotation: float = 0.0,
        process: ProcessSpec = None,
        pbr: PbrProperties | None = None,
    ) -> None:
        """Bundle a material with the per-part choices.

        Args:
            material: The range ``Material`` (physics) this part is made of.
            finish: An ``AppliedFinish`` or list of them; mutually exclusive with
                ``process``.
            color: A selectable base color -- a build123d ``ColorLike`` (name, hex,
                ``0xRRGGBB`` int, RGB(A) tuple, or a ``Color``).
            thickness_mm: Pane thickness in mm, meaningful only for a ``transparent``
                material.
            opacity: How see-through this part is, from ``0.0`` (fully clear) to ``1.0``
                (opaque); meaningful only for a ``transparent`` material. ``None`` keeps
                the material's intrinsic look (clear). Lets a nominally clear polymer
                (e.g. PC) render as a translucent part -- a milky V-wheel is ``0.65``.
            roughness: Surface roughness from ``0.0`` (glossy) to ``1.0`` (matte /
                frosted); meaningful only for a ``transparent`` material. ``None`` keeps
                the factory value. Independent of ``opacity`` -- a molded translucent
                part is glossy, an etched pane is rough.
            scale: Texture UV scale ``(u, v)`` for a substrate texture (wood grain,
                fabric weave, ...); ``(2, 2)`` tiles it twice as fine. A textured
                finish's own scale takes precedence over this. Default ``(1, 1)``.
            rotation: Texture rotation in degrees (counterclockwise). Default ``0``.
            process: How the part was made -- an ``AppliedProcess`` from a process
                function (e.g. ``fdm(rotation=90)``), which nudges the bare as-made
                surface. Mutually exclusive with ``finish``. A bare ``Process`` member
                is accepted but deprecated (it carries no per-part geometry).
            pbr: A ready-made look that overrides everything else; cannot be combined
                with ``finish`` / ``process`` / ``color`` / ``thickness_mm`` /
                ``opacity`` / ``roughness`` / ``scale`` / ``rotation``.

        Raises:
            TypeError: If ``material`` is not a range ``Material``.
            ValueError: If ``pbr`` is combined with other look inputs, or ``finish``
                and ``process`` are both given.
        """
        if not isinstance(material, RangeMaterial):
            raise TypeError(
                "material must be a range Material (e.g. metals.aluminum().material), "
                f"not {type(material).__name__}"
            )
        if pbr is not None and (
            finish is not None
            or process is not None
            or color is not None
            or thickness_mm is not None
            or opacity is not None
            or roughness is not None
            or scale != (1.0, 1.0)
            or rotation != 0.0
        ):
            raise ValueError(
                "pbr=... is a full override; do not combine it with finish, "
                "process, color, thickness_mm, opacity, roughness, scale, or rotation"
            )
        if finish is not None and process is not None:
            raise ValueError(
                "finish and process are mutually exclusive: a finish defines the "
                "surface, so a process (the raw as-made surface) is ignored -- pass "
                "one or the other"
            )
        self.material: MaterialT = material
        self.finish = finish
        self.color = color
        self.thickness_mm = thickness_mm
        self.opacity = opacity
        self.roughness = roughness
        if isinstance(process, Process):
            warnings.warn(
                f"process={process} is deprecated; call the process function instead "
                f"-- process={process.value}() (from bd_materials.processes), which is "
                "also the only way to pass the per-part geometry, e.g. fdm(rotation=90)",
                DeprecationWarning,
                stacklevel=2,
            )
        self.scale = scale
        self.rotation = rotation
        self.process = _normalize_process(process)
        self._pbr = pbr

    @property
    def name(self) -> str:
        """The underlying material's catalog name (e.g. ``"Alu_G6061_T6"``)."""
        return self.material.name

    @property
    def pbr(self) -> PbrProperties:
        """The resolved three.js look (needs ``threejs_materials``).

        The explicit override if supplied, else derived from the material's identity,
        the selected color/thickness, the finish(es), and the process. The viz stack
        is imported here and nowhere else.

        Returns:
            The resolved ``PbrProperties``.
        """
        if self._pbr is not None:
            return self._pbr
        from .pbr import get_pbr_properties  # lazy: only here is the viz stack needed

        return get_pbr_properties(
            self.material,
            self.finish,
            self.process,
            color=self.color,
            thickness_mm=self.thickness_mm,
            opacity=self.opacity,
            roughness=self.roughness,
            scale=self.scale,
            rotation=self.rotation,
        )

    @pbr.setter
    def pbr(self, value: PbrProperties) -> None:
        """Pin a ready-made look, from now on returned unchanged by ``.pbr``.

        The assignment counterpart to the ``pbr=`` constructor arg: resolve the look
        from the per-part fields, tune it (e.g. ``.pbr.override(roughness=0.45)``), and
        store the result back. Unlike the constructor arg -- which forbids mixing a raw
        ``pbr`` with the per-part fields -- this path is *derived from* those fields, so
        they stay on the object as provenance (still shown in ``repr``) but no longer
        drive ``.pbr``.

        Args:
            value: The ``PbrProperties`` to return from now on.
        """
        self._pbr = value

    def __str__(self) -> str:
        """The underlying material's typical-value dump (physics only)."""
        return str(self.material)

    def __repr__(self) -> str:
        """Compact repr: the material name plus any per-part choices set."""
        parts = [self.material.name]
        if self.color is not None:
            parts.append(f"color={self.color!r}")
        if self.thickness_mm is not None:
            parts.append(f"thickness_mm={self.thickness_mm}")
        if self.opacity is not None:
            parts.append(f"opacity={self.opacity}")
        if self.roughness is not None:
            parts.append(f"roughness={self.roughness}")
        if self.scale != (1.0, 1.0):
            parts.append(f"scale={self.scale}")
        if self.rotation != 0.0:
            parts.append(f"rotation={self.rotation}")
        if self.finish is not None:
            parts.append(f"finish={self.finish!r}")
        if self.process is not None:
            parts.append(f"process={self.process}")
        if self._pbr is not None:
            parts.append("pbr=<override>")
        return f"FinishedMaterial({', '.join(parts)})"
