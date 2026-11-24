"""Cost adversary pass 7, P7 + P8: "request sent" is stamped where the request leaves the process, never before.

Real: the funnel's ``stamp_request_sent_on_failure``, the transport stamp (``wire_sent.py``), the real google-genai,
openai and groq SDKs, ``capture_request_payload``. Double: the provider's server (an httpx ``MockTransport`` answering
the SDK's real serialized request), and an unreachable port for the never-connected case.

* P7: google-genai rejects a bad setting client-side (pydantic) after the snapshot and before any connection; it was
  stamped "sent" and booked at the catalog price. Now unstamped (free).
* P8: a speech call that WAS sent (and billed) and then failed locally carried no stamp (openai / groq speech never ran
  the snapshot): booked free, filed nowhere. Now stamped by the transport whatever path sent it.
"""

from __future__ import annotations

import pytest

from matrx_ai.providers.errors import stamp_request_sent_on_failure, was_request_sent
from matrx_ai.providers.outbound_capture import resolve_sdk_httpx
from matrx_ai.providers.snapshot import capture_request_payload


def _mock_client(sdk: object) -> object:
    flavor = resolve_sdk_httpx(sdk)

    def answer(request: object) -> object:
        return flavor.Response(200, content=b"RIFF....audio", headers={"content-type": "audio/wav"})

    # NOT a capture client: the SDK frames on the stack alone make it a provider send.
    return flavor.AsyncClient(transport=flavor.MockTransport(answer))


def test_an_sdk_client_side_rejection_after_the_snapshot_is_not_sent() -> None:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key="not-a-key", http_options=types.HttpOptions(base_url="http://127.0.0.1:9"))
    kwargs = {"model": "imagen-4.0-generate-001", "prompt": "a lighthouse", "config": {"number_of_images": "many"}}
    with pytest.raises(Exception) as caught, stamp_request_sent_on_failure():
        capture_request_payload(kwargs, provider="google")
        client.models.generate_images(**kwargs)
    assert not was_request_sent(caught.value)


@pytest.mark.parametrize("sdk_name", ["openai", "groq"])
async def test_a_failure_after_a_sent_speech_call_is_stamped_sent(sdk_name: str) -> None:
    import importlib

    sdk = importlib.import_module(sdk_name)
    client_cls = sdk.AsyncOpenAI if sdk_name == "openai" else sdk.AsyncGroq
    client = client_cls(api_key="k", base_url="http://provider.test/v1", http_client=_mock_client(sdk), max_retries=0)
    with pytest.raises(ValueError) as caught, stamp_request_sent_on_failure():
        response = await client.audio.speech.create(model="m", voice="v", input="hello")
        body = response.read()
        assert (await body) if hasattr(body, "__await__") else body  # sdk versions differ: sync or async read()
        raise ValueError("audio body could not be decoded")  # after the billed call returned
    assert was_request_sent(caught.value)


async def test_a_call_that_never_connected_is_not_sent() -> None:
    import openai

    client = openai.AsyncOpenAI(api_key="k", base_url="http://127.0.0.1:9/v1", max_retries=0)
    with pytest.raises(openai.APIConnectionError) as caught, stamp_request_sent_on_failure():
        await client.audio.speech.create(model="m", voice="v", input="hello")
    assert not was_request_sent(caught.value)


async def test_a_non_provider_request_inside_the_funnel_is_not_a_send() -> None:
    import httpx

    fetch = httpx.AsyncClient(transport=httpx.MockTransport(lambda r: httpx.Response(200, content=b"img")))
    with pytest.raises(ValueError) as caught, stamp_request_sent_on_failure():
        await fetch.get("http://cdn.test/a.png")  # a media fetch before the provider call
        raise ValueError("bad setting")
    assert not was_request_sent(caught.value)


async def test_a_capture_client_request_is_a_send() -> None:
    import httpx

    from matrx_ai.providers.outbound_capture import make_capture_http_client

    http = make_capture_http_client(transport=httpx.MockTransport(lambda r: httpx.Response(200, content=b"x")))
    with pytest.raises(ValueError) as caught, stamp_request_sent_on_failure():
        await http.post("http://provider.test/v1/tts", json={"text": "hi"})  # a raw provider call site (xAI speech)
        raise ValueError("audio body could not be decoded")
    assert was_request_sent(caught.value)


def test_every_transport_seam_carries_the_stamp() -> None:
    from matrx_ai.providers.wire_sent import wire_sent_seams

    seams = wire_sent_seams()
    assert seams and all(seams.values()), seams
