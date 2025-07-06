# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Paragraph(Component):
    """A Paragraph component.
A SSB styled paragraph

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional)

- className (string; optional)

- negative (boolean; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'ssb_dash_components'
    _type = 'Paragraph'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, negative=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'negative']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'negative']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Paragraph, self).__init__(children=children, **args)
