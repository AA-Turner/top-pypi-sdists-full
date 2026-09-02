# encoding: utf-8

import json
import logging_helper
from future.utils import iteritems, string_types
from uiutil.frame.frame import BaseFrame
from configurationutil import Configuration, cfg_params
from .._metadata import __version__, __authorshort__, __module_name__
from ..resources import templates, schema
from ._dynamic_widget import DynamicWidgetFrame
from ._dynamic_scroll import DynamicScrollFrame
from ._dynamic_base import EXPANDING_ROWS, EXPANDING_COLUMNS
from ..helper.dynamic_variable import handle_variable

# Register Config details (These are expected to be overwritten by an importing app)
cfg_params.APP_NAME = __module_name__
cfg_params.APP_AUTHOR = __authorshort__
cfg_params.APP_VERSION = __version__

# Set the config initialisation parameters
LAYOUT_CFG = u'ui_layout'
TEMPLATE = templates.ui_layout

logging = logging_helper.setup_logging()

# ConfigFrame keys
CONFIG_FRAMES = u'frames'
CONFIG_VARS = u'variables'

# config frame keys
CONFIG_CLASS = u'class'
CONFIG_KEY = u'key'
CONFIG_ROW = u'row'
CONFIG_COLUMN = u'column'
CONFIG_STICKY = u'sticky'
CONFIG_VERTICAL = u'scroll_vertical'
CONFIG_HORIZONTAL = u'scroll_horizontal'

# Layout types
ROOT_LAYOUT = u'root_layouts'
WIDGET_LAYOUT = u'widget_layouts'


def _add_layout(layout_type,
                layout_name,
                layout):

    cfg = Configuration()

    # Register configuration
    cfg.register(config=LAYOUT_CFG,
                 config_type=cfg_params.CONST.json,
                 template=TEMPLATE,
                 schema=schema.ui_layout)

    key = u'{c}.{t}.{n}'.format(c=LAYOUT_CFG,
                                t=layout_type,
                                n=layout_name)

    cfg[key] = layout


def add_root_layout(layout_name,
                    layout):

    _add_layout(ROOT_LAYOUT,
                layout_name,
                layout)


def add_widget_layout(layout_name,
                      layout):

    _add_layout(WIDGET_LAYOUT,
                layout_name,
                layout)


def add_layout_config(layout_cfg):

    if isinstance(layout_cfg, string_types):
        layout_cfg = json.load(open(layout_cfg))

    root_layouts = layout_cfg.get(ROOT_LAYOUT)
    widget_layouts = layout_cfg.get(WIDGET_LAYOUT)

    if root_layouts is not None:
        for layout_name, layout in iteritems(root_layouts):
            add_root_layout(layout_name,
                            layout)

    if widget_layouts is not None:
        for layout_name, layout in iteritems(widget_layouts):
            add_widget_layout(layout_name,
                              layout)


class DynamicFrame(BaseFrame):

    # Add the available frame classes
    FRAME_CLASSES = {
        u'DynamicWidgetFrame': DynamicWidgetFrame,
        u'DynamicScrollFrame': DynamicScrollFrame
    }

    def __init__(self,
                 layout_key,
                 item_dict=None,
                 item_list=None,
                 selected=None,
                 *args,
                 **kwargs):

        self.key = layout_key
        self.item_dict_name = u''
        self.item_dict = item_dict if item_dict is not None else {}
        self.item_list = item_list if item_list is not None else []

        self.selected = self.string_var(value=u'' if selected is None else selected)
        self.default = self.string_var()

        self.cfg = Configuration()

        # Register configuration
        self.cfg.register(config=LAYOUT_CFG,
                          config_type=cfg_params.CONST.json,
                          template=TEMPLATE,
                          schema=schema.ui_layout)

        self.frames = {}
        self.variables = {}
        self.layout = self.cfg[self.key]

        BaseFrame.__init__(self,
                           padx=0,
                           pady=0,
                           *args,
                           **kwargs)

        self.init_variables()
        self.before_draw()
        self.draw_frames()

    def init_variables(self):

        for var_config in self.layout.get(CONFIG_VARS, []):
            var = handle_variable(frame=self,
                                  var_config=var_config)

            self.variables[var.name] = var

    def draw_frames(self):

        for frame_name, frame_config in iteritems(self.layout.get(CONFIG_FRAMES, {})):
            self.draw_frame(frame_name, frame_config)

        # Configure columns that are allowed to expand
        for column in self.layout.get(EXPANDING_COLUMNS, []):
            self.columnconfigure(column, weight=1)

        # Configure rows that are allowed to expand
        for row in self.layout.get(EXPANDING_ROWS, []):
            self.rowconfigure(row, weight=1)

    def draw_frame(self,
                   name,
                   config):

        frame_class = self.FRAME_CLASSES[config[CONFIG_CLASS]]

        frame_kwargs = {
            u'parent': self,
            u'key': config[CONFIG_KEY],
            u'row': config[CONFIG_ROW],
            u'column': config[CONFIG_COLUMN]
        }

        # If we are using a scroll frame check on scrollbar specific params
        # TODO: We should convert this to kwargs at some point.
        if config[CONFIG_CLASS] == u'DynamicScrollFrame':
            scroll_v = config.get(CONFIG_VERTICAL)
            scroll_h = config.get(CONFIG_HORIZONTAL)

            if scroll_v is not None:
                frame_kwargs[u'vbar'] = scroll_v

            if scroll_h is not None:
                frame_kwargs[u'hbar'] = scroll_h

        frame = frame_class(**frame_kwargs)

        sticky = config.get(CONFIG_STICKY)

        if sticky is not None:
            frame.grid(sticky=sticky)

        self.frames[name] = frame

    def refresh(self):

        logging.debug(u'REFRESH FRAMES')

        # Destroy existing frames
        for name, frame in iteritems(self.frames):
            frame.destroy()

        # Reset self.frames
        self.frames = {}

        # Re-draw
        self.init_variables()
        self.before_draw()
        self.draw_frames()

        # re-size window
        self.parent.parent.update_geometry()

    def update_layout(self,
                      layout):

        # Change the DynamicFrame layout to use the add/edit layout
        self.layout = self.cfg[layout]

        # Remove variables specific to this layout
        for var_name in self.variables.keys():
            if hasattr(self, var_name):
                delattr(self, var_name)

        # Call refresh to redraw with new layout
        self.refresh()

    def return_to_root_layout(self):

        self.selected.set(u'')
        self.default.set(u'')

        self.item_dict_name = u''
        self.item_dict = {}
        self.item_list = []

        self.update_layout(self.key)

    def close(self):
        self.parent.parent.destroy()

    def before_draw(self):

        """ Override this to run any extra steps before UI is drawn """
