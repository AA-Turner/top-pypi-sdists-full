# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..typing import DictKeys, DictValues

from abc import ABC, abstractmethod
from typing import Any, TypeAlias
import os
import random

# ======================================== ALIASES ========================================
CacheKey: TypeAlias = tuple | str

# ======================================== ABSTRACT CLASS ========================================
class Bundle(ABC):
    """Classe abstraite des paquets d'assets"""
    __slots__ = ("_paths", "_cache", "_keys_list")

    def __init__(self, paths: dict[str, str]):
        self._paths: dict[str, str] = paths
        self._cache: dict[CacheKey, Any] = {}
        self._keys_list: list[str] = list(paths.keys())

    # ======================================== PROPERTIES ========================================
    @property
    def paths(self) -> dict[str, str]:
        """Renvoie les entrées du bundle"""
        return self._paths

    # ======================================== FACTORY ========================================
    @classmethod
    def from_folder(cls, folder_path: str, prefix: str  ="", extensions: list[str] = None, remove_prefix: bool = False, **kwargs) -> Bundle:
        """Crée un bundle à partir d'un dossier

        Args:
            folder_path: chemin d'accès au dossier contenant les sons
            prefix: préfixe à ajouter à la clé de chaque son du bundle
            extensions: extensions de fichiers à inclure dans le bundle
            remove_prefix: si ``True``, supprime le préfixe du nom
            **kwargs: arguments supplémentaires à passer au constructeur du bundle
        """
        paths: dict[str, str] = {}
        for filename in sorted(os.listdir(folder_path)):
            name, ext = os.path.splitext(filename)
            if extensions is not None and ext.lower() not in extensions:
                continue
            key = name
            if prefix != "":
                if not key.startswith(prefix):
                    continue
                if remove_prefix:
                    key = key[len(prefix):]
            paths[key] = os.path.join(folder_path, filename)
        return cls(paths, **kwargs)

    def preload(self) -> Bundle:
        """Précharge tous les éléments du bundle"""
        for key in self._paths:
            self.get(key)
        return self

    # ======================================== INTERFACE ========================================
    @abstractmethod
    def get(self, key: str, **kwargs) -> Any: ...

    def __getitem__(self, key):
        """Renvoie l'élément associé à la clé"""
        return self.get(key)

    def keys(self) -> DictKeys[str]:
        """Renvoie une vue des clés du bundle"""
        return self._paths.keys()
    
    def keys_list(self) -> list[str]:
        """Renvoie une liste des clés du bundle"""
        return self._keys_list
    
    def values(self) -> DictValues[Any]:
        """Renvoie une vue des valeurs du bundle"""
        return self._paths.values()
    
    def values_list(self) -> list[Any]:
        """Renvoie une liste des valeurs du bundle"""
        return [self.get(value) for value in self._paths]
    
    def values_dict(self) -> dict[str, Any]:
        """Renvoie un dictionnaire des valeurs du bundle"""
        return {name: self.get(value) for name, value in self.paths}
    
    def __iter__(self):
        """Itère sur les entrées du bundle"""
        return iter(self._paths)

    def has(self, key: str) -> bool:
        """Vérifie qu'une clé est présente dans le bundle

        Args:
            key: clé à vérifier
        """
        return key in self._paths
    
    def __contains__(self, key: str) -> bool:
        """Vérifie qu'une clé est présente dans le bundle"""
        return self.has(key)
    
    def __len__(self) -> int:
        """Renvoie le nombre d'entrées du bundle"""
        return len(self._paths)
    
    def random(self) -> Any:
        """Renvoie une entrée aléatoire du bundle"""
        key = random.choice(self._keys_list)
        return self.get(key)