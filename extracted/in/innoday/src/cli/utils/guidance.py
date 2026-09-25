"""What to tell someone who is signed out, holds a dead token, or is outside a
workspace -- one wording each, so every command gives the same next step
(PF-460). Before this, a new user saw "run 'innoday config init'" (wrong since
PF-456), a bare "HTTP 401", or "Organization ID not found".
"""

NOT_SIGNED_IN = (
    "You're not signed in. Run `innoday login`. "
    "(No account yet? Accounts are by invitation — ask your InnoDay admin.)"
)

IDENTITY_NOT_CACHED = (
    "This machine doesn't know who you are yet. Run `innoday whoami` to "
    "refresh your identity, or `innoday login` if you haven't signed in."
)

SIGN_IN_REJECTED = (
    "Your sign-in has expired or isn't valid. Run `innoday login` to sign in again."
)

OPERATOR_ONLY = (
    "This needs the team secret: it is a platform-admin operation. Operators "
    "use `scripts/bootstrap_cli.py` in the innoday repo."
)

NO_PROJECT = (
    "No InnoDay project here. Run this from a workspace "
    "(`innoday init <org>/<project>`), or pass --org/--project."
)


def org_not_found(ref: str) -> str:
    return (
        f"No organization '{ref}' that you can reach. Check the alias "
        "(`innoday orgs list`), or ask its admin to invite you."
    )
