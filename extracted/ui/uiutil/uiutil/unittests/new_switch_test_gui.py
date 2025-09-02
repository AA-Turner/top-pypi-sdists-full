# encoding: utf-8

import logging_helper

from uiutil.tk_names import NORMAL, EW, HORIZONTAL

from uiutil import BaseFrame, Label, standalone, Position
from uiutil import NewSwitch as Switch
from stateutil import Persist

logging = logging_helper.setup_logging()


class TestNewSwitch(BaseFrame):

    AUTO_POSITION = HORIZONTAL

    def __init__(self,
                 *args,
                 **kwargs):

        BaseFrame.__init__(self, *args, **kwargs)

        self.grid(sticky=EW)

        self.switch_1 = Switch(text='test',
                               trace=self.trace_fn,  # No link
                               switch_state=Switch.ON)

        self.label_1 = Label(value=("Value:{state}"
                                    .format(state=self.switch_1.switched_on)))

        self.persistent_store = {}
        self.switch_2_persist = Persist(persistent_store=self.persistent_store,
                                        key=u"switch_2",
                                        init=Switch.OFF)

        self.switch_2 = Switch(text='two',
                               link=self.switch_2_persist,  # Persist object
                               row=Position.NEXT,
                               column=Position.START)

        self.label_2 = Label(value=("Value:{state}"
                                    .format(state=self.switch_2.switched_on)))

        self.observe(self.switch_2)

        self.switch_3 = Switch(text='three',  # No link or trace. Let the widget set up the persist object
                               row=Position.NEXT,
                               column=Position.START)

        self.label_3 = Label(value=("Value:{state}"
                                    .format(state=self.switch_3.switched_on)))

        self.observe(self.switch_3)

        self.nice_grid()

    def notification(self,
                     notifier,
                     **kwargs):
        logging.info('>>> {notifier}{kwargs}'.format(notifier=notifier, kwargs=kwargs))
        if notifier is self.switch_2:
            self.label_2.value = "Value:{state}".format(state=self.switch_2.switched_on)

        elif notifier is self.switch_3:
            self.label_3.value = "Value:{state}".format(state=self.switch_3.switched_on)

    def trace_fn(self):
        print(u'in switch update')
        self.label_1.value = "Value:{state}".format(state=self.switch_1.switched_on)


if __name__ == u'__main__':
    standalone(TestNewSwitch)
