"""
Interactive capacity flow.

When stub creation reports that no serverless pool supports the requested GPU
(a guaranteed scheduling blackhole), this module lets the user launch
on-demand hardware from a cloud provider offer and routes the workload onto
it — or fails fast with an actionable error in headless environments.

A call can also find, once it is made, that there is no machine for it now.
What it does then is at the end of this module (CapacityWait): it says what
it waits for, keeps waiting, gives up after as long as its caller allows, or
has its caller reserve a machine.
"""

import math
import os
import threading
import time
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Set

from ... import terminal
from ...clients.gateway import (
    GetOrCreateStubRequest,
    GetOrCreateStubResponse,
    ListPoolOffersRequest,
    ListPrivatePoolsRequest,
    PoolConfig,
    PoolOffer,
)
from ...exceptions import NoCapacityError
from ...terminal import cli_name

if TYPE_CHECKING:
    from .runner import RunnerAbstraction

CAPACITY_STATUS_AVAILABLE = "available"
CAPACITY_STATUS_LOW = "low"
CAPACITY_STATUS_NONE = "none"

DEFAULT_ONDEMAND_TTL = "1h"
DEFAULT_ONDEMAND_NODES = 1
# "Indefinite" reservations: the control plane requires a TTL and spend cap
# on every reservation, so manual-spindown mode reserves a 30-day window the
# user releases early with 'beta9 machine release' (or extends with
# 'beta9 pool extend').
INDEFINITE_TTL = "720h"
MAX_OFFER_CHOICES = 10
PROVISION_TIMEOUT_S = 15 * 60
PROVISION_POLL_INTERVAL_S = 5


def requested_gpus(stub_request: GetOrCreateStubRequest) -> List[str]:
    return [g for g in (stub_request.gpu or "").split(",") if g and g != "NO_GPU"]


def no_capacity_hint(gpus: List[str]) -> str:
    gpu = gpus[0] if gpus else "<gpu>"
    return (
        f"run '{cli_name()} machine reserve --gpu {gpu}' to get hardware, or pick a different GPU"
    )


def no_offers_hint() -> str:
    cli = cli_name()
    return (
        f"browse available GPUs with '{cli} machine list', "
        f"or attach your own machine with '{cli} pool join'"
    )


def credits_url() -> Optional[str]:
    """
    The dashboard credits page, derived from the SDK's API host so the link
    follows the environment (app.beam.cloud -> platform.beam.cloud,
    app.stage.beam.cloud -> platform.stage.beam.cloud). Self-hosted installs
    have no credits page, so hosts without the app. prefix return None.
    """
    from ...config import get_settings

    host = (get_settings().api_host or "").split(":")[0]
    if host.startswith("app."):
        return f"https://platform.{host[len('app.') :]}/settings/credits"
    return None


def credit_error_hint(message: str) -> Optional[str]:
    """A purchase link for credit-related failures that do not already name one."""
    url = credits_url()
    text = (message or "").lower()
    if url and "credit" in text and "http" not in text:
        return f"purchase credits at {url}"
    return None


def launch_failure_hint(
    err_msg: str,
    error_code: str = "",
    required_cents: int = 0,
    available_cents: int = 0,
) -> Optional[str]:
    """Actionable hint for a failed capacity launch; currently credit-focused."""
    if "credit" not in (error_code or "") and not credit_error_hint(err_msg):
        return None

    parts = []
    if required_cents:
        parts.append(
            f"requires ${required_cents / 100:.2f} in credit, you have ${available_cents / 100:.2f}"
        )
    if url := credits_url():
        parts.append(f"purchase credits at {url}")
    return " — ".join(parts) or None


def offer_hardware_label(offer: PoolOffer, nodes: int = 1) -> str:
    """Human label for an offer's hardware, e.g. '2 nodes of 4x A6000'."""
    gpu_count = offer.gpu_count or 1
    hardware = (
        f"{gpu_count}x {offer.gpu}"
        if offer.gpu
        else (offer.display_name or offer.instance_type or "CPU node")
    )
    if nodes > 1:
        hardware = f"{nodes} nodes of {hardware}"
    return hardware


def no_offers_error(gpu_label: str, pricing: str = "on_demand") -> None:
    """Report that nothing is offered for a GPU; pricing is what was asked for (on_demand, spot, any)."""
    kind = {"spot": "spot ", "any": ""}.get(pricing, "on-demand ")
    terminal.error(
        f"No {kind}offers currently available for {gpu_label}.",
        exit=False,
        hint=no_offers_hint(),
    )


def _runner_interactive(runner: "RunnerAbstraction") -> bool:
    return terminal.is_interactive() and not getattr(runner, "headless", False)


def handle_capacity_verdict(
    runner: "RunnerAbstraction",
    stub_request: GetOrCreateStubRequest,
    stub_response: GetOrCreateStubResponse,
    stub_type: str,
) -> Optional[GetOrCreateStubResponse]:
    """
    Reacts to the capacity verdict on a stub creation response. Returns the
    response to continue with, or None when the workload should not proceed.
    """
    # Kept so that the stub can be created again on a machine that is
    # reserved for a call later (CapacityWait).
    runner.stub_request = stub_request

    if not stub_response.ok:
        return stub_response

    # An explicit pool config is the user's placement choice; don't second-guess it.
    if runner.pool_config is not None:
        return stub_response

    if stub_response.matched_private_pool:
        return _attach_to_private_pool(runner, stub_request, stub_response)

    if stub_response.capacity_status != CAPACITY_STATUS_NONE:
        return stub_response

    gpus = requested_gpus(stub_request)
    gpu_label = ", ".join(gpus) if gpus else "the requested GPU"

    if stub_type.endswith("/deployment"):
        return _handle_deployment_capacity(runner, stub_request, stub_response, gpus, gpu_label)

    if _runner_interactive(runner):
        return _run_interactive_capacity_flow(
            runner,
            stub_request,
            gpus,
            gpu_label,
            wait_for_ready=stub_type != "pod/run",
        )

    terminal.error(
        f"No compute capacity supports {gpu_label}, so this workload can never be scheduled.",
        exit=False,
        hint=no_capacity_hint(gpus),
    )
    return None


def _handle_deployment_capacity(
    runner: "RunnerAbstraction",
    stub_request: GetOrCreateStubRequest,
    stub_response: GetOrCreateStubResponse,
    gpus: List[str],
    gpu_label: str,
) -> Optional[GetOrCreateStubResponse]:
    """
    Deployments are long-lived and capacity is dynamic. Interactively the
    best path is to reserve on-demand hardware and pin the deployment to
    that pool; alternatively the user can deploy anyway (requests fail fast
    with a clear reason until capacity is attached, then start succeeding
    with no redeploy). Headless deploys warn and proceed — CI never blocks.
    """
    terminal.warn(f"No compute capacity currently supports {gpu_label}.")

    if not _runner_interactive(runner):
        terminal.detail(f"  hint: {no_capacity_hint(gpus)}")
        return stub_response

    try:
        choice = terminal.select(
            "How do you want to proceed?",
            [
                terminal.SelectOption(
                    label="Reserve on-demand hardware",
                    value="reserve",
                    description="pins this deployment to the reserved machine",
                ),
                terminal.SelectOption(
                    label="Deploy anyway",
                    value="deploy",
                    description="requests fail until capacity is attached",
                ),
                terminal.SelectOption(label="Cancel", value="cancel"),
            ],
        )
    except KeyboardInterrupt:
        choice = "cancel"

    if choice == "reserve":
        return _run_interactive_capacity_flow(runner, stub_request, gpus, gpu_label, announce=False)
    if choice == "cancel":
        # Cancelling is not a failure.
        terminal.detail("Deployment cancelled.")
        raise SystemExit(0)
    return stub_response


def _attach_to_private_pool(
    runner: "RunnerAbstraction",
    stub_request: GetOrCreateStubRequest,
    stub_response: GetOrCreateStubResponse,
) -> GetOrCreateStubResponse:
    pool_name = stub_response.matched_private_pool
    pool = PoolConfig(name=pool_name, selector=pool_name)

    terminal.print(
        f"[bold {terminal.BRAND_COLOR}]=>[/bold {terminal.BRAND_COLOR}] "
        f"No serverless capacity for this GPU — using your pool [bold]{pool_name}[/bold]"
    )

    stub_request.pool = pool
    response = runner.gateway_stub.get_or_create_stub(stub_request)
    if response.ok:
        runner.pool_config = pool
    return response


def _run_interactive_capacity_flow(
    runner: "RunnerAbstraction",
    stub_request: GetOrCreateStubRequest,
    gpus: List[str],
    gpu_label: str,
    announce: bool = True,
    wait_for_ready: bool = True,
) -> Optional[GetOrCreateStubResponse]:
    if announce:
        terminal.warn(f"No serverless capacity for {gpu_label}.")

    offers = fetch_offers(runner.gateway_stub, gpus)
    if offers is None:
        return None
    if not offers:
        no_offers_error(gpu_label)
        return None

    try:
        offer = terminal.select(
            "Launch on-demand hardware to run this workload?",
            offer_options(offers),
        )
        if offer is None:
            return None

        hourly = offer.hourly_cost_micros / 1_000_000
        ttl = select_ttl(hourly)
        if not terminal.confirm(
            f"Launch {offer_hardware_label(offer)} for ~${hourly:.2f}/hr ({ttl_label(ttl)})?",
            default=True,
        ):
            terminal.detail("Cancelled.")
            return None
    except KeyboardInterrupt:
        terminal.detail("Cancelled.")
        return None

    pool = pool_config_for_offer(offer, ttl=ttl)
    stub_request.pool = pool

    response = runner.gateway_stub.get_or_create_stub(stub_request)
    if not response.ok:
        return response
    runner.pool_config = pool

    if wait_for_ready and not wait_for_pool_ready(runner.gateway_stub, pool.name):
        return None
    return response


# How the machines of an offer are sold, as PoolConfig.pricing names it. On
# demand is the default and is sent as nothing.
PRICING_ON_DEMAND = ""
PRICING_SPOT = "spot"
PRICING_ANY = "any"


def fetch_offers(
    gateway_stub,
    gpus: List[str],
    limit: int = MAX_OFFER_CHOICES,
    pricing: str = PRICING_ON_DEMAND,
) -> Optional[List[PoolOffer]]:
    """
    Fetch offers sorted by price; None indicates a fetch error. Offers are
    on-demand unless pricing asks for spot machines, or for both ("any").
    """
    with terminal.progress("Finding available hardware..."):
        res = gateway_stub.list_pool_offers(
            ListPoolOffersRequest(pool=PoolConfig(gpu=gpus, pricing=pricing))
        )
    if not res.ok:
        terminal.error(f"Failed to list hardware offers: {res.err_msg}", exit=False)
        return None

    offers = list(res.offers)
    offers.sort(key=lambda o: o.hourly_cost_micros)
    if limit > 0:
        offers = offers[:limit]
    return offers


def _offer_columns(offer: PoolOffer) -> tuple:
    hourly = offer.hourly_cost_micros / 1_000_000
    region = offer.region_display_name or offer.region or "any region"
    hardware = offer_hardware_label(offer)
    details = []
    if offer.spot:
        details.append("spot, can be taken back")
    if offer.cpu_millicores:
        details.append(f"{offer.cpu_millicores // 1000} vCPU")
    if offer.memory_mb:
        details.append(f"{offer.memory_mb // 1024}GB RAM")
    if offer.reliability:
        details.append(f"{offer.reliability * 100:.0f}% reliability")
    return hardware, region, f"${hourly:.2f}/hr", ", ".join(details)


def offer_options(offers: List[PoolOffer]) -> List[terminal.SelectOption]:
    """
    Build select options with the hardware/region/price columns padded to
    equal widths across all offers, so the picker reads like a table.
    """
    rows = [_offer_columns(o) for o in offers]
    widths = [max(len(row[i]) for row in rows) for i in range(3)] if rows else [0, 0, 0]
    return [
        terminal.SelectOption(
            label=f"{hardware:<{widths[0]}}  {region:<{widths[1]}}  {price:>{widths[2]}}",
            value=offer,
            description=details,
        )
        for offer, (hardware, region, price, details) in zip(offers, rows)
    ]


def pool_config_for_offer(
    offer: PoolOffer,
    name: str = "",
    nodes: int = DEFAULT_ONDEMAND_NODES,
    ttl: str = DEFAULT_ONDEMAND_TTL,
    max_spend: float = 0.0,
) -> PoolConfig:
    hourly = offer.hourly_cost_micros / 1_000_000
    if max_spend <= 0:
        # Cover the TTL with headroom so billing reconciliation never kills
        # the node mid-session; the TTL is what actually bounds the spend.
        # Long/indefinite reservations get a slimmer buffer so the cap stays
        # a sane guardrail rather than a blank check.
        hours = max(1.0, ttl_hours(ttl))
        buffer = 2.0 if hours <= 24 else 1.25
        max_spend = max(1.0, round(hourly * nodes * hours * buffer, 2))
    pool_name = _sanitize_pool_name(name or f"ondemand-{offer.gpu or 'cpu'}")
    return PoolConfig(
        name=pool_name,
        selector=pool_name,
        gpu=[offer.gpu] if offer.gpu else [],
        nodes=nodes,
        ttl=ttl,
        max_spend=max_spend,
        providers=[offer.provider] if offer.provider else [],
        offer_id=offer.id,
        # A machine that is sold both ways is two offers with one ID.
        pricing=PRICING_SPOT if offer.spot else PRICING_ON_DEMAND,
    )


def ttl_hours(ttl: str) -> float:
    value = (ttl or "").strip().lower()
    try:
        if value.endswith("h"):
            return float(value[:-1])
        if value.endswith("m"):
            return float(value[:-1]) / 60
        if value.endswith("d"):
            return float(value[:-1]) * 24
        return float(value)
    except ValueError:
        return 1.0


def ttl_label(ttl: str) -> str:
    if ttl == INDEFINITE_TTL:
        return "runs until you release it (30d cap)"
    return f"expires in {ttl}"


def valid_ttl(ttl: str) -> bool:
    value = (ttl or "").strip().lower()
    if len(value) < 2 or value[-1] not in "mhd":
        return False
    try:
        return float(value[:-1]) > 0
    except ValueError:
        return False


TTL_CHOICES = ["1h", "2h", "4h", "8h", "24h"]


def select_ttl(hourly: float, nodes: int = 1, default: str = DEFAULT_ONDEMAND_TTL) -> str:
    """
    Interactive duration picker with the projected cost per choice. Falls
    back to the default duration when the terminal isn't interactive.
    """
    if not terminal.is_interactive():
        return default

    options = [
        terminal.SelectOption(
            label="until I stop it",
            value=INDEFINITE_TTL,
            description=f"~${hourly * nodes:.2f}/hr until '{cli_name()} machine release' (30d cap)",
        )
    ]
    for ttl in TTL_CHOICES:
        cost = hourly * nodes * ttl_hours(ttl)
        options.append(terminal.SelectOption(label=f"{ttl:<12}  ~${cost:.2f}", value=ttl))
    options.append(terminal.SelectOption(label="other", value="", description="custom duration"))

    choice = terminal.select("How long do you need it?", options)
    if choice:
        return choice

    while True:
        raw = str(terminal.prompt(text="Duration (e.g. 45m, 6h, 2d)", default=default))
        if valid_ttl(raw):
            return raw
        terminal.warn("Use a number with a unit: 45m, 6h, or 2d.")


def _sanitize_pool_name(value: str) -> str:
    out = "".join(c if (c.isalnum() or c in "-._") else "-" for c in value.lower())
    return out.strip("-._") or "ondemand"


def wait_for_pool_ready(
    gateway_stub,
    pool_name: str,
    timeout_s: int = PROVISION_TIMEOUT_S,
) -> bool:
    """
    Block with live progress until the pool has at least one ready machine.
    Milestones (reservation → booting → ready) print with elapsed times as
    they are observed.
    """
    start = time.monotonic()
    milestones_seen = set()

    def milestone(name: str, label: str):
        if name in milestones_seen:
            return
        milestones_seen.add(name)
        terminal.print(
            f"[bold green]✓[/bold green] {label} [dim]({time.monotonic() - start:.0f}s)[/dim]"
        )

    try:
        with terminal.progress("Provisioning node...") as status:
            while time.monotonic() - start < timeout_s:
                pool = _find_pool(gateway_stub, pool_name)
                if pool is not None:
                    if pool.reservations or pool.reserved_nodes > 0:
                        milestone("reserved", "Node reserved")
                        status.update("Waiting for instance to boot...")
                    if pool.machine_count > 0:
                        milestone("joined", "Machine online, agent joined")
                        status.update("Waiting for machine to become ready...")
                    if pool.ready_machine_count > 0:
                        milestone("ready", "Machine ready")
                        return True
                time.sleep(PROVISION_POLL_INTERVAL_S)
    except KeyboardInterrupt:
        terminal.warn(f"Interrupted; pool '{pool_name}' keeps provisioning in the background.")
        terminal.detail(f"  hint: check progress with '{cli_name()} pool machines {pool_name}'")
        return False

    terminal.error(
        f"Timed out waiting for pool '{pool_name}' to become ready; it may still be provisioning.",
        exit=False,
        hint=f"check progress with '{cli_name()} pool machines {pool_name}' and re-run once a machine is ready",
    )
    return False


def _find_pool(gateway_stub, pool_name: str):
    res = gateway_stub.list_private_pools(ListPrivatePoolsRequest())
    if not res.ok:
        return None
    for pool in res.pools:
        if pool.name == pool_name or pool.selector == pool_name:
            return pool
    return None


# A call that waits for a machine
#
# A call is pending from when it is made until its container runs: a second
# when a machine has room, minutes when one has to start, and longer when
# there is no capacity to be had. The gateway says which on the call's
# stream, in words, each time it changes and every few seconds while it does
# not. CapacityWait shows that, gives the call up after as long as its caller
# allows, and says once what can be done about capacity that is not there. At
# a terminal that is a question, and the answer may be to reserve a machine
# and run the call on it.

# How long a call goes without capacity before its caller is asked what to
# do about it, or, where nobody can be asked, told what can be done.
ASK_AFTER_S = 60.0

# The phases the gateway reports (FunctionInvokeResponse.pending_phase).
QUEUED = "queued"
PROVISIONING = "provisioning"
WAITING_FOR_CAPACITY = "waiting_for_capacity"
STARTING = "starting"

WAIT, RESERVE, CANCEL = "wait", "reserve", "cancel"

_UNITS = {"s": 1, "m": 60, "h": 3600}
_batch_lock = threading.Lock()


class Reserved(Exception):
    """A call that waited was given up for one on a machine its caller reserved."""


def wait_limit_name() -> str:
    """The environment variable that limits how long a call waits for a machine."""
    from ...config import get_settings

    return f"{get_settings().name.upper()}_CAPACITY_WAIT"


def wait_limit() -> float:
    """
    The longest a call may go without a machine, in seconds, as the
    environment sets it: a number of seconds, or a number with a unit (90s,
    5m, 1h). Nothing, or 0, is no limit.
    """
    name = wait_limit_name()
    raw = os.getenv(name, "").strip().lower()
    if not raw:
        return 0.0
    number, unit = (raw[:-1], _UNITS[raw[-1]]) if raw[-1] in _UNITS else (raw, 1)
    try:
        seconds = float(number) * unit
    except ValueError:
        seconds = math.nan
    if not math.isfinite(seconds) or seconds < 0:
        terminal.error(
            f"{name}={raw} is not a length of time.",
            hint="Use a number of seconds, or a number with a unit: 90, 90s, 5m.",
            code="INVALID_CONFIG",
        )
    return seconds


def clock(seconds: float) -> str:
    """A length of time as a spinner counts it: 1:15."""
    minutes, seconds = divmod(max(int(seconds), 0), 60)
    return f"{minutes}:{seconds:02d}"


def _took(seconds: float) -> str:
    if seconds < 120:
        return f"{int(seconds)} seconds"
    return f"{round(seconds / 60)} minutes"


def capacity_label(gpus: List[str]) -> str:
    """The capacity that was asked for: "A10G capacity", "A10G or T4 capacity", "capacity"."""
    if not gpus:
        return "capacity"
    if len(gpus) == 1:
        return f"{gpus[0]} capacity"
    return f"{', '.join(gpus[:-1])} or {gpus[-1]} capacity"


def _advice(gpus: List[str], reason: str) -> str:
    """What a caller can do other than wait, or "" when there is nothing."""
    if reason == "no_spare_capacity":
        return (
            "The Spot tier runs on capacity the other tiers leave spare. "
            'cpu_tier="shared" or "performance" does not wait for it.'
        )
    if reason == "machine_busy" or not gpus:
        return ""
    if len(gpus) > 1:
        more = "Add GPU types to the list"
    else:
        other = "A10G" if gpus[0] == "T4" else "T4"
        more = f'List more than one GPU type (gpu=["{gpus[0]}", "{other}"])'
    return (
        f"{more} so that whichever has capacity is used, or reserve a machine: "
        f"`{cli_name()} machine reserve --gpu {gpus[0]}`."
    )


def _once(said: Set[str], what: str) -> bool:
    """True the first time `what` is said to a batch."""
    with _batch_lock:
        if what in said:
            return False
        said.add(what)
        return True


class CapacityWait:
    """
    What one call shows and does until its container runs, by what the
    gateway says it waits for (told).

    title is the text of the spinner the call runs under. In a terminal the
    spinner says what the call waits for and counts the time; anywhere else
    each change is a line of output. The calls of a batch have no title and
    share one set (batch): each kind of wait is then one line for all of
    them, and nobody is asked anything.

    limit is the longest the call may go without a machine, in seconds, and
    0 is no limit.
    """

    def __init__(
        self,
        runner: "RunnerAbstraction",
        title: Optional[str] = None,
        limit: float = 0.0,
        batch: Optional[Set[str]] = None,
    ) -> None:
        self.runner = runner
        self.limit = limit
        self._title = title
        self._batch = batch
        self._advised = False
        # What was shown last, as (phase, reason).
        self._shown: Optional[tuple] = None
        # When the call began to wait for a machine, on the monotonic clock.
        self._began: Optional[float] = None
        # The time it has had no capacity to wait for: the stretches that
        # are over, and when the one under way began.
        self._without = 0.0
        self._without_since: Optional[float] = None

    def told(self, response: Any, stop: Callable[[], None], started: Callable[[], bool]) -> None:
        """
        Take a response that says what the call waits for. stop gives the
        call up, and started says whether it runs after all.

        Raises NoCapacityError for a call that has gone without a machine
        for as long as it may, and Reserved for one that is to be made again
        on a machine its caller reserved.
        """
        phase, reason = response.pending_phase, response.pending_reason
        now = time.monotonic()
        if phase == STARTING:
            # Only a call that was said to wait is said to have stopped.
            if self._shown is not None and self._shown[0] != STARTING:
                self._shown = (phase, reason)
                self._show(f"{response.pending_message} (waited {clock(now - self._began)})")
            self._placed()
            return

        # The gateway says how long the container has been in its phase, and
        # the wait counts from there: a client that joins late, or whose
        # clock stood still for a while, has waited as long as the gateway
        # says.
        since = now - response.pending_waited_seconds
        self._began = since if self._began is None else min(self._began, since)
        if phase != WAITING_FOR_CAPACITY:
            self._without, self._without_since = self._without_capacity(now), None
        elif self._without_since is None:
            self._without_since = since
        else:
            self._without_since = min(self._without_since, since)

        # A call that is queued is about to be placed: not a wait worth a
        # word. Nor is a phase with no words, from a gateway that has none.
        if phase != QUEUED and response.pending_message and (phase, reason) != self._shown:
            self._shown = (phase, reason)
            self._show(response.pending_message, since)

        if self.limit > 0 and now - self._began >= self.limit:
            error = self._gave_up(phase, reason, now - self._began)
            # A call that is given up on must not run later.
            stop()
            raise error

        without = self._without_capacity(now)
        if phase == WAITING_FOR_CAPACITY and not self._advised and without >= ASK_AFTER_S:
            self._advised = True
            self._advise(reason, without, stop, started)

    def running(self) -> None:
        """
        The call's container runs, or the call is over: the spinner gets its
        own text back. A call that waits again, for another attempt, starts
        over.
        """
        if self._shown is not None and self._on_spinner():
            terminal.update_progress(self._title)
        self._shown = None
        self._placed()

    def _placed(self) -> None:
        self._began = self._without_since = None
        self._without = 0.0

    def _without_capacity(self, now: float) -> float:
        if self._without_since is None:
            return self._without
        return self._without + now - self._without_since

    def _on_spinner(self) -> bool:
        return self._title is not None and terminal.spinner_visible()

    def _show(self, message: str, since: Optional[float] = None) -> None:
        """Show what the call waits for, and since when if it still waits."""
        words = message[0].lower() + message[1:]
        if self._batch is not None:
            if since is not None and _once(self._batch, self._shown[0]):
                terminal.note(f"Some calls are waiting: {words}")
        elif not self._on_spinner():
            terminal.note(message)
        elif since is None:
            terminal.update_progress(f"{self._title} · {words}")
        else:
            terminal.update_progress(
                lambda: f"{self._title} · {words} ({clock(time.monotonic() - since)})"
            )

    def _gpus(self) -> List[str]:
        """The GPU types the call asked for, in its order of preference."""
        stub_request = getattr(self.runner, "stub_request", None)
        return requested_gpus(stub_request) if stub_request is not None else []

    def _gave_up(self, phase: str, reason: str, seconds: float) -> NoCapacityError:
        """The call has gone without a machine for as long as it may: why, and what else there is."""
        gpus = self._gpus()
        if phase == WAITING_FOR_CAPACITY:
            what = f"No {capacity_label(gpus)} became available in {_took(seconds)}."
        elif phase == PROVISIONING:
            what = f"A machine for this call was still starting after {_took(seconds)}."
        else:
            what = f"This call was not placed on a machine in {_took(seconds)}."
        hint = (
            _advice(gpus, reason),
            f"`{cli_name()} machine list` shows what can be reserved."
            if reason not in ("no_spare_capacity", "machine_busy")
            else "",
            f"{wait_limit_name()} limits the wait to {_took(self.limit)}.",
        )
        return NoCapacityError(
            f"{what} The call was cancelled.", hint=" ".join(part for part in hint if part)
        )

    def _advise(
        self, reason: str, waited: float, stop: Callable[[], None], started: Callable[[], bool]
    ) -> None:
        """Say what can be done about capacity that is not there: a question, where somebody can answer."""
        gpus = self._gpus()
        if self._batch is None:
            # Whether there is somebody to ask is known only with the
            # spinner off the screen: while it is on, it stands in for the
            # terminal's output.
            with terminal.progress_paused():
                if _runner_interactive(self.runner):
                    self._ask(gpus, reason, waited, stop, started)
                    return
        elif not _once(self._batch, "advice"):
            return

        if self.limit > 0:
            keeps = f"The call waits until {clock(self.limit)} ({wait_limit_name()})."
        else:
            keeps = f"The call keeps waiting; {wait_limit_name()}=<seconds> gives up sooner."
        terminal.note(f"Still no {capacity_label(gpus)} after {clock(waited)}. {keeps}")
        if advice := _advice(gpus, reason):
            terminal.note(advice)

    def _ask(
        self,
        gpus: List[str],
        reason: str,
        waited: float,
        stop: Callable[[], None],
        started: Callable[[], bool],
    ) -> None:
        """Ask the caller what to do about a call there is no capacity for, and do it."""
        runner = self.runner
        terminal.warn(
            f"No {capacity_label(gpus)} has been available for {clock(waited)}. "
            "This is a platform limit, not your code."
        )
        options = [
            terminal.SelectOption(
                label="Keep waiting", value=WAIT, description="runs as soon as there is capacity"
            )
        ]
        # Reserving a machine gets the call one if it asked for a GPU and
        # left it to the platform where to run.
        if gpus and reason == "no_capacity" and getattr(runner, "pool_config", None) is None:
            options.append(
                terminal.SelectOption(
                    label="Reserve a machine",
                    value=RESERVE,
                    description="on demand, billed by the hour; runs this call on it",
                )
            )
        elif advice := _advice(gpus, reason):
            terminal.detail(f"  {advice}")
        options.append(
            terminal.SelectOption(
                label="Cancel", value=CANCEL, description="the function does not run"
            )
        )
        try:
            choice = terminal.select("How do you want to proceed?", options)
        except KeyboardInterrupt:
            choice = CANCEL

        if choice == CANCEL:
            stop()
            terminal.detail("Cancelled. The function did not run.")
            raise SystemExit(1)
        if choice != RESERVE:
            return
        # The question may have stood for a while.
        if started():
            terminal.detail("A machine took the call while you were choosing.")
            return

        response = _run_interactive_capacity_flow(
            runner,
            runner.stub_request,
            gpus,
            ", ".join(gpus),
            announce=False,
            wait_for_ready=False,
        )
        if response is not None and not response.ok:
            # Why is reported. The call that waits is still the way to run.
            runner._apply_stub_response(response)
            runner.stub_request.pool = None
        if response is None or not response.ok:
            terminal.detail("No machine was reserved. Still waiting for capacity.")
            return

        # A machine is reserved. The call that waits is given up first, so
        # that it cannot run twice, and is made again once the machine is
        # ready. If it is not, why was said.
        stop()
        if not runner._apply_stub_response(response) or not wait_for_pool_ready(
            runner.gateway_stub, runner.pool_config.name
        ):
            raise SystemExit(1)
        raise Reserved()
