# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc._bundle import Bundle

from .._sound import Sound

from typing import TYPE_CHECKING
from numbers import Real

if TYPE_CHECKING:
    from ..._managers._audio import SoundGroup

# ======================================== BUNDLE ========================================
class SoundBundle(Bundle):
    """Paquet d'effets sonores"""
    __slots__ = ("_volume", "_cooldown", "_group")

    def __init__(self, paths: dict[str, str], volume: Real = 1.0, cooldown: Real = 0.0, group: SoundGroup = None):
        super().__init__(paths)
        self._volume: Real = volume
        self._cooldown: Real = cooldown
        self._group: SoundGroup | None = group

    # ======================================== PROPERTIES ========================================
    @property
    def volume(self) -> Real:
        """Volume de lecture des sons du bundle

        Le volume doit être un ``Réel`` positif.
        Mettre cette propriété à ``1.0`` pour un volume normal.
        """
        return self._volume
    
    @volume.setter
    def volume(self, value: Real) -> None:
        value = float(value)
        assert value >= 0.0, f"volume ({value}) must be positive"
        self._volume = value

    @property
    def cooldown(self) -> Real:
        """Cooldown entre les lectures des sons du bundle

        Le cooldown doit être un ``Réel`` positif.
        Mettre cette propriété à ``0.0`` pour ne pas appliquer de cooldown.
        """
        return self._cooldown

    @cooldown.setter
    def cooldown(self, value: Real) -> None:
        value = float(value)
        assert value >= 0.0, f"cooldown ({value}) must be positive"
        self._cooldown = value

    @property
    def group(self) -> SoundGroup | None:
        """Groupe de sons auquel les sons du bundle appartiennent
        
        Mettre cette propriété à ``None`` pour utiliser le groupe par défaut.
        """
        return self._group
    
    @group.setter
    def group(self, value: SoundGroup | None) -> None:
        assert value is None or isinstance(value, SoundGroup), f"group must be a SoundGroup or None, not {type(value).__name__}"
        self._group = value

    # ======================================== INTERFACE ========================================
    def get(self, key: str, volume: Real | None = None, cooldown: Real | None = None, group: SoundGroup | None = None) -> Sound:
        """Renvoie le chemin d'accès à un son du bundle

        Args:
            key: clé du son à récupérer
            volume: volume (volume du Bundle si ``None``)
            cooldown: délai (délai du Bundle si ``None``)
            group: groupe de sons (groupe du Bundle si ``None``)
        """
        # Choix des paramètres du son
        volume = volume if volume is not None else self._volume
        cooldown = cooldown if cooldown is not None else self._cooldown
        group = group if group is not None else self._group

        # Génération de la clé de cache
        cache_key  = (key, volume, cooldown, group)
        if cache_key not in self._cache:
            self._cache[cache_key] = Sound(
                path = self._paths[key],
                volume = volume,
                cooldown = cooldown,
                group = group,
            )

        return self._cache[cache_key]