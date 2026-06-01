"""Network handler interactors."""

import subprocess as sup
from bacore.domain.settings import SystemSettings


def connected_to_gateway() -> bool:
    """Verify if connected to a gateway."""
    gateway_values = ["Default Gateway", "0.0.0.0", "default"]
    os_name = SystemSettings().os
    unix_cmd = ["netstat", "-rn"]
    windows_cmd = ["ipconfig"]

    cmd = windows_cmd if os_name == "Windows" else unix_cmd

    try:
        result = sup.run(cmd, capture_output=True, text=True, check=True)
    except sup.CalledProcessError as e:
        raise RuntimeError("Failed to execute network command") from e

    return any(gateway_value in result.stdout for gateway_value in gateway_values)
