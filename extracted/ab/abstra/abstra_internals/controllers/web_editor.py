from typing import Optional

from abstra_internals.contracts_generated import AbstraLibApiEditorWebEditorResponse
from abstra_internals.environment import EDITOR_MODE, WAITING_ROOM_URL
from abstra_internals.services.api_key_status import ApiKeyStatus


class WebEditorController:
    def inspect(self) -> AbstraLibApiEditorWebEditorResponse:
        return AbstraLibApiEditorWebEditorResponse(
            waiting_room_url=WAITING_ROOM_URL,
            # False means this pod's API key was revoked; the frontend asks for
            # the repair below (see ApiKeyStatus).
            api_key_valid=ApiKeyStatus.is_valid(),
        )

    def repair_api_key(self, user_jwt: Optional[str]) -> bool:
        """Replace this pod's revoked API key with a live one, in place.

        cloud-api hands the key over against the editor session token, since the
        pod's own key is the broken credential. Storing it makes get_credentials
        prefer it over the (rejected) one from the deployment, so the pod recovers
        without being replaced — nothing here needs a restart or a new pod.

        Returns whether the pod ended up with a new credential. False leaves the
        editor exactly as it was, still failing, which is what the caller falls
        back on.
        """
        if EDITOR_MODE != "web":
            # A local install has no deployment credential to repair: an invalid
            # token there means `abstra login`, which owns its own flow.
            return False

        if not user_jwt:
            return False

        return ApiKeyStatus.repair(user_jwt)
