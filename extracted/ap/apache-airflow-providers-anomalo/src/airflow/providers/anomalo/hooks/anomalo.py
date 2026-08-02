from typing import Any, Mapping

from airflow.hooks.base import BaseHook

from anomalo import Client


class AnomaloHook(BaseHook):
    """
    Hook for connecting to an Anomalo instance.
    """

    conn_name_attr = "anomalo_conn_id"
    default_conn_name = "anomalo_default"
    conn_type = "anomalo"
    hook_name = "Anomalo"

    @staticmethod
    def get_connection_form_widgets() -> Mapping[str, Any]:
        """Returns connection widgets to add to connection form"""
        from flask_appbuilder.fieldwidgets import BS3PasswordFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import PasswordField

        return {
            "api_token": PasswordField(
                lazy_gettext("API secret token", widget=BS3PasswordFieldWidget())
            ),
        }

    @staticmethod
    def get_ui_field_behaviour() -> Mapping[str, Any]:
        """Returns custom field behaviour"""
        return {
            "hidden_fields": ["login", "password", "schema", "extra", "uri", "port"],
            "relabeling": {},
        }

    def __init__(self, anomalo_conn_id=default_conn_name):
        super().__init__()
        self.anomalo_conn_id = anomalo_conn_id

    def get_conn(self):
        params = self.get_connection(conn_id=self.anomalo_conn_id)
        return Client(api_token=params.extra_dejson["api_token"], host=params.host)

    def get_client(self):
        params = self.get_connection(conn_id=self.anomalo_conn_id)
        return Client(api_token=params.extra_dejson["api_token"], host=params.host)
