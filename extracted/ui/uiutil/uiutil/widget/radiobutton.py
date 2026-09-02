# -*- coding: utf-8 -*-


from uiutil.helper.introspection import calling_base_frame
from uiutil.tk_names import NORMAL, W
from ..helper.arguments import pop_kwarg, pop_mandatory_kwarg, raise_on_positional_args, get_grid_kwargs
from ..mixin import VarMixIn, ObservableMixIn, WidgetMixIn


class RadioButton(VarMixIn,
                  WidgetMixIn,
                  ObservableMixIn):

    VALUE_IS_MANDATORY = False

    def __init__(self,
                 # frame=None,
                 # text=None,
                 # value=None,
                 # command=None,
                 # link=None,
                 # associate=None,
                 # int_values=False,
                 *args,
                 **kwargs):
        """
        Instantiate multiple times to set up radio buttons in a frame
        where RadioBox is inappropriate.

        All RadioButtons:

            :param text: Text for the label
            :param value: A value associated with this selection.
                          Defaults to the same value as 'text'
                          Must provide if text is None.
            :param args: invalid. positional args are poison in BaseWidget!
            :param kwargs:

        First RadioButton:

            :param link: A Persist object (or subclass).
            :param command: Command to run when a radio button is selected
            :param associate: If there are multiple radiobutton
                              sets in a single frame, set to True
                              for additional radio button sets.

        Subsequent RadioButtons:

            :param associate: Pass in the first radio button widget
                              if using multiple radiobutton sets in
                              a single frame for additional radio
                              button sets.
        """

        self.initialising = True

        raise_on_positional_args(self, args)
        frame = pop_kwarg(kwargs, u'frame', calling_base_frame())
        associate = pop_kwarg(kwargs, u'associate')
        command = pop_kwarg(kwargs, u'command')
        self.link = pop_kwarg(kwargs, u'link')
        state = pop_kwarg(kwargs, u'state', NORMAL)
        text = pop_kwarg(kwargs, u'text')
        if self.VALUE_IS_MANDATORY:
            value = pop_mandatory_kwarg(kwargs, u'value')
        else:
            value = pop_kwarg(kwargs, u'value', text)
        kwargs[u'sticky'] = pop_kwarg(kwargs, u'sticky', W)

        if value is None:
            raise ValueError(u'RadioButton must be supplied with text or value parameter')

        # All other kwargs are discarded.

        super(RadioButton, self).__init__(*args, **kwargs)

        if associate is True:
            #
            self._var = self.string_var(link=self.link,
                                        value=None if self.link else value)
            self.command = command

        elif associate:
            self._var = associate._var
            self.command = associate.command

        else:
            # Associate with RadioButtons in the same frame
            if not hasattr(frame, "_radiobutton_var"):
                frame._radiobutton_var = self.string_var(link=self.link,
                                                         value=None if self.link else value)
                frame._radiobutton_command = command

            self._var = frame._radiobutton_var
            self.command = frame._radiobutton_command

        self.radiobutton = frame.radiobutton(text=text,
                                             variable=self._var,
                                             value=value,
                                             state=state,
                                             command=self._state_change,
                                             **kwargs)

    def _state_change(self,
                      _=None):
        if self.link:
            self.link.value = self.value

        if self.command:
            self.command()

        self.notify_observers()

    @staticmethod
    def conversion(value):
        return value

    @property
    def value(self):
        return self.conversion(self._var.get())

    @value.setter
    def value(self,
              value):
        self._var.set(str(value))


class IntRadioButton(RadioButton):

    VALUE_IS_MANDATORY = True

    @staticmethod
    def conversion(value):
        return int(value)
