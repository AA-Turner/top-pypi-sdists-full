import time
from datetime import timedelta, datetime, timezone
from typing import Tuple

import boto3
import pyotp


class Okta:
    def __init__(self, **kwargs):
        self.previous_otp = None
        self.__okta_username = kwargs.get("username")
        self.__okta_password = kwargs.get("password")
        self.__okta_totp = kwargs.get("totp")
        self.__client_name = kwargs.get("client_name")
        self.__role_name = kwargs.get("role_name")
        self.__account_id = kwargs.get("account_id")
        self.__client_type = kwargs.get("client_type")
        self.__service_name = kwargs.get("service_name")
        self.__region_name = kwargs.get("region_name")
        self.__start_url = kwargs.get("start_url")

    def get_aws_session(self) -> Tuple[boto3.Session, datetime]:
        session = boto3.Session()
        sso_client = session.client(
            self.__service_name,
            region_name=self.__region_name,
        )

        register_response = sso_client.register_client(clientName=self.__client_name, clientType=self.__client_type)

        sso_device_auth_response = sso_client.start_device_authorization(
            clientId=register_response["clientId"],
            clientSecret=register_response["clientSecret"],
            startUrl=self.__start_url,
        )

        self.__okta_auth(sso_device_auth_response["verificationUriComplete"])
        token_response = sso_client.create_token(
            grantType="urn:ietf:params:oauth:grant-type:device_code",
            clientId=register_response["clientId"],
            clientSecret=register_response["clientSecret"],
            deviceCode=sso_device_auth_response["deviceCode"],
        )

        sso = session.client("sso", region_name=self.__region_name)
        account_roles = sso.list_account_roles(accessToken=token_response["accessToken"], accountId=self.__account_id)
        roles = account_roles["roleList"]
        result = [role for role in roles if role["roleName"].__contains__(self.__role_name)]
        if len(result) == 0:
            role = roles[0]
        else:
            role = result[0]
        role_creds = sso.get_role_credentials(
            roleName=role["roleName"],
            accountId=role["accountId"],
            accessToken=token_response["accessToken"],
        )

        session = boto3.Session(
            region_name=self.__region_name,
            aws_access_key_id=role_creds["roleCredentials"]["accessKeyId"],
            aws_secret_access_key=role_creds["roleCredentials"]["secretAccessKey"],
            aws_session_token=role_creds["roleCredentials"]["sessionToken"],
        )
        expiration_time = datetime.fromtimestamp(role_creds["roleCredentials"]["expiration"] / 1000, tz=timezone.utc)
        return session, expiration_time

    @staticmethod
    def __wait_until_one_of_elements_visible(browser, locators: Tuple[str], timeout: int = 10) -> str:
        """Waits until one of the locators becomes visible on the page within the timeout.

        Args:
            locators (Tuple[str]): A tuple of element locators to check for visibility.
            timeout (int): The maximum time to wait for an element to become visible, in seconds.

        Returns:
            str: The locator of the first visible element.

        """
        timeout = datetime.now() + timedelta(seconds=timeout)
        while datetime.now() <= timeout:
            for locator in locators:
                if browser.is_element_visible(locator):
                    return locator
            time.sleep(0.5)
        raise AssertionError(f"None of the locators {locators} became visible within {timeout}s timeout.")

    def __okta_auth(self, verification_url):
        try:
            from RPA.Browser.Selenium import Selenium
        except ImportError:
            raise ImportError("Rpaframework is not installed. Please install it via pip")

        selenium_wait_time = 30
        browser = Selenium()
        browser.open_available_browser(url=verification_url, headless=True)
        try:
            browser.wait_until_element_is_visible(
                '//button[text() ="Confirm and continue"]', timedelta(seconds=selenium_wait_time)
            )
            browser.click_element('xpath://button[text() ="Confirm and continue"]')
            username_id = "//input[@autocomplete='username']"
            browser.wait_until_element_is_enabled(username_id, timedelta(seconds=selenium_wait_time + 15))
            current_username = browser.get_text(username_id)
            username = str(self.__okta_username).split("@")[0]
            if current_username != username:
                browser.input_text(username_id, username)

            browser.click_button("//input[@value='Next']")
            password_input = "//input[@type='password']"

            browser.wait_until_element_is_visible(password_input, timedelta(seconds=selenium_wait_time))
            if not self.__okta_password:
                raise ValueError("Password is required for Okta, please provide it in arguments.")
            browser.input_text(password_input, self.__okta_password)
            browser.click_button("//input[@type='submit']")

            totp = pyotp.TOTP(self.__okta_totp)
            button_allow = '//button/*[text()="Allow"]'
            for tries in range(4):
                while self.previous_otp == totp.now():
                    time.sleep(1)
                    continue

                self.previous_otp = totp.now()
                time.sleep(3)
                answer_input = "//input[@name='credentials.passcode']"
                browser.input_text(answer_input, totp.now())
                browser.click_button("//input[@type='submit']")
                try:
                    browser.wait_until_element_is_visible(button_allow, timeout=timedelta(seconds=selenium_wait_time))
                    break
                except AssertionError:
                    if tries == 3:
                        raise
                    otp_error_box = "//div[contains(@class, 'o-form-has-errors')]"
                    if browser.find_elements(otp_error_box):
                        continue
                    raise

            browser.click_element(button_allow)
            browser.wait_until_element_is_visible(
                "//*[contains(text(),'Request approved')]", timeout=timedelta(seconds=selenium_wait_time)
            )
        except Exception as e:
            raise Exception(f"Error during Okta authentication: {e}")
        finally:
            browser.close_browser()
