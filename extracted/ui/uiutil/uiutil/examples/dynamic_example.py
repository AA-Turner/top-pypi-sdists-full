# encoding: utf-8

import logging_helper
from uiutil.window.dynamic import DynamicRootWindow
from configurationutil import Configuration, cfg_params
from uiutil._metadata import __version__, __authorshort__, __module_name__
from uiutil.resources import templates
from uiutil.frame import dynamic

logging = logging_helper.setup_logging()

# Register Config details (These are expected to be overwritten by an importing app)
cfg_params.APP_NAME = __module_name__
cfg_params.APP_AUTHOR = __authorshort__
cfg_params.APP_VERSION = __version__

# Set the config initialisation parameters
TEST_LAYOUT_CFG = u'example_config'


class ExampleDynamicWindow(DynamicRootWindow):

    def __init__(self,
                 *args,
                 **kwargs):

        self.cfg = Configuration()

        super(ExampleDynamicWindow, self).__init__(*args, **kwargs)

    # Button Methods
    @staticmethod
    def dummy():
        print(u'The dummy button was clicked!')


# Register configuration
Configuration().register(config=TEST_LAYOUT_CFG,
                         config_type=cfg_params.CONST.json,
                         template=templates.example_config)

cw = ExampleDynamicWindow(layout_key=u'{c}.root_layouts.example_layout'.format(c=dynamic.LAYOUT_CFG),
                          window_title=u'Example Dynamic Window')
