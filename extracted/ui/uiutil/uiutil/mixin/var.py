# encoding: utf-8

from uiutil.tk_names import StringVar, IntVar, BooleanVar
from future.builtins import str


class VarMixIn(object):

    def __init__(self,
                 *args,
                 **kwargs):
        super(VarMixIn, self).__init__()

    def _safe_get(self):
        try:
            return self._var.get()
        except ValueError as ve:
            message = str(ve)
            if u'invalid literal' in message:
                # Handle ValueError: invalid literal for int() with base 10: ''
                # to prevent unnecessary tk errors.
                return u"'".join(message.split(u"'")[1:-1])
            else:
                return u''

    def _make_var(self,
                  var,
                  name=u'',
                  value=None,
                  trace=None,
                  link=None):

        """
        Call with either value, value + trace or link. If these are mixed,
        link is used.
        :param var: This is the Var type, e.g. StringVar
        :param value: value to set the Var object to
        :param trace: Add a trace to the Var for triggering on change.
                      this is just the function to call
        :param link: link an object that has a get and set method
        :return:
        """

        if link and (value or trace):
            raise ValueError(u"If 'var' is called with 'link' set, "
                             u"don't also set value or trace. "
                             u"If you need both link and trace, "
                             u"register as an observer with the "
                             u"linked object and implement notify.")
        if link:
            # Initial value taken from the linked object
            value = link.get()

        if name.startswith(u'__'):
            raise ValueError(u"Private names (beginning with '__') aren't"
                             u"allowed. Mangling can't be done at runtime.")

        var = var() if value is None else var(value=value)

        if name:
            setattr(self,
                    name,
                    var)
            setattr(var,
                    u'name',
                    name)

        if link:
            # set the linked object value to the Var's value
            var.trace(u"w",
                      lambda name, index, mode: link.set(self._safe_get()))

        elif trace is not None:
            var.trace(u"w",
                      lambda name, index, mode: trace())

        return var

    def string_var(self,
                   *args,
                   **kwargs):

        """See GUIHelpers.var for *args/**kwargs"""

        return self._make_var(var=StringVar,
                              *args,
                              **kwargs)

    def int_var(self,
                *args,
                **kwargs):

        """See GUIHelpers.var for *args/**kwargs"""

        return self._make_var(var=IntVar,
                              *args,
                              **kwargs)

    def boolean_var(self,
                    *args,
                    **kwargs):

        """See GUIHelpers.var for *args/**kwargs"""

        return self._make_var(var=BooleanVar,
                              *args,
                              **kwargs)
