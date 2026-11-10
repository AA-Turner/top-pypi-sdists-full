import asyncio

from playwright.async_api import async_playwright

from steel import AsyncSteel

client = AsyncSteel()


async def main() -> None:
    session = await client.sessions.create()
    print(f"Watch the session live at {session.session_viewer_url}")

    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.connect_over_cdp(
                f"{session.websocket_url}&apiKey={client.steel_api_key}"
            )
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            page = context.pages[0] if context.pages else await context.new_page()

            await page.goto("https://example.com")
            print(await page.title())

            await browser.close()
    finally:
        await client.sessions.release(session.id)


if __name__ == "__main__":
    asyncio.run(main())
