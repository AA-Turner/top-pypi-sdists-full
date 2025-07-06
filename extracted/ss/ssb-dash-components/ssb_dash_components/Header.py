# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Header(Component):
    """A Header component.
SSB styled Header component.
A wrapper for displaying a header

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    All rendered content.

- className (string; optional):
    Optional container class."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'ssb_dash_components'
    _type = 'Header'
    @_explicitize_args
    def __init__(self, children=None, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'className']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'className']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Header, self).__init__(children=children, **args)
