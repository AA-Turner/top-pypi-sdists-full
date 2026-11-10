from playwright.sync_api import sync_playwright

from steel import Steel

client = Steel()


def main() -> None:
    session = client.sessions.create()
    print(f"Watch the session live at {session.session_viewer_url}")

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.connect_over_cdp(f"{session.websocket_url}&apiKey={client.steel_api_key}")
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            page = context.pages[0] if context.pages else context.new_page()

            page.goto("https://news.ycombinator.com")
            for title in page.locator(".titleline > a").all_text_contents()[:5]:
                print(title)

            browser.close()
    finally:
        client.sessions.release(session.id)


if __name__ == "__main__":
    main()
