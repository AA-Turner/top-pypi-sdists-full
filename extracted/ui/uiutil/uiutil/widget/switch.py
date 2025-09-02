# encoding: utf-8

from uiutil.tk_names import ttk
from stateutil.switch import Switch as _Switch
from stateutil.persist import Persist
from classutils.observer import Observer
from ..helper.arguments import pop_kwarg, raise_on_positional_args
from .base_widget import BaseWidget


class Switch(BaseWidget,
             _Switch,
             Observer):

    WIDGET = ttk.Checkbutton
    STYLE = u"TCheckbutton"
    VAR_TYPE = BaseWidget.boolean_var
    VAR_PARAM = u'variable'
    VAR_IS_OPTIONAL = False

    def __init__(self,
                 # switch_state=_Switch.ON,
                 # link=None,
                 # trace=None,
                 # take_focus=None,
                 *args,
                 **kwargs):
        """
        Note: Link and trace are bit strange in this widget.
        A link is always used, even if one is not provided.
        This is because we want to observe it and use
        notifications to update the state (ON or OFF), in order to
        have access ot the _Switch methods.
         
        Trace is still available, calling the traced function
        on notification of the link changing
        
        :param switch_state: Switch.ON or Switch.Off
        :param link: a Persist object
        :param trace: function to call on value change
        :param take_focus: used to set takefocus in the kwargs.
                           Does not override takefocus if already
                           in kwargs.
        :param args: invalid. positional args are poison in BaseWidget!
        :param kwargs: keyword arguments to the underlying widget
        """
        self.initialising = True

        raise_on_positional_args(self, args)
        switch_state = pop_kwarg(kwargs, u'switch_state', self.ON)
        link = pop_kwarg(kwargs, u'link')
        trace = pop_kwarg(kwargs, u'trace')
        take_focus = pop_kwarg(kwargs, u'take_focus')

        if switch_state not in [self.ON, self.OFF]:
            raise ValueError(u'Switch state should be one of Switch.ON or Switch.OFF! ({v}).'.format(v=switch_state))

        self.link = link
        self.trace = trace

        if not self.link:
            self.persistent_store = {}
            self.link = Persist(persistent_store=self.persistent_store,
                                key=u'dummy',
                                init=switch_state)

        if take_focus is not None and u'takefocus' not in kwargs:
             kwargs.update({u'takefocus': take_focus})

        super(Switch, self).__init__(link=self.link,
                                     onvalue=self.ON,
                                     offvalue=self.OFF,
                                     **kwargs)

        self.link.register_observer(self)

        del self.initialising  # Need this to prevent notifications being processed before
        #                      # the widget has finished initialising
        self.__update_state()

    def notification(self,
                     notifier,
                     **params):

        try:
            self.initialising
            return
        except AttributeError:
            pass

        if notifier == self.link:
            self.__update_state()
            if self.trace:
                self.trace()

    def __update_state(self):
        self._state = self.value

    def _switch_on_action(self):
        # Synchronise self.state & self._var as with trace above
        self.value = self._state

    def _switch_off_action(self):
        # Synchronise self.state & self._var as with trace above
        self.value = self._state
