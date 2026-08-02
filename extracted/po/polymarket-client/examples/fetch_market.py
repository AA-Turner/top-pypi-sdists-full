"""Fetch a single market by url, slug, and id.

    uv run python -m examples.fetch_market

No credentials required. Discovers a few live markets, then re-fetches them
three ways.
"""

from __future__ import annotations

from polymarket import PublicClient


def main() -> None:
    with PublicClient() as client:
        items = client.list_markets(page_size=3).first_page().items
        if len(items) < 3:
            raise SystemExit("Not enough live markets to demo all three lookups.")

        slug0 = items[0].slug
        slug1 = items[1].slug
        if slug0 is None or slug1 is None:
            raise SystemExit("Discovered markets are missing slugs; try again.")

        by_url = client.get_market(url=f"https://polymarket.com/market/{slug0}")
        by_slug = client.get_market(slug=slug1)
        by_id = client.get_market(id=str(items[2].id))

        print(f"URL lookup:  {by_url.question or by_url.id}")
        print(f"Slug lookup: {by_slug.question or by_slug.id}")
        print(f"ID lookup:   {by_id.question or by_id.id}")


if __name__ == "__main__":
    main()
