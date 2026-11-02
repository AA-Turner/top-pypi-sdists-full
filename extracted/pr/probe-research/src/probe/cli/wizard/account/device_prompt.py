"""the device-flow prompt (browser URL + user code) every sign-in prints."""

from __future__ import annotations
from ....sdk.settings.device import DevicePrompt


def _show_device_prompt(prompt: DevicePrompt) -> None:
    """Print the browser URL + user code for a device-flow approval. One definition,
    reused by every command that mints via the device flow (login, token, mcp).

    FLUSHED for the same reason `tui.Progress.render` is: every caller prints
    this and then blocks polling for an approval that cannot arrive until a
    human reads it. Under a pipe -- an agent's shell tool, a CI log -- an
    unflushed write stays in the buffer for the whole poll, so the caller waits
    on a human who was never shown the code, and the command looks like a hang.
    """
    print(f"  visit: {prompt.verification_uri_complete}", flush=True)
    print(f"  code:  {prompt.user_code}", flush=True)
