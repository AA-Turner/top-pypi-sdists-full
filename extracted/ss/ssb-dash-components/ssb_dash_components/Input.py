# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Input(Component):
    """An Input component.
SSB styled Input field and search field

Keyword arguments:

- id (string; optional)

- ariaLabel (string; optional)

- ariaLabelSearchButton (string; default 'search')

- ariaLabelWrapper (string; optional)

- ariaLabelledBy (string; optional)

- className (string; default '')

- debounce (boolean; default False):
    If this is set to True, then values will only be sent when Enter
    is pressed or focus is lost.

- description (string; optional):
    Add explanation text.

- disabled (boolean; default False)

- error (boolean; default False)

- errorMessage (string; optional)

- label (string; optional)

- n_submit (number; optional)

- name (string; optional)

- negative (boolean; default False)

- placeholder (string; optional)

- readOnly (boolean; default False):
    Use this attribute on non editable input fields.

- role (string; optional)

- searchField (boolean; default False)

- showDescription (boolean; optional):
    Set True to show description.

- size (string; optional)

- type (string; default 'text')

- value (string; default '')"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'ssb_dash_components'
    _type = 'Input'
    @_explicitize_args
    def __init__(self, role=Component.UNDEFINED, ariaLabelWrapper=Component.UNDEFINED, ariaLabel=Component.UNDEFINED, ariaLabelledBy=Component.UNDEFINED, ariaLabelSearchButton=Component.UNDEFINED, name=Component.UNDEFINED, className=Component.UNDEFINED, disabled=Component.UNDEFINED, error=Component.UNDEFINED, errorMessage=Component.UNDEFINED, id=Component.UNDEFINED, label=Component.UNDEFINED, negative=Component.UNDEFINED, placeholder=Component.UNDEFINED, searchField=Component.UNDEFINED, size=Component.UNDEFINED, type=Component.UNDEFINED, value=Component.UNDEFINED, n_submit=Component.UNDEFINED, showDescription=Component.UNDEFINED, description=Component.UNDEFINED, readOnly=Component.UNDEFINED, debounce=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'ariaLabel', 'ariaLabelSearchButton', 'ariaLabelWrapper', 'ariaLabelledBy', 'className', 'debounce', 'description', 'disabled', 'error', 'errorMessage', 'label', 'n_submit', 'name', 'negative', 'placeholder', 'readOnly', 'role', 'searchField', 'showDescription', 'size', 'type', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ariaLabel', 'ariaLabelSearchButton', 'ariaLabelWrapper', 'ariaLabelledBy', 'className', 'debounce', 'description', 'disabled', 'error', 'errorMessage', 'label', 'n_submit', 'name', 'negative', 'placeholder', 'readOnly', 'role', 'searchField', 'showDescription', 'size', 'type', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Input, self).__init__(**args)
