# encoding: utf-8

try:
    import ttk
except ImportError:
    # For some reason the future version of tkinter.ttk does not seem to have Widget!
    from tkinter import ttk


class Spinbox(ttk.Widget):
    def __init__(self, master, **kw):
        ttk.Widget.__init__(self, master, 'ttk::spinbox', kw)
