# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import System

from .._world import World
from .._component import Animator, SpriteRenderer

from typing import TypeAlias
from dataclasses import dataclass

# ======================================== Alias ========================================
AnimationRequest: TypeAlias = dataclass

# ======================================== SYSTEM ========================================
class AnimationSystem(System):
    """Met à jour les animations de toutes les entités"""
    __slots__ = ()
    order = 90
    exclusive = True

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du système"""
        return f"AnimationSystem()"

    # ======================================== LIFE CYCLE ========================================
    def update(self, world: World, dt: float) -> None:
        """Mise à jour des animations

        Args:
            world(World): monde à mettre à jour
            dt(float): delta time
        """
        for entity in world.query(Animator):
            animator: Animator = entity.get(Animator)
            sr: SpriteRenderer = entity.get(SpriteRenderer)
            self._update_animator(animator, sr, dt)

    # ======================================== INTERNALS ========================================
    def _update_animator(self, animator: Animator, sr: SpriteRenderer, dt: float) -> None:
        """Mise à jour d'un composant animateur"""
        target_req = self._resolve(animator)
        target_anim = target_req.animation if target_req else animator.idle

        # Changement d'animation
        if target_anim is not animator._current_animation:
            animator._current_request = target_req
            animator._current_animation = target_anim
            animator._frame = 0
            animator._elapsed = 0.0
            if target_req and target_req.on_start:
                target_req.on_start()

        # Aucune animation à jouer
        if animator._current_animation is None:
            sr.set_to_default()
            return

        # Pousse la frame courante dans le SpriteRenderer
        sr.image = animator.current_frame

        # Avance la frame
        animator._elapsed += dt
        delay = 1.0 / animator._current_animation.framerate
        if animator._elapsed >= delay:
            animator._elapsed -= delay
            animator._frame += 1

            # Fin d'animation
            if animator._frame >= len(animator._current_animation.frames):
                req = animator._current_request

                if req and req.on_end:
                    req.on_end()

                if req and req.loop:
                    animator._frame = 0
                else:
                    animator._current_animation = animator.idle
                    animator._current_request = None
                    animator._frame = 0
                    animator._elapsed = 0.0

    def _resolve(self, animator: Animator) -> AnimationRequest | None:
        """Résout la requête active selon les priorités et conditions"""
        best: AnimationRequest | None = None
        for req in animator._requests:
            if req.condition is None or req.condition():
                if best is None or req.priority >= best.priority:
                    best = req

        # Nettoyage des requêtes cutable qui ont perdu la main
        to_remove = []
        for req in animator._requests:
            if req.cutable and req is not best:
                if req.loop:
                    animator._frame = 0
                    animator._elapsed = 0.0
                else:
                    to_remove.append(req)

        for req in to_remove:
            animator._requests.remove(req)

        return best