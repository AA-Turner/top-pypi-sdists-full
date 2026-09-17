"""Loop-exhaustion contract for exported v4 while-loops."""


class LoopExhausted(Exception):
    """Raised by emitted code when a v4 while-loop consumes its iteration
    budget with ``on_exhaust="error"``."""
