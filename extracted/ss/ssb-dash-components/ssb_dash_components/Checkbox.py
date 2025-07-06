# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Checkbox(Component):
    """A Checkbox component.
Checkbox is rendered as an input / label pair with value true/false

Keyword arguments:

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- className (string; optional):
    The class of the container (div).

- description (string; optional):
    Add explanation text to Glossary.

- disabled (boolean; default False):
    Disable the Checkbox.

- inputStyle (dict; optional):
    **DEPRECATED** Use `input_style` instead.  The style of the
    <input> checkbox element.

- input_style (dict; optional):
    The style of the <input> checkbox element.

- label (a list of or a singular dash component, string or number; optional):
    The label of the <input> element.

- labelStyle (dict; optional):
    **DEPRECATED** Use `label_style` instead.  Inline style arguments
    to apply to the <label> element for each item.

- label_id (string; optional):
    The id of the label.

- label_style (dict; optional):
    Inline style arguments to apply to the <label> element for each
    item.

- name (string; optional):
    The name of the control, which is submitted with the form data.

- persisted_props (list of a value equal to: 'value's; default ['value']):
    Properties whose user interactions will persist after refreshing
    the component or the page. Since only `value` is allowed this prop
    can normally be ignored.

- persistence (boolean | string | number; optional):
    Used to allow user interactions in this component to be persisted
    when the component - or the page - is refreshed. If `persisted` is
    truthy and hasn't changed from its previous value, a `value` that
    the user has changed while using the app will keep that change, as
    long as the new `value` also matches what was given originally.
    Used in conjunction with `persistence_type`.

- persistence_type (a value equal to: 'local', 'session', 'memory'; default 'local'):
    Where persisted user changes will be stored: memory: only kept in
    memory, reset on page refresh. local: window.localStorage, data is
    kept after the browser quit. session: window.sessionStorage, data
    is cleared once the browser quit.

- showDescription (boolean; optional):
    Must be set to show Glossary component.

- style (dict; optional):
    The style of the container (div).

- value (boolean; default False):
    The value of the input."""
    _children_props = ['label']
    _base_nodes = ['label', 'children']
    _namespace = 'ssb_dash_components'
    _type = 'Checkbox'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, input_style=Component.UNDEFINED, inputStyle=Component.UNDEFINED, label=Component.UNDEFINED, label_id=Component.UNDEFINED, label_style=Component.UNDEFINED, labelStyle=Component.UNDEFINED, name=Component.UNDEFINED, disabled=Component.UNDEFINED, value=Component.UNDEFINED, showDescription=Component.UNDEFINED, description=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'description', 'disabled', 'inputStyle', 'input_style', 'label', 'labelStyle', 'label_id', 'label_style', 'name', 'persisted_props', 'persistence', 'persistence_type', 'showDescription', 'style', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'description', 'disabled', 'inputStyle', 'input_style', 'label', 'labelStyle', 'label_id', 'label_style', 'name', 'persisted_props', 'persistence', 'persistence_type', 'showDescription', 'style', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Checkbox, self).__init__(**args)
