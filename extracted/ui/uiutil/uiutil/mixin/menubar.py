# encoding: utf-8

import attr
import logging_helper
import inspect
from tkinter import Menu
from tkinter.constants import FALSE, DISABLED
from tkinter.messagebox import showinfo
from classutils.decorators import profiling

logging = logging_helper.setup_logging()


class MenuNotEnabled(Exception):
    pass


@attr.s(frozen=True)
class _OptionTypes(object):
    command = attr.ib(default=u'command', init=False)
    separator = attr.ib(default=u'separator', init=False)
    radiobutton = attr.ib(default=u'radiobutton', init=False)
    checkbutton = attr.ib(default=u'checkbutton', init=False)
    heading = attr.ib(default=u'heading', init=False)


OptionTypes = _OptionTypes()


class MenuBarMixIn(object):

    DEBUG_MENU_ENABLED = False

    def enable_menubar(self):

        # Debug Menu Variables
        self._debug_enabled = None
        self._profiling_enabled = None
        self._profilers_enabled = {}

        self.window_platform = self.tk.call('tk', 'windowingsystem')  # Returns x11, win32 or aqua depending on platform

        self.primary_modifier = "Cmd" if self.window_platform == u'aqua' else "Ctrl"

        self.menu_app_name = False

        # Without this each of your menus (on Windows and X11) will start with what looks like a dashed line,
        # and allows you to "tear off" the menu so it appears in its own window. We don't want this!
        self.option_add('*tearOff', FALSE)

        # Create our windows menubar object!
        self.menubar = Menu(self)

        # Ordering here is important!
        self._app_menus()
        self.add_user_menus()

        if self.DEBUG_MENU_ENABLED:
            self._debug_menus()

        self._window_help_menus()  # Must be last for Help to be in the correct place!

        # Attach menubar to window
        self.config(menu=self.menubar)  # We have to do this last for OSX so we don't get a duplicate app menu!

    def show_about(self):

        """ Override to launch an about window """

        showinfo(u"About",
                 u"No about window has been defined",
                 icon=u'info',
                 parent=self)

    def show_preferences(self):

        """ Override to launch a preferences window """

        showinfo(u"Preferences",
                 u"No preferences window has been defined",
                 icon=u'info',
                 parent=self)

    def show_help(self):

        """ Override to launch a help window """

        showinfo(u"Help",
                 u"No help window has been defined",
                 icon=u'info',
                 parent=self)

    def _menubar_check(self):
        try:
            self.menubar
        except AttributeError as e:
            logging.exception(e)
            raise MenuNotEnabled('Cannot call {fn} if menubar has not been enabled.'
                                 .format(fn=inspect.stack()[1][3]))

    def add_menu(self,
                 config):

        self._menubar_check()

        kwargs = config.get(u'init_kwargs', {})

        menu = Menu(self.menubar,
                    **kwargs)

        for option in config.get(u'options', []):
            option_type = option.get(u'type')
            option_kwargs = option.get(u'option_kwargs', {})

            if option_type is not None:
                if option_type == OptionTypes.command:
                    menu.add_command(**option_kwargs)

                elif option_type == OptionTypes.separator:
                    menu.add_separator(**option_kwargs)

                elif option_type == OptionTypes.radiobutton:
                    menu.add_radiobutton(**option_kwargs)

                elif option_type == OptionTypes.checkbutton:
                    menu.add_checkbutton(**option_kwargs)

                elif option_type == OptionTypes.heading:
                    option_kwargs[u'state'] = DISABLED
                    menu.add_command(**option_kwargs)

        cascade_kwargs = config.get(u'cascade_kwargs', {})

        self.menubar.add_cascade(menu=menu,
                                 **cascade_kwargs)

    def add_user_menus(self):

        """ Override this method to draw any menus you require for your app

            Note: The Help menu will be added automatically on all platforms
                  plus the app & window menus will also be drawn on OSX.

            Menus can be added by calling self.add_menu.

        """

        pass

    # Built-in Menus
    def _app_menus(self):

        # Create App menu (Mac only)
        if self.window_platform == u'aqua':
            # This ordering must not change!
            cfg = {
                u'init_kwargs': {u'name': u'apple'},
                u'options': [
                    {
                        u'type': OptionTypes.command,
                        u'option_kwargs': {
                            u'label': u'About {app}'.format(app=self.menu_app_name)
                            if self.menu_app_name else u'About...',
                            u'command': self.show_about
                        }
                    },
                    {
                        u'type': OptionTypes.separator
                    }
                ]
            }

            self.add_menu(config=cfg)

            # Preferences
            self.createcommand('tk::mac::ShowPreferences', self.show_preferences)

    def _window_help_menus(self):

        # Window menu on OSX
        if self.window_platform == u'aqua':
            window_cfg = {
                u'init_kwargs': {u'name': u'window'},
                u'cascade_kwargs': {u'label': u'Window'}
            }

            self.add_menu(config=window_cfg)

        # Create Help menu
        help_cfg = {
            u'init_kwargs': {u'name': u'help'},
            u'cascade_kwargs': {u'label': u'Help'}
        }

        if self.window_platform == u'aqua':
            # OSX can setup a help menu all by itself if we set this!
            self.createcommand('tk::mac::ShowHelp', self.show_help)

        else:
            # Not OSX so lets setup a help menu.
            # Also adding the about & preferences menu items (these reside in the app menu on OSX)
            help_cfg[u'options'] = [
                {
                    u'type': OptionTypes.command,
                    u'option_kwargs': {
                        u'label': u'About {app}'.format(app=self.menu_app_name) if self.menu_app_name else u'About...',
                        u'command': self.show_about
                    }
                },
                {
                    u'type': OptionTypes.command,
                    u'option_kwargs': {
                        u'label': u'Show Help',
                        u'command': self.show_help,
                        u'accelerator': "{mod}-?".format(mod=self.primary_modifier)
                    }
                },
                {
                    u'type': OptionTypes.separator
                },
                {
                    u'type': OptionTypes.command,
                    u'option_kwargs': {
                        u'label': u'Preferences',
                        u'command': self.show_preferences,
                        u'accelerator': "{mod}-,".format(mod=self.primary_modifier)
                    }
                }
            ]

        self.add_menu(config=help_cfg)  # Must be last menu added for OSX

    def _debug_menus(self):

        # Menu Variables
        self._debug_enabled = self.boolean_var(value=False,
                                               trace=self._debug)
        self._profiling_enabled = self.boolean_var(value=False,
                                                   trace=self._profile)

        # Config Menu
        cfg = {
            u'cascade_kwargs': {u'label': u'Debug'},
            u'options': [
                {
                    u'type': OptionTypes.command,
                    u'option_kwargs': {
                        u'label': u'Dump logging tree',
                        u'command': logging.dump_tree
                    }
                },
                {
                    u'type': OptionTypes.separator
                },

                {
                    u'type': OptionTypes.checkbutton,
                    u'option_kwargs': {
                        u'label': u'Debug',
                        u'variable': self._debug_enabled,
                        u'onvalue': True,
                        u'offvalue': False
                    }
                },
                {
                    u'type': OptionTypes.checkbutton,
                    u'option_kwargs': {
                        u'label': u'Profile',
                        u'variable': self._profiling_enabled,
                        u'onvalue': True,
                        u'offvalue': False
                    }
                },
                {
                    u'type': OptionTypes.separator
                },
                {
                    u'type': OptionTypes.heading,
                    u'option_kwargs': {
                        u'label': u'Profilers'
                    }
                }
                # Profilers get added here
            ]
        }

        for profiler in profiling.profilers.registered_profiles:
            if profiler is not None:
                self._profilers_enabled[profiler] = self.boolean_var(value=False,
                                                                     trace=lambda:
                                                                     self._individual_profilers(profile_id=profiler))

                profiler_menu_cfg = {
                    u'type': OptionTypes.checkbutton,
                    u'option_kwargs': {
                        u'label': u'{profiler}'.format(profiler=profiler),
                        u'variable': self._profilers_enabled[profiler],
                        u'onvalue': True,
                        u'offvalue': False
                    }
                }

                cfg[u'options'].append(profiler_menu_cfg)

        self.add_menu(config=cfg)

    # Debug menu methods
    def _debug(self):

        if self._debug_enabled is not None:
            if self._debug_enabled.get():
                logging_helper.getLogger().lh_set_console_level(logging_helper.DEBUG)
                logging_helper.getLogger().lh_set_file_level(logging_helper.DEBUG)
                logging.debug(u'********** Debug logging enabled **********')

            else:
                logging_helper.getLogger().lh_set_console_level(logging_helper.INFO)
                logging_helper.getLogger().lh_set_file_level(logging_helper.INFO)
                logging.info(u'********* Debug logging disabled **********')

    def _profile(self):

        if self._profiling_enabled is not None:
            if self._profiling_enabled.get():
                profiling.enable()
                logging.info(u'************ Profiling enabled ************')

            else:
                profiling.disable()
                logging.info(u'*********** Profiling disabled ************')

    def _individual_profilers(self,
                              profile_id):

        if profile_id is not None:
            if self._profilers_enabled[profile_id].get():
                profiling.enable(profile_id=profile_id)

            else:
                profiling.disable(profile_id=profile_id)
