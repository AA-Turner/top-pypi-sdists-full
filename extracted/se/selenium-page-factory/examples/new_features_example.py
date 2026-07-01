"""
Example demonstrating the new features added to selenium-page-factory
- scroll_into_view: Scroll elements into view before interaction
- get_web_elements: Find multiple elements (lists)
- drag_and_drop_to: Drag and drop functionality
- click_with_retry: Retry mechanism for flaky elements
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumpagefactory.Pagefactory import PageFactory


class DemoPage(PageFactory):
    """Example Page Object with locators"""
    
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 15
        self.highlight = True
        
    # Define your locators as dictionary
    locators = {
        "search_box": ("ID", "search-input"),
        "search_button": ("CSS", "button.search-btn"),
        "footer_link": ("XPATH", "//footer//a[@class='contact']"),
        "draggable_item": ("ID", "draggable"),
        "drop_zone": ("ID", "droppable"),
        "dynamic_button": ("CSS", "button.dynamic-load"),
    }


def example_scroll_into_view():
    """
    Example 1: scroll_into_view
    Useful when element is not in viewport (below the fold)
    """
    driver = webdriver.Chrome()
    driver.get("https://example.com")
    
    page = DemoPage(driver)
    
    # Scroll footer link into view before clicking
    page.footer_link.scroll_into_view()  # Aligns to top by default
    page.footer_link.click_button()
    
    # Or align to bottom of viewport
    page.footer_link.scroll_into_view(align_to_top=False)
    
    driver.quit()


def example_multiple_elements():
    """
    Example 2: get_web_elements (Multiple Elements Support)
    Essential for working with lists, tables, search results, etc.
    """
    driver = webdriver.Chrome()
    driver.get("https://example.com/search-results")
    
    page = DemoPage(driver)
    
    # Get all search result elements
    search_results = page.get_web_elements(By.CSS_SELECTOR, ".result-item")
    
    print(f"Found {len(search_results)} search results")
    
    # Iterate through results
    for idx, result in enumerate(search_results):
        title = result.find_element(By.CLASS_NAME, "title").text
        print(f"Result {idx + 1}: {title}")
    
    # Get all table rows
    table_rows = page.get_web_elements(By.XPATH, "//table//tr")
    
    # Click on specific item in list
    if len(search_results) > 2:
        search_results[2].click()  # Click 3rd result
    
    driver.quit()


def example_drag_and_drop():
    """
    Example 3: drag_and_drop_to
    Complete ActionChains support for drag and drop operations
    """
    driver = webdriver.Chrome()
    driver.get("https://example.com/drag-drop-demo")
    
    page = DemoPage(driver)
    
    # Drag an item to drop zone
    page.draggable_item.drag_and_drop_to(page.drop_zone)
    
    # Can also chain with other operations
    page.draggable_item.scroll_into_view().drag_and_drop_to(page.drop_zone)
    
    driver.quit()


def example_click_with_retry():
    """
    Example 4: click_with_retry
    Handles flaky tests with stale element references
    """
    driver = webdriver.Chrome()
    driver.get("https://example.com/dynamic-content")
    
    page = DemoPage(driver)
    
    # Click with default retry (3 attempts, 1 second delay)
    page.dynamic_button.click_with_retry()
    
    # Custom retry settings (5 attempts, 2 second delay)
    page.dynamic_button.click_with_retry(retries=5, delay=2)
    
    # Useful for elements that reload frequently
    # or in Single Page Applications with dynamic DOM updates
    
    driver.quit()


def example_combined_usage():
    """
    Example 5: Combining multiple new features
    Real-world scenario demonstrating all features together
    """
    driver = webdriver.Chrome()
    driver.get("https://example.com/shopping")
    
    page = DemoPage(driver)
    
    # 1. Get all product cards
    products = page.get_web_elements(By.CSS_SELECTOR, ".product-card")
    
    # 2. Scroll to a specific product and click with retry
    if len(products) > 5:
        products[5].scroll_into_view()
        products[5].find_element(By.CLASS_NAME, "add-to-cart").click_with_retry()
    
    # 3. Drag product to cart (if supported)
    cart_icon = driver.find_element(By.ID, "cart-icon")
    if len(products) > 0:
        products[0].drag_and_drop_to(cart_icon)
    
    # 4. Process all products in a list
    for product in products:
        product.scroll_into_view(align_to_top=False)
        title = product.find_element(By.CLASS_NAME, "title").get_text()
        price = product.find_element(By.CLASS_NAME, "price").get_text()
        print(f"{title}: {price}")
    
    driver.quit()


def example_with_page_factory_locators():
    """
    Example 6: Using new methods with Page Factory locators
    Shows how new methods work seamlessly with existing PageFactory pattern
    """
    driver = webdriver.Chrome()
    driver.get("https://example.com")
    
    page = DemoPage(driver)
    
    # All WebElement methods from locators support new features
    page.search_box.scroll_into_view().set_text("selenium automation")
    page.search_button.click_with_retry()
    
    # For multiple elements, use get_web_elements directly
    results = page.get_web_elements(By.CSS_SELECTOR, ".search-result")
    for result in results:
        result.scroll_into_view()
        print(result.get_text())
    
    driver.quit()


if __name__ == "__main__":
    print("New Features Examples for selenium-page-factory")
    print("=" * 50)
    print("\n1. scroll_into_view - Scroll element into viewport")
    print("2. get_web_elements - Find multiple elements")
    print("3. drag_and_drop_to - Drag and drop support")
    print("4. click_with_retry - Retry mechanism for flaky elements")
    print("\nRun individual functions to see examples")
    print("Note: Update URLs and locators for your actual application")

