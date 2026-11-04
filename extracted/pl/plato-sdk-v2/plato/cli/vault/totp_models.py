"""Models for `plato vault totp`: authenticator-app 2FA (TOTP) per vault account.

The login vault keeps the TOTP seed (field ``totp_seed``). The vault has no
notes field, so backup codes go to a local store on this machine (mode 600).

Secrets are ``SecretStr``: they print as ``**********``. Only the stores and the
vault write reveal them. What a command prints goes through
:class:`TotpEnrollReport` (lengths and counts only, never a prefix of a seed).
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, SecretStr, SerializationInfo, field_serializer

from plato.cli.vault.prompts import GoalTemplate
from plato.cli.vault.sign_in_models import CANVA_SIGN_IN, SignInRecipe

# The only TOTP parameters the login vault and the login world support: the vault
# keeps the seed only, and the login world computes 6 digits, 30 s, SHA1.
VAULT_DIGITS = 6
VAULT_PERIOD_S = 30


class TotpVendor(StrEnum):
    canva = "canva"


class TotpAlgorithm(StrEnum):
    """RFC 6238 hash functions. The vault path takes SHA1 only (see VAULT_DIGITS)."""

    sha1 = "SHA1"
    sha256 = "SHA256"
    sha512 = "SHA512"


class NeedPersonReason(StrEnum):
    """Why the setup agent stopped for a person. The agent never types these."""

    password = "password"
    email_code = "email_code"
    login = "login"


class KeySource(StrEnum):
    """Where code read the seed: an ``otpauth://`` URI in the DOM, or the shown text key."""

    otpauth = "otpauth"
    text = "text"


class AccountMatch(StrEnum):
    """The signed-in check before the setup: is the browser signed in as the vault account?
    Only ``match`` lets the setup start."""

    match = "match"  # the page shows the vault item's email, and no other account email
    mismatch = "mismatch"  # the page shows another email, not the vault item's
    ambiguous = "ambiguous"  # the page shows the vault item's email AND another one
    unknown = "unknown"  # the page shows no email (a sign-in page, or a page that hides it)
    no_vault_email = "no_vault_email"  # the vault item's username is not an email


class CodeResult(StrEnum):
    """What the page did after code typed the 6-digit code and clicked the confirm button."""

    accepted = "accepted"  # the backup-codes step or the finish button is visible
    # an error text that is NEW after the click, while the code step is still open
    rejected = "rejected"
    unknown = "unknown"  # neither (the window closed, moved on, or showed no clear answer)


class TotpRecipe(BaseModel):
    """Everything vendor-specific about one vendor's authenticator-app setup. Data, not
    code: a second vendor is a second recipe. Texts are matched case-insensitively on
    the trimmed text (or ``aria-label``) of buttons, links and ``[role=button]``."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    vendor: TotpVendor
    settings_url: str
    # The pages where code reads the signed-in account's email before the setup starts,
    # in order (the first page that shows an email decides). The settings page comes
    # first: it is open anyway.
    account_urls: list[str]
    # Emails at these domains are the vendor's own (support, privacy) and never an account.
    vendor_email_domains: list[str]
    # The setup agent's goal ($space_id, $settings_url, $no_files): a template file in
    # cli/vault/prompts/. It ends BEFORE the key is shown: code reveals and reads the
    # key, so no model sees it.
    agent_template: GoalTemplate
    # The same goal for `--browser pi` (the `computer` screen tools only):
    # $settings_url and $screen_rule.
    pi_agent_template: GoalTemplate
    # Buttons or links that show the text key behind the QR code. Code clicks one.
    reveal_texts: list[str]
    # A shown text key (base32; groups of 4 with spaces or dashes are allowed).
    key_pattern: str
    # The code input: CSS selectors tried in order; else `digits` one-character boxes.
    code_input_selectors: list[str]
    confirm_button: str
    # Button names that show the code was accepted (the backup-codes step of the setup
    # window). Buttons only: the settings page behind the window can show the same words.
    accepted_buttons: list[str]
    # Texts in the setup window (``[role=dialog]``) that show the code was refused.
    error_texts: list[str]
    # One backup code (a leaf text in the setup window). Read by code, never printed.
    backup_code_pattern: str
    backup_codes_min: int
    backup_codes_max: int
    finish_button: str
    # The vendor's sign-in pages: code fills them from the vault item (cli/vault/sign_in.py).
    sign_in: SignInRecipe
    digits: int = VAULT_DIGITS
    period_s: int = VAULT_PERIOD_S
    algorithm: TotpAlgorithm = TotpAlgorithm.sha1


class TotpParams(BaseModel):
    """The TOTP parameters of a seed (from its otpauth URI, else the recipe's)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    digits: int = VAULT_DIGITS
    period_s: int = VAULT_PERIOD_S
    algorithm: TotpAlgorithm = TotpAlgorithm.sha1
    issuer: str | None = None

    def vault_ok(self) -> bool:
        """The vault keeps only the seed, so only the login world's defaults can work."""
        return self.digits == VAULT_DIGITS and self.period_s == VAULT_PERIOD_S and self.algorithm == TotpAlgorithm.sha1


class KeyCandidates(BaseModel):
    """What the reveal script writes to the private temp file, read back once and deleted."""

    model_config = ConfigDict(extra="forbid")

    uris: list[SecretStr] = Field(default_factory=list)
    keys: list[SecretStr] = Field(default_factory=list)


class TotpKey(BaseModel):
    """The seed that code read, with its parameters. Never print it."""

    model_config = ConfigDict(extra="forbid")

    seed: SecretStr
    params: TotpParams
    source: KeySource


class BackupCodesFile(BaseModel):
    """What the backup-codes script writes to the private temp file."""

    model_config = ConfigDict(extra="forbid")

    codes: list[SecretStr] = Field(default_factory=list)


class BackupCodesRecord(BaseModel):
    """The local record of an account's backup codes (mode 600). Never print it."""

    model_config = ConfigDict(extra="forbid")

    vendor: TotpVendor
    login_key: str
    account: str
    codes: list[SecretStr]
    saved_at: datetime

    @field_serializer("codes")
    def _reveal(self, value: list[SecretStr], info: SerializationInfo) -> list[str]:
        """Plain text only for the store (``context={"reveal": True}``); masked otherwise."""
        if info.context and info.context.get("reveal"):
            return [v.get_secret_value() for v in value]
        return [str(v) for v in value]


class PendingSeedFile(BaseModel):
    """The local copy of a seed between the code step and the vault write.

    Its JSON is exactly ``{"totp_seed": "..."}``, so a person can save it with
    ``plato vault edit <login_key> -a <account> --creds-stdin < <file>``."""

    model_config = ConfigDict(extra="forbid")

    totp_seed: SecretStr

    @field_serializer("totp_seed")
    def _reveal(self, value: SecretStr, info: SerializationInfo) -> str:
        if info.context and info.context.get("reveal"):
            return value.get_secret_value()
        return str(value)


class VaultTotpState(BaseModel):
    """What the login vault holds for the account, read before the setup starts."""

    model_config = ConfigDict(extra="forbid")

    login_key: str
    account: str
    archived: bool
    seed: SecretStr | None = None
    # Who made the item (``user:<email>``, ``run:<session>``, ``org-key:<digest>``). An
    # org-wide key may edit only the items a run or an org-wide key made.
    created_by: str | None = None
    # The no-change PATCH that checks the edit right sends this value back.
    login_url: str | None = None
    # The account's sign-in name; for Canva its email. The signed-in check compares it with
    # the email the vendor's page shows.
    username: str | None = None
    # The account password: code types it at a sign-in prompt (cli/vault/sign_in.py).
    password: SecretStr | None = None

    @property
    def has_seed(self) -> bool:
        return self.seed is not None and bool(self.seed.get_secret_value())


class SignedInCheck(BaseModel):
    """What the signed-in check found. Emails are not secrets: the error names them, so a
    person sees which account the browser holds."""

    model_config = ConfigDict(extra="forbid")

    result: AccountMatch
    expected: str | None  # the vault item's username, case-folded
    found: list[str] = Field(default_factory=list)  # the account emails on the page, case-folded
    page: str | None = None  # the page that showed them (None: no page showed one)


class TotpPlan(BaseModel):
    """`enroll --dry-run` output. Nothing ran."""

    model_config = ConfigDict(extra="forbid")

    vendor: TotpVendor
    login_key: str
    account: str
    settings_url: str
    replace: bool
    steps: list[str]
    backup_codes_store: str
    pending_seed_file: str


class TotpEnrollReport(BaseModel):
    """`enroll` output: lengths, counts and paths only. No seed, no code, no backup code."""

    model_config = ConfigDict(extra="forbid")

    vendor: TotpVendor
    login_key: str
    account: str
    space_id: int | None
    key_source: KeySource
    seed_len: int
    code_result: CodeResult
    code_attempts: int
    seed_saved: bool
    backup_codes_saved: int
    backup_codes_path: str | None
    setup_finished: bool
    # The TaskSpace stays open for a person (a password prompt, or backup codes to copy).
    handed_off: bool = False
    check: str
    # The email the vendor's page showed before the setup started (= the vault item's username).
    signed_in_as: str


class TotpCodeReport(BaseModel):
    """`code` output. ``code`` IS the secret this command exists to print."""

    model_config = ConfigDict(extra="forbid")

    login_key: str
    account: str
    code: str
    valid_for_s: int


# Canva: not yet checked on the live page.

CANVA_TOTP = TotpRecipe(
    vendor=TotpVendor.canva,
    settings_url="https://www.canva.com/settings/login-and-security",
    # Not yet checked on the live page: if neither page shows the email, the check stops
    # with "unknown" and nothing changes.
    account_urls=["https://www.canva.com/settings/login-and-security", "https://www.canva.com/settings/your-account"],
    vendor_email_domains=["canva.com"],
    agent_template=GoalTemplate.canva_totp,
    pi_agent_template=GoalTemplate.canva_pi_totp,
    reveal_texts=["Show secret key", "Can't scan the QR code?", "Enter this key", "Show key"],
    key_pattern=r"^[A-Za-z2-7]{4}(?:[ -]?[A-Za-z2-7]{4}){3,}[A-Za-z2-7]{0,3}=*$",
    code_input_selectors=[
        "input[autocomplete='one-time-code']",
        "input[inputmode='numeric']",
        "input[maxlength='6']",
        "input[type='tel']",
        "input[type='text']",
    ],
    confirm_button="Enable authenticator app",
    accepted_buttons=["Copy codes", "Finish setup"],
    error_texts=["incorrect", "invalid", "try again", "doesn't match", "wrong code"],
    backup_code_pattern=r"^(?=.*[0-9])(?:[A-Za-z0-9]{8,12}|[A-Za-z0-9]{4,6}[- ][A-Za-z0-9]{4,6})$",
    backup_codes_min=4,
    backup_codes_max=20,
    finish_button="Finish setup",
    sign_in=CANVA_SIGN_IN,
)

TOTP_RECIPES: dict[TotpVendor, TotpRecipe] = {TotpVendor.canva: CANVA_TOTP}
