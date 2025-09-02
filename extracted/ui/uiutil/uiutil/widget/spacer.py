# -*- coding: utf-8 -*-

from logging_helper import setup_logging
from uiutil.helper.introspection import calling_base_frame
from ..helper.arguments import pop_kwarg

logging = setup_logging()


class Spacer(object):
    def __init__(self,
                 *args,
                 **kwargs):
        frame = calling_base_frame(pop_kwarg(kwargs, u'frame'))
        kwargs['frame'] = frame
        frame.position_for_next_widget(**kwargs)
