from typing import Any
import asyncio
from collections.abc import Callable
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import random
import httpx
import pandas as pd
import backoff
import os
from pathlib import Path
# Selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
# Internals
from ..exceptions import (
    ComponentError,
    DataNotFound,
    DataError
)
from ..interfaces.http import ua
from .reviewscrap import ReviewScrapper, on_backoff, bad_gateway_exception
from ..utils.json import json_decoder, json_encoder


class NetworkNinjaClaims(ReviewScrapper):
    """
    NetworkNinja Claims Component

    **Overview**

    This component extracts claims data from NetworkNinja.com using automated browser authentication.
    It uses Selenium to perform login and dynamically extract session cookies, then uses HTTP requests
    to fetch claims data from the API. Supports persistent browser sessions to avoid re-authentication.

    The component handles the two-step SSO login process:
    1. Enter username and click "Continue to Site"
    2. Enter password and submit the form

    It automatically manages session cookies and can reuse authenticated sessions across multiple runs.

       :widths: auto

    |   nn_username              | Yes      | NetworkNinja username/email for authentication. Can be provided via environment variables.   |
    |                            |          | Example: `trocadvrpt@trocglobal.com`                                                         |
    |   nn_password              | Yes      | NetworkNinja password for authentication. Should be provided via environment variables.      |
    |                            |          | For security, never hardcode credentials in YAML files.                                      |
    |   use_persistent_session   | No       | Whether to use persistent browser profile for SSO sessions. Default: `true`.                |
    |                            |          | When enabled, saves browser profile to avoid re-login on subsequent runs.                    |
    |   headless                 | No       | Whether to run browser in headless mode. Default: `false`.                                  |
    |                            |          | Set to `false` for debugging or first-time setup.                                           |
    |   use_proxy                | No       | Whether to use proxy for requests. Default: `true`.                                         |
    |                            |          | Uses the configured proxy type (decodo, oxylabs, geonode).                                  |
    |   proxy_type               | No       | Type of proxy to use. Options: `decodo`, `oxylabs`, `geonode`. Default: `decodo`.           |

    **Returns**

    This component returns a pandas DataFrame containing claims data from NetworkNinja.
    The DataFrame includes all available claim fields such as:

    - `c.id`: Claim ID
    - `c.claim_conflict`: Whether the claim has conflicts
    - `c.conflicting_claim_ids`: List of conflicting claim IDs
    - Additional claim details and metadata

    **Example YAML Configuration**

    Basic usage with environment variables:


    Advanced configuration with proxy:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          NetworkNinjaClaims:
          nn_username: NN_USERNAME
          nn_password: NN_PASSWORD
          use_persistent_session: true
          headless: false
        ```
    """
    _version = "1.0.0"

    # dict of expected credentials
    _credentials: dict = {
        "nn_username": str,
        "nn_password": str,
    }

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        # Network Ninja credentials - will be processed by processing_credentials()
        self.use_persistent_session: bool = kwargs.pop('use_persistent_session', True)
        self.headless: bool = kwargs.pop('headless', False)  # Default to visible for SSO
        self.type: str = kwargs.get('type', 'claims')
        kwargs['type'] = self.type

        # Configure user data directory for persistent sessions
        if self.use_persistent_session:
            userdata_dir = Path.home() / '.flowtask' / 'selenium_profiles' / 'networkninja'
            userdata_dir.mkdir(parents=True, exist_ok=True)
            kwargs['userdata'] = str(userdata_dir)

        super().__init__(
            loop=loop,
            job=job,
            stat=stat,
            headless=self.headless,
            **kwargs
        )
        # Always use proxies:
        self.use_proxy: bool = True
        self._free_proxy: bool = False

        # Cookies will be extracted dynamically from Selenium session
        # These are just fallback/default values
        self.cookies = {
            "PHPSESSID": "",
            "sid": "",
            "claims_page": "1",
            "claims_showFavorites": "false"
        }
        self.headers: dict = {
            'authority': 'networkninja.com',
            "Host": "flex.troc.networkninja.com",
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6",
            "content-language": "en-US",
            "Origin": "https://flex.troc.networkninja.com/",
            "Sec-CH-UA": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Linux"',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            "Sec-Fetch-Site": "none",
            "User-Agent": random.choice(ua),
            "Connection": "keep-alive",
            'dnt': '1',
            'upgrade-insecure-requests': '1',
        }
        self.semaphore = asyncio.Semaphore(10)
        self.login_url = "https://flex.troc.networkninja.com/"
        self.claims_url = "https://flex.troc.networkninja.com/payroll/claims.php"

    async def start(self, **kwargs):
        # Process credentials (replaces environment variables)
        self.processing_credentials()

        # Debug: Check what credentials we have
        self._logger.info(f"Credentials after processing: {self.credentials}")
        self._logger.info(f"nn_username: {self.credentials.get('nn_username')}")
        self._logger.info(f"nn_password: {'***' if self.credentials.get('nn_password') else 'None'}")

        return await super().start(**kwargs)

    async def login_and_extract_cookies(self) -> dict:
        """
        Login to NetworkNinja using Selenium and extract session cookies.

        Uses persistent browser profile to maintain SSO sessions.
        If already logged in (cookies exist), it will skip login.

        Returns:
            dict: Extracted cookies for use in HTTP requests
        """
        try:
            # Initialize Selenium driver if not already done
            if not self._driver:
                await self.get_driver()

            self._logger.info("Navigating to NetworkNinja login page...")

            # Navigate to the main page
            self._driver.get(self.login_url)

            # Wait for page to load
            await asyncio.sleep(2)

            # Check if already logged in by looking for logout button or dashboard elements
            current_url = self._driver.current_url
            self._logger.info(f"Current URL after navigation: {current_url}")

            # Check if we're already logged in (URL changed to dashboard or claims page)
            if 'login' not in current_url.lower() and 'signin' not in current_url.lower():
                self._logger.info("Already logged in via persistent session!")
            else:
                # Need to login
                if not self.credentials.get('nn_username') or not self.credentials.get('nn_password'):
                    raise ComponentError(
                        "NetworkNinja credentials required. Pass nn_username and nn_password."
                    )

                self._logger.info("Attempting login (two-step process)...")

                # NetworkNinja uses a two-step login process:
                # Step 1: Enter username and click "Continue to Site"
                # Step 2: Enter password and submit

                # Step 1: Enter username
                self._logger.info("Step 1: Entering username...")

                username_field = WebDriverWait(self._driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"], input[type="email"], input[name="username"]'))
                )
                username_field.clear()
                username_field.send_keys(self.credentials.get('nn_username'))

                # Click "Continue to Site" button
                self._logger.info("Clicking 'Continue to Site' button...")
                continue_button = WebDriverWait(self._driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"], button.btn-primary, input[type="submit"]'))
                )
                continue_button.click()

                # Wait for password field to appear
                await asyncio.sleep(2)

                # Step 2: Enter password
                self._logger.info("Step 2: Entering password...")
                password_field = WebDriverWait(self._driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"], input[name="password"]'))
                )
                password_field.clear()
                password_field.send_keys(self.credentials.get('nn_password'))

                # Submit password form - SSO uses a span with id="submitButton"
                self._logger.info("Clicking Sign in button...")
                submit_button = WebDriverWait(self._driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'submitButton'))
                )
                submit_button.click()

                # Wait for login to complete
                self._logger.info("Waiting for login to complete...")
                await asyncio.sleep(5)

            # Navigate to claims page to ensure we're in the right context
            self._logger.info("Navigating to claims page...")
            self._driver.get(self.claims_url)
            await asyncio.sleep(2)

            # Extract cookies from Selenium session
            cookies = await self.extract_cookies(domain='networkninja.com')

            self._logger.info(f"Successfully extracted {len(cookies)} cookies")

            # Update instance cookies
            self.cookies.update(cookies)

            # Close driver to free resources (session persists via user-data-dir)
            self.close_driver()

            return cookies

        except Exception as e:
            self._logger.error(f"Login and cookie extraction failed: {e}")
            # Close driver on error
            try:
                self.close_driver()
            except:
                pass
            raise ComponentError(f"Failed to login to NetworkNinja: {e}") from e

    async def ensure_authenticated(self) -> dict:
        """
        Ensure we have valid session cookies.

        Returns cookies either from cache or by performing login.

        Returns:
            dict: Session cookies
        """
        # Check if we have valid cookies (PHPSESSID and sid are required)
        if self.cookies.get('PHPSESSID') and self.cookies.get('sid'):
            self._logger.info("Using existing session cookies")
            return self.cookies

        # No valid cookies, perform login
        self._logger.info("No valid cookies found, performing login...")
        return await self.login_and_extract_cookies()

    @backoff.on_exception(
        backoff.expo,
        (httpx.TimeoutException, httpx.ConnectTimeout, httpx.HTTPStatusError, httpx.HTTPError),
        max_tries=3,
        jitter=backoff.full_jitter,
        on_backoff=on_backoff,
        giveup=lambda e: not bad_gateway_exception(e) and not isinstance(e, httpx.ConnectTimeout)
    )
    async def _fetch_claims(self, cookies) -> list:
        async with self.semaphore:
            # Prepare payload for the API request
            base_url = "https://flex.troc.networkninja.com/payroll/claims.php"
            result = []
            total_records = 0
            page = 1
            try:
                while True:
                    json_data, error = await self.session(
                        url=base_url,
                        method='post',
                        headers=self.headers,
                        follow_redirects=True,
                        use_json=True,
                        data={
                            "xhr": True,
                            "loadCount": 1,
                            "page": page,
                            "perPage": 100,
                            "orderBy": "",
                            "orderDirection": "",
                            "search": "",
                            "saveFilter": False,
                            "showFavorites": False,
                            "selectedItems": [],
                            "currentColumns": [],
                            "checkAll": False,
                            "columnState": []
                        },
                        cookies=cookies
                    )
                    print('fetched page ', page)
                    if not error:
                        data = json_decoder(json_data)
                        total_records = int(data.get('total_records', 0))
                        result.extend(data.get('data', []))
                        print('fetched records ', len(result), ' of ', total_records)
                        if len(result) >= total_records:
                            break
                        page += 1
                        await asyncio.sleep(
                            random.uniform(1, 3)
                        )  # Be polite with a random delay
                # Convert result to DataFrame
                if result:
                    df = pd.DataFrame(result)
                    print(df)
                    return df
                else:
                    raise DataNotFound("No claims data found.")
            except Exception as e:
                print('error fetching claims ', e)
                raise ComponentError(
                    f"An error occurred: {e}"
                ) from e

    async def claims(self):
        """claims.

        NetworkNinja Claims Data.

        This method ensures authentication before fetching claims data.
        It will automatically login using Selenium if needed and extract session cookies.
        """
        # Ensure we have valid session cookies
        self._logger.info("Ensuring authentication...")
        cookies = await self.ensure_authenticated()

        # Convert cookies to httpx format
        httpx_cookies = httpx.Cookies()
        for key, value in cookies.items():
            if key == "PHPSESSID":
                httpx_cookies.set(
                    key, value,
                    domain='.troc.networkninja.com',
                    path='/'
                )
            else:
                httpx_cookies.set(
                    key, value,
                    domain='.flex.troc.networkninja.com',
                    path='/'
                )

        # Iterate over each row in the DataFrame
        self._logger.info('Starting claims data fetch...')
        result = await self._fetch_claims(
            httpx_cookies
        )
        self._result = result
        return self._result
