# encoding: utf-8

import copy
import logging_helper
from future.utils import iteritems
from fdutil.dict_tools import sort_dict
from configurationutil import Configuration
from ..helper.dynamic_kwarg import handle_kwarg, LINE_KWARG_ITER_NAME, LINE_KWARG_ITER_VALUE
from ..helper.dynamic_variable import handle_variable

logging = logging_helper.setup_logging()

# General keys
EXPANDING_COLUMNS = u'expand_col'
EXPANDING_ROWS = u'expand_row'

# Frame Keys
ROWS_FIRST = u'rows_first'
WIDGET_GRID = u'widget_grid'
ITEM_KEY = u'item_key'
ITERABLE_LINE = u'iterable'
ITERABLE_SORTED = u'sort_iterable'
ITERABLE_FORCE_LIST = u'force_iter_list'

# Line keys
WIDGET_GRID_LINE = u'line'
LINE_DEFAULT = u'default'

# Widget Keys
WIDGET_NAME = u'name'
WIDGET_TYPE = u'type'
WIDGET_KWARGS = u'kwargs'
WIDGET_BINDING = u'binding'
WIDGET_VAR = u'var'
WIDGET_VAR_SETTINGS = u'var_settings'

BIND_FUNCTION = u'function'
BIND_EVENTS = u'events'

# Internal line kwarg keys
_LINE_KWARG_LINE = u'line'
_LINE_KWARG_ROW = u'row'
_LINE_KWARG_COLUMN = u'column'
_LINE_KWARG_DEFAULT = u'default'


class DynamicBaseFrame(object):

    def __init__(self,
                 *args,
                 **kwargs):

        self.cfg = Configuration()

        self.item_key = self.cfg[self.key].get(ITEM_KEY)
        self.iterable_line = self.cfg[self.key].get(ITERABLE_LINE)
        self.sort_iterable = self.cfg[self.key].get(ITERABLE_SORTED, False)
        self.force_iter_list = self.cfg[self.key].get(ITERABLE_FORCE_LIST, False)
        self.rows_first = self.cfg[u'{k}.{c}'.format(k=self.key, c=ROWS_FIRST)]
        self.widget_grid = self.cfg[u'{k}.{c}'.format(k=self.key, c=WIDGET_GRID)]

        self.iter_list = False

        # If an item_key is set then load it from self.cfg
        if self.item_key is not None:
            config = self.cfg[self.item_key]

            if isinstance(config, dict):
                self.parent.item_dict = config

            if isinstance(config, list):
                self.parent.item_list = config
                self.iter_list = True

        if self.sort_iterable:
            # sort_iterable is true convert item_dict to an Ordered dict and sort it
            self.parent.item_dict = sort_dict(self.parent.item_dict)
            self.parent.item_list.sort()

        if self.force_iter_list:
            self.iter_list = True

        self.draw_layout()

    def __iter_layout(self,
                      line_idx,
                      line_cfg,
                      offset,
                      item_name,
                      item_value=None,
                      **line_kwargs):

        line_kwargs[LINE_KWARG_ITER_NAME] = item_name

        if item_value is not None:
            line_kwargs[_LINE_KWARG_DEFAULT] = line_cfg.get(LINE_DEFAULT, False)
            line_kwargs[LINE_KWARG_ITER_VALUE] = item_value

        line_kwargs[
            _LINE_KWARG_ROW
            if self.rows_first
            else _LINE_KWARG_COLUMN
        ] = line_idx + offset

        self.draw_line(**line_kwargs)

        # Update iterable offset so that further lines are drawn in their correct position
        offset += 1

        return offset, line_kwargs

    def draw_layout(self):

        iterable_offset = 0

        for line_idx, line in enumerate(self.widget_grid):

            line_kwargs = {
                _LINE_KWARG_LINE: line[WIDGET_GRID_LINE],
                _LINE_KWARG_ROW if self.rows_first else _LINE_KWARG_COLUMN: line_idx + iterable_offset
            }

            logging.debug(u'draw_layout line kwargs: {k}'.format(k=line_kwargs))

            if line_idx == self.iterable_line:

                if self.iter_list:
                    for item_name in self.parent.item_list:
                        iterable_offset, line_kwargs = self.__iter_layout(line_idx=line_idx,
                                                                          line_cfg=line,
                                                                          offset=iterable_offset,
                                                                          item_name=item_name,
                                                                          **line_kwargs)

                else:
                    for item_name, item_value in iteritems(self.parent.item_dict):
                        iterable_offset, line_kwargs = self.__iter_layout(line_idx=line_idx,
                                                                          line_cfg=line,
                                                                          offset=iterable_offset,
                                                                          item_name=item_name,
                                                                          item_value=item_value,
                                                                          **line_kwargs)

                # Once iteration complete remove the extra kwargs
                del line_kwargs[LINE_KWARG_ITER_NAME]

                if not self.iter_list:
                    del line_kwargs[_LINE_KWARG_DEFAULT]
                    del line_kwargs[LINE_KWARG_ITER_VALUE]

            else:
                self.draw_line(**line_kwargs)

        # Configure columns that are allowed to expand
        for column in self.cfg[self.key].get(EXPANDING_COLUMNS, []):
            self.columnconfigure(column, weight=1)

        # Configure rows that are allowed to expand
        for row in self.cfg[self.key].get(EXPANDING_ROWS, []):
            self.rowconfigure(row, weight=1)

    def draw_line(self,
                  line,
                  row=0,
                  column=0,
                  default=False,
                  **iter_kwargs):

        for idx, widget in enumerate(line):

            # Set row / column value
            if self.rows_first:
                column = idx

            else:
                row = idx

            # Draw the widget for this position
            self.draw_widget(widget_config=copy.deepcopy(widget),
                             row=row,
                             column=column,
                             **iter_kwargs)

        if default:
            item_name = iter_kwargs.get(LINE_KWARG_ITER_NAME)

            if item_name is not None:
                item_dict = self.parent.item_dict.get(item_name)

                if item_dict is not None and LINE_DEFAULT in item_dict:
                    self.label(text=u'X' if item_dict[LINE_DEFAULT] else u'',
                               row=row if self.rows_first else row + 1,
                               column=column + 1 if self.rows_first else column)
                    if item_dict[LINE_DEFAULT]:
                        self.parent.default.set(item_name)

    def draw_widget(self,
                    widget_config,
                    row=None,
                    column=None,
                    **iter_kwargs):

        # Get the Tk objects (These must be defined in widget & var mix-ins!)
        widget_object = getattr(self, widget_config[WIDGET_TYPE])  # Tk widget object

        # Get the kwarg configurations for both objects
        widget_kwargs = widget_config.get(WIDGET_KWARGS, {})

        # Setup object name parameters
        widget_name = u'_{id}_{type}'.format(id=widget_config[WIDGET_NAME],
                                             type=widget_config[WIDGET_TYPE])

        # if this is an iterable then we must set the name accordingly to stop each new line overwriting the previous
        if LINE_KWARG_ITER_NAME in iter_kwargs:
            widget_name = u'{widget_name}_{iter_name}'.format(widget_name=widget_name,
                                                              iter_name=iter_kwargs[LINE_KWARG_ITER_NAME])

        # Setup dict of available local params for use in kwargs
        locals_dict = {
            u'widget_name': widget_name,
            u'row': row,
            u'column': column
        }

        # add the iterable kwargs for this widget line to the locals dict
        locals_dict.update(iter_kwargs)

        # Create the widget var.
        widget_var = handle_variable(frame=self,
                                     var_config=widget_config[WIDGET_VAR],
                                     name_default=u'{widget_name}_var'.format(widget_name=widget_name),
                                     **locals_dict)

        # Add widget_var to locals_dict
        locals_dict[u'var_name'] = widget_var.name
        locals_dict[u'widget_var'] = widget_var

        # Process the widget kwargs
        for kw_name, kw in iteritems(widget_kwargs):
            widget_kwargs[kw_name] = handle_kwarg(self, kw, locals_dict)

        # Handle grid row & column
        if u'row' not in widget_kwargs:
            widget_kwargs[u'row'] = row

        if u'column' not in widget_kwargs:
            widget_kwargs[u'column'] = column

        # If this is a radiobutton and selected has not been set then set selected
        if widget_config[WIDGET_TYPE] == u'radiobutton' \
                and self.parent.selected.get() == u'' \
                and LINE_KWARG_ITER_NAME in locals_dict:
                self.parent.selected.set(locals_dict[LINE_KWARG_ITER_NAME])

        # Draw the widget
        widget_object(name=widget_name,
                      **widget_kwargs)

        # Handle bind for widget (if required)
        bind = widget_config.get(WIDGET_BINDING, False)

        if bind:
            bind_fn = handle_kwarg(self, bind[BIND_FUNCTION], locals_dict)

            # Ensure the function has not evaluated as a string value (this is possible!)
            if not isinstance(bind_fn, str):
                self.bind_events(control=getattr(self, widget_name),
                                 events=bind[BIND_EVENTS],
                                 function=bind_fn)
