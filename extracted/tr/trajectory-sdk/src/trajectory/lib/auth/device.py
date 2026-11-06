from __future__ import annotations

import importlib.metadata
import math
import platform
import socket
import time
from collections.abc import Callable
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Literal

import httpx2
from pydantic import BaseModel, Field, ValidationError

from trajectory.lib.auth.credentials import AuthError, CredentialStore
from trajectory.lib.browser import open_default_browser


class DeviceSession(BaseModel):
  device_code: str = Field(min_length=1, repr=False)
  user_code: str = Field(min_length=1)
  verification_url: str
  expires_at: datetime
  poll_interval_seconds: float = Field(gt=0)


class Organization(BaseModel):
  id: str = Field(min_length=1)
  key: str
  name: str


class ApprovedToken(BaseModel):
  status: Literal["approved"]
  api_key: str = Field(min_length=1, repr=False)
  api_key_prefix: str
  organization: Organization
  user_email: str


class DeviceAuth:
  def __init__(
    self,
    base_url: str,
    http_client: httpx2.Client | None = None,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
  ) -> None:
    self.base_url = CredentialStore.validate_login_url(base_url)
    self._http = http_client or httpx2.Client(timeout=15, follow_redirects=False)
    self._owns_http = http_client is None
    self._clock = clock
    self._sleep = sleep

  def close(self) -> None:
    if self._owns_http:
      self._http.close()

  def login(
    self,
    no_browser: bool = False,
    timeout: float = 600,
    report: Callable[[str], None] | None = None,
  ) -> ApprovedToken:
    if not math.isfinite(timeout) or timeout <= 0:
      raise AuthError("invalid_timeout", "Login timeout must be a positive number of seconds.")
    deadline = self._clock() + min(timeout, 600)
    payload = {
      "client_name": "trajectory",
      "client_version": importlib.metadata.version("trajectory-sdk"),
      "hostname": socket.gethostname()[:255],
      "platform": f"{platform.system().lower()}-{platform.machine()}"[:64],
    }
    response = self._request(
      "POST", "/api/v1/device/auth/sessions", payload, timeout=min(15, timeout)
    )
    self._check_response(response)
    try:
      session = DeviceSession.model_validate(response.json())
      verification_url = httpx2.URL(session.verification_url)
      if (
        verification_url.scheme not in {"https", "http"}
        or not verification_url.host
        or verification_url.username
        or verification_url.password
      ):
        raise ValueError("invalid verification URL")
      if verification_url.scheme == "http" and verification_url.host not in {
        "localhost",
        "127.0.0.1",
        "::1",
      }:
        raise ValueError("insecure verification URL")
      expires_in = (session.expires_at - datetime.now(timezone.utc)).total_seconds()
    except (ValueError, ValidationError) as error:
      raise AuthError("invalid_response", "The API returned an invalid login session.") from error
    deadline = min(deadline, self._clock() + expires_in)
    if report is not None:
      report(f"Open {session.verification_url}\nConfirm code: {session.user_code}")
    if not no_browser:
      opened = open_default_browser(session.verification_url)
      if not opened and report is not None:
        report("Could not open a browser; open the URL above on a device where you can sign in.")
    interval = session.poll_interval_seconds
    while True:
      remaining = deadline - self._clock()
      if remaining <= interval:
        raise AuthError("login_expired", "Login expired. Run tj login again to get a new code.")
      self._sleep(interval)
      remaining = deadline - self._clock()
      if remaining <= 0:
        raise AuthError("login_expired", "Login expired. Run tj login again to get a new code.")
      try:
        response = self._request(
          "POST",
          "/api/v1/device/auth/token",
          {"device_code": session.device_code},
          timeout=min(15, remaining),
        )
      except AuthError as error:
        raise AuthError(
          "login_redemption_uncertain",
          "The login response was lost. A key may have been issued; review and revoke the CLI key in the web app, then run tj login again.",
        ) from error
      if response.status_code == 429:
        interval = max(interval, self._retry_after(response))
        continue
      if response.status_code >= 500:
        raise AuthError(
          "login_redemption_uncertain",
          "The API could not confirm login redemption. Review and revoke any newly issued CLI key in the web app, then run tj login again.",
        )
      self._check_response(response)
      try:
        token = response.json()
        status = token["status"]
        if status == "approved":
          return ApprovedToken.model_validate(token)
        if status == "pending":
          interval = max(session.poll_interval_seconds, float(token["poll_interval_seconds"]))
          if not math.isfinite(interval):
            raise ValueError("invalid polling interval")
          continue
      except (ValueError, KeyError, TypeError, ValidationError) as error:
        raise AuthError(
          "login_redemption_uncertain",
          "The login response was invalid. Review and revoke any newly issued CLI key in the web app, then run tj login again.",
        ) from error
      if status == "denied":
        raise AuthError("login_denied", "Login was denied in the browser.")
      if status == "expired":
        raise AuthError(
          "login_expired", "Login expired or was already redeemed. Run tj login again."
        )
      raise AuthError("invalid_response", "The API returned an unknown login status.")

  def whoami(self, api_key: str) -> dict[str, Any]:
    response = self._request("GET", "/api/v1/organizations/current", api_key=api_key)
    self._check_response(response)
    try:
      data = response.json()
      if not isinstance(data, dict) or not isinstance(data.get("organization_id"), str):
        raise ValueError("invalid organization")
      return {key: data[key] for key in ("organization_id", "organization_key") if key in data}
    except ValueError as error:
      raise AuthError(
        "invalid_response", "The API returned an invalid organization response."
      ) from error

  def logout(self, api_key: str) -> None:
    response = self._request("POST", "/api/v1/device/auth/logout", api_key=api_key)
    if response.status_code == 401:
      return
    self._check_response(response)
    try:
      if response.json().get("revoked") is not True:
        raise ValueError("revocation unconfirmed")
    except (ValueError, AttributeError) as error:
      raise AuthError(
        "revocation_unconfirmed",
        "The API did not confirm revocation; the saved credential was retained.",
      ) from error

  def _request(
    self,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    api_key: str | None = None,
    timeout: float = 15,
  ) -> httpx2.Response:
    request = self._http.build_request(method, self.base_url + path, json=payload, timeout=timeout)
    for header in ("Authorization", "X-API-Key", "Cookie", "X-Model-Endpoint-Access-Token"):
      request.headers.pop(header, None)
    request.headers["Trajectory-API-Version"] = "tmp-contract"
    if api_key:
      request.headers["X-API-Key"] = api_key
    try:
      return self._http.send(request, auth=None, follow_redirects=False)
    except httpx2.HTTPError as error:
      raise AuthError(
        "auth_connection_failed", "Could not reach the API. Check your connection and API URL."
      ) from error

  @staticmethod
  def _check_response(response: httpx2.Response) -> None:
    if response.is_success:
      return
    if response.status_code == 401:
      raise AuthError("not_authenticated", "The credential is no longer valid; run tj login.")
    if response.status_code == 404:
      raise AuthError(
        "login_unavailable",
        "This API does not support CLI login yet. Use TRAJECTORY_API_KEY until device login is deployed.",
      )
    raise AuthError(
      "auth_request_failed", f"The authentication request failed (HTTP {response.status_code})."
    )

  @staticmethod
  def _retry_after(response: httpx2.Response) -> float:
    value = response.headers.get("Retry-After", "2")
    try:
      seconds = float(value)
    except ValueError:
      try:
        seconds = (parsedate_to_datetime(value) - datetime.now(timezone.utc)).total_seconds()
      except (ValueError, TypeError):
        seconds = 2
    return max(0, seconds) if math.isfinite(seconds) else 2
