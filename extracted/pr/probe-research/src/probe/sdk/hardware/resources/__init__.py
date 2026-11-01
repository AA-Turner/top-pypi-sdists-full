"""Hardware sources, one contract: ``probe()`` once for static inventory, ``sample(ts)`` per tick.
Every ``create()`` is an availability probe returning None when its substrate is absent, so absent hardware costs nothing."""
