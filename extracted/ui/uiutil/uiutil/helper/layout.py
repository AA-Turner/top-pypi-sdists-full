# encoding: utf-8


# Tk frame / window grid expansion methods
def nice_grid_columns(parent):

    cols, _ = parent.grid_size()

    for col in range(0, cols):
        parent.columnconfigure(col, weight=1)


def nice_grid_rows(parent):

    _, rows = parent.grid_size()

    for row in range(0, rows):
        parent.rowconfigure(row, weight=1)


def nice_grid(parent,
              rows=True,
              columns=True):

    if columns:
        nice_grid_columns(parent)

    if rows:
        nice_grid_rows(parent)


# Get co-ordinate centres
def get_centre(x=0,
               y=0,
               width=0,
               height=0,
               geometry=None):

    if geometry is not None:
        size, x, y = geometry.split(u'+')
        width, height = size.split(u'x')

    x_centre = int(x) + (int(width) / 2)
    y_centre = int(y) + (int(height) / 2)

    return x_centre, y_centre
