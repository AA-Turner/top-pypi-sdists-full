# encoding: utf-8

from ..tk_names import ttk, HORIZONTAL, VERTICAL
from stateutil.incrementer import Incrementer
from ..helper.layout import nice_grid, get_centre
from ..helper.arguments import get_grid_kwargs


class LayoutMixIn(object):

    def __init__(self,
                 *args,
                 **kwargs):
        super(LayoutMixIn, self).__init__()

    def modal_window(self,
                     window):

        window.transient()
        window.grab_set()
        self.wait_window(window)

    def nice_grid(self,
                  *args,
                  **kwargs):
        nice_grid(self, *args, **kwargs)

    def nice_grid_rows(self,
                       *args,
                       **kwargs):
        nice_grid(self, columns=False, *args, **kwargs)

    def nice_grid_columns(self,
                          *args,
                          **kwargs):
        nice_grid(self, rows=False, *args, **kwargs)

    def get_centre(self):
        return get_centre(geometry=self.winfo_geometry())

    def get_parent_centre(self):
        return get_centre(geometry=self.parent_geometry)

    def get_screen_centre(self):
        return get_centre(x=(self.winfo_screenwidth() / 2),
                          y=(self.winfo_screenheight() / 2),
                          width=self.width,
                          height=self.height)


class FrameLayoutMixIn(LayoutMixIn):

    DEFAULT_PAD_X = 5
    DEFAULT_PAD_Y = 5
    AUTO_POSITION = None  # Set to None, HORIZONTAL or VERTICAL

    def __init__(self,
                 layout=None,
                 padx=None,
                 pady=None,
                 *args,
                 **kwargs):

        self.AUTO_POSITION = layout if layout is not None else self.AUTO_POSITION

        super(LayoutMixIn, self).__init__(*args,
                                          **kwargs)

        self.row = Incrementer()
        self.column = Incrementer()

        grid_kwargs = get_grid_kwargs(frame=self.parent,
                                      padx=self.DEFAULT_PAD_X if padx is None else padx,
                                      pady=self.DEFAULT_PAD_Y if pady is None else pady,
                                      **kwargs)

        self.grid(**grid_kwargs)

    def set_insert_position(self,
                            row=None,
                            column=None):
        get_grid_kwargs(frame=self,
                        row=row,
                        column=column)

    def position_for_next_widget(self,
                                 columnspan=1,
                                 rowspan=1,
                                 **_):
        if self.AUTO_POSITION is HORIZONTAL:
            self.column.next(columnspan)
            if rowspan > 1:
                self.row.next(rowspan - 1)

        elif self.AUTO_POSITION is VERTICAL:
            self.row.next(rowspan)
            if columnspan > 1:
                self.column.next(columnspan - 1)

    def _set_title(self, title):
        if isinstance(self, ttk.LabelFrame):
            self.config(text=title)
