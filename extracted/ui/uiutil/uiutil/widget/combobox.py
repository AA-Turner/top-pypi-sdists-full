# -*- coding: utf-8 -*-

import logging_helper
from warnings import warn
from uiutil.tk_names import ttk, READONLY, NORMAL
from .base_widget import BaseWidget
from ..helper.arguments import pop_kwarg
from collections import OrderedDict
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

logging = logging_helper.setup_logging()

try:
    basestring
except:
    basestring = str

def is_str(s):
    return isinstance(s, str)


class Combobox(BaseWidget):
    WIDGET = ttk.Combobox
    STYLE = "TCombobox"
    VAR_TYPE = BaseWidget.string_var
    VAR_PARAM = 'textvariable'
    VAR_IS_OPTIONAL = False

    EDITABLE = 'editable'
    SORT = 'sort'
    VALUES = 'values'

    @staticmethod
    def sorted_except_first_value(values):
        return values[:1] + sorted(values[1:])

    def __init__(self,
                 # editable=False,
                 # sort=False,
                 *args,
                 **kwargs):
        """
        :param editable: Boolean
                         True: Can type into Combobox (enabled state is NORMAL)
                         False: Can't type into combobox (enabled state is READONLY)
        :param sort: False: Does not sort
                     True: Sorts by key
                     Func: Uses the function to sort the keys
                           e.g. Combobox.sorted_except_first_value
        :param args:
        :param kwargs:
        """

        enabled_state = pop_kwarg(kwargs, 'enabled_state')
        if enabled_state is not None:
            warn(u'"enabled_state" parameter into Combobox is deprecated. Use "editable" instead.',
                 category=DeprecationWarning)
            kwargs[self.EDITABLE] = enabled_state is NORMAL

        self.editable = pop_kwarg(kwargs, "editable", False)
        kwargs['enabled_state'] = (NORMAL if self.editable else READONLY)
        kwargs['state'] = kwargs.get('state', kwargs['enabled_state'])
        values = kwargs.get(self.VALUES)
        value = kwargs.get('value')

        self.sort = pop_kwarg(kwargs, self.SORT, False)
        self.store_value_map(values)
        kwargs[self.VALUES] = self.sorted_keys()

        super(Combobox, self).__init__(*args, **kwargs)

        if not value and self.value not in self.value_map.values():
            try:
                self.value = self.sorted_keys()[0]
            except IndexError:
                pass

    def store_value_map(self,
                        values):
        if not values:
            values = OrderedDict()  # No values yet
        if not isinstance(values, Mapping):
            values = OrderedDict([(value, value) for value in values])
        self.value_map = values

    def sorted_keys(self):
        keys = list(self.value_map.keys())
        if self.sort is True:
            keys.sort()
        elif self.sort:
            keys = self.sort(keys)
        return keys

    def _lookup_key_by_key_or_value(self,
                                    key_or_value):

        # Match to the key
        if key_or_value in self.value_map:
            return key_or_value

        # Associated value may have been supplied. Return the key
        for key, value in iter(self.value_map.items()):
            if value == key_or_value:
                return key

        raise LookupError(u'Key or value: {key_or_value} not found'
                          .format(key_or_value))

    def add_key_value(self,
                      key_value):

        # Not found - new value
        try:
            if is_str(key_value):
                raise TypeError("Don't treat string as iterable")  # Avoids 2 chars string unpacking to key, value
            key, value = key_value  # (key, value) supplied
        except (TypeError, ValueError):
            key = value = key_value

        self.value_map[key] = value
        self.values = list(self.values) + [key]

        return key

    @property
    def value(self):
        selection = self._var.get()
        try:
            return self.value_map[selection]
        except AttributeError:
            self.raise_missing_variable_error()
        except KeyError:
            pass
        return selection

    @value.setter
    def value(self,
              key_or_value):
        try:
            key = self._lookup_key_by_key_or_value(key_or_value=key_or_value)
        except LookupError:
            key = self.add_key_value(key_or_value)
        try:
            self._var.set(key)
        except AttributeError:
            self.raise_missing_variable_error()

    @property
    def values(self):
        # When fetching all values, returns the keys
        return self.widget[self.VALUES]

    @values.setter
    def values(self,
               values):
        self.store_value_map(values)
        self.config(values=self.sorted_keys())

    @staticmethod
    def int_sort(string_values):
        return sorted(string_values, key=lambda string_value: int(string_value))
