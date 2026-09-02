# encoding: utf-8

import logging_helper
from functools import reduce

logging = logging_helper.setup_logging()

KWARG_VALUE = u'value'
KWARG_LOCATION = u'location'
KWARG_LAMBDA = u'lambda'

# kwarg locations
KWARG_LOCAL = u'local'
KWARG_SELF = u'self'
KWARG_PARENT = u'parent'
KWARG_WINDOW = u'window'
KWARG_DICT = u'dict'
KWARG_LIST = u'list'
KWARG_CFG = u'cfg'
KWARG_ITER_VALUE = u'iter_value'
KWARG_VAR = u'var'

LINE_KWARG_ITER_NAME = u'iterable_name'
LINE_KWARG_ITER_VALUE = u'iterable_value'


def handle_kwarg(frame,
                 kwarg_cfg,
                 locals_dict=None):

    logging.debug(u'un-processed kwarg: {k}'.format(k=kwarg_cfg))

    if locals_dict is None:
        locals_dict = {}

    logging.debug(u'locals_dict: {l}'.format(l=locals_dict))

    # Handle specific kwargs that are expected to have config
    # Get kwarg config
    kw_value = kwarg_cfg[KWARG_VALUE]
    kw_location = kwarg_cfg.get(KWARG_LOCATION)
    kw_lambda = kwarg_cfg.get(KWARG_LAMBDA, False)

    # If the value is a number set the kwarg otherwise we have to do some processing!
    if isinstance(kw_value, (int, float)):
        kwarg = kw_value

    else:
        # Split the attribute path in case we have to reduce
        attribute_pth = kw_value.split(u'.')

        # Decode the kwarg value
        if kw_location == KWARG_LOCAL and kw_value in locals_dict:
            kwarg = locals_dict[kw_value]

        elif kw_location == KWARG_SELF:
            kwarg = reduce(getattr, attribute_pth, frame)

        elif kw_location == KWARG_PARENT:
            kwarg = reduce(getattr, attribute_pth, frame.parent)

        elif kw_location == KWARG_WINDOW:
            kwarg = reduce(getattr, attribute_pth, frame.parent.parent.master)

        elif kw_location == KWARG_VAR:
            # Get the self reference to our widget var
            kwarg = getattr(frame, locals_dict[kw_value])

        elif kw_location == KWARG_DICT:
            kwarg = frame.parent.item_dict.get(kw_value)

        elif kw_location == KWARG_LIST:
            kwarg = frame.parent.item_list[kw_value]

        elif kw_location == KWARG_CFG and frame.item_key is not None:
            key = u'{c}.{k}'.format(c=frame.item_key,
                                    k=kw_value)

            kwarg = frame.cfg[key]

        elif kw_location == KWARG_ITER_VALUE:
            # Get the iterable_value param
            iterable_values = locals_dict.get(LINE_KWARG_ITER_VALUE)

            # If iterable_values or lookup value is not available then return empty string
            kwarg = u'' if iterable_values is None else iterable_values.get(kw_value, u'')

        else:
            kwarg = kw_value

        # Handle lambda
        if kw_location in (KWARG_WINDOW, KWARG_PARENT, KWARG_SELF) and kw_lambda:
            cmd_fn = kwarg  # We need to use a temp var otherwise lambda will pass itself!
            kwarg = (lambda name=locals_dict.get(u'var_name'), var=locals_dict.get(u'widget_var'):
                     cmd_fn(widget_var_name=name,
                            widget_var=var))

    logging.debug(u'processed kwarg: {k}'.format(k=kwarg))

    return kwarg
