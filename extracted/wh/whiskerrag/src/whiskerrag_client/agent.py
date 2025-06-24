import json
from typing import Any, AsyncIterator, Dict

import httpx

from whiskerrag_client.http_client import BaseClient
from whiskerrag_types.model.agent import ProResearchRequest


class AgentClient:
    """Agent API client for research tasks"""

    def __init__(self, http_client: BaseClient, base_path: str = "/v1/api/agent"):
        self.http_client = http_client
        self.base_path = base_path

    async def pro_research(
        self, request: ProResearchRequest
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        Pro research method, return streaming response

        Args:
            request: ProResearchRequest instance, contains all parameters for research request

        Yields:
            Dict[str, Any]: streaming response data blocks

        Example:
            >>> client = AgentClient(http_client)
            >>> request = ProResearchRequest(
            ...     messages=[HumanMessage(content="research the history of artificial intelligence")],
            ...     enable_knowledge_retrieval=True
            ... )
            >>> async for chunk in client.pro_research(request):
            ...     print(chunk)
        """
        # build complete URL
        url = f"{self.http_client.base_url}{self.base_path}/pro_research"

        # prepare request data
        json_data = request.model_dump()

        # use low-level httpx client for streaming request
        if hasattr(self.http_client, "client") and isinstance(
            self.http_client.client, httpx.AsyncClient
        ):
            async with self.http_client.client.stream(
                method="POST",
                url=url,
                json=json_data,
                headers=self.http_client.headers,
                timeout=self.http_client.timeout,
            ) as response:
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if line:
                        # handle Server-Sent Events (SSE) format
                        if line.startswith("data: "):
                            data_str = line[6:]  # remove "data: " prefix
                            if data_str.strip() == "[DONE]":
                                break
                            try:
                                yield json.loads(data_str)
                            except json.JSONDecodeError:
                                # if not JSON format, return text directly
                                yield {"content": data_str, "type": "text"}
                        else:
                            # handle normal JSON lines
                            try:
                                yield json.loads(line)
                            except json.JSONDecodeError:
                                # if not JSON format, return text directly
                                yield {"content": line, "type": "text"}
        else:
            raise ValueError("HTTP client does not support streaming")

    async def pro_research_sync(self, request: ProResearchRequest) -> Dict[str, Any]:
        """
        Synchronous version of pro research method, wait for complete response

        Args:
            request: ProResearchRequest instance

        Returns:
            Dict[str, Any]: complete research result
        """
        # collect all streaming responses
        chunks = []
        async for chunk in self.pro_research(request):
            chunks.append(chunk)

        # merge all response blocks
        if chunks:
            # if the last block contains the complete result, return it
            if len(chunks) == 1:
                return chunks[0]

            # otherwise
            combined_content = []
            for chunk in chunks:
                if isinstance(chunk, dict):
                    if "content" in chunk:
                        combined_content.append(str(chunk["content"]))
                    else:
                        combined_content.append(str(chunk))
                else:
                    combined_content.append(str(chunk))

            return {
                "content": "\n".join(combined_content),
                "type": "combined",
                "chunks_count": len(chunks),
            }
        else:
            return {"content": "", "type": "empty"}
