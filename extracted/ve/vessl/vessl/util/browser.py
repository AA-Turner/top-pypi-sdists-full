import webbrowser

bypass_browsers = ["www-browser", "links", "lynx", "elinks", "w3m"]


def try_open_gui_browser(url: str) -> bool:
    """
    Open a browser window to the specified URL.
    """

    try:
        default_browser = webbrowser.get()
    except webbrowser.Error:
        return False

    if default_browser in bypass_browsers:
        return False  # Don't open a browser if the default is a text-based browser

    webbrowser.open(url)

    return True
