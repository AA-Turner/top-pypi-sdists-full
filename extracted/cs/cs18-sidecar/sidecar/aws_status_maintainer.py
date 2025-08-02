import threading
import traceback
from contextlib import contextmanager
from logging import Logger
from typing import List
from sidecar.aws_session import AwsSession
from sidecar.const import Const
from sidecar.utils import Utils
from sidecar.status_maintainer import StatusMaintainer, IngressRouteRequest
from sidecar.sandbox_error import SandboxError


class AWSStatusMaintainer(StatusMaintainer):
    table_data = {}

    def __init__(self, awssessionservice: AwsSession, sandbox_id: str, logger: Logger, default_region: str,
                 table_name: str):
        super().__init__(logger)
        self.default_region = default_region
        self.dynamo_resource = awssessionservice.get_dynamo_resource(default_region=self.default_region)
        self.table_data = None
        self._sandbox_id = sandbox_id
        self._logger = logger
        self._table_name = table_name
        self._apps_lock = threading.RLock()
        self._logical_apps_lock = threading.RLock()

        self.refresh_db()

    def _item_exist_in_db(self):
        table = self.dynamo_resource.Table(self._table_name)
        response = table.get_item(
            Key={
                Const.SANDBOX_ID_TAG: self._sandbox_id
            }
        )
        return True if "Item" in response else False

    def _set_table_data(self, table, sandbox_id):
        response = table.get_item(
            Key={
                Const.SANDBOX_ID_TAG: sandbox_id
            }
        )

        if "Item" in response:
            self.table_data = response["Item"]
            self._logger.info("dynamo table response for sandbox {id} is {data}".format(id=sandbox_id, data=response))
            return "Item"

        return None

    def refresh_db(self):
        table = self.dynamo_resource.Table(self._table_name)
        try:
            Utils.wait_for(func=lambda: self._set_table_data(table, self._sandbox_id) is not None,
                           interval_sec=1,
                           max_retries=5,
                           error='No sandbox data available')
        except Exception:
            self._logger.exception("Failed to get sandbox data from dynamodb after 5 times")
            return

    def _update_item(self, key, value):
        if not self._item_exist_in_db():
            return

        table = self.dynamo_resource.Table(self._table_name)
        response = table.update_item(
            Key={Const.SANDBOX_ID_TAG: self._sandbox_id},
            UpdateExpression="set #f = :r",
            ExpressionAttributeValues={':r': value},
            ExpressionAttributeNames={"#f": key},
            ReturnValues="UPDATED_NEW"
        )

        if self.response_failed(response):
            raise Exception(
                f"Failed to update QualiY field: '{key}', with value: '{value}' in sandbox '{self._sandbox_id}'\n "
                f"Response: {response}\n"
                f"Trace: {''.join(traceback.format_stack())}")
        return response

    def update_qualiy_status(self, status: str):
        self._update_item(Const.QUALIY_STATUS, status)

    def update_service_in_dynamo(self):
        return self._update_item("services", self.table_data["services"])

    def get_deployment_outputs(self, entity_name: str) -> {}:
        if entity_name in self.table_data["services"]:
            return self.table_data["services"][entity_name].get("outputs", {})

        for logical_id, logical_details in self.table_data["apps"].items():
            for instance_id, instance_json in logical_details['instances'].items():
                for app_name, app_details in instance_json['apps'].items():
                    if app_name == entity_name:
                        return app_details.get('outputs', {})
        raise Exception(f"could not find service/application with name '{entity_name}'")

    def get_service_deployment_outputs(self, service_name: str) -> {}:
        service = self.table_data["services"].get(service_name)
        if service:
            return service.get("outputs", {})
        raise Exception(f"could not find service with name '{service_name}'")

    def get_app_deployment_outputs(self, app_name: str) -> {}:
        app_details = self._get_first_application(app_name)
        if app_details:
            return app_details.get('outputs', {})
        raise Exception(f"could not find application with name '{app_name}'")

    def _get_first_application(self, app_name: str):
        for logical_id, logical_details in self.table_data["apps"].items():
            for instance_id, instance_json in logical_details['instances'].items():
                for name, app_details in instance_json['apps'].items():
                    if name == app_name:
                        return app_details
        return None

    def update_service_outputs(self, service_name: str, outputs: {}):
        if not self._item_exist_in_db():
            return

        self.table_data["services"][service_name]["outputs"] = outputs
        response = self.update_service_in_dynamo()
        if self.response_failed(response):
            self._logger.error(
                "error while updating service '{SERVICE}' outputs in sandbox '{SANDBOX}'. {RESPONSE}".format(
                    SERVICE=service_name,
                    SANDBOX=self._sandbox_id,
                    RESPONSE=response))

    def update_app_instance_healthcheck_status(self, instance_logical_id, instance_id, app_name, status):
        if not self._item_exist_in_db():
            return

        with self._modify_apps():
            instance = self.get_or_add_instance_under_logical_id(instance_id, instance_logical_id)
            app_details = self.get_or_add_app_under_instance(instance, app_name)
            app_details[Const.APP_STATUS_TAG] = status

    def update_app_instance_configuration_status(self, instance_logical_id, instance_id, app_name, status):
        if not self._item_exist_in_db():
            return

        with self._modify_apps():
            instance = self.get_or_add_instance_under_logical_id(instance_id, instance_logical_id)
            app_details = self.get_or_add_app_under_instance(instance, app_name)
            app_details[Const.CONFIGURATION_STATUS] = status

    def update_app_instance_artifacts_status(self, instance_logical_id, instance_id, app_name, status):
        if not self._item_exist_in_db():
            return

        with self._modify_apps():
            instance = self.get_or_add_instance_under_logical_id(instance_id, instance_logical_id)
            app_details = self.get_or_add_app_under_instance(instance, app_name)
            app_details[Const.ARTIFACTS_INTO_INSTANCE_STATUS] = status

    def update_app_instance_outputs(self, instance_logical_id, instance_id, app_name, outputs: {}):
        if not self._item_exist_in_db():
            return

        with self._modify_apps():
            instance = self.get_or_add_instance_under_logical_id(instance_id, instance_logical_id)
            app_details = self.get_or_add_app_under_instance(instance, app_name)
            app_details["outputs"] = outputs

    def add_app_instance_error(self, instance_logical_id, instance_id, app_name, error: SandboxError):
        if not self._item_exist_in_db():
            return

        with self._modify_apps():
            instance = self.get_or_add_instance_under_logical_id(instance_id, instance_logical_id)
            app_details = self.get_or_add_app_under_instance(instance, app_name)
            app_details[Const.APP_INSTANCE_ERRORS].append(error.to_dict())

    @contextmanager
    def _modify_apps(self):
        with self._apps_lock:
            yield  # executes the code inside the "with self._modify_apps():"
            self._update_item("apps", self.table_data["apps"])

    def update_logical_app_artifacts_status(self, app_name: str, status: str):
        if not self._item_exist_in_db():
            return

        with self._modify_logical_apps():
            self.table_data["logical-apps"][app_name][Const.ARTIFACTS_INTO_SIDECAR_STATUS] = status

    def update_logical_app_healthcheck_status(self, app_name: str, status: str):
        if not self._item_exist_in_db():
            return

        with self._modify_logical_apps():
            self.table_data["logical-apps"][app_name][Const.HEALTH_CHECK_STATUS] = status

    def add_logical_app_error(self, app_name: str, error: SandboxError):
        if not self._item_exist_in_db():
            return

        with self._modify_logical_apps():
            self.table_data["logical-apps"][app_name][Const.APP_ERRORS].append(error.to_dict())

    @contextmanager
    def _modify_logical_apps(self):
        with self._logical_apps_lock:
            yield  # executes the code inside the "with self._modify_logical_apps():"
            self._update_item('logical-apps', self.table_data['logical-apps'])

    def update_service_status(self, name: str, status: str):
        if not self._item_exist_in_db():
            return

        self.table_data["services"][name]["status"] = status
        response = self.update_service_in_dynamo()
        if self.response_failed(response):
            self._logger.error(
                "error while updating service '{SERVICE}' status in sandbox '{SANDBOX}'. {RESPONSE}".format(
                    SERVICE=name,
                    SANDBOX=self._sandbox_id,
                    RESPONSE=response))

    def get_or_add_instance_under_logical_id(self, instance_id, instance_logical_id) -> dict:
        try:
            instances = self.table_data["apps"][instance_logical_id]["instances"]
            return instances.setdefault(instance_id, {"apps": {}})
        except Exception as ex:  # log details for debugging, related to bug #1689
            self._logger.exception(f'Fail to update app instance (instance_id: {instance_id}, '
                                   f'instance_logical_id: {instance_logical_id})\n'
                                   f'Table data: {self.table_data}')
            raise ex

    def get_or_add_app_under_instance(self, instance: dict, app_name: str) -> dict:
        if app_name not in instance['apps']:
            instance['apps'][app_name] = {
                Const.ARTIFACTS_INTO_INSTANCE_STATUS: None,
                Const.CONFIGURATION_STATUS: None,
                Const.APP_STATUS_TAG: None,
                Const.APP_INSTANCE_ERRORS: []
            }
        return instance['apps'][app_name]

    def add_sandbox_error(self, error: SandboxError):
        errors_dict = self.table_data[Const.SANDBOX_ERRORS]
        errors_dict.append(error.to_dict())

        self._update_item(Const.SANDBOX_ERRORS, self.table_data[Const.SANDBOX_ERRORS])

    def update_sandbox_end_status(self, sandbox_deployment_end_status: str):
        if not self._item_exist_in_db():
            return

        table = self.dynamo_resource.Table(self._table_name)

        response = table.update_item(
            Key={
                Const.SANDBOX_ID_TAG: self._sandbox_id
            },
            UpdateExpression="set #f = :r, #newend = :r",
            ExpressionAttributeValues={
                ':r': sandbox_deployment_end_status
            },
            ExpressionAttributeNames={
                "#f": Const.SANDBOX_DEPLOYMENT_END_STATUS,
                "#newend": Const.SANDBOX_DEPLOYMENT_END_STATUS_v2
            },
            ReturnValues="UPDATED_NEW"
        )

        if self.response_failed(response):
            self._logger.error("Error update_sandbox_end_status(sandbox_id: {sandbox_id} status: {status})\n"
                               "Response: {data}"
                               .format(sandbox_id=self._sandbox_id, status=sandbox_deployment_end_status, data=response))

    def update_sandbox_start_status(self, sandbox_start_time):
        if not self._item_exist_in_db():
            return

        table = self.dynamo_resource.Table(self._table_name)

        response = table.update_item(
            Key={
                Const.SANDBOX_ID_TAG: self._sandbox_id
            },
            UpdateExpression="set #f = :r, #newstart = :r",
            ExpressionAttributeValues={
                ':r': str(sandbox_start_time)
            },
            ExpressionAttributeNames={
                "#f": Const.SANDBOX_START_TIME,
                "#newstart": Const.SANDBOX_START_TIME_v2
            },
            ReturnValues="UPDATED_NEW"
        )

        if self.response_failed(response):
            self._logger.error("Error update_sandbox_start_status(sandbox_id: {sandbox_id} status: {status})\n"
                               "Response: {data}"
                               .format(sandbox_id=self._sandbox_id, status=sandbox_start_time, data=response))

    def get_all_app_names_for_instance(self, logical_id: str):
        return self.table_data["spec"]["expected_apps"][logical_id]["apps"]

    @staticmethod
    def response_failed(response: dict) -> bool:
        return not response.get("ResponseMetadata") and \
               not response.get("ResponseMetadata").get("HTTPStatusCode") == 200

    def get_ingress_routes(self) -> List[IngressRouteRequest]:
        items = []
        for ingress_route in self.table_data.get('ingress_routes', []):
            items.append(IngressRouteRequest(
                listener_port=ingress_route['listener_port'],
                path=ingress_route['path'],
                host=ingress_route['host'],
                app_name=ingress_route['app_name'],
                app_port=ingress_route['app_port'],
                color=ingress_route['color']))
        return items

    def get_terminating_flag(self) -> bool:
        table = self.dynamo_resource.Table(self._table_name)

        response = table.get_item(
            Key={Const.SANDBOX_ID_TAG: self._sandbox_id},
            ConsistentRead=True,
            ProjectionExpression='terminating'
        )

        if "Item" in response:
            doc = response["Item"]
            if 'terminating' in doc:
                return doc['terminating']

        return False
