"""Release-status Slack message, split into three layers so the model and the
rendering evolve independently of the Slack transport (and the rendering /
chunking is testable as pure functions):

- ``state``  — the :class:`ReleaseState` model, track table and transitions.
- ``render`` — pure Block Kit / plain-text rendering + chunking.
- ``cli``    — the ``release-status`` command and its Slack transport.
"""
