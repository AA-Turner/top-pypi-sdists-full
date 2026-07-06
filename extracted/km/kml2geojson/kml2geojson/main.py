from __future__ import annotations
import xml.dom.minidom as md
import xml.dom.minicompat as mc
import math
import re
import pathlib as pl
from typing import Callable, TextIO, BinaryIO

__all__ = [
    "STYLE_TYPES",
    "FOLDER_PROPS",
    "SVG_TO_LEAFLET",
    "TYPE_CONVERTERS",
    "get",
    "get1",
    "attr",
    "val",
    "valf",
    "numarray",
    "coords1",
    "coords",
    "fix_ring",
    "gx_coords1",
    "gx_coords",
    "disambiguate",
    "to_filename",
    "build_rgb_and_opacity",
    "build_schema",
    "build_style",
    "build_svg_style",
    "build_leaflet_style",
    "build_geometry",
    "build_feature",
    "build_ground_overlay",
    "build_network_link",
    "build_feature_collection",
    "build_feature_tree",
    "build_layers",
    "convert",
]

#: Supported style types
STYLE_TYPES = [
    "svg",
    "leaflet",
]

#: KML container properties copied to folder metadata in feature trees.
FOLDER_PROPS = [
    "name",
    "visibility",
    "open",
    "address",
    "description",
    "phoneNumber",
]

#: Map from SVG style keys to Leaflet style keys.
SVG_TO_LEAFLET = {
    "fill": "fillColor",
    "fill-opacity": "fillOpacity",
    "stroke": "color",
    "stroke-opacity": "opacity",
    "stroke-width": "weight",
    "iconUrl": "iconUrl",
    "icon-color": "iconColor",
    "icon-opacity": "iconOpacity",
    "icon-scale": "iconScale",
    "icon-heading": "iconHeading",
    "icon-offset": "iconOffset",
    "icon-offset-units": "iconOffsetUnits",
    "label-color": "labelColor",
    "label-opacity": "labelOpacity",
    "label-scale": "labelScale",
}

SPACE = re.compile(r"\s+")

DEGREES_TO_RADIANS = math.pi / 180


def get(node: md.Document, name: str) -> mc.NodeList:
    """
    Given a KML Document Object Model (DOM) node, return a list of its sub-nodes that have the given tag name.
    """
    return node.getElementsByTagName(name)


def get1(node: md.Document, name: str) -> md.Element | None:
    """
    Return the first element of ``get(node, name)``, if it exists.
    Otherwise return ``None``.
    """
    s = get(node, name)
    if s:
        return s[0]
    else:
        return None


def attr(node: md.Document, name: str) -> str:
    """
    Return as a string the value of the given DOM node's attribute named by ``name``, if it exists.
    Otherwise, return an empty string.
    """
    return node.getAttribute(name)


def val(node: md.Document) -> str:
    """
    Normalize the given DOM node and return the value of its first child (the string content of the node) stripped of leading and trailing whitespace.
    """
    try:
        node.normalize()
        return node.firstChild.wholeText.strip()  # Handles CDATASection too
    except AttributeError:
        return ""


def valf(node: md.Document) -> float | None:
    """
    Cast ``val(node)`` as a float.
    Return ``None`` if that does not work.
    """
    try:
        return float(val(node))
    except ValueError:
        return None


def numarray(a: list) -> list[float]:
    """
    Cast the given list into a list of floats.
    """
    return [float(aa) for aa in a]


def coords1(s: str) -> list[float]:
    """
    Convert the given KML string containing one coordinate tuple into a list of floats.

    EXAMPLE::

        >>> coords1(' -112.2,36.0,2357 ')
        [-112.2, 36.0, 2357.0]

    """
    return numarray(re.sub(SPACE, "", s).split(","))


def coords(s: str) -> list[list[float]]:
    """
    Convert the given KML string containing multiple coordinate tuples into a list of lists of floats.

    EXAMPLE::

        >>> coords('''
        ... -112.0,36.1,0
        ... -113.0,36.0,0
        ... ''')
        [[-112.0, 36.1, 0.0], [-113.0, 36.0, 0.0]]

    """
    s = s.split()  # sub(TRIM_SPACE, '', v).split()
    return [coords1(ss) for ss in s]


def fix_ring(ring: list[list[float]]) -> list[list[float]]:
    """
    Return the given list of coordinate lists, closed into a linear ring if it is not already closed.

    EXAMPLE::

        >>> fix_ring([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]])
        [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 0.0]]

    """
    if ring and ring[0] != ring[-1]:
        return ring + [ring[0]]
    return ring


def gx_coords1(s: str) -> list[float]:
    """
    Convert the given KML string containing one gx coordinate tuple into a list of floats.

    EXAMPLE::

        >>> gx_coords1('-113.0 36.0 0')
        [-113.0, 36.0, 0.0]

    """
    return numarray(s.split(" "))


def gx_coords(node: md.Document) -> dict:
    """
    Given a KML DOM node, grab its <gx:coord> (or unprefixed <coord>) and <when> subnodes, and convert them into a dictionary with the keys and values

    - ``'coordinates'``: list of lists of float coordinates
    - ``'times'``: list of timestamps corresponding to the coordinates

    """
    els = get(node, "gx:coord")
    if not els:
        els = get(node, "coord")
    coordinates = [gx_coords1(val(el)) for el in els]
    times = [val(t) for t in get(node, "when")]
    return {
        "coordinates": coordinates,
        "times": times,
    }


def disambiguate(names: list[str], mark: str = "1") -> list[str]:
    """
    Given a list of strings ``names``, return a new list of names where repeated names have been disambiguated by repeatedly appending the given mark.

    EXAMPLE::

        >>> disambiguate(['sing', 'song', 'sing', 'sing'])
        ['sing', 'song', 'sing1', 'sing11']

    """
    names_seen = set()
    new_names = []
    for name in names:
        new_name = name
        while new_name in names_seen:
            new_name += mark
        new_names.append(new_name)
        names_seen.add(new_name)

    return new_names


def to_filename(s: str) -> str:
    """
    Based on `django/utils/text.py <https://github.com/django/django/blob/master/django/utils/text.py>`_.
    Return the given string converted to a string that can be used for a clean filename.
    Specifically, leading and trailing spaces are removed; other spaces are converted to underscores, and anything that is not a unicode alphanumeric, dash, underscore, or dot, is removed.

    EXAMPLE::

        >>> to_filename("%  A dbla'{-+)(ç? ")
        'A_dbla-ç'

    """
    s = re.sub(r"(?u)[^-\w. ]", "", s)
    s = s.strip().replace(" ", "_")
    return s


def _document(node: md.Document) -> md.Document:
    """
    Return the DOM document that owns the given node, or the node itself if it is a document.
    """
    if isinstance(node, md.Document):
        return node
    return node.ownerDocument or node


def _is_element(node) -> bool:
    """
    Return ``True`` if the given DOM node is an element node.
    """
    return node.nodeType == md.Node.ELEMENT_NODE


def _normalize_style_url(s: str) -> str:
    """
    Return the given style URL string prefixed with '#' if it is not already.
    """
    if s and not s.startswith("#"):
        return "#" + s
    return s


# ---------------
# Main functions
# ---------------
def build_rgb_and_opacity(s: str) -> tuple:
    """
    Given a KML color string, return an equivalent RGB hex color string and an opacity float rounded to 2 decimal places.

    EXAMPLE::

        >>> build_rgb_and_opacity('ee001122')
        ('#221100', 0.93)

    """
    # Set defaults
    color = "000000"
    opacity = 1

    if s.startswith("#"):
        s = s[1:]
    if len(s) == 8:
        color = s[6:8] + s[4:6] + s[2:4]
        opacity = round(int(s[0:2], 16) / 255, 2)
    elif len(s) == 6:
        color = s[4:6] + s[2:4] + s[0:2]
    elif len(s) == 3:
        color = s[::-1]

    return "#" + color, opacity


def _convert_int(x: str):
    """
    Cast the given string to an integer, falling back to the original string on failure.
    """
    try:
        return int(float(x))
    except ValueError:
        return x


def _convert_float(x: str):
    """
    Cast the given string to a float, falling back to the original string on failure.
    """
    try:
        return float(x)
    except ValueError:
        return x


def _convert_bool(x: str) -> bool:
    """
    Cast the given string to a boolean.
    """
    return x.strip().lower() in ("1", "true")


def _identity(x: str) -> str:
    """
    Return the given string unchanged.
    """
    return x


#: Map from KML SimpleField types to Python type converters.
TYPE_CONVERTERS: dict[str, Callable] = {
    "string": _identity,
    "int": _convert_int,
    "uint": _convert_int,
    "short": _convert_int,
    "ushort": _convert_int,
    "float": _convert_float,
    "double": _convert_float,
    "bool": _convert_bool,
}


def build_schema(node: md.Document) -> dict:
    """
    Given a KML DOM node, grab its <SimpleField> subnodes and build a dictionary of the form

        field name -> type converter function

    to convert <SimpleData> string values into typed Python values.
    """
    schema = {}
    for field in get(node, "SimpleField"):
        name = attr(field, "name")
        type_ = attr(field, "type")
        schema[name] = TYPE_CONVERTERS.get(type_, _identity)
    return schema


def build_style(node: md.Document) -> dict:
    """
    Given a DOM node containing KML style subelements, such as a <Style> element or a <Placemark> element with inline styles, convert the styles found into an SVG-ish style dictionary and return the result.

    The possible keys and values of the dictionary are

    - ``iconUrl``: URL of icon
    - ``icon-color``: icon color; RGB hex string
    - ``icon-opacity``: icon opacity
    - ``icon-scale``: icon scale factor
    - ``icon-heading``: icon heading in degrees
    - ``icon-offset``: icon hot spot offset as an [x, y] list
    - ``icon-offset-units``: icon hot spot offset units as an [xunits, yunits] list
    - ``label-color``: label color; RGB hex string
    - ``label-opacity``: label opacity
    - ``label-scale``: label scale factor
    - ``stroke``: stroke color; RGB hex string
    - ``stroke-opacity``: stroke opacity
    - ``stroke-width``:  stroke width in pixels
    - ``fill``: fill color; RGB hex string
    - ``fill-opacity``: fill opacity
    """
    props = {}
    for x in get(node, "PolyStyle")[:1]:
        color = val(get1(x, "color"))
        if color:
            rgb, opacity = build_rgb_and_opacity(color)
            props["fill"] = rgb
            props["fill-opacity"] = opacity
            # Set default border style
            props["stroke"] = rgb
            props["stroke-opacity"] = opacity
            props["stroke-width"] = 1
        fill = valf(get1(x, "fill"))
        if fill == 0:
            props["fill-opacity"] = fill
        elif fill == 1 and "fill-opacity" not in props:
            props["fill-opacity"] = fill
        outline = valf(get1(x, "outline"))
        if outline == 0:
            props["stroke-opacity"] = outline
        elif outline == 1 and "stroke-opacity" not in props:
            props["stroke-opacity"] = outline
    for x in get(node, "LineStyle")[:1]:
        color = val(get1(x, "color"))
        if color:
            rgb, opacity = build_rgb_and_opacity(color)
            props["stroke"] = rgb
            props["stroke-opacity"] = opacity
        width = valf(get1(x, "width"))
        if width is not None:
            props["stroke-width"] = width
    for x in get(node, "LabelStyle")[:1]:
        color = val(get1(x, "color"))
        if color:
            rgb, opacity = build_rgb_and_opacity(color)
            props["label-color"] = rgb
            props["label-opacity"] = opacity
        scale = valf(get1(x, "scale"))
        if scale is not None:
            props["label-scale"] = scale
    for x in get(node, "IconStyle")[:1]:
        color = val(get1(x, "color"))
        if color:
            rgb, opacity = build_rgb_and_opacity(color)
            props["icon-color"] = rgb
            props["icon-opacity"] = opacity
        scale = valf(get1(x, "scale"))
        if scale is not None:
            props["icon-scale"] = scale
        heading = valf(get1(x, "heading"))
        if heading is not None:
            props["icon-heading"] = heading
        hot_spot = get1(x, "hotSpot")
        if hot_spot is not None:
            try:
                left = float(attr(hot_spot, "x"))
                top = float(attr(hot_spot, "y"))
                props["icon-offset"] = [left, top]
                props["icon-offset-units"] = [
                    attr(hot_spot, "xunits"),
                    attr(hot_spot, "yunits"),
                ]
            except ValueError:
                pass
        icon = get1(x, "Icon")
        if icon is not None:
            href = val(get1(icon, "href"))
            if href:
                props["iconUrl"] = href

    return props


def _build_style_catalog(node: md.Document, style_map_key: str = "normal") -> dict:
    """
    Given a DOM node, grab its <Style> and <StyleMap> subnodes and build a dictionary of the form

        #style ID -> SVG style dictionary,

    resolving each StyleMap to the style referenced by its pair with the given key ('normal' or 'highlight').
    """
    d = {}
    for item in get(node, "Style"):
        style_id = attr(item, "id")
        if not style_id:
            continue
        d["#" + style_id] = build_style(item)
    for item in get(node, "StyleMap"):
        style_id = attr(item, "id")
        if not style_id:
            continue
        pairs = get(item, "Pair")
        chosen = None
        for pair in pairs:
            if val(get1(pair, "key")) == style_map_key:
                chosen = pair
                break
        if chosen is None and pairs:
            chosen = pairs[0]
        if chosen is None:
            continue
        style_url = _normalize_style_url(val(get1(chosen, "styleUrl")))
        if style_url in d:
            d["#" + style_id] = dict(d[style_url])
        else:
            style = get1(chosen, "Style")
            if style is not None:
                d["#" + style_id] = build_style(style)
    return d


def build_svg_style(node: md.Document, *, style_map_key: str = "normal") -> dict:
    """
    Given a DOM node, grab its top-level <Style> and <StyleMap> nodes, convert every one into an SVG style dictionary via :func:`build_style`, put them in a master dictionary of the form

        #style ID -> SVG style dictionary,

    and return the result.

    StyleMaps are resolved to the style referenced by their pair with key ``style_map_key``, which is 'normal' by default.
    """
    return _build_style_catalog(node, style_map_key)


def build_leaflet_style(node: md.Document, *, style_map_key: str = "normal") -> dict:
    """
    Given a DOM node, grab its top-level <Style> and <StyleMap> nodes, convert every one into a Leaflet style dictionary, put them in a master dictionary of the form

        #style ID -> Leaflet style dictionary,

    and return the result.

    StyleMaps are resolved to the style referenced by their pair with key ``style_map_key``, which is 'normal' by default.

    The possible keys and values of each Leaflet style dictionary, the style options, are

    - ``iconUrl``: URL of icon
    - ``iconColor``: icon color; RGB hex string
    - ``iconOpacity``: icon opacity
    - ``iconScale``: icon scale factor
    - ``iconHeading``: icon heading in degrees
    - ``iconOffset``: icon hot spot offset as an [x, y] list
    - ``iconOffsetUnits``: icon hot spot offset units as an [xunits, yunits] list
    - ``labelColor``: label color; RGB hex string
    - ``labelOpacity``: label opacity
    - ``labelScale``: label scale factor
    - ``color``: stroke color; RGB hex string
    - ``opacity``: stroke opacity
    - ``weight``:  stroke width in pixels
    - ``fillColor``: fill color; RGB hex string
    - ``fillOpacity``: fill opacity
    """
    d = _build_style_catalog(node, style_map_key)
    return {
        style_id: {SVG_TO_LEAFLET.get(k, k): v for k, v in style.items()}
        for style_id, style in d.items()
    }


def build_geometry(node: md.Document) -> dict:
    """
    Return a dictionary with the keys and values

    - ``'geoms'``: list of (decoded) GeoJSON geometry dictionaries corresponding to the geometry subelements of the given KML node
    - ``'times'``: list of lists of timestamps corresponding to any tracks present

    Only direct geometry children of the node are considered, and MultiGeometry and (gx:)MultiTrack containers are recursed into.
    Bare LinearRings are converted to LineStrings, unclosed Polygon rings are closed, and degenerate geometries are skipped.
    """
    geoms = []
    times = []
    for child in node.childNodes:
        if not _is_element(child):
            continue
        tag = child.tagName
        if tag in ("MultiGeometry", "MultiTrack", "gx:MultiTrack"):
            sub = build_geometry(child)
            geoms.extend(sub["geoms"])
            times.extend(sub["times"])
        elif tag == "Point":
            s = val(get1(child, "coordinates"))
            if not s:
                continue
            coordinates = coords1(s)
            if len(coordinates) >= 2:
                geoms.append(
                    {
                        "type": "Point",
                        "coordinates": coordinates,
                    }
                )
        elif tag in ("LineString", "LinearRing"):
            s = val(get1(child, "coordinates"))
            if not s:
                continue
            coordinates = coords(s)
            if len(coordinates) >= 2:
                geoms.append(
                    {
                        "type": "LineString",
                        "coordinates": coordinates,
                    }
                )
        elif tag == "Polygon":
            rings = []
            for ring_node in get(child, "LinearRing"):
                s = val(get1(ring_node, "coordinates"))
                if not s:
                    continue
                ring = fix_ring(coords(s))
                if len(ring) >= 4:
                    rings.append(ring)
            if rings:
                geoms.append(
                    {
                        "type": "Polygon",
                        "coordinates": rings,
                    }
                )
        elif tag in ("Track", "gx:Track"):
            track = gx_coords(child)
            coordinates = track["coordinates"]
            if not coordinates:
                continue
            if len(coordinates) == 1:
                geoms.append(
                    {
                        "type": "Point",
                        "coordinates": coordinates[0],
                    }
                )
            else:
                geoms.append(
                    {
                        "type": "LineString",
                        "coordinates": coordinates,
                    }
                )
            if track["times"]:
                times.append(track["times"])

    return {"geoms": geoms, "times": times}


def _build_common_props(node: md.Document, schema: dict) -> dict:
    """
    Build and return the dictionary of GeoJSON Feature properties shared by Placemarks, GroundOverlays, and NetworkLinks.
    """
    props = {}
    for key in ["name", "address", "open", "phoneNumber"]:
        for x in get(node, key)[:1]:
            v = val(x)
            if v:
                props[key] = v
    for x in get(node, "visibility")[:1]:
        v = val(x)
        if v:
            props["visibility"] = v != "0"
    for x in get(node, "description")[:1]:
        cdata = None
        for c in x.childNodes:
            if c.nodeType == md.Node.CDATA_SECTION_NODE:
                cdata = c
                break
        if cdata is not None:
            desc = cdata.wholeText.strip()
            if desc:
                props["description"] = {"@type": "html", "value": desc}
        else:
            desc = val(x)
            if desc:
                props["description"] = desc
    for x in get(node, "styleUrl")[:1]:
        style_url = _normalize_style_url(val(x))
        if style_url:
            props["styleUrl"] = style_url
    props.update(build_style(node))
    for x in get(node, "ExtendedData")[:1]:
        datas = get(x, "Data")
        for data in datas:
            props[attr(data, "name")] = val(get1(data, "value"))
        simple_datas = get(x, "SimpleData")
        for simple_data in simple_datas:
            name = attr(simple_data, "name")
            convert_type = schema.get(name, _identity)
            props[name] = convert_type(val(simple_data))
    for x in get(node, "TimeSpan")[:1]:
        begin = val(get1(x, "begin"))
        end = val(get1(x, "end"))
        props["timeSpan"] = {"begin": begin, "end": end}
    for x in get(node, "TimeStamp")[:1]:
        when = val(get1(x, "when"))
        if when:
            props["timeStamp"] = when
    return props


def build_feature(
    node: md.Document,
    schema: dict | None = None,
    *,
    skip_null_geometry: bool = False,
) -> dict | None:
    """
    Build and return a (decoded) GeoJSON Feature corresponding to this KML node (typically a KML Placemark).

    If a schema dictionary from :func:`build_schema` is given, use it to convert <SimpleData> values to typed Python values.
    Otherwise, build the schema from the node's document.

    If the node contains no geometry, then set the Feature's geometry to ``None``, or return ``None`` instead if ``skip_null_geometry``.
    """
    geoms_and_times = build_geometry(node)
    geoms = geoms_and_times["geoms"]
    if not geoms and skip_null_geometry:
        return None

    if schema is None:
        schema = build_schema(_document(node))

    props = _build_common_props(node, schema)
    if geoms_and_times["times"]:
        times = geoms_and_times["times"]
        props["coordinateProperties"] = {"times": times[0] if len(times) == 1 else times}

    feature = {
        "type": "Feature",
        "properties": props,
    }

    if not geoms:
        feature["geometry"] = None
    elif len(geoms) == 1:
        feature["geometry"] = geoms[0]
    else:
        feature["geometry"] = {
            "type": "GeometryCollection",
            "geometries": geoms,
        }

    if attr(node, "id"):
        feature["id"] = attr(node, "id")

    return feature


def _rotate_box(
    bbox: list[float], coordinates: list[list[list[float]]], rotation: float
) -> list[list[list[float]]]:
    """
    Rotate the given Polygon coordinates counterclockwise about the center of the given bounding box by the given rotation in degrees.
    """
    center = [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]
    ring = []
    for coordinate in coordinates[0]:
        dx = coordinate[0] - center[0]
        dy = coordinate[1] - center[1]
        distance = math.hypot(dx, dy)
        angle = math.atan2(dy, dx) + rotation * DEGREES_TO_RADIANS
        ring.append(
            [
                center[0] + math.cos(angle) * distance,
                center[1] + math.sin(angle) * distance,
            ]
        )
    return [ring]


def build_ground_overlay(
    node: md.Document,
    schema: dict | None = None,
    *,
    skip_null_geometry: bool = False,
) -> dict | None:
    """
    Build and return a (decoded) GeoJSON Feature with a Polygon geometry corresponding to this KML GroundOverlay node.

    Both <LatLonBox> (with optional rotation) and <gx:LatLonQuad> overlays are supported.
    The Feature gets the property ``'@geometry-type': 'groundoverlay'`` and the overlay's image URL in the ``'iconUrl'`` property.

    If the node contains no valid box, then set the Feature's geometry to ``None``, or return ``None`` instead if ``skip_null_geometry``.
    """
    geometry = None
    bbox = None
    quad = get1(node, "gx:LatLonQuad")
    if quad is not None:
        s = val(get1(quad, "coordinates"))
        if s:
            ring = fix_ring(coords(s))
            if len(ring) >= 4:
                geometry = {"type": "Polygon", "coordinates": [ring]}
    else:
        box = get1(node, "LatLonBox")
        if box is not None:
            north = valf(get1(box, "north"))
            south = valf(get1(box, "south"))
            east = valf(get1(box, "east"))
            west = valf(get1(box, "west"))
            rotation = valf(get1(box, "rotation"))
            if all(x is not None for x in [north, south, east, west]):
                bbox = [west, south, east, north]
                coordinates = [
                    [
                        [west, north],
                        [east, north],
                        [east, south],
                        [west, south],
                        [west, north],
                    ]
                ]
                if rotation is not None:
                    coordinates = _rotate_box(bbox, coordinates, rotation)
                geometry = {"type": "Polygon", "coordinates": coordinates}

    if geometry is None and skip_null_geometry:
        return None

    if schema is None:
        schema = build_schema(_document(node))

    props = {"@geometry-type": "groundoverlay"}
    props.update(_build_common_props(node, schema))
    for child in node.childNodes:
        if _is_element(child) and child.tagName == "Icon":
            href = val(get1(child, "href"))
            if href:
                props["iconUrl"] = href
            break

    feature = {
        "type": "Feature",
        "properties": props,
        "geometry": geometry,
    }

    if bbox is not None:
        feature["bbox"] = bbox

    if attr(node, "id"):
        feature["id"] = attr(node, "id")

    return feature


def build_network_link(
    node: md.Document,
    schema: dict | None = None,
    *,
    skip_null_geometry: bool = False,
) -> dict | None:
    """
    Build and return a (decoded) GeoJSON Feature corresponding to this KML NetworkLink node.

    The linked KML file is *not* fetched.
    Instead, the Feature gets the property ``'@geometry-type': 'networklink'``, the <Link> subelement's fields as properties, and a Polygon geometry built from the NetworkLink's <Region> bounding box, if present.

    If the node contains no region box, then set the Feature's geometry to ``None``, or return ``None`` instead if ``skip_null_geometry``.
    """
    geometry = None
    bbox = None
    lod = None
    region = get1(node, "Region")
    if region is not None:
        box = get1(region, "LatLonAltBox")
        if box is not None:
            north = valf(get1(box, "north"))
            south = valf(get1(box, "south"))
            east = valf(get1(box, "east"))
            west = valf(get1(box, "west"))
            if all(x is not None for x in [north, south, east, west]):
                bbox = [west, south, east, north]
                geometry = {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [west, north],
                            [east, north],
                            [east, south],
                            [west, south],
                            [west, north],
                        ]
                    ],
                }
        lod_node = get1(region, "Lod")
        if lod_node is not None:
            min_lod = valf(get1(lod_node, "minLodPixels"))
            max_lod = valf(get1(lod_node, "maxLodPixels"))
            lod = [
                min_lod if min_lod is not None else -1,
                max_lod if max_lod is not None else -1,
                valf(get1(lod_node, "minFadeExtent")),
                valf(get1(lod_node, "maxFadeExtent")),
            ]

    if geometry is None and skip_null_geometry:
        return None

    if schema is None:
        schema = build_schema(_document(node))

    props = {"@geometry-type": "networklink"}
    props.update(_build_common_props(node, schema))
    for key in ["refreshVisibility", "flyToView"]:
        for x in get(node, key)[:1]:
            v = val(x)
            if v:
                props[key] = v
    link = get1(node, "Link") or get1(node, "Url")
    if link is not None:
        for key in [
            "href",
            "refreshMode",
            "refreshInterval",
            "viewRefreshMode",
            "viewRefreshTime",
            "viewBoundScale",
            "viewFormat",
            "httpQuery",
        ]:
            v = val(get1(link, key))
            if v:
                props[key] = v
    if lod is not None:
        props["lod"] = lod

    feature = {
        "type": "Feature",
        "properties": props,
        "geometry": geometry,
    }

    if bbox is not None:
        feature["bbox"] = bbox

    if attr(node, "id"):
        feature["id"] = attr(node, "id")

    return feature


def build_feature_collection(
    node: md.Document,
    name: str | None = None,
    *,
    skip_null_geometry: bool = False,
) -> dict:
    """
    Build and return a (decoded) GeoJSON FeatureCollection corresponding to this KML DOM node (typically a KML Folder).
    Include Features built from the node's Placemarks, GroundOverlays, and NetworkLinks.
    If a name is given, store it in the FeatureCollection's ``'name'`` attribute.

    If ``skip_null_geometry``, then omit Features without geometry.
    """
    schema = build_schema(_document(node))

    # Initialize
    geojson = {
        "type": "FeatureCollection",
        "features": [],
    }

    # Build features
    for placemark in get(node, "Placemark"):
        feature = build_feature(placemark, schema, skip_null_geometry=skip_null_geometry)
        if feature is not None:
            geojson["features"].append(feature)
    for overlay in get(node, "GroundOverlay"):
        feature = build_ground_overlay(
            overlay, schema, skip_null_geometry=skip_null_geometry
        )
        if feature is not None:
            geojson["features"].append(feature)
    for link in get(node, "NetworkLink"):
        feature = build_network_link(link, schema, skip_null_geometry=skip_null_geometry)
        if feature is not None:
            geojson["features"].append(feature)

    # Give the collection a name if requested
    if name is not None:
        geojson["name"] = name

    return geojson


def build_feature_tree(node: md.Document, *, skip_null_geometry: bool = False) -> dict:
    """
    Build and return a tree of (decoded) GeoJSON Features that preserves the given KML DOM node's nested folder structure.

    The tree has the form::

        {
            "type": "root",
            "children": [
                {
                    "type": "folder",
                    "meta": {"name": "Test"},
                    "children": [
                        # ...features and folders
                    ],
                },
                # ...features
            ],
        }

    where folder metadata contains the folder's properties named in :const:`FOLDER_PROPS`.

    If ``skip_null_geometry``, then omit Features without geometry.
    """
    schema = build_schema(_document(node))
    tree = {"type": "root", "children": []}

    def visit(n, pointer):
        for child in n.childNodes:
            if not _is_element(child):
                continue
            tag = child.tagName
            if tag == "Placemark":
                feature = build_feature(
                    child, schema, skip_null_geometry=skip_null_geometry
                )
                if feature is not None:
                    pointer["children"].append(feature)
            elif tag == "GroundOverlay":
                feature = build_ground_overlay(
                    child, schema, skip_null_geometry=skip_null_geometry
                )
                if feature is not None:
                    pointer["children"].append(feature)
            elif tag == "NetworkLink":
                feature = build_network_link(
                    child, schema, skip_null_geometry=skip_null_geometry
                )
                if feature is not None:
                    pointer["children"].append(feature)
            elif tag == "Folder":
                meta = {}
                for grandchild in child.childNodes:
                    if _is_element(grandchild) and grandchild.tagName in FOLDER_PROPS:
                        v = val(grandchild)
                        if v:
                            meta[grandchild.tagName] = v
                folder = {"type": "folder", "meta": meta, "children": []}
                pointer["children"].append(folder)
                visit(child, folder)
            else:
                visit(child, pointer)

    visit(node, tree)
    return tree


def build_layers(
    node: md.Document,
    *,
    disambiguate_names: bool = True,
    skip_null_geometry: bool = False,
) -> list[dict]:
    """
    Return a list of GeoJSON FeatureCollections, one for each folder in the given KML DOM node that contains geodata.
    Name each FeatureCollection (via a ``'name'`` attribute) according to its corresponding KML folder name.

    If ``disambiguate_names == True``, then disambiguate repeated layer names via :func:`disambiguate`.

    If ``skip_null_geometry``, then omit Features without geometry.

    Warning: this can produce layers with the same geodata in case the KML node has nested folders with geodata.
    """
    layers = []
    names = []
    for i, folder in enumerate(get(node, "Folder")):
        name = val(get1(folder, "name"))
        geojson = build_feature_collection(
            folder, name, skip_null_geometry=skip_null_geometry
        )
        if geojson["features"]:
            layers.append(geojson)
            names.append(name)

    if not layers:
        # No folders, so use the root node
        name = val(get1(node, "name"))
        geojson = build_feature_collection(
            node, name, skip_null_geometry=skip_null_geometry
        )
        if geojson["features"]:
            layers.append(geojson)
            names.append(name)

    if disambiguate_names:
        new_names = disambiguate(names)
        new_layers = []
        for i, layer in enumerate(layers):
            layer["name"] = new_names[i]
            new_layers.append(layer)
        layers = new_layers

    return layers


def convert(
    kml_path_or_buffer: str | pl.Path | TextIO | BinaryIO,
    feature_collection_name: str | None = None,
    style_type: str | None = None,
    *,
    separate_folders: bool = False,
    skip_null_geometry: bool = False,
    style_map_key: str = "normal",
) -> dict:
    """
    Given a path to a KML file or given a KML file object, convert it to GeoJSON.
    Close the KML file afterwards.

    Return a dictionary with the key 'feature_collections', whose value is a list containing a single GeoJSON FeatureCollection dictionary named ``feature_collection_name``.

    If ``separate_folders``, then the list contains several FeatureCollections instead, one for each folder in the KML file that contains geodata or that has a descendant node that contains geodata.
    Warning: this can produce FeatureCollections with the same geodata in case the KML file has nested folders with geodata.

    If ``skip_null_geometry``, then omit Features without geometry.

    If a style type from :const:`STYLE_TYPES` is given, then also include the key 'style', whose value is a JSON dictionary that encodes into the style type the style information contained in the KML file.
    KML StyleMaps are resolved to the style referenced by their pair with key ``style_map_key``, which is 'normal' by default.
    """
    # Read KML
    if isinstance(kml_path_or_buffer, (str, pl.Path)):
        kml_path_or_buffer = pl.Path(kml_path_or_buffer).resolve()
        with kml_path_or_buffer.open(encoding="utf-8", errors="ignore") as src:
            kml_str = src.read()
    else:
        kml_str = kml_path_or_buffer.read()
        kml_path_or_buffer.close()

    # Parse KML
    root = md.parseString(kml_str)

    # Build GeoJSON layers
    if separate_folders:
        feature_collections = build_layers(root, skip_null_geometry=skip_null_geometry)
    else:
        feature_collections = [
            build_feature_collection(
                root,
                name=feature_collection_name,
                skip_null_geometry=skip_null_geometry,
            )
        ]

    result = {"feature_collections": feature_collections}

    if style_type is not None:
        # Build style dictionary
        if style_type not in STYLE_TYPES:
            raise ValueError(f"style type must be one of {STYLE_TYPES}")
        builder = build_svg_style if style_type == "svg" else build_leaflet_style
        result["style"] = builder(root, style_map_key=style_map_key)

    return result
