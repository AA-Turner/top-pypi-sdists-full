# encoding: utf-8

import logging_helper
from ..tk_names import EW, NORMAL
from ..window.child import ChildWindow
from ..widget.button import Button
from ..helper.arguments import Position, grid_and_non_grid_kwargs
from .frame import BaseFrame
from .label import BaseLabelFrame

logging = logging_helper.setup_logging()


class LauncherMixIn(object):

    BUTTON_WIDTH = 20

    def __init__(self,
                 window_class=ChildWindow,
                 *args,
                 **kwargs):
        super(LauncherMixIn, self).__init__(*args,
                                            **kwargs)

        self.subwindow_class = window_class
        self.sub_windows = {}

        self.groups = {}
        self.launcher_buttons = {}

    def close(self):
        for name in self.sub_windows:
            logging.info(u'Exiting {w}'.format(w=name))

            try:
                self.sub_windows[name].exit()

            except Exception as err:
                logging.error(u'Something went wrong while exiting window: {w}'.format(w=name))
                logging.error(err)

        for name in self.groups:
            logging.info(u'Exiting {g}'.format(g=name))

            try:
                self.groups[name].exit()

            except Exception as err:
                logging.error(u'Something went wrong while exiting launcher group: {g}'.format(g=name))
                logging.error(err)

        self.groups = {}
        self.sub_windows = {}
        self.launcher_buttons = {}

    def add_launcher_group(self,
                           name,
                           **kwargs):

        self._update_grid_kwargs(kwargs)

        self.groups[name] = self.add_frame(frame=LauncherGroupFrame,
                                           parent=self,
                                           title=name,
                                           **kwargs)

        return self.groups[name]

    def add_launcher(self,
                     name,
                     button_text=None,
                     button_state=NORMAL,
                     button_tooltip=None,
                     # window_class=None,
                     *args,
                     **kwargs):

        grid_kwargs, non_grid_kwargs = self._update_grid_kwargs(kwargs)

        self.launcher_buttons[name] = Button(text=button_text if button_text is not None else name,
                                             state=button_state,
                                             width=self.BUTTON_WIDTH,
                                             command=lambda: self._launch_window(name=name,
                                                                                 *args,
                                                                                 **non_grid_kwargs),
                                             tooltip=button_tooltip,
                                             **grid_kwargs)

        return self.launcher_buttons[name]

    def add_show_hide(self,
                      name,
                      button_text=None,
                      button_state=NORMAL,
                      button_tooltip=None,
                      init=True,
                      # hidden=False,
                      # window_class=None,
                      *args,
                      **kwargs):

        """ Adds a window launcher that will keep window state when closed.

        :param name:            Window Name
        :param button_text:     Test displayed on the launcher button if difrerent from name
        :param button_state:    Startup state of the button NORMAL / DISABLED
        :param button_tooltip:  Tooltip to show for button
        :param init:            If True pre initialise the window.  (Hidden can be True / False)
                                If False window is initialised on first click.  (Hidden should be False)
        :param args:
        :param kwargs:
        :return:
        """

        grid_kwargs, non_grid_kwargs = self._update_grid_kwargs(kwargs)

        if init:
            self._show_hide_window(name=name,
                                   *args,
                                   **non_grid_kwargs)

        self.launcher_buttons[name] = Button(text=button_text if button_text is not None else name,
                                             state=button_state,
                                             width=self.BUTTON_WIDTH,
                                             command=lambda: self._show_hide_window(name=name,
                                                                                    *args,
                                                                                    **non_grid_kwargs),
                                             tooltip=button_tooltip,
                                             **grid_kwargs)

        return self.launcher_buttons[name]

    def _update_grid_kwargs(self,
                            kwargs):

        if u'row' not in kwargs:
            kwargs[u'row'] = Position.START if not self.groups and not self.launcher_buttons else Position.NEXT

        if u'column' not in kwargs:
            kwargs[u'column'] = Position.CURRENT

        if u'sticky' not in kwargs:
            kwargs[u'sticky'] = EW

        return grid_and_non_grid_kwargs(**kwargs)

    def _create_window(self,
                       name,
                       window_class=None,
                       *args,
                       **kwargs):

        if window_class is None:
            window_class = self.subwindow_class

        # Add parent to window kwargs
        window_kwargs = kwargs.get(u'window_kwargs', {})
        window_kwargs[u'parent'] = self
        kwargs[u'window_kwargs'] = window_kwargs

        # Create window
        if name not in self.sub_windows:
            # Window not registered yet so lets open it
            self.sub_windows[name] = window_class(title=name,
                                                  *args,
                                                  **kwargs)

        else:
            # You should not get here!  But just in case...  Log a warning.
            logging.warning(u'Not creating window, there is already a definition for {w}'.format(w=name))

    def _launch_window(self,
                       name,
                       # window_class=None,
                       *args,
                       **kwargs):

        # Activate window
        if name not in self.sub_windows:
            # Window not registered yet so lets open it
            self._create_window(name=name,
                                *args,
                                **kwargs)

        elif not self.sub_windows[name].exists():
            # Window is registered but no longer open, so:
            # Clean it up
            self.sub_windows[name].close()
            self.sub_windows[name].destroy()
            del self.sub_windows[name]

            # Re-open it
            self._create_window(name=name,
                                *args,
                                **kwargs)

        elif self.sub_windows[name].state() == u'withdrawn':
            self.sub_windows[name].show()

        else:
            # Window is open so bring to front
            self.sub_windows[name].make_active_window()

    def _show_hide_window(self,
                          name,
                          hidden=False,
                          window_class=None,
                          *args,
                          **kwargs):

        if name not in self.sub_windows:
            # Add ensure os_closable is in window kwargs
            window_kwargs = kwargs.get(u'window_kwargs', {})
            window_kwargs[u'os_closable'] = False
            kwargs[u'window_kwargs'] = window_kwargs

            # Create window
            self._create_window(name=name,
                                window_class=window_class,
                                *args,
                                **kwargs)

            # Hide window if default is hidden
            if hidden:
                self.sub_windows[name].hide()

        else:
            if self.sub_windows[name].state() == u'withdrawn':
                self.sub_windows[name].show()

            else:
                self.sub_windows[name].hide()

    def nice_groups(self,
                    *args,
                    **kwargs):
        for group_name, group in iter(self.groups.items()):
            group.nice_grid(*args, **kwargs)


class LauncherGroupFrame(LauncherMixIn,
                         BaseLabelFrame):
    pass


class LauncherFrame(LauncherMixIn,
                    BaseFrame):
    pass
