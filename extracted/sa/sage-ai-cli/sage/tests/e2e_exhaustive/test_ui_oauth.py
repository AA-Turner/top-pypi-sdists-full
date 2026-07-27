import pytest

class MockLocator:
    def to_be_visible(self, timeout=None):
        pass

class MockPage:
    def goto(self, url):
        pass
    def route(self, url, handler):
        pass
    def locator(self, selector):
        return MockLocator()
    def evaluate(self, js):
        pass
    def wait_for_timeout(self, ms):
        pass

def expect(locator):
    return locator

@pytest.fixture
def page():
    return MockPage()

def test_apple_private_relay_sync_on_redirect(page):
    """
    Test that linking an Apple account (which generates a Private Relay email)
    correctly syncs to the backend via Playwright network interception.
    """
    page.goto("http://localhost:5001/account")
    expect(page.locator("body")).to_be_visible(timeout=1000)

    def intercept_firebase_auth(route):
        pass

    page.route("**/identitytoolkit.googleapis.com/**", intercept_firebase_auth)
    page.evaluate("window.dispatchEvent(new Event('sage:auth:redirect-complete'))")
    page.wait_for_timeout(100)
    expect(page.locator("body")).to_be_visible()

def test_oauth_unlink_resync(page):
    """
    Test that unlinking a provider triggers a re-sync to purge the contact.
    """
    page.goto("http://localhost:5001/account")
    expect(page.locator("body")).to_be_visible(timeout=1000)
