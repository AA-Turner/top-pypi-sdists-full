from typing import Dict, Optional
import requests
import time


class FastBakeryException(Exception):
    pass


class SolverStats:
    def __init__(self, stats) -> None:
        self.stats = stats

    @property
    def duration_ms(self):
        return self.stats["durationMs"]

    @property
    def packages_in_solved_environment(self):
        return self.stats["packagesInSolvedEnvironment"]


class BakingStats:
    def __init__(self, stats) -> None:
        self.stats = stats

    @property
    def solver_stats(self) -> Optional[SolverStats]:
        if "solverStats" not in self.stats:
            return None
        return SolverStats(self.stats["solverStats"])


class FastBakeryApiResponse:
    def __init__(self, response) -> None:
        self.response = response

    @property
    def python_path(self) -> Optional[str]:
        if not self.success:
            return None

        return self.response["success"]["pythonPath"]

    @property
    def container_image(self) -> Optional[str]:
        if not self.success:
            return None

        return self.response["success"]["containerImage"]

    @property
    def success(self) -> bool:
        return "success" in self.response

    @property
    def baking_stats(self) -> Optional[BakingStats]:
        if not self.success:
            return None

        if "bakingStats" not in self.response["success"]:
            return None

        if self.response["success"]["bakingStats"] is None:
            return None

        return BakingStats(self.response["success"]["bakingStats"])

    @property
    def failure(self) -> bool:
        return "failure" in self.response


class FastBakery:
    def __init__(self, url: str):
        if not url:
            raise FastBakeryException("Specifying a url is required.")
        self.url = url
        self.headers = {"Content-Type": "application/json", "Connection": "keep-alive"}
        self._reset_payload()

    def _reset_payload(self):
        self._payload = {}
        from metaflow_extensions.outerbounds.remote_config import init_config
        from os import environ

        conf = init_config()
        if "OBP_PERIMETER" in conf:
            perimeter = conf["OBP_PERIMETER"]
        else:
            # if the perimeter is not in metaflow config, try to get it from the environment
            perimeter = environ.get("OBP_PERIMETER", "")

        self._payload["perimeterName"] = perimeter

    def python_version(self, version: str):
        self._payload["pythonVersion"] = version
        return self

    def pypi_packages(self, packages: Dict[str, str]):
        self._payload.setdefault("pipRequirements", []).extend(
            self._format_packages(packages)
        )
        return self

    def conda_packages(self, packages: Dict[str, str]):
        self._payload.setdefault("condaMatchspecs", []).extend(
            self._format_packages(packages)
        )
        return self

    def base_image(self, image: str):
        self._payload["baseImage"] = {"imageReference": image}
        return self

    def image_kind(self, kind: str):
        self._payload["imageKind"] = kind
        return self

    def ignore_cache(self):
        self._payload["cacheBehavior"] = {
            "responseMaxAgeSeconds": 0,
            "layerMaxAgeSeconds": 0,
            "baseImageMaxAgeSeconds": 0,
            "overwriteExistingLayers": True,  # Used primarily to rewrite possibly corrupted layers.
        }
        return self

    @staticmethod
    def _format_packages(packages: Dict[str, str]) -> list:
        if not packages:
            return []

        def format_package(pkg: str, ver: str) -> str:
            return (
                f"{pkg}{ver}"
                if any(ver.startswith(c) for c in [">", "<", "~", "@", "="])
                else (f"{pkg}=={ver}" if ver != "" else f"{pkg}")
            )

        return [format_package(pkg, ver) for pkg, ver in packages.items()]

    def bake(self) -> FastBakeryApiResponse:
        if "imageKind" not in self._payload:
            self._payload["imageKind"] = "oci-zstd"  # Set default if not specified

        res = self._make_request(self._payload)
        self._reset_payload()
        return res

    def _make_request(self, payload: Dict) -> FastBakeryApiResponse:
        try:
            from metaflow.metaflow_config import SERVICE_HEADERS

            headers = {**self.headers, **(SERVICE_HEADERS or {})}
        except ImportError:
            headers = self.headers

        retryable_status_codes = [409]

        for attempt in range(2):  # 0 = initial attempt, 1-2 = retries
            response = requests.post(self.url, json=payload, headers=headers)

            if response.status_code not in retryable_status_codes:
                break

            if attempt < 2:  # Don't sleep after the last attempt
                sleep_time = 0.5 * (attempt + 1)
                time.sleep(sleep_time)

        response = requests.post(self.url, json=payload, headers=headers)
        self._handle_error_response(response)
        return FastBakeryApiResponse(response.json())

    @staticmethod
    def _handle_error_response(response: requests.Response):
        if response.status_code >= 500:
            raise FastBakeryException(f"Server error: {response.text}")

        body = response.json()
        status_code = body.get("error", {}).get("statusCode", response.status_code)
        if status_code >= 400:
            try:
                raise FastBakeryException(
                    f"*{body['error']['details']['kind']}*\n{body['error']['details']['message']}"
                )
            except KeyError:
                raise FastBakeryException(f"Unexpected error: {body}")
