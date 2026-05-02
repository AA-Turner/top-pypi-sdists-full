from abc import ABC
from typing import Optional
from collections.abc import Callable
import asyncio
import random
import time
# BeautifulSoup:
from bs4 import BeautifulSoup
from lxml import html, etree
# Undetected Chrome Driver:
import undetected_chromedriver as uc
# WebDriver Support:
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
# Selenium:
from selenium import webdriver
# Selenium Proxy:
from selenium.webdriver import Proxy
# Chrome Support:
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
# Firefox Support:
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# Edge Support:
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
# Safari Support:
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.safari.service import Service as SafariService
# WebKitGTK Support:
from selenium.webdriver.webkitgtk.service import Service as WebKitGTKService
from selenium.webdriver.webkitgtk.options import Options as WebKitGTKOptions
# Selenium Options:
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)
from navconfig import BASE_DIR
from navconfig.logging import logging
from ...conf import (
    ### Oxylabs Proxy Support for Selenium
    OXYLABS_USERNAME,
    OXYLABS_PASSWORD,
    OXYLABS_ENDPOINT,
    GOOGLE_SEARCH_ENGINE_ID
)
from ...exceptions import (
    NotSupported,
    TimeOutError,
    ComponentError
)
from .options import (
    USER_AGENTS,
    MOBILE_USER_AGENTS,
    MOBILE_DEVICES,
    CHROME_OPTIONS,
    UNDETECTED_OPTIONS,
    FIREFOX_OPTIONS
)


logging.getLogger(name='selenium.webdriver').setLevel(logging.INFO)
logging.getLogger(name='WDM').setLevel(logging.WARNING)
logging.getLogger(name='hpack').setLevel(logging.WARNING)
logging.getLogger(name='seleniumwire').setLevel(logging.WARNING)
logging.getLogger(name='undetected_chromedriver').setLevel(logging.INFO)


class SeleniumService(ABC):
    """SeleniumService.

        Interface for making HTTP connections using Selenium.
    """
    accept: str = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"  # noqa

    def __init__(
        self,
        browser: str = 'chrome',
        headless: bool = True,
        mobile: bool = False,
        mobile_device: Optional[str] = None,
        browser_binary: Optional[str] = None,
        driver_binary: Optional[str] = None,
        user_data_dir: Optional[str] = None,
        timeout: int = 60,
        detach: bool = False,
        debugger_address: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize SeleniumService.

        Args:
            browser: Browser type to use ('chrome', 'firefox', 'edge', 'safari', 'undetected').
            headless: Run in headless mode.
            mobile: Enable mobile emulation.
            mobile_device: Specific mobile device to emulate.
            browser_binary: Path to browser executable.
            driver_binary: Path to driver executable.
            user_data_dir: Custom user data directory.
            timeout: Timeout for waits.
            detach: Keep browser open after script ends.
            debugger_address: Address to connect to an existing browser instance.
        """
        self._driver: Callable = None
        self._wait: WebDriverWait = None

        # Backwards compatibility for boolean flags
        self.use_firefox: bool = kwargs.get('use_firefox', False)
        self.use_edge: bool = kwargs.get('use_edge', False)
        self.use_safari: bool = kwargs.get('use_safari', False)
        self.use_webkit: bool = kwargs.get('use_webkit', False)
        self.use_undetected: bool = kwargs.get('use_undetected', False)
        self.as_mobile: bool = kwargs.get('as_mobile', False)
        self._logger = logging.getLogger("Flowtask.SeleniumService")
        # Determine browser from flags if not explicitly set to something other than default 'chrome'
        if self.use_firefox:
            self.browser = 'firefox'
        elif self.use_edge:
            self.browser = 'edge'
        elif self.use_safari:
            self.browser = 'safari'
        elif self.use_undetected:
            self.browser = 'undetected'
        elif self.use_webkit:
            self.browser = 'webkit'
        else:
            self.browser = browser

        # Set mobile mode based on boolean or argument
        self.mobile = mobile or self.as_mobile

        # Configuration
        self.headless = headless
        self.enable_http2: bool = kwargs.get('enable_http2', True)
        self._browser_binary = browser_binary or kwargs.get('browser_binary')
        self._driver_binary = driver_binary or kwargs.get('driver_binary')
        self._userdata = user_data_dir or kwargs.get('userdata')

        # Mobile Device
        self.mobile_device = mobile_device or kwargs.get('mobile_device', 'Pixel 2')
        if not self.mobile_device and self.mobile:
            self.mobile_device = random.choice(MOBILE_DEVICES)

        # Other internal options
        self.default_tag: str = kwargs.get('default_tag', 'body')
        self.accept_is_clickable: bool = kwargs.get('accept_is_clickable', False)
        self.timeout = timeout
        self.wait_until: tuple = kwargs.get('wait_until', None)
        self.inner_tag: tuple = kwargs.get('inner_tag', None)
        self.detach = detach
        self.debugger_address = debugger_address
        self.custom_user_agent = kwargs.get('custom_user_agent')
        self.disable_images = kwargs.get('disable_images', False)
        self.disable_javascript = kwargs.get('disable_javascript', False)
        self.disable_images = kwargs.get('disable_images', False)
        self.disable_javascript = kwargs.get('disable_javascript', False)
        self.auto_install = kwargs.get('auto_install', True)
        self.cache_valid_range = kwargs.get('cache_valid_range', 7)
        self.prefs = kwargs.get('prefs', {})

        # Accept Cookies
        self.accept_cookies: tuple = kwargs.get('accept_cookies', None)
        if hasattr(self, 'screenshot'):
            # Handle screenshot config if it exists on subclass/mixin
            pass

        self._options = None

        # Proxy configuration
        self.use_proxy: bool = kwargs.get('use_proxy', False)
        self.proxy_type: str = kwargs.get('proxy_type', 'decodo')
        self._free_proxy: bool = kwargs.get('free_proxy', False)

        super().__init__()

        headers = kwargs.get('headers', {})
        self.headers: dict = {
            "Accept": self.accept,
            "TE": "trailers",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self._get_user_agent(),
            **headers
        }

        # Configure Cookies:
        self.cookies: dict = kwargs.get('cookies', {})
        if isinstance(self.cookies, str):
            self.cookies = self.parse_cookies(self.cookies)

    async def __aenter__(self):
        """Async context manager entry."""
        return await self.get_driver()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._driver:
            try:
                # quit() is sync in selenium 4 but standard drivers.
                # For undetected-chromedriver it might also be sync.
                # However, if we want to be safe we can run it in a thread
                # or just call it if it's fast.
                # UC quit() involves file I/O for cleanup.
                await asyncio.to_thread(self._driver.quit)
            except Exception as e:
                self._logger.warning(f"Error closing driver: {e}")
            finally:
                self._driver = None

    def _get_user_agent(self) -> str:
        """Get appropriate user agent based on mobile/desktop mode."""
        if self.custom_user_agent:
            return self.custom_user_agent
        if self.mobile:
            return random.choice(MOBILE_USER_AGENTS)
        else:
            return random.choice(USER_AGENTS)

    def _setup_chrome_options(self) -> ChromeOptions:
        """Setup Chrome options."""
        options = ChromeOptions()

        for option in CHROME_OPTIONS:
            try:
                options.add_argument(option)
            except Exception:
                pass

        if self.headless:
            options.add_argument("--headless=new")

        if self._browser_binary:
            options.binary_location = self._browser_binary

        if self._userdata:
            options.add_argument(f"--user-data-dir={self._userdata}")

        if self.detach:
            options.add_experimental_option("detach", True)

        if self.debugger_address:
            options.debugger_address = self.debugger_address

        # Mobile emulation
        if self.mobile:
            if not self.mobile_device:
                self.mobile_device = random.choice(MOBILE_DEVICES)

            mobile_emulation = {
                "deviceName": self.mobile_device,
                "userAgent": self._get_user_agent()
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)
            self._logger.debug(f"Running in mobile emulation mode as {self.mobile_device}")
        else:
            # Regular user agent
            options.add_argument(f"user-agent={self._get_user_agent()}")

        # HTTP/2
        if not self.enable_http2:
            self.prefs["disable-http2"] = True

        # Disable images
        if self.disable_images:
            self.prefs["profile.managed_default_content_settings.images"] = 2

        if self.prefs:
            options.add_experimental_option("prefs", self.prefs)

        return options

    def _setup_undetected_chrome_options(self):
        """Setup Undetected Chrome options."""
        options = uc.ChromeOptions()

        for option in UNDETECTED_OPTIONS:
            try:
                options.add_argument(option)
            except Exception:
                pass

        # User agent
        options.add_argument(f"--user-agent={self._get_user_agent()}")

        if self.headless:
            options.headless = True

        if self._browser_binary:
            options.binary_location = self._browser_binary

        if self.prefs:
            options.add_experimental_option("prefs", self.prefs)

        return options

    def _setup_firefox_options(self) -> FirefoxOptions:
        """Setup Firefox options."""
        options = FirefoxOptions()

        for option in FIREFOX_OPTIONS:
            options.add_argument(option)

        if self.headless:
            options.add_argument("--headless")

        # User agent
        options.set_preference("general.useragent.override", self._get_user_agent())

        options.set_preference("network.http.http2.enabled", self.enable_http2)

        if self.disable_images:
            options.set_preference("permissions.default.image", 2)

        if self.disable_javascript:
            options.set_preference("javascript.enabled", False)

        if self._browser_binary:
            options.binary_location = self._browser_binary

        return options

    def _setup_edge_options(self) -> EdgeOptions:
        """Setup Edge options."""
        options = EdgeOptions()

        # Edge uses Chrome options usually
        for option in CHROME_OPTIONS:
            options.add_argument(option)

        if self.headless:
            options.add_argument("--headless=new")

        options.add_argument(f"user-agent={self._get_user_agent()}")

        if self._browser_binary:
            options.binary_location = self._browser_binary

        options.add_experimental_option("ms:edgeOptions", {"http2": self.enable_http2})

        return options

    def _setup_safari_options(self) -> SafariOptions:
        """Setup Safari options."""
        options = SafariOptions()
        # Safari has limited options through this interface
        return options

    def _setup_webkit_options(self) -> WebKitGTKOptions:
        """Setup WebKitGTK options."""
        options = WebKitGTKOptions()
        return options

    async def _get_service(self, browser_type: str):
        """Get appropriate WebDriver service."""
        if self._driver_binary:
            # Use custom driver binary
            if browser_type == 'chrome':
                return ChromeService(executable_path=self._driver_binary)
            elif browser_type == 'firefox':
                return FirefoxService(executable_path=self._driver_binary)
            elif browser_type == 'edge':
                return EdgeService(executable_path=self._driver_binary)
            elif browser_type == 'safari':
                return SafariService(executable_path=self._driver_binary)

        if not self.auto_install:
            # Use system driver
            if browser_type == 'chrome':
                return ChromeService()
            elif browser_type == 'firefox':
                return FirefoxService()
            elif browser_type == 'edge':
                return EdgeService()
            elif browser_type == 'safari':
                return SafariService()

        # Auto-install using DriverManager
        cache_manager = DriverCacheManager(valid_range=self.cache_valid_range)

        if browser_type == 'chrome':
            driver_path = ChromeDriverManager(cache_manager=cache_manager).install()
            return ChromeService(executable_path=driver_path)
        elif browser_type == 'firefox':
            driver_path = GeckoDriverManager(cache_manager=cache_manager).install()
            return FirefoxService(executable_path=driver_path)
        elif browser_type == 'edge':
            driver_path = EdgeChromiumDriverManager(cache_manager=cache_manager).install()
            return EdgeService(executable_path=driver_path)
        elif browser_type == 'safari':
            return SafariService()
        elif browser_type == 'webkit':
            return WebKitGTKService().install()

        return None

    async def _configure_proxy(self, options, browser_type: str):
        """Configure Proxy for the options."""
        proxy = None
        proxies = None

        if not self.use_proxy:
            return options

        proxy = Proxy()
        if self._free_proxy is False:
            # Use commercial proxies (Oxylabs, Decodo, etc.)
            from proxylists.proxies import Decodo, Oxylabs, Geonode

            proxy_list = None
            if self.proxy_type == 'decodo':
                proxy_list = await Decodo().get_list()
            elif self.proxy_type == 'oxylabs':
                proxy_list = await Oxylabs(session_time=0.4, timeout=10).get_list()
            elif self.proxy_type == 'geonode':
                proxy_list = await Geonode().get_list()
            else:
                # Default
                proxy_list = await Decodo().get_list()

            if proxy_list:
                selected_proxy = proxy_list[0] if isinstance(proxy_list, list) else proxy_list

                # Parse proxy
                user = password = ""
                endpoint = selected_proxy
                if '@' in selected_proxy:
                    auth, endpoint = selected_proxy.split('@', 1)
                    if ':' in auth:
                        user, password = auth.split(':', 1)

                # Set proxy capability/arguments
                if browser_type == 'chrome':
                    options.add_argument(f"--proxy-server=http://{endpoint}")
                    # Note: Authenticated proxy on Chrome often requires extensions or other tricks
                    # simple --proxy-server works for IP auth or if we use wire.
                elif browser_type == 'firefox':
                    # Firefox allows manual proxy config more easily
                    # Logic for Oxylabs from original code:
                    if self.proxy_type == 'oxylabs':
                        customer = f"customer-{OXYLABS_USERNAME}-sesstime-1"
                        proxy_config = {
                            "proxyType": "manual",
                            "httpProxy": f"{customer}:{OXYLABS_PASSWORD}@{OXYLABS_ENDPOINT}",
                            "sslProxy": f"{customer}:{OXYLABS_PASSWORD}@{OXYLABS_ENDPOINT}",
                        }
                        options.set_preference("network.proxy.type", 1)
                        options.set_preference("network.proxy.http", OXYLABS_ENDPOINT.split(':')[0])
                        options.set_preference("network.proxy.http_port", int(OXYLABS_ENDPOINT.split(':')[1]))
                    else:
                        # Basic proxy
                        proxy.http_proxy = f"http://{selected_proxy}"
                        proxy.ssl_proxy = f"https://{selected_proxy}"
                        options.set_capability("proxy", proxy)

                self._logger.notice(f'[SeleniumService] Using {self.proxy_type.upper()} proxy: {endpoint}')

        else:
            # Free Proxy
            proxies = await self.get_proxies()
            if proxies:
                proxy_url = proxies[0]
                proxy.http_proxy = f"http://{proxy_url}"
                proxy.ssl_proxy = f"https://{proxy_url}"

                if browser_type == 'chrome':
                    options.add_argument(f"--proxy-server={proxy.http_proxy}")
                else:
                    options.set_capability("proxy", proxy)

                self._logger.notice(f'[SeleniumService] Using FREE proxy: {proxy_url}')

        return options

    async def get_driver(self):
        """
        Return a Selenium Driver instance for configured browser.
        """
        self._webdriver = webdriver

        try:
            if self.browser == 'undetected':
                self._options = self._setup_undetected_chrome_options()
                # Proxy setup for undetected chrome might need special handling, keeping it simple or reusing existing
                self._options = await self._configure_proxy(self._options, 'chrome')

                driver_path = None
                if self._driver_binary:
                    driver_path = self._driver_binary
                elif self.auto_install:
                    driver_path = ChromeDriverManager().install()

                self._driver = uc.Chrome(
                    options=self._options,
                    headless=self.headless,
                    use_subprocess=False,
                    advanced_elements=True,
                    enable_cdp_events=True,
                    driver_executable_path=driver_path,
                    browser_executable_path=self._browser_binary,
                )

            elif self.browser == 'firefox':
                self._options = self._setup_firefox_options()
                self._options = await self._configure_proxy(self._options, 'firefox')

                service = await self._get_service('firefox')
                self._driver = self._webdriver.Firefox(
                    service=service,
                    options=self._options
                )

            elif self.browser == 'edge':
                self._options = self._setup_edge_options()
                # Proxy for edge
                self._options = await self._configure_proxy(self._options, 'edge')

                service = await self._get_service('edge')
                self._driver = self._webdriver.Edge(
                    service=service,
                    options=self._options
                )

            elif self.browser == 'safari':
                self._options = self._setup_safari_options()
                service = await self._get_service('safari')
                self._driver = self._webdriver.Safari(
                    service=service,
                    options=self._options
                )

            elif self.browser == 'webkit':
                self._options = self._setup_webkit_options()
                service = await self._get_service('webkit')
                self._driver = self._webdriver.WebKitGTK(
                    service=service,
                    options=self._options
                )

            else:
                # Default to Chrome
                self._options = self._setup_chrome_options()
                self._options = await self._configure_proxy(self._options, 'chrome')

                service = await self._get_service('chrome')
                self._driver = self._webdriver.Chrome(
                    service=service,
                    options=self._options
                )

            # Create WebDriverWait
            self._wait = WebDriverWait(self._driver, self.timeout)
            return self._driver

        except Exception as e:
            self._logger.error(f"Failed to initialize {self.browser} driver: {e}")
            raise ComponentError(f"Driver initialization failed: {e}") from e

    def _execute_scroll(self, scroll_pause_time=1.0, max_scrolls=5):
        """
        Execute a progressive scroll through the page to ensure dynamic content loads.

        Args:
            scroll_pause_time (float): Time to pause between scrolls
            max_scrolls (int): Maximum number of scroll operations
        """
        try:
            # Wait for the page to be loaded initially
            WebDriverWait(self._driver, 20).until(
                lambda driver: driver.execute_script("return document.body.scrollHeight") > 0
            )

            # Get initial scroll height
            last_height = self._driver.execute_script("return document.body.scrollHeight")

            # Progressive scrolling
            for scroll in range(max_scrolls):
                # Scroll down to bottom in steps
                self._driver.execute_script(f"window.scrollTo(0, {(scroll+1) * last_height/max_scrolls});")

                # Wait to load page
                time.sleep(scroll_pause_time)

                # Check if new elements have loaded after each partial scroll
                new_height = self._driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height and scroll > 0:
                    # If no new content loaded after first scroll, break
                    break

                last_height = new_height

                # If this is the last scroll, try to wait for any AJAX to complete
                if scroll == max_scrolls - 1:
                    time.sleep(scroll_pause_time * 1.5)

            # Scroll back to top for better user interaction
            self._driver.execute_script("window.scrollTo(0, 0);")
        except Exception as e:
            # Log but don't fail completely on scroll errors
            self._logger.warning(f"Error during scroll operation: {e}")

    def save_screenshot(self, filename: str) -> None:
        """Saving and Screenshot of entire Page."""
        original_size = self._driver.get_window_size()
        width = self._driver.execute_script(
            'return document.body.parentNode.scrollWidth'
        ) or 1920
        height = self._driver.execute_script(
            'return document.body.parentNode.scrollHeight'
        ) or 1080
        if not width:
            width = 1920
        if not height:
            height = 1080
        self._driver.set_window_size(width, height)
        self._execute_scroll()

        # Ensure the page is fully loaded after resizing
        self._wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        # Wait for specific elements to load
        if self.wait_until:
            WebDriverWait(self._driver, 20).until(
                EC.presence_of_all_elements_located(
                    self.wait_until
                )
            )
        if 'portion' in self.screenshot:
            element = self._driver.find_element(*self.screenshot['portion'])
            # Check if the element has a size
            size = element.size
            if size['height'] == 0 or size['width'] == 0:
                # Try scrolling or waiting until element is visible
                self.logger.warning(
                    "Element to screenshot has zero dimension, waiting for it to render..."
                )
                WebDriverWait(self._driver, 20).until(
                    lambda driver: element.size['height'] > 0 and element.size['width'] > 0
                )
            element.screenshot(filename)
        else:
            # Take a full-page screenshot
            self._driver.save_screenshot(filename)
        # resize to the Original Size:
        self._driver.set_window_size(
            original_size['width'],
            original_size['height']
        )

    def get_soup(self, content: str, parser: str = 'html.parser'):
        """Get a BeautifulSoup Object."""
        return BeautifulSoup(content, parser)

    def get_etree(self, content: str) -> tuple:
        try:
            x = etree.fromstring(content)
        except etree.XMLSyntaxError:
            x = None
        try:
            h = html.fromstring(content)
        except etree.XMLSyntaxError:
            h = None
        return x, h

    async def selenium_authenticate(
        self,
        url: str,
        username: str,
        password: str,
        username_selector: str = 'input[type="text"], input[type="email"], input[name="username"]',
        password_selector: str = 'input[type="password"], input[name="password"]',
        submit_selector: str = 'button[type="submit"], input[type="submit"]',
        enter_on_username: bool = False,
        wait_after_submit: int = 3,
        timeout: int = 10
    ) -> bool:
        """
        Authenticate using form-based login with Selenium.

        Args:
            url: Login page URL
            username: Username or email
            password: Password
            username_selector: CSS selector for username field
            password_selector: CSS selector for password field
            submit_selector: CSS selector for submit button
            enter_on_username: Press Enter after username (for multi-step logins)
            wait_after_submit: Seconds to wait after submitting
            timeout: Timeout for finding elements

        Returns:
            bool: True if authentication successful
        """
        try:
            if not self._driver:
                await self.get_driver()

            # Navigate to login page
            self._driver.get(url)

            # Wait for page to load
            self._wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )

            # Find and fill username
            username_element = WebDriverWait(self._driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, username_selector))
            )
            username_element.clear()
            username_element.send_keys(username)

            if enter_on_username:
                from selenium.webdriver.common.keys import Keys
                username_element.send_keys(Keys.ENTER)
                time.sleep(1)

            # Find and fill password
            password_element = WebDriverWait(self._driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, password_selector))
            )
            password_element.clear()
            password_element.send_keys(password)

            # Click submit button
            submit_button = WebDriverWait(self._driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, submit_selector))
            )
            submit_button.click()

            # Wait for navigation/login completion
            time.sleep(wait_after_submit)

            self._logger.info("Authentication completed successfully")
            return True

        except Exception as e:
            self._logger.error(f"Authentication failed: {str(e)}")
            raise ComponentError(f"Selenium authentication failed: {e}") from e

    async def extract_cookies(self, domain: str = None) -> dict:
        """
        Extract cookies from current Selenium session.

        Args:
            domain: Optional domain filter

        Returns:
            dict: Cookies as {name: value} dictionary
        """
        try:
            if not self._driver:
                raise ComponentError("Driver not initialized. Call get_driver() first.")

            cookies = self._driver.get_cookies()

            # Filter by domain if specified
            if domain:
                cookies = [c for c in cookies if domain in c.get('domain', '')]

            # Convert to simple dict
            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}

            self._logger.info(f"Extracted {len(cookie_dict)} cookies")
            return cookie_dict

        except Exception as e:
            self._logger.error(f"Failed to extract cookies: {str(e)}")
            raise ComponentError(f"Cookie extraction failed: {e}") from e

    async def set_selenium_cookies(self, cookies: dict, domain: str = None) -> bool:
        """
        Set cookies in Selenium session.

        Args:
            cookies: Dictionary of cookies {name: value}
            domain: Optional domain for cookies

        Returns:
            bool: True if successful
        """
        try:
            if not self._driver:
                raise ComponentError("Driver not initialized. Call get_driver() first.")

            for name, value in cookies.items():
                cookie_dict = {
                    'name': name,
                    'value': value
                }
                if domain:
                    cookie_dict['domain'] = domain

                self._driver.add_cookie(cookie_dict)

            self._logger.info(f"Set {len(cookies)} cookies in Selenium session")
            return True

        except Exception as e:
            self._logger.error(f"Failed to set cookies: {str(e)}")
            return False

    async def get_page(
        self,
        url: str,
        cookies: Optional[dict] = None,
        retries: int = 3,
        backoff_delay: int = 2
    ):
        """get_page with selenium.

        Get one page using Selenium.
        """
        if not self._driver:
            await self.get_driver()
        attempt = 0
        # Debug for using Proxy:
        # self._driver.get('https://api.ipify.org?format=json')
        # page_source = self._driver.page_source
        # print(page_source)
        while attempt < retries:
            try:
                try:
                    self._driver.delete_all_cookies()
                except Exception:
                    pass
                self._driver.get(url)
                if cookies:
                    # Add the cookies
                    for cookie_name, cookie_value in cookies.items():
                        if cookie_value:
                            self._driver.add_cookie({'name': cookie_name, 'value': cookie_value})
                        # Refresh the page to apply the cookies
                        self._driver.refresh()

                # Ensure the page is fully loaded before attempting to click
                self._wait.until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )

                # Wait for specific elements to load (replace with your actual elements)
                if self.wait_until:
                    WebDriverWait(self._driver, 20).until(
                        EC.presence_of_all_elements_located(
                            self.wait_until
                        )
                    )
                else:
                    # Wait for the tag to appear in the page.
                    self._wait.until(
                        EC.presence_of_element_located(
                            (By.TAG_NAME, self.default_tag)
                        )
                    )
                # Accept Cookies if enabled.
                if self.accept_cookies:
                    # Wait for the button to appear and click it.
                    try:
                        # Wait for the "Ok" button to be clickable and then click it
                        if self.accept_is_clickable is True:
                            accept_button = self._wait.until(
                                EC.element_to_be_clickable(self.accept_cookies)
                            )
                            accept_button.click()
                        else:
                            accept_button = self._wait.until(
                                EC.presence_of_element_located(
                                    self.accept_cookies
                                )
                            )
                        self._driver.execute_script("arguments[0].click();", accept_button)
                    except TimeoutException:
                        self._logger.warning(
                            'Accept Cookies Button not found'
                        )
                # Execute an scroll of the page:
                self._execute_scroll()
                return
            except TimeoutException:
                # The page never reached complete.
                print("Page did not reach a complete readyState.")
                print("Current Page Source:")
                print('===========================')
                print(self._driver.page_source)
                print('===========================')
                # Challenge Button:
                # Try to detect the challenge element. For example, if the button has text "Pulsar y mantener pulsado"

                wait = WebDriverWait(self._driver, 20)
                base = wait.until(EC.presence_of_element_located((By.ID, "px-captcha")))
                iframe = base.find_element(By.TAG_NAME, "iframe")
                print('IFRAME > ', iframe)
                self._driver.switch_to.frame(iframe)
                challenge_button = self._driver.find_element(
                    By.XPATH, "//p[contains(text(), 'Pulsar y mantener pulsado')]"
                )
                print('BUTTON HERE > ', challenge_button)

                try:
                    challenge_button = WebDriverWait(self._driver, 5).until(
                        EC.presence_of_element_located(challenge_button)
                    )
                    print('BUTTON HERE > ', challenge_button)
                    # If we found the button, simulate the click and hold action
                    actions = ActionChains(self._driver)
                    # Hold the button for, say, 5 seconds
                    actions.click_and_hold(challenge_button).pause(5).release().perform()
                    self._driver.switch_to.default_content()
                    # Optionally wait again for the page to load after the challenge
                    self._wait.until(
                        lambda driver: driver.execute_script("return document.readyState") == "complete"
                    )
                    # Execute an scroll of the page:
                    self._execute_scroll()
                    return
                except TimeoutException:
                    # If the challenge button isn't present, continue as normal
                    pass
                attempt += 1
                if attempt < retries:
                    self._logger.warning(
                        f"TimeoutException occurred. Retrying ({attempt}/{retries}) in {backoff_delay}s..."
                    )
                    time.sleep(backoff_delay)
                else:
                    raise TimeOutError(f"Timeout Error on URL {self.url} after {retries} attempts")
            except Exception as exc:
                raise ComponentError(
                    f"Error running Scrapping Tool: {exc}"
                )

    async def search_google_cse(self, query: str, max_results: int = 5):
        """
        Search Google Custom Search Engine (CSE) using Selenium.

        Args:
            query (str): The search query.
            max_results (int, optional): Maximum number of search results to return.

        Returns:
            list[dict]: A list of search results with 'title' and 'link'.
        """
        try:
            search_url = f"https://cse.google.com/cse?cx={GOOGLE_SEARCH_ENGINE_ID}#gsc.tab=0&gsc.q={query}&gsc.sort="
            driver = await self.get_driver()
            driver.get(search_url)

            # ✅ Wait for search results or "No results" message
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "gsc-results"))
                )
            except TimeoutException:
                try:
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "gs-no-results-result"))
                    )
                    return []  # No results found, return an empty list
                except TimeoutException:
                    raise RuntimeError("CSE: No results found or page failed to load.")

            time.sleep(2)  # Allow JS to finalize

            # ✅ Extract search results
            results = []
            try:
                search_results = driver.find_elements(By.CLASS_NAME, "gsc-webResult")
            except NoSuchElementException:
                search_results = driver.find_elements(By.CLASS_NAME, "gsc-expansionArea")

            for result in search_results[:max_results]:
                try:
                    title_element = result.find_element(By.CLASS_NAME, "gs-title")
                    url_element = title_element.find_element(By.TAG_NAME, "a") if title_element else None

                    if title_element and url_element:
                        title = title_element.text.strip()
                        url = url_element.get_attribute("href").strip()
                        if title and url:
                            results.append({"title": title, "link": url})

                except NoSuchElementException:
                    continue  # Skip missing results

            return results

        except NoSuchElementException as e:
            raise RuntimeError(f"CSE Error: Element not found ({e})")
        except TimeoutException as e:
            raise RuntimeError(f"CSE Timeout: {e}")
        except WebDriverException as e:
            raise RuntimeError(f"CSE WebDriver Error: {e}")
        except RuntimeError as e:
            if str(e) == "CSE: No results found or page failed to load.":
                return []
            raise RuntimeError(f"CSE Runtime Error: {e}")
        except Exception as e:
            raise RuntimeError(f"CSE Unexpected Error: {e}")
        finally:
            self.close_driver()  # Always close driver
