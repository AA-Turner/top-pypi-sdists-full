def wait_for_dom(driver, timeout=10):
    """Wait for document.readyState to become 'complete'.

    This is a pragmatic port of V2 wait_for_dom. V2's implementation also
    checks jQuery/Ajax/Angular/React frameworks; this V3 port covers only
    document.readyState so far. For stricter framework-aware idle semantics,
    inject a richer version of this helper at runtime without regenerating
    code.

    Args:
        driver: WebDriver instance
        timeout: Max seconds to wait (default 10, matches V2's 10s budget)

    Returns:
        True when readyState reports complete within timeout.

    Raises:
        selenium.common.exceptions.TimeoutException on timeout.
    """
    from selenium.webdriver.support.ui import WebDriverWait

    return WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState === 'complete'")
    )
