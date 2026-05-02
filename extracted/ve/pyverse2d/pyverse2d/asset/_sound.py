from __future__ import annotations

from .._internal import expect, positive
from .._flag import AudioState
from ..abc import Asset

from typing import TYPE_CHECKING, Type, Any, Callable
from numbers import Real
import os

if TYPE_CHECKING:
    from .._managers._audio import AudioManager, SoundGroup, SoundHandle

class Sound(Asset):
    """Son court chargé en mémoire *(SFX)*

    Args:
        path: chemin vers le fichier audio
        volume: volume propre [0, 1]
        cooldown: délai minimal entre deux lectures *(secondes)*
        group: groupe auquel appartient ce son
    """
    __slots__ = (
        "_path", "_volume", "_cooldown", "_group",
        "_paths", "_handles", "_cooldown_timer", "_state",
    )

    _GROUP_CLASS: Type[SoundGroup] = None
    _AUDIO_MANAGER: AudioManager = None

    @classmethod
    def _get_group_class(cls) -> Type[SoundGroup]:
        """Renvoie la class ``SoundGroup``"""
        if cls._GROUP_CLASS is None:
            from .._managers._audio import SoundGroup
            cls._GROUP_CLASS = SoundGroup
        return cls._GROUP_CLASS

    @classmethod
    def _get_audio_manager(cls) -> AudioManager:
        """Renvoie le gestionnaire audio"""
        if cls._AUDIO_MANAGER is None:
            from .._managers._audio import AudioManager
            cls._AUDIO_MANAGER = AudioManager.get_instance()
        return cls._AUDIO_MANAGER

    def __init__(
        self,
        path: str,
        volume: Real = 1.0,
        cooldown: float = 0.0,
        group: SoundGroup | None = None,
    ):
        self._path: str = path
        self._volume: float = float(volume)
        self._cooldown: float = float(cooldown)
        self._group: SoundGroup | None = group

        if __debug__:
            positive(self._volume)
            positive(self._cooldown)
            expect(self._group, (self._get_group_class(), None))

        self._paths: list[str] = [path]
        self._handles: set[SoundHandle] = set()
        self._cooldown_timer: float = 0.0
        self._state: AudioState = AudioState.SLEEPING

    def __hash__(self) -> int:
        """Renvoie le hash du son"""
        return hash((self._path, self._volume, self._cooldown, self._group))
    
    # ======================================== FACTORY ========================================
    @classmethod
    def from_variations(
        cls,
        folder_path: str,
        prefix: str = "",
        extensions: list[str] = None,
        volume: Real = 1.0,
        cooldown: float = 0.0,
        group: SoundGroup | None = None,
    ) -> Sound:
        """Crée un son avec ses variations à partir d'un dossier.

        Le premier fichier trouvé (ordre alphabétique) devient le son principal.
        les suivants sont ajoutés comme variations.

        Args:
            folder_path: chemin vers le dossier contenant les fichiers audio
            prefix: ne retenir que les fichiers dont le nom commence par ce préfixe
            extensions: liste des extensions à inclure
            volume: volume propre [0, 1]
            cooldown: délai minimal entre deux lectures *(secondes)*
            group: groupe auquel appartient ce son
        """
        paths: list[str] = []
        for filename in sorted(os.listdir(folder_path)):
            name, ext = os.path.splitext(filename)
            if extensions is not None and ext.lower() not in extensions:
                continue
            if prefix and not name.startswith(prefix):
                continue
            paths.append(os.path.join(folder_path, filename))
        if not paths:
            raise FileNotFoundError(f"No sound found in '{folder_path}'" + (f" with prefix '{prefix}'" if prefix else "") + (f" and extensions {extensions}" if extensions else ""))
        sound = cls(path=paths[0], volume=volume, cooldown=cooldown, group=group)
        for path in paths[1:]:
            sound.add_variation(path)
        return sound

    # ======================================== PROPERTIES ========================================
    @property
    def path(self) -> str:
        """Chemin du fichier audio"""
        return self._path

    @path.setter
    def path(self, value: str) -> None:
        self._path = value
        self._refresh_paths()

    @property
    def volume(self) -> float:
        """Volume propre
        
        Le volume doit être un ``Réel`` positif.
        """
        return self._volume

    @volume.setter
    def volume(self, value: float) -> None:
        value = float(value)
        assert value >= 0.0, f"volume ({value}) must be positive"
        self._volume = value

    @property
    def cooldown(self) -> float:
        """Délai minimal entre deux lectures

        Le délai doit être un ``Réel`` positif.
        Mettre cette propriété à ``0.0`` pour ne pas avoir de délai.
        """
        return self._cooldown

    @cooldown.setter
    def cooldown(self, value: float) -> None:
        value = float(value)
        assert value >= 0.0, f"cooldown ({value}) must be positive"
        self._cooldown = value

    @property
    def group(self) -> SoundGroup:
        """Groupe de sons

        Le groupe doit être un ``SoundGroup``.
        Mettre cette propriété à ``None`` pour être lu dans le groupe par défaut.
        """
        return self._group

    @group.setter
    def group(self, value: SoundGroup | None) -> None:
        assert isinstance(value, self._get_group_class()), f"group ({value}) must be a SoundGroup"
        self._group = value

    # ======================================== PREDICATES ========================================
    def __eq__(self, other: object) -> bool:
        """Vérifie la correspondance de deux sons"""
        if isinstance(other, Sound):
            return (self._path == other.path
                and self._volume == other.volume
                and self._cooldown == other.cooldown
                and self._group == other.group)
        return NotImplemented

    def is_ready(self) -> bool:
        """Vérifie que le son soit prêt à être joué"""
        return self._cooldown_timer == 0.0

    def is_playing(self) -> bool:
        """Vérifie que le son soit entrain d'être joué"""
        return self._state == AudioState.PLAYING

    def is_paused(self) -> bool:
        """Vérifie que le son soit en pause"""
        return self._state == AudioState.PAUSED

    # ======================================== VARIATIONS ========================================
    def add_variation(self, path: str) -> None:
        """Ajoute une variation audio à ce son.

        Args:
            path: chemin vers le fichier de variation
        """
        self._paths.append(path)

    def remove_variation(self, path: str) -> None:
        """Retire une variation audio de ce son.

        Args:
            path: chemin vers le fichier de variation
        """
        if path == self._paths[0]:
            raise ValueError("cannot remove the main path")
        self._paths.remove(path)
    
    def get_variations(self) -> list[str]:
        """Renvoie la liste des chemins de variation de ce son (lecture seule)"""
        return self._paths[1:]
    
    def has_variation(self, path: str) -> bool:
        """Vérifie que ce son possède une variation audio.

        Args:
            path: chemin vers le fichier de variation
        """
        return path in self._paths[1:]

    # ======================================== INTERFACE ========================================
    def copy(self) -> Sound:
        """Renvoie une copie du son"""
        return Sound(path=self._path, volume=self._volume, cooldown=self._cooldown, group=self._group)

    def play(self, volume: Real = 1.0, loop: bool = False, limit: int | None = None, on_end: Callable[[SoundHandle], Any] = None) -> SoundHandle | None:
        """Joue le son si disponible
        
        Args:
            volume: volume ponctuel *[0, 1]*
            loop: lecture en boucle
            limit: limite d'itérations
            on_end: callback final
        """
        return self._get_audio_manager().play_sound(self, volume=volume, loop=loop, limit=limit, on_end=on_end)

    def resume(self) -> None:
        """Reprend le son"""
        self._get_audio_manager().resume_sound(self)

    def pause(self) -> None:
        """Met le son en pause"""
        self._get_audio_manager().pause_sound(self)

    def stop(self) -> None:
        """Arrête le son"""
        self._get_audio_manager().stop_sound(self)

    # ======================================== INTERNALS ========================================
    def _apply_cooldown(self) -> None:
        """Initialise le délai"""
        self._cooldown_timer = self._cooldown

    def _refresh_paths(self) -> None:
        """Actualise les chemins de variation"""
        self._paths[0] = self._path

    def _tick(self, dt: float) -> bool:
        """Actualise le délai"""
        self._cooldown_timer -= dt
        if self._cooldown_timer <= 0.0:
            self._cooldown_timer = 0.0
            return True
        return False

    def _set_state(self, value: AudioState) -> None:
        """Fixe l'état"""
        self._state = value

    def _add_handle(self, handle: SoundHandle) -> None:
        """Ajoute un handle"""
        self._handles.add(handle)

    def _remove_handle(self, handle: SoundHandle) -> None:
        """Retire un handle"""
        self._handles.discard(handle)

    def _clear_handles(self) -> None:
        """Retire tous les handles"""
        self._handles = set()

    def _get_handles(self) -> frozenset[SoundHandle]:
        """Renvoie les handles (lecture seule)"""
        return self._handles