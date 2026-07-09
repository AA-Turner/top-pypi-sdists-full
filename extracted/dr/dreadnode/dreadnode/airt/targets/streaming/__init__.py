"""Streaming target adapters (realtime / speech-to-speech protocols).

Each adapter drives a bespoke stateful handshake but presents the same ``@task``
interface as the HTTP transport, so attacks treat them interchangeably.
"""

from dreadnode.airt.targets.streaming.nova_sonic import nova_sonic_target

__all__ = ["nova_sonic_target"]
