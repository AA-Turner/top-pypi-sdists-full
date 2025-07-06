# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tabs(Component):
    """A Tabs component.
A SSB styled tab selector component

Keyword arguments:

- id (string; optional)

- active (string; optional)

- activeOnInit (string; optional):
    Will set an item to be active on init.

- className (string; optional):
    Optional container class.

- items (list of dicts; optional):
    Sets label and path of buttons.

    `items` is a list of dicts with keys:

    - title (string; optional)

    - path (string; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'ssb_dash_components'
    _type = 'Tabs'
    @_explicitize_args
    def __init__(self, activeOnInit=Component.UNDEFINED, className=Component.UNDEFINED, items=Component.UNDEFINED, id=Component.UNDEFINED, active=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'active', 'activeOnInit', 'className', 'items']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'active', 'activeOnInit', 'className', 'items']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Tabs, self).__init__(**args)
