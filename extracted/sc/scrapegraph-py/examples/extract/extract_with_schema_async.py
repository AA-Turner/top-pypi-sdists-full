from dotenv import load_dotenv

load_dotenv()

import asyncio
import json

from scrapegraph_py import AsyncScrapeGraphAI


async def main():
    async with AsyncScrapeGraphAI() as sgai:
        res = await sgai.extract(
            "Extract structured information about this page",
            url="https://example.com",
            schema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "links": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": ["title"],
            },
        )

        if res.status == "success":
            print("Extracted:", json.dumps(res.data.json_data, indent=2))
            print("\nRaw:", res.data.raw)
            print("\nTokens used:", res.data.usage)
        else:
            print("Failed:", res.error)


asyncio.run(main())
