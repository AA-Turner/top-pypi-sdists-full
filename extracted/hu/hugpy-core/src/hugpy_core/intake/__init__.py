"""Wrapper observations mirrored into Core's database by one collector.

Core components read committed tables directly. Both standalone and embedded
intake use the same service and durable worker registrations.
"""


def start():
    from hugpy_core.intake.feed import start as start_collector
    return start_collector()


__all__ = ['start']
