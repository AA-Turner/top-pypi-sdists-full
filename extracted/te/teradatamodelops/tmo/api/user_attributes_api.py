from tmo.api.iterator_base_api import BaseApi


class UserAttributesApi(BaseApi):
    name = "User Attributes API"
    path = "userAttributes"
    type = "USER_ATTRIBUTES"

    def _get_header_params(self):
        header_vars = [
            "AOA-Project-ID",
            "VMO-Project-ID",
            "Accept",
        ]  # AOA-Project-ID kept for backwards compatibility
        header_vals = [
            self.tmo_client.project_id,
            self.tmo_client.project_id,
            self.tmo_client.select_header_accept([self.json_type, "text/plain", "*/*"]),
        ]

        return self.generate_params(header_vars, header_vals)

    def get_default_connection(self):

        result = self.tmo_client.get_request(
            path=f"{self.base_path + self.path}/search/findByName",
            header_params=self._get_header_params(),
            query_params=self.generate_params(["name"], ["DEFAULT_CONNECTION"]),
        )

        if not isinstance(result, dict):
            raise ValueError("Default connection not found or invalid API response.")

        connection_id = (result.get("value") or {}).get("defaultDatasetConnectionId")
        excluded_keys = {"value"}

        return {
            **{k: v for k, v in result.items() if k not in excluded_keys},
            "attribute_id": result.get("id"),
            "id": connection_id,
        }
