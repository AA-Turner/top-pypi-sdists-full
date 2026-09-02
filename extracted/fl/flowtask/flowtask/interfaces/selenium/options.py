USER_AGENTS = [
    # Chrome 148 - Desktop (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    # Chrome 148 - Desktop (Mac)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",  # noqa
    # Chrome 148 - Desktop (Linux)
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    # Safari 17 - Desktop (Mac)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",  # noqa
    # Firefox 138 - Desktop (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
    # Edge 148 - Desktop (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0",  # noqa
    # Chrome 148 - Mobile (Android)
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36",  # noqa
    # Safari 17 - Mobile (iOS)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",  # noqa
    # Firefox 138 - Desktop (Linux)
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0",
]  # noqa


DESKTOP_USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0',
]

MOBILE_USER_AGENTS = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
]

MOBILE_DEVICES = [
    'iPhone X',
    'iPhone 12 Pro',
    'iPhone 14 Pro Max',
    'Google Nexus 7',
    'Pixel 2',
    'Pixel 5',
    'Samsung Galaxy S21',
    'Samsung Galaxy Tab',
    'iPad Pro'
]

# Browser options configurations
CHROME_OPTIONS = [
    "--disable-gpu",
    "--no-sandbox",
    "--lang=en",
    "--disable-dev-shm-usage",
    "--disable-features=VizDisplayCompositor",
    "--disable-features=IsolateOrigins",
    "--disable-blink-features=AutomationControlled",
    "--window-size=1920,1080",
]

UNDETECTED_OPTIONS = [
    "--disable-gpu",
    "--no-sandbox",
    "--disable-blink-features=AutomationControlled",
    "--disable-features=NetworkService,NetworkServiceInProcess",
    "--disable-dev-shm-usage",
    "--disable-http2",
]

FIREFOX_OPTIONS = [
    "--no-sandbox",
    "--disable-gpu",
    "--width=1920",
    "--height=1080"
]
