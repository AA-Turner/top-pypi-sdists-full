# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect

from ._tile_map import TileMap

# ======================================== MAP ASSET ========================================
class MapAsset:
    """
    Conteneur de couches issues d'un même fichier de map

    Args:
        layers(dict[str, TileMap]): couches nommées
    """
    __slots__ = ("_layers",)

    def __init__(self, layers: dict[str, TileMap]):
        expect(layers, dict)
        self._layers: dict[str, TileMap] = {
            expect(k, str): expect(v, TileMap)
            for k, v in layers.items()
        }

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        keys = list(self._layers.keys())
        return f"MapAsset(layers={keys})"

    # ======================================== ACCÈS ========================================
    def __getitem__(self, name: str) -> TileMap:
        """
        Renvoie la couche par son nom

        Args:
            name(str): nom de la couche
        """
        try:
            return self._layers[expect(name, str)]
        except KeyError:
            available = list(self._layers.keys())
            raise KeyError(f"Layer '{name}' introuvable. Couches disponibles : {available}")

    def __contains__(self, name: str) -> bool:
        """Vérifie si une couche existe"""
        return name in self._layers

    def __iter__(self):
        """Itère sur les noms de couches"""
        return iter(self._layers)

    def __len__(self) -> int:
        """Renvoie le nombre de couches"""
        return len(self._layers)

    # ======================================== GETTERS ========================================
    @property
    def layer_names(self) -> list[str]:
        """Renvoie les noms de couches dans l'ordre d'insertion"""
        return list(self._layers.keys())

    def get(self, name: str, default: TileMap | None = None) -> TileMap | None:
        """
        Renvoie la couche par son nom, ou default si absente

        Args:
            name(str): nom de la couche
            default(TileMap, optional): valeur par défaut
        """
        return self._layers.get(expect(name, str), default)