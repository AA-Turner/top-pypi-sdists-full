######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.891535                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow


TYPE_CHECKING: bool

class MetaflowCard(object, metaclass=type):
    """
    Metaflow cards derive from this base class.
    
    Subclasses of this class are called *card types*. The desired card
    type `T` is defined in the `@card` decorator as `@card(type=T)`.
    
    After a task with `@card(type=T, options=S)` finishes executing, Metaflow instantiates
    a subclass `C` of `MetaflowCard` that has its `type` attribute set to `T`, i.e. `C.type=T`.
    The constructor is given the options dictionary `S` that contains arbitrary
    JSON-encodable data that is passed to the instance, parametrizing the card. The subclass
    may override the constructor to capture and process the options.
    
    The subclass needs to implement a `render(task)` method that produces the card
    contents in HTML, given the finished task that is represented by a `Task` object.
    
    Attributes
    ----------
    type : str
        Card type string. Note that this should be a globally unique name, similar to a
        Python package name, to avoid name clashes between different custom cards.
    
    Parameters
    ----------
    options : Dict
        JSON-encodable dictionary containing user-definable options for the class.
    """
    def __init__(self, options = {}, components = [], graph = None, flow = None):
        ...
    def render(self, task: "metaflow.Task") -> str:
        """
        Produce custom card contents in HTML.
        
        Subclasses override this method to customize the card contents.
        
        Parameters
        ----------
        task : Task
            A `Task` object that allows you to access data from the finished task and tasks
            preceding it.
        
        Returns
        -------
        str
            Card contents as an HTML string.
        """
        ...
    def render_runtime(self, task, data):
        ...
    def refresh(self, task, data):
        ...
    def reload_content_token(self, task, data):
        ...
    ...

class MetaflowCardComponent(object, metaclass=type):
    @property
    def component_id(self):
        ...
    @component_id.setter
    def component_id(self, value):
        ...
    def update(self, *args, **kwargs):
        """
        #FIXME document
        """
        ...
    def render(self):
        """
        `render` returns a string or dictionary. This class can be called on the client side to dynamically add components to the `MetaflowCard`
        """
        ...
    ...

def create_component_id(component):
    ...

def with_default_component_id(func):
    ...

