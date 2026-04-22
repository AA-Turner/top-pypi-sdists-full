from dotenv import load_dotenv

load_dotenv()

from scrapegraph_py import MarkdownFormatConfig, ScrapeGraphAI

sgai = ScrapeGraphAI()

res = sgai.scrape(
    "https://example.com",
    formats=[MarkdownFormatConfig()],
)

if res.status == "success":
    print("Markdown:", res.data.results.get("markdown", {}).get("data"))
    print(f"\nTook {res.elapsed_ms}ms")
else:
    print("Failed:", res.error)
