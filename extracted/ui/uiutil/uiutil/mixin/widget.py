# encoding: utf-8

from uiutil.tk_names import ttk, Listbox, HORIZONTAL, EW
from ..widget.tooltip import ToolTip
from ..helper.event import bind_events
from ..ttk_override.ttk_spinbox import Spinbox
from ..helper.arguments import get_widget_kwargs, get_grid_kwargs


class WidgetMixIn(object):

    def __init__(self,
                 *args,
                 **kwargs):
        super(WidgetMixIn, self).__init__()

    def add_widget_and_position(self,
                                widget,
                                name=u'',
                                frame=None,
                                tooltip=None,
                                **kwargs):
        """
        Adds a widget, sets its position and adds an optional tooltip

        :param widget:
        :param name:
        :param frame:
        :param tooltip: tooltip text/function or a parameter dictionary into
                        Tooltip
        :return:
        """

        frame = frame if frame else self

        grid_kwargs = get_grid_kwargs(frame=frame,
                                      **kwargs)

        widget_kwargs = get_widget_kwargs(**kwargs)

        if name.startswith(u'__'):
            raise ValueError(u"Private names (beginning with '__') aren't"
                             u"allowed. Mangling can't be done at runtime.")

        widget_object = widget(frame,
                               **widget_kwargs)

        widget_object.grid(**grid_kwargs)

        # TODO: Could auto bump position here, based on columnspan/rowspan
        #       Maybe use a hint for fill direction, default to horizontal

        frame.position_for_next_widget(**grid_kwargs)

        if name:
            setattr(self,
                    name,
                    widget_object)
            setattr(widget_object,
                    u'name',
                    name)

        tooltip = self.add_tooltip_to_widget(tooltip=tooltip,
                                             widget_object=widget_object,
                                             name=name)
        if tooltip is not None:
            return widget_object, tooltip
        else:
            return widget_object  # TODO: Number of args returned is not consistent!  fix this!

    def add_tooltip_to_widget(self,
                              tooltip,
                              widget_object,
                              name):
        if tooltip is not None:
            if not isinstance(tooltip, dict):
                tooltip = {u'text': tooltip}

            tooltip = ToolTip(widget=widget_object,
                              **tooltip)
            if name:
                setattr(self,
                        u'{name}_tooltip'.format(name=name),
                        tooltip)

            return tooltip

    def label(self,
              **kwargs):
        """
        Adds and positions a label
        """

        return self.add_widget_and_position(widget=ttk.Label,
                                            **kwargs)

    def button(self,
               **kwargs):
        """
        Adds and positions a button
        """

        return self.add_widget_and_position(widget=ttk.Button,
                                            **kwargs)

    def radio_button(self,
                     **kwargs):
        """
        Adds and positions a radio button
        """

        return self.add_widget_and_position(widget=ttk.Radiobutton,
                                            **kwargs)

    def separator(self,
                  **kwargs):
        """
        Adds and positions a separator line
        """

        return self.add_widget_and_position(widget=ttk.Separator,
                                            **kwargs)

    def horizontal_separator(self,
                             **kwargs):
        """
        Adds and positions a horizontal separator line
        
        Uses some default parameters if not supplied so the actual call doesn't need them
        """
        defaults = {'orient': HORIZONTAL,
                    'sticky': EW,
                    'padx':   5,
                    'pady':   5}

        for default, default_value in iter(defaults.items()):
            kwargs[default] = kwargs.get(default, default_value)

        if 'row' not in kwargs:
            kwargs['row'] = self.row.next()

        if 'column' not in kwargs:
            kwargs['column'] = self.column.start()

        return self.add_widget_and_position(widget=ttk.Separator,
                                            **kwargs)

    def combobox(self,
                 **kwargs):

        """
        Adds and positions a combobox
        """

        return self.add_widget_and_position(widget=ttk.Combobox,
                                            **kwargs)

    def entry(self,
              **kwargs):

        """
        Adds and positions a Entry field
        """

        return self.add_widget_and_position(widget=ttk.Entry,
                                            **kwargs)

    def spinbox(self,
                **kwargs):

        """
        Adds and positions a spinbox
        """

        return self.add_widget_and_position(widget=Spinbox,
                                            **kwargs)

    def checkbutton(self,
                    **kwargs):
        """
        Adds and positions a checkbutton
        """
        return self.add_widget_and_position(widget=ttk.Checkbutton,
                                            **kwargs)

    def checkbox(self,
                 **kwargs):

        """
        Adds and positions a checkbutton
        """

        return self.checkbutton(**kwargs)

    def radiobutton(self,
                    **kwargs):

        """
        Adds and positions a radiobutton
        """

        return self.add_widget_and_position(widget=ttk.Radiobutton,
                                            **kwargs)

    def progressbar(self,
                    **kwargs):

        """
        Adds and positions a progress bar
        """

        return self.add_widget_and_position(widget=ttk.Progressbar,
                                            **kwargs)

    def listbox(self,
                **kwargs):

        """
        Adds and positions a listbox
        """

        return self.add_widget_and_position(widget=Listbox,
                                            **kwargs)

    def blank_row(self,
                  **kwargs):
        self.label(text=u'',
                   row=self.row.next(),
                   column=self.column.start(),
                   **kwargs)

    def blank_column(self,
                     expanding=False):
        self.label(text=u'',
                   row=self.row.current,
                   column=self.column.next())

        if expanding:
            self.columnconfigure(self.column.current,
                                 weight=1)

    @staticmethod
    def bind_events(*args,
                    **kwargs):
        bind_events(*args, **kwargs)
