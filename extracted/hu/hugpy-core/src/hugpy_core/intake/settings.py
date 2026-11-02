"""Retired automatic settings replay; wrapper observations never trigger writes.

Explicit operator changes use intake.wrapper_settings.command. Kept as inert
entry points for older startup callers; cached observations are not commands.
"""

def start():
    return None


def sync_box(worker):
    return 0
