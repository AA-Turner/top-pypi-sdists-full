"""V3 Playwright JS-dialog handling — prime a persistent accept/dismiss policy.

Playwright auto-dismisses a JavaScript dialog (alert / confirm / prompt) unless
a ``page.on("dialog")`` listener is registered BEFORE the action that opens it.
The code generator records the dialog-response operation AFTER the action that triggers the
dialog (instruction N = trigger, N+1 = JS_DIALOG — the Selenium post-hoc order),
so the Selenium ``switch_to.alert`` approach is impossible on Playwright: by the
time the JS_DIALOG op runs the dialog has already been auto-dismissed.

The fix is a permanent handler primed up-front. ``prime_dialog`` registers ONE
idempotent, page-scoped ``dialog`` listener and mutates a per-page policy that
the listener consults for every dialog. The code generator primes it from the test
preamble (before any trigger fires) with the first dialog's policy, and again at
each authored JS_DIALOG op (updating the policy for subsequent dialogs).

This is the driver-scoped, selectorless counterpart to the Selenium binding's
``handle_alert`` — dialogs have no element/frame, so there is no locator here.
"""
from __future__ import annotations

import asyncio
from weakref import WeakKeyDictionary

_DEFAULT_POLICY = {"action": "dismiss", "value": ""}

# Per-page policy + registration tracking. Keyed weakly so a closed/GC'd page
# auto-evicts (and never collides via id() reuse). Playwright Page objects are
# regular, weak-referenceable, id()-hashable objects.
_dialog_policies: "WeakKeyDictionary" = WeakKeyDictionary()
_handler_registered: "WeakKeyDictionary" = WeakKeyDictionary()


async def prime_dialog(page, *, action: str = "dismiss", value: str = "") -> None:
    """Arm/refresh the JS-dialog policy for ``page`` and ensure a live listener.

    Idempotent per page: the ``page.on("dialog")`` listener is registered exactly
    once; subsequent calls only update the policy (``action`` + prompt ``value``)
    that the listener applies to every future dialog.

    Args:
        page:   The Playwright ``Page``.
        action: ``"accept"`` or ``"dismiss"`` (case-insensitive; default dismiss).
        value:  Text typed into a prompt when accepting (ignored on dismiss).

    Async (returns a coroutine) so generated code can ``await`` it uniformly with
    the other ``testmu`` page helpers; it performs no I/O itself.
    """
    _dialog_policies[page] = {
        "action": (action or "dismiss").strip().lower(),
        "value": value or "",
    }

    if _handler_registered.get(page):
        return

    def _on_dialog(dialog) -> None:
        policy = _dialog_policies.get(page, _DEFAULT_POLICY)
        if policy["action"] == "accept":
            coro = dialog.accept(policy["value"]) if policy["value"] else dialog.accept()
        else:
            coro = dialog.dismiss()
        # page.on dispatches the listener synchronously; accept()/dismiss() are
        # coroutines in the async API, so schedule the resolution on the running
        # loop. The triggering action (await page.click(...)) yields control,
        # letting the loop run this task and unblock the dialog.
        asyncio.ensure_future(coro)

    page.on("dialog", _on_dialog)
    _handler_registered[page] = True


__all__ = ["prime_dialog"]
