######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.20.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-03-09T17:10:37.662165                                                            #
######################################################################################################

from __future__ import annotations



NAMESPACED_EVENTS_PREFIX: str

class ParsedEvent(tuple, metaclass=type):
    """
    ParsedEvent(full_name, project, branch, logical_name, is_namespaced)
    """
    @staticmethod
    def __new__(_cls, full_name, project, branch, logical_name, is_namespaced):
        """
        Create new instance of ParsedEvent(full_name, project, branch, logical_name, is_namespaced)
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

def namespaced_event_name(event_name):
    """
    Creates a project-namespaced event name based on @project settings.
    
    Use this to automatically prefix event names with your @project
    namespace, ensuring events are isolated per project and branch.
    
    The resolved name follows the format:
        mfns.<project>.<branch>.<event_name>
    
    If no @project decorator is present, resolves to:
        mfns.<event_name>
    
    Parameters
    ----------
    event_name : str
        The logical event name (e.g., 'data_ready')
    
    Returns
    -------
    Callable[..., str]
        A callable that returns the fully namespaced event name (str) when invoked
    
    Examples
    --------
    With @trigger decorator:
    
        ```
        from metaflow import namespaced_event_name, project
    
        @project(name="foo")
        @trigger(event=namespaced_event_name('data_ready'))
        class MyFlow(FlowSpec):
            ...
    
        @project(name="foo")
        @trigger(event={'name': namespaced_event_name('data_ready'), 'parameters': {'x': 'y'}})
        class MyFlow(FlowSpec):
        ```
    
    With ArgoEvent:
    
        ```
        from metaflow import namespaced_event_name
        from metaflow.integrations import ArgoEvent
    
        ArgoEvent(namespaced_event_name('data_ready')).publish()
        ```
    """
    ...

