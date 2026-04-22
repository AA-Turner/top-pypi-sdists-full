from dotenv import load_dotenv

load_dotenv()

import asyncio
import json

from scrapegraph_py import AsyncScrapeGraphAI


async def main():
    async with AsyncScrapeGraphAI() as sgai:
        res = await sgai.extract(
            "What is this page about? Extract the main heading and description.",
            url="https://example.com",
        )

        if res.status == "success":
            print("Extracted:", json.dumps(res.data.json_data, indent=2))
            print("\nTokens used:", res.data.usage)
        else:
            print("Failed:", res.error)


asyncio.run(main())
