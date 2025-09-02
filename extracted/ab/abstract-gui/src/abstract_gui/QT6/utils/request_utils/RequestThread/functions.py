from abstract_apis import *
# RequestThread/functions.py
from ..imports import *
from abstract_apis import getRequest, postRequest
import json, requests

def run(self):
    try:
        if self.is_detect:
            base = self.url.rstrip("/")
            for path in ("/config", "/__config", "/_meta"):
                try:
                    r = requests.get(base + path, headers={"Accept":"application/json"},
                                     timeout=self.timeout, allow_redirects=False)
                    j = r.json()
                    val = (j.get("static_url_path") or j.get("api_prefix") or "").strip()
                    if val:
                        self.response_signal.emit(val, f"API prefix set to: {val}")
                        return
                except Exception as e:
                    logging.debug(f"detect probe failed: {e}")
            self.response_signal.emit("/api", "API prefix defaulted to /api")
            return

        # Normal GET/POST via abstract_apis with timeouts
        if self.method == "GET":
            res = getRequest(url=self.url, headers=self.headers, data=self.params, timeout=self.timeout)
        else:
            res = postRequest(url=self.url, headers=self.headers, data=self.params, timeout=self.timeout)

        # Normalize to text for the UI
        try:
            txt = json.dumps(res, indent=4) if isinstance(res, (dict, list)) else str(res)
        except Exception:
            txt = str(res)
        self.response_signal.emit(txt, "✔ Response displayed")
    except requests.TooManyRedirects as e:
        self.error_signal.emit(f"Redirect loop: {e}")
    except requests.Timeout:
        self.error_signal.emit("Request timed out.")
    except Exception as ex:
        self.error_signal.emit(f"✖ Error: {ex}")
