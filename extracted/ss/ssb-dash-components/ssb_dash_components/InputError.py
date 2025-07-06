# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class InputError(Component):
    """An InputError component.


Keyword arguments:

- id (string; optional)

- className (string; optional)

- errorMessage (string; required)

- negative (boolean; default False)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'ssb_dash_components'
    _type = 'InputError'
    @_explicitize_args
    def __init__(self, className=Component.UNDEFINED, errorMessage=Component.REQUIRED, negative=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'errorMessage', 'negative']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'errorMessage', 'negative']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['errorMessage']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(InputError, self).__init__(**args)
