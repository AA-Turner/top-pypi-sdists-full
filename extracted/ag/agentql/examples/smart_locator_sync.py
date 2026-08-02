from playwright.sync_api import sync_playwright

import agentql


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = agentql.wrap(browser.new_page())
        page.goto("https://www.google.com/")

        search_box = page.get_by_prompt("Search input field")  # type: ignore
        search_btn = page.get_by_prompt("Search button which initiaties the search")  # type: ignore

        if search_box is None or search_btn is None:
            print("Element not found")
            return

        search_box.type("Tiny Fish")
        search_btn.click(force=True)

        page.wait_for_timeout(5000)


if __name__ == "__main__":
    main()
