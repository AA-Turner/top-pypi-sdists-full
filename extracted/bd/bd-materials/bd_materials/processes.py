"""Manufacturing processes -- how a part was produced, and the surface that leaves.

A :class:`Process` is **intrinsic spec only**: the production route, nothing per-part.
The **public API is the flat verb functions** (``fdm(rotation=90)``, ``sls()``), which
bind the per-part texture geometry to a process and return an :class:`AppliedProcess`.
This is deliberately the same shape :mod:`.finishes` uses for ``Finish`` /
``AppliedFinish`` -- and for the same reason: the surface a route leaves has a
per-part orientation and scale, which belong on the application, not on the route.

Which geometry each function exposes follows what its surface actually looks like,
matching the finish convention (``brushed`` takes scale + rotation, the isotropic
``bead_blast`` takes scale only, ``passivate`` takes nothing):

- :func:`fdm` -- extruded layer lines are **directional**, so it takes ``rotation`` (to
  lay the lines parallel to the base plate) and ``layer_height_mm`` (the printed pitch,
  which is a real millimetre length, not a UV multiplier).
- :func:`sls` / :func:`mjf` / :func:`slm` -- a sintered powder surface is **isotropic**,
  so ``scale`` only, no rotation.
- :func:`vat`, :func:`molded`, :func:`machined`, :func:`cast`, :func:`wrought` -- no
  as-made relief, so no geometry at all.

``process`` and ``finish`` stay mutually exclusive: a finish defines the surface, so
the raw as-made one is no longer visible.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

# The printed pitches the two bundled FDM maps are authored at; a part printed at these
# needs no rescaling. Only the pitches are fixed here -- the tile size each corresponds
# to is read off the material itself (see ``pbr._fdm_scale``). The wall shows stacked
# layers, so its pitch is the layer height; the skin shows side-by-side infill beads, so
# its pitch is the extrusion width -- a different quantity, hence a separate constant.
AUTHORED_LAYER_HEIGHT_MM = 0.2
AUTHORED_LINE_WIDTH_MM = 0.4

# the infill direction the skin map is authored at; slicers alternate top/bottom, so the
# bottom face is the same map at ``-45``
AUTHORED_SKIN_ROTATION = 45.0


class Process(Enum):
    """How a part is produced -- the intrinsic route.

    The key behind the verb functions below, which are the public API. Passing a bare
    member as ``process=`` still works but is deprecated -- call the matching function
    (``Process.FDM`` -> ``fdm()``), which is the only way to reach the per-part
    geometry.
    """

    FDM = "fdm"
    SLS = "sls"
    MJF = "mjf"
    SLM = "slm"  # metal powder-bed / additive
    VAT = "vat"  # SLA / DLP resin
    MOLDED = "molded"
    MACHINED = "machined"
    CAST = "cast"
    WROUGHT = "wrought"


@dataclass(frozen=True)
class AppliedProcess:
    """A process plus the per-part geometry of the surface it leaves.

    Produced by the process functions below -- the counterpart to ``AppliedFinish``.
    A field is meaningful only for the processes whose function exposes it:
    ``pitch_mm`` is ``None`` for every route but FDM, and ``scale`` stays at the
    as-authored ``(1, 1)`` for the routes that leave no tileable relief.
    """

    process: Process
    scale: tuple[float, float] = (1.0, 1.0)  # texture UV scale (u, v); 1 = as-authored
    rotation: float = 0.0  # texture rotation in degrees (counterclockwise)
    # FDM: the pitch of the extrusion lines this face shows, in mm -- the layer height
    # on a wall, the infill line width on a skin. ``skin`` says which.
    pitch_mm: float | None = None
    skin: bool = False  # FDM: the solid top/bottom surface rather than the wall
    mm_per_uv: float = 1.0  # mm one UV unit spans on this face; 1 = already metric


# process input accepted by ``process=`` (an applied process, a bare route, or none).
# The bare ``Process`` is the deprecated spelling -- see ``FinishedMaterial``.
ProcessSpec = AppliedProcess | Process | None


# --- additive: the routes that leave an as-built relief ----------------------
def fdm(
    layer_height_mm: float = AUTHORED_LAYER_HEIGHT_MM,
    rotation: float = 0.0,
    mm_per_uv: float = 1.0,
) -> AppliedProcess:
    """Fused-deposition (filament) printing -- extruded layer lines.

    ``rotation`` and ``mm_per_uv`` both compensate for how the face carrying this look is
    parameterized -- the layer-line map is applied in raw surface-parameter space, so its
    direction and its spacing each depend on the face. ``rotation`` fixes the direction,
    ``mm_per_uv`` the spacing.

    Args:
        layer_height_mm: The printed layer pitch in millimetres. The map is authored at
            ``0.2`` and rendered at a real-world scale, so the lines keep this spacing
            on a part of any size. Default ``0.2``.
        rotation: Texture rotation in degrees (counterclockwise) -- the knob for laying
            the layer lines parallel to the base plate, which depends on how the part
            is oriented on it. Default ``0``.
        mm_per_uv: How many millimetres one UV unit spans on this face. ``1`` (the
            default) is right wherever the parameterization is already metric along the
            build axis -- planar faces and a cylinder's lateral surface. It is **not**
            right where the parameter is an angle: a sphere's latitude spans pi radians
            whatever its size, so one UV unit is its radius in mm and the layer count
            would otherwise come out fixed at ~16. Pass the radius there.

    Returns:
        The applied process.
    """
    return AppliedProcess(
        Process.FDM,
        rotation=rotation,
        pitch_mm=layer_height_mm,
        mm_per_uv=mm_per_uv,
    )


def fdm_skin(
    line_width_mm: float = AUTHORED_LINE_WIDTH_MM,
    rotation: float = AUTHORED_SKIN_ROTATION,
) -> AppliedProcess:
    """Fused-deposition printing, the **solid top/bottom surface** rather than the wall.

    Same route as :func:`fdm` -- the part is still FDM-printed -- but the face shows the
    skin (the slicer's word for the solid top and bottom layers): side-by-side infill
    beads squashed flat against the layer beneath, so a much finer relief than the wall's
    stacked layer lines, and correspondingly glossier. Assign this to the faces normal to
    the build axis and :func:`fdm` to the walls.

    Its pitch is the **extrusion width**, not the layer height -- the beads sit beside
    each other rather than stacked -- which is why this is a separate function rather
    than a flag on :func:`fdm`.

    Args:
        line_width_mm: The infill line pitch in millimetres, i.e. the extrusion width.
            The map is authored at ``0.4``. Default ``0.4``.
        rotation: Infill direction in degrees (counterclockwise). The map is authored at
            ``45``; pass ``-45`` for the bottom face, the way slicers alternate.
            Default ``45``.

    Returns:
        The applied process.
    """
    return AppliedProcess(
        Process.FDM, rotation=rotation, pitch_mm=line_width_mm, skin=True
    )


def sls(scale: tuple[float, float] = (1.0, 1.0)) -> AppliedProcess:
    """Selective laser sintering -- a matte sintered-powder surface.

    Args:
        scale: Texture UV scale ``(u, v)``; ``(2, 2)`` reads the grain twice as large.
            Isotropic, so no rotation. Default ``(1, 1)`` is the as-authored size.

    Returns:
        The applied process.
    """
    return AppliedProcess(Process.SLS, scale=scale)


def mjf(scale: tuple[float, float] = (1.0, 1.0)) -> AppliedProcess:
    """Multi Jet Fusion -- a matte fused-powder surface.

    Args:
        scale: Texture UV scale ``(u, v)``; ``(2, 2)`` reads the grain twice as large.
            Isotropic, so no rotation. Default ``(1, 1)`` is the as-authored size.

    Returns:
        The applied process.
    """
    return AppliedProcess(Process.MJF, scale=scale)


def slm(scale: tuple[float, float] = (1.0, 1.0)) -> AppliedProcess:
    """Selective laser melting -- metal powder bed, a matte as-built surface.

    Args:
        scale: Texture UV scale ``(u, v)``; ``(2, 2)`` reads the grain twice as large.
            Isotropic, so no rotation. Default ``(1, 1)`` is the as-authored size.

    Returns:
        The applied process.
    """
    return AppliedProcess(Process.SLM, scale=scale)


# --- routes with no as-made relief (the surface stays smooth) ----------------
def vat() -> AppliedProcess:
    """Vat photopolymerization (SLA / DLP) -- a smooth as-printed resin surface."""
    return AppliedProcess(Process.VAT)


def molded() -> AppliedProcess:
    """Injection / compression molding -- takes the tool's smooth surface."""
    return AppliedProcess(Process.MOLDED)


def machined() -> AppliedProcess:
    """Machined from stock -- a smooth as-cut surface."""
    return AppliedProcess(Process.MACHINED)


def cast() -> AppliedProcess:
    """Cast -- a smooth as-cast surface."""
    return AppliedProcess(Process.CAST)


def wrought() -> AppliedProcess:
    """Wrought / formed stock -- a smooth mill surface."""
    return AppliedProcess(Process.WROUGHT)


__all__ = [
    "AUTHORED_LAYER_HEIGHT_MM",
    "AppliedProcess",
    "Process",
    "ProcessSpec",
    "cast",
    "fdm",
    "fdm_skin",
    "machined",
    "mjf",
    "molded",
    "slm",
    "sls",
    "vat",
    "wrought",
]
