# clipit/__init__.py

import os
import sys
import threading
import webbrowser

from PyQt5 import QtCore, QtWidgets

from .clipit import gui_main, gui_web
from .clipit.client import client_main
from .clipit.flask import abstract_clip_app


# ── ENVIRONMENT: force Qt into software OpenGL ─────────────────────────────────

# Disable hardware GLX/EGL:
os.environ["QT_XCB_GL_INTEGRATION"] = "none"
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseSoftwareOpenGL)


# ── FLASK LAUNCHER ───────────────────────────────────────────────────────────────

def run_flask(port: int | None = None) -> None:
    """
    Start the Flask app on `port` (defaults to 7823), then open the browser.
    """
    port = port or 7823
    app = abstract_clip_app()
    url = f"http://127.0.0.1:{port}/drop-n-copy.html"

    print(f"→ Opening browser to: {url}")
    # Slight delay so Flask has time to bind before opening the browser:
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    app.run(debug=True, port=port)


# ── MODE DISPATCHER ──────────────────────────────────────────────────────────────

def initialize_clipit(choice: str = "display", *, port: int | None = None, url: str | None = None) -> None:
    """
    Dispatch based on `choice`:
      - "display": run the PyQt GUI (`gui_main`)
      - "web":     run the PyQt web‐view GUI (`gui_web(url)`)
      - "client":  run the CLI client (`client_main`)
      - "script":  (not implemented)
      - "flask":   launch the Flask + browser (`run_flask(port)`)
    """
    choice = choice.lower()
    if choice == "display":
        gui_main()

    elif choice == "web":
        if not url:
            raise ValueError("When choice=='web', you must pass a `url` argument.")
        gui_web(url)

    elif choice == "client":
        client_main()

    elif choice == "script":
        print("Running in script mode (not implemented).")

    elif choice == "flask":
        run_flask(port=port)

    else:
        raise ValueError(f"Unknown mode: {choice!r}")


# ── ENTRY POINT ─────────────────────────────────────────────────────────────────

def clipit_main(*argv: str) -> None:
    """
    Parse sys.argv and call initialize_clipit appropriately.

    Usage patterns:
      $ python -m clipit               →   display mode
      $ python -m clipit display       →   display mode
      $ python -m clipit web  http://… →   web mode
      $ python -m clipit flask 7823    →   flask mode
      $ python -m clipit client        →   client mode
    """
    # argv[0] is the module name (e.g. "-m clipit"); so look at argv[1], argv[2]
    if len(argv) < 2:
        # No mode specified → default to "display"
        initialize_clipit("display")
        return

    choice = argv[1].lower()

    if choice == "web":
        # Expect: python -m clipit web <url>
        url = argv[2] if len(argv) >= 3 else None
        initialize_clipit("web", url=url)

    elif choice == "flask":
        # Expect: python -m clipit flask <port>
        port_str = argv[2] if len(argv) >= 3 else None
        port = int(port_str) if port_str and port_str.isdigit() else None
        initialize_clipit("flask", port=port)

    else:
        # display, client, script, or unrecognized mode
        initialize_clipit(choice)


def get_clipit():
    clipit_main(*sys.argv)
