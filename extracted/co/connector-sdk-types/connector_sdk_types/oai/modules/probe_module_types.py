from __future__ import annotations

from pydantic import BaseModel, Field, StrictBool, field_validator

# Import directly from modules to avoid circular import through generated/__init__.py
from connector_sdk_types.generated.models.probe_check_name import ProbeCheckName
from connector_sdk_types.oai.probe import ProbeCheckSpec

# The checks the SDK can perform on a connector's behalf, in the order a caller would
# normally walk them. Each check is self-contained, so a check fetches whatever it needs
# rather than relying on an earlier one having run.
DEFAULT_PROBE_CHECK_ORDER: tuple[ProbeCheckName, ...] = (
    ProbeCheckName.ACCOUNTS,
    ProbeCheckName.ENTITLEMENTS,
    ProbeCheckName.ENTITLEMENT_ASSOCIATIONS,
)


class ProbeSettings(BaseModel):
    """Settings for the ProbeModule.

    A connector opts into `probe_integration` globally by default. To opt out of the default
    you can either implement the capability manually, or generally opt-out.

    ```python
    integration = Integration(
        # Full disable
        probe_settings=ProbeSettings.disabled(),
        # or like this and implement your own
        probe_settings=ProbeSettings.manual(),
    )
    ```

    Each entry in `checks` either names the connector's own implementation or leaves `run`
    unset, which asks the SDK to perform that check by exercising the connector's standard
    capabilities with a minimal page size.

    Example - the SDK does the ordinary checks, the connector implements the hard one:
    ```python
    integration = Integration(
        ...,
        probe_settings=ProbeSettings(
            checks=[
                ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS),
                ProbeCheckSpec(check=ProbeCheckName.ENTITLEMENTS),
                ProbeCheckSpec(
                    check=ProbeCheckName.ENTITLEMENT_ASSOCIATIONS,
                    run=capabilities_probe.probe_associations,
                ),
            ],
        ),
    )
    ```
    """

    register_probe_capability: StrictBool = Field(
        default=True,
        description=(
            "Flag that indicates whether the ProbeModule should register the probe_integration "
            "capability. Set to `False` to skip registration and implement the capability manually."
        ),
    )
    checks: list[ProbeCheckSpec] = Field(
        default_factory=list,
        description=(
            "The checks this connector's probe performs, in order. Checks absent from this "
            "list are reported as `unsupported`."
        ),
    )
    page_size: int = Field(
        default=10,
        ge=1,
        description=(
            "Page size the SDKs checks request, and so the most samples a check returns. Ten "
            "gives a consumer several records to recognize."
        ),
    )
    max_entitlement_pages: int = Field(
        default=5,
        ge=1,
        description=(
            "How many pages of entitlements the SDKs check reads while looking for one "
            "entitlement of every declared entitlement type. Types still unseen when the budget "
            "runs out are reported as `not_checked` rather than `not_found`, because a probe "
            "runs while a customer waits and might not be able to page an entire tenant."
        ),
    )
    per_check_timeout_seconds: float = Field(
        default=180.0,
        gt=0,
        description=(
            "Wall-clock budget for a single check. A check that exceeds it fails with a timeout "
            "error rather than hanging the run."
        ),
    )

    @field_validator("checks")
    @classmethod
    def _reject_duplicate_checks(cls, checks: list[ProbeCheckSpec]) -> list[ProbeCheckSpec]:
        """One entry per check: a second entry for the same check would be ignored."""
        seen = [spec.check.value for spec in checks]
        duplicates = sorted({name for name in seen if seen.count(name) > 1})
        if duplicates:
            raise ValueError(f"Duplicate probe check configuration for: {', '.join(duplicates)}")
        return checks

    @classmethod
    def disabled(cls) -> ProbeSettings:
        """Disable the global probe_integration opt-in for a connector."""
        return cls(register_probe_capability=False)

    @classmethod
    def manual(cls) -> ProbeSettings:
        """Implement the probe_integration capability manually and skip the module registration."""
        return cls(register_probe_capability=False)

    @classmethod
    def default(cls) -> ProbeSettings:
        """Every check, all performed by the SDK against the connector's standard capabilities."""
        return cls(checks=[ProbeCheckSpec(check=check) for check in DEFAULT_PROBE_CHECK_ORDER])
