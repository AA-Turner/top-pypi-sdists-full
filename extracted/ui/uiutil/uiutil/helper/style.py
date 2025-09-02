# encoding: utf-8

from tkinter import ttk, FLAT


def add_border(form,
               border_width):

    inner_frame = ttk.Frame(form, borderwidth=border_width, relief=FLAT)
    inner_frame.grid(row=0, column=0)

    return inner_frame
