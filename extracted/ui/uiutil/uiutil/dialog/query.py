# encoding: utf-8

from tkinter import ttk, StringVar
from tkinter.constants import EW, W, NORMAL

from ..frame.frame import BaseFrame
from ..helper.layout import nice_grid
from ..window.child import ChildWindow


class _QueryDialogWithOptions(ChildWindow):

    def __init__(self,
                 title,
                 prompt,
                 values=None,
                 *args,
                 **kwargs):

        self.prompt = prompt
        self.values = values if values else []
        self.result = None

        super(_QueryDialogWithOptions, self).__init__(*args, **kwargs)

        self.title = title

    def _draw_widgets(self):

        self.base = BaseFrame(self._main_frame,
                              column=0,
                              row=0)
        self.base.grid(sticky=EW)

        self.query = ttk.Label(self.base, text=self.prompt)
        self.query.grid(row=self.base.row.start(),
                        column=self.base.column.start(),
                        columnspan=3,
                        sticky=W)

        self.entry_var = StringVar(self.base)
        self.entry_var.set(u'Select or enter a value...')
        self.entry = ttk.Combobox(self.base,
                                  values=self.values,
                                  textvariable=self.entry_var)

        self.entry.grid(row=self.base.row.next(),
                        column=self.base.column.start(),
                        columnspan=3,
                        sticky=EW)

        self.ok_button = ttk.Button(self.base,
                                    state=NORMAL,
                                    text=u'OK',
                                    width=15,
                                    command=self.__ok)

        self.ok_button.grid(row=self.base.row.next(),
                            column=self.base.column.start())

        self.cancel_button = ttk.Button(self.base,
                                        state=NORMAL,
                                        text=u'Cancel',
                                        width=15,
                                        command=self.exit)

        self.cancel_button.grid(row=self.base.row.current,
                                column=self.base.column.next())

        nice_grid(self._main_frame)
        nice_grid(self.base)

    def __ok(self):
        self.result = self.entry_var.get()
        self.exit()

    def exit(self):
        self.destroy()


def query_dialog_with_options(title,
                              prompt,
                              values,
                              parent,
                              **kwargs):

    """ Get a string from the user

    Args:
        title: the dialog title
        prompt: the label text
        values: default values (list)
        parent: Dialog parent
        **kwargs: see SimpleDialog class

    Returns: string

    """

    window = _QueryDialogWithOptions(title, prompt, values, **kwargs)

    window.transient(parent)
    window.grab_set()
    parent.wait_window(window)

    return window.result
