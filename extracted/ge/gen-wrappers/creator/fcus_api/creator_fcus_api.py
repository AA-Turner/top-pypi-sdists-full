import asyncio
import json
import logging
import os
from typing import Any, Union, List

import httpx
import requests

from creator.base.base_app import BaseApp
from creator.base.base_request import BaseRequest
from creator.base.base_response import BaseResponse, ResponseDataType, ResponseData
from creator.base.job_status import JobStatus
from creator.fcus_api.request_fcus_api import FcusTxt2Img, FcusUpscaleOrVary, FcusInpaintOrOutpaint
from creator.fcus_api.response_fcus_api import ResponseFcusApi

logger = logging.getLogger(__name__)


class AppFcusApi(BaseApp):
    param_classes = [FcusTxt2Img, FcusUpscaleOrVary, FcusInpaintOrOutpaint]
    output = {}

    def __init__(self):
        super().__init__()
        focus_port = os.environ.get("PORT_FCUS_API", 8888)
        if isinstance(focus_port, str):
            focus_port = int(focus_port)
        self.api_base_url = f"http://0.0.0.0:{focus_port}"

    async def create(self, params: Union[FcusTxt2Img, FcusUpscaleOrVary, FcusInpaintOrOutpaint]) -> BaseResponse:
        if isinstance(params, FcusTxt2Img):
            url = f"{self.api_base_url}/v1/generation/text-to-image"
        elif isinstance(params, FcusUpscaleOrVary):
            url = f"{self.api_base_url}/v1/generation/image-upscale-vary"
        elif isinstance(params, FcusInpaintOrOutpaint):
            url = f"{self.api_base_url}/v1/generation/image-inpaint-outpaint"
        else:
            raise ValueError("Invalid parameters for creation")

        data = json.dumps(params.__dict__)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=data, headers=headers)
        # If we have a 422 here, print what the unprocessable entity is
        if response.status_code == 422:
            logger.warning(f"Unprocessable entity: {response.text}")
        response.raise_for_status()

        self.output = response.json()
        logger.debug(f"Response: {self.output}")
        job_id = self.output.get('job_id', None)
        output = None
        if job_id is not None:
            job_count = 0
            while output is None and job_count < 60:
                logger.debug(f"Job count: {job_count}")
                output = await self._get_output(job_id)
                job_count += 1
                if output is None:
                    await asyncio.sleep(1)
            response_data = ResponseData(data=output, data_type=ResponseDataType.IMAGE, total_count=len(output))
            return ResponseFcusApi(status="Job Finished", output=response_data, job_id=job_id)

    async def create_async(self, params: Union[FcusTxt2Img, FcusUpscaleOrVary, FcusInpaintOrOutpaint]) -> BaseResponse:
        if isinstance(params, FcusTxt2Img):
            model = params.base_model_name
            url = f"{self.api_base_url}/v1/generation/text-to-image"
        elif isinstance(params, FcusUpscaleOrVary):
            model = params.base_model_name
            url = f"{self.api_base_url}/v1/generation/image-upscale-vary"
        elif isinstance(params, FcusInpaintOrOutpaint):
            model = params.base_model_name
            url = f"{self.api_base_url}/v1/generation/image-inpaint-outpaint"
        else:
            raise ValueError("Invalid parameters for creation")
        if model is not None and model not in self.loaded_models:
            self.loaded_models.append(model)
        max_cached_models = os.environ.get("MAX_CACHED_MODELS", 3)
        if len(self.loaded_models) > max_cached_models:
            self.loaded_models = self.loaded_models[-max_cached_models:]

        data = json.dumps(params.model_dump())
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=data, headers=headers)
        # If we have a 422 here, print what the unprocessable entity is
        if response.status_code == 422:
            logger.warning(f"Unprocessable entity: {response.text}")
        response.raise_for_status()

        self.output = response.json()
        logger.debug(f"Response: {self.output}")
        job_id = self.output.get('job_id', None)
        if job_id is not None:
            return ResponseFcusApi.running(job_id)
        return ResponseFcusApi.error("Job ID not found", job_id)

    async def get_status(self, job_id: str) -> BaseResponse:
        output = await self._get_output(job_id)
        if output is None:
            return BaseResponse.error("Error getting job status")
        if not output:
            print(f"Job {job_id} is still running (or can't get output)")
            return BaseResponse.running(job_id)
        return BaseResponse.success(
            ResponseData(data=output, data_type=ResponseDataType.IMAGE, total_count=len(output)))

    async def upload_image(self, image_data: Any) -> str:
        pass

    async def get_models(self) -> List[str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_base_url}/v1/engines/all-models")
            response.raise_for_status()
            response_json = response.json()
            return response_json.get("model_filenames", [])

    async def test(self):
        async with httpx.AsyncClient() as client:
            url = f"{self.api_base_url}/docs"
            response = await client.get(url)
            if response.status_code == 200:
                return BaseResponse.active()
            else:
                return BaseResponse.error("Error testing connection")

    async def _get_output(self, job_id: str) -> Union[None, List[str]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_base_url}/v1/generation/query-job", params={'job_id': job_id})
            response.raise_for_status()
            response_json = response.json()
            status = response_json.get('job_status')
            logger.debug(f"Status: {status}")
            if status is None:
                return None
            if status != "Finished":
                return []
            outputs = [result.get('base64') for result in response_json.get('job_result', []) if result.get('finish_reason', "UNKNOWN") == "SUCCESS"]
            return outputs

    async def cache_model(self, model: str = "Juggernaut-XI-Prototype.safetensors") -> bool:
        # FCUS_API doesn't have a specific endpoint for caching models, so we just
        # Run a txt2img job with a very low resolution to load the model
        request = FcusTxt2Img().example()
        request.prompt = "foo"
        request.base_model_name = model
        request.aspect_ratios_selection = "64*64"
        response = await self.create(request)
        if response.status == JobStatus.FINISHED:
            return True
        return False