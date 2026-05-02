# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, positive, not_null
from ..abc import Widget

# ======================================== GROUP ========================================
class SelectionGroup:
    """Groupe de sélection pour les SelectBehavior
    
    Args:
        name: nom du groupe
        limit: nombre maximum de membres sélectionnés simultanément
        replace: remplacement lors du dépassement
        deselectable: possibilité de désélection
    """
    __slots__ = (
        "_name", "_limit", "_replace", "_deselectable",
        "_members", "_selected",
    )
    _groups: dict[str, SelectionGroup] = {}

    def __init__(
            self,
            name: str,
            limit: int = None,
            replace: bool = False,
            deselectable: bool = True,
        ):
        # Paramètres
        self._name: str = expect(name, str)
        self._limit: int | None = expect(limit, (int, None))
        self._replace: bool = expect(replace, bool)
        self._deselectable: bool = expect(deselectable, bool)

        # Construction
        self._members: set[Widget] = set()
        self._selected: list[Widget] = []

        # Enregistrement
        if self._name in self._groups.keys():
            raise ValueError(f"A SelectionGroup with name {self._name!r} already exists")
        self._groups[name] = self

    # ======================================== CLASSMETHODS ========================================
    @classmethod
    def get(cls, name: str) -> SelectionGroup:
        """Renvoie un groupe de sélection

        Args:
            name: nom du groupe
        """
        return cls._groups[name]
    
    # ======================================== PROPERTIES ========================================
    @property
    def name(self) -> str:
        """Nom du groupe de sélection

        Le nom doit être unique.
        """
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        if value == self._name:
            return
        if value in self._groups.keys():
            raise ValueError(f"A SelectionGroup with name {value!r} already exists")
        del self._groups[self._name]
        self._name = value
        self._groups[value] = self

    @property
    def limit(self) -> int | None:
        """Nombre maximum de membres sélectionnés simultanément

        La limite doit être un ``int``, ou ``None`` pour une sélection illimitée.
        """
        return self._limit

    @limit.setter
    def limit(self, value: int | None) -> None:
        self._limit = positive(not_null(expect(value, (int, None))))

    @property
    def replace(self) -> bool:
        """Remplacement lors du dépassement de la limite

        Si ``True``, les membres sélectionnés sont désélectionnés dans l'ordre d'ajout.
        Si ``False``, les nouveaux membres ne sont pas sélectionnés.
        """
        return self._replace
    
    @replace.setter
    def replace(self, value: bool) -> None:
        self._replace = expect(value, bool)

    @property
    def deselectable(self) -> bool:
        """Possibilité de désélection

        Si ``True``, les membres sélectionnés peuvent être désélectionnés.
        Si ``False``, les membres sélectionnés ne peuvent pas être désélectionnés (sauf remplacement).
        """
        return self._deselectable
    
    @deselectable.setter
    def deselectable(self, value: bool) -> None:
        self._deselectable = expect(value, bool)

    # ======================================== COLLECTION ========================================
    def add(self, widget: Widget) -> None:
        """Ajoute un ``Widget`` au groupe"""
        self._members.add(widget)

    def remove(self, widget: Widget) -> None:
        """Retire un ``Widget`` du groupe"""
        if widget in self._selected:
            self.deselect(widget)
        self._members.remove(widget)

    def clear(self) -> None:
        """Vide le groupe de tous ses membres"""
        for widget in list(self._selected):
            self.deselect(widget)
        self._members.clear()

    def get_members(self) -> set[Widget]:
        """Renvoie l'ensemble des membres du groupe"""
        return self._members
    
    def __len__(self) -> int:
        """Renvoie le nombre de membres du groupe"""
        return len(self._members)

    # ======================================== STATE ========================================
    def click(self, widget: Widget) -> None:
        """Gère les clics sur un membre du groupe"""
        if widget in self._selected:
            if self._deselectable: self.deselect(widget)
        else:
            self.select(widget)

    def select(self, widget: Widget) -> None:
        """Sélectionne un membre du groupe"""
        if self._limit is not None and len(self._selected) >= self._limit:
            if not self._replace:
                return
            self.deselect(self._selected[0])
        self._selected.append(widget)
        widget.select.select()
    
    def deselect(self, widget: Widget) -> None:
        """Désélectionne un membre du groupe"""
        self._selected.remove(widget)
        widget.select.deselect()
    
    def deselect_all(self) -> None:
        """Désélectionne tous les membres du groupe"""
        for widget in list(self._selected):
            self.deselect(widget)

    def is_selected(self, widget: Widget) -> bool:
        """Indique si un membre du groupe est sélectionné"""
        return widget in self._selected
    
    def get_selected(self) -> list[Widget]:
        """Renvoie la liste des membres sélectionnés"""
        return self._selected