# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import re

GENEVA_RAY_HEAD_NODE = "geneva.lancedb.com/ray-head"
GENEVA_RAY_CPU_NODE = "geneva.lancedb.com/ray-worker-cpu"
GENEVA_RAY_GPU_NODE = "geneva.lancedb.com/ray-worker-gpu"

CPU_ONLY_NODE = "cpu-only"

# Custom resource to identify Geneva-managed autoscaling clusters
# This is set on KubeRay head nodes and can be detected via ray.cluster_resources()
GENEVA_AUTOSCALING_RESOURCE = "geneva_autoscaling"

DEFAULT_MAX_WORKER_REPLICAS = 100


def get_ray_image(
    version: str, python_version: str, *, gpu: bool = False, arm: bool = False
) -> str:
    """Return the Ray Docker image name for the given version and options.

    Parameters
    ----------
    version : str
        Ray version (e.g. ``"2.9.0"``).
    python_version : str
        Python version (e.g. ``"3.12"``); dots are stripped (e.g. ``"3.12"`` →
        ``"312"``).
    gpu : bool, optional
        If True, use the GPU variant of the image (adds ``-gpu``). Default is False.
    arm : bool, optional
        If True, use the ARM/aarch64 variant (adds ``-aarch64``). Default is False.

    Returns
    -------
    str
        Image name, e.g. ``"rayproject/ray:2.9.0-py312"`` or
        ``"rayproject/ray:2.9.0-py312-gpu-aarch64"``.
    """
    py_version = python_version.replace(".", "")
    image = f"rayproject/ray:{version}-py{py_version}"
    if gpu:
        image += "-gpu"
    if arm:
        # todo: is this needed? ray provides multi-platform images
        image += "-aarch64"
    return image


# K8s quantity suffixes: binary (1024^n) and SI (1000^n).
# See: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
_QUANTITY_BINARY = {
    "ki": 1024**1,
    "mi": 1024**2,
    "gi": 1024**3,
    "ti": 1024**4,
    "pi": 1024**5,
    "ei": 1024**6,
}
_QUANTITY_SI = {
    "n": 1e-9,
    "u": 1e-6,
    "m": 1e-3,  # milli
    "k": 1e3,
    "M": 1e6,
    "G": 1e9,
    "T": 1e12,
    "P": 1e15,
    "E": 1e18,
    "g": 1e9,
    "t": 1e12,
    "p": 1e15,
    "e": 1e18,  # same as uppercase
}
_QUANTITY_PATTERN = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*([a-zA-Z]+)?\s*$")


def size_to_bytes(value: int | str) -> int:
    """Convert a K8s-style quantity string to bytes.
    Does not import kubernetes.utils.parse_quantity to avoid dependency on kubernetes.

    Supports:
    - Binary suffixes: Ki, Mi, Gi, Ti, Pi, Ei
    - SI suffixes: n, u, m, k, M, G, T, P, E
    - Decimal values: 1.5Gi
    - Plain integers: 1000000000

    See: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
    """
    if isinstance(value, int):
        return value
    s = str(value).strip()
    m = _QUANTITY_PATTERN.match(s)
    if not m:
        raise ValueError(
            f"Invalid quantity format: {value!r}. "
            f"Expected format: <number><unit> (e.g., '8Gi', '16G', '1.5Mi', '1000'). "
            f"Supported units: Ki, Mi, Gi, Ti, Pi, Ei (binary) or "
            f"n, u, m, k, M, G, T, P, E (SI)."
        )
    num_str, suffix = m.group(1), (m.group(2) or "").strip()
    num = float(num_str)
    if not suffix:
        return int(num)
    suffix_lower = suffix.lower()
    if suffix_lower in _QUANTITY_BINARY:
        return int(num * _QUANTITY_BINARY[suffix_lower])
    if suffix in _QUANTITY_SI:
        return int(num * _QUANTITY_SI[suffix])
    if suffix_lower in _QUANTITY_SI:
        return int(num * _QUANTITY_SI[suffix_lower])
    raise ValueError(
        f"Invalid quantity format: {value!r}. "
        f"Expected format: <number><unit> (e.g., '8Gi', '16G', '1.5Mi', '1000'). "
        f"Supported units: Ki, Mi, Gi, Ti, Pi, Ei (binary) or "
        f"n, u, m, k, M, G, T, P, E (SI)."
    )
