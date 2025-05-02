import asyncio
import base64
import json
import logging
import os
import traceback
from typing import Any, List, Union

import httpx

from creator.auto.request_auto import AutoTxt2Img, AutoImg2Img
from creator.auto.response_auto import ResponseAuto
from creator.base.base_app import BaseApp
from creator.base.base_response import BaseResponse, ResponseData, ResponseDataType
from creator.base.job_status import JobStatus

logger = logging.getLogger(__name__)


class AppAuto(BaseApp):
    param_classes = [AutoTxt2Img, AutoImg2Img]
    output = {}
    jobs = {}
    sched_jobs = {}
    credentials = {}

    def __init__(self):
        super().__init__()
        auto_port = os.environ.get("PORT_AUTO", 8081)
        if isinstance(auto_port, str):
            auto_port = int(auto_port)
        self.jobs = {}
        self.output = {}
        self.credentials = {}
        self.api_base_url = f"http://0.0.0.0:{auto_port}"
        app_config_path = "/opt/rd/apps/stable-diffusion-webui/config.json"
        if os.path.exists(app_config_path):
            with open(app_config_path, "r") as f:
                app_config = json.load(f)
                default_checkpoint = app_config.get("sd_model_checkpoint", None)
                if default_checkpoint:
                    self.loaded_models.append(default_checkpoint)

    async def create(self, params: Union[AutoTxt2Img, AutoImg2Img], job_id=None) -> BaseResponse:
        print(f"Creating job with params: {params}")
        endpoint_name = "txt2img" if isinstance(params, AutoTxt2Img) else "img2img"
        url = f"{self.api_base_url}/agent-scheduler/v1/queue/{endpoint_name}"
        data = params.model_dump()
        # POP user_name and password
        user_name = data.pop("user_name", None)
        password = data.pop("password", None)
        if user_name and password:
            self.credentials[job_id] = (user_name, password)
        checkpoint = data.get("sd_model_checkpoint", None)
        if checkpoint and checkpoint not in self.loaded_models:
            self.loaded_models.append(checkpoint)
            if len(self.loaded_models) > 3:
                self.loaded_models.pop(0)
        headers = {'Content-Type': 'application/json'}
        if user_name and password:
            headers['Authorization'] = f"Basic {base64.b64encode(f'{user_name}:{password}'.encode()).decode()}"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, headers=headers)
            response.raise_for_status()
        output = response.json()
        task_id = output.get("task_id", None)
        print(f"Response received: {output}")
        if task_id:
            self.jobs[task_id] = endpoint_name
            result = await self.get_status(task_id)
            while result.status == JobStatus.RUNNING:
                await asyncio.sleep(5)
            return result

    async def create_async(self, params: Union[AutoTxt2Img, AutoImg2Img]) -> BaseResponse:
        endpoint_name = "txt2img" if isinstance(params, AutoTxt2Img) else "img2img"
        url = f"{self.api_base_url}/agent-scheduler/v1/queue/{endpoint_name}"
        data = params.model_dump()
        # POP user_name and password
        user_name = data.pop("user_name", None)
        password = data.pop("password", None)
        headers = {'Content-Type': 'application/json'}
        if user_name and password:
            headers['Authorization'] = f"Basic {base64.b64encode(f'{user_name}:{password}'.encode()).decode()}"
        checkpoint = data.get("sd_model_checkpoint", None)
        if checkpoint and checkpoint not in self.loaded_models:
            self.loaded_models.append(checkpoint)
            if len(self.loaded_models) > 3:
                self.loaded_models.pop(0)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data, headers=headers)
                response.raise_for_status()
            output = response.json()
            task_id = output.get("task_id", None)
            if task_id:
                return ResponseAuto.running(task_id)
        except Exception as e:
            logger.error(f"Error creating job: {e}")
            traceback.print_exc()
            return ResponseAuto.error(f"Error creating job: {e}")

    async def get_status(self, job_id: str, user_name: str = None, password: str = None) -> BaseResponse:
        try:
            url = f"{self.api_base_url}/agent-scheduler/v1/task/{job_id}/results"
            user_name, password = self.credentials.get(job_id, (user_name, password))
            headers = {'Content-Type': 'application/json'}
            if user_name and password:
                headers['Authorization'] = f"Basic {base64.b64encode(f'{user_name}:{password}'.encode()).decode()}"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
            output = response.json()

            job_success = output.get("success", False)
            if not job_success:
                message = output.get("message", "Unknown status")
                if message == "Task is pending":
                    return ResponseAuto.running(job_id)
                else:
                    return ResponseAuto.error(f"Error getting job status: {message}", job_id)
            else:
                images = []
                data = output.get("data", [])
                if data and isinstance(data, list):
                    for output in data:
                        image = output.get("image", None)
                        if image:
                            # Remove the data:image/png;base64, prefix
                            image = image.split(",")[-1]
                            images.append(image)
                response_data = ResponseData(data=images, data_type=ResponseDataType.IMAGE, total_count=len(images))
                return ResponseAuto.success(response_data, job_id)

        except Exception as e:
            logger.error(f"Error getting job status for job ID {job_id}: {e}")
            traceback.print_exc()
            return ResponseAuto.error(f"Error getting job status: {e}", job_id)

    async def get_models(self) -> List[Any]:
        url = f"{self.api_base_url}/sdapi/v1/sd-models"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            response_json = response.json()
        models = [model.get("title") for model in response_json if model.get("title")]
        return models

    # Assuming you will provide more detail or use this method later
    async def upload_image(self, image_data: Any) -> str:
        pass

    async def test(self):
        auto_port = int(os.environ.get("PORT_AUTO", 8081))
        url = f"http://0.0.0.0:{auto_port}/docs"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return BaseResponse.active()
            else:
                return BaseResponse.error("Error testing connection")

    async def cache_model(self, model: str = "Juggernaut-XI-Prototype.safetensors") -> bool:
        request = {
            "sd_model_checkpoint": model
        }
        if model not in self.loaded_models:
            self.loaded_models.append(model)
        if len(self.loaded_models) > 3:
            self.loaded_models.pop(0)
        url = f"{self.api_base_url}/sdapi/v1/options"
        headers = {'Content-Type': 'application/json'}
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(url, json=request, headers=headers, timeout=300)
            response.raise_for_status()
            if response.status_code == 200:
                return True
            print(f"Error caching model: {response.text}")
        return False
