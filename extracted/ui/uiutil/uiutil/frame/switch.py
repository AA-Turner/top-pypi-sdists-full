# encoding: utf-8

import logging_helper

from tkinter import NORMAL, EW
from collections import OrderedDict
from stateutil.persist import Persist
from ..widget.switch import Switch
from ..frame.label import BaseLabelFrame
logging = logging_helper.setup_logging()


class BaseSwitchFrame(BaseLabelFrame):

    SWITCH_WIDGET = Switch
    DEFAULT_SWITCH_STATE = Switch.ON

    def __init__(self,
                 title,
                 switches,
                 switch_states=None,
                 switch_parameters=None,
                 link=None,
                 width=None,
                 sort=True,
                 *args,
                 **kwargs):
        """
        There's small leap to make with labels versus objects.
        Objects can be anything hashable, which the switch is associated with
        and the labels are the strings displayed. If just labels are supplied,
        the labels are used as the associated objects (This is likely to be the
        most common usage).
        
        Getting the state of a switch uses the associated object as a key,
        not the label (unless they're the same)
        
        :param title: Text for the label frame
        :param switches: A list of switch names or, if the switch objects
                         and labels are different, a dictionary:

                                  {"switch label": <switch object>,
                                   ...
                                   "switch label": <switch object>}

        :param switch_states: Initial switch states, a dictionary:

                                  {<switch object>: <switch state>,
                                    ...
                                   <switch object>: <switch state>}
                                   
        :param link: A Persist object (or subclass). A dictionary is stored that 
                     uses the labels as keys. This is because they're strings,
                     which are easier to store than objects
                     
        :param switch_parameters: Parameters for the individual switches, e.g.:
        
                                  {<switch object>: {"tooltip", "Switch for the thing"},
                                    ...
                                   <switch object>: {"tooltip", "Switch for another thing"}}
        :param width: 
        :param args:
        :param kwargs:
        """

        logging.warning(u'BaseSwitchFrame is deprecated. Use the SwitchBox widget instead')

        super(BaseSwitchFrame, self).__init__(*args, **kwargs)

        self._set_title(title=title)

        if not isinstance(switches, dict):
            # Only label labels, so make a dictionary
            # using those labels as the objects
            temp = OrderedDict()

            for switch in switches:
                # key=label: value=label (labels and objects are the same)
                temp[switch] = switch

            switches = temp

        if sort:
            switches = OrderedDict(sorted(switches.items(),
                                          key=lambda t: t[0]))

        switch_states = {} if switch_states is None else switch_states

        self.switch_states = {switches[key]: value for key, value in iter(switch_states.items())}
        switch_parameters = {} if not switch_parameters else switch_parameters

        self.link = link

        if self.link:
            self.switch_states.update(self.link.get())
            self.link.value = self.switch_states

        self.switches = {}

        for switch_label, switch_object in iter(switches.items()):

            command = (lambda sw=switch_object: self.state_change(sw))

            # kyy into self.switch_states is the label, not the object
            switch_link = Persist(persistent_store=self.switch_states,
                                  key=switch_label,
                                  init=self.switch_states.get(switch_label, self.DEFAULT_SWITCH_STATE))

            switch_params = switch_parameters.get(switch_object, {})
            switch_params[u'sticky'] = switch_params.get(u'sticky', EW)

            self.switches[switch_object] = self.SWITCH_WIDGET(text=switch_label,
                                                              state=NORMAL,
                                                              width=width,
                                                              command=command,
                                                              link=switch_link,
                                                              row=self.row.current,
                                                              column=self.column.start(),
                                                              **switch_params)
            self.row.next()

    def state_change(self,
                     switch):

        if self.switched_on(switch):
            self.switch_on(switch)

        else:
            self.switch_off(switch)

        if self.link:
            self.link.set(self.switch_states)

    def switch_state(self,
                     switch):
        return self.switches[switch].state

    def switched_on(self,
                    switch):
        return self.switches[switch].switched_on

    def switched_off(self,
                     switch):
        return self.switches[switch].switched_off

    def switch_on(self,
                  switch):

        """
        Override this method to take action when the
        state of a switch changes to on if the actions needs
        to be at the switch array level, otherwise override
        switch_on in the switch_widget
        """

        self.switches[switch].switch_on()

    def switch_off(self,
                   switch):

        """
        Override this method to take action when the
        state of a switch changes to off if the actions needs
        to be at the switch array level, otherwise override
        switch_off in the switch_widget
        """

        self.switches[switch].switch_off()

    @property
    def get_switched_on_list(self):
        return [switch for switch in self.switches if self.switched_on(switch)]

    def enable_all(self):
        for switch in self.switches.values():
            switch.enable()

    def disable_all(self):
        for switch in self.switches.values():
            switch.disable()
