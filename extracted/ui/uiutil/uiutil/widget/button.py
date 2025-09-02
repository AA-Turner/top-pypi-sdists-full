# -*- coding: utf-8 -*-

from uiutil.tk_names import ttk
from .base_widget import BaseWidget


class Button(BaseWidget):
    WIDGET = ttk.Button
    STYLE = u"TButton"
    VAR_TYPE = BaseWidget.string_var
    VAR_PARAM = u'textvariable'

    def __init__(self,
                 *args,
                 **kwargs):
        """
        Note: If the button text is static, you can use the 'text' parameter to initialise it.
        In that case, you don't need to store the button object in your frame.
        If you need to change the button text dynamically, you need to store the button object
        in your frame and you should initialise with the initial_value parameter
        
        :param args: Do not pass positional arguments.
        :param kwargs: 
        """
        super(Button, self).__init__(*args, **kwargs)
