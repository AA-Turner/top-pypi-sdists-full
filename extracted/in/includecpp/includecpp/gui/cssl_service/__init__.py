"""
CSSL Service Manager - Runtime control & introspection tool.
Launch via: includecpp cssl service
"""


def launch_service_manager():
    """Entry point: create and run the CSSL Service Manager window."""
    from .app import CSSLServiceApp
    app = CSSLServiceApp()
    app.mainloop()
