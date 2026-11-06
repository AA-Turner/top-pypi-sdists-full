from __future__ import annotations

import importlib.metadata
from pathlib import Path

DOCS_URL = "https://docs.trajectory.ai"
AUTHENTICATION_URL = f"{DOCS_URL}/authentication"


class GuideLinks:
  @staticmethod
  def for_setup(template: str, can_train: bool = True) -> list[dict[str, str]]:
    if template == "connect":
      pages = [("Capture production traces", "guides/production-traces")]
    else:
      pages = [
        ("Set up and diagnose a benchmark", "guides/spec"),
        ("Evaluate a model", "guides/evaluations"),
      ]
      if template == "cookbook" and can_train:
        pages.append(("Train and compare checkpoints", "guides/training"))
    return [{"title": title, "url": f"{DOCS_URL}/{path}"} for title, path in pages]


class BundledDocs:
  @staticmethod
  def path(relative: str) -> Path:
    for file in importlib.metadata.files("trajectory-sdk") or []:
      if str(file).endswith(f"share/doc/trajectory-sdk/{relative}"):
        resource = Path(file.locate())
        if resource.is_file():
          return resource.resolve()
    docs = Path(__file__).resolve().parents[4] / "docs"
    local = docs / ".mintlify" / relative if relative.startswith("skills/") else docs / relative
    if local.is_file():
      return local
    raise FileNotFoundError(
      f"Bundled documentation {relative} is missing. Reinstall trajectory-sdk or read {DOCS_URL}."
    )
