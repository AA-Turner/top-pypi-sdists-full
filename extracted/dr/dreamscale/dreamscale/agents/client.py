"""Authenticated hosted decisions; retries recover identities, never new generations."""

import asyncio

import httpx
from dreamscale_transport.llm import TurnResult


class Gateway:
    def __init__(self, url, key, *, client=None):
        self.client = client or httpx.AsyncClient(
            base_url=url.rstrip("/"), headers={"Authorization": f"Bearer {key}"}, timeout=40
        )

    async def create(self, request):
        response = await self.client.post("/v1/llm/sessions", json=request.model_dump(mode="json"))
        self.check(response)
        return response.json()["id"]

    @staticmethod
    def check(response):
        if response.is_error:
            try:
                message = response.json().get("detail", "LLM gateway rejected the request.")
            except ValueError:
                message = "LLM gateway is unavailable."
            raise RuntimeError(str(message))

    async def turn(self, sid, turn):
        path = f"/v1/llm/sessions/{sid}/turns"
        submit = True
        async with asyncio.timeout(600):
            while True:
                try:
                    response = await (
                        self.client.post(path, json=turn.model_dump(mode="json"))
                        if submit
                        else self.client.get(path + "/" + turn.id)
                    )
                    if response.status_code == 404 and not submit:
                        # Admission may not have completed. Same identity and payload
                        # are safe to resubmit; the DB elects at most one generation.
                        submit = True
                    else:
                        self.check(response)
                        result = TurnResult.model_validate(response.json())
                        if result.status != "pending":
                            return result
                        submit = False
                except (httpx.TimeoutException, httpx.NetworkError):
                    submit = False
                await asyncio.sleep(1)

    async def close(self, sid):
        response = await self.client.delete(f"/v1/llm/sessions/{sid}")
        self.check(response)

    async def aclose(self):
        await self.client.aclose()
