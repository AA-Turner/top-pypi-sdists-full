# -*- coding: utf-8 -*-

from uiutil.tk_names import ttk
from .base_widget import BaseWidget


class Label(BaseWidget):
    WIDGET = ttk.Label
    STYLE = u"TLabel"
    VAR_TYPE = BaseWidget.string_var
    VAR_PARAM = u'textvariable'

    def __init__(self,
                 *args,
                 **kwargs):
        """
        Note: If the label text is static, you can use the 'text' parameter to initialise it.
        In that case, you don't need to store the label object in your frame.
        If you need to change the label text dynamically, you need to store the label object
        in your frame and you should initialise with the initial_text parameter.

        :param args: 
        :param kwargs: 
        """
        super(Label, self).__init__(*args, **kwargs)


class IntLabel(BaseWidget):
    WIDGET = ttk.Label
    VAR_TYPE = BaseWidget.int_var
    VAR_PARAM = u'textvariable'

    def __init__(self,
                 *args,
                 **kwargs):
        """
        Note: If the label text is static, you can use the 'text' parameter to initialise it.
        In that case, you don't need to store the label object in your frame.
        If you need to change the label text dynamically, you need to store the label object
        in your frame and you should initialise with the initial_text parameter.

        :param args:
        :param kwargs:
        """
        super(IntLabel, self).__init__(*args, **kwargs)
