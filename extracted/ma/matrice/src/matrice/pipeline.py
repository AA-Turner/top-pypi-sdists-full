from matrice.utils import handle_response
from matrice.projects import Projects


class Pipeline:

    def __init__(self, session, pipeline_id = None):
        self.pipeline_id = pipeline_id
        self.session = session
        self.rpc = session.rpc
        self.project_id = session.project_id 
    
    def get_pipeline(self):
        if not self.pipeline_id:
            raise ValueError("Pipeline ID is required to get pipeline details.")

        path = f"/v1/project/pipeline/{self.pipeline_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Pipeline details fetched successfully",
            "Could not fetch pipeline details",
        )
    
    def get_stages(self, pipeline_version = "v1.0", run = 1):
        if not self.pipeline_id:
            raise ValueError("Pipeline ID is required to get pipeline stages.")

        path = f"/v1/project/pipeline/get_stages/{self.pipeline_id}/{pipeline_version}?run={run}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Pipeline stages fetched successfully",
            "Could not fetch pipeline stages",
        )
    
    def get_actions_by_stage(self, stage_id):
        if not self.pipeline_id:
            raise ValueError("Pipeline ID is required to get pipeline actions.")

        path = f"/v1/project/pipeline/get_actions_by_stage/{stage_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Pipeline actions fetched successfully",
            "Could not fetch pipeline actions",
        )
    
    def get_stages_and_actions(self, pipeline_version = "v1.0", run = 1):
        if not self.pipeline_id:
            raise ValueError("Pipeline ID is required to get pipeline stages and actions.")

        path = f"/v1/project/pipeline/get_stages_and_actions/{self.pipeline_id}/{pipeline_version}?run={run}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Pipeline stages and actions fetched successfully",
            "Could not fetch pipeline stages and actions",
        )

    def create_pipeline(self, pipeline_name):
        payload = {
            "pipelineName": pipeline_name,
            "projectId": self.project_id,
        }
        project = Projects(session=self.session, project_id=self.project_id)
        payload["inputs"] = [project.project_input]
        payload["outputs"] = [project.output_type]
        path = f"/v1/project/pipeline"
        resp = self.rpc.post(path=path, payload=payload)
        return handle_response(
            resp,
            "Pipeline created successfully",
            "Could not create the pipeline",
        )
    
    def construct_stage_payload(
    self,
    action_type=None,
    run=1,
    pipeline_version="v1.0",
    pull_queue_id=None,
    push_queue_id=None,
    creation_type="manual",
    resource_constraints=None,
    process_input="single",
    process_output="single",
    input_service_id=None,
    action_params=None,
    trigger_ids=None,
    position=None,
    is_editable=True,
    ):
        if not self.pipeline_id:
            raise ValueError("Pipeline ID is required in stage payload.")


        return {
            "run": run,
            "pipelineId": self.pipeline_id,
            "pipelineVersion": pipeline_version,
            "pullQueueId": str(pull_queue_id) if pull_queue_id else None,
            "pushQueueId": str(push_queue_id) if push_queue_id else None,
            "actionType": action_type,
            "creationType": creation_type,
            "autoResourceConstraintsPerIP": resource_constraints,
            "processInputType": process_input,
            "processOutputType": process_output,
            "inputServiceId": str(input_service_id) if input_service_id else None,
            "actionParams": action_params if action_params else [],
            "triggerIds": [str(tid) for tid in trigger_ids] if trigger_ids else [],
            "position": position if position else [0, 0],
            "isEditable": is_editable,
        }

    def add_pipeline_stages_and_actions(self, stages_payload):
        if not self.pipeline_id:
            raise ValueError("Pipeline ID is required to add stages and actions.")

        if not isinstance(stages_payload, list):
            stages_payload = [stages_payload]

        path = "/v1/project/pipeline/add_stages_and_actions"
        resp = self.rpc.post(path=path, payload=stages_payload)
        return handle_response(
            resp,
            "Pipeline stages and actions added successfully",
            "Could not add pipeline stages and actions",
        )

    def run_pipeline(self, pipeline_version = "v1.0", run = 1):
        if not self.pipeline_id:
            raise ValueError("Pipeline ID is required to run the pipeline.")

        path = f"/v1/project/pipeline/run/{self.pipeline_id}/{pipeline_version}?run={run}"
        resp = self.rpc.post(path=path)
        return handle_response(
            resp,
            "Pipeline run successfully",
            "Could not run the pipeline",
        )
