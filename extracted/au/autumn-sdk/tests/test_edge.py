import json
import re
import socket
import unittest
from typing import Any, Callable, Dict, List, Optional

import httpx
from autumn_sdk import Autumn
from autumn_sdk.utils import BackoffStrategy, RetryConfig

EDGE = "https://edge.test"
AUTUMN = "https://autumn.test"
CHECK: Dict[str, Any] = {"customer_id": "customer_123", "feature_id": "messages"}
UUID = re.compile(r"^[0-9a-f-]{36}$")

Reply = Callable[[httpx.Request], httpx.Response]


def check_answer(customer_id: str) -> httpx.Response:
    return httpx.Response(
        200, json={"allowed": True, "customer_id": customer_id, "balance": None, "flag": None}
    )


def edge_down(_request: httpx.Request) -> httpx.Response:
    return httpx.Response(503, json={"message": "Atom thread 1 is unavailable", "code": "atom_unavailable"})


EDGE_DOWN_REPLIES: Dict[str, Reply] = {
    "503 atom_unavailable": edge_down,
    "500 internal_error": lambda _: httpx.Response(500, json={"code": "internal_error"}),
    "502 from a proxy": lambda _: httpx.Response(502, text="Bad Gateway"),
    "504 from a proxy": lambda _: httpx.Response(504, text="Gateway Timeout"),
}


def raises(error: type) -> Reply:
    def reply(request: httpx.Request) -> httpx.Response:
        raise error("stand-in", request=request)

    return reply


class Hosts:
    """A transport answering the edge and Autumn with stand-ins, keeping what each was sent."""

    def __init__(self, edge: Reply, autumn: Reply, real_edge: bool = False):
        self.sent: Dict[str, List[httpx.Request]] = {"edge": [], "autumn": []}
        self._replies = {"edge": edge, "autumn": autumn}
        self._real = httpx.HTTPTransport() if real_edge else None

    def host_of(self, request: httpx.Request) -> str:
        return "autumn" if request.url.host == "autumn.test" else "edge"

    def handle(self, request: httpx.Request) -> httpx.Response:
        host = self.host_of(request)
        request.read()
        self.sent[host].append(request)
        if host == "edge" and self._real is not None:
            return self._real.handle_request(request)
        return self._replies[host](request)

    def keys(self, host: str) -> List[Optional[str]]:
        return [request.headers.get("idempotency-key") for request in self.sent[host]]

    def body_keys(self, host: str) -> List[Optional[str]]:
        """The body's `idempotency_key` of each request sent: where a track's key lives."""
        return [json.loads(request.content).get("idempotency_key") for request in self.sent[host]]


class SyncTransport(httpx.BaseTransport):
    def __init__(self, hosts: Hosts):
        self.hosts = hosts

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        return self.hosts.handle(request)


class AsyncTransport(httpx.AsyncBaseTransport):
    def __init__(self, hosts: Hosts):
        self.hosts = hosts

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        return self.hosts.handle(request)


def client_for(
    hosts: Hosts, edge_url: str = EDGE, use_edge: bool = True, **options
) -> Autumn:
    return Autumn(
        secret_key="am_sk_test",
        server_url=AUTUMN,
        edge_url=edge_url,
        use_edge=use_edge,
        client=httpx.Client(transport=SyncTransport(hosts)),
        async_client=httpx.AsyncClient(transport=AsyncTransport(hosts)),
        **options,
    )


def closed_url() -> str:
    """A port nothing listens on: connecting is refused."""
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return f"http://127.0.0.1:{sock.getsockname()[1]}"


WRITES = {
    "send_event": {**CHECK, "send_event": True},
    "lock": {**CHECK, "lock": {"enabled": True, "lock_id": "lock_1"}},
}


class WriteCheckTests(unittest.TestCase):
    def test_goes_to_the_edge_with_a_generated_key(self):
        for name, write in WRITES.items():
            with self.subTest(name):
                hosts = Hosts(edge=lambda _: check_answer("from_edge"), autumn=lambda _: check_answer("from_autumn"))
                response = client_for(hosts).check(**write)
                self.assertEqual(response.customer_id, "from_edge")
                self.assertEqual(hosts.sent["autumn"], [])
                [key] = hosts.keys("edge")
                self.assertRegex(key or "", UUID)

    def test_each_call_gets_its_own_key(self):
        for name, write in WRITES.items():
            with self.subTest(name):
                hosts = Hosts(edge=lambda _: check_answer("from_edge"), autumn=lambda _: check_answer("from_autumn"))
                client = client_for(hosts)
                client.check(**write)
                client.check(**write)
                first, second = hosts.keys("edge")
                self.assertIsNotNone(first)
                self.assertNotEqual(first, second)

    def test_sends_the_callers_key_unchanged(self):
        for name, write in WRITES.items():
            with self.subTest(name):
                hosts = Hosts(edge=lambda _: check_answer("from_edge"), autumn=lambda _: check_answer("from_autumn"))
                client_for(hosts).check(**write, http_headers={"Idempotency-Key": "caller_key_1"})
                self.assertEqual(hosts.keys("edge"), ["caller_key_1"])

    def test_falls_back_on_edge_down_with_the_same_key(self):
        for fail_open in (True, False):
            for down_name, down in EDGE_DOWN_REPLIES.items():
                for name, write in WRITES.items():
                    with self.subTest(name, down=down_name, fail_open=fail_open):
                        hosts = Hosts(edge=down, autumn=lambda _: check_answer("from_autumn"))
                        response = client_for(hosts, fail_open=fail_open).check(**write)
                        self.assertEqual(response.customer_id, "from_autumn")
                        [key] = hosts.keys("edge")
                        self.assertIsNotNone(key)
                        self.assertEqual(hosts.keys("autumn"), [key])

    def test_falls_back_after_an_edge_timeout_with_the_same_key(self):
        for fail_open in (True, False):
            for name, write in WRITES.items():
                with self.subTest(name, fail_open=fail_open):
                    hosts = Hosts(edge=raises(httpx.ReadTimeout), autumn=lambda _: check_answer("from_autumn"))
                    response = client_for(hosts, fail_open=fail_open).check(**write)
                    self.assertEqual(response.customer_id, "from_autumn")
                    [key] = hosts.keys("edge")
                    self.assertIsNotNone(key)
                    self.assertEqual(hosts.keys("autumn"), [key])

    def test_falls_back_with_the_callers_key_when_the_edge_refuses_the_connection(self):
        for fail_open in (True, False):
            for name, write in WRITES.items():
                with self.subTest(name, fail_open=fail_open):
                    hosts = Hosts(edge=edge_down, autumn=lambda _: check_answer("from_autumn"), real_edge=True)
                    client_for(hosts, edge_url=closed_url(), fail_open=fail_open).check(
                        **write, http_headers={"Idempotency-Key": "caller_key_1"}
                    )
                    self.assertEqual(hosts.keys("autumn"), ["caller_key_1"])

    def test_keeps_one_key_across_every_retry_and_fallback(self):
        for name, write in WRITES.items():
            with self.subTest(name):
                hosts = Hosts(edge=edge_down, autumn=lambda _: httpx.Response(503, json={"message": "Down"}))
                retries = RetryConfig("backoff", BackoffStrategy(1, 5, 1, 50), False)
                with self.assertRaises(Exception):
                    client_for(hosts, fail_open=False).check(**write, retries=retries)
                keys = hosts.keys("edge") + hosts.keys("autumn")
                self.assertGreater(len(hosts.sent["edge"]), 1)
                self.assertEqual(len(set(keys)), 1)
                self.assertIsNotNone(keys[0])

    def test_without_use_edge_goes_to_autumn_with_no_key(self):
        for name, write in WRITES.items():
            with self.subTest(name):
                hosts = Hosts(edge=lambda _: check_answer("from_edge"), autumn=lambda _: check_answer("from_autumn"))
                client_for(hosts, use_edge=False).check(**write)
                self.assertEqual(hosts.sent["edge"], [])
                self.assertEqual(hosts.keys("autumn"), [None])

    def test_a_plain_check_carries_no_key(self):
        hosts = Hosts(edge=edge_down, autumn=lambda _: check_answer("from_autumn"))
        client_for(hosts).check(**CHECK)
        self.assertEqual(hosts.keys("edge"), [None])
        self.assertEqual(hosts.keys("autumn"), [None])


class WriteCheckAsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_falls_back_with_the_same_key(self):
        hosts = Hosts(edge=edge_down, autumn=lambda _: check_answer("from_autumn"))
        response = await client_for(hosts).check_async(**WRITES["send_event"])
        self.assertEqual(response.customer_id, "from_autumn")
        [key] = hosts.keys("edge")
        self.assertRegex(key or "", UUID)
        self.assertEqual(hosts.keys("autumn"), [key])


class FinalizeTests(unittest.TestCase):
    def test_use_edge_leaves_finalize_with_autumn(self):
        hosts = Hosts(edge=lambda _: check_answer("from_edge"), autumn=lambda _: httpx.Response(200, json={"success": True}))
        client_for(hosts).balances.finalize(customer_id="customer_123", lock_id="lock_1", action="confirm")
        self.assertEqual(hosts.sent["edge"], [])
        self.assertEqual([r.url.path for r in hosts.sent["autumn"]], ["/v1/balances.finalize"])


TRACK: Dict[str, Any] = {"customer_id": "customer_123", "feature_id": "messages", "value": 3}
TRACK_PATH = "/v1/balances.track"


def track_reply(customer_id: str) -> Reply:
    return lambda _: httpx.Response(202, json={"customer_id": customer_id, "value": 3, "balance": None})


def duplicate_key(_request: httpx.Request) -> httpx.Response:
    return httpx.Response(
        409,
        json={
            "code": "duplicate_idempotency_key",
            "message": "Another request with idempotency key has already been received",
        },
    )


def forwarded(status: int, body: dict) -> Reply:
    """An answer the Autumn API gave through the edge."""
    return lambda _: httpx.Response(status, json=body, headers={"x-atom-forwarded": "track_denied"})


class TrackTests(unittest.TestCase):
    def test_use_edge_sends_track_to_the_edge_with_a_generated_body_key(self):
        hosts = Hosts(edge=track_reply("from_edge"), autumn=track_reply("from_autumn"))
        response = client_for(hosts).track(**TRACK)
        self.assertEqual(response.customer_id, "from_edge")
        self.assertEqual(paths(hosts, "edge"), [TRACK_PATH])
        self.assertEqual(hosts.sent["autumn"], [])
        [sent] = hosts.sent["edge"]
        body = json.loads(sent.content)
        self.assertRegex(body.pop("idempotency_key"), UUID)
        self.assertEqual(body, TRACK)
        self.assertEqual(sent.headers["content-length"], str(len(sent.content)))
        # A track's key is its body's, never the header.
        self.assertEqual(hosts.keys("edge"), [None])

    def test_client_edge_track_goes_to_the_edge_and_client_track_to_autumn(self):
        hosts = Hosts(edge=track_reply("from_edge"), autumn=track_reply("from_autumn"))
        client = client_for(hosts, use_edge=False)
        self.assertEqual(client.edge.track(**TRACK).customer_id, "from_edge")
        self.assertEqual(client.track(**TRACK).customer_id, "from_autumn")
        self.assertRegex(hosts.body_keys("edge")[0] or "", UUID)
        self.assertEqual(hosts.body_keys("autumn"), [None])

    def test_each_track_gets_its_own_key(self):
        hosts = Hosts(edge=track_reply("from_edge"), autumn=track_reply("from_autumn"))
        client = client_for(hosts)
        client.track(**TRACK)
        client.track(**TRACK)
        first, second = hosts.body_keys("edge")
        self.assertIsNotNone(first)
        self.assertNotEqual(first, second)

    def test_a_track_the_caller_keyed_by_header_goes_to_autumn_alone_as_sent(self):
        hosts = Hosts(edge=track_reply("from_edge"), autumn=track_reply("from_autumn"))
        response = client_for(hosts).track(**TRACK, http_headers={"Idempotency-Key": "caller_key_1"})
        self.assertEqual(response.customer_id, "from_autumn")
        self.assertEqual(hosts.sent["edge"], [])
        self.assertEqual(hosts.keys("autumn"), ["caller_key_1"])
        self.assertEqual(hosts.body_keys("autumn"), [None])

    def test_a_body_that_already_names_a_key_keeps_it_unmarked_as_the_sdks(self):
        from autumn_sdk._hooks.edge_clients import SDK_TRACK_KEY_EXTENSION
        from autumn_sdk._hooks.idempotency_key_hook import IdempotencyKeyHook

        client = client_for(Hosts(edge=track_reply("from_edge"), autumn=track_reply("from_autumn")))
        request = httpx.Request(
            "POST", f"{AUTUMN}{TRACK_PATH}", json={**TRACK, "idempotency_key": "caller_key_1"}
        )

        class Ctx:
            operation_id = "track"
            config = client.sdk_configuration

        sent = IdempotencyKeyHook().before_request(Ctx(), request)  # type: ignore[arg-type]
        self.assertIs(sent, request)
        self.assertNotIn(SDK_TRACK_KEY_EXTENSION, request.extensions)

    def test_without_use_edge_goes_to_autumn_with_no_key(self):
        hosts = Hosts(edge=track_reply("from_edge"), autumn=track_reply("from_autumn"))
        response = client_for(hosts, use_edge=False).track(**TRACK)
        self.assertEqual(response.customer_id, "from_autumn")
        self.assertEqual(hosts.sent["edge"], [])
        self.assertEqual(hosts.body_keys("autumn"), [None])

    def test_use_edge_without_an_edge_url_goes_to_autumn_with_no_key(self):
        hosts = Hosts(edge=track_reply("from_edge"), autumn=track_reply("from_autumn"))
        client_for(hosts, edge_url="").track(**TRACK)
        self.assertEqual(hosts.body_keys("autumn"), [None])

    def test_falls_back_on_the_404_of_an_edge_that_doesnt_serve_it_yet_with_the_same_key(self):
        hosts = Hosts(edge=edge_not_found, autumn=track_reply("from_autumn"))
        response = client_for(hosts, fail_open=False).track(**TRACK)
        self.assertEqual(response.customer_id, "from_autumn")
        self.assertEqual(paths(hosts, "autumn"), [TRACK_PATH])
        [key] = hosts.body_keys("edge")
        self.assertRegex(key or "", UUID)
        self.assertEqual(hosts.body_keys("autumn"), [key])

    def test_falls_back_after_an_edge_timeout_with_the_same_key(self):
        for fail_open in (True, False):
            with self.subTest(fail_open=fail_open):
                hosts = Hosts(edge=raises(httpx.ReadTimeout), autumn=track_reply("from_autumn"))
                response = client_for(hosts, fail_open=fail_open).track(**TRACK)
                self.assertEqual(response.customer_id, "from_autumn")
                [key] = hosts.body_keys("edge")
                self.assertRegex(key or "", UUID)
                self.assertEqual(hosts.body_keys("autumn"), [key])

    def test_falls_back_on_edge_down_with_the_same_key(self):
        for down_name, down in EDGE_DOWN_REPLIES.items():
            with self.subTest(down=down_name):
                hosts = Hosts(edge=down, autumn=track_reply("from_autumn"))
                response = client_for(hosts, fail_open=False).track(**TRACK)
                self.assertEqual(response.customer_id, "from_autumn")
                [key] = hosts.body_keys("edge")
                self.assertRegex(key or "", UUID)
                self.assertEqual(hosts.body_keys("autumn"), [key])

    def test_falls_back_when_the_edge_refuses_the_connection(self):
        hosts = Hosts(edge=edge_down, autumn=track_reply("from_autumn"), real_edge=True)
        response = client_for(hosts, edge_url=closed_url(), fail_open=False).track(**TRACK)
        self.assertEqual(response.customer_id, "from_autumn")
        self.assertRegex(hosts.body_keys("autumn")[0] or "", UUID)

    def test_is_not_sent_to_autumn_again_on_an_answer_the_edge_keeps(self):
        answers: Dict[str, tuple[Reply, int]] = {
            "a 400 the edge gave itself": (lambda _: httpx.Response(400, json={"code": "invalid_request"}), 400),
            "a 404 the API gave through the edge": (forwarded(404, {"code": "customer_not_found"}), 404),
            "a 500 the API gave through the edge": (forwarded(500, {"code": "internal_error"}), 500),
        }
        for name, (reply, status) in answers.items():
            with self.subTest(name):
                hosts = Hosts(edge=reply, autumn=track_reply("from_autumn"))
                with self.assertRaises(Exception) as caught:
                    client_for(hosts, fail_open=False).track(**TRACK)
                self.assertEqual(getattr(caught.exception, "status_code", None), status)
                self.assertEqual(hosts.sent["autumn"], [])

    def test_a_track_the_edge_forwarded_is_returned_as_is(self):
        edge = forwarded(202, {"customer_id": "from_api_through_edge", "value": 3, "balance": None})
        hosts = Hosts(edge=edge, autumn=track_reply("from_autumn"))
        self.assertEqual(client_for(hosts).track(**TRACK).customer_id, "from_api_through_edge")
        self.assertEqual(hosts.sent["autumn"], [])

    def test_a_duplicate_reply_on_the_fallback_for_the_sdks_own_key_is_the_tracks_success(self):
        # The edge recorded the track but its reply came too late; the API refuses the same key.
        hosts = Hosts(edge=raises(httpx.ReadTimeout), autumn=duplicate_key)
        response = client_for(hosts, fail_open=False).track(**TRACK)
        self.assertEqual((response.customer_id, response.value, response.balance), ("customer_123", 3, None))
        self.assertEqual(hosts.body_keys("autumn"), hosts.body_keys("edge"))

    def test_a_duplicate_reply_to_a_retry_for_the_sdks_own_key_is_the_tracks_success(self):
        attempts: List[int] = []

        def edge(request: httpx.Request) -> httpx.Response:
            attempts.append(1)
            return edge_down(request) if len(attempts) == 1 else duplicate_key(request)

        hosts = Hosts(edge=edge, autumn=lambda _: httpx.Response(503, json={"message": "Down"}))
        retries = RetryConfig("backoff", BackoffStrategy(1, 5, 1, 5_000), False)
        response = client_for(hosts, fail_open=False).track(
            customer_id="customer_123", feature_id="messages", retries=retries
        )
        self.assertEqual((response.customer_id, response.value), ("customer_123", 1))
        self.assertEqual(len(set(hosts.body_keys("edge") + hosts.body_keys("autumn"))), 1)

    def test_a_duplicate_reply_for_the_callers_own_key_is_the_callers_error(self):
        hosts = Hosts(edge=track_reply("from_edge"), autumn=duplicate_key)
        with self.assertRaises(Exception) as caught:
            client_for(hosts, fail_open=False).track(**TRACK, http_headers={"Idempotency-Key": "caller_key_1"})
        self.assertEqual(getattr(caught.exception, "status_code", None), 409)
        self.assertEqual(hosts.sent["edge"], [])

    def test_use_edge_leaves_track_tokens_with_autumn(self):
        hosts = Hosts(edge=track_reply("from_edge"), autumn=lambda _: httpx.Response(500, json={}))
        with self.assertRaises(Exception):
            client_for(hosts, fail_open=False).track_tokens(
                customer_id="customer_123", model_id="model_1", input_tokens=1, output_tokens=1
            )
        self.assertEqual(hosts.sent["edge"], [])
        self.assertEqual(paths(hosts, "autumn"), ["/v1/balances.track_tokens"])


class TrackAsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_falls_back_with_the_same_key(self):
        hosts = Hosts(edge=edge_down, autumn=track_reply("from_autumn"))
        response = await client_for(hosts).track_async(**TRACK)
        self.assertEqual(response.customer_id, "from_autumn")
        [key] = hosts.body_keys("edge")
        self.assertRegex(key or "", UUID)
        self.assertEqual(hosts.body_keys("autumn"), [key])

    async def test_a_duplicate_reply_on_the_fallback_for_the_sdks_own_key_is_the_tracks_success(self):
        hosts = Hosts(edge=edge_down, autumn=duplicate_key)
        response = await client_for(hosts, fail_open=False).track_async(**TRACK)
        self.assertEqual((response.customer_id, response.value), ("customer_123", 3))


def customer_reply(customer_id: str) -> Reply:
    body = {
        "id": customer_id, "name": None, "email": None, "created_at": 0, "fingerprint": None, "stripe_id": None,
        "env": "sandbox", "metadata": {}, "send_email_receipts": False, "billing_controls": {},
        "subscriptions": [], "purchases": [], "licenses": [], "balances": {}, "flags": {},
    }
    return lambda _: httpx.Response(200, json=body)


def entity_reply(entity_id: str) -> Reply:
    body = {
        "id": entity_id, "name": None, "customer_id": "customer_123", "feature_id": "seats", "created_at": 0,
        "env": "sandbox", "subscriptions": [], "purchases": [], "balances": {}, "flags": {},
    }
    return lambda _: httpx.Response(200, json=body)


# The reads the edge answers, by name: their path, a stand-in answering with `id` naming who answered, and the call.
READS: Dict[str, tuple[str, Callable[[str], Reply], Callable[[Autumn], Any]]] = {
    "customers.get": (
        "/v1/customers.get", customer_reply, lambda client: client.customers.get(customer_id="customer_123")
    ),
    "entities.get": (
        "/v1/entities.get",
        entity_reply,
        lambda client: client.entities.get(customer_id="customer_123", entity_id="entity_1"),
    ),
    "customers.get_or_create": (
        "/v1/customers.get_or_create",
        customer_reply,
        lambda client: client.customers.get_or_create(customer_id="customer_123"),
    ),
}

def edge_not_found(_request: httpx.Request) -> httpx.Response:
    """What an edge from before it served reads answers them with."""
    return httpx.Response(404, text="404 Not Found")


# Refusals the edge gives itself, not the API's answers it forwarded.
EDGE_REFUSALS: Dict[str, Reply] = {
    "404 from an edge that doesn't serve reads yet": edge_not_found,
    "400 invalid_request": lambda _: httpx.Response(400, json={"message": "Bad body", "code": "invalid_request"}),
}


def forwarded_not_found(_request: httpx.Request) -> httpx.Response:
    return httpx.Response(
        404,
        json={"message": "Customer not found", "code": "customer_not_found"},
        headers={"x-atom-forwarded": "customer_not_stored"},
    )


def paths(hosts: Hosts, host: str) -> List[str]:
    return [request.url.path for request in hosts.sent[host]]


class ReadTests(unittest.TestCase):
    def test_use_edge_sends_each_read_to_the_edge(self):
        for name, (path, reply, send) in READS.items():
            with self.subTest(name):
                hosts = Hosts(edge=reply("from_edge"), autumn=reply("from_autumn"))
                self.assertEqual(send(client_for(hosts)).id, "from_edge")
                self.assertEqual(paths(hosts, "edge"), [path])
                self.assertEqual(hosts.sent["autumn"], [])

    def test_falls_back_on_a_refusal_the_edge_gave_itself(self):
        for refusal_name, refusal in EDGE_REFUSALS.items():
            for name, (path, reply, send) in READS.items():
                with self.subTest(name, refusal=refusal_name):
                    hosts = Hosts(edge=refusal, autumn=reply("from_autumn"))
                    self.assertEqual(send(client_for(hosts)).id, "from_autumn")
                    self.assertEqual(len(hosts.sent["edge"]), 1)
                    self.assertEqual(paths(hosts, "autumn"), [path])

    def test_returns_the_apis_own_404_the_edge_forwarded(self):
        for name, (_path, reply, send) in READS.items():
            with self.subTest(name):
                hosts = Hosts(edge=forwarded_not_found, autumn=reply("from_autumn"))
                with self.assertRaises(Exception) as caught:
                    send(client_for(hosts))
                self.assertEqual(getattr(caught.exception, "status_code", None), 404)
                self.assertEqual(len(hosts.sent["edge"]), 1)
                self.assertEqual(hosts.sent["autumn"], [])

    def test_falls_back_on_edge_down(self):
        for down_name, down in EDGE_DOWN_REPLIES.items():
            for name, (_path, reply, send) in READS.items():
                with self.subTest(name, down=down_name):
                    hosts = Hosts(edge=down, autumn=reply("from_autumn"))
                    self.assertEqual(send(client_for(hosts)).id, "from_autumn")
                    self.assertEqual(len(hosts.sent["edge"]), 1)
                    self.assertEqual(len(hosts.sent["autumn"]), 1)

    def test_without_use_edge_goes_to_autumn(self):
        for name, (_path, reply, send) in READS.items():
            with self.subTest(name):
                hosts = Hosts(edge=reply("from_edge"), autumn=reply("from_autumn"))
                self.assertEqual(send(client_for(hosts, use_edge=False)).id, "from_autumn")
                self.assertEqual(hosts.sent["edge"], [])

    def test_a_check_returns_the_edges_own_404(self):
        hosts = Hosts(edge=edge_not_found, autumn=lambda _: check_answer("from_autumn"))
        with self.assertRaises(Exception) as caught:
            client_for(hosts, fail_open=False).check(**CHECK)
        self.assertEqual(getattr(caught.exception, "status_code", None), 404)
        self.assertEqual(hosts.sent["autumn"], [])


class ReadAsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_falls_back_on_the_edges_own_404(self):
        hosts = Hosts(edge=edge_not_found, autumn=customer_reply("from_autumn"))
        response = await client_for(hosts).customers.get_async(customer_id="customer_123")
        self.assertEqual(response.id, "from_autumn")
        self.assertEqual(paths(hosts, "edge"), ["/v1/customers.get"])
        self.assertEqual(paths(hosts, "autumn"), ["/v1/customers.get"])


if __name__ == "__main__":
    unittest.main()
