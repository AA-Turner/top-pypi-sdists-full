######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.866149                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow
    import metaflow.events


TYPE_CHECKING: bool

class MetaflowEvent(tuple, metaclass=type):
    """
    Container of metadata that identifies the event that triggered
    the `Run` under consideration.
    
    Attributes
    ----------
    name : str
        name of the event.
    id : str
        unique identifier for the event.
    timestamp : datetime
        timestamp recording creation time for the event.
    type : str
        type for the event - one of `event` or `run`
    """
    @staticmethod
    def __new__(_cls, name, id, timestamp, type):
        """
        Create new instance of MetaflowEvent(name, id, timestamp, type)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    ...

class Trigger(object, metaclass=type):
    """
    Defines a container of event triggers' metadata.
    """
    def __init__(self, _meta = None):
        ...
    @classmethod
    def from_runs(cls, run_objs: typing.List["metaflow.Run"]):
        ...
    @property
    def event(self) -> typing.Optional[metaflow.events.MetaflowEvent]:
        """
        The `MetaflowEvent` object corresponding to the triggering event.
        
        If multiple events triggered the run, this property is the latest event.
        
        Returns
        -------
        MetaflowEvent, optional
            The latest event that triggered the run, if applicable.
        """
        ...
    @property
    def events(self) -> typing.Optional[typing.List[metaflow.events.MetaflowEvent]]:
        """
        The list of `MetaflowEvent` objects correspondings to all the triggering events.
        
        Returns
        -------
        List[MetaflowEvent], optional
            List of all events that triggered the run
        """
        ...
    @property
    def run(self) -> typing.Optional["metaflow.Run"]:
        """
        The corresponding `Run` object if the triggering event is a Metaflow run.
        
        In case multiple runs triggered the run, this property is the latest run.
        Returns `None` if none of the triggering events are a `Run`.
        
        Returns
        -------
        Run, optional
            Latest Run that triggered this run, if applicable.
        """
        ...
    @property
    def runs(self) -> typing.Optional[typing.List["metaflow.Run"]]:
        """
        The list of `Run` objects in the triggering events.
        Returns `None` if none of the triggering events are `Run` objects.
        
        Returns
        -------
        List[Run], optional
            List of runs that triggered this run, if applicable.
        """
        ...
    def __getitem__(self, key: str) -> typing.Union["metaflow.Run", metaflow.events.MetaflowEvent]:
        """
        If triggering events are runs, `key` corresponds to the flow name of the triggering run.
        Otherwise, `key` corresponds to the event name and a `MetaflowEvent` object is returned.
        
        Returns
        -------
        Union[Run, MetaflowEvent]
            `Run` object if triggered by a run. Otherwise returns a `MetaflowEvent`.
        """
        ...
    def __iter__(self):
        ...
    def __contains__(self, ident: str) -> bool:
        ...
    ...

