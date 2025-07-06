"""Backward compatibility for ActionTracker"""

from matrice.action_tracker import ActionTracker, _dotdict, LocalActionTracker

class ActionTracker(ActionTracker):
    """Backward compatibility for ActionTracker"""
    pass

class LocalActionTracker(LocalActionTracker):
    """Backward compatibility for LocalActionTracker"""
    pass

class _dotdict(_dotdict):
    """Backward compatibility for _dotdict"""
    pass
