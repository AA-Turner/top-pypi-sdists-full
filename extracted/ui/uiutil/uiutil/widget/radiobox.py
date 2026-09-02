# -*- coding: utf-8 -*-

from collections import OrderedDict
import logging_helper
from uiutil.helper.introspection import calling_base_frame
from uiutil.tk_names import EW, NORMAL, DISABLED
from ..frame.label import BaseLabelFrame
from ..helper.arguments import pop_kwarg, pop_mandatory_kwarg, raise_on_positional_args, get_grid_kwargs
from ..mixin import VarMixIn, ObservableMixIn, WidgetMixIn

logging = logging_helper.setup_logging()


class RadioBox(VarMixIn,
               WidgetMixIn,
               ObservableMixIn):
    # TODO: Add max_rows/max_columns, same behaviour as SwitchBox

    Radiobutton = u"TRadiobutton"  # TODO: Figure out how to add to radiobutton. Need a new widget?

    def __init__(self,
                 # title,
                 # frame=None,
                 # options=None,
                 # command=None,
                 # option_parameters=None,
                 # link=None,
                 # width=None,
                 # sort=True,
                 # take_focus=None,
                 # max_columns=None,
                 # max_rows=None,
                 *args,
                 **kwargs):
        """
        There's small leap to make with labels versus objects.
        Objects can be anything hashable, which the option is associated with
        and the labels are the strings displayed. If just labels are supplied,
        the labels are used as the associated objects (This is likely to be the
        most common usage).

        Getting the state of a switch uses the associated object as a key,
        not the label (unless they're the same)

        :param title: Text for the label frame
        :param options: A list of option labels or, if the option objects
                        and labels are different, a dictionary:

                                  {"label": <switch object>,
                                   ...
                                   "label": <switch object>}

        :param link: A Persist object (or subclass). A dictionary is stored that 
                     uses the labels as keys. This is because they're strings,
                     which are easier to store than objects

        :param option_parameters: Parameters for the individual radiobuttons, e.g.:

                                  {<radiobutton name>: {"tooltip", "Switch for the thing"},
                                    ...
                                   <radiobutton name>: {"tooltip", "Switch for another thing"}}
        :param width: 
        :param args: invalid. positional args are poison in BaseWidget!
        :param kwargs:
        """

        self.initialising = True

        raise_on_positional_args(self, args)
        frame = pop_kwarg(kwargs, u'frame', calling_base_frame())
        title = pop_mandatory_kwarg(kwargs, u'title')
        options = pop_mandatory_kwarg(kwargs, u'options')
        option_parameters = pop_kwarg(kwargs, u'option_parameters', {})
        self.command = pop_kwarg(kwargs, u'command')
        self.link = pop_kwarg(kwargs, u'link')
        width = pop_kwarg(kwargs, u'width')
        sort = pop_kwarg(kwargs, u'sort', True)
        take_focus = pop_kwarg(kwargs, u'take_focus')
        max_rows = pop_kwarg(kwargs, u'max_rows')
        max_columns = pop_kwarg(kwargs, u'max_columns')

        grid_kwargs = get_grid_kwargs(frame=frame,
                                      **kwargs)

        # All other kwargs are discarded.

        super(RadioBox, self).__init__(*args, **kwargs)

        # Setup a containing frame
        self.containing_frame = BaseLabelFrame(frame)

        self.containing_frame._set_title(title=title)

        # Set up object to label mapping...

        if not isinstance(options, dict):
            # Only label labels, so make a dictionary
            # using those labels as the objects
            temp = OrderedDict()

            for option in options:
                # key=label: value=label (labels and objects are the same)
                temp[option] = option

            options = temp

        if sort:
            options = OrderedDict(sorted(options.items(),
                                         key=lambda t: t[0]))
        self.options = options
        self.radiobuttons = {}

        self._var = self.string_var(link=self.link,
                                    value=None if self.link else options.keys()[0])
        if width:
            minimum_width_for_labels = max([len(option) for option in options]) + 1
            if width < minimum_width_for_labels:
                width = minimum_width_for_labels

        if max_columns:
            # Respect max_columns, but allow expansion downwards (ignores max rows)
            if max_rows:
                logging.warning(u"max_rows ignored. Respecting max_columns")
            max_rows = int(len(options)/max_columns) + (1 if len(options) % max_columns else 0) - 1

        elif max_rows:
            # Respect max_rows, but allow expansion rightwards (ignores max columns)
            max_rows -= 1

        else:
            # defaults to vertical layout
            max_rows = len(options) - 1

        for label, option_object in iter(options.items()):

            option_params = option_parameters.get(label, {})

            if take_focus is not None and u'takefocus' not in option_params:
                option_params.update({u'takefocus': take_focus})

            self.radiobuttons[label] = self.containing_frame.radiobutton(
                                           text=label,
                                           variable=self._var,
                                           value=label,
                                           state=NORMAL,
                                           command=self._state_change,
                                           width=width,
                                           sticky=EW,
                                           **option_params)

            if self.containing_frame.row.current == max_rows:
                self.containing_frame.column.next()
                self.containing_frame.row.start()
            else:
                self.containing_frame.row.next()

        self.containing_frame.grid(**grid_kwargs)

    def _state_change(self,
                      _=None):
        if self.link:
            self.link.value = self.value

        if self.command:
            self.command()

        self.notify_observers()

    def key(self,
            option=None):
        """
        Use this to find the key/label associated with an object

        :param option: The option object/value of a radio button
        :return: the key/label
        """
        if not option:
            return self.selected
        try:
            return [label for label, option_object in iter(self.options.items()) if option_object == option][0]
        except IndexError as e:
            logging.exception(e)
            raise ValueError(u'Unknown option "{option}" for RadioBox'.format(option=option))

    @property
    def selected(self):
        return self._var.get()

    @property
    def value(self):
        # return the object, not the string value
        return self.options[self.selected]

    @value.setter
    def value(self,
              value):
        if value not in self.options.keys():
            value = self.key(value)
        self._var.set(value)

    def enable(self,
               option=None):
        if option is None:
            for option in self.radiobuttons.values():
                option.config(state=NORMAL)
        else:
            try:
                self.radiobuttons[option].config(state=NORMAL)
            except KeyError:
                key = self.key(option)
                self.radiobuttons[key].config(state=NORMAL)

    def disable(self,
                option=None):
        if option is None:
            for option in self.radiobuttons.values():
                option.config(state=DISABLED)
        else:
            try:
                self.radiobuttons[option].config(state=DISABLED)
            except KeyError:
                key = self.key(option)
                self.radiobuttons[key].config(state=DISABLED)

    def destroy(self):
        self.containing_frame.destroy()
