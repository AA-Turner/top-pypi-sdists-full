######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.890924                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.cards.card_client
    import metaflow

from .card_resolver import resolve_paths_from_task as resolve_paths_from_task
from .card_resolver import resumed_info as resumed_info
from .card_datastore import CardDatastore as CardDatastore
from .card_datastore import CardNameSuffix as CardNameSuffix
from .exception import UnresolvableDatastoreException as UnresolvableDatastoreException
from .exception import IncorrectArgumentException as IncorrectArgumentException
from .exception import IncorrectPathspecException as IncorrectPathspecException

TYPE_CHECKING: bool

CARD_SUFFIX: str

class Card(object, metaclass=type):
    """
    `Card` represents an individual Metaflow Card, a single HTML file, produced by
    the card `@card` decorator. `Card`s are contained by `CardContainer`, returned by
    `get_cards`.
    
    Note that the contents of the card, an HTML file, is retrieved lazily when you call
    `Card.get` for the first time or when the card is rendered in a notebook.
    """
    def __init__(self, card_ds, type, path, hash, id = None, html = None, created_on = None, from_resumed = False, origin_pathspec = None):
        ...
    def get_data(self) -> typing.Optional[dict]:
        ...
    def get(self) -> str:
        """
        Retrieves the HTML contents of the card from the
        Metaflow datastore.
        
        Returns
        -------
        str
            HTML contents of the card.
        """
        ...
    @property
    def path(self) -> str:
        """
        The path of the card in the datastore which uniquely
        identifies the card.
        
        Returns
        -------
        str
            Path to the card
        """
        ...
    @property
    def id(self) -> typing.Optional[str]:
        """
        The ID of the card, if specified with `@card(id=ID)`.
        
        Returns
        -------
        Optional[str]
            ID of the card
        """
        ...
    def __str__(self):
        ...
    def view(self):
        """
        Opens the card in a local web browser.
        
        This call uses Python's built-in [`webbrowser`](https://docs.python.org/3/library/webbrowser.html)
        module to open the card.
        """
        ...
    ...

class CardContainer(object, metaclass=type):
    """
    `CardContainer` is an immutable list-like object, returned by `get_cards`,
    which contains individual `Card`s.
    
    Notably, `CardContainer` contains a special
    `_repr_html_` function which renders cards automatically in an output
    cell of a notebook.
    
    The following operations are supported:
    ```
    cards = get_cards(MyTask)
    
    # retrieve by index
    first_card = cards[0]
    
    # check length
    if len(cards) > 1:
        print('many cards present!')
    
    # iteration
    list_of_cards = list(cards)
    ```
    """
    def __init__(self, card_paths, card_ds, origin_pathspec = None):
        ...
    def __len__(self):
        ...
    def __iter__(self):
        ...
    def __getitem__(self, index):
        ...
    ...

def get_cards(task: typing.Union[str, "metaflow.Task"], id: typing.Optional[str] = None, type: typing.Optional[str] = None, follow_resumed: bool = True) -> CardContainer:
    """
    Get cards related to a `Task`.
    
    Note that `get_cards` resolves the cards contained by the task, but it doesn't actually
    retrieve them from the datastore. Actual card contents are retrieved lazily either when
    the card is rendered in a notebook to when you call `Card.get`. This means that
    `get_cards` is a fast call even when individual cards contain a lot of data.
    
    Parameters
    ----------
    task : Union[str, `Task`]
        A `Task` object or pathspec `{flow_name}/{run_id}/{step_name}/{task_id}` that
        uniquely identifies a task.
    id : str, optional, default None
        The ID of card to retrieve if multiple cards are present.
    type : str, optional, default None
        The type of card to retrieve if multiple cards are present.
    follow_resumed : bool, default True
        If the task has been resumed, then setting this flag will resolve the card for
        the origin task.
    
    Returns
    -------
    CardContainer
        A list-like object that holds `Card` objects.
    """
    ...

