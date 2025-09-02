# encoding: utf-8

import logging_helper
from .dynamic_kwarg import handle_kwarg

logging = logging_helper.setup_logging()

# Variable keys
VARIABLE_NAME = u'name'
VARIABLE_TYPE = u'type'
VARIABLE_SETTINGS = u'settings'


def handle_variable(frame,
                    var_config,
                    name_default=None,
                    **locals_dict):

    # Get the var name
    var_name = var_config.get(VARIABLE_NAME, name_default)
    logging.debug(u'var name: {k}'.format(k=var_name))

    # Get the Tk var object
    var_object = getattr(frame, var_config[VARIABLE_TYPE])

    # Get the var settings
    var_settings = var_config.get(VARIABLE_SETTINGS, {})
    logging.debug(u'var settings: {k}'.format(k=var_settings))

    # Process var kwargs
    var_kwargs = {}

    # Process the var name
    if var_name is not None:
        var_kwargs[u'name'] = var_name
        locals_dict[u'var_name'] = var_name

    # Process var default value
    if u'value' in var_settings:
        var_kwargs[u'value'] = handle_kwarg(frame, var_settings[u'value'], locals_dict)

    logging.debug(u'var kwargs: {k}'.format(k=var_kwargs))

    # Create the widget var.
    var = var_object(**var_kwargs)

    # Process the widget var trace value (if required)
    if u'trace' in var_settings:
        widget_var_trace_fn = handle_kwarg(frame, var_settings[u'trace'], locals_dict)

        # Ensure the function has not evaluated as a string value (this is possible!)
        if not isinstance(widget_var_trace_fn, str):
            logging.debug(u'Setup trace for {v}'.format(v=var_name))
            var.trace("w", (lambda name, index, mode, var_name=var_name, var_obj=var:
                            widget_var_trace_fn(var_name, var_obj)))

    return var
