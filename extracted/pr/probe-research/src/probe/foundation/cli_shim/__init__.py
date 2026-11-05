"""cli_shim: the `probe` console script as plumbing to the Probe service (service-only T7). Stdlib only."""

from probe.foundation.cli_shim.cli_shim import ShimError, run_command

__all__ = ["ShimError", "run_command"]
