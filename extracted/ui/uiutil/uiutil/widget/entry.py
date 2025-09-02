# -*- coding: utf-8 -*-

from uiutil.tk_names import ttk
from .base_widget import BaseWidget
from ..helper.arguments import pop_kwarg, raise_on_positional_args


class TextEntry(BaseWidget):
    WIDGET = ttk.Entry
    STYLE = u"TEntry"
    VAR_TYPE = BaseWidget.string_var
    VAR_PARAM = u'textvariable'
    VAR_IS_OPTIONAL = False

    def __init__(self,
                 *args,
                 **kwargs):
        super(TextEntry, self).__init__(*args, **kwargs)


class IntEntry(BaseWidget):
    WIDGET = ttk.Entry
    VAR_TYPE = BaseWidget.int_var
    VAR_PARAM = u'textvariable'
    VAR_IS_OPTIONAL = False

    def __init__(self,
                 # min,
                 # max,
                 *args,
                 **kwargs):
        raise_on_positional_args(self, args)
        self.min = pop_kwarg(kwargs, u'min', None)
        self.max = pop_kwarg(kwargs, u'max', None)

        super(IntEntry, self).__init__(allow_invalid_values=False,
                                       *args,
                                       **kwargs)

    def valid(self,
              value=None):
        if value is None:
            value = self.value
        try:
            int_value = int(value)
            value = str(value)
            does_not_have_spaces = len(value) == len(value.strip())
            inside_lower_limit = self.min <= int_value if self.min is not None else True
            inside_upper_limit = int_value <= self.max if self.max is not None else True
            return inside_lower_limit and inside_upper_limit and does_not_have_spaces
        except ValueError:
            return value == u'-' and (self.min is None or self.min < 0)

    def permit_invalid_value(self,
                             value):
        try:
            int_value = int(value)
            does_not_have_spaces = len(value) == len(value.strip())
            outside_lower_limit = self.min > int_value if self.min is not None else False
            outside_upper_limit = self.max < int_value if self.max is not None else False
            return (outside_lower_limit or outside_upper_limit) and does_not_have_spaces
        except ValueError:
            lower_limit_is_negative = self.min < 0 if self.min is not None else False
            return value == u'-' and lower_limit_is_negative


class PINEntry(TextEntry):

    DIGITS = u'0123456789'

    def __init__(self,
                 # digits=4,
                 *args,
                 **kwargs):
        raise_on_positional_args(self, args)
        self.digits = pop_kwarg(kwargs, u'digits', 4)
        super(TextEntry, self).__init__(*args, **kwargs)

    def valid(self,
              value=None):
        value = self.value if value is None else value
        if len(value) != self.digits:
            return False
        return len(value) == len([d for d in value if d in self.DIGITS])

    def permit_invalid_value(self,
                             value):
        # This allows typing followed by delete
        # rather than forcing the user to delete
        # first to make room
        return len(value) == len([d for d in value if d in self.DIGITS])
