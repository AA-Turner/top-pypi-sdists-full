"""
What `Policy.ready()` answers (Ready).

An act's own answer is what the policy's act function returned, as it returned it: nothing here wraps it.


"""

from __future__ import annotations


class Ready(tuple):
    """
    What `Policy.ready()` answers: `(ready, eta_s)`, unpacked - `ready, eta = policy.ready()` - and, once a
    worker serves, the card it runs on, read as attributes:

    - `card`: the deployment's card ("L4", "H100:2");
    - `usd_per_hour`: what one worker costs an hour on it, as billed (the price `seq policy status` says for it).

    Each None while no worker serves, or for a worker on CPU.

    While this robot waits in line for a slot (the deployment holds its `max_gpus` with every slot taken), `ready` is
    False and these say where it stands:

    - `queued`: True while it waits in line;
    - `queue_position`: its place (1 = next to be served);
    - `eta_s`: about how long until it can serve, when that can be estimated from how long the robots ahead keep their
      slot - else None, with `eta_unknown` saying why ("no_history", "past_average", "not_measured").

    While a worker starts for it, `eta_s` counts down to when the start should serve; past that it is None, with
    `eta_unknown` "past_expected": the start takes longer than it should (most often waiting for its card), and how
    long it may wait for one is the platform's start wait.


    """

    card: str | None
    usd_per_hour: float | None
    queued: bool
    queue_position: int | None
    eta_unknown: str | None

    def __new__(cls, ready: bool, eta_s: float | None, card: dict | None = None,
                body: dict | None = None) -> "Ready":
        self = super().__new__(cls, (bool(ready), eta_s))
        said = card if isinstance(card, dict) else {}
        self.card = said.get("name")
        self.usd_per_hour = said.get("usd_per_hour")
        b = body if isinstance(body, dict) else {}
        self.queued = b.get("status") == "queued"
        self.queue_position = b.get("queue_position") if self.queued else None

        self.eta_unknown = b.get("eta_unknown") if eta_s is None and not bool(ready) else None
        return self

    @property
    def ready(self) -> bool:
        return self[0]

    @property
    def eta_s(self) -> float | None:
        return self[1]

    def __repr__(self) -> str:
        if self.queued:
            eta = f", eta_s={self[1]!r}" if self[1] is not None else f" ({self.eta_unknown})" if self.eta_unknown else ""
            return f"Ready(ready=False, queued=True, queue_position={self.queue_position!r}{eta})"
        on = f", card={self.card!r}, usd_per_hour={self.usd_per_hour!r}" if self.card else ""
        why = f" ({self.eta_unknown})" if self.eta_unknown else ""
        return f"Ready(ready={self[0]!r}, eta_s={self[1]!r}{why}{on})"
