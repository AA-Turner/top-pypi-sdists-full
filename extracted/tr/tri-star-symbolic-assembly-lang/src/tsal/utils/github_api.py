from typing import Dict, List, Optional

try:  # optional dependency
    import requests  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback used in CI
    import urllib.request

    class _Response:
        def __init__(self, text: str, status: int = 200) -> None:
            self.text = text
            self.status_code = status

        def json(self) -> List[Dict]:
            import json

            return json.loads(self.text)

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise RuntimeError(f"status {self.status_code}")

    class requests:  # minimal shim for tests
        @staticmethod
        def get(url: str, headers: Dict[str, str] | None = None) -> _Response:
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req) as resp:
                text = resp.read().decode()
            return _Response(text, resp.getcode())

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - simple parser
    yaml = None

def _get_json(url: str, headers: Dict[str, str]) -> List[Dict]:
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def fetch_repo_files(
    repo: str,
    extensions: Optional[List[str]] = None,
    token: Optional[str] = None,
) -> Dict[str, str]:
    """Fetch files from a GitHub repository via the GitHub API."""
    base = f"https://api.github.com/repos/{repo}/contents"
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    def recurse(path: str) -> Dict[str, str]:
        url = base + ("/" + path if path else "")
        items = _get_json(url, headers)
        files: Dict[str, str] = {}
        for item in items:
            if item["type"] == "file":
                if extensions is None or any(
                    item["name"].endswith(ext) for ext in extensions
                ):
                    f = requests.get(item["download_url"], headers=headers)
                    if f.status_code == 200:
                        files[item["path"]] = f.text
            elif item["type"] == "dir":
                files.update(recurse(item["path"]))
        return files

    return recurse("")

def fetch_languages(
    url: str = "https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml",
) -> List[str]:
    """Return the list of programming languages from GitHub's Linguist database."""
    resp = requests.get(url)
    resp.raise_for_status()
    if yaml:
        data = yaml.safe_load(resp.text)
        return list(data.keys())
    langs = []
    for line in resp.text.splitlines():
        if ":" in line:
            langs.append(line.split(":", 1)[0].strip())
    return langs
