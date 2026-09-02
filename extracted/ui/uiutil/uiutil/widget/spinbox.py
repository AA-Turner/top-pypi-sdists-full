# encoding: utf-8

from uiutil.tk_names import Spinbox as TTKSpinbox
from .base_widget import BaseWidget


class Spinbox(BaseWidget):
    WIDGET = TTKSpinbox
    VAR_TYPE = BaseWidget.int_var
    VAR_PARAM = u'textvariable'
    VAR_IS_OPTIONAL = False

    def __init__(self,
                 *args,
                 **kwargs):
        super(Spinbox, self).__init__(*args,
                                      **kwargs)
