import asyncio

from agentql.tools.async_api import query_document


async def main():
    PROMPT = """
    get name
    """
    file_path = "path/to/file.pdf"

    response = await query_document(
        file_path,
        prompt=PROMPT,
        timeout=10,
        mode="fast",
    )
    print(f"name: {response['name']}")


if __name__ == "__main__":
    asyncio.run(main())
