# encoding: utf-8

import os
import sys
import platform
import logging_helper
from future.builtins import str
from uiutil.tk_names import NSEW, FALSE
from ..mixin.var import VarMixIn
from ..mixin.frames import FramesMixIn
from ..frame.frame import BaseFrame
from ..mixin.layout import LayoutMixIn

logging = logging_helper.setup_logging()


class BaseWindow(LayoutMixIn,
                 VarMixIn,
                 FramesMixIn):

    def __init__(self,
                 width=None,
                 height=None,
                 x=None,
                 y=None,
                 parent_geometry=None,
                 auto_resize=True,
                 layout=None,
                 fixed=False,
                 center=False,
                 icon_path=None,
                 padding=None,
                 borderless=False,
                 os_closable=True,
                 *args,
                 **kwargs):

        super(BaseWindow, self).__init__(*args, **kwargs)

        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.parent_geometry = parent_geometry
        self.center = center
        self.auto_resize = auto_resize
        self.fixed = fixed
        self.padding = padding
        self.borderless = borderless
        self.os_closable = os_closable

        # Set window title
        try:
            title = self.window_title

        except AttributeError:
            title = u'Base Window'

        if sys.gettrace():
            title += u' (Debugging)'

        self.title(title)

        # Set app window icon
        if icon_path:
            self.wm_iconbitmap(icon_path)

        self._main_frame = BaseFrame(self,
                                     layout=layout,
                                     padx=0,
                                     pady=0,
                                     padding=(u'10 10 10 10'
                                              if self.padding is None
                                              else self.padding))

        if self.borderless:
            self.overrideredirect(1)  # Setting this to 1 makes window borderless (plus no OS close button)

        self._draw_widgets()
        self.__configure_main_frame()

        self.__position()

        if self.os_closable:
            # OS Close button is allowed to close window
            # Associate window close button to our exit method
            self.wm_protocol(u'WM_DELETE_WINDOW', self.exit)

        else:
            # OS Close button is not allowed to close window
            # Associate window close button to our hide method
            self.wm_protocol(u'WM_DELETE_WINDOW', self.hide)

        # Expand to fit
        self._main_frame.nice_grid()
        self.nice_grid()

        self._post_setup()

    def exists(self):
        return self._main_frame.exists()

    def show(self):
        self.update()
        self.deiconify()

    def hide(self):
        self.withdraw()

    def make_active_window(self):
        self.lift()
        self.grab_set()
        self.focus()
        self.grab_release()

    def make_active_application(self):
        self.make_active_window()

        # Little workaround for OS X to activate window!
        # (may not get the correct python if more than one active python process)
        if platform.system() == u'Darwin':
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "python" to true' ''')

    def __configure_main_frame(self):

        if not self.auto_resize:
            self._main_frame.grid_propagate(0)

        self._main_frame.grid(sticky=NSEW)

    def __position(self):

        self.update_idletasks()

        # Extract individual default geometry values
        default_width = self.winfo_width()
        default_height = self.winfo_height()
        default_x = self.winfo_x()
        default_y = self.winfo_y()

        # Extract individual parent geometry values
        if self.parent_geometry:
            (parent_size,
             parent_x,
             parent_y) = self.parent_geometry.split(u'+')

            (parent_width,
             parent_height) = parent_size.split(u'x')

            parent_x_center = int(parent_x) + (int(parent_width) // 2)
            parent_y_center = int(parent_y) + (int(parent_height) // 2)

        else:
            parent_x_center = 0
            parent_y_center = 0

        # Check for window width & height being explicitly defined
        if not self.width:
            self.width = default_width

        if not self.height:
            self.height = default_height

        # Constrain Window size to the max screen size
        self.__constrain_window()

        # Check for window x & y being explicitly defined
        if not self.x:
            if self.parent_geometry:
                # Center window over parent window
                self.x = parent_x_center - self.width // 2

            else:
                if self.center:
                    # Center on display
                    self.x = self.winfo_screenwidth() // 2 - self.width // 2

                else:
                    self.x = default_x

        if not self.y:
            if self.parent_geometry:
                # Center window over parent window
                self.y = parent_y_center - self.height // 2

            else:
                if self.center:
                    # Center on display
                    self.y = self.winfo_screenheight() // 2 - self.height // 2

                else:
                    self.y = default_y

        # Ensure window is actually on the screen
        self.__validate_position()

        # Update geometry
        self.geometry(u'{w}x{h}+{x}+{y}'.format(w=self.width,
                                                h=self.height,
                                                x=self.x,
                                                y=self.y))

        self.update_idletasks()

    def __constrain_window(self):

        # Constrain Window size to the max screen size
        if self.width > self.winfo_screenwidth():
            self.width = self.winfo_screenwidth()

        if self.height > self.winfo_screenheight():
            self.height = self.winfo_screenheight()

        self.minsize(self.width,
                     self.height)

        if self.fixed:
            # TODO: Figure out why this breaks combobox
            self.resizable(width=FALSE,
                           height=FALSE)

    def __validate_position(self):

        if self.x is None:
            self.x = 0

        if self.y is None:
            self.y = 0

        # Ensure window is actually on the screen
        if (self.x + self.width) > self.winfo_screenwidth():
            self.x = self.winfo_screenwidth() - self.width

        if self.x < 0:
            self.x = 0

        if (self.y + self.height) > self.winfo_screenheight():
            self.y = self.winfo_screenheight() - self.height

        if self.y < 0:
            self.y = 0

    def exit(self):

        # Withdraw the window so its hidden while we perform a clean exit
        self.withdraw()

        # Call our close method
        self.close()

        # Call frame close methods
        try:
            self._main_frame.exit()

        except Exception as err:
            logging.error(u'Something went wrong while exiting main_frame '
                          u'for window: {w}'.format(w=self))
            logging.exception(err)

        self.exit_frames()

        # Finally destroy the window
        self.destroy()

    def close(self):

        """
        Override this to perform steps when the window is closed
        """

        pass

    def _draw_widgets(self):

        """
        Override this to add your widgets to the window

        self._mainframe: This is the root frame you should use to place widgets.
        self.title: Set title for window.
        """

        self._setup()  # TODO: self._setup is deprecated but we need to call it for compatibility for a while!
        pass

    def _setup(self):

        """ This method is deprecated as it overrides existing BaseWidget._setup
            when merged with tk window classes and will soon be removed to allow
            BaseWidget._setup to run again!

        """

        pass

    def _post_setup(self):

        """
        Override this to perform any setup that is required once the window has been drawn!
        """

        pass

    def update_geometry(self):

        self.update_idletasks()
        self._main_frame.update_idletasks()

        # Extract current geometry values
        current_width = self.winfo_width()
        current_height = self.winfo_height()
        current_x = self.winfo_x()
        current_y = self.winfo_y()

        # Extract size of self._main_frame
        if self._main_frame.winfo_reqwidth() != self._main_frame.winfo_width():
            new_width = self._main_frame.winfo_reqwidth()

        else:
            new_width = self._main_frame.winfo_width()

        if self._main_frame.winfo_reqheight() != self._main_frame.winfo_height():
            new_height = self._main_frame.winfo_reqheight()

        else:
            new_height = self._main_frame.winfo_height()

        # Get current centre
        x_centre = current_x + current_width // 2
        y_centre = current_y + current_height // 2

        # Update window size to match self._main_frame
        self.width = new_width
        self.height = new_height

        # Centre re-sized window over previous window configuration
        self.x = x_centre - self.width // 2
        self.y = y_centre - self.height // 2

        # Validate
        self.__constrain_window()
        self.__validate_position()

        # Update geometry
        self.geometry(u'{w}x{h}+{x}+{y}'.format(w=self.width,
                                                h=self.height,
                                                x=self.x,
                                                y=self.y))

        self.update_idletasks()

