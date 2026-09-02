# encoding: utf-8

from tkinter import ttk
from tkinter.constants import VERTICAL, HORIZONTAL, NW
from tkinter import Canvas

from uiutil.frame.frame import BaseFrame


class BaseScrollFrame(BaseFrame):

    def __init__(self,
                 parent=None,
                 vbar=True,
                 hbar=True,
                 canvas_height=0,
                 canvas_width=0,
                 *args,
                 **kwargs):

        self._vbar_enabled = vbar
        self._hbar_enabled = hbar

        self._vbar_drawn = False
        self._hbar_drawn = False

        # Create a frame to put the canvas & scroll bars on.
        # self will be used as the inner frame so that the BaseScrollFrame acts
        # like a BaseFrame as much as possible
        self._canvas_frame = BaseFrame(parent, *args, **kwargs)

        # Create canvas
        self._canvas = Canvas(self._canvas_frame,
                              highlightthickness=0,
                              height=canvas_height,
                              width=canvas_width)
        self._canvas.grid(row=0,
                          column=0,
                          sticky=u'nsew')

        BaseFrame.__init__(self,
                           parent=self._canvas,
                           height=canvas_height,
                           width=canvas_width)

        # Add frame (self) to canvas
        self._canvas_window = self._canvas.create_window((0, 0),
                                                         window=self,
                                                         anchor=NW)

        # Update parent to hideaway canvas frame & canvas
        self.parent = parent

        # Create the scroll bars
        self._vbar = ttk.Scrollbar(self._canvas_frame, orient=VERTICAL)
        self._hbar = ttk.Scrollbar(self._canvas_frame, orient=HORIZONTAL)

        # Draw scroll bars (if enabled & required)
        self._enable_vertical_scrollbar()
        self._enable_horizontal_scrollbar()

        # Set the canvas grid square to expand to fill space
        self._canvas_frame.columnconfigure(0, weight=1)
        self._canvas_frame.rowconfigure(0, weight=1)

        # reset the view
        self._canvas.xview_moveto(0)
        self._canvas.yview_moveto(0)

        # track changes to the canvas and frame width
        # and sync them, also updating the scrollbar
        self._canvas.bind('<Configure>', self._configure_canvas)
        self.bind('<Configure>', self._configure_scrolled_frame)

        # Bind Enter/Leave events to allow activation of scroll bars only if over the scroll frame.
        # This stops all frames scrolling when multiple scroll frames are drawn.
        # Though this likely will not work as expected for nested scroll frames!
        self._canvas.bind('<Enter>', self._frame_enter)
        self._canvas.bind('<Leave>', self._frame_leave)

        self._remap_frame_methods()

    def _remap_frame_methods(self):
        # remap self.grid to the canvas_frame.
        # This is required to keep similar functionality to BaseFrame
        self._grid = self.grid
        self.grid = self._canvas_frame.grid

        # remap self.destroy custom destroy method as we are hiding a frame and
        # a canvas we need to destroy those also when destroy is called!
        self._destroy = self.destroy
        self.destroy = self._destroy_base_frame

    def _destroy_base_frame(self):
        self._destroy()
        self._canvas_frame.destroy()

    def _frame_enter(self,
                     _):

        # Bind only if scroll bars are both enabled and drawn
        if self._vbar_enabled and self._vbar_drawn:
            # Bind the mouse so we can scroll vertically anywhere on the canvas!
            self._canvas.bind_all('<MouseWheel>', self._on_vertical)

        if self._hbar_enabled and self._hbar_drawn:
            # Bind the mouse so we can scroll horizontally anywhere on the canvas!
            self._canvas.bind_all('<Shift-MouseWheel>', self._on_horizontal)

    def _frame_leave(self,
                     _):

        # If bound then unbind no matter what as we are no longer over the frame
        self._canvas.unbind_all('<MouseWheel>')
        self._canvas.unbind_all('<Shift-MouseWheel>')

    def _enable_vertical_scrollbar(self):

        if self._vbar_enabled and not self._vbar_drawn:
            # Draw the vertical scrollbar and associate it with the canvas
            self._vbar.config(command=self._canvas.yview)
            self._vbar.grid(row=0,
                            column=1,
                            rowspan=2,
                            sticky=u'ns')

            self._canvas.configure(yscrollcommand=self._vbar.set)

            self._vbar_drawn = True

    def _disable_vertical_scrollbar(self):

        if self._vbar_enabled and self._vbar_drawn:
            self._vbar.config(command=u'')
            self._vbar.grid_remove()
            self._canvas.configure(yscrollcommand=u'')

            self._vbar_drawn = False

    def _enable_horizontal_scrollbar(self):

        if self._hbar_enabled and not self._hbar_drawn:
            # Draw the horizontal scrollbar and associate it with the canvas
            self._hbar.config(command=self._canvas.xview)
            self._hbar.grid(row=1,
                            column=0,
                            sticky=u'ew')

            self._canvas.configure(xscrollcommand=self._hbar.set)

            self._hbar_drawn = True

    def _disable_horizontal_scrollbar(self):

        if self._hbar_enabled and self._hbar_drawn:
            self._hbar.config(command=u'')
            self._hbar.grid_remove()
            self._canvas.configure(xscrollcommand=u'')

            self._hbar_drawn = False

    def _on_vertical(self,
                     event):

        """ Mouse wheel vertical scroll bind function """

        self._canvas.yview_scroll(-1 * event.delta, 'units')

    def _on_horizontal(self,
                       event):

        """ Mouse wheel horizontal scroll bind function """

        self._canvas.xview_scroll(-1 * event.delta, 'units')

    def _configure_canvas(self,
                          _):

        req_buffer = 7

        # Update widths to fill visible areas
        if self.winfo_reqwidth() + req_buffer != self._canvas.winfo_width():
            if self._canvas.winfo_width() > self.winfo_reqwidth() + req_buffer:
                # update the canvas frame's width to fill the canvas
                self._canvas.itemconfigure(self._canvas_window,
                                           width=self._canvas.winfo_width())
                self._disable_horizontal_scrollbar()

            else:
                self._canvas.itemconfigure(self._canvas_window,
                                           width=self.winfo_reqwidth())
                self._enable_horizontal_scrollbar()

        # Update heights to fill visible areas
        if self.winfo_reqheight() + req_buffer != self._canvas.winfo_height():
            if self._canvas.winfo_height() > self.winfo_reqheight() + req_buffer:
                # update the canvas frame's width to fill the canvas
                self._canvas.itemconfigure(self._canvas_window,
                                           height=self._canvas.winfo_height())
                self._disable_vertical_scrollbar()

            else:
                self._canvas.itemconfigure(self._canvas_window,
                                           height=self.winfo_reqheight())
                self._enable_vertical_scrollbar()

    def _configure_scrolled_frame(self,
                                  _):

        # Update the scrollable area to match the size of the inner frame
        # We use canvas.bbox('all') here to account for when the canvas is larger than
        # the frame which can induce some weird scroll behaviour on some platforms!
        self._canvas.config(scrollregion=self._canvas.bbox('all'))

        if not self._hbar_enabled:
            # update the canvas's width to fit the inner frame
            if self.winfo_reqwidth() != self._canvas.winfo_width():
                self._canvas.config(width=self.winfo_reqwidth())

        if not self._vbar_enabled:
            # update the canvas's width to fit the inner frame
            if self.winfo_reqheight() != self._canvas.winfo_height():
                self._canvas.config(height=self.winfo_reqheight())
