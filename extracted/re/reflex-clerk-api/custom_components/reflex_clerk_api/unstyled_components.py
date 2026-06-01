from reflex_clerk_api.base import ClerkBase


class SignUpButton(ClerkBase):
    tag = "SignUpButton"

    force_redirect_url: str | None = None
    "If provided, this URL will always be redirected to after the user signs up. It's recommended to use the environment variable instead."

    fallback_redirect_url: str | None = None
    "The fallback URL to redirect to after the user signs up, if there's no redirect_url in the path already. Defaults to /. It's recommended to use the environment variable instead."

    sign_in_force_redirect_url: str | None = None
    "If provided, this URL will always be redirected to after the user signs in. It's recommended to use the environment variable instead."

    sign_in_fallback_redirect_url: str | None = None
    "The fallback URL to redirect to after the user signs in, if there's no redirect_url in the path already. Defaults to /. It's recommended to use the environment variable instead."

    mode: str | None = None
    "Determines what happens when a user clicks on the <SignUpButton>. Setting this to 'redirect' will redirect the user to the sign-up route. Setting this to 'modal' will open a modal on the current route. Defaults to 'redirect'."


class SignInButton(ClerkBase):
    tag = "SignInButton"

    force_redirect_url: str | None = None
    "If provided, this URL will always be redirected to after the user signs in. It's recommended to use the environment variable instead."

    fallback_redirect_url: str | None = None
    "The fallback URL to redirect to after the user signs in, if there's no redirect_url in the path already. Defaults to /. It's recommended to use the environment variable instead."

    sign_up_force_redirect_url: str | None = None
    "If provided, this URL will always be redirected to after the user signs up. It's recommended to use the environment variable instead."

    sign_up_fallback_redirect_url: str | None = None
    "The fallback URL to redirect to after the user signs up, if there's no redirect_url in the path already. Defaults to /. It's recommended to use the environment variable instead."

    mode: str | None = None
    "Determines what happens when a user clicks on the <SignInButton>. Setting this to 'redirect' will redirect the user to the sign-in route. Setting this to 'modal' will open a modal on the current route. Defaults to 'redirect'."


class SignOutButton(ClerkBase):
    tag = "SignOutButton"

    redirect_url: str | None = None
    "The full URL or path to navigate after successful sign-out."


sign_up_button = SignUpButton.create
sign_in_button = SignInButton.create
sign_out_button = SignOutButton.create
