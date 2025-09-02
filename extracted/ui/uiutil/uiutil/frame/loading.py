# encoding: utf-8

import logging
from tkinter.constants import HORIZONTAL, EW
from .frame import BaseFrame


class LoadingFrame(BaseFrame):

    def __init__(self, wait_func=None, *args, **kwargs):

        self.wait_func = wait_func

        super(LoadingFrame, self).__init__(*args, **kwargs)

        self.progress = self.progressbar(length=280,
                                         orient=HORIZONTAL,
                                         mode=u'indeterminate',
                                         sticky=EW)
        self.progress.start()

        if self.wait_func is not None:
            self.after(ms=500, func=self.run)

    def run(self):
        try:
            self.wait_func()

        except Exception as err:
            logging.exception(err)

        finally:
            self.parent.master.exit()
