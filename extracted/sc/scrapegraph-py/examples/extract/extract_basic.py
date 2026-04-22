from dotenv import load_dotenv

load_dotenv()

import json

from scrapegraph_py import ScrapeGraphAI

sgai = ScrapeGraphAI()

res = sgai.extract(
    "What is this page about? Extract the main heading and description.",
    url="https://example.com",
)

if res.status == "success":
    print("Extracted:", json.dumps(res.data.json_data, indent=2))
    print("\nTokens used:", res.data.usage)
else:
    print("Failed:", res.error)
