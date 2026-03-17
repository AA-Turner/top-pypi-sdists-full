######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.21.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-03-16T23:47:56.040445                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.cards.card_modules.card
    import typing

from .card import MetaflowCardComponent as MetaflowCardComponent
from .card import with_default_component_id as with_default_component_id
from .renderer_tools import render_safely as render_safely
from ...._vendor import yaml as yaml

class JSONViewer(metaflow.plugins.cards.card_modules.card.MetaflowCardComponent, metaclass=type):
    """
    A component for displaying JSON data with syntax highlighting and collapsible sections.
    
    This component provides a rich view of JSON data with proper formatting, syntax highlighting,
    and the ability to collapse/expand sections for better readability.
    
    Example:
    ```python
    from metaflow.cards import JSONViewer
    from metaflow import current
    
    data = {
        "user": {"name": "Alice", "age": 30},
        "items": [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}],
        "metadata": {"created": "2024-01-01", "version": "1.0"}
    }
    
    json_viewer = JSONViewer(data, collapsible=True, max_height="400px")
    current.card.append(json_viewer)
    ```
    
    Parameters
    ----------
    data : Any
        The data to display as JSON. Will be serialized using json.dumps().
    collapsible : bool, default True
        Whether to make the JSON viewer collapsible.
    max_height : str, optional
        Maximum height for the viewer (CSS value like "300px" or "20rem").
    show_copy_button : bool, default True
        Whether to show a copy-to-clipboard button.
    """
    def __init__(self, data: typing.Any, collapsible: bool = True, max_height: typing.Optional[str] = None, show_copy_button: bool = True, title: typing.Optional[str] = None):
        ...
    def update(self, data: typing.Any):
        """
        Update the JSON data.
        
        Parameters
        ----------
        data : Any
            New data to display as JSON.
        """
        ...
    def render(self, *args, **kwargs):
        ...
    ...

class YAMLViewer(metaflow.plugins.cards.card_modules.card.MetaflowCardComponent, metaclass=type):
    """
    A component for displaying YAML data with syntax highlighting and collapsible sections.
    
    This component provides a rich view of YAML data with proper formatting and syntax highlighting.
    
    Example:
    ```python
    from metaflow.cards import YAMLViewer
    from metaflow import current
    
    data = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "credentials": {"username": "admin", "password": "secret"}
        },
        "features": ["auth", "logging", "monitoring"]
    }
    
    yaml_viewer = YAMLViewer(data, collapsible=True)
    current.card.append(yaml_viewer)
    ```
    
    Parameters
    ----------
    data : Any
        The data to display as YAML. Will be serialized to YAML format.
    collapsible : bool, default True
        Whether to make the YAML viewer collapsible.
    max_height : str, optional
        Maximum height for the viewer (CSS value like "300px" or "20rem").
    show_copy_button : bool, default True
        Whether to show a copy-to-clipboard button.
    """
    def __init__(self, data: typing.Any, collapsible: bool = True, max_height: typing.Optional[str] = None, show_copy_button: bool = True, title: typing.Optional[str] = None):
        ...
    def update(self, data: typing.Any):
        """
        Update the YAML data.
        
        Parameters
        ----------
        data : Any
            New data to display as YAML.
        """
        ...
    def render(self, *args, **kwargs):
        ...
    ...

