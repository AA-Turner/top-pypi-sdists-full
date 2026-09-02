# encoding: utf-8

from collections import OrderedDict
from logging_helper import setup_logging
from stateutil.persist import Persist

from uiutil.helper.introspection import calling_base_frame
from uiutil.tk_names import NORMAL, EW, GROOVE
from .new_switch import Switch
from ..frame.frame import BaseFrame
from ..frame.label import BaseLabelFrame
from ..frame.scroll import BaseScrollFrame
from ..helper.arguments import pop_kwarg, pop_mandatory_kwarg, raise_on_positional_args, get_grid_kwargs
from ..mixin import WidgetMixIn

logging = setup_logging()


class SwitchBox(WidgetMixIn):

    SWITCH_WIDGET = Switch
    ON = SWITCH_WIDGET.ON
    OFF = SWITCH_WIDGET.OFF
    DEFAULT_SWITCH_STATE = SWITCH_WIDGET.ON

    def __init__(self,
                 # title,
                 # switches,
                 # frame=None,
                 # switch_states=None,
                 # default_switch_state=None,
                 # switch_parameters=None,
                 # link=None,
                 # command=None,
                 # width=None,
                 # sort=True,
                 # take_focus=None,
                 # max_columns=None,
                 # max_rows=None,
                 scroll=False,
                 *args,
                 **kwargs):
        """
        There's small leap to make with labels versus objects.
        Objects can be any object, which the switch is associated with
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

        :param switch_states: Dictionary of initial switch states, these values
                              also override persisted states. Not all objects
                              need to be in this list, so if you always want
                              to set a subset of the switches, this is where
                              you do it. Dict looks like this:

                                  {<switch object>: <switch state>,
                                    ...
                                   <switch object>: <switch state>}
                                   
        :param link: A Persist object (or subclass). A dictionary is stored that 
                     uses the labels as keys. This is because they're strings,
                     which are easier to store than objects
                     
        :param switch_parameters: Parameters for the individual switches, e.g.:
        
                                  {<switch label>: {"tooltip": "Switch for the thing"},
                                    ...
                                   <switch label>: {"tooltip": "Switch for another thing"}}

        :param width: Width of all labels.
        :param sort: Sorts switches by label if True
        :param max_rows: maximum number of rows used when laying out the switches.
        :param max_columns: maximum number of columns used when laying out the switches.
        :param args: invalid. positional args are poison in BaseWidget!
        :param kwargs:
        """
        raise_on_positional_args(self, args)
        frame = pop_kwarg(kwargs, u'frame', calling_base_frame())
        title = pop_kwarg(kwargs, u'title')
        switches = pop_mandatory_kwarg(kwargs, u'switches')
        switch_states = pop_kwarg(kwargs, u'switch_states', {})
        default_switch_state = pop_kwarg(kwargs, u'default_switch_state', self.DEFAULT_SWITCH_STATE)
        switch_parameters = pop_kwarg(kwargs, u'switch_parameters', {})
        self.link = pop_kwarg(kwargs, u'link')
        self._command = pop_kwarg(kwargs, u'command')
        width = pop_kwarg(kwargs, u'width')
        sort = pop_kwarg(kwargs, u'sort', True)
        take_focus = pop_kwarg(kwargs, u'take_focus')
        max_rows = pop_kwarg(kwargs, u'max_rows')
        max_columns = pop_kwarg(kwargs, u'max_columns')
        # TODO: Fix. Specifying max_columns instead of max_rows does not work!
        padx = pop_kwarg(kwargs, u'padx')
        pady = pop_kwarg(kwargs, u'padx')

        grid_kwargs = get_grid_kwargs(frame=frame,
                                      **kwargs)

        # All other kwargs are discarded.

        super(SwitchBox, self).__init__(*args, **kwargs)

        # Setup a containing frame
        if title is not None:
            self.containing_frame = BaseLabelFrame(parent=frame,
                                                   title=title,
                                                   padx=padx,
                                                   pady=pady)

        elif scroll:
            scroll_width = kwargs.get(u'width') if u'width' in kwargs else 0
            scroll_height = kwargs.get(u'height') if u'height' in kwargs else 0

            self.containing_frame = BaseScrollFrame(parent=frame,
                                                    title=title,
                                                    padx=padx,
                                                    pady=pady,
                                                    hbar=False,
                                                    canvas_width=scroll_width,
                                                    canvas_height=scroll_height)

        else:
            self.containing_frame = BaseFrame(parent=frame,
                                              padx=padx,
                                              pady=pady,
                                              borderwidth=1,
                                              relief=GROOVE)

        # Set up object to label mapping...

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
        self.switch_objects = switches
        self.switch_states = switch_states.copy()

        if self.link:
            # Retrieve persisted states (link), but then override with any
            # supplied states, then write these back to the linked store.
            persisted_states = self.link.value
            try:
                persisted_states.update(self.switch_states)
                self.switch_states = persisted_states
            except AttributeError:
                pass
            self.link.value = self.switch_states

        self.switch_widgets = OrderedDict()

        if width:
            minimum_width_for_labels = max([len(switch_label) for switch_label in switches]) + 1
            if width < minimum_width_for_labels:
                width = minimum_width_for_labels

        if max_columns:
            # Respect max_columns, but allow expansion downwards (ignores max rows)
            if max_rows:
                logging.warning(u"max_rows ignored. Respecting max_columns")
            max_rows = int(len(switches)/max_columns) + (1 if len(switches) % max_columns else 0) - 1

        elif max_rows:
            # Respect max_rows, but allow expansion rightwards (ignores max columns)
            max_rows -= 1

        else:
            # defaults to vertical layout
            max_rows = len(switches) - 1

        for switch_label in iter(switches.keys()):

            command = (lambda sw=switch_label: self.state_change(sw))

            # key into self.switch_states is the label, not the object
            switch_link = Persist(persistent_store=self.switch_states,
                                  key=switch_label,
                                  init=self.switch_states.get(switch_label, default_switch_state))

            switch_params = switch_parameters.get(switch_label, {})
            switch_params[u'sticky'] = switch_params.get(u'sticky', EW)

            self.switch_widgets[switch_label] = self.SWITCH_WIDGET(frame=self.containing_frame,
                                                                   text=switch_label,
                                                                   state=NORMAL,
                                                                   width=width,
                                                                   command=command,
                                                                   link=switch_link,
                                                                   take_focus=take_focus,
                                                                   **switch_params)

            if self.containing_frame.row.current == max_rows:
                self.containing_frame.column.next()
                self.containing_frame.row.start()
            else:
                self.containing_frame.row.next()

        self.containing_frame.grid(**grid_kwargs)

    def state_change(self,
                     switch):

        if self.switched_on(switch):
            self.switch_on(switch)

        else:
            self.switch_off(switch)

        if self.link:
            self.link.set(self.switch_states)

        if self._command:
            self._command(switch)

    def switch_state(self,
                     switch):
        return self.switch_widgets[switch].state

    def switched_on(self,
                    switch):
        return self.switch_widgets[switch].switched_on

    def switched_off(self,
                     switch):
        return self.switch_widgets[switch].switched_off

    def switch_on(self,
                  switch):

        """
        Override this method to take action when the
        state of a switch changes to on if the actions needs
        to be at the switch array level, otherwise override
        switch_on in the switch_widget
        """

        self.switch_widgets[switch].switch_on()

    def switch_off(self,
                   switch):

        """
        Override this method to take action when the
        state of a switch changes to off if the actions needs
        to be at the switch array level, otherwise override
        switch_off in the switch_widget
        """

        self.switch_widgets[switch].switch_off()

    @property
    def all_switched_on(self):
        return [self.value(switch) for switch in self.switch_widgets if self.switched_on(switch)]

    @property
    def all_switched_off(self):
        return [self.value(switch) for switch in self.switch_widgets if self.switched_off(switch)]

    @property
    def all_states(self):
        return {switch: self.switch_state(switch) for switch in self.switch_widgets}

    def enable(self):
        for switch in self.switch_widgets.values():
            switch.enable()

    def disable(self):
        for switch in self.switch_widgets.values():
            switch.disable()

    def key(self,
            switch):
        if switch in self.switch_objects.keys():
            return switch

        try:
            return [label for label, switch_object in iter(self.switch_objects.items()) if switch_object == switch][0]
        except IndexError as e:
            logging.exception(e)
            raise ValueError(u'Unknown switch "{switch}" for RadioBox'.format(switch=switch))

    def value(self,
              switch):
        return self.switch_objects[self.key(switch)]

    def destroy(self):
        self.containing_frame.destroy()
