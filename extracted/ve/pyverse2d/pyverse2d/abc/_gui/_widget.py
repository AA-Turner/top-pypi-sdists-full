# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, clamped, over, CallbackList
from ...math import Point
from ..._core import Transform, Geometry

from .._shape import Shape

from ._behavior import Behavior

import pyglet.gl as gl
from pyglet.graphics import Group

from abc import ABC, abstractmethod
from bisect import insort
from numbers import Real
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from ..._rendering import Pipeline
    from ...scene import GuiLayer
    from ...gui import (
        RenderContext,
        ClickBehavior,
        HoverBehavior,
        SelectBehavior,
        FocusBehavior,
    )

# ======================================== GROUP ========================================
class WidgetGroup(Group):
    """Groupe spécialisé des widgets"""
    _cache: dict[tuple, WidgetGroup] = {}

    def __init__(self, order=0, parent=None, scissor=None):
        super().__init__(order=order, parent=parent)
        self.scissor = scissor
        self.resolved = (
            intersect(parent.resolved, scissor) if scissor and isinstance(parent, WidgetGroup) and parent.resolved
            else scissor if scissor
            else parent.resolved if isinstance(parent, WidgetGroup)
            else None
        )

    def __hash__(self) -> int:
        """Renvoie le hash du groupe"""
        return hash((self.order, self.parent, self.resolved))

    def __eq__(self, other: WidgetGroup) -> bool:
        """Vérifie la correspondance de deux groupes"""
        return super().__eq__(other) and self.resolved == other.resolved

    def set_state(self):
        """Active l'état OpenGl"""
        if self.resolved is not None:
            gl.glEnable(gl.GL_SCISSOR_TEST)
            gl.glScissor(*self.resolved)

    def unset_state(self):
        """Désactive l'état OpenGl"""
        if self.resolved is not None:
            gl.glDisable(gl.GL_SCISSOR_TEST)

    @classmethod
    def get_group(cls, order: int, parent: WidgetGroup | None, scissor: tuple | None) -> WidgetGroup:
        """Renvoie un groupe correspondant
        
        Args:
            order: ordre de priorité
            parent: groupe parent
            scissor: rect de clipping
        """
        key = (order, id(parent), scissor)
        if key not in cls._cache:
            cls._cache[key] = cls(order=order, parent=parent, scissor=scissor)
        return cls._cache[key]

    @classmethod
    def invalidate(cls, parent_id: int) -> None:
        """Invalide le scissor du groupe et de ses enfants"""
        cls._cache = {k: v for k, v in cls._cache.items() if k[1] != parent_id}

# ======================================== ABSTRACT CLASS ========================================
class Widget(ABC):
    """Classe abstraite des composants UI

    Args:
        position: position
        anchor: ancre locale
        scale: facteur de redimensionnement
        rotation: angle de rotation
        opacity: opacité
    """
    __slots__ = (
        "_layer", "_parent", "_children",
        "_transform", "_world_transform", "_geometry",
        "_opacity", "_active", "_visible", "_clipping",
        "_on_activate", "_on_deactivate", "_on_show", "_on_hide",
        "_attr_locks", "_behaviors", "_click", "_hover", "_select", "_focus",
        "_cached_scissor", "_scissor_dirty",
        "_context",
    )

    _RENDER_CONTEXT_CLS: RenderContext = None

    @classmethod
    def _get_render_context(cls) -> RenderContext:
        """Renvoie la class ``RenderContext``"""
        if cls._RENDER_CONTEXT_CLS is None:
            from ...gui import RenderContext
            cls._RENDER_CONTEXT_CLS = RenderContext
        return cls._RENDER_CONTEXT_CLS

    def __init__(
            self,
            position: Point = (0, 0),
            anchor: Point = (0.5, 0.5),
            scale: Real = 1.0,
            rotation: Real = 0.0,
            opacity: float = 1.0,
            clipping: bool = False,
        ):
        # Transtyping
        transform: Transform = Transform(position, anchor, rotation, scale)
        opacity = float(opacity)

        if __debug__:
            clamped(opacity)
            expect(clipping, bool)

        # Attributs publique
        self._transform: Transform = transform
        self._world_transform: Transform = self._transform.copy()
        self._geometry: Geometry = Geometry(self.hitbox, self._world_transform)
        self._opacity: float = opacity
        self._clipping: bool = clipping
            
        # Arbre
        self._layer: GuiLayer = None
        self._parent: Widget = None
        self._children: list[WidgetWrapper] = []

        # Etat
        self._active: bool = True
        self._visible: bool = True

        # Hooks
        self._on_activate: CallbackList = None
        self._on_deactivate: CallbackList = None
        self._on_show: CallbackList = None
        self._on_hide: CallbackList = None

        # Behaviors
        self._attr_locks: dict[str, int] = {}
        self._behaviors: list[str] = []
        self._click: ClickBehavior = None
        self._hover: HoverBehavior = None
        self._select: SelectBehavior = None
        self._focus: FocusBehavior = None

        # Scissor test
        self._cached_scissor: tuple | None = None
        self._scissor_dirty: bool = True

        # Contexte courant
        self._context: RenderContext = self._get_render_context()(
            pipeline = None,
            x = self._transform.x,
            y = self._transform.y,
            scale = self._transform.scale,
            rotation = self._transform.rotation,
            opacity = self._opacity,
            group = None,
            z = 0,
        )

    # ======================================== PROPERTIES ========================================
    @property
    def layer(self) -> GuiLayer | None:
        """``Layer`` gui maître"""
        return self._layer

    @property
    def parent(self) -> Widget| None:
        """``Widget`` parent"""
        return self._parent
    
    @property
    def root(self) -> Widget:
        """``Widget`` racine"""
        if self._parent is None:
            return self
        return self._parent.root

    @property
    def children(self) -> tuple[Widget]:
        """Liste des ``Widgets`` enfants"""
        return tuple(wrapper.widget for wrapper in self._children)
    
    @property
    def position(self) -> Point:
        """Position

        La position peut être un objet ``Point`` ou un tuple ``(x, y)``.
        """
        return self._transform.position
    
    @position.setter
    def position(self, value: Point) -> None:
        self._transform.position = value
        self._invalidate_scissor()
    
    @property
    def x(self) -> float:
        """Position horizontale

        La coordonnée doit être un ``Réel``.
        """
        return self._transform._position.x
    
    @x.setter
    def x(self, value: Real) -> None:
        self._transform.x = value
        self._invalidate_scissor()
    
    @property
    def y(self) -> float:
        """Position verticale
        
        La coordonnée doit être un ``Réel``.
        """
        return self._transform.y
    
    @y.setter
    def y(self, value: Real) -> None:
        self._transform.y = value
        self._invalidate_scissor()
    
    @property
    def absolute_position(self) -> Point:
        """Position absolue"""
        if self._parent is None:
            return self.position
        return self._parent.absolute_position + self.position
    
    @property
    def absolute_x(self) -> float:
        """Position horizontale absolue"""
        if self._parent is None:
            return self.position.x
        return self._parent.absolute_x + self.position.x
    
    @property
    def absolute_y(self) -> float:
        """Position verticale absolue"""
        if self._parent is None:
            return self.position.y
        return self._parent.absolute_y + self.position.y
    
    @property
    def anchor(self) -> Point:
        """Ancre relative locale

        L'ancre peut être un objet ``Point`` ou un tuple ``(ax, ay)``.
        Les coordonnées de l'ancre doivent être comprises dans l'intervalle [0, 1].
        """
        return self._transform.anchor
    
    @anchor.setter
    def anchor(self, value: Point) -> None:
        self._transform.anchor = value
        self._invalidate_scissor()
    
    @property
    def anchor_x(self) -> float:
        """Ancre horizontale relative locale

        La coordonnée doit être un réel compris dans l'invervalle [0, 1].
        """
        return self._transform.anchor_x
    
    @anchor_x.setter
    def anchor_x(self, value: Real) -> None:
        self._transform.anchor_x = value
        self._invalidate_scissor()
    
    @property
    def anchor_y(self) -> float:
        """Ancre verticale relative locale
        
        La coordonnée doit être un réel compris dans l'intervalle [0, 1].
        """
        return self._transform.anchor_y
    
    @anchor_y.setter
    def anchor_y(self, value: Real) -> None:
        self._transform.anchor_y = value
        self._invalidate_scissor()

    @property
    def scale(self) -> float:
        """Facteur de redimensionnement

        Ce facteur doit être un ``réel`` positif non nul
        """
        return self._transform.scale
    
    @scale.setter
    def scale(self, value: Real) -> None:
        self._transform.scale = value
        self._invalidate_scissor()

    @property
    def rotation(self) -> float:
        """Angle de rotation

        La rotation se fait *en degrés*, dans le sens trigonométrique *(CCW)*.
        """
        return self._transform.rotation

    @rotation.setter
    def rotation(self, value: Real) -> None:
        self._transform.rotation = value
        self._invalidate_scissor()
    
    @property
    def opacity(self) -> float:
        """Opacité relative

        L'opacité doit être un ``Réel`` compris dans l'invervalle [0, 1].
        """
        return self._opacity
    
    @opacity.setter
    def opacity(self, value: Real) -> None:
        value = float(value)
        assert 0.0 <= value <= 1.0, f"opacity ({value}) must be within 0.0 and 1.0"
        self._opacity: float = value

    @property
    def clipping(self) -> bool:
        """Limitation du rendu

        Lorsque cette propriété est activée, les widgets enfants sont rendus strictement dans la zone de ce widget.
        """
        return self._clipping
    
    @clipping.setter
    def clipping(self, value: bool) -> None:
        assert isinstance(value, bool), f"clipping ({value}) must be a boolean"
        if value != self._clipping:
            self._clipping = value
            self._invalidate_scissor()
    
    @property
    @abstractmethod
    def hitbox(self) -> Shape: ...

    # ======================================== PREDICATES ========================================
    def is_active(self) -> bool:
        """Vérifie l'activité"""
        return self._active
    
    def is_visible(self) -> bool:
        """Vérifie la visibilité"""
        return self._visible
    
    def collidespoint(self, point: Point) -> bool:
        """Vérifie la collision avec un point"""
        return self._geometry.world_contains(point)
    
    # ======================================== INTERFACE ========================================
    @abstractmethod
    def copy(self) -> Widget: ...

    def deepcopy(self) -> Widget:
        """Renvoie une copie profonde du ``Widget``"""
        copy = self.copy()
        self.give_hooks(copy)
        self.give_children(copy)
        self.give_behaviors(copy)

    def give_state(self, other: Widget) -> None:
        """Donne une copie de l'état du ``Widget``à un autre ``Widget``"""
        other._active = self._active
        other._visible = self._visible

    def give_hooks(self, other: Widget) -> None:
        """Donne une copie des hooks du ``Widget`` à un autre ``Widget``"""
        other._on_activate = self._on_activate.copy() if self._on_activate else None
        other._on_deactivate = self._on_deactivate.copy() if self._on_deactivate else None
        other._on_show = self._on_show.copy() if self._on_show else None
        other._on_hide = self._on_hide.copy() if self._on_hide else None

    def give_children(self, other: Widget) -> None:
        """Donne une copie des enfants du ``Widget`` à un autre ``Widget``"""
        other._children = [wrapper.copy() for wrapper in self._children]

    def give_behaviors(self, other: Widget) -> None:
        """Donne une copie des comportements du ``Widget`` à un autre ``Widget``"""
        for name in self._behaviors:
            behavior = getattr(self, name)
            id_ = name[1:]
            if other.has_behavior(id_):
                other.remove_behavior(id_)
            other.add_behavior(behavior)

    # ========================================  TRANSFORMATIONS ========================================
    def resize(self, factor: Real) -> None:
        """Redimensionne le widget par un facteur

        Le facteur de redimensionnement doit être un ``Réel`` positif non nul.
        """
        self._scale *= over(float(factor), 0.0, include=False)
        self._invalidate_scissor()

    def rotate(self, angle: Real) -> None:
        """Applique une rotation au widget

        La rotation est *en degrés* et se fait dans le sens trigonométrique *(CCW)*.
        """
        self._rotation += float(angle)
        self._invalidate_scissor()

    # ========================================  STATE ========================================
    def activate(self, propagate: bool = True) -> None:
        """Active le composant

        Args:
            propagate: propage l'état aux enfants
        """
        was_active = self._active
        self._active = True
        for behavior in self._behaviors:
            getattr(self, f"_{behavior}").enable()
        if not was_active and self._on_activate:
            self._on_activate.trigger()
        if propagate:
            for child in self._children:
                child.widget.activate()
    
    def deactivate(self, propagate: bool = True) -> None:
        """Désactive le composant

        Args:
            propagate: propage l'état aux enfants
        """
        was_active = self._active
        self._active = False
        for behavior in self._behaviors:
            getattr(self, f"_{behavior}").disable()
        self._attr_locks.clear()
        if was_active and self._on_deactivate:
            self._on_deactivate.trigger()
        if propagate:
            for child in self._children:
                child.widget.deactivate()
    
    def switch_activity(self, propagate: bool = True) -> None:
        """Bascule l'activité

        Args:
            propagate: propage l'état aux enfants
        """
        if self._active:
            self.deactivate(propagate=propagate)
        else:
            self.activate(propagate=propagate)

    def set_activity(self, value: bool, propagate: bool = True) -> None:
        """Fixe l'activité

        Args:
            value: nouvelle activité
        """
        if value:
            self.activate(propagate=propagate)
        else:
            self.deactivate(propagate=propagate)

    def show(self, propagate: bool = True) -> None:
        """Montre le composant

        Args:
            propagate: propage l'état aux enfants
        """
        was_visible = self._visible
        self._visible = True
        if not was_visible and self._on_show:
            self._on_show.trigger()
        if propagate:
            for child in self._children:
                child.widget.show()

    def hide(self, propagate: bool = True) -> None:
        """Cache le composant

        Args:
            propagate: propage l'état aux enfants
        """
        was_visible = self._visible
        self._visible = False
        if was_visible and self._on_hide:
            self._on_hide.trigger()
        if propagate:
            for child in self._children:
                child.widget.hide()
    
    def switch_visibility(self, propagate: bool = True) -> None:
        """Bascule la visibilité

        Args:
            propagate: propage l'état aux enfants
        """
        if self._visible:
            self.hide(propagate=propagate)
        else:
            self.show(propagate=propagate)

    def set_visibility(self, value: bool, propagate: bool = True) -> None:
        """Fixe la visibilité

        Args:
            value: nouvelle visibilité
        """
        if value:
            self.show(propagate=propagate)
        else:
            self.hide(propagate=propagate)
    
    # ======================================== BEHAVIORS ========================================
    def add_behavior(self, behavior: Behavior) -> None:
        """Ajoute un comportement

        Les comportements sont exclusifs par widget.
        """
        # Vérifications
        if getattr(self, f"_{behavior._ID}", None) is not None:
            raise ValueError(f"This widget already has a {type(behavior).__name__}, try to remove it first")
        
        # Attachement
        behavior.attach(self, _from_widget=True)
        setattr(self, f"_{behavior._ID}", behavior)

        # Insertion
        for i in range(len(self._behaviors)):
            if behavior._PRIORITY > getattr(self, self._behaviors[i])._PRIORITY:
                self._behaviors.insert(i, behavior._ID)
                return
        self._behaviors.append(behavior._ID)

    def remove_behavior(self, behavior: Behavior | Type[Behavior] | str) -> None:
        """Retire un comportement

        Args:
            behavior: élément ``Behavior`` ou ``Type`` ou identifiant de behavior à retirer
        """
        # Vérifications
        id_ = behavior if isinstance(behavior, str) else behavior._ID
        if getattr(self, f"_{id_}", None) is None:
            raise ValueError(f"This widget has no {type(behavior).__name__}")
        if isinstance(behavior, Behavior) and getattr(self, f"_{id_}") != behavior:
            raise ValueError("This widget does not own that behavior")
        
        # Dissociation
        behavior.detach(_from_widget=True)
        self._attr_locks = {attr: p for attr, p in self._attr_locks.items() if p != behavior._PRIORITY}
        self._behaviors.remove(id_)
        setattr(self, f"_{id_}", None)

    def get_behavior(self, behavior: type[Behavior] | str) -> Behavior | None:
        """Renvoie un comportement

        Args:
            behavior: ``Type`` ou ``id`` du comportement
        """
        id_ = behavior if isinstance(behavior, str) else behavior._ID
        return getattr(self, f"_{id_}", None)
    
    def get_behaviors(self) -> tuple[Behavior]:
        """Renvoie les comportements attachés"""
        return tuple(behavior for id_ in self._behaviors if (behavior := getattr(self, f"_{id_}", None)) is not None)

    def has_behavior(self, behavior: type[Behavior] | str) -> bool:
        """Vérfie la possession d'un comportement

        Args:
            behavior: ``Type`` ou ``id`` du comportement
        """
        id_ = behavior if isinstance(behavior, str) else behavior._ID
        return getattr(self, f"_{id_}", None) is not None
    
    @property
    def behaviors(self) -> tuple[Behavior]:
        """Renvoie les comportements attachés"""
        return self.get_behaviors()

    @property
    def click(self) -> ClickBehavior:
        """Comportement de clique"""
        return self._click

    @property
    def hover(self) -> HoverBehavior:
        """Comportement de survol"""
        return self._hover

    @property
    def select(self) -> SelectBehavior:
        """Comportement de sélection"""
        return self._select

    @property
    def focus(self) -> FocusBehavior:
        """Comportement de concentration"""
        return self._focus
    
    # ======================================== LOCKING ========================================
    def _lock_attr(self, attr: str, priority: int) -> bool:
        """Tente de verrouiller un attribut pour un behavior de priorité donnée
        
        Args:
            attr: attribut à vérouiller
            priority: niveau de priorité
        """
        current = self._attr_locks.get(attr, 0)
        if priority >= current:
            self._attr_locks[attr] = priority
            return True
        return False

    def _unlock_attr(self, attr: str, priority: int) -> None:
        """Libère le verrou d'un attribut si il appartient à cette priorité
        
        Args:
            attr: attribut à déverouiller
            priority: niveau de priorité
        """
        if self._attr_locks.get(attr) == priority:
            del self._attr_locks[attr]

    # ======================================== CHILDREN ========================================
    def add_child(self, child: Widget, name: str = None, z: int = 1, share_scale: bool = True, share_rotation: bool = True) -> Widget:
        """Ajoute un composant enfant

        Args:
            child: composant à associer
            name: identifiant local du composant
            z: ordre de rendu local
            share_scale: l'enfant suit le redimensionnement du parent
            share_rotaiton: l'enfant suit la rotation du parent

        Returns:
            child: widget enfant associé
        """
        # Vérifications
        if child._layer is not None and child._layer != self._layer:
            raise ValueError(f"{child} is in another layer")
        if child.parent is not None:
            raise ValueError(f"{child} has already a parent")
    
        # Ajout
        wrapper = WidgetWrapper(expect(child, Widget), expect(name, (str, None)), expect(z, int), share_scale, share_rotation)
        child._layer = self._layer
        child._parent = self
        insort(self._children, wrapper)
        return child

    def remove_child(self, child: Widget) -> Widget:
        """Retire un composant enfant

        Args:
            child(Widget): composant à dissocier

        Returns:
            child: widget enfant dissocié
        """
        # Dissociation
        if expect(child, Widget) in self._children:
            child._layer = None
            child._parent = None
            child.sleep()
            self._children.remove(child)
        return child

    def remove_child_by_name(self, name: str) -> None:
        """Retire un composant enfant par son identifiant

        Args:
            name: nom du composant à dissocier
        """
        # Détection
        to_remove: list[WidgetWrapper] = []
        for child in self._children:
            if child.name == name:
                to_remove.append(child)

        # Dissociation
        for wrapper in to_remove:
            wrapper.widget._layer = None
            wrapper.widget._parent = None
            wrapper.widget.sleep()
            self._children.remove(wrapper)

    def clear_children(self) -> None:
        """Retire tous les enfants"""
        for child in self._children:
            child.widget._layer = None
            child.widget._parent = None
            child.widget.sleep()
        self._children.clear()
    
    def reorder(self, child: Widget, z: int) -> None:
        """Modifie le z-order d'un composant enfant

        Args:
            child: composant enfant
            z: ordre de rendu
        """
        wrapper = self._get_wrapper(expect(child, Widget))
        if wrapper.z != z:
            wrapper.z = z
            self._children.remove(child)
            insort(self._children, wrapper)
    
    def child(self, name: str) -> Widget:
        """Renvoie un ``Widget`` enfant par son identifiant

        Args:
            name: identifiant du composant
        """
        for child in self._children:
            if child.name == name:
                return child.widget
        return None

    # ======================================== HOOKS ========================================
    @property
    def on_activate(self) -> CallbackList:
        """Hook d'activation"""
        if self._on_activate is None:
            self._on_activate = CallbackList()
        return self._on_activate
    
    @property
    def on_deactivate(self) -> CallbackList:
        """Hook de désactivation"""
        if self._on_deactivate is None:
            self._on_deactivate = CallbackList()
        return self._on_deactivate
    
    @property
    def on_show(self) -> CallbackList:
        """Hook d'apparition"""
        if self._on_show is None:
            self._on_show = CallbackList()
        return self._on_show

    @property
    def on_hide(self) -> CallbackList:
        """Hook de désapparition"""
        if self._on_hide is None:
            self._on_hide = CallbackList()
        return self._on_hide

    # ======================================== LIFE CYCLE ========================================
    @abstractmethod
    def _update(self, dt: float) -> None: ...

    def update(self, dt: float) -> None:
        """Actualisation
        
        Args:
            dt: delta-time
        """
        if not self._active:
            return
        
        # Actualisation personnel
        self._update(dt)
        for behavior in self.get_behaviors():
            behavior.update(dt)

        # Actualisation des enfants
        for child in reversed(self._children):
            child.widget.update(dt)

        return
    
    @abstractmethod
    def _draw(self, pipeline: Pipeline, context: RenderContext): ...

    def draw(self, pipeline: Pipeline, context: RenderContext, share_scale: bool = True, share_rotation: bool = True) -> None:
        """Affichage
        
        Args:
            pipeline: ``Pipeline`` de rendu
            context: ``RenderContext``du parent
            share_scale: partage de la taille du parent
            share_rotation: partage de la rotation du parent
        """
        if not self._visible:
            return
        self_context = self._context

        # Actualisation du contexte de rendu
        self._update_render_context(context, share_scale, share_rotation)

        # Actualisation de la transformation monde
        self._update_world_transform(self_context)

        # Affichage personnel
        self._draw(pipeline, self_context)

        # Passage au zorder des enfants
        z = self._context.z
        self_context.z = 0

        # Affichage des enfants
        for child in self._children:
            child.widget.draw(pipeline, self_context, share_scale=child.share_scale, share_rotation=child.share_rotation)

        # Restauration du zorder
        self_context.z = z
    
    @abstractmethod
    def _destroy(self) -> None: ...

    def destroy(self) -> None:
        """Destruction"""
        self._destroy()
        if self._parent is not None:
            self._parent.remove_child(self)
        for behavior in self._behaviors:
            behavior.delete()
        for child in self._children:
            child.widget.destroy()
    
    def sleep(self) -> None:
        """Nettoie les ressources"""
        self._destroy()
        for child in self._children:
            child.widget.sleep()
    
    # ======================================== INTERNALS ========================================
    def _switch_layer(self, layer: GuiLayer | None) -> None:
        """Change le layer du composant et de ses enfants

        Args:
            layer: nouveau ``GuiLayer``
        """
        self._layer = layer
        for child in self._children:
            child.widget._switch_layer(layer)
    
    def _get_wrapper(self, child: Widget) -> WidgetWrapper:
        """Récupère le wrapper d'un composant

        Args:
            child: ``Widget`` à chercher
        """
        for wrapper in self._children:
            if wrapper.widget == child:
                return wrapper
        return None
    
    def _update_render_context(self, context: RenderContext, share_scale: bool = True, share_rotation: bool = True) -> RenderContext:
        """Actualise le contexte de rendu avec les paramètres courants

        Args:
            context: ``RenderContext`` du parent
            share_scale: partage de la taille du parent
            share_rotation: partage de la rotation du parent
        """
        self_context = self._context
        self_context.x = self._transform.x + context.x
        self_context.y = self._transform.y + context.y
        self_context.scale = self._transform.scale * (context.scale if share_scale else 1.0)
        self_context.rotation = self._transform.rotation + (context.rotation if share_rotation else 0.0)
        self_context.opacity = self._opacity * context.opacity
        self_context.z = context.z + 1
        self_context.group = WidgetGroup.get_group(order=context.z, parent=context.group, scissor=self._compute_scissor())
        return self_context
    
    def _update_world_transform(self, context: RenderContext) -> None:
        """Actualisation de la transformation monde"""
        tr = self._world_transform
        tr.x = context.x
        tr.y = context.y
        tr.scale = context.scale
        tr.rotation = context.rotation

    def _compute_scissor(self) -> tuple | None:
        """Calcule le scissor résolu en coordonnées framebuffer"""
        if not self._scissor_dirty:
            return self._cached_scissor
        if not self._clipping:
            result = self._parent._compute_scissor() if self._parent else None
        else:
            self_context = self._context
            xmin, ymin, xmax, ymax = self._geometry.world_bounding_box()
            x, y = self_context.pipeline.world_to_framebuffer(xmin, ymin)
            width, height = self_context.pipeline.scale_to_framebuffer(xmax - xmin, ymax - ymin)
            scissor = (int(x), int(y), int(width), int(height))
            parent_scissor = self._parent._compute_scissor() if self._parent else None
            result = intersect(parent_scissor, scissor) if parent_scissor else scissor
        self._cached_scissor = result
        self._scissor_dirty = False
        return result

    def _invalidate_scissor(self) -> None:
        """Propage l'invalidation du scissor aux enfants"""
        if not self._scissor_dirty:
            self._scissor_dirty = True
            WidgetGroup.invalidate(id(self))
            for child in self._children:
                child.widget._invalidate_scissor()
    
    def _invalidate_geometry(self) -> None:
        """Invalide la géométrie *(changement de hitbox)*"""
        self._geometry = Geometry(self.hitbox, self._world_transform)

# ======================================== WRAPPER ========================================
class WidgetWrapper:
    """Wrapper des composants UI"""
    __slots__ = ("_widget", "name", "z", "share_scale", "share_rotation")

    def __init__(self, widget: Widget, name: str, z: int, share_scale: bool, share_rotation: bool):
        self._widget: Widget = widget
        self.name: str = name
        self.z: int = z
        self.share_scale: bool = share_scale
        self.share_rotation: bool = share_rotation
    
    @property
    def widget(self) -> Widget:
        """``Widget`` contenu"""
        return self._widget

    def __eq__(self, other: Widget | WidgetWrapper) -> bool:
        """Vérifie la correspondance des composants"""
        if isinstance(other, Widget):
            return self._widget == other
        elif isinstance(other, WidgetWrapper):
            return self._widget == other._widget
        return NotImplemented

    def __lt__(self, other: WidgetWrapper) -> bool:
        """Comparaison inférieure"""
        return self.z < other.z
    
    def copy(self) -> WidgetWrapper:
        """Renvoie une copie du wrapper"""
        return WidgetWrapper(
            widget = self._widget.copy(),
            name = self.name,
            z = self.z,
            share_scale = self.share_scale,
            share_rotation = self.share_rotation,
        )
    
# ======================================== HELPERS ========================================
def intersect(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Renvoie l'intersection de deux Rectangles

    Args:
        a: premier rect
        b: second rect
    """
    # Unpackaging
    ax, ay, aw, ah = a
    bx, by, bw, bh = b

    # Calcul de l'intersection
    x = max(ax, bx)
    y = max(ay, by)
    w = max(0, min(ax + aw, bx + bw) - x)
    h = max(0, min(ay + ah, by + bh) - y)
    return x, y, w, h