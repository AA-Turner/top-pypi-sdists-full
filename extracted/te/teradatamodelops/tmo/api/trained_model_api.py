from __future__ import absolute_import

from tmo.api.iterator_base_api import IteratorBaseApi


class TrainedModelApi(IteratorBaseApi):

    path = "/api/trainedModels"
    type = "TRAINED_MODEL"

    def _get_header_params(self):
        return self._get_standard_header_params(
            accept_types=[
                self.json_type,
                "application/hal+json",
                "text/uri-list",
                "application/x-spring-data-compact+json",
            ]
        )

    def find_dataset(self, trained_model_id: str, projection: str = None):
        """
        returns dataset of a trained model

        Parameters:
           trained_model_id (str): trained model id(uuid)
           projection (str): projection type

        Returns:
            (dict): dataset
        """
        query_vars = ["projection"]
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/{trained_model_id}/dataset",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_events(self, trained_model_id: str, projection: str = None):
        """
        returns trained model events

        Parameters:
           trained_model_id (str): trained model id(uuid)
           projection (str): projection type

        Returns:
            (dict): events of trained model
        """
        query_vars = ["projection"]
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/{trained_model_id}/events",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_by_model_id(self, model_id: str, projection: str = None):
        """
        returns a trained models by model id

        Parameters:
           model_id (str): model id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): trained models
        """
        query_vars = ["modelId", "projection"]
        query_vals = [model_id, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findByModelId",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def find_by_model_id_and_status(
        self, model_id: str, status: str, projection: str = None
    ):
        """
        returns a trained models by model id

        Parameters:
           model_id (str): model id(uuid) to find
           status (str): model status
           projection (str): projection type

        Returns:
            (dict): trained models
        """
        query_vars = ["modelId", "status", "projection"]
        query_vals = [model_id, status, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            path=f"{self.path}/search/findByModelIdAndStatus",
            header_params=self._get_header_params(),
            query_params=query_params,
        )

    def evaluate(self, trained_model_id: str, evaluation_request: dict[str, str]):
        """
        evaluate a model

        Parameters:
           trained_model_id (str): trained model id(uuid) to evaluate
           evaluation_request (dict): request to evaluate trained model

        Returns:
            (dict): job
        """
        self.required_params(["datasetId"], evaluation_request)

        return self.tmo_client.post_request(
            path=f"{self.path}/{trained_model_id}/evaluate",
            header_params=self._get_header_params(),
            query_params={},
            body=evaluation_request,
        )

    def approve(self, trained_model_id: str, comments: str):
        """
        approve a trained model
        :param trained_model_id:  model version
        :param comments: approval comments
        :return:
        """
        return self._approve_entity(trained_model_id, comments)

    def reject(self, trained_model_id: str, comments: str):
        """
        reject a trained model
        :param trained_model_id:  model version
        :param comments: approval comments
        :return:
        """
        return self._reject_entity(trained_model_id, comments)

    def deploy(self, trained_model_id: str, deploy_request: dict):
        """
        deploy a trained model
        :param trained_model_id:  model version
        :param deploy_request: deployment request
        :return:
        """
        return self._deploy_entity(trained_model_id, deploy_request)

    def retire(self, trained_model_id: str, retire_request: dict):
        """
        retire a trained model
        :param trained_model_id:  model version
        :param retire_request: retire request
        :return:
        """
        return self._retire_entity(trained_model_id, retire_request)
