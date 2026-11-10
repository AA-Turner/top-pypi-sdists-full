import time
from typing import TypeVar, Callable

from playwright.sync_api import BrowserContext, sync_playwright

from steel import Steel

T = TypeVar("T")

client = Steel()


def in_browser(websocket_url: str, use: Callable[[BrowserContext], T]) -> T:
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(f"{websocket_url}&apiKey={client.steel_api_key}")
        try:
            return use(browser.contexts[0] if browser.contexts else browser.new_context())
        finally:
            browser.close()


def wait_for_profile(profile_id: str) -> None:
    while True:
        profile = client.profiles.get(profile_id)
        if profile.status == "READY":
            return
        if profile.status == "FAILED":
            raise RuntimeError(f"Profile {profile_id} could not be saved")
        time.sleep(2)


def main() -> None:
    first = client.sessions.create(persist_profile=True)
    profile_id = first.profile_id
    if profile_id is None:
        raise RuntimeError("The session did not create a profile")

    try:
        in_browser(
            first.websocket_url,
            lambda context: context.add_cookies(
                [
                    {
                        "name": "greeting",
                        "value": "saved by the first session",
                        "url": "https://example.com",
                        "expires": time.time() + 24 * 60 * 60,
                    }
                ]
            ),
        )
    finally:
        client.sessions.release(first.id)

    wait_for_profile(profile_id)

    second = client.sessions.create(profile_id=profile_id)
    try:
        cookies = in_browser(second.websocket_url, lambda context: context.cookies("https://example.com"))
        greeting = next((cookie.get("value") for cookie in cookies if cookie.get("name") == "greeting"), None)
        print(f"The second session sees: {greeting or 'nothing'}")
    finally:
        client.sessions.release(second.id)


if __name__ == "__main__":
    main()
