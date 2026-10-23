"""Models for the code sign-in step (:mod:`sign_in`), shared by `plato vault app consent`
and `plato vault totp enroll`.

Secrets are ``SecretStr``: they print as ``**********``. Only the fill step in
:mod:`sign_in` reveals them, and only into the page's input, never into a model's
prompt, a log or an exception.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, SecretStr


class SignInStep(StrEnum):
    """What the page asks for, read by code from the fields on the page (never from a model)."""

    email = "email"  # one visible email (or username) input on a sign-in page
    password = "password"  # exactly one visible password input
    totp = "totp"  # a one-time-code input next to authenticator-app text
    email_code = "email_code"  # a one-time-code input for a code that the vendor sent by email
    entry = "entry"  # a sign-in page with no field yet, and a button that opens the email form
    none = "none"  # no sign-in prompt on the page


class OnEmailCode(StrEnum):
    """``--on-email-code``: code cannot read the inbox yet, so an email code needs a person."""

    person = "person"  # hand the window to a person and wait while they type the code
    stop = "stop"  # stop the command; nothing was typed


class SignInRecipe(BaseModel):
    """Everything vendor-specific about the vendor's sign-in pages. Data, not code.
    Texts are matched case-insensitively."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    # The vendor's hosts (a host is one of them or a subdomain of one), over https only.
    # Code fills nothing on any other page: a "Continue with Google" click by the agent
    # leads to a Google sign-in page with an email and a password field of its own.
    hosts: list[str]
    # Code fills a field only on a page whose path holds one of these. A settings page
    # can show the account email in an input, and its dialogs ask for the password or a
    # code to delete the account or to turn 2FA off: code must never submit those. A
    # caller that knows a re-sign-in prompt can show on another page names that path
    # itself (``sign_in(reauth_paths=...)``), for the password and code steps only.
    sign_in_paths: list[str]
    # Buttons code clicks after it fills a field (exact accessible name). Never a word that
    # also ends a destructive dialog ("Confirm", "Done", "Delete", "Turn off"): the same
    # fill on such a dialog would then delete the account or turn 2FA off.
    submit_buttons: list[str]
    # Extra submit buttons on a re-sign-in page only (``sign_in(reauth_paths=...)``), never
    # on a sign-in page: the vendor's re-sign-in dialog before a 2FA change.
    reauth_submit_buttons: list[str] = Field(default_factory=list)
    # Buttons that open the email form on a sign-in page with no field yet.
    entry_buttons: list[str]
    # Page texts that mark a one-time-code input as the authenticator app's.
    authenticator_texts: list[str]
    # Page texts that mark a one-time-code input as a code the vendor sent by email.
    email_code_texts: list[str]
    # Page texts of a destructive dialog (delete the account, turn 2FA off). A page that
    # shows one asks for nothing: code fills no field there, on any path. When every value
    # field sits in one open dialog, only that dialog's text counts: the settings page
    # under a re-sign-in dialog always shows "Delete your account".
    danger_texts: list[str] = Field(default_factory=list)
    # Account emails at these domains are the vendor's own (support, privacy), never the
    # signed-in account: the other-account check leaves them out.
    vendor_email_domains: list[str] = Field(default_factory=list)
    digits: int = 6


class SignInSecrets(BaseModel):
    """The vault item's sign-in values. Read only when a prompt shows. Never print it."""

    model_config = ConfigDict(extra="forbid")

    username: str | None = None
    password: SecretStr | None = None
    totp_seed: SecretStr | None = None


class SignInProbe(BaseModel):
    """What the detect script found on the page: counts, the path and two text flags.
    No value of any input."""

    model_config = ConfigDict(extra="ignore")

    path: str = ""
    # location.hostname over https, else "" (code fills nothing on an http page).
    host: str = ""
    # The account emails that a person can see on the page (totp_portal.SIGNED_IN_EMAILS_JS).
    # Not a secret. Code types a password or a code only when the vault username is one of
    # them, or when the page shows none.
    emails: list[str] = Field(default_factory=list)
    email: int = 0  # visible, enabled email or username inputs
    email_empty: int = 0  # of those, the empty ones
    password: int = 0  # visible, enabled password inputs
    otp: int = 0  # visible one-time-code inputs (autocomplete=one-time-code)
    otp_boxes: int = 0  # visible one-character boxes
    entry: int = 0  # visible entry buttons (SignInRecipe.entry_buttons)
    authenticator_text: bool = False
    email_code_text: bool = False
    danger_text: bool = False  # the page (or the open dialog that holds the field) shows a danger text


class SignInFill(BaseModel):
    """What the fill script did: counts and flags only, never the value."""

    model_config = ConfigDict(extra="ignore")

    filled: bool = False
    submitted: bool = False
    inputs: int = 0
    error: str | None = None


class SignInReport(BaseModel):
    """What the sign-in step did. No secret: the steps and who did them."""

    model_config = ConfigDict(extra="forbid")

    filled: list[SignInStep] = Field(default_factory=list)  # the steps code filled, in order
    person: list[SignInStep] = Field(default_factory=list)  # the steps a person did
    entry_clicks: int = 0
    # The path of the page after the step (never its query: an OAuth URL holds state there).
    path: str = ""

    @property
    def acted(self) -> bool:
        return bool(self.filled or self.person or self.entry_clicks)


# The field types are the standard ones, so a change of the button names is the main risk.

CANVA_SIGN_IN = SignInRecipe(
    hosts=["canva.com"],
    sign_in_paths=["/login", "/signup", "/signin", "/sign-in", "/oauth"],
    submit_buttons=["Continue", "Log in", "Sign in", "Next", "Verify", "Submit"],
    reauth_submit_buttons=["Confirm Password"],  # "Confirm your existing password" before the MFA setup
    entry_buttons=["Continue with email", "Log in with email", "Sign in with email", "Continue with work email"],
    authenticator_texts=["authenticator", "authentication app", "2-step", "two-step", "two-factor"],
    email_code_texts=[
        "sent a code",
        "sent you a code",
        "check your email",
        "code to your email",
        "we emailed",
        "sent to",
    ],
    danger_texts=[
        "delete your account",
        "delete account",
        "turn off two-step",
        "turn off 2-step",
        "turn off two-factor",
        "disable two-step",
        "remove the authenticator",
    ],
    vendor_email_domains=["canva.com"],
)
