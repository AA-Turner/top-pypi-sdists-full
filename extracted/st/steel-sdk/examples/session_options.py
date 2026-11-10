from steel import Steel

client = Steel()


def main() -> None:
    session = client.sessions.create(
        use_proxy=True,
        solve_captcha=True,
        block_ads=True,
        region="us-east",
        timeout=10 * 60 * 1000,
        dimensions={"width": 1440, "height": 900},
    )

    try:
        print(f"Session {session.id} runs in {session.region} for up to {session.timeout} ms")
        print(f"Proxy: {session.proxy_source}, captcha solving: {session.solve_captcha}")
        print(f"Connect Playwright or Puppeteer to {session.websocket_url}&apiKey=<your API key>")
    finally:
        client.sessions.release(session.id)


if __name__ == "__main__":
    main()
