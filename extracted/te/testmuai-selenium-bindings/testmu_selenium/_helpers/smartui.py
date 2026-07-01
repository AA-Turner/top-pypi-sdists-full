def smartui_snapshot(driver, name, options=None):
    """Capture a SmartUI snapshot for a Selenium WebDriver session."""
    from lambdatest_selenium_driver import smartui_snapshot as _smartui_snapshot

    if options is None:
        options = {}
    return _smartui_snapshot(driver, name, options)
