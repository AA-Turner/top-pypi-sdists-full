# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, positive
from .._flag import AudioState
from ..abc import Manager, Request, AudioHandle
from ..asset import Sound, Music, Playlist, SoundBundle, MusicBundle
from ..math.easing import EasingFunc, linear

from ._context import ContextManager

import pyglet.media as _media

import random
from dataclasses import dataclass
from numbers import Real
from typing import ClassVar, Type, Callable, Any

# ======================================== CONSTANTS ========================================
_CROSSFADE_STEPS = 20

# ======================================== HANDLES ========================================
class SoundHandle(AudioHandle):
    """Handle de son en cours de lecture"""
    __slots__ = (
        "sound",
        "loop", "iterations_left",
    )

    def __init__(self, sound: Sound, source: _media.StaticSource, player: _media.Player, on_stop: Callable[[SoundHandle], Any] = None):
        # Attributs publiques
        self.sound: Sound = sound
        
        self.loop: bool = False
        self.iterations_left = None

        # Configuration du token
        super().__init__(source, player, on_stop=on_stop)

    def on_eos(self) -> None:
        """Fin de lecture avec boûcle si loop activé"""
        if not self.loop:
            self.stop()
            return
        if self.iterations_left is None:
            self.player.queue(self.source)
            self.player.play()
        elif self.iterations_left > 1:
            self.iterations_left -= 1
            self.player.queue(self.source)
            self.player.play()
        else:
            self.stop()

    def resume(self) -> None:
        """Reprend le son"""
        if self._active:
            self.player.play()

    def pause(self) -> None:
        """Met le son en pause"""
        if self._active:
            self.player.pause()

    def stop(self) -> None:
        """Arrête le son"""
        if self._active:
            self.sound._remove_handle(self)
            if not self.sound._handles:
                self.sound._set_state(AudioState.SLEEPING)
            self.delete()


class MusicHandle(AudioHandle):
    """Handle de musique en cours de lecture"""
    __slots__ = (
        "music",
    )

    def __init__(self, music: Music, source: _media.StreamingSource, player: _media.Player, on_stop: Callable[[MusicHandle], Any] = None):
        # Attributs publiques
        self.music: Music = music

        # Configuration du token
        super().__init__(source, player, on_stop=on_stop)

    @property
    def duration(self) -> float | None:
        """Durée totale de la musique en secondes"""
        if self._active and self.source.duration is not None:
            return self.source.duration
        return None

    @property
    def time(self) -> float:
        """Temps écoulé en secondes"""
        if self._active:
            return self.player.time
        return 0.0

    @property
    def time_remaining(self) -> float | None:
        """Temps restant en secondes"""
        if self._active and self.source.duration is not None:
            return max(0.0, self.source.duration - self.player.time)
        return None

    def on_eos(self):
        """Fin de lecture"""
        self.stop()

    def resume(self) -> None:
        """Reprend la musique"""
        if self._active:
            self.player.play()
            self.music._set_state(AudioState.PLAYING)

    def pause(self) -> None:
        """Met la musique en pause"""
        if self._active:
            self.player.pause()
            self.music._set_state(AudioState.PAUSED)

    def stop(self) -> None:
        """Arrête la musique"""
        if self._active:
            self.music._set_state(AudioState.SLEEPING)
            self.music._set_handle(None)
            self.delete()

# ======================================== GROUPS ========================================
class SoundGroup:
    """Pool de players pour un groupe de sons

    Args:
        pool_max: nombre de lectures simultanées maximum
        volume: volume du groupe [0, 1]
        parent: groupe parent (hérite du volume)
    """
    __slots__ = (
        "_volume", "_pool_max", "_parent",
        "_handles",
    )

    def __init__(self, volume: Real = 1.0, pool_max: int = None, parent: SoundGroup = None):
        # Attributs publiques
        self._volume: float = float(volume)
        self._pool_max: int | None = pool_max
        self._parent: SoundGroup | None = parent

        if __debug__:
            positive(self._volume)
            expect(self._pool_max, (int, None))
            expect(self._parent, (SoundGroup, None))
        
        # Attributs internes
        self._handles: set[SoundHandle] = set()

    @property
    def volume(self) -> float:
        """Volume du groupe

        Le volume doit être un ``Réel`` positif.
        """
        return self._volume
    
    @volume.setter
    def volume(self, value: Real) -> None:
        value = float(value)
        assert value >= 0.0, f"volume ({value}) must be positive"
        self._volume = value

    @property
    def pool_max(self) -> int | None:
        """Nombre de lectures simultanées maximum

        Cette propriété limite le nombre de sons du groupe joués en même temps.
        Mettre cette propriété à ``None`` pour ne pas imposer de limite.
        """
        return self._pool_max
    
    @pool_max.setter
    def pool_max(self, value: int | None) -> None:
        assert value is None or isinstance(value, int), f"pool_max ({value}) must be an integer or None"
        self._pool_max = value

    @property
    def parent(self) -> SoundGroup:
        """Groupe parent

        Le ``SoundGroup`` hérite du volume du parent.
        Le parent est fixe après initialisation du groupe.
        """
        return self._parent
    
    def get_absolute_volume(self) -> float:
        """Renvoie le volume absolu du groupe"""
        if self._parent is None:
            return self._volume
        return self._volume * self._parent.get_absolute_volume()
    
    def resume_all(self) -> None:
        """Reprend tous les sons du groupe"""
        for h in self._handles:
            h.resume()
    
    def pause_all(self) -> None:
        """Met en pause tous les sons du groupe"""
        for h in self._handles:
            h.pause()
    
    def stop_all(self) -> None:
        """Arrête tous les sons du groupe"""
        for h in self._handles:
            h.stop()
        self._handles.clear()

    def _get_free_handle(self, sound: Sound, source: _media.StaticSource) -> SoundHandle | None:
        """Renvoie un cannal libre si possible

        Args:
            sound: son à jouer
            source: source statique du son
        """
        self._handles = {h for h in self._handles if h.is_active()}
        if self._pool_max is not None and len(self._handles) >= self._pool_max:
            return None
        handle = SoundHandle(sound, source, _media.Player())
        self._handles.add(handle)
        return handle

# ======================================== REQUESTS ========================================
@dataclass(slots=True)
class _CrossfadeRequest(Request):
    handle_out: MusicHandle | None
    handle_in: MusicHandle | None
    steps: int
    step_dt: float
    step: int
    elapsed: float
    vol_out: float
    vol_in: float
    easing: EasingFunc

@dataclass(slots=True)
class _PlaylistRequest(Request):
    playlist: Playlist
    musics: list[Music]
    order: list[int]
    shuffle: bool
    loop: bool
    fade_in: float
    fade_out: float
    delay: float
    cross_fade: float
    playing: bool = True
    index: int = 0
    delay_timer: float = 0.0

# ======================================== MANAGER ========================================
class AudioManager(Manager):
    """Gestionnaire audio"""
    __slots__ = (
        "_master_volume", "_music_volume",
        "_active_sounds", "_current_music", "_crossfade", "_playlist",
        "_source_cache",
    )

    _ID: str = "audio"

    # Types alias
    AudioState: ClassVar[Type[AudioState]] = AudioState
    SoundGroup: ClassVar[Type[SoundGroup]] = SoundGroup
    SoundHandle: ClassVar[Type[SoundHandle]] = SoundHandle
    MusicHandle: ClassVar[Type[MusicHandle]] = MusicHandle

    # Groupes par défaut
    _DEFAULT_SOUN_GROUP: SoundGroup = None

    @classmethod
    def get_default_sound_group(cls) -> SoundGroup:
        """Renvoie le groupe de sons par défaut"""
        if cls._DEFAULT_SOUN_GROUP is None:
            cls._DEFAULT_SOUN_GROUP = SoundGroup()
        return cls._DEFAULT_SOUN_GROUP

    def __init__(self, context_manager: ContextManager):
        # Initialisation du gestionnaire
        super().__init__(context_manager)

        # Attributs publiques
        self._master_volume: float = 1.0
        self._music_volume: float = 1.0

        # Attributs privés
        self._active_sounds: set[Sound] = set()
        self._current_music: Music | None = None
        self._crossfade: _CrossfadeRequest | None = None
        self._playlist: _PlaylistRequest | None = None
        self._source_cache: dict[str, _media.StaticSource] = {}

    # ======================================== PROPERTIES ========================================
    @property
    def master_volume(self) -> float:
        """Volume général
        
        Le volume doit être un ``Réel`` positif.
        """
        return self._master_volume

    @master_volume.setter
    def master_volume(self, value: float) -> None:
        value = float(value)
        assert value >= 0.0, f"master_volume ({value}) must be positive"
        self._master_volume = value
        self._refresh_volumes()

    @property
    def music_volume(self) -> float:
        """Volume musical
        
        Le volume doit être un ``Réel`` positif non nul.
        """
        return self._music_volume

    @music_volume.setter
    def music_volume(self, value: float) -> None:
        value = float(value)
        assert value >= 0.0, f"music_volume ({value}) must be positive"
        self._music_volume = value
        self._refresh_volumes()

    # ======================================== FACTORY ========================================
    @staticmethod
    def create_sound(
            path: str,
            volume: Real = 1.0,
            cooldown: Real = 0.0,
            group: SoundGroup = None,
        ) -> Sound:
        """Crée et retourne un ``Sound`` asset

        Args:
            path: chemin vers le fichier audio
            volume: volume propre [0, 1]
            cooldown: délai minimal entre deux lectures (secondes)
            group: groupe SFX
        """
        return Sound(
            path = path,
            volume=volume,
            cooldown=cooldown,
            group=group
        )
    
    @staticmethod
    def create_sound_with_variations(
        folder_path: str,
        prefix: str = "",
        extensions: list[str] | None = None,
        volume: Real = 1.0,
        cooldown: Real = 0.0,
        group: SoundGroup |  None = None
    ):
        """"""
        return Sound.from_variations(
            folder_path = folder_path,
            prefix = prefix,
            extensions = extensions,
            volume = volume,
            cooldown = cooldown,
            group = group,
        )  

    @staticmethod
    def create_music(
        path: str,
        volume: Real = 1.0,
    ) -> Music:
        """Crée et retourne un ``Music``asset

        Args:
            path: chemin vers le fichier audio
            volume: volume propre [0, 1]
        """
        return Music(
            path = path,
            volume=volume,
        )

    @staticmethod
    def load_sounds(
        folder_path: str,
        prefix: str = "",
        extensions: list[str] = None,
        remove_prefix: bool = False,
        volume: Real = 1.0,
        cooldown: Real = 0.0,
        group: SoundGroup = None,
    ) -> SoundBundle:
        """Charge un ensemble de sons

        Args:
            folder_path: chemin du dossier
            prefix: préfixe des fichiers à charger
            extensions: extensions acceptées (toutes si None)
            remove_prefix: retirer le préfixe au chargement            
            volume: volume appliqué à tous les sons
            cooldown: cooldown appliqué à tous les sons
            group: groupe SFX à assigner
        """
        return SoundBundle.from_folder(
            folder_path = folder_path,
            prefix = prefix,
            extensions = extensions,
            remove_prefix = remove_prefix,
            volume = volume,
            cooldown = cooldown,
            group = group,
        )
    
    @staticmethod
    def load_musics(
        folder_path: str,
        prefix: str = "",
        extensions: list[str] = None,
        remove_prefix: bool = False,
        volume: Real = 1.0,
    ) -> MusicBundle:
        """Charge un ensemble de musiques

        Args:
            folder_path: chemin du dossier
            prefix: préfixe des fichiers à charger
            extensions: extensions acceptées (toutes si None)
            remove_prefix: retirer le préfixe au chargement            
            volume: volume appliqué à toutes les musiques
        """
        return MusicBundle.from_folder(
            folder_path = folder_path,
            prefix = prefix,
            extensions = extensions,
            remove_prefix = remove_prefix,
            volume = volume,
        )
    
    # ======================================== INTERFACE ========================================
    def clear(self) -> None:
        """Nettoyage complet"""
        self.stop_sounds()
        self._stop_music_immediate()

    # ======================================== SOUNDS ========================================
    def play_sound(
            self,
            sound: Sound,
            volume: Real = 1.0,
            loop: bool = False,
            limit: int | None = None,
            on_end: Callable[[SoundHandle], Any] = None
        ) -> SoundHandle | None:
        """Joue un ``Sound`` asset

        Args:
            sound: son à jouer
            volume: volume ponctuel
            loop: active le loop
            limit: limite de répétitions
            on_end: callback de fin de son

        Returns:
            handle: handle du son joué, ou None si le son n'a pas pu être joué
        """
        # Vérification de la disponibilité du son
        if not sound.is_ready() or sound.is_paused():
            return None

        # Récupération d'un player
        path = random.choice(sound._paths)
        source = self._load_source(path)
        group = sound._group or self.get_default_sound_group()
        handle = group._get_free_handle(sound, source)
        if handle is None:
            return None
        handle.on_stop = on_end

        # Lecture du son
        handle.loop = loop
        handle.iterations_left = limit
        handle.player.queue(source)
        handle.player.play()

        # Calcul du volume
        group_vol = group.get_absolute_volume() if group is not None else 1.0
        handle.set_volumes(self._master_volume * group_vol * sound.volume, volume)

        # Actualisation de l'état du son
        sound._add_handle(handle)
        sound._set_state(self.AudioState.PLAYING)
        sound._apply_cooldown()
        self._active_sounds.add(sound)
        return handle

    def resume_sound(self, sound: Sound) -> None:
        """Reprend un ``Sound`` asset

        Args:
            sound: son à reprendre
        """
        if not sound.is_paused():
            return
        for handle in sound._get_handles():
            handle.resume()
        sound._set_state(AudioState.PLAYING)

    def pause_sound(self, sound: Sound) -> None:
        """Met en ``Sound`` asset en pause

        Args:
            sound: son à mettre en pause
        """
        if not sound.is_playing() or sound.is_paused():
            return
        for handle in sound._get_handles():
            handle.pause()
        sound._set_state(AudioState.PAUSED)

    def stop_sound(self, sound: Sound) -> None:
        """Arrête un ``Sound`` asset

        Args:
            sound: son à arrêter
        """
        if not sound.is_playing():
            return
        for handle in list(sound._get_handles()):
            handle.stop()

    # ======================================== GROUPS ========================================
    def resume_sounds(self, group: SoundGroup = None) -> None:
        """Reprend les SFX en cours

        Args:
            group: si fourni, reprend uniquement ce groupe
        """
        for sound in list(self._active_sounds):
            if group is None or sound._group is group:
                self.resume_sound(sound)

    def pause_sounds(self, group: SoundGroup = None) -> None:
        """Met en pause les SFX en cours

        Args:
            group: si fourni, met en pause uniquement ce groupe
        """
        for sound in list(self._active_sounds):
            if group is None or sound._group is group:
                self.pause_sound(sound)

    def stop_sounds(self, group: SoundGroup = None) -> None:
        """Arrête les SFX en cours.

        Args:
            group: si fourni, arrête uniquement ce groupe
        """
        for sound in list(self._active_sounds):
            if group is None or sound._group is group:
                self.stop_sound(sound)
    
    @property
    def active_sounds(self) -> frozenset[Sound]:
        """Renvoie l'ensemble des sons en cours de lecture (lecture seule)"""
        return self._active_sounds

    # ======================================== MUSICS ========================================
    def play_music(
            self,
            music: Music,
            volume: Real = 1.0,
            loop: bool = True,
            fade_s: float = 0.0,
            fade_easing: EasingFunc = linear,
            on_end: Callable[[MusicHandle], Any] = None,
            playlist_fallback: bool = True,
            _interrupt_playlist: bool = True,
        ) -> MusicHandle:
        """Joue un ``Music`` asset en remplaçant l'éventuel en cours.

        Args:
            music: musique à jouer
            volume: volume ponctuel
            loop: boucle si True
            fade_s: fade-in en secondes
            fade_easing: fonction d'atténuation du fade-in
            on_end: callback de fin de lecture
            playlist_fallback: relancer la playliste en cours après la musique
        """
        # Arrêt de la musique en cours
        self._stop_music_immediate()

        # Arrêt de la playlist en cours
        if self._playlist is not None and _interrupt_playlist:
            self._playlist.playing = False

        # Génération du handle
        source = music._source or _media.load(music.path, streaming=True)
        player = _media.Player()
        player.loop = loop
        player.queue(source)
        handle = MusicHandle(music, source, player, on_stop=self._make_on_stop(music, on_end=on_end, playlist_fallback=playlist_fallback))

        # Lecture de la musique
        handle.player.play()
        handle.set_volumes(self._master_volume * self._music_volume * music.volume, 0.0)
        music._set_handle(handle)
        music._set_loop(loop)
        music._set_state(AudioState.PLAYING)
        self._current_music = music

        # Cas avec fade-in
        if fade_s > 0.0:
            handle.player.volume = 0.0
            self._crossfade = _CrossfadeRequest(
                handle_out=None,
                handle_in=handle,
                steps=_CROSSFADE_STEPS,
                step_dt=fade_s / _CROSSFADE_STEPS,
                step=0,
                elapsed=0.0,
                vol_out=0.0,
                vol_in=volume,
                easing=fade_easing,
            )

        # Cas sans fade-in
        else:
            handle.player.volume = self._master_volume * self._music_volume * music.volume * volume
        
        return handle

    def resume_music(self) -> None:
        """Reprend la musique en cours"""
        if self._current_music is None or not self._current_music.is_paused():
            return
        self._current_music._handle.resume()
    
    def pause_music(self) -> None:
        """Met en pause la musique en cours"""
        if self._current_music is None or not self._current_music.is_playing():
            return
        self._current_music._handle.pause()

    def stop_music(self, fade_s: float = 0.0, fade_easing: EasingFunc = linear) -> None:
        """Arrête la musique en cours

        Args:
            fade_s: fade-out en secondes
            fade_easing: fonction d'atténuation du fade-out
        """
        # Annulation du cross-fade en cours
        if self._current_music is None:
            return
        self._cancel_crossfade()

        # Cas avec fade-out
        if fade_s > 0.0:            
            self._crossfade = _CrossfadeRequest(
                handle_out=self._current_music._handle if self._current_music else None,
                handle_in=None,
                steps=_CROSSFADE_STEPS,
                step_dt=fade_s / _CROSSFADE_STEPS,
                step=0,
                elapsed=0.0,
                vol_out=self._current_music._handle.play_volume,
                vol_in=0.0,
                easing=fade_easing,
            )
            self._current_music = None
        
        # Cas sans Fade-out
        else:
            self._stop_music_immediate()

    def switch_music(
            self,
            music: Music,
            volume: Real = 1.0,
            loop: bool = True,
            fade_s: float = 1.0,
            fade_easing: EasingFunc = linear,
            on_end: Callable[[MusicHandle], Any] = None,
            playlist_fallback: bool = True,
            _interrupt_playlist: bool = True,
        ) -> MusicHandle:
        """Crossfade vers une nouvelle musique

        Args:
            music: musique cible
            fade_s: durée totale du crossfade en secondes
            fade_easing: fonction d'atténuation du cross-fade
            loop: boucle la nouvelle musique
            playlist_fallback: relancer la playliste en cours après la musique
        """
        # Cas sans cross-fade
        if fade_s <= 0.0:
            return self.play_music(music, loop=loop)
        
        # Arrêt de la playlist en cours
        if self._playlist is not None and _interrupt_playlist:
            self._playlist.playing = False

        # Annulation du cross-fade en cours et récupération de la musique sortante
        self._cancel_crossfade()
        music_out = self._current_music

        # Génération du handle
        if music == music_out:
            source = _media.load(music.path, streaming=True)
        else:
            source = music._source or _media.load(music.path, streaming=True)
        player = _media.Player()
        player.loop = loop
        player.queue(source)
        handle = MusicHandle(music, source, player, on_stop=self._make_on_stop(music, on_end=on_end, playlist_fallback=playlist_fallback))

        # Création du cross-fade
        self._crossfade = _CrossfadeRequest(
            handle_out=music_out._handle if music_out is not None else None,
            handle_in=handle,
            steps=_CROSSFADE_STEPS,
            step_dt=fade_s / _CROSSFADE_STEPS,
            step=0,
            elapsed=0.0,
            vol_out=music_out._handle.play_volume if music_out else 0.0,
            vol_in=volume,
            easing=fade_easing,
        )

        # Lecture de la musique
        handle.set_volumes(self._master_volume * self._music_volume * music.volume, 0.0)
        handle.player.play()
        music._set_handle(handle)
        music._loop = loop
        music._set_state(AudioState.PLAYING)
        self._current_music = music

        return handle

    @property
    def current_music(self) -> Music:
        """Renvoie le musique en cours"""
        return self._current_music
    
    # ======================================== PLAYLISTS ========================================
    def play_playlist(self, playlist: Playlist) -> None:
        """Lance la lecture d'une playlist
        
        Args:
            playlist: playlist à jouer
        """
        if __debug__:
            expect(playlist, Playlist)
        self._playlist = _PlaylistRequest(
            playlist = playlist,
            musics = list(playlist.musics),
            order = list(playlist.order),
            shuffle = playlist.shuffle,
            loop = playlist.loop,
            fade_in = playlist.fade_in,
            fade_out = playlist.fade_out,
            delay = playlist.delay,
            cross_fade = playlist.cross_fade,
        )
        self._play_playlist_next()

    def resume_playlist(self) -> None:
        """Reprend la playlist en cours"""
        if self._playlist is None or self._playlist.playing:
            return
        self._playlist.playing = True
        self.resume_music()

    def pause_playlist(self) -> None:
        """Met la playlist en cours en pause"""
        if self._playlist is None or not self._playlist.playing:
            return
        self._playlist.playing = False
        self.pause_music()

    def stop_playlist(self, fade_s: Real = 0.0) -> None:
        """Arrête la playlist en cours
        
        Args:
            fade_s: fade-out *(en secondes)*
        """
        if self._playlist is None:
            return
        self._playlist = None
        self.stop_music(fade_s=fade_s)

    @property
    def current_playlist(self) -> Playlist:
        """Renvoie la playlist en cours"""
        if self._playlist is None:
            return None
        return self._playlist.playlist
    
    @property
    def playlist_index(self) -> int:
        """Renvoie l'indice de lecture de la playlist en cours"""
        if self._playlist is None:
            return 0
        return self._playlist.index
    
    @property
    def playlist_playing(self) -> bool:
        """Vérifie que la playliste courant soit en cours de lecture"""
        if self._playlist is None:
            return False
        return self._playlist.playing

    # ======================================== CYCLE DE VIE ========================================
    def update(self, dt: float) -> None:
        """Actualisation
        
        Args:
            dt: delta-time
        """
        # Mise à jour des cooldowns
        self._update_sounds(dt)

        # Gestion de la playlist
        self._update_playlist(dt)

        # Fade musical
        self._update_fade(dt)

    def _update_sounds(self, dt: float) -> None:
        """Actualisation des sons actifs

        Args:
            dt: delta-time
        """
        done: set[Sound] = set()
        for sound in self._active_sounds:
            if sound.is_paused():
                continue
            if sound._tick(dt) and not sound.is_playing():
                done.add(sound)
        self._active_sounds -= done

    def _update_playlist(self, dt: float) -> None:
        """Actualisation de la playlist en cours
        
        Args:
            dt: delta-time
        """
        if not self.playlist_playing:
            return
        pr = self._playlist

        # Délai en cours
        if pr.delay_timer > 0.0:
            pr.delay_timer -= dt
            if pr.delay_timer <= 0.0:
                pr.delay_timer = 0.0
                self._play_playlist_next()
            return

        # Crossfade anticipé
        if pr.cross_fade > 0.0 and pr.delay == 0.0 and self._current_music is not None:
            handle = self._current_music._handle
            if handle is not None and self._crossfade is None:
                remaining = handle.time_remaining
                if remaining is not None and remaining <= pr.cross_fade:
                    self._play_playlist_next()

    def _update_fade(self, dt: float) -> None:
        """Actualisation du fondu
        
        Args:
            dt: delta-time
        """
        if self._crossfade is None:
            return
        cf = self._crossfade
        cf.elapsed += dt
    
        while cf.elapsed >= cf.step_dt and cf.step < cf.steps:
            cf.step += 1
            cf.elapsed -= cf.step_dt
            t = max(0.0, min(cf.easing(cf.step / cf.steps), 1.0))
            if cf.handle_out is not None:
                cf.handle_out.play_volume = cf.vol_out * (1.0 - t)
            if cf.handle_in is not None:
                cf.handle_in.play_volume = cf.vol_in * t

        if cf.step >= cf.steps:
            if cf.handle_out is not None:
                if cf.handle_in is not None and cf.handle_in.music == cf.handle_out.music:
                    cf.handle_out.delete()
                else:
                    cf.handle_out.stop()
            if cf.handle_in is not None:
                cf.handle_in.play_volume = cf.vol_in
            self._crossfade = None

    def flush(self) -> None:
        """Nettoyage"""
        pass

    # ======================================== INTERNALS ========================================
    def _load_source(self, path: str) -> _media.StaticSource:
        """Charge une source audio en cacheant les résultats
        
        Args
            path: chemin vers le fichier audio
        """
        if path not in self._source_cache:
            self._source_cache[path] = _media.load(path, streaming=False)
        return self._source_cache[path]

    def _stop_music_immediate(self) -> None:
        """Arrête la musique brutalement"""
        self._cancel_crossfade()
        if self._current_music is not None:
            if self._current_music._handle is not None:
                self._current_music._handle.stop()
            self._current_music = None

    def _clear_current_music(self, music: Music) -> None:
        """Nettoie la musique courante si elle correspond à la musique donnée
        
        Args:
            music: musique à tester
        """
        if self._current_music is music:
            self._current_music = None

    def _on_interrupted_music_end(self, handle: MusicHandle) -> None:
        """Reprend la playlist après une musique de surcharge
        
        Args:
            handle: token de lecture
        """
        if self._playlist is not None and not self._playlist.playing:
            self._playlist.playing = True
            self._playlist.delay_timer = 0.0
            self._play_playlist_next()

    def _make_on_stop(self, music: Music, on_end: Callable[[MusicHandle], Any], playlist_fallback: bool) -> Callable:
        """Construit le callback on_stop en fusionnant la logique musique et playlist
        
        Args:
            music: musique concernée
            on_end: callback de fin de lecture
            playlist_fallback: reprise de la playlist à la fin de lecture
        """
        def on_stop(h: MusicHandle) -> None:
            self._clear_current_music(music)
            if on_end is not None:
                on_end(h)
            if playlist_fallback and self._playlist is not None and not self._playlist.playing:
                self._on_interrupted_music_end(h)
        return on_stop

    def _cancel_crossfade(self) -> None:
        """Annule le cross-fade"""
        self._crossfade = None

    def _refresh_volumes(self) -> None:
        """Actualise les volumes"""
        base_musics_volume = self.master_volume * self.music_volume
        if self._crossfade is not None:
            cf = self._crossfade
            if cf.handle_out is not None:
                cf.handle_out.base_volume = base_musics_volume * cf.handle_in.music.volume
            if cf.handle_in is not None:
                cf.handle_in.base_volume = base_musics_volume * cf.handle_in.music.volume
        elif self._current_music is not None:
            self._current_music._handle.base_volume = base_musics_volume * self._current_music.volume

    def _play_playlist_next(self) -> None:
        """Joue la prochaine musique de la playlist en cours"""
        pr = self._playlist
        if pr.index >= len(pr.order):
            if pr.loop:
                if pr.shuffle:
                    random.shuffle(pr.order)
                pr.index = 0
            else:
                self.stop_playlist(fade_s=pr.fade_out)
                return
        next_music = pr.musics[pr.order[pr.index]]
        if pr.index == 0:
            self.play_music(next_music, fade_s=pr.fade_in, loop=False, _interrupt_playlist=False)
        else:
            self.switch_music(next_music, fade_s=pr.cross_fade, loop=False, _interrupt_playlist=False)
        pr.index += 1

        # Armer le délai pour la piste suivante
        pr.delay_timer = pr.delay

# ======================================== EXPORTS ========================================
__all__ = [
    "SoundHandle",
    "MusicHandle",

    "SoundGroup",

    "AudioManager",
]