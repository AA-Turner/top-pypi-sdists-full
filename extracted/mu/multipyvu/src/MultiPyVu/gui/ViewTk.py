"""
View.py holds the code for a gui for MultiPyVu.Server

@author: djackson
"""


import gc
import io
import logging
import logging.handlers
import sys
import tkinter as tk
from enum import IntEnum, auto
from threading import Lock
from tkinter import font, ttk
try:
    from PIL import ImageTk, Image
except ImportError:
    msg = "Must import the PIL module.  Use:  \n"
    msg += "\tpip install Pillow"
    exit(msg)


from ..__version import __version__ as mpv_version
from ..project_vars import SERVER_NAME
from .font_loader import register_fonts, resolve_family
from .IView import IView
from .IController import IController


class TextWidgetHandler(logging.Handler):
    """
    Configure a handler for info messages to the std.out
    """
    def __init__(self, text_widget: tk.Text):
        super().__init__()
        self.text_widget = text_widget
        self.text_widget.config(state=tk.NORMAL)

    def emit(self, record):
        msg = self.format(record)
        # enable editing
        self.text_widget.config(state=tk.NORMAL)
        # insert logging message into the Text widget
        self.text_widget.insert(tk.END, msg + '\n')
        # auto-scroll to the end
        self.text_widget.see(tk.END)
        # disable editing
        self.text_widget.config(state=tk.DISABLED)

    def stop(self):
        """
        Remove the handler.
        """
        self.close()


class StdoutRedirector(io.TextIOBase):
    """
    This is used to redirect stdout to the gui
    """
    def __init__(self, text_widget: tk.Text):
        self.text_widget = text_widget
        # Redirect sys.stdout to the custom redirector
        sys.stdout = self

    def write(self, string):
        """
        Overwrite the io.TextIOBase.write command to go to the text_widget
        """
        self.text_widget.config(state='normal')
        self.text_widget.insert("end", string)
        self.text_widget.see("end")  # Auto-scroll to the end
        self.text_widget.config(state='disabled')
        return len(string)

    def stop(self):
        sys.stdout = sys.__stdout__


class RedirectOutputToGui():
    def __init__(self, text_widget: tk.Text):
        """
        Redirect stdio and INFO logging handlers to the gui

        Parameters:
        -----------
        text_widget: tkinter.Text
            The text widget target
        """
        self.stdio = StdoutRedirector(text_widget)
        self.add_tkinter_handler(text_widget)

    def add_tkinter_handler(self, text_widget: tk.Text):
        """
        This adds the tkinter text widget handler so that messages
        will show up in the gui text box
        """
        self.tk_logger = logging.getLogger(SERVER_NAME)
        # check if the tkinter handler is already attached
        for handler in self.tk_logger.handlers:
            if isinstance(handler, TextWidgetHandler):
                # it exists, so do nothing
                return
        tk_handler = TextWidgetHandler(text_widget)
        tk_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s',
                                      '%m-%d %H:%M')
        tk_handler.setFormatter(formatter)
        self.tk_logger.addHandler(tk_handler)

    def stop(self):
        """
        Stop redirecting output to the gui
        """
        self.stdio.stop()


class ViewTk(IView):
    """
    The implementation of the View in the Model-View-Controller 
    design pattern.  This implements a Tkinter gui.
    """
    TK_RUNNING = False
    _pad = 7
    _border_width_main_frames = 3
    _thin_border = 1
    _info_label_width = 19
    _num_of_clients: int = 0
    _btn_style = 'QD.TButton'

    class start_button_text(IntEnum):
        start = auto()
        idle = auto()
        stop = auto()
    start_button_enum = start_button_text

    def __init__(self, controller: IController):
        self._controller = controller

        # Hand the bundled QD font to the OS before Tk starts up, since Tk
        # builds its list of available families during initialization.  The
        # family name is resolved once the root window exists.
        self._qd_font_family = register_fonts(
            [self._controller.absolute_path(f'../font/{f}')
             for f in ('Play-Regular.ttf', 'Play-Bold.ttf')]
            )

        self.gui = tk.Tk()
        self.gui.title(f'MultiPyVu Server {mpv_version}')
        # the root window background shows through any gap the frames do
        # not cover, so pin it rather than let it follow the OS appearance
        self.gui.configure(background=self.qd_white)
        # The layout is sized to its contents, so widening the window only
        # exposes background on the right.  Block interactive resizing; the
        # window still tracks its requested size as widgets are shown/hidden.
        self.gui.resizable(False, False)
        self.gui.protocol("WM_DELETE_WINDOW", self.quit_gui)

        # the image needs to be defined here in order to keep it in memory
        rel_path = '../images/QD_logo.jpg'
        file_image = Image.open(self._controller.absolute_path(rel_path))
        self.logo_img = ImageTk.PhotoImage(file_image)

        # this gets instantiated when the server starts
        self.redirector = None

    def _configure_button_style(self, btn_font):
        """
        Set up the ttk style used by the buttons.

        tk.Button ignores 'background' on macOS, where the button is drawn
        as a native Aqua bezel with its own margins and focus ring -- which
        is why the classic buttons looked thicker and darker there than on
        Windows.  ttk.Button honors the color options, but only under a
        Tk-drawn theme; the macOS default theme ('aqua') ignores them just
        like tk.Button does.  'clam' ships with Tk on every platform and
        draws identically on all of them, so select it explicitly.

        Parameters:
        -----------
        btn_font: tkinter.font.Font
            The font used for the button text.  ttk.Button takes no 'font'
            option of its own, so it has to be set through the style.
        """
        style = ttk.Style(self.gui)
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure(
            ViewTk._btn_style,
            font=btn_font,
            background=self.qd_btn_face,
            foreground=self.qd_black,
            bordercolor=self.qd_btn_border,
            # clam shades its 3-D bevel with these two; flattening them to
            # the face color keeps the button looking like a Windows button
            lightcolor=self.qd_btn_face,
            darkcolor=self.qd_btn_face,
            borderwidth=ViewTk._thin_border,
            relief=tk.RAISED,
            padding=(ViewTk._pad, ViewTk._pad),
            anchor='center',
            )
        # clam draws a dashed rectangle inside a button whenever it holds
        # focus, which happens on click.  Setting -focusthickness to 0 is
        # not enough, so drop Button.focus from the element tree: with no
        # focus element there is nothing left to draw a ring in any state.
        # The typeshed stub for Style.layout types layoutspec too
        # narrowly to express a spec with nested children, so it
        # rejects this at type check time.  The call is correct and
        # is what builds the button style at runtime.
        style.layout(  # type: ignore[arg-type]
            ViewTk._btn_style,
            [('Button.border', {
                'sticky': 'nswe',
                'border': '1',
                'children': [
                    ('Button.padding', {
                        'sticky': 'nswe',
                        'children': [
                            ('Button.label', {'sticky': 'nswe'}),
                            ],
                        }),
                    ],
                })],
            )
        style.map(
            ViewTk._btn_style,
            background=[('pressed', self.qd_btn_pressed),
                        ('active', self.qd_btn_active)],
            bordercolor=[('pressed', self.qd_btn_border),
                         ('active', self.qd_btn_border)],
            foreground=[('disabled', self.qd_btn_disabled_text)],
            relief=[('pressed', tk.SUNKEN)],
            )
        return style

    def create_display(self):
        """
        Create the Server window
        """
        # The QD font is for chrome only -- the box labels, the Server
        # Status title, and the buttons.  register_fonts() ran in __init__;
        # ask Tk which family it ended up with so a failed registration
        # degrades to the same fallback face on every platform instead of
        # Tk's own default.
        qd_family = resolve_family(self._qd_font_family)
        qd_font_small = font.Font(family=qd_family, size=17)
        qd_font_status = font.Font(family=qd_family, size=12)

        # The values shown inside the boxes use the platform's own UI font
        # at the same sizes, so readouts look native on each OS.
        box_family = font.nametofont('TkDefaultFont').actual('family')
        box_font_large = font.Font(family=box_family, size=17)
        box_font_small = font.Font(family=box_family, size=12)

        # the buttons are ttk widgets, so their look comes from a style
        self.btn_style = self._configure_button_style(qd_font_small)

        # create the header
        frm_header = tk.Frame(
            master=self.gui,
            background=self.qd_white,
            border=ViewTk._border_width_main_frames,
            relief=tk.RAISED,
            padx=10,
            pady=ViewTk._pad,
            )
        panel = tk.Label(master=frm_header,
                         image=self.logo_img,
                         background=self.qd_white,
                         borderwidth=0,
                         highlightthickness=0,
                         )
        # let column 0 absorb the extra width so the logo stays centered
        # once the header is stretched across the window
        frm_header.columnconfigure(0, weight=1)
        panel.grid(row=0, column=0)
        # The header is narrower than the info frame below it, so without
        # fill=X the root window shows through on both sides -- black under
        # macOS Dark Mode.  Stretching the header across removes the gap.
        frm_header.pack(fill=tk.X)

        # create the main info frame
        frm_info = tk.Frame(
            master=self.gui,
            background=self.qd_red,
            border=ViewTk._border_width_main_frames,
            relief=tk.SUNKEN,
            padx=ViewTk._pad,
            pady=ViewTk._pad,
            )

        # create an indicator to show connection status
        self.frm_connected = tk.Frame(
            master=frm_info,
            background=self.qd_red,
            padx=ViewTk._pad,
            pady=ViewTk._pad,
            )
        self._var_connected = tk.BooleanVar(value=False)
        self.lbl_connected_indicator = tk.Label(
            master=self.frm_connected,
            width=2,
            height=1,
            padx=ViewTk._pad,
            background=self.qd_grey,
            borderwidth=0,
            highlightthickness=0,
        )
        self.lbl_connected = tk.Label(
            master=self.frm_connected,
            font=qd_font_small,
            padx=ViewTk._pad,
            background=self.qd_red,
            fg=self.qd_white,
            borderwidth=0,
            highlightthickness=0,
        )
        self.lbl_connected_indicator.pack(fill=tk.BOTH, side=tk.LEFT)
        self.lbl_connected.pack(fill=tk.BOTH, side=tk.LEFT)

        # start server button
        self.btn_start = ttk.Button(
            master=frm_info,
            style=ViewTk._btn_style,
            width=10,
            command=lambda: self._start_btn_action()
        )
        self.btn_start.grid(row=0, column=2, sticky='e')
        btn_txt = self._get_start_btn_txt(self.start_button_enum.start)
        self.btn_start.config(text=btn_txt)

        # set the indicator light and start button
        self.server_status('closed')

        # ip address
        frm_address = tk.Frame(master=frm_info,
                               background=self.qd_red,
                               padx=ViewTk._pad,
                               pady=ViewTk._pad,
                               )
        lbl_ip_name = tk.Label(master=frm_address,
                               font=qd_font_status,
                               text='IP Address',
                               width=len('IP Address'),
                               background=self.qd_red,
                               fg=self.qd_white,
                               anchor='w',
                               justify='left',
                               )
        lbl_ip_name.grid(row=0, column=0, sticky='w')
        self.txt_ip = tk.Text(master=frm_address,
                              font=box_font_large,
                              height=1,
                              width=ViewTk._info_label_width,
                              relief=tk.SUNKEN,
                              border=ViewTk._border_width_main_frames,
                              borderwidth=ViewTk._border_width_main_frames,
                              background=self.qd_white,
                              fg=self.qd_black,
                              insertbackground=self.qd_black,
                              highlightthickness=0,
                              )
        self.txt_ip.grid(row=1,
                         column=0,
                         padx=ViewTk._pad,
                         ipady=ViewTk._pad,
                         )
        self.txt_ip.tag_configure('center', justify='center')
        self.txt_ip.tag_add('center', '1.0', tk.END)
        self.txt_ip.insert(tk.END, self._controller.ip_address)
        self.txt_ip.configure(state=tk.DISABLED)

        # port label
        lbl_port_name = tk.Label(master=frm_address,
                                 font=qd_font_status,
                                 text='Port Number',
                                 width=len('Port Number'),
                                 background=self.qd_red,
                                 fg=self.qd_white,
                                 anchor='w',
                                 justify='left',
                                 )
        lbl_port_name.grid(row=0, column=1, sticky='W')
        # port number
        self.ent_port = tk.Entry(master=frm_address,
                                 font=box_font_large,
                                 width=int(ViewTk._info_label_width / 2),
                                 relief=tk.SUNKEN,
                                 border=ViewTk._border_width_main_frames,
                                 borderwidth=ViewTk._border_width_main_frames,
                                 background=self.qd_white,
                                 fg=self.qd_black,
                                 insertbackground=self.qd_black,
                                 disabledbackground=self.qd_white,
                                 disabledforeground=self.qd_black,
                                 readonlybackground=self.qd_white,
                                 highlightthickness=0,
                                 )
        self.port = self._controller.model.port
        self.ent_port.grid(row=1, column=1,
                           sticky='e',
                           padx=ViewTk._pad,
                           ipady=ViewTk._pad,
                           )

        # number of connected indicator
        lbl_num_connected_name = tk.Label(master=frm_address,
                                          font=qd_font_status,
                                          text='Connected Clients',
                                          width=len('Connected Clients'),
                                          background=self.qd_red,
                                          fg=self.qd_white,
                                          anchor='w',
                                          )
        lbl_num_connected_name.grid(row=0, column=2, sticky='e')
        self.lbl_num_connected = tk.Label(
            master=frm_address,
            font=box_font_large,
            text=ViewTk._num_of_clients,
            padx=ViewTk._pad,
            background=self.qd_white,
            fg=self.qd_black,
            highlightthickness=0,
        )
        self.lbl_num_connected.grid(row=1, column=2, sticky='e')
        lbl_num_connected_name.grid_forget()
        self.lbl_num_connected.grid_forget()
        frm_address.grid(row=1, column=0, sticky='w')

        # flavor name
        # create a frame so that the alignment matches other widgets
        frm_flavor = tk.Frame(
            master=frm_info,
            background=self.qd_red,
            padx=ViewTk._pad,
            pady=ViewTk._pad,
            )
        self.lbl_flavor = tk.Label(
            master=frm_flavor,
            font=box_font_large,
            text='',
            width=ViewTk._info_label_width,
            relief=tk.SUNKEN,
            padx=ViewTk._pad,
            pady=ViewTk._pad,
            background=self.qd_white,
            fg=self.qd_black,
            border=ViewTk._border_width_main_frames,
            highlightthickness=0,
        )
        self.lbl_flavor.pack()
        frm_flavor.grid(row=2, column=0, sticky='w')

        # Output the command line info to the gui.  The vertical pad is
        # applied by grid() below rather than here, because a widget's own
        # -pady takes a single distance and this one is needed on the top
        # edge only.
        frm_readback = tk.Frame(master=frm_info,
                                background=self.qd_red,
                                padx=ViewTk._pad,
                                pady=0,
                                )
        lbl_readback_title = tk.Label(master=frm_readback,
                                      font=qd_font_small,
                                      background=self.qd_white,
                                      fg=self.qd_black,
                                      text='Server Status',
                                      border=ViewTk._border_width_main_frames,
                                      padx=ViewTk._pad,
                                      pady=ViewTk._pad,
                                      highlightthickness=0,
                                      )
        self.txt_readback = tk.Text(
            master=frm_readback,
            font=box_font_small,
            background=self.qd_white,
            fg=self.qd_black,
            insertbackground=self.qd_black,
            highlightthickness=0,
            width=55,
            height=8,
            state="disabled",
            )
        # Create vertical scroll bar and link it to the Text widget
        self.vertical_scrollbar = tk.Scrollbar(master=frm_readback,
                                               command=self.txt_readback.yview)
        self.txt_readback.configure(yscrollcommand=self.vertical_scrollbar.set)
        self.vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        lbl_readback_title.pack(fill=tk.BOTH)
        self.txt_readback.pack()
        # Pad the top only.  The Quit button shares this grid row and is
        # anchored south, so leaving the bottom unpadded puts the text
        # box's lower edge on the row boundary and the two line up --
        # independently of the font metrics on either platform.
        frm_readback.grid(row=3, column=0, sticky='w', pady=(ViewTk._pad, 0))

        # Quit button
        btn_quit = ttk.Button(
            master=frm_info,
            style=ViewTk._btn_style,
            text='Quit',
            command=lambda: self.quit_gui()
        )
        btn_quit.grid(row=3, column=2, sticky='se')

        frm_info.pack()

    @property
    def ip_address(self) -> str:
        """
        Returns the IP address being used by the Server

        Returns:
        --------
        string of the IP address
        """
        return self.txt_ip.get('1.0', tk.END)

    @ip_address.setter
    def ip_address(self, new: str):
        """
        Setter for the IP address
        """
        # change the state
        self.txt_ip.config(state=tk.NORMAL)
        # remove the current text
        self.txt_ip.delete(1.0, tk.END)
        # set the text
        self.txt_ip.insert(tk.END, new)
        # change the state back
        self.txt_ip.config(state=tk.DISABLED)

    @property
    def port(self) -> int:
        """
        Returns the port being used by the Server

        Returns:
        --------
        int with the port number.
        """
        try:
            p = int(self.ent_port.get())
        except AttributeError:
            p = self._controller.model.port
        return p

    @port.setter
    def port(self, new: int):
        """
        The setter for the Port number
        """
        # remove the current text
        self.ent_port.delete(0, tk.END)
        # set the text
        self.ent_port.insert(0, str(new))

    def get_connection_status(self) -> bool:
        """
        Returns True (False) if a client is connected (not connected)

        Returns:
        --------
        bool
        """
        return self._var_connected.get()

    def set_number_of_clients(self, num: int):
        """
        Updates the number of clients connected
        """
        ViewTk._num_of_clients = num
        self.lbl_num_connected.config(text=num)

    def server_status(self, server_status: str):
        """
        Updates the gui based on the server status
        """
        if server_status == 'closed':
            # hide the connection frame
            self.frm_connected.grid_remove()
            self._var_connected.set(False)
            # update the button text
            btn_text = self._get_start_btn_txt(self.start_button_enum.start)
        elif server_status == 'idle':
            # show the light
            self.frm_connected.grid(row=0, column=0, sticky='w')
            # turn the indicator light off
            self.lbl_connected_indicator.config(bg=self.qd_grey)
            self._var_connected.set(True)
            # update the button text
            btn_text = self._get_start_btn_txt(self.start_button_enum.stop)
        elif server_status == 'connected':
            # show the light
            self.frm_connected.grid(row=0, column=0, sticky='w')
            # turn the indicator light on
            self.lbl_connected_indicator.config(bg='green')
            self._var_connected.set(True)
            # update the button text
            btn_text = self._get_start_btn_txt(self.start_button_enum.stop)
        self.lbl_connected.config(text=server_status)
        self.btn_start.config(text=btn_text)

    def _get_start_btn_txt(self, btn_enum: start_button_enum) -> str:
        """
        Helper method to get the text on this button
        """
        if btn_enum == self.start_button_enum.start:
            return 'Start Server'
        elif btn_enum == self.start_button_enum.idle:
            return 'Waiting for Client'
        elif btn_enum == self.start_button_enum.stop:
            return 'Close Server'
        else:
            raise ValueError('Unknown option')

    def _start_btn_action(self):
        """
        Toggle between this button starting/stopping the server
        """
        with Lock():
            # server is not running and needs to be opened
            if self._controller.server_status() == 'closed':
                # redirect the output to the gui
                self.redirector = RedirectOutputToGui(self.txt_readback)
                instance = self._controller.start_server()

                # check if an instance was returned
                if not instance:
                    # Failed to start the server.  Check the IP address
                    self._controller.stop_server()
                    return None
            else:
                # stop the server
                self._controller.stop_server()

    @property
    def mvu_flavor(self):
        """
        Gets the flavor of the MultiVu which is running
        """
        return self.lbl_flavor['text']

    @mvu_flavor.setter
    def mvu_flavor(self, flavor):
        """
        The setter for the MultiVu flavor
        """
        self.lbl_flavor.config(text=flavor)
        self.lbl_flavor['text'] = flavor

    def start_gui(self):
        """
        Opens the gui window and runs the gui.
        """
        ViewTk.TK_RUNNING = True
        self.gui.mainloop()

    def quit_gui(self):
        """
        Close the gui and its window.
        """
        self._controller.stop_server()
        if self.redirector is not None:
            self.redirector.stop()
            self.redirector = None
        # Release the Tk variables before tearing down the
        # interpreter.  tkinter.Variable.__del__ calls back into Tcl,
        # so a variable which outlives .destroy() is finalized against
        # a dead interpreter whenever the garbage collector next runs.
        # That collection can happen on any thread once the server
        # threads are going, and Tcl responds to being touched from
        # the wrong thread by calling Tcl_Panic, which takes the whole
        # process down with
        #     Tcl_AsyncDelete: async handler deleted by the wrong thread
        # Dropping them here runs their __del__ while the interpreter
        # is still alive and while this is still the thread which
        # created them.
        for name, value in list(vars(self).items()):
            if isinstance(value, tk.Variable):
                setattr(self, name, None)
        gc.collect()
        self.gui.destroy()
        ViewTk.TK_RUNNING = False
