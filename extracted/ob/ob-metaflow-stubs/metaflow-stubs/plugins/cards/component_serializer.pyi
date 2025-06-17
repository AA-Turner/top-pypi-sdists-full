######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.922293                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.cards.card_modules.basic

from .card_modules.card import MetaflowCardComponent as MetaflowCardComponent
from .card_modules.card import create_component_id as create_component_id
from .card_modules.basic import ErrorComponent as ErrorComponent
from .card_modules.basic import SectionComponent as SectionComponent
from .card_modules.components import UserComponent as UserComponent
from .card_modules.components import StubComponent as StubComponent
from .exception import ComponentOverwriteNotSupportedException as ComponentOverwriteNotSupportedException

RUNTIME_CARD_RENDER_INTERVAL: int

def get_card_class(card_type):
    ...

def warning_message(message, logger = None, ts = False):
    ...

class WarningComponent(metaflow.plugins.cards.card_modules.basic.ErrorComponent, metaclass=type):
    def __init__(self, warning_message):
        ...
    ...

class ComponentStore(object, metaclass=type):
    """
    The `ComponentStore` object helps store the components for a single card in memory.
    This class has combination of a array/dictionary like interfaces to access/change the stored components.
    
    It exposes the `append` /`extend` methods (like an array) to add components.
    It also exposes the `__getitem__`/`__setitem__` methods (like a dictionary) to access the components by their Ids.
    """
    def __init__(self, logger, card_type = None, components = None, user_set_id = None):
        ...
    @property
    def layout_last_changed_on(self):
        """
        This property helps the CardComponentManager identify when the layout of the card has changed so that it can trigger a re-render of the card.
        """
        ...
    def __iter__(self):
        ...
    def __setitem__(self, key, value):
        ...
    def __getitem__(self, key):
        ...
    def __delitem__(self, key):
        ...
    def __contains__(self, key):
        ...
    def append(self, component, id = None):
        ...
    def extend(self, components):
        ...
    def clear(self):
        ...
    def keys(self):
        ...
    def values(self):
        ...
    def __str__(self):
        ...
    def __len__(self):
        ...
    ...

class CardComponentManager(object, metaclass=type):
    """
    This class manages the card's state for a single card.
    - It uses the `ComponentStore` to manage the storage of the components
    - It exposes methods to add, remove and access the components.
    - It exposes a `refresh` method that will allow refreshing a card with new data
    for realtime(ish) updates.
    - The `CardComponentCollector` exposes convenience methods similar to this class for a default
    editable card. These methods include :
        - `append`
        - `extend`
        - `clear`
        - `refresh`
        - `components`
        - `__iter__`
    
    ## Usage Patterns :
    
    ```python
    current.card["mycardid"].append(component, id="comp123")
    current.card["mycardid"].extend([component])
    current.card["mycardid"].refresh(data) # refreshes the card with new data
    current.card["mycardid"].components["comp123"] # returns the component with id "comp123"
    current.card["mycardid"].components["comp123"].update()
    current.card["mycardid"].components.clear() # Wipe all the components
    del current.card["mycardid"].components["mycomponentid"] # Delete a component
    ```
    """
    def __init__(self, card_uuid, decorator_attributes, card_creator, components = None, logger = None, no_warnings = False, user_set_card_id = None, runtime_card = False, card_options = None, refresh_interval = 5):
        ...
    def append(self, component, id = None):
        ...
    def extend(self, components):
        ...
    def clear(self):
        ...
    def refresh(self, data = None, force = False):
        ...
    @property
    def components(self):
        ...
    def __iter__(self):
        ...
    ...

class CardComponentCollector(object, metaclass=type):
    """
    This class helps collect `MetaflowCardComponent`s during runtime execution
    
    ### Usage with `current`
    `current.card` is of type `CardComponentCollector`
    
    ### Main Usage TLDR
    - [x] `current.card.append` customizes the default editable card.
    - [x] Only one card can be default editable in a step.
    - [x] The card class must have `ALLOW_USER_COMPONENTS=True` to be considered default editable.
        - [x] Classes with `ALLOW_USER_COMPONENTS=False` are never default editable.
    - [x] The user can specify an `id` argument to a card, in which case the card is editable through `current.card[id].append`.
        - [x] A card with an id can be also default editable, if there are no other cards that are eligible to be default editable.
    - [x] If multiple default-editable cards exist but only one card doesn't have an id, the card without an id is considered to be default editable.
    - [x] If we can't resolve a single default editable card through the above rules, `current.card`.append calls show a warning but the call doesn't fail.
    - [x] A card that is not default editable can be still edited through:
        - [x] its `current.card['myid']`
        - [x] by looking it up by its type, e.g. `current.card.get(type='pytorch')`.
    """
    def __init__(self, logger = None, card_creator = None):
        ...
    @staticmethod
    def create_uuid():
        ...
    def get(self, type = None):
        """
        `get`
        gets all the components arrays for a card `type`.
        Since one `@step` can have many `@card` decorators, many decorators can have the same type. That is why this function returns a list of lists.
        
        Args:
            type ([str], optional): `type` of MetaflowCard. Defaults to None.
        
        Returns: will return empty `list` if `type` is None or not found
            List[List[MetaflowCardComponent]]
        """
        ...
    def __getitem__(self, key):
        """
        Choose a specific card for manipulation.
        
        When multiple @card decorators are present, you can add an
        `ID` to distinguish between them, `@card(id=ID)`. This allows you
        to add components to a specific card like this:
        ```
        current.card[ID].append(component)
        ```
        
        Parameters
        ----------
        key : str
            Card ID.
        
        Returns
        -------
        CardComponentManager
            An object with `append` and `extend` calls which allow you to
            add components to the chosen card.
        """
        ...
    def __setitem__(self, key, value):
        """
        Specify components of the chosen card.
        
        Instead of adding components to a card individually with `current.card[ID].append(component)`,
        use this method to assign a list of components to a card, replacing the existing components:
        ```
        current.card[ID] = [FirstComponent, SecondComponent]
        ```
        
        Parameters
        ----------
        key: str
            Card ID.
        
        value: List[MetaflowCardComponent]
            List of card components to assign to this card.
        """
        ...
    def append(self, component, id = None):
        """
        Appends a component to the current card.
        
        Parameters
        ----------
        component : MetaflowCardComponent
            Card component to add to this card.
        """
        ...
    def extend(self, components):
        """
        Appends many components to the current card.
        
        Parameters
        ----------
        component : Iterator[MetaflowCardComponent]
            Card components to add to this card.
        """
        ...
    @property
    def components(self):
        ...
    def clear(self):
        ...
    def refresh(self, *args, **kwargs):
        ...
    ...

