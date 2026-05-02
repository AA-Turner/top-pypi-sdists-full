async def request_summary(read_stream, write_stream, prompt: str) -> str:
    """
    Use MCP sampling to ask Claude to generate a summary.
    The MCP client (Claude Desktop) handles the actual model call.
    """
    try:
        from mcp.types import (
            CreateMessageRequest,
            CreateMessageRequestParams,
            TextContent as MCPTextContent,
            SamplingMessage,
        )
        import mcp.types as types

        request = CreateMessageRequest(
            method="sampling/createMessage",
            params=CreateMessageRequestParams(
                messages=[
                    SamplingMessage(
                        role="user",
                        content=MCPTextContent(type="text", text=prompt)
                    )
                ],
                maxTokens=500,
                systemPrompt=(
                    "You are a senior software engineer. Given Java source code or "
                    "structured data about a Spring Boot class, write a concise "
                    "plain-English summary. Focus on: what the class does, its "
                    "responsibilities, and any notable design observations. "
                    "Be direct and technical. 3-5 sentences max."
                ),
            )
        )

        response = await write_stream.send_request(request)
        if response and hasattr(response, 'content'):
            content = response.content
            if isinstance(content, list) and len(content) > 0:
                return content[0].text if hasattr(content[0], 'text') else str(content[0])
            if hasattr(content, 'text'):
                return content.text

    except Exception as e:
        return ""
    
    return ""
