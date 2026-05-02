# ======================================== IMPORTS ========================================
from .._internal import expect
from .._flag import StackMode, SceneState
from .._rendering import Pipeline

from ._world_layer import WorldLayer
from ._tile_layer import TileLayer
from ._gui_layer import GuiLayer
from ._light_layer import LightLayer
from ._scene import Scene

# ======================================== STATE ========================================
_stack: list[Scene] = []
_update_states: tuple[SceneState, ...] = (SceneState.RUNNING, SceneState.HIDDEN)
_draw_states: tuple[SceneState, ...] = (SceneState.RUNNING, SceneState.PAUSED)

# ======================================== GETTERS ========================================
def get_current() -> Scene | None:
    """Renvoie la scene active"""
    return _stack[-1] if _stack else None

# ======================================== TRANSITIONS ========================================
def load(scene: Scene):
    """Remplace toute la stack par une scene"""
    _stop_all()
    _stack.clear()
    _stack.append(expect(scene, Scene))
    scene._set_state(SceneState.RUNNING)
    scene.on_start()

def switch(scene: Scene):
    """Remplace la scene active par une autre"""
    if _stack:
        top = _stack[-1]
        top._set_state(SceneState.SLEEPING)
        top.on_stop()
        _stack.pop()
    _stack.append(expect(scene, Scene))
    scene._set_state(SceneState.RUNNING)
    scene.on_start()

def push(scene: Scene):
    """Empile une scene par dessus la scene active"""
    if _stack and scene.stack_mode is not StackMode.OVERLAY:
        top = _stack[-1]
        if scene.stack_mode is StackMode.PAUSE: top._set_state(SceneState.PAUSED)
        elif scene.stack_mode is StackMode.HIDE: top._set_state(SceneState.HIDDEN)
        else:
            top._set_state(SceneState.SLEEPING)
            top.on_stop()
    _stack.append(expect(scene, Scene))
    scene._set_state(SceneState.RUNNING)
    scene.on_start()

def pop():
    """Dépile la scene active et reprend la précédente"""
    if _stack:
        top = _stack[-1]
        top._set_state(SceneState.SLEEPING)
        top.on_stop()
        _stack.pop()
        if _stack:
            new_top = _stack[-1]
            new_top._set_state(SceneState.RUNNING)
            new_top.on_start()
        return top

# ======================================== LIFE CYCLE ========================================
def _preload(pipeline: Pipeline) -> None:
    """Préchargement"""
    for scene in _stack:
        scene._preload(pipeline)

def update(dt: float):
    """Actualisation des scènes"""
    for scene in reversed(_stack):
        if scene.state in _update_states:
            scene.update(dt)

def draw(pipeline: Pipeline):
    """Affichage des scènes"""
    for scene in _stack:
        if scene.state in _draw_states:
            scene.draw(pipeline)

# ======================================== INTERNALS ========================================
def _stop_all():
    for scene in _stack:
        scene._set_state(SceneState.SLEEPING)
        scene.on_stop()

# ======================================== EXPORTS ========================================
__all__ = [
    "StackMode",
    "SceneState",

    "WorldLayer",
    "TileLayer",
    "GuiLayer",
    "LightLayer",
    "Scene",

    "get_current",
    "load",
    "switch",
    "push",
    "pop",
    "update",
    "draw"
]