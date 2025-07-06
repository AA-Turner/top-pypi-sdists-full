from typing import Any, Dict

from .._actions import _Actions


class ActionsInfo:

    def __init__(self, actions: _Actions):
        self.__actions = actions

    def get_all_available_actions(self, locust_request_label_breadcrumb: str = "Actions.MainMenu.AvailableActions") -> Dict[str, Any]:
        """
        Retrieves all the available "actions" and associated metadata from "Appian-Tempo-Actions"

        Args:
            locust_request_label_breadcrumb (str): Base label used for each of the multiple requests made by this method

        Returns (dict): List of actions and associated metadata

        Examples:

            >>> actions_info.get_all_available_actions()

        """
        return self.__actions.get_all(locust_request_label=locust_request_label_breadcrumb)

    def get_action_info(self, action_name: str, exact_match: bool = False) -> Dict[str, Any]:
        """
        Get the information about specific action by name.

        Args:
            action_name (str): Name of the action
            exact_match (bool): Should action name match exactly or to be partial match. Default : False

        Returns (dict): Specific Action's info

        Raises: In case of action is not found in the system, it throws an "Exception"

        Example:
            If full name of action is known:

            >>> action_info.get_action_info("action_name", exact_match=True)

            If only the display name is known, or part of the display name:

            >>> action_info.get_action_info("actio")

        """
        return self.__actions.get_action(action_name=action_name, exact_match=exact_match)
