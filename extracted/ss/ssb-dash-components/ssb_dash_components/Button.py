# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Button(Component):
    """A Button component.
SSB styled Button for triggering actions

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Button text or/and icon.

- id (string; optional)

- ariaLabel (string; default '')

- className (string; default ''):
    Optional container class.

- disabled (boolean; default False):
    Decides if the button is disabled.

- icon (a list of or a singular dash component, string or number; optional):
    Renders an icon.

- n_clicks (number; default 0):
    Number of times the button has been clicked.

- negative (boolean; default False):
    Changes design.

- primary (boolean; default False):
    Changes style to represent a primary button.

- type (string; default 'button'):
    Button type. Can be 'submit', 'reset', or 'button'. Defaults to
    'button'."""
    _children_props = ['icon']
    _base_nodes = ['icon', 'children']
    _namespace = 'ssb_dash_components'
    _type = 'Button'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, n_clicks=Component.UNDEFINED, className=Component.UNDEFINED, disabled=Component.UNDEFINED, icon=Component.UNDEFINED, negative=Component.UNDEFINED, primary=Component.UNDEFINED, type=Component.UNDEFINED, ariaLabel=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'ariaLabel', 'className', 'disabled', 'icon', 'n_clicks', 'negative', 'primary', 'type']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'ariaLabel', 'className', 'disabled', 'icon', 'n_clicks', 'negative', 'primary', 'type']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Button, self).__init__(children=children, **args)
