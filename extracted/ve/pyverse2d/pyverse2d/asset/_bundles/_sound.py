# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import positive, expect
from ...abc import Bundle

from .._sound import Sound

from typing import TYPE_CHECKING
from numbers import Real

if TYPE_CHECKING:
    from ..._managers._audio import SoundGroup

# ======================================== BUNDLE ========================================
class SoundBundle(Bundle):
    """Paquet d'effets sonores
    
    Args:
        paths: chemins vers les fichiers
        volume: volume par défaut
        cooldown: délai entre chaque lecture d'un son par défaut
        group: ``SoundGroup`` des sons par défaut
    """
    __slots__ = ("_volume", "_cooldown", "_group")

    def __init__(self, paths: dict[str, str], volume: Real = 1.0, cooldown: Real = 0.0, group: SoundGroup = None):
        # Initialisation du paquet
        super().__init__(paths)

        # Transtypage et vérifications
        volume = float(volume)
        cooldown = float(cooldown)
        
        if __debug__:
            positive(volume)
            positive(cooldown)
            expect(group, (Sound._get_group_class(), None))

        # Attributs publiques
        self._volume: float = volume
        self._cooldown: float = cooldown
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
        if __debug__:
            positive(value)
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
        if __debug__:
            positive(value)
        self._cooldown = value

    @property
    def group(self) -> SoundGroup | None:
        """Groupe de sons auquel les sons du bundle appartiennent
        
        Mettre cette propriété à ``None`` pour utiliser le groupe par défaut.
        """
        return self._group
    
    @group.setter
    def group(self, value: SoundGroup | None) -> None:
        if __debug__:
            expect(value, (Sound._get_group_class(), None))
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
    
# ======================================== EXPORTS ========================================
__all__ = [
    "SoundBundle",
]