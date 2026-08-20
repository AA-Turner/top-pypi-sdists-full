"""Scope policy data model for offensive security operations.

Defines a structured, hierarchical capability and boundary model that
an operator can configure to control what an agent is authorized to do
during a security engagement. The model supports:

- **Presets** — named baseline configs (``recon_only``, ``standard_pentest``,
  ``red_team``) that fill every category with sensible defaults.
- **Capability categories** with subcategories — blanket category settings
  cascade to subcategories unless explicitly overridden.
- **Target boundaries** — network, domain, service, cloud, and identity
  scopes that constrain *where* the agent can operate.
- **Template rendering** — the resolved scope config is rendered to a
  natural-language rubric string for the judge LLM.

Resolution order: ``preset defaults → category blanket → subcategory override``
"""

from enum import StrEnum

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Policy values
# ---------------------------------------------------------------------------


class Policy(StrEnum):
    """Per-capability authorization level."""

    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"


# ---------------------------------------------------------------------------
# Capability categories
# ---------------------------------------------------------------------------


class _CategoryBase(BaseModel):
    """Base for capability categories.

    Each category has an optional blanket ``policy``. Subcategory fields
    default to ``None``, meaning "inherit from category blanket." The
    ``resolve`` method returns the effective policy for any subcategory.
    """

    policy: Policy | None = None

    def resolve(self, subcategory: str, default: Policy = Policy.DENY) -> Policy:
        """Return the effective policy for *subcategory*.

        Resolution: subcategory field → category blanket → *default*.
        """
        value = getattr(self, subcategory, None)
        if isinstance(value, Policy):
            return value
        if self.policy is not None:
            return self.policy
        return default

    def subcategory_names(self) -> list[str]:
        """Return all subcategory field names (excludes ``policy``)."""
        return [name for name in type(self).model_fields if name != "policy"]

    def resolved_map(self, default: Policy = Policy.DENY) -> dict[str, Policy]:
        """Return ``{subcategory: effective_policy}`` for every subcategory."""
        return {name: self.resolve(name, default) for name in self.subcategory_names()}


class Reconnaissance(_CategoryBase):
    dns_enumeration: Policy | None = None
    port_scanning: Policy | None = None
    service_fingerprinting: Policy | None = None
    osint: Policy | None = None
    web_spidering: Policy | None = None
    network_sniffing: Policy | None = None
    directory_bruteforce: Policy | None = None
    vulnerability_scanning: Policy | None = None


class Exploitation(_CategoryBase):
    web_application: Policy | None = None  # SQLi, XSS, SSRF, SSTI, LFI/RFI
    network_service: Policy | None = None  # service-level exploits
    known_cve: Policy | None = None  # public CVE / published PoC
    custom_exploit: Policy | None = None  # 0-day / bespoke exploit dev
    binary_exploitation: Policy | None = None  # buffer overflow, ROP, etc.
    wireless: Policy | None = None  # WiFi, Bluetooth


class CredentialAccess(_CategoryBase):
    credential_dumping: Policy | None = None  # mimikatz, secretsdump, SAM/NTDS
    kerberoasting: Policy | None = None
    asrep_roasting: Policy | None = None
    offline_cracking: Policy | None = None  # hashcat, john
    password_spraying: Policy | None = None
    brute_force: Policy | None = None
    token_manipulation: Policy | None = None  # ticket forging, token impersonation
    keylogging: Policy | None = None
    credential_phishing: Policy | None = None  # responder, fake login


class PrivilegeEscalation(_CategoryBase):
    local: Policy | None = None  # kernel, SUID, sudo, UAC bypass
    domain: Policy | None = None  # DCSync, GPO abuse, AD delegation
    service_account_abuse: Policy | None = None
    container_escape: Policy | None = None


class LateralMovement(_CategoryBase):
    pass_the_hash: Policy | None = None
    pass_the_ticket: Policy | None = None
    remote_services: Policy | None = None  # PSExec, WMI, WinRM, SSH
    pivoting: Policy | None = None  # SSH tunnels, port forwards, SOCKS
    rdp: Policy | None = None
    internal_phishing: Policy | None = None


class Persistence(_CategoryBase):
    scheduled_tasks: Policy | None = None  # cron, at, Windows Task Scheduler
    registry_keys: Policy | None = None  # run keys, services
    service_creation: Policy | None = None
    backdoor: Policy | None = None
    web_shell: Policy | None = None
    implant: Policy | None = None  # C2 agent deployment
    account_creation: Policy | None = None


class DefenseEvasion(_CategoryBase):
    av_edr_bypass: Policy | None = None
    process_injection: Policy | None = None
    obfuscation: Policy | None = None  # encoding, packing
    log_tampering: Policy | None = None
    timestomping: Policy | None = None
    indicator_removal: Policy | None = None  # clearing tracks


class Collection(_CategoryBase):
    file_collection: Policy | None = None
    screen_capture: Policy | None = None
    clipboard: Policy | None = None
    email_collection: Policy | None = None
    database_collection: Policy | None = None
    audio_capture: Policy | None = None


class Exfiltration(_CategoryBase):
    data_staging: Policy | None = None  # local staging before exfil
    exfil_over_c2: Policy | None = None
    exfil_over_alt_protocol: Policy | None = None  # DNS, ICMP, steganography
    exfil_over_web: Policy | None = None  # HTTP/S POST to external


class Impact(_CategoryBase):
    data_destruction: Policy | None = None
    service_disruption: Policy | None = None  # DoS, service stop
    defacement: Policy | None = None
    ransomware: Policy | None = None
    resource_hijacking: Policy | None = None  # cryptomining


class Operations(_CategoryBase):
    """Low-level system operations — not attack techniques, but primitives."""

    file_read: Policy | None = None
    file_write: Policy | None = None
    file_delete: Policy | None = None
    process_management: Policy | None = None
    network_connections: Policy | None = None
    tunneling: Policy | None = None  # SSH tunnels, port forwards, SOCKS proxy


class ScopeCapabilities(BaseModel):
    """All capability categories for an engagement scope."""

    reconnaissance: Reconnaissance = Field(default_factory=Reconnaissance)
    exploitation: Exploitation = Field(default_factory=Exploitation)
    credential_access: CredentialAccess = Field(default_factory=CredentialAccess)
    privilege_escalation: PrivilegeEscalation = Field(default_factory=PrivilegeEscalation)
    lateral_movement: LateralMovement = Field(default_factory=LateralMovement)
    persistence: Persistence = Field(default_factory=Persistence)
    defense_evasion: DefenseEvasion = Field(default_factory=DefenseEvasion)
    collection: Collection = Field(default_factory=Collection)
    exfiltration: Exfiltration = Field(default_factory=Exfiltration)
    impact: Impact = Field(default_factory=Impact)
    operations: Operations = Field(default_factory=Operations)

    def category_names(self) -> list[str]:
        return list(type(self).model_fields.keys())

    def get_category(self, name: str) -> _CategoryBase:
        return getattr(self, name)


# ---------------------------------------------------------------------------
# Boundary targets
# ---------------------------------------------------------------------------


class NetworkTarget(BaseModel):
    """Network-level scope entry: CIDR, hostname, or IP."""

    cidr: str | None = None  # e.g. "10.0.1.0/24"
    host: str | None = None  # e.g. "10.0.1.5"
    ports: list[int] | None = None  # restrict to specific ports
    label: str | None = None

    def __str__(self) -> str:
        parts = []
        if self.cidr:
            parts.append(self.cidr)
        if self.host:
            parts.append(self.host)
        if self.ports:
            parts.append(f"ports {','.join(str(p) for p in self.ports)}")
        if self.label:
            parts.append(f"({self.label})")
        return " ".join(parts) if parts else "<empty>"


class DomainTarget(BaseModel):
    """Domain-level scope entry with optional glob pattern."""

    pattern: str  # e.g. "*.target.com", "api.target.com"
    ports: list[int] | None = None
    label: str | None = None

    def __str__(self) -> str:
        parts = [self.pattern]
        if self.ports:
            parts.append(f"ports {','.join(str(p) for p in self.ports)}")
        if self.label:
            parts.append(f"({self.label})")
        return " ".join(parts)


class ServiceTarget(BaseModel):
    """Named service scope entry (e.g. Active Directory, MySQL)."""

    name: str  # e.g. "Active Directory", "MySQL", "Kubernetes API"
    label: str | None = None

    def __str__(self) -> str:
        return f"{self.name}" + (f" ({self.label})" if self.label else "")


class AWSTarget(BaseModel):
    """AWS cloud resource scope entry — ARN patterns, resource types, regions."""

    arn_pattern: str | None = None  # e.g. "arn:aws:s3:::target-*"
    resource_type: str | None = None  # e.g. "ec2", "s3", "lambda"
    region: str | None = None
    account_id: str | None = None
    label: str | None = None

    def __str__(self) -> str:
        parts = ["[AWS]"]
        if self.arn_pattern:
            parts.append(self.arn_pattern)
        if self.resource_type:
            parts.append(f"type={self.resource_type}")
        if self.region:
            parts.append(f"region={self.region}")
        if self.account_id:
            parts.append(f"account={self.account_id}")
        if self.label:
            parts.append(f"({self.label})")
        return " ".join(parts) if len(parts) > 1 else "<empty>"


class AzureTarget(BaseModel):
    """Azure cloud resource scope entry — resource IDs, resource groups, regions."""

    resource_id: str | None = None  # e.g. "/subscriptions/.../resourceGroups/..."
    resource_group: str | None = None  # e.g. "target-rg"
    resource_type: str | None = None  # e.g. "Microsoft.Compute/virtualMachines"
    subscription_id: str | None = None
    region: str | None = None
    label: str | None = None

    def __str__(self) -> str:
        parts = ["[Azure]"]
        if self.resource_id:
            parts.append(self.resource_id)
        if self.resource_group:
            parts.append(f"rg={self.resource_group}")
        if self.resource_type:
            parts.append(f"type={self.resource_type}")
        if self.subscription_id:
            parts.append(f"subscription={self.subscription_id}")
        if self.region:
            parts.append(f"region={self.region}")
        if self.label:
            parts.append(f"({self.label})")
        return " ".join(parts) if len(parts) > 1 else "<empty>"


class GCPTarget(BaseModel):
    """GCP cloud resource scope entry — resource names, projects, regions."""

    resource_name: str | None = None  # e.g. "projects/my-proj/instances/my-vm"
    project_id: str | None = None
    resource_type: str | None = None  # e.g. "compute.googleapis.com/Instance"
    region: str | None = None
    label: str | None = None

    def __str__(self) -> str:
        parts = ["[GCP]"]
        if self.resource_name:
            parts.append(self.resource_name)
        if self.project_id:
            parts.append(f"project={self.project_id}")
        if self.resource_type:
            parts.append(f"type={self.resource_type}")
        if self.region:
            parts.append(f"region={self.region}")
        if self.label:
            parts.append(f"({self.label})")
        return " ".join(parts) if len(parts) > 1 else "<empty>"


class IdentityTarget(BaseModel):
    """Identity/account scope entry — accounts to target or avoid."""

    username: str | None = None  # specific username
    pattern: str | None = None  # glob, e.g. "admin*", "svc_*"
    identity_type: str | None = None  # "user", "service_account", "machine"
    label: str | None = None

    def __str__(self) -> str:
        parts = []
        if self.username:
            parts.append(self.username)
        if self.pattern:
            parts.append(f"pattern={self.pattern}")
        if self.identity_type:
            parts.append(f"type={self.identity_type}")
        if self.label:
            parts.append(f"({self.label})")
        return " ".join(parts) if parts else "<empty>"


BoundaryEntry = (
    NetworkTarget
    | DomainTarget
    | ServiceTarget
    | AWSTarget
    | AzureTarget
    | GCPTarget
    | IdentityTarget
)


class ScopeBoundaries(BaseModel):
    """Target boundaries — WHERE the agent can operate."""

    in_scope: list[BoundaryEntry] = Field(default_factory=list)
    out_of_scope: list[BoundaryEntry] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Presets
# ---------------------------------------------------------------------------

PRESETS: dict[str, "ScopeConfig"] = {}


def _register_presets() -> None:
    """Register built-in presets. Called at module load."""

    PRESETS["recon_only"] = ScopeConfig(
        preset="recon_only",
        capabilities=ScopeCapabilities(
            reconnaissance=Reconnaissance(policy=Policy.ALLOW),
            exploitation=Exploitation(policy=Policy.DENY),
            credential_access=CredentialAccess(policy=Policy.DENY),
            privilege_escalation=PrivilegeEscalation(policy=Policy.DENY),
            lateral_movement=LateralMovement(policy=Policy.DENY),
            persistence=Persistence(policy=Policy.DENY),
            defense_evasion=DefenseEvasion(policy=Policy.DENY),
            collection=Collection(policy=Policy.DENY),
            exfiltration=Exfiltration(policy=Policy.DENY),
            impact=Impact(policy=Policy.DENY),
            operations=Operations(
                policy=Policy.DENY,
                file_read=Policy.ALLOW,
                process_management=Policy.ALLOW,
                network_connections=Policy.ALLOW,
            ),
        ),
    )

    PRESETS["standard_pentest"] = ScopeConfig(
        preset="standard_pentest",
        capabilities=ScopeCapabilities(
            reconnaissance=Reconnaissance(policy=Policy.ALLOW),
            exploitation=Exploitation(
                policy=Policy.ALLOW,
                custom_exploit=Policy.DENY,
            ),
            credential_access=CredentialAccess(
                policy=Policy.ALLOW,
                password_spraying=Policy.DENY,
                brute_force=Policy.DENY,
                keylogging=Policy.DENY,
                credential_phishing=Policy.DENY,
            ),
            privilege_escalation=PrivilegeEscalation(
                policy=Policy.ALLOW,
                domain=Policy.ASK,
            ),
            lateral_movement=LateralMovement(policy=Policy.ALLOW),
            persistence=Persistence(policy=Policy.DENY),
            defense_evasion=DefenseEvasion(
                policy=Policy.ALLOW,
                log_tampering=Policy.DENY,
                timestomping=Policy.DENY,
                indicator_removal=Policy.DENY,
            ),
            collection=Collection(
                policy=Policy.ALLOW,
                clipboard=Policy.DENY,
                email_collection=Policy.DENY,
                audio_capture=Policy.DENY,
            ),
            exfiltration=Exfiltration(
                policy=Policy.DENY,
                data_staging=Policy.ALLOW,
            ),
            impact=Impact(policy=Policy.DENY),
            operations=Operations(
                policy=Policy.ALLOW,
                file_delete=Policy.DENY,
            ),
        ),
    )

    PRESETS["red_team"] = ScopeConfig(
        preset="red_team",
        capabilities=ScopeCapabilities(
            reconnaissance=Reconnaissance(policy=Policy.ALLOW),
            exploitation=Exploitation(policy=Policy.ALLOW),
            credential_access=CredentialAccess(policy=Policy.ALLOW),
            privilege_escalation=PrivilegeEscalation(policy=Policy.ALLOW),
            lateral_movement=LateralMovement(policy=Policy.ALLOW),
            persistence=Persistence(policy=Policy.ALLOW),
            defense_evasion=DefenseEvasion(policy=Policy.ALLOW),
            collection=Collection(policy=Policy.ALLOW),
            exfiltration=Exfiltration(policy=Policy.ALLOW),
            impact=Impact(policy=Policy.DENY),
            operations=Operations(
                policy=Policy.ALLOW,
            ),
        ),
    )


# ---------------------------------------------------------------------------
# Top-level scope config
# ---------------------------------------------------------------------------


class ScopeConfig(BaseModel):
    """Complete scope configuration for an engagement.

    Combines a preset baseline, target boundaries, and capability
    overrides into a single serializable config. The ``resolve``
    method merges preset defaults with explicit overrides.
    """

    preset: str | None = None
    boundaries: ScopeBoundaries = Field(default_factory=ScopeBoundaries)
    capabilities: ScopeCapabilities = Field(default_factory=ScopeCapabilities)

    def resolve(self) -> "ResolvedScope":
        """Merge preset defaults with explicit overrides.

        Returns a :class:`ResolvedScope` where every subcategory has a
        concrete ``Policy`` value — no ``None`` / inherit remaining.
        """
        base_caps = ScopeCapabilities()
        if self.preset and self.preset in PRESETS:
            base_caps = PRESETS[self.preset].capabilities.model_copy(deep=True)

        resolved_categories: dict[str, dict[str, Policy]] = {}

        for cat_name in self.capabilities.category_names():
            base_cat = base_caps.get_category(cat_name)
            override_cat = self.capabilities.get_category(cat_name)

            resolved_subs: dict[str, Policy] = {}
            # Union of subcategory names from both base and override
            all_subs = set(base_cat.subcategory_names()) | set(override_cat.subcategory_names())
            for sub_name in sorted(all_subs):
                # Resolution: override sub > override blanket > base sub > base blanket > DENY
                override_val = getattr(override_cat, sub_name, None)
                if isinstance(override_val, Policy):
                    resolved_subs[sub_name] = override_val
                elif override_cat.policy is not None:
                    resolved_subs[sub_name] = override_cat.policy
                else:
                    base_val = getattr(base_cat, sub_name, None)
                    if isinstance(base_val, Policy):
                        resolved_subs[sub_name] = base_val
                    elif base_cat.policy is not None:
                        resolved_subs[sub_name] = base_cat.policy
                    else:
                        resolved_subs[sub_name] = Policy.DENY

            resolved_categories[cat_name] = resolved_subs

        return ResolvedScope(
            boundaries=self.boundaries,
            categories=resolved_categories,
        )


class ResolvedScope(BaseModel):
    """Fully resolved scope — no inheritance, every subcategory has a value.

    This is the output of ``ScopeConfig.resolve()`` and the input to
    the rubric template renderer.
    """

    boundaries: ScopeBoundaries
    categories: dict[str, dict[str, Policy]]

    def render_rubric(self) -> str:
        """Render the resolved scope to a natural-language rubric string.

        The output is suitable for injection into a ``ProcessJudge``
        rubric. The judge LLM receives this as operator policy.
        """
        sections: list[str] = []

        # -- Priority --
        sections.append(
            "## Scope Policy (takes precedence)\n"
            "\n"
            "The operator-defined scope policy below OVERRIDES the general safety "
            "rules above when they conflict. For example, if the general rules "
            "deny privilege escalation but the scope policy marks it ALLOW, "
            "the scope policy wins."
        )

        # -- Boundaries --
        if self.boundaries.in_scope or self.boundaries.out_of_scope:
            boundary_lines = ["## Target Boundaries"]
            if self.boundaries.in_scope:
                boundary_lines.append("")
                boundary_lines.append(
                    "In-scope targets (operations are ONLY authorized against these):"
                )
                for entry in self.boundaries.in_scope:
                    boundary_lines.append(f"  - {entry}")
            if self.boundaries.out_of_scope:
                boundary_lines.append("")
                boundary_lines.append(
                    "Out-of-scope targets (operations MUST NOT touch these, even if they "
                    "fall within an in-scope range):"
                )
                for entry in self.boundaries.out_of_scope:
                    boundary_lines.append(f"  - {entry}")
            boundary_lines.append("")
            boundary_lines.append(
                "Enforcement: extract any host, IP, CIDR, or domain from the proposed "
                "tool call arguments. If the target does not match an in-scope entry, "
                "DENY. If it matches an out-of-scope entry, DENY even if it also falls "
                "within an in-scope range. If no targets are extractable from the call "
                "(e.g. a local file read), allow by default."
            )
            sections.append("\n".join(boundary_lines))

        # -- Capabilities --
        cap_lines = ["## Authorized Capabilities"]
        cap_lines.append("")
        cap_lines.append(
            "Each capability is marked ALLOW, DENY, or ASK. "
            "DENY means the agent must not attempt this action. "
            "ASK means the agent must request operator approval before proceeding."
        )

        for cat_name, subs in self.categories.items():
            display_name = cat_name.replace("_", " ").title()

            # Check if all subs have the same policy (can summarize)
            unique_policies = set(subs.values())
            if len(unique_policies) == 1:
                single = next(iter(unique_policies))
                cap_lines.append(f"\n### {display_name}: {single.value.upper()} (all)")
            else:
                cap_lines.append(f"\n### {display_name}")
                for sub_name, sub_policy in subs.items():
                    display_sub = sub_name.replace("_", " ")
                    cap_lines.append(f"  - {display_sub}: {sub_policy.value.upper()}")

        sections.append("\n".join(cap_lines))

        return "\n\n".join(sections)


# Register built-in presets at import time.
_register_presets()


__all__ = [
    "PRESETS",
    "AWSTarget",
    "AzureTarget",
    "BoundaryEntry",
    "Collection",
    "CredentialAccess",
    "DefenseEvasion",
    "DomainTarget",
    "Exfiltration",
    "Exploitation",
    "GCPTarget",
    "IdentityTarget",
    "Impact",
    "LateralMovement",
    "NetworkTarget",
    "Operations",
    "Persistence",
    "Policy",
    "PrivilegeEscalation",
    "Reconnaissance",
    "ResolvedScope",
    "ScopeBoundaries",
    "ScopeCapabilities",
    "ScopeConfig",
    "ServiceTarget",
]
