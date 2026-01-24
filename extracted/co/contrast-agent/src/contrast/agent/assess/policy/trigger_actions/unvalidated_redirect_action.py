# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from contrast.agent.assess.policy.trigger_actions.default_action import DefaultAction
from contrast.utils.stack_trace_utils import build_stack


class StarletteRedirectAction(DefaultAction):
    """
    Custom trigger action that implements unvalidated redirect rule logic for Starlette.
    """

    def is_violated(self, source, required_tags, disallowed_tags, **kwargs):
        if super().is_violated(source, required_tags, disallowed_tags, **kwargs):
            if call_frames := build_stack(limit=1):
                frame = call_frames[0]
                if (
                    frame.name == "app"
                    and frame.filename.endswith("/starlette/routing.py")
                    and frame.line
                    == "response = RedirectResponse(url=str(redirect_url))"
                ):
                    # Don't report unvalidated-redirect for routing.Router.redirect_slash behavior
                    # https://github.com/Kludex/starlette/blob/49d4de92867cb38a781069701ad57cecab4a1a36/starlette/routing.py#L750-L764
                    return False
            return True

        return False
