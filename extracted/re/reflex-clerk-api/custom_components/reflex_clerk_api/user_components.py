import reflex as rx

from reflex_clerk_api.base import ClerkBase
from reflex_clerk_api.models import Appearance


class UserButton(ClerkBase):
    tag = "UserButton"

    after_switch_session_url: str | None = None
    "The full URL or path to navigate to after a successful account change in a multi-session app."

    # NOTE: `apperance.base_theme` does not work yet.
    appearance: Appearance | None = None
    """Optional object to style your components. Will only affect Clerk components."""

    default_open: bool | None = None
    "Controls whether the <UserButton /> should open by default during the first render."

    show_name: bool | None = None
    "Controls if the user name is displayed next to the user image button."

    sign_in_url: str | None = None
    "The full URL or path to navigate to when the Add another account button is clicked. It's recommended to use the environment variable instead."

    user_profile_mode: str | None = None
    "Controls whether selecting the Manage your account button will cause the <UserProfile /> component to open as a modal, or if the browser will navigate to the userProfileUrl where <UserProfile /> is mounted as a page. Defaults to: 'modal'."

    user_profile_props: dict | None = None
    "Specify options for the underlying <UserProfile /> component. For example: {additionalOAuthScopes: {google: ['foo', 'bar'], github: ['qux']}}."

    user_profile_url: str | None = None
    "The full URL or path leading to the user management interface."

    fallback: rx.Component | None = None
    "An optional element to be rendered while the component is mounting."


class UserProfile(ClerkBase):
    tag = "UserProfile"

    appearance: Appearance | None = None
    """Optional object to style your components. Will only affect Clerk components."""

    routing: str | None = None
    "The routing strategy for your pages. Defaults to 'path' for frameworks that handle routing, such as Next.js and Remix. Defaults to hash for all other SDK's, such as React."

    path: str | None = None
    "The path where the component is mounted on when routing is set to path. It is ignored in hash-based routing. For example: /user-profile."

    additional_oauth_scopes: dict | None = None
    "Specify additional scopes per OAuth provider that your users would like to provide if not already approved. For example: {google: ['foo', 'bar'], github: ['qux']}."

    fallback: rx.Component | None = None
    "An optional element to be rendered while the component is mounting."


user_button = UserButton.create
user_profile = UserProfile.create
