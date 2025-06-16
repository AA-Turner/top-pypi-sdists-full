# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Button(Component):
    """A Button component.
A Button component. 
 Used as a part of Upload component.

Keyword arguments:

- btnClass (default 'dash-uploader-btn'):
    The CSS class for the button.

- disabled (default False):
    Is disabled, the component is not shown.

- isUploading (default False):
    Is True, the parent component  has upload in progress.

- onClick (default () => { }):
    Function to call when clicked.

- text (default ''):
    The text on the button."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_uploader'
    _type = 'Button'
    @_explicitize_args
    def __init__(self, text=Component.UNDEFINED, btnClass=Component.UNDEFINED, onClick=Component.UNDEFINED, disabled=Component.UNDEFINED, isUploading=Component.UNDEFINED, **kwargs):
        self._prop_names = ['btnClass', 'disabled', 'isUploading', 'onClick', 'text']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['btnClass', 'disabled', 'isUploading', 'onClick', 'text']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Button, self).__init__(**args)
