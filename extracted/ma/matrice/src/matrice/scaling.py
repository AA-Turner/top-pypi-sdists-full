"""Module providing scaling functionality."""


class _Scaling:
    """This is a private class used internally."""

    def __init__(self, session, instance_id=None):
        self.instance_id = instance_id
        self.rpc = session.rpc

    def handle_response(self, resp, success_message, error_message):
        """Helper function to handle API response"""
        if resp.get("success"):
            error = None
            message = success_message
        else:
            error = resp.get("message")
            message = error_message
        return resp, error, message

    def get_downscaled_ids(self):
        if self.instance_id is None:
            print(
                "Instance id not set for this instance. Cannot perform the operation for job-scheduler without instance id"
            )
        path = f"/v1/scaling/down_scaled_ids/{self.instance_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Downscaled ids info fetched successfully",
            "Could not fetch the Downscaled ids info",
        )

    def stop_instance(self):
        if self.instance_id is None:
            print(
                "Instance id not set for this instance. Cannot perform the operation for job-scheduler without instance id"
            )
        path = "/v1/scaling/compute_instance/stop"
        resp = self.rpc.put(
            path=path,
            payload={
                "_idInstance": self.instance_id,
                "isForcedStop": False,
            },
        )
        return self.handle_response(
            resp,
            "Instance stopped successfully",
            "Could not stop the instance",
        )

    def update_action_status(
        self,
        service_provider="",
        action_record_id="",
        isRunning=True,
        status="",
        docker_start_time=None,
        action_duration=0,
        cpuUtilisation=0.0,
        gpuUtilisation=0.0,
        memoryUtilisation=0.0,
        gpuMemoryUsed=0,
        createdAt=None,
        updatedAt=None,
    ):
        if self.instance_id is None:
            print(
                "Instance id not set for this instance. Cannot perform the operation for job-scheduler without instance id"
            )
        path = "/v1/scaling/update_action_status"
        payload_scaling = {
            "instanceID": self.instance_id,
            "serviceProvider": service_provider,
            "actionRecordId": action_record_id,
            "isRunning": isRunning,
            "status": status,
            "dockerContainerStartTime": docker_start_time,
            "cpuUtilisation": cpuUtilisation,
            "gpuUtilisation": gpuUtilisation,
            "memoryUtilisation": memoryUtilisation,
            "gpuMemoryUsed": gpuMemoryUsed,
            "actionDuration": action_duration,
            "createdAt": createdAt,
            "updatedAt": updatedAt,
        }
        resp = self.rpc.put(path=path, payload=payload_scaling)
        return self.handle_response(
            resp,
            "Action status details updated successfully",
            "Could not update the action status details ",
        )

    def update_status(
        self,
        action_record_id,
        action_type,
        service_name,
        stepCode,
        status,
        status_description,
    ):
        url = "/v1/project/action"
        payload = {
            "_id": action_record_id,
            "action": action_type,
            "serviceName": service_name,
            "stepCode": stepCode,
            "status": status,
            "statusDescription": status_description,
        }
        self.rpc.put(path=url, payload=payload)

    def get_shutdown_details(self):
        if self.instance_id is None:
            print(
                "Instance id not set for this instance. Cannot perform the operation for job-scheduler without instance id"
            )
        path = f"/v1/scaling/get_shutdown_details/{self.instance_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Shutdown info fetched successfully",
            "Could not fetch the shutdown details",
        )

    def get_tasks_details(self):
        if self.instance_id is None:
            print(
                "Instance id not set for this instance. Cannot perform the operation for job-scheduler without instance id"
            )
        path = f"/v1/project/action/instance/{self.instance_id}/action_details"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Task details fetched successfully",
            "Could not fetch the task details",
        )

    def get_action_details(self, action_status_id):
        path = f"/v1/project/action/{action_status_id}/details"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Task details fetched successfully",
            "Could not fetch the task details",
        )

    def log_error(
        self,
        service_name="",
        stack_trace="",
        error_type="",
        description="",
        filename="",
        function_name="",
        more_info={},
        action_record_id="",
    ):
        log_err = {
            "serviceName": service_name,
            "stackTrace": stack_trace,
            "errorType": error_type,
            "description": description,
            "fileName": filename,
            "functionName": function_name,
            "moreInfo": more_info,
        }
        if action_record_id != "":
            log_err["actionRecordID"] = action_record_id
        path = "/v1/system/log_error"
        resp = self.rpc.post(path=path, payload=log_err)
        return self.handle_response(
            resp,
            "Error logged successfully",
            "Could not log the errors",
        )

    def update_action(
        self,
        id="",
        step_code="",
        action_type="",
        status="",
        sub_action="",
        status_description="",
        service="",
        job_params={},
    ):
        path = "/v1/project/action"
        payload = {
            "_id": id,
            "stepCode": step_code,
            "action": action_type,
            "status": status,
            "subAction": sub_action,
            "statusDescription": status_description,
            "serviceName": service,
            "jobParams": job_params,
        }
        resp = self.rpc.put(path=path, payload=payload)
        return self.handle_response(
            resp,
            "Error logged successfully",
            "Could not log the errors",
        )

    def assign_jobs(self, is_gpu):
        path = "/v1/scaling/assign_jobs/" + str(is_gpu) + f"/{self.instance_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Pinged successfully",
            "Could not ping the scaling jobs",
        )

    def update_available_resources(
        self,
        availableCPU=0,
        availableGPU=0,
        availableMemory=0,
        availableGPUMemory=0,
    ):
        path = f"/v1/scaling/update_available_resources/{self.instance_id}"
        payload = {
            "availableMemory": availableMemory,
            "availableCPU": availableCPU,
            "availableGPUMemory": availableGPUMemory,
            "availableGPU": availableGPU,
        }
        resp = self.rpc.put(path=path, payload=payload)
        return self.handle_response(
            resp,
            "Resources updated successfully",
            "Could not update the resources",
        )
    

    def update_action_docker_logs(self, action_record_id, log_content):
        path = "/v1/project/update_action_docker_logs"
        payload = {
            "actionRecordId": action_record_id,
            "logContent": log_content,
        }
        resp = self.rpc.put(path=path, payload=payload)
        return self.handle_response(
            resp,
            "Docker logs updated successfully",
            "Could not update the docker logs",
        )

    def get_model_secret_keys(self, secret_name):
        path = f"/v1/scaling/get_models_secret_keys?secret_name={secret_name}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Secret keys fetched successfully",
            "Could not fetch the secret keys",
        )

    def get_model_codebase(self, modelfamily_id):
        path = f"/v1/model_store/get_user_code_download_path/{modelfamily_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Codebase fetched successfully",
            "Could not fetch the codebase",
        )

    def get_docker_hub_credentials(self):
        path = "/v1/scaling/get_docker_hub_credentials"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Docker hub credentials fetched successfully",
            "Could not fetch the docker hub credentials",
        )

    def get_model_codebase_requirements(self, model_family_id):
        path = f"/v1/model_store/get_user_requirements_download_path/{model_family_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Codebase requirements fetched successfully",
            "Could not fetch the codebase requirements",
        )

    def get_model_codebase_script(self, model_family_id):
        path = f"/v1/model_store/get_user_script_download_path/:{model_family_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Codebase script fetched successfully",
            "Could not fetch the codebase script",
        )

    def add_account_compute_instance(
        self,
        account_number,
        alias,
        service_provider,
        instance_type,
        shut_down_time,
        lease_type,
        launch_duration,
    ):
        path = "/v1/scaling/add_account_compute_instance"
        payload = {
            "accountNumber": account_number,
            "alias": alias,
            "serviceProvider": service_provider,
            "instanceType": instance_type,
            "shutDownTime": shut_down_time,
            "leaseType": lease_type,
            "launchDuration": launch_duration,
        }
        resp = self.rpc.post(path=path, payload=payload)
        return self.handle_response(
            resp,
            "Compute instance added successfully",
            "Could not add the compute instance",
        )

    def stop_account_compute(self, account_number, alias):
        path = f"/v1/scaling/stop_account_compute/{account_number}/{alias}"
        resp = self.rpc.put(path=path)
        return self.handle_response(
            resp,
            "Compute instance stopped successfully",
            "Could not stop the compute instance",
        )

    def restart_account_compute(self, account_number, alias):
        path = f"/v1/scaling/restart_account_compute/{account_number}/{alias}"
        resp = self.rpc.put(path=path)
        return self.handle_response(
            resp,
            "Compute instance restarted successfully",
            "Could not restart the compute instance",
        )

    def delete_account_compute(self, account_number, alias):
        path = f"/v1/scaling/delete_account_compute/{account_number}/{alias}"
        resp = self.rpc.delete(path=path)
        return self.handle_response(
            resp,
            "Compute instance deleted successfully",
            "Could not delete the compute instance",
        )

    def get_all_instances_type(self):
        path = "/v1/scaling/get_all_instances_type"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "All instance types fetched successfully",
            "Could not fetch the instance types",
        )

    def get_compute_details(self):
        path = f"/v1/scaling/get_compute_details/{self.instance_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Compute details fetched successfully",
            "Could not fetch the compute details",
        )

    def get_user_access_key_pair(self, user_id):
        path = f"/v1/scaling/get_user_access_key_pair/{user_id}/{self.instance_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "User access key pair fetched successfully",
            "Could not fetch the user access key pair",
        )
