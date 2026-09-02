# encoding: utf-8

from tkinter import ttk


# TODO: Rethink this. A MixIn doesn't really make sense.
#       Maybe a separate class

class StyleMixIn(object):

    STYLES = {}

    def __init__(self,
                 *args,
                 **kwargs):

        super(StyleMixIn, self).__init__()

        self.style = ttk.Style()

        for name, style in iter(self.STYLES.items()):
            self.style.configure(name,
                                 **style)

    def add_style(self,
                  name,
                  **style):
        self.style.configure(name,
                             **style)
