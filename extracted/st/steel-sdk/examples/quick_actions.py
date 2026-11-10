from steel import Steel

client = Steel()


def main() -> None:
    url = "https://steel.dev"

    page = client.scrape(url=url, format=["markdown"])
    print((page.content.markdown or "")[:500])

    screenshot = client.screenshot(url=url, full_page=True)
    print(f"Screenshot: {screenshot.url}")

    pdf = client.pdf(url=url)
    print(f"PDF: {pdf.url}")


if __name__ == "__main__":
    main()
