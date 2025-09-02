# encoding: utf-8

from future.builtins import str

try:
    import win32gui
except ImportError:
    # I guess we are not on Windows!
    pass


def window_handles():
    u"""
    Get the window handles for all windows (on Windows)

    On other platforms, will return an empty dictionary

    return : {window name 1 : handle,
              ...
              window name N : handle}

    e.g. {'DB Browser for SQLite':         659978,
          'ITT':                           1575924,
          'Microsoft Outlook':             66840,
          'Microsoft Word':                68296,
          'Outlook Send/Receive Progress': 724146,
          'SourceTree':                    3736990,
          'Start':                         65658,
          'Start menu':                    262346,
          'Windows Task Manager':          262604,
    """
    handles = {}

    def append_window_handle(hwnd, ctx ):
        title = win32gui.GetWindowText(hwnd)
        if title:
            handles[win32gui.GetWindowText(hwnd)] = hwnd

    try:
        win32gui.EnumWindows(append_window_handle, None)
    except NameError:
        # Not on windows.
        pass

    return handles


def window_titles():
    return window_handles().keys()


def window_is_already_open(title):
    unicode_titles = []
    for str_title in window_titles():
        try:
            unicode_titles.append(str(str_title))
        except UnicodeDecodeError:
            pass

    return title in unicode_titles


def switch_to_window(title):
    handle = window_handles().get(title, None)
    if handle:
        try:
            win32gui.SetForegroundWindow(handle)
        except NameError:
            pass


if __name__ == u"__main__":
    import pprint
    pprint.pprint(window_handles())
    pprint.pprint(window_titles())
    switch_to_window(u'Microsoft Outlook')
