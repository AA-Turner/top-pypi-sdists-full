from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Callable
from typing import Any

from trajectory.lib.auth.credentials import DEFAULT_BASE_URL, AuthError, CredentialStore
from trajectory.lib.auth.device import DeviceAuth


class AuthCommands:
  def __init__(
    self,
    base_url: str | None = None,
    profile: str | None = None,
    report: Callable[[str], None] | None = None,
  ) -> None:
    self.base_url = base_url
    self.profile = profile or os.environ.get("TRAJECTORY_PROFILE")
    self.report = report or self._report
    self.store = CredentialStore()

  def ensure_authenticated(self) -> dict[str, Any]:
    if "TRAJECTORY_API_KEY" in os.environ:
      try:
        identity = self.whoami()
      except AuthError as error:
        if error.code != "not_authenticated":
          raise
        raise AuthError(
          "not_authenticated",
          "TRAJECTORY_API_KEY is empty or was rejected. Replace it or unset it and run tj init to sign in.",
        ) from error
    else:
      identity = self.login()
    organization = (
      identity["organization"]["name"]
      if "organization" in identity
      else identity.get("organization_key") or identity["organization_id"]
    )
    self.report(f"Signed in to {organization}.")
    return identity

  def login(self, no_browser: bool = False, timeout: float = 600) -> dict[str, Any]:
    metadata = self.store.metadata()
    name = self.profile or metadata["active"] or "default"
    existing = metadata["profiles"].get(name, {})
    destination = (
      self.base_url
      or os.environ.get("TRAJECTORY_BASE_URL")
      or existing.get("base_url")
      or DEFAULT_BASE_URL
    )
    if name in metadata["profiles"]:
      credential = self.store.get(name, destination)
      device = DeviceAuth(credential.base_url)
      try:
        identity = device.whoami(credential.api_key or "")
        if credential.organization and identity["organization_id"] != credential.organization["id"]:
          raise AuthError(
            "organization_mismatch",
            "The saved profile does not match the credential's organization.",
          )
        return {
          "authenticated": True,
          "already_authenticated": True,
          "profile": name,
          "credential_source": "profile",
          "base_url": credential.base_url,
          **identity,
        }
      except AuthError as error:
        if error.code != "not_authenticated":
          raise
        self.store.remove(name, credential.api_key)
      finally:
        device.close()
    device = DeviceAuth(destination)
    try:
      token = device.login(no_browser, timeout, self.report)
      try:
        self.store.save(
          name, device.base_url, token.api_key, token.organization.model_dump(), token.user_email
        )
      except (OSError, AuthError) as error:
        try:
          device.logout(token.api_key)
        except AuthError:
          raise AuthError(
            "credential_save_failed",
            "Could not save the credential or confirm its revocation. Revoke the newly issued CLI key in the web app before logging in again.",
          ) from error
        raise AuthError(
          "credential_save_failed",
          "Could not save the credential; the new key was revoked. Check your login directory permissions and retry.",
        ) from error
      return {
        "authenticated": True,
        "already_authenticated": False,
        "profile": name,
        "credential_source": "profile",
        "base_url": device.base_url,
        "organization": token.organization.model_dump(),
        "user_email": token.user_email,
        "next_action": "tj init",
      }
    finally:
      device.close()

  def logout(self) -> dict[str, Any]:
    name = self.profile or self.store.metadata()["active"]
    if not name:
      raise AuthError(
        "not_authenticated",
        "There is no saved login to revoke. Environment credentials are managed separately.",
      )
    credential = self.store.get(name, self.base_url)
    device = DeviceAuth(credential.base_url)
    try:
      device.logout(credential.api_key or "")
    finally:
      device.close()
    self.store.remove(name, credential.api_key)
    return {
      "revoked": True,
      "profile": name,
      "environment_credential_active": bool(os.environ.get("TRAJECTORY_API_KEY")),
    }

  def whoami(self) -> dict[str, Any]:
    credential = CredentialStore.resolve(base_url=self.base_url, profile=self.profile)
    if not credential.api_key:
      raise AuthError("not_authenticated", "Run tj login or set TRAJECTORY_API_KEY.")
    device = DeviceAuth(credential.base_url)
    try:
      identity = device.whoami(credential.api_key)
      if credential.organization and identity["organization_id"] != credential.organization["id"]:
        raise AuthError(
          "organization_mismatch", "The saved profile does not match the credential's organization."
        )
      return {
        "authenticated": True,
        "credential_source": credential.source,
        "profile": credential.profile,
        "base_url": credential.base_url,
        **identity,
      }
    finally:
      device.close()

  def profiles(self) -> dict[str, Any]:
    return self.store.metadata()

  def use_profile(self, name: str) -> dict[str, Any]:
    result = self.store.use(name)
    result["environment_credential_active"] = bool(os.environ.get("TRAJECTORY_API_KEY"))
    return result

  @staticmethod
  def _report(message: str) -> None:
    print(message, file=sys.stderr)


def configure_parser(subparsers: Any) -> None:
  login = subparsers.add_parser("login", help="Sign in through your browser")
  login.add_argument("--no-browser", action="store_true")
  login.add_argument("--timeout", type=float, default=600)
  subparsers.add_parser("logout", help="Revoke a saved login")
  subparsers.add_parser("whoami", help="Verify credentials and show the current organization")
  profiles = subparsers.add_parser("profiles", help="List or select saved login profiles")
  actions = profiles.add_subparsers(dest="profile_action")
  actions.add_parser("list")
  use = actions.add_parser("use")
  use.add_argument("name")


def run(args: argparse.Namespace, report: Callable[[str], None] | None = None) -> dict[str, Any]:
  commands = AuthCommands(getattr(args, "base_url", None), getattr(args, "profile", None), report)
  if args.command == "login":
    return commands.login(args.no_browser, args.timeout)
  if args.command == "logout":
    return commands.logout()
  if args.command == "whoami":
    return commands.whoami()
  if getattr(args, "profile_action", None) == "use":
    return commands.use_profile(args.name)
  return commands.profiles()
