# encoding: utf-8

from tkinter.messagebox import askquestion

import logging_helper
from uiutil.window.dynamic import DynamicRootWindow
from configurationutil import Configuration, cfg_params
from uiutil._metadata import __version__, __authorshort__, __module_name__
from uiutil.resources import templates
from uiutil.frame import dynamic
from uiutil.frame._dynamic_base import LINE_DEFAULT

logging = logging_helper.setup_logging()

# Register Config details (These are expected to be overwritten by an importing app)
cfg_params.APP_NAME = __module_name__
cfg_params.APP_AUTHOR = __authorshort__
cfg_params.APP_VERSION = __version__

# Set the config initialisation parameters
dynamic.add_layout_config(templates.example_ui_layout)
TEST_LAYOUT_CFG = u'example_config'

BUTTONS = u'widget_layouts.device_config_button_layout'

DEFAULT_DEVICE = {
    u'ip': u'0.0.0.0',
    u'port': 22,
    u'active': True,
    u'connect': False,
    u'remote': False,
    u'html': False
}


class ExampleDeviceConfigWindow(DynamicRootWindow):

    def __init__(self,
                 *args,
                 **kwargs):
        super(ExampleDeviceConfigWindow, self).__init__(*args, **kwargs)

    # Button Helpers
    def update_item(self,
                    widget_var_name,
                    widget_var):

        logging.debug(u'WIDGET_VAR_NAME: {n}'.format(n=widget_var_name))
        logging.debug(u'WIDGET_VAR: {v}'.format(v=widget_var.get()))

        widget_name_parts = widget_var_name.split(u'_')

        # Split the device name off the widget name
        item_name = u'_'.join(widget_name_parts[4:-1])
        logging.debug(u'ITEM_NAME: {v}'.format(v=item_name))

        key = u'{c}.{i}.{v}'.format(c=TEST_LAYOUT_CFG,
                                    i=item_name,
                                    v=widget_name_parts[2])
        logging.debug(u'KEY: {v}'.format(v=key))

        self.cfg[key] = widget_var.get()

    def add_device_name_trace(self,
                              widget_var_name,
                              widget_var):

        logging.debug(u'WIDGET_VAR_NAME: {n}'.format(n=widget_var_name))
        logging.debug(u'WIDGET_VAR: {v}'.format(v=widget_var.get()))

        # Split the device name off the widget name
        item_name = widget_var.get()
        logging.debug(u'NAME: {v}'.format(v=item_name))

        self.dynamic_frame.item_dict_name = item_name

    def add_edit_trace(self,
                       widget_var_name,
                       widget_var):

        logging.debug(u'WIDGET_VAR_NAME: {n}'.format(n=widget_var_name))
        logging.debug(u'WIDGET_VAR: {v}'.format(v=widget_var.get()))

        widget_name_parts = widget_var_name.split(u'_')

        # Split the device name off the widget name
        item_name = widget_name_parts[2]
        logging.debug(u'ITEM_NAME: {v}'.format(v=item_name))

        item_value = widget_var.get()
        logging.debug(u'ITEM_VALUE: {v}'.format(v=item_value))

        self.dynamic_frame.item_dict[item_name] = item_value

    def _add_edit(self,
                  edit=False):

        if edit:
            # Set the key for the edit layout
            key = u'{c}.root_layouts.edit_device_layout'.format(c=dynamic.LAYOUT_CFG)

            # Load item to be edited
            selected = self.dynamic_frame.selected.get()
            logging.debug(u'SELECTED: {d}'.format(d=selected))

            item_key = u'{c}.{i}'.format(c=TEST_LAYOUT_CFG,
                                         i=selected)

            self.dynamic_frame.item_dict_name = selected
            self.dynamic_frame.item_dict = self.cfg[item_key].copy()

        else:
            # Set the key for the add layout
            key = u'{c}.root_layouts.add_device_layout'.format(c=dynamic.LAYOUT_CFG)

            # Load a blank item
            self.dynamic_frame.item_dict = DEFAULT_DEVICE

        # Change the DynamicFrame layout to use the add/edit layout
        self.dynamic_frame.layout = self.cfg[key]

        # Call refresh to redraw with new layout
        self.dynamic_frame.refresh()

    def _return_to_root_layout(self):
        self.dynamic_frame.layout = self.cfg[self.key]
        self.dynamic_frame.item_dict_name = u''
        self.dynamic_frame.item_dict = None
        self.dynamic_frame.refresh()

    # Button Methods
    def add(self):
        self._add_edit()

    def edit(self):
        self._add_edit(edit=True)

    def delete(self):
        selected = self.dynamic_frame.selected.get()
        logging.debug(u'SELECTED: {d}'.format(d=selected))

        result = askquestion(u"Delete Device",
                             u"Are you sure you want to delete: {item}?".format(item=selected),
                             parent=self._main_frame)

        if result == u'yes':
            key = u'{c}.{i}'.format(c=TEST_LAYOUT_CFG,
                                    i=selected)

            del self.cfg[key]

            new_selected = self.cfg[TEST_LAYOUT_CFG].keys()[0]
            select_key = u'{c}.{k}'.format(c=TEST_LAYOUT_CFG,
                                           k=new_selected)

            default = self.dynamic_frame.default.get()

            if default == selected:
                self.cfg[u'{c}.default'.format(c=select_key)] = True
                self.dynamic_frame.default.set(new_selected)

            self.dynamic_frame.selected.set(new_selected)

            self.dynamic_frame.refresh()

    def set_default(self):
        selected = self.dynamic_frame.selected.get()
        logging.debug(u'SELECTED: {d}'.format(d=selected))

        for item in self.cfg[TEST_LAYOUT_CFG]:
            key = u'{c}.{i}.{d}'.format(c=TEST_LAYOUT_CFG,
                                        i=item,
                                        d=LINE_DEFAULT)

            self.cfg[key] = True if item == selected else False

        # Call refresh to redraw with new layout
        self.dynamic_frame.refresh()

    def cancel(self):
        self._return_to_root_layout()

    def save(self):

        key = u'{c}.{i}'.format(c=TEST_LAYOUT_CFG,
                                i=self.dynamic_frame.item_dict_name)

        self.cfg[key] = self.dynamic_frame.item_dict

        self._return_to_root_layout()


# Register configuration
Configuration().register(config=TEST_LAYOUT_CFG,
                         config_type=cfg_params.CONST.json,
                         template=templates.example_config)

cw = ExampleDeviceConfigWindow(layout_key=u'{c}.root_layouts.device_config_layout'.format(c=dynamic.LAYOUT_CFG),
                               window_title=u'Device Config')
