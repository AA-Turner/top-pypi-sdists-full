# encoding: utf-8

import os
from ..tk_names import E, W, NSEW, NORMAL, DISABLED
from fdutil.crossplatform_startfile import mailto

from .._metadata import __version__, __authorshort__, __module_name__

from .frame import BaseFrame
from ..widget.scroll import TextScroll
from ..helper.text_handler import TextHandler
from ..widget.combobox import Combobox
from ..widget.label import Label
from ..widget.button import Button

# Configuration initialisation
from configurationutil import cfg_params, Configuration
import logging_helper

logging = logging_helper.setup_logging()

# Register app details for configuration
cfg_params.APP_NAME = __module_name__
cfg_params.APP_AUTHOR = __authorshort__
cfg_params.APP_VERSION = __version__


class LogFrame(BaseFrame):

    BUTTON_WIDTH = 20
    LOG_LEVELS = [u'DEBUG',
                  u'INFO',
                  u'WARNING',
                  u'ERROR',
                  u'CRITICAL']
    DEFAULT_LEVEL = u'INFO'

    def __init__(self,
                 log_level_persistence=None,
                 *args,
                 **kwargs):
        """
        :param log_level_persistence: a stateutil.persist.Persist object
        :param args: passed to the BaseFrame
        :param kwargs: passed to the BaseFrame
        """

        self.__enable_poll = False
        self.polling_interval = 10
        self.email_recipients = u'example@example.com'

        BaseFrame.__init__(self, *args, **kwargs)

        Label(text=u'Log Level:',
              row=self.row.start(),
              column=self.column.start(),
              sticky=W)

        self.log_level_persistence = log_level_persistence

        self.log_level = Combobox(value=self.DEFAULT_LEVEL if not self.log_level_persistence else None,
                                  link=log_level_persistence,
                                  values=self.LOG_LEVELS,
                                  trace=self.__level_change if not self.log_level_persistence else None,
                                  column=self.column.next(),
                                  sticky=W)

        self.columnconfigure(self.column.current, weight=1)

        Button(state=NORMAL,
               text=u'Email Log',
               width=self.BUTTON_WIDTH,
               command=self.__email,
               column=self.column.next(),
               sticky=E,
               tooltip=u'Email logfile')

        Button(state=NORMAL,
               text=u'Clear',
               width=self.BUTTON_WIDTH,
               command=self.__clear,
               column=self.column.next(),
               sticky=E,
               tooltip=u'Clear the log window')

        self.log_text = TextScroll(state=DISABLED,
                                   row=self.row.next(),
                                   column=self.column.start(),
                                   columnspan=4,
                                   sticky=NSEW)
        self.rowconfigure(self.row.current, weight=1)

        self.log_text.configure(font=u'TkFixedFont')

        # Create textLogger
        self.text_handler = TextHandler(self.log_text)
        self.text_handler.setLevel(self.log_level.value)

        # Add the handler to root logger
        logger = logging_helper.getLogger()
        logger.addHandler(self.text_handler)

        if self.log_level_persistence:
            self.log_level_persistence.register_observer(self)

        self.__enable_poll = True

    def __level_change(self):
        self.text_handler.setLevel(self.log_level.value)

    def __clear(self):
        self.text_handler.clear()

    def __email(self):
        cfg = Configuration()

        log_file = u'{f}'.format(f=os.path.join(cfg.log_path,
                                                logging_helper.getLogger().LH_FILE_HANDLER.baseFilename))

        mailto(
            u'',
            to=self.email_recipients,
            subject=u'{app} {ver} Logs'.format(app=cfg.app_name,
                                               ver=cfg.app_version),
            body=u'Please see attach the following file if not already attached: '
                 u'{f}'.format(f=log_file),
            attach=log_file
        )
        # TODO: get attach working!

    def notification(self,
                     notifier,
                     **params):

        if notifier == self.log_level_persistence:
            self.__level_change()

    def poll(self):
        if self.__enable_poll:
            self.text_handler.poll()
