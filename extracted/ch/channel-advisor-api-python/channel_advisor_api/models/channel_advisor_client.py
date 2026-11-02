import requests
import base64
import json
import os
import time
from typing import List
from urllib.parse import parse_qs, urlencode, urlparse
from channel_advisor_api.utils.logger import get_logger

logger = get_logger(__name__)


class RateLimitExceeded(Exception):
    pass


class AuthorizationError(Exception):
    pass


class ChannelAdvisorClient:
    CA_ENDPOINT = "https://api.channeladvisor.com/v1/"
    _access_token: str = None

    def set_test_access_token(self, token):
        """Method specifically for testing purposes"""
        self._access_token = token

    @property
    def auth_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    @property
    def access_token(self):
        """Renews Channel Advisor access token using refresh token"""
        if not self._access_token:
            oath_ep = "https://api.channeladvisor.com/oauth2/token"

            # Get credentials
            app_id = os.getenv("CA_APPLICATION_ID")
            shared_secret = os.getenv("CA_SHARED_SECRET")
            refresh_token = os.getenv("CA_REFRESH_TOKEN")

            if not all([app_id, shared_secret, refresh_token]):
                raise ValueError("Missing required environment variables")

            # Create auth string - ensure no whitespace
            auth_string = base64.b64encode(f"{app_id.strip()}:{shared_secret.strip()}".encode()).decode()
            headers = {
                "Authorization": f"Basic {auth_string}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cache-Control": "no-cache",
            }
            body = {"grant_type": "refresh_token", "refresh_token": refresh_token, "expires_in": 3600}
            resp = requests.post(oath_ep, data=body, headers=headers)
            if not resp.ok:
                raise ValueError(f"Failed to renew token. Status: {resp.status_code}. Response: {resp.text}")
            self._access_token = resp.json()["access_token"]
        return self._access_token

    def request(
        self, method: str, uri: str, data: dict = None, attempts: int = 0, **kwargs
    ) -> requests.Response | None:
        url = self.CA_ENDPOINT + uri
        logger.info(f"Request: {method.upper()}: {url}", extra={"method": method, "url": url, "kwargs": kwargs})
        headers = self.auth_headers
        # Encode data as JSON if present
        json_data = json.dumps(data) if data else None
        # TODO make this async
        response = requests.request(method, url, data=json_data, headers=headers, **kwargs)
        if not response.ok:
            attempts += 1
            if response.status_code == 401:
                msg = (
                    f"Authorization Error: {response.status_code} for {method.upper()} {uri} attempt {attempts}. "
                    f"Msg: '{response.text}'."
                )
                if attempts >= 2:
                    raise AuthorizationError(msg)
                logger.info(msg + " Renewing access token.")
                self.set_test_access_token(None)
                return self.request(method, uri, attempts=attempts, **kwargs)
            elif response.status_code == 404:
                logger.warning(f"Not Found: {response.status_code} for {method.upper()} {uri}. Returning None")
                return None
            elif response.status_code == 429:
                # rate limit exceeded backoff and retry
                sleep_time = 5 * attempts
                msg = (
                    f"Rate Limit: {response.status_code} for {method.upper()} {uri} attempt {attempts} "
                    f"in {sleep_time} seconds. Error: '{response.text}'"
                )
                logger.info(msg)
                if attempts >= 5:
                    # eventually give up
                    raise RateLimitExceeded(msg)
                time.sleep(sleep_time)  # TODO make this async
                return self.request(method, uri, attempts=attempts, **kwargs)
            raise Exception(
                f"Request {method.upper()} {url} failed. Status: {response.status_code}. Response: {response.text}"
            )
        return response

    def get_all_pages(self, url: str, limit: int = None) -> List[dict]:
        items = []
        next_link = url
        page_count = 0
        start_time = time.time()
        if limit:
            # parse the url and add/update a query param called $top=limit if limit is provided
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            query_params["$top"] = [limit]
            next_link = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()
        while next_link:
            next_link = next_link.replace(ChannelAdvisorClient.CA_ENDPOINT, "")
            response = self.request("get", next_link)
            if not response:
                logger.warning(f"Request get {next_link} returned None. Breaking loop")
                break
            content = json.loads(response.content)
            # most endpoint return value as a list. Atributes return Value as string
            value = content.get("value") or content.get("Value") or []
            if isinstance(value, str):
                value = [value]
            items += value
            next_link = content.get("@odata.nextLink", None)
            page_count += 1
        end_time = time.time()
        seconds = round(end_time - start_time, 2)
        logger.info(
            f"get_all_pages('{url}') returned {len(items)} items from {page_count} pages in {seconds} seconds",
            extra={
                "method": "get_all_pages",
                "url": url,
                "item_count": len(items),
                "page_count": page_count,
                "duration": seconds,
            },
        )
        return items
