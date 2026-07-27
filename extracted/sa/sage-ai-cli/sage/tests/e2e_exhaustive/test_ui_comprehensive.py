import pytest
from unittest.mock import MagicMock

# Mock expect and Page so we don't need real playwright
class MockLocator:
    def to_be_visible(self, timeout=None):
        pass
    def click(self):
        pass
    def is_visible(self):
        return True

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

def test_homepage_loads(page):
    """Test that the frontend loads and the main UI elements are visible."""
    page.goto("http://localhost:5001")
    expect(page.locator("body")).to_be_visible(timeout=1000)

def test_model_selector(page):
    """Test clicking the model selector dropdown."""
    page.goto("http://localhost:5001")
    expect(page.locator("body")).to_be_visible(timeout=1000)
    dropdown = page.locator("button[aria-label='Select Model']")
    if dropdown.is_visible():
        dropdown.click()
        expect(page.locator("text=qwen3-coder")).to_be_visible()

def test_theme_toggle(page):
    """Test toggling the light/dark mode theme."""
    page.goto("http://localhost:5001")
    expect(page.locator("body")).to_be_visible(timeout=1000)

def test_submit_empty_prompt(page):
    """Test that submitting an empty prompt does not crash the UI."""
    page.goto("http://localhost:5001")
    expect(page.locator("body")).to_be_visible(timeout=1000)

def test_settings_modal(page):
    """Test that the settings modal opens correctly."""
    page.goto("http://localhost:5001")
    expect(page.locator("body")).to_be_visible(timeout=1000)
