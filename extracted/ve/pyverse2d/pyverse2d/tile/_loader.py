# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..shape import Rect, Polygon

from ._tile import Tile, TileMeta
from ._tile_map import TileMap, FLIP_H, FLIP_V, FLIP_D
from ._map_asset import MapAsset

import json
import numpy as np
from pathlib import Path
from xml.etree import ElementTree as ET

# ======================================== LOADER ========================================
class MapLoader:
    """Charge un fichier de map externe et produit un MapAsset"""

    # ======================================== TILED JSON ========================================
    @staticmethod
    def from_tiled_json(path: str | Path, scale: float = 1.0, tile_width: float = 1.0, tile_height: float = 1.0) -> MapAsset:
        """Charge un fichier Tiled au format JSON

        Args:
            path(str | Path): chemin du fichier
            scale(float, optional): facteur de redimensionnement des tuiles monde
            tile_width(float, optional): largeur cible des tuiles en unités
            tile_height(float, optional): hauteur cible des tuiles en unités
        """
        path = Path(path)
        raw = json.loads(path.read_text(encoding="utf-8"))

        tiles = _load_tiles_json(raw["tilesets"], path.parent, tile_width, tile_height)
        layers = {}

        for layer in raw.get("layers", []):
            if layer["type"] != "tilelayer":
                continue
            layers[layer["name"]] = _parse_layer_json(layer, raw, tiles, scale, tile_width, tile_height)

        return MapAsset(layers)

    # ======================================== TILED TMX ========================================
    @staticmethod
    def from_tiled_tmx(path: str | Path, scale: float = 1.0, tile_width: float = 1.0, tile_height: float = 1.0) -> MapAsset:
        """Charge un fichier Tiled au format natif XML (.tmx)

        Args:
            path(str | Path): chemin du fichier
            scale(float, optional): facteur de redimensionnement des tuiles monde
            tile_width(float, optional): largeur cible des tuiles monde ; prioritaire sur scale
            tile_height(float, optional): hauteur cible des tuiles monde ; prioritaire sur scale
        """
        path = Path(path)
        root = ET.parse(path).getroot()

        map_tw = int(root.attrib["tilewidth"])
        map_th = int(root.attrib["tileheight"])

        tiles = _load_tiles_tmx(root.findall("tileset"), path.parent, tile_width, tile_height)
        layers = {}

        for layer in root.findall("layer"):
            layers[layer.attrib["name"]] = _parse_layer_tmx(layer, map_tw, map_th, tiles, scale, tile_width, tile_height)

        return MapAsset(layers)


# ======================================== JSON INTERNALS ========================================
def _load_tiles_json(raw_tilesets: list[dict], base_dir: Path, tw: float, th: float) -> list[tuple[int, Tile]]:
    """Charge tous les tilesets JSON et renvoie une liste ``(firstgid, Tile)`` triée

    Args:
        raw_tilesets(list[dict]): liste brute des tilesets depuis le JSON
        base_dir(Path): répertoire de base pour résoudre les chemins relatifs
        tw(float): largeur cible des tuiles en unités monde
        th(float): hauteur cible des tuiles en unités monde
    """
    result = []
    for entry in raw_tilesets:
        firstgid = entry["firstgid"]
        if "source" in entry:
            data = json.loads((base_dir / entry["source"]).read_text(encoding="utf-8"))
        else:
            data = entry
        result.append((firstgid, _tile_from_dict(data, base_dir, tw, th)))
    result.sort(key=lambda t: t[0])
    return result


def _tile_from_dict(data: dict, base_dir: Path, tw: float, th: float) -> Tile:
    """Construit un Tile depuis un dict JSON de tileset

    Args:
        data(dict): données brutes du tileset
        base_dir(Path): répertoire de base pour résoudre les chemins relatifs
        tw(float): largeur cible des tuiles en unités monde
        th(float): hauteur cible des tuiles en unités monde
    """
    src_tw = data["tilewidth"]
    src_th = data["tileheight"]
    tile = Tile(
        image_path = str(base_dir / data["image"]),
        tile_width = src_tw,
        tile_height = src_th,
        margin = data.get("margin", 0),
        spacing = data.get("spacing", 0),
    )
    for tile_data in data.get("tiles", []):
        local_id = tile_data["id"] + 1
        props = {p["name"]: p["value"] for p in tile_data.get("properties", [])}
        shape = _parse_collision_shape_json(tile_data, src_tw, src_th, tw, th)
        meta = _meta_from_props_dict(props, shape)
        if meta is not None:
            tile.set_meta(local_id, meta)
    return tile


def _parse_layer_json(layer: dict, raw: dict, tiles: list[tuple[int, Tile]], scale: float = 1.0, tile_width: float = 1.0, tile_height: float = 1.0) -> TileMap:
    """Construit un TileMap depuis un layer JSON Tiled

    Args:
        layer(dict): données brutes du layer
        raw(dict): données brutes de la map entière (pour tilewidth/tileheight globaux)
        tiles(list): liste (firstgid, Tile) issue de _load_tiles_json
        scale(float, optional): facteur de redimensionnement fallback
        tile_width(float, optional): largeur cible des tuiles en unités monde
        tile_height(float, optional): hauteur cible des tuiles en unités monde
    """
    cols = layer["width"]
    rows = layer["height"]
    flags_flat, flat_ids = _extract_flags(layer["data"])
    firstgid, tile = _tile_for(flat_ids, tiles)
    local_ids = [(gid - firstgid + 1) if gid != 0 else 0 for gid in flat_ids]
    grid = np.array(local_ids, dtype=np.int32).reshape(rows, cols)
    flags = np.array(flags_flat, dtype=np.uint8).reshape(rows, cols)
    grid = np.flipud(grid)
    flags = np.flipud(flags)
    tw = tile_width if tile_width is not None else raw["tilewidth"]  * scale
    th = tile_height if tile_height is not None else raw["tileheight"] * scale
    return TileMap(tile=tile, grid=grid, flags=flags, tile_width=tw, tile_height=th)


def _parse_collision_shape_json(tile_data: dict, src_tw: int, src_th: int, tw: float, th: float):
    """Parse l'objectgroup d'une tuile JSON et renvoie la Shape correspondante

    Args:
        tile_data: données brutes de la tuile
        src_tw: largeur pixel de la tuile source
        src_th: hauteur pixel de la tuile source
        tw: largeur cible en unités monde
        th: hauteur cible en unités monde
    """
    og = tile_data.get("objectgroup")
    if og is None:
        return None
    objects = og.get("objects", [])
    if not objects:
        return None
    obj = objects[0]

    ox = float(obj.get("x", 0))
    oy = float(obj.get("y", 0))

    poly = obj.get("polygon")
    if poly is not None:
        pts = []
        for pt in poly:
            px, py = float(pt["x"]), float(pt["y"])
            pts.append((
                (ox + px) / src_tw * tw,
                th - (oy + py) / src_th * th,
            ))
        return Polygon(*pts)

    w = float(obj.get("width", src_tw))
    h = float(obj.get("height", src_th))
    return Rect(w / src_tw * tw, h / src_th * th)


# ======================================== TMX INTERNALS ========================================
def _load_tiles_tmx(tileset_nodes: list[ET.Element], base_dir: Path, tw: float, th: float) -> list[tuple[int, Tile]]:
    """Charge tous les tilesets TMX et renvoie une liste ``(firstgid, Tile)`` triée

    Args:
        tileset_nodes: noeuds <tileset> de la map
        base_dir: répertoire de base pour résoudre les chemins relatifs
        tw: largeur cible des tuiles en unités monde
        th: hauteur cible des tuiles en unités monde
    """
    result = []
    for node in tileset_nodes:
        firstgid = int(node.attrib["firstgid"])
        if "source" in node.attrib:
            tsx_path = base_dir / node.attrib["source"]
            tsx_root = ET.parse(tsx_path).getroot()
            tile = _tile_from_tsx(tsx_root, tsx_path.parent, tw, th)
        else:
            tile = _tile_from_tsx(node, base_dir, tw, th)
        result.append((firstgid, tile))
    result.sort(key=lambda t: t[0])
    return result


def _tile_from_tsx(node: ET.Element, base_dir: Path, tw: float, th: float) -> Tile:
    """Construit un Tile depuis un noeud TSX/XML

    Args:
        node: noeud racine du tileset
        base_dir: répertoire de base pour résoudre les chemins relatifs
        tw: largeur cible des tuiles en unités monde
        th: hauteur cible des tuiles en unités monde
    """
    image_node = node.find("image")
    src_tw = int(node.attrib["tilewidth"])
    src_th = int(node.attrib["tileheight"])
    tile = Tile(
        image_path = str(base_dir / image_node.attrib["source"]),
        tile_width = src_tw,
        tile_height = src_th,
        margin = int(node.attrib.get("margin", 0)),
        spacing = int(node.attrib.get("spacing", 0)),
    )
    for tile_node in node.findall("tile"):
        local_id = int(tile_node.attrib["id"]) + 1
        props_node = tile_node.find("properties")
        props = {}
        if props_node is not None:
            props = {
                p.attrib["name"]: _cast_xml_prop(p)
                for p in props_node.findall("property")
            }
        shape = _parse_collision_shape(tile_node, src_tw, src_th, tw, th)
        meta = _meta_from_props_dict(props, shape)
        if meta is not None:
            tile.set_meta(local_id, meta)
    return tile


def _parse_layer_tmx(layer: ET.Element, map_tw: int, map_th: int, tiles: list[tuple[int, Tile]], scale: float = 1.0, tile_width: float = 1.0, tile_height: float = 1.0) -> TileMap:
    """Construit un TileMap depuis un layer TMX Tiled

    Args:
        layer: noeud <layer> de la map
        map_tw: largeur pixel des tuiles déclarée dans la map
        map_th: hauteur pixel des tuiles déclarée dans la map
        tiles: liste (firstgid, Tile) issue de _load_tiles_tmx
        scale(: facteur de redimensionnement fallback
        tile_width: largeur cible des tuiles en unités monde
        tile_height: hauteur cible des tuiles en unités monde
    """
    cols      = int(layer.attrib["width"])
    rows      = int(layer.attrib["height"])
    data_node = layer.find("data")
    encoding  = data_node.attrib.get("encoding", "xml")

    if encoding == "csv":
        raw_ids = [int(v) for v in data_node.text.strip().split(",") if v.strip()]
    elif encoding == "xml":
        raw_ids = [int(tile.attrib["gid"]) for tile in data_node.findall("tile")]
    else:
        raise NotImplementedError(f"Encodage TMX non supporté : '{encoding}' (utilisez CSV ou XML dans Tiled)")

    flags_flat, flat_ids = _extract_flags(raw_ids)
    firstgid, tile = _tile_for(flat_ids, tiles)
    local_ids = [(gid - firstgid + 1) if gid != 0 else 0 for gid in flat_ids]
    grid  = np.array(local_ids, dtype=np.int32).reshape(rows, cols)
    flags = np.array(flags_flat, dtype=np.uint8).reshape(rows, cols)
    grid  = np.flipud(grid)
    flags = np.flipud(flags)
    tw = tile_width  if tile_width  is not None else map_tw * scale
    th = tile_height if tile_height is not None else map_th * scale
    return TileMap(tile=tile, grid=grid, flags=flags, tile_width=tw, tile_height=th)


# ======================================== SHARED INTERNALS ========================================
def _cast_xml_prop(prop: ET.Element):
    """Convertit une propriété XML Tiled vers le bon type Python

    Args:
        prop(ET.Element): noeud <property>
    """
    ptype = prop.attrib.get("type", "string")
    value = prop.attrib.get("value", "")
    if ptype == "bool": return value == "true"
    if ptype == "float": return float(value)
    if ptype == "int": return int(value)
    return value


def _parse_collision_shape(tile_node, src_tw: int, src_th: int, tw: float, th: float):
    """Parse l'objectgroup d'une tuile TMX et renvoie la Shape correspondante

    Args:
        tile_node: noeud <tile> du tileset
        src_tw: largeur pixel de la tuile source
        src_th: hauteur pixel de la tuile source
        tw: largeur cible en unités monde
        th: hauteur cible en unités monde
    """
    og = tile_node.find("objectgroup")
    if og is None:
        return None
    obj = og.find("object")
    if obj is None:
        return None

    ox = float(obj.attrib.get("x", 0))
    oy = float(obj.attrib.get("y", 0))

    poly = obj.find("polygon")
    if poly is not None:
        pts = []
        for pair in poly.attrib["points"].split():
            px, py = pair.split(",")
            pts.append((
                (ox + float(px)) / src_tw * tw,
                th - (oy + float(py)) / src_th * th,
            ))
        return Polygon(*pts)

    w = float(obj.attrib.get("width", src_tw))
    h = float(obj.attrib.get("height", src_th))
    return Rect(w / src_tw * tw, h / src_th * th)


def _meta_from_props_dict(props: dict, collision_shape=None) -> TileMeta | None:
    """Construit un TileMeta depuis un dict de propriétés

    Args:
        props: propriétés brutes de la tuile
        collision_shape: shape de collision pré-parsée
    """
    tags = []
    friction = props.get("friction")
    restitution = props.get("restitution")
    category = props.get("category")
    mask = props.get("mask")

    if props.get("solid"): tags.append("solid")
    if props.get("ladder"): tags.append("ladder")
    if props.get("one_way"): tags.append("one_way")

    if not tags and friction is None and restitution is None and category is None and mask is None and collision_shape is None:
        return None

    return TileMeta(
        *tags,
        friction = friction,
        restitution = restitution,
        category = int(category) if category is not None else None,
        mask = int(mask) if mask is not None else None,
        collision_shape = collision_shape,
    )


def _extract_flags(raw_ids: list[int]) -> tuple[list[int], list[int]]:
    """Extrait les bits de flip Tiled et renvoie (flags, ids_masqués)

    Args:
        raw_ids: liste brute des GIDs avec bits de flip encodés
    """
    GID_FLIP_H = 0x80000000
    GID_FLIP_V = 0x40000000
    GID_FLIP_D = 0x20000000
    GID_MASK = 0x1FFFFFFF
    flags = []
    ids = []
    for gid in raw_ids:
        f = 0
        if gid & GID_FLIP_H: f |= FLIP_H
        if gid & GID_FLIP_V: f |= FLIP_V
        if gid & GID_FLIP_D: f |= FLIP_D
        flags.append(f)
        ids.append(gid & GID_MASK)
    return flags, ids


def _tile_for(flat_ids: list[int], tiles: list[tuple[int, Tile]]) -> tuple[int, Tile]:
    """Renvoie le (firstgid, Tile) correspondant au GID minimal de la liste

    Args:
        flat_ids: liste des GIDs du layer
        tiles: liste ``(firstgid, Tile)`` triée par firstgid croissant
    """
    non_empty = [gid for gid in flat_ids if gid != 0]
    if not non_empty:
        return tiles[0]
    min_gid = min(non_empty)
    candidate = tiles[0]
    for firstgid, tile in tiles:
        if firstgid <= min_gid:
            candidate = (firstgid, tile)
    return candidate