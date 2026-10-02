from __future__ import absolute_import

from tmo.api.iterator_base_api import IteratorBaseApi


class FeatureEngineeringApi(IteratorBaseApi):
    name = "Feature Engineering API"
    path = "featureEngineeringTasks"
    type = "FEATURE_ENGINEERING"

    def import_task(self, import_request: dict[str, str]):
        """
        import a feature engineering task

        Parameters:
            import_request (dict): request to import model version

        Returns:
            (dict): job
        """
        self.required_params(
            ["artefactImportId", "name", "description", "language", "functionName"],
            import_request,
        )

        return self.tmo_client.post_request(
            path=f"{self.base_path + self.path}/import",
            header_params=self._get_header_params(),
            query_params={},
            body=import_request,
        )

    def run(self, task_id: str, run_request: dict[str, str]):
        """
        run feature engineering task

        Parameters:
            task_id (str): model id(uuid)
            run_request (dict): request to import model version

        Returns:
            (dict): job
        """
        task_id = self.validate_uuid(task_id)

        self.required_params(["automation", "datasetConnectionId"], run_request)

        return self.tmo_client.post_request(
            path=f"{self.base_path + self.path}/{task_id}/run",
            header_params=self._get_header_params(),
            query_params={},
            body=run_request,
        )

    def approve(self, task_id: str, comments: str):
        """
        approve a feature engineering task
        :param task_id:  task id
        :param comments: approval comments
        :return:
        """
        task_id = self.validate_uuid(task_id)

        return self._approve_entity(task_id, comments)

    def reject(self, task_id: str, comments: str):
        """
        reject a feature engineering task
        :param task_id:  task id
        :param comments: approval comments
        :return:
        """
        task_id = self.validate_uuid(task_id)

        return self._reject_entity(task_id, comments)

    def deploy(self, task_id: str, deploy_request: dict):
        """
        deploy a trained model
        :param task_id:  fe task id
        :param deploy_request: deployment request
        :return:
        """
        task_id = self.validate_uuid(task_id)

        return self._deploy_entity(task_id, deploy_request)

    def retire(self, task_id: str, retire_request: dict):
        """
        retire a trained model
        :param task_id:  fe task id
        :param retire_request: retire request
        :return:
        """
        return self._retire_entity(task_id, retire_request)
