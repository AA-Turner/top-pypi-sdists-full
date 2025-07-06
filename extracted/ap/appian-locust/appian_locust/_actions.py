from typing import Any, Dict, Optional

from requests.models import Response

from .utilities import logger
from ._base import _Base
from ._interactor import _Interactor
from .utilities.helper import format_label
from .exceptions import MissingUrlProviderException
from .objects import TEMPO_ACTIONS_PAGE

log = logger.getLogger(__name__)

ACTIONS_ALL_PATH = "/suite/api/tempo/open-a-case/available-actions?ids=%5B%5D"
ACTIONS_FEED_PATH = "/suite/api/feed/tempo?m=menu-actions&c=0"
ACTIONS_INTERFACE_PATH = "/suite/rest/a/sites/latest/D6JMim/pages/actions/interface"
KEY_FORM_HREF = "formHref"


class _Actions(_Base):
    def __init__(self, interactor: _Interactor) -> None:
        """
        Actions class, wraps a list of possible activities that can be performed with Appian-Tempo-Actions

        Warnings: This class is internal and should not be access by tests directly. It can be accessed via "appian" object

        Note: "appian" is created as part of ``AppianTaskSet``'s ``on_start`` function

        Args:
            interactor: mechanism for interacting with UI via locust

        """
        self.interactor = interactor

        # When Get All functions called, these variables will be used to cache the values
        self._actions: Dict[str, Any] = dict()
        self._errors: int = 0

    def get_errors_count(self) -> int:
        return self._errors

    def clear_actions_cache(self) -> None:
        self._actions = dict()

    def get_actions_interface(self, locust_request_label: str = "Actions") -> Dict[str, Any]:
        uri = self.interactor.host + ACTIONS_INTERFACE_PATH
        headers = self.interactor.setup_sail_headers()
        resp = self.interactor.get_page(uri, headers, f'{locust_request_label}.Interface')
        return resp.json()

    def get_actions_nav(self, locust_request_label: str = "Actions") -> Dict[str, Any]:
        uri = self.interactor.get_url_provider().get_page_nav_path(TEMPO_ACTIONS_PAGE)
        headers = self.interactor.setup_sail_headers()
        resp = self.interactor.get_page(uri, headers, f'{locust_request_label}.Nav')
        return resp.json()

    def get_actions_feed(self, locust_request_label: str = "Actions") -> Dict[str, Any]:
        uri = self.interactor.host + ACTIONS_FEED_PATH
        headers = self.interactor.setup_feed_headers()
        resp = self.interactor.get_page(uri, headers, f'{locust_request_label}.Feed')
        return resp.json()

    def get_all(self, search_string: Optional[str] = None,
                locust_request_label: str = "Actions.MainMenu.AvailableActions") -> Dict[str, Any]:
        """
        Retrieves all the available "actions" and associated metadata from "Appian-Tempo-Actions"

        Note: All the retrieved data about actions is stored in the private variable self._actions

        Returns (dict): List of actions and associated metadata

        Examples:

            >>> self.appian.action.get_all()

        """
        try:
            self.get_actions_interface(locust_request_label=locust_request_label)
            self.get_actions_nav(locust_request_label=locust_request_label)
            self.get_actions_feed(locust_request_label=locust_request_label)
        except Exception as e:
            log.error(e)

        headers = self.interactor.setup_request_headers(self.interactor.host + ACTIONS_ALL_PATH)

        resp = self.interactor.get_page(
            self.interactor.host + ACTIONS_ALL_PATH, headers=headers, label=locust_request_label
        )
        self._actions = dict()
        error_key_string = "ERROR::"
        error_key_count = 0
        try:
            json_resp = resp.json()[0]
            for current_action in json_resp["actions"]:
                try:
                    key = current_action["displayLabel"] + \
                        "::" + current_action["opaqueId"]
                    self._actions[key] = current_action
                except Exception as e:
                    error_key_count += 1
                    self._actions[error_key_string + str(error_key_count)] = current_action
            self._errors = error_key_count
        except Exception as e:
            log.info("No Actions Returned")
            return self._actions
        return self._actions

    def get_action(self, action_name: str, exact_match: bool = False) -> Dict[str, Any]:
        """
        Get the information about specific action by name.

        Args:
            action_name (str): Name of the action
            exact_match (bool): Should action name match exactly or to be partial match. Default : False

        Returns (dict): Specific Action's info

        Raises: In case of action is not found in the system, it throws an "Exception"

        Example:
            If full name of action is known, with the opaque ID,

            >>> self.appian.action.get_action("action_name:igB0K7YxC0UQ2Fhx4hicRw...", exact_match=True)

            If only the display name is known, or part of the display name

            >>> self.appian.action.get_action("action_name")
            >>> self.appian.action.get_action("actio")

        """
        _, current_action = super().get(self._actions, action_name, exact_match)
        if not current_action:
            raise (Exception("There is no action with name {} in the system under test (Exact match = {})".format(
                action_name, exact_match)))
        return current_action

    def fetch_action_json(self, action_name: str, exact_match: bool = False, label: str = "") -> Dict[str, Any]:
        """
        This function calls the API for the specific action to get its "form" data

        Args:
            action_name (str): Name of the action to be called. Name of the action will be in the below pattern.
                         "displayLabel::opaquqId"
            exact_match (bool, optional): Should action name match exactly or to be partial match. Default : False

        Returns (dict): Response of actions's Get UI call in dictionary

        Examples:

            If the full name of the action is known, with the opaque ID,

            >>> self.appian.action.fetch_action_json("action_name:igB0K7YxC0UQ2Fhx4hicRw...", exact_match=True)

            If only the display name is known, or part of the display name

            >>> self.appian.action.fetch_action_json("action_name")
            >>> self.appian.action.fetch_action_json("actio")

        """
        action_under_test = self.get_action(action_name, exact_match)

        headers = self.interactor.setup_request_headers(action_under_test[KEY_FORM_HREF])
        headers["Accept"] = "application/vnd.appian.tv.ui+json"
        headers["Content-Type"] = "text/plain;charset=UTF-8"

        if not label:
            label = 'Actions.GetUi.' + format_label(action_name, "::", 0)

        resp = self.interactor.get_page(
            action_under_test[KEY_FORM_HREF],
            headers=headers,
            label=label,
        )
        resp_json = resp.json()
        # Check to see if we're in an activity chained form, and if so, make post call
        if resp_json.get('empty') == 'true':
            activity_chained_form_resp: Response = self.start_action(action_name, skip_design_call=True, exact_match=exact_match)
            activity_chained_form_resp.raise_for_status()
            resp_json = activity_chained_form_resp.json()

        return resp_json

    def start_action(self, action_name: str, skip_design_call: bool = False, exact_match: bool = False) -> Response:
        """
        Perform the post operation on action's API to start specific action.
        Actions that do not have a UI can be called directly without using "GET" to retrieve the UI.
        this is controlled by the optional skip_design_call parameter

        Args:
            action_name(str): Name of the action
            skip_design_call(bool, optional): to skip the "GET" call for the action's UI. Default : False
            exact_match (bool, optional): Should action name match exactly or to be partial match. Default : False

        Returns: NONE

        Example:

            >>> self.appian.action.start_action("action_name")

        """
        action_under_test = self.get_action(action_name, exact_match)

        if not skip_design_call:
            # Note: Actions which do not have a UI component this call is
            # not required to kick off processes. This request causes a call
            # to design to retrieve the UI, meaning this it will cause more K
            # activity, but it does not kick off processes on the exec engines.
            self.fetch_action_json(action_name)

        headers = self.interactor.setup_sail_headers()
        headers["Origin"] = self.interactor.host

        del headers["X-Atom-Content-Type"]
        headers["X-Client-Mode"] = "TEMPO"

        # To debug with wireshark, force http for this connection:
        #   action[KEY_FORM_HREF].replace("https","http"),
        resp = self.interactor.post_page(
            action_under_test[KEY_FORM_HREF].replace("/form", ""),
            payload={},
            headers=headers,
            label='Actions.StartAction.' + format_label(
                action_name, "::", 0)
        )
        return resp
