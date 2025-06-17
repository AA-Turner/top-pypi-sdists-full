######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.929382                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException

ARGO_EVENTS_WEBHOOK_AUTH: str

ARGO_EVENTS_WEBHOOK_URL: None

SERVICE_HEADERS: dict

class ArgoEventException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class ArgoEvent(object, metaclass=type):
    """
    ArgoEvent is a small event, a message, that can be published to Argo Workflows. The
    event will eventually start all flows which have been previously deployed with `@trigger`
    to wait for this particular named event.
    
    Parameters
    ----------
    name : str,
        Name of the event
    url : str, optional
        Override the event endpoint from `ARGO_EVENTS_WEBHOOK_URL`.
    payload : Dict, optional
        A set of key-value pairs delivered in this event. Used to set parameters of triggered flows.
    """
    def __init__(self, name, url = None, payload = None, access_token = None):
        ...
    def add_to_payload(self, key, value):
        """
        Add a key-value pair in the payload. This is typically used to set parameters
        of triggered flows. Often, `key` is the parameter name you want to set to
        `value`. Overrides any existing value of `key`.
        
        Parameters
        ----------
        key : str
            Key
        value : str
            Value
        """
        ...
    def safe_publish(self, payload = None, ignore_errors = True):
        """
        Publishes an event when called inside a deployed workflow. Outside a deployed workflow
        this function does nothing.
        
        Use this function inside flows to create events safely. As this function is a no-op
        for local runs, you can safely call it during local development without causing unintended
        side-effects. It takes effect only when deployed on Argo Workflows.
        
        Parameters
        ----------
        payload : dict
            Additional key-value pairs to add to the payload.
        ignore_errors : bool, default True
            If True, events are created on a best effort basis - errors are silently ignored.
        """
        ...
    def publish(self, payload = None, force = True, ignore_errors = True):
        """
        Publishes an event.
        
        Note that the function returns immediately after the event has been sent. It
        does not wait for flows to start, nor it guarantees that any flows will start.
        
        Parameters
        ----------
        payload : dict
            Additional key-value pairs to add to the payload.
        ignore_errors : bool, default True
            If True, events are created on a best effort basis - errors are silently ignored.
        """
        ...
    ...

