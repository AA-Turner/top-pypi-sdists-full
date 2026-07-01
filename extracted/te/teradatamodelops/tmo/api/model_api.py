from __future__ import absolute_import

from tmo.api.iterator_base_api import IteratorBaseApi


class ModelApi(IteratorBaseApi):
    name = "Model API"
    path = "models"
    type = "MODEL"

    def find_by_source_id(self, source_model_id: str, projection: str = None):
        """
        returns a model by source model id taken from git repo

        Parameters:
           source_model_id (str): source model id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): model
        """
        source_model_id = self.validate_uuid(source_model_id)

        query_vars = ["sourceId", "projection"]
        query_vals = [source_model_id, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            f"{self.base_path + self.path}/search/findBySourceId",
            self._get_header_params(),
            query_params,
        )

    def find_all_commits(self, model_id: str, projection: str = None):
        """
        returns model commits

        Parameters:
           model_id (str): model id(uuid) for commits
           projection (str): projection type

        Returns:
            (dict): model commits
        """
        model_id = self.validate_uuid(model_id)

        query_vars = ["projection"]
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            f"{self.base_path + self.path}/{model_id}/commits",
            self._get_header_params(),
            query_params,
        )

    def diff_commits(
        self, model_id: str, commit_id1: str, commit_id2: str, projection: str = None
    ):
        """
        returns difference between model commits

        Parameters:
           model_id (str): model id(uuid)
           commit_id1 (str): id of commit to compare
           commit_id2 (str): id of commit to compare
           projection (str): projection type

        Returns:
            (str): difference between model commits
        """
        model_id = self.validate_uuid(model_id)

        query_vars = ["projection"]
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            f"{self.base_path + self.path}/{model_id}/diff/{commit_id1}/{commit_id2}/",
            self._get_header_params(),
            query_params,
        )

    def save(self, model: dict[str, str]):
        """
        register a dataset

        Parameters:
           model (dict): external model to register

        Returns:
            (dict): model
        """

        return self.tmo_client.post_request(
            path=self.base_path + self.path,
            header_params=self._get_header_params(),
            query_params={},
            body=model,
        )

    def train(self, model_id: str, training_request: dict[str, str]):
        """
        train a model

        Parameters:
            model_id (str): model id(uuid)
            training_request (dict): request to train model

        Returns:
            (dict): job
        """
        model_id = self.validate_uuid(model_id)

        self.required_params(["datasetId"], training_request)

        return self.tmo_client.post_request(
            path=f"{self.base_path + self.path}/{model_id}/train",
            header_params=self._get_header_params(),
            query_params={},
            body=training_request,
        )

    def import_byom(self, model_id: str, import_request: dict[str, str]):
        """
        import a model version

        Parameters:
            model_id (str): model id(uuid)
            import_request (dict): request to import model version

        Returns:
            (dict): job
        """
        model_id = self.validate_uuid(model_id)

        self.required_params(["artefactImportId", "externalId"], import_request)

        return self.tmo_client.post_request(
            path=f"{self.base_path + self.path}/{model_id}/import",
            header_params=self._get_header_params(),
            query_params={},
            body=import_request,
        )
