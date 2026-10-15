"""Training workload for profile-guided optimisation of the Rust extension.

``maturin build --pgo`` builds an instrumented wheel, installs it in a
temporary virtualenv, runs ``[tool.maturin] pgo-command`` (this script) and
rebuilds using the recorded profile.

The script needs only the standard library and an installed Kolo, so it runs
in every wheel job that can execute the wheel it just built, on every
supported Python. It is deliberately not derived from ``python/bench``: a
profile trained on the benchmarks would make them flatter the build. It is a
small order-processing program that goes through the paths real traces spend
their time in: plain calls, methods, keyword arguments, generators,
coroutines, threads, exceptions, a mix of value types, objects with their own
``__repr__`` (finished and still under construction), calls into excluded
library code, the plugins the standard library can trigger (``logging``,
``unittest``, ``urllib`` against a local server), assignments
(``line_events``), and the whole way to disk and back: small traces and a
large one, saved inline and by the writer thread, with and without subtree
flushing, then loaded again.

Code this never runs is optimised for size, so a path that matters and is
missing here gets slower, not just no faster. Not reachable with the standard
library alone: the Django SQL plugins and the ``requests``/``urllib3`` ones
(the plugin dispatch they go through is trained by the other plugins).
"""

import asyncio
import dataclasses
import datetime
import decimal
import http.server
import importlib.util
import json
import logging
import os
import re
import shutil
import sys
import tempfile
import textwrap
import threading
import time
import unittest
import urllib.request
from pathlib import Path

TRACE_ROOT = tempfile.mkdtemp(prefix="kolo-pgo-")
os.environ["KOLO_PATH"] = TRACE_ROOT

import kolo._kolo  # noqa: E402,F401  Fail here, not silently, if the extension is missing.
from kolo import enable  # noqa: E402
from kolo.db import list_traces_from_db, load_trace_from_db, setup_db  # noqa: E402
from kolo.trace_container import load_trace  # noqa: E402
from kolo.utils import extract_main_frames_from_data  # noqa: E402

HERE = str(Path(__file__).resolve())

IGNORED = str(Path(TRACE_ROOT) / "kolo_pgo_ignored.py")
Path(IGNORED).write_text(
    "def audit(order_id, lines):\n"
    "    return sum(checksum(order_id, index) for index in range(len(lines)))\n"
    "\n\n"
    "def checksum(order_id, index):\n"
    "    return (order_id * 31 + index) % 97\n"
)
_spec = importlib.util.spec_from_file_location("kolo_pgo_ignored", IGNORED)
assert _spec is not None and _spec.loader is not None
ignored = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ignored)
ORDERS = 25
REPEATS = 3
SMALL_TRACES = 30
LARGE_ROWS = 4000
logger = logging.getLogger("kolo_pgo_train")
logger.addHandler(logging.NullHandler())
logger.propagate = False
logger.setLevel(logging.INFO)


@dataclasses.dataclass
class Item:
    sku: str
    qty: int
    price: decimal.Decimal
    tags: tuple = ()


class OutOfStock(Exception):
    pass


class Inventory:
    def __init__(self, stock):
        self.stock = dict(stock)

    def reserve(self, item):
        left = self.stock.get(item.sku, 0) - item.qty
        if left < 0:
            raise OutOfStock(item.sku)
        self.stock[item.sku] = left
        return left

    def describe(self, item, *, width=40):
        text = f"{item.sku} x{item.qty} @ {item.price} {' '.join(item.tags)}"
        return textwrap.shorten(text, width)


class Money:
    """A value with its own `__repr__`, built in `__new__`."""

    amount: decimal.Decimal
    currency: str

    def __new__(cls, amount, currency="eur"):
        self = object.__new__(cls)
        self.amount = amount
        self.currency = normalise_currency(self, currency)
        return self

    def __repr__(self):
        return f"Money({self.amount}, {self.currency!r})"


def normalise_currency(money, currency):
    return currency.upper()


class Ledger:
    """Hands itself to its own methods before `__init__` is done."""

    def __init__(self, owner):
        self.owner = owner
        self.entries = []
        self.opened = self.open()

    def open(self):
        return len(self.entries)

    def post(self, money):
        self.entries.append(money)
        return self

    def __repr__(self):
        return f"Ledger({self.owner!r}, {len(self.entries)} entries)"


@dataclasses.dataclass
class Shipment:
    order_id: int
    lines: list
    weight: decimal.Decimal = dataclasses.field(init=False)

    def __post_init__(self):
        self.weight = shipment_weight(self)

    def __repr__(self):
        return f"Shipment({self.order_id}, {len(self.lines)} lines)"


def shipment_weight(shipment):
    return sum(item.qty for item, _ in shipment.lines) * decimal.Decimal("0.4")


def ship(order_id, lines):
    """Objects under construction, which Kolo must not `repr()`, and the
    same objects once built, which it does."""
    ledger = Ledger(f"order-{order_id}")
    for _item, amount in lines[:5]:
        ledger.post(Money(amount))
    shipment = Shipment(order_id, lines)
    return ledger, shipment.weight


def line_total(item, tax=decimal.Decimal("0.2")):
    net = item.price * item.qty
    gross = net * (1 + tax)
    return gross


def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def items(count):
    for index in range(count):
        yield Item(
            sku=f"sku-{index % 17:03d}",
            qty=1 + index % 5,
            price=decimal.Decimal(index % 90) / 7,
            tags=("new",) if index % 3 else ("sale", "bulk"),
        )


def priced(source):
    for item in source:
        yield item, line_total(item)


def try_reserve(inventory, item):
    try:
        return inventory.reserve(item)
    except OutOfStock as exc:
        logger.info("out of stock: %s", exc, extra={"sku": item.sku})
        return str(exc)


def summarise(order_id, lines, when, meta=None, *extra, **options):
    total = sum(amount for _, amount in lines)
    payload = {
        "id": order_id,
        "when": when.isoformat(),
        "total": str(total),
        "lines": [
            dict(dataclasses.asdict(item), price=str(item.price)) for item, _ in lines
        ],
        "meta": meta,
    }
    encoded = json.dumps(payload, sort_keys=True)
    slug = re.sub(r"[^a-z0-9]+", "-", encoded[:60].lower())
    return len(json.loads(encoded)["lines"]), slug


def process_order(order_id, inventory):
    lines = []
    for item, amount in priced(items(30)):
        left = try_reserve(inventory, item)
        label = inventory.describe(item, width=30 + order_id % 10)
        lines.append((item, amount))
        seen = (
            left,
            label,
            amount > 5,
            None,
            1.5 * order_id,
            b"raw",
            {order_id: [left]},
        )
    when = datetime.datetime(2026, 1, 1) + datetime.timedelta(minutes=order_id)
    audit = ignored.audit(order_id, lines)
    ship(order_id, lines)
    meta = {"source": "pgo", "n": order_id, "seen": len(seen), "audit": audit}
    return summarise(order_id, lines, when, meta, 1, 2, flag=True)


async def quote(order_id):
    await asyncio.sleep(0)
    return order_id, line_total(Item("sku-async", order_id % 4 + 1, decimal.Decimal(3)))


async def quotes(count):
    return await asyncio.gather(*(quote(order_id) for order_id in range(count)))


def worker(results, errors, inventory, start):
    try:
        orders = range(start, start + 3)
        results.append([process_order(order_id, inventory) for order_id in orders])
    except Exception as exc:
        errors.append(exc)


class OrderTests(unittest.TestCase):
    def test_total(self):
        item = Item("sku-test", 2, decimal.Decimal(5))
        self.assertEqual(line_total(item), decimal.Decimal(12))

    def test_out_of_stock(self):
        with self.assertRaises(OutOfStock):
            Inventory({}).reserve(Item("sku-test", 1, decimal.Decimal(1)))


def run_tests():
    result = unittest.TestResult()
    unittest.defaultTestLoader.loadTestsFromTestCase(OrderTests).run(result)
    if not result.wasSuccessful() or result.testsRun != 2:
        raise SystemExit(f"training tests failed: {result.failures + result.errors}")
    return result.testsRun


class QuietHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"path": self.path, "stock": 40}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def fetch_stock(port, count):
    """HTTP requests through urllib, for Kolo's urllib plugin."""
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    levels = []
    for index in range(count):
        request = urllib.request.Request(
            f"http://127.0.0.1:{port}/stock/{index}", headers={"X-Order": str(index)}
        )
        with opener.open(request, timeout=30) as response:
            levels.append(json.loads(response.read())["stock"])
    return levels


def render_row(catalogue, index, depth=0):
    """One frame of the large trace: the same big values in every frame."""
    if depth < 3:
        return render_row(catalogue, index, depth + 1)
    row = catalogue["rows"][index % len(catalogue["rows"])]
    return f"{row['sku']}:{len(catalogue['banner'])}:{index}"


def large_report(rows):
    catalogue = {
        "banner": "kolo " * 60,
        "rows": [{"sku": f"sku-{n:04d}", "notes": ["x" * 20] * 3} for n in range(8)],
    }
    return [render_row(catalogue, index) for index in range(rows)]


def workload():
    inventory = Inventory({f"sku-{index:03d}": 40 for index in range(17)})
    done = [process_order(order_id, inventory) for order_id in range(ORDERS)]
    quoted = asyncio.run(quotes(ORDERS))
    results: list = []
    errors: list = []
    threads = [
        threading.Thread(target=worker, args=(results, errors, inventory, start))
        for start in (100, 200)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    if errors or len(results) != len(threads):
        raise SystemExit(f"training worker threads failed: {errors!r}")
    return done, quoted, results, run_tests(), fib(15)


def configs():
    base = {"auto_emit": False}
    only_this_file = dict(base, filters={"include_frames": [HERE]})
    yield base
    yield only_this_file
    yield dict(only_this_file, threading=True)
    yield dict(base, filters={"ignore_frames": [IGNORED]})
    if sys.version_info >= (3, 12):
        yield dict(base, line_events=True)
        yield dict(only_this_file, line_events=True)
        yield dict(base, use_monitoring=False)
        yield dict(only_this_file, use_monitoring=False)
        yield dict(only_this_file, use_monitoring=False, threading=True)
        yield dict(base, use_monitoring=False, filters={"ignore_frames": [IGNORED]})


def large_configs():
    base = {"auto_emit": False, "filters": {"include_frames": [HERE]}}
    yield base
    yield dict(base, flush_subtree_mb=0.25)
    yield dict(base, flush_subtree_mb=False)
    if sys.version_info >= (3, 12):
        yield dict(base, use_monitoring=False)


class Recorded:
    """Counts, per function name, the saved traces that recorded a call to it."""

    def __init__(self, db_path):
        self.db_path = db_path
        self.names_by_trace = {}

    def count(self, name):
        for trace_id, _created_at, _size in list_traces_from_db(self.db_path):
            if trace_id not in self.names_by_trace:
                data, _ = load_trace_from_db(self.db_path, trace_id)
                frames = extract_main_frames_from_data(load_trace(data))
                self.names_by_trace[trace_id] = {f.get("co_name") for f in frames}
        return sum(name in names for names in self.names_by_trace.values())

    def wait_for(self, name, expected, timeout=120):
        """Fail the build if the sessions did not record the workload: a
        profile of nothing would optimise the whole extension as cold code.
        Sessions saved by the writer thread land a moment after they end."""
        deadline = time.monotonic() + timeout
        while True:
            found = self.count(name)
            if found >= expected:
                return
            if time.monotonic() > deadline:
                raise SystemExit(f"{found} traces recorded {name}, expected {expected}")
            time.sleep(0.2)


def main():
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    port = server.server_address[1]
    try:
        recorded = Recorded(setup_db())
        sessions = 0
        for _ in range(REPEATS):
            for config in configs():
                with enable(config, _save_in_thread=False):
                    workload()
                sessions += 1
        recorded.wait_for("process_order", sessions)

        requests = 0
        for _ in range(SMALL_TRACES):
            with enable({"auto_emit": False}):
                fetch_stock(port, 3)
            requests += 1
        recorded.wait_for("fetch_stock", requests)

        reports = 0
        for config in large_configs():
            for save_in_thread in (False, True):
                with enable(config, _save_in_thread=save_in_thread):
                    large_report(LARGE_ROWS)
                reports += 1
        recorded.wait_for("large_report", reports)
    finally:
        server.shutdown()
        shutil.rmtree(TRACE_ROOT, ignore_errors=True)


if __name__ == "__main__":
    main()
