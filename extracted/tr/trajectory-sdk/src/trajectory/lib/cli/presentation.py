from __future__ import annotations

import json
from typing import Any

from trajectory.lib.cli.guides import AUTHENTICATION_URL


class Presenter:
  @staticmethod
  def render(command: str, value: Any) -> str:
    if not isinstance(value, dict):
      return json.dumps(value, indent=2, ensure_ascii=False)
    if command in {"login", "whoami"}:
      organization = value.get("organization") or {}
      name = (
        organization.get("name")
        or organization.get("key")
        or value.get("organization_key", "your organization")
      )
      lines = [f"Signed in to {name}."]
      if value.get("profile"):
        lines.append(f"Profile: {value['profile']}")
      if command == "whoami":
        lines.extend(
          [
            f"Credential source: {value.get('credential_source', 'unknown')}",
            f"API: {value['base_url']}",
          ]
        )
      elif value.get("next_action") and not value.get("setup"):
        lines.append(f"Next: {value['next_action']}")
      if command == "login":
        lines.append(f"Login and profiles: {AUTHENTICATION_URL}")
      if value.get("setup"):
        lines.append(Presenter.render("init", value["setup"]))
      return "\n".join(lines)
    if command == "logout":
      lines = [f"Signed out of profile {value['profile']}; its key was revoked."]
      if value.get("environment_credential_active"):
        lines.append("TRAJECTORY_API_KEY is still set and takes precedence over saved logins.")
      return "\n".join(lines)
    if command == "init":
      if value.get("cancelled"):
        return "Setup cancelled. Run tj init when you are ready."
      if value.get("template") == "skip":
        return "Setup skipped. Run tj init when you are ready."
      lines = [f"Project: {value['project']}", f"Setup: {value['template']}"]
      if value.get("repo"):
        lines.append(f"Benchmark source: {value['repo']}")
      if value.get("cookbook"):
        lines.append(f"Cookbook: {value['cookbook']} ({value['cookbook_url']})")
      lines.extend(f"{guide['title']}: {guide['url']}" for guide in value.get("guides", []))
      created = value.get("created", [])
      lines.append(
        f"Created {len(created)} files." if created else "Existing project files preserved."
      )
      assistant = value.get("assistant")
      if assistant:
        status = assistant["status"]
        if status == "finished":
          lines.append(f"{assistant['name']} session finished. Run tj init to continue setup.")
          return "\n".join(lines)
        if status == "not_installed":
          lines.append(
            f"{assistant['name']} is not installed. Install it: {assistant['install_url']}"
          )
        elif status in {"failed", "launch_failed"}:
          lines.append(
            f"{assistant['name']} did not finish successfully (exit {assistant['exit_code']}). Setup is saved; rerun tj init --assistant {assistant['name']} to retry."
          )
        elif status == "copied":
          lines.append("Setup prompt copied. Paste it into your coding assistant in this project.")
          return "\n".join(lines)
        lines.extend(["", "Paste this prompt into your coding assistant:", assistant["prompt"]])
        return "\n".join(lines)
      lines.extend(["", "Next steps:"])
      lines.extend(
        f"  {index}. {step}" for index, step in enumerate(value.get("next_steps", []), 1)
      )
      return "\n".join(lines)
    if command == "profiles" and "profiles" in value:
      profiles = value["profiles"]
      if not profiles:
        return "No saved profiles. Run tj login."
      lines = []
      for name, profile in profiles.items():
        marker = "*" if name == value.get("active") else " "
        organization = profile["organization"]
        lines.append(
          f"{marker} {name}  {organization.get('name') or organization.get('key')}  {profile['base_url']}"
        )
      return "\n".join(lines)
    return json.dumps(value, indent=2, ensure_ascii=False)
