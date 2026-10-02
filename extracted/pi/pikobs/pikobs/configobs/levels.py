#!/usr/bin/python3
"""Vertical layers: grouping levels so a figure stays readable.

A radiance family has one figure per channel and that is fine -- a
channel is a thing you can name. A family on pressure or height does not
work that way: ``ua`` has fifty levels and ``ro`` has a hundred, and one
figure per level is a hundred figures nobody opens. So those families
are grouped into layers, a handful of them, each holding the levels
between two edges.

The edges come from the wrapper and are read from the ground up::

    PRESSURE_LAYERS=(1100 850 500 250 100 10 1 0)   # hPa
    HEIGHT_LAYERS=(0 5 10 20 30 40 60 100)          # km

Both lists are written the way they read on a chart: pressures descend
from the ground, heights climb from it. A layer holds its top edge, so
850-500 hPa holds 500 and not 850, and the labels are prefixed with a
rank so the viewer sorts them by height rather than alphabetically.

The same layers are used by histogram, profile and scatter, which is
what lets a figure of one be compared with a figure of another::

    from pikobs.configobs.levels import layers_for, layer_of

    layers = layers_for(VCOTYP, pressure=PRESSURE_LAYERS,
                        height=HEIGHT_LAYERS)
    label = layer_of(vcoord, layers)
"""

from typing import List, Optional, Sequence

from .families import family as _family

__all__ = ["PRESSURE_LAYERS_HPA", "HEIGHT_LAYERS_KM", "layers_for",
           "layer_case", "layer_of", "layer_label", "layer_unit_scale",
           "needs_layers"]

# Defaults: the troposphere in four layers, then the stratosphere, where
# observations thin out and a layer has to be wide to hold anything.
PRESSURE_LAYERS_HPA = (1100, 850, 500, 250, 100, 10, 1, 0)
HEIGHT_LAYERS_KM = (0, 5, 10, 20, 30, 40, 60, 100)

_PRESSURE = 'PRESSION'
_HEIGHT = 'HAUTEUR'


def needs_layers(vcotyp: str) -> bool:
    """Is this a family whose levels are a continuum rather than a list?

    A channel is a named thing and stays one per figure; a surface family
    or a band of latitude has no vertical axis to group.
    """
    kind = str(vcotyp).strip().upper()
    return kind.startswith(_PRESSURE) or kind.startswith(_HEIGHT)


def layer_unit_scale(vcotyp: str) -> float:
    """What to multiply a layer edge by to reach the unit of the data.

    Layers are written the way they are read -- hPa for a pressure
    family, km for a height one -- and the databases hold Pa and metres.
    A family with neither keeps the number as it is.
    """
    kind = str(vcotyp).strip().upper()
    if kind.startswith(_PRESSURE):
        return 100.0
    if kind.startswith(_HEIGHT):
        return 1000.0
    return 1.0


def layers_for(family: str, pressure_hpa=PRESSURE_LAYERS_HPA,
               height_km=HEIGHT_LAYERS_KM) -> Optional[List[tuple]]:
    """[(low, high, label)] in the unit the data is stored in, or None.

    None means the family has no layer to speak of: a channel is named
    and selected on its own, a surface family has no vertical axis.

    Pressure is stored in Pa and height in metres while the edges are
    written in hPa and km, so the conversion happens here and no module
    has to remember which is which. A layer holds its top edge -- 40-60
    km holds the 60 km level -- and the half-metre shift is what makes
    that exact on levels that are whole kilometres.

    The label starts with its rank from the ground, ``2 | 850-500 hPa``,
    because a viewer sorts its entries as text and 1000 would otherwise
    come before 500.
    """
    _, _, _, _, _, vcotyp = _family(family)
    kind = str(vcotyp).strip().upper()
    out: List[tuple] = []
    if kind.startswith(_PRESSURE):
        edges = sorted(set(float(x) for x in pressure_hpa), reverse=True)
        for i, (hi, lo) in enumerate(zip(edges[:-1], edges[1:]), start=1):
            out.append((lo * 100.0, hi * 100.0, f"{i} | {hi:g}-{lo:g} hPa"))
        return out
    if kind.startswith(_HEIGHT):
        edges = sorted(set(float(x) for x in height_km))
        for i, (lo, hi) in enumerate(zip(edges[:-1], edges[1:]), start=1):
            low = lo * 1000.0 + (0.5 if i > 1 else -0.5)
            out.append((low, hi * 1000.0 + 0.5, f"{i} | {lo:g}-{hi:g} km"))
        return out
    return None


def layer_case(expr: str, layers: Sequence[tuple]) -> str:
    """SQL giving the layer label of a level; NULL outside every layer.

    A level in no layer is not folded into a neighbour: it gives NULL,
    and the query decides whether to drop it or keep it apart.
    """
    whens = " ".join(f"WHEN {expr} >= {lo!r} AND {expr} < {hi!r} "
                     f"THEN '{label}'" for lo, hi, label in layers)
    return f"(CASE {whens} END)"


def layer_of(value, layers: Sequence[tuple]) -> Optional[str]:
    """The label of the layer a level falls in, or None when it is out."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    for lo, hi, label in layers:
        if lo <= v < hi:
            return label
    return None


def layer_label(label: str) -> str:
    """The label without its rank, for a title: '850-500 hPa'."""
    return str(label).split(' | ', 1)[-1]
