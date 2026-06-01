from reflex_clerk_api.base import ClerkBase


class SignIn(ClerkBase):
    tag = "SignIn"

    path: str


class SignUp(ClerkBase):
    tag = "SignUp"

    path: str


sign_in = SignIn.create
sign_up = SignUp.create
