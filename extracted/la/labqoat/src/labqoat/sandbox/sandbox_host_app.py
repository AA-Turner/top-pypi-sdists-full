"""The function the platform runs on a machine of its own to host sandboxes created through ``labqoat.Sandbox``.

Clients never call it. A client publishes it once per project, when the platform first asks, and the platform then
launches it as often as the project's sandboxes need room, sized to a whole machine.
"""

from labqoat.compute.app import App
from labqoat.compute.sandboxes import Sandboxes
from labqoat.run_context import RunContext
from labqoat.sandbox.sandbox_host_service import SandboxHostService

app = App("labqoat-sandboxes")


@app.function(cpu=2, memory=2048, timeout=86_400, queue_timeout=3600, sandboxes=Sandboxes(Sandboxes.ANY, driver_gpu=0))
def host(context: RunContext) -> None:
    """Serve this machine's sandboxes to the platform until it says the host is no longer needed.

    The host keeps none of its machine's GPUs: all of them are its sandboxes'.
    """
    SandboxHostService(context).serve()
