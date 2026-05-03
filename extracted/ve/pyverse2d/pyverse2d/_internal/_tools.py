# ======================================== IMPORTS ========================================
from __future__ import annotations
from typing import Callable
import time

# ======================================== PROCESSOR ========================================
class Processor:
    """Exécute une séquence de fonctions sur un contexte

    Args:
        name: nom de la pipeline pour le debug
    """
    __slots__ = ("_name", "_steps")

    def __init__(self, name: str = ""):
        self._name: str = name
        self._steps: list[Callable] = []

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        return f"Pipeline(name={self._name!r}, steps={[s.__name__ for s in self._steps]})"

    def __len__(self) -> int:
        return len(self._steps)

    # ======================================== DECORATEUR ========================================
    def step(self, fn: Callable) -> Callable:
        """
        Enregistre une fonction comme étape de la pipeline

        Args:
            fn(callable): fonction à enregistrer, prend un contexte en argument
        """
        self._steps.append(fn)
        return fn

    # ======================================== EXECUTION ========================================
    def run(self, ctx) -> None:
        """
        Exécute toutes les étapes séquentiellement sur le contexte

        Args:
            ctx: contexte partagé entre les étapes
        """
        for step in self._steps:
            if step(ctx) is False:
                return
            
    def __call__(self, ctx) -> None:
        """
        Exécute toutes les étapes séquentiellement sur le contexte

        Args:
            ctx: contexte partagé entre les étapes
        """
        self.run(ctx)
    
    # ======================================== DEBUGGING ========================================
    def profile(self, ctx) -> None:
        """Exécute les étapes avec timing"""
        for step in self._steps:
            t = time.perf_counter()
            result = step(ctx)
            print(f"{step.__name__}: {(time.perf_counter() - t) * 1000:.3f}ms")
            if result is False:
                return

# ======================================== CALLBACK LIST ========================================
class CallbackList:
    """Stockage des hooks
    
    Cette objet est un ``Callable`` permettant de stocker des fonctions à appeler.
    """
    __slots__ = ("_callbacks",)

    def __init__(self):
        self._callbacks: list[Callable] = []

    # ======================================== INTERFACE ========================================
    def copy(self) -> CallbackList:
        """Renvoie une copie du CallbackList"""
        new = CallbackList()
        new._inject(self._exctract())
        return new

    def __call__(self, callback: Callable, once: bool = False) -> Callable:
        """Ajoute une fonction
        
        Args:
            callback: fonction à ajouter
            once: supprime la fonction après le premier appel

        Returns:
            token: fonction de suppression automatique du callback
        """
        if once:
            token_holder = [None]
            def _once(*args, **kwargs):
                token_holder[0]()
                callback(*args, **kwargs)
            token_holder[0] = self._make_delete_token(_once)
            self._callbacks.append(_once)
            return token_holder[0]
        
        self._callbacks.append(callback)
        return self._make_delete_token(callback)
    
    def remove(self, callback: Callable) -> Callable:
        """Supprime une fonction
        
        Args:
            callback: fonction à supprimer

        Returns:
            callback: fonction supprimée
        """
        self._callbacks.remove(callback)

    def trigger(self, *args, **kwargs) -> None:
        """Appelle les fonctions"""
        for func in self._callbacks:
            func(*args, **kwargs)

    def __len__(self) -> int:
        """Renvoie le nombre de callbacks assignés"""
        return len(self._callbacks)
    
    # ======================================== INTERNALS ========================================
    def _inject(self, callbacks: list[Callable]) -> None:
        """Injecte une liste de callbacks"""
        self._callbacks += callbacks

    def _exctract(self) -> list[Callable]:
        """Extrait les callbacks"""
        return self._callbacks
    
    def _make_delete_token(self, func: Callable) -> Callable[[], None]:
        """Génère un token de suppression"""
        def delete() -> None:
            self._callbacks.remove(func)
        return delete

# ======================================== EXPORTS ========================================
__all__ = [
    "Processor",
    "CallbackList",
]