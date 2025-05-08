from datetime import timedelta
import functools
from fireworks.client.api_client import FireworksClient
from fireworks.client.chat import Chat as FireworksChat
from fireworks.client.chat_completion import ChatCompletionV2 as FireworksChatCompletion
from typing import (
    AsyncGenerator,
    Generator,
    Iterable,
    Literal,
    Optional,
    Union,
    overload,
)
from fireworks.gateway import Gateway
from fireworks.control_plane.generated.protos.gateway import (
    AutoscalingPolicy,
    DeployedModelState,
    Deployment,
    DeploymentState,
    Model,
)
import asyncio
import logging
import os
from openai.types.chat.chat_completion import ChatCompletion as OpenAIChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from fireworks._util import run_coroutine_in_appropriate_loop, async_lru_cache

# Configure logger with a consistent format for better debugging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False  # Prevent duplicate logs

if os.environ.get("FIREWORKS_SDK_DEBUG"):
    logger.setLevel(logging.DEBUG)


class ChatCompletion:
    def __init__(self, llm: "LLM"):
        self._client = FireworksChatCompletion(llm._client)
        self._llm = llm

    @overload
    def create(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: Literal[False] = False,
        extra_headers=None,
        **kwargs,
    ) -> OpenAIChatCompletion:
        pass

    @overload
    def create(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: Literal[True] = True,
        extra_headers=None,
        **kwargs,
    ) -> Generator[ChatCompletionChunk, None, None]:
        pass

    def create(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: bool = False,
        extra_headers=None,
        **kwargs,
    ) -> Union[OpenAIChatCompletion, Generator[ChatCompletionChunk, None, None]]:
        # Use the helper method to handle the coroutine execution
        run_coroutine_in_appropriate_loop(self._llm._ensure_deployment_ready())
        model_id = run_coroutine_in_appropriate_loop(self._llm.model_id())
        return self._client.create(
            model=model_id,
            prompt_or_messages=messages,
            stream=stream,
            extra_headers=extra_headers,
            **kwargs,
        )

    @overload
    async def acreate(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: Literal[False] = False,
        extra_headers=None,
        **kwargs,
    ) -> OpenAIChatCompletion: ...

    @overload
    async def acreate(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: Literal[True] = True,
        extra_headers=None,
        **kwargs,
    ) -> AsyncGenerator[ChatCompletionChunk, None]:
        pass

    async def acreate(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        stream: bool = False,
        extra_headers=None,
        **kwargs,
    ) -> Union[OpenAIChatCompletion, AsyncGenerator[ChatCompletionChunk, None]]:
        await self._llm._ensure_deployment_ready()
        model_id = await self._llm.model_id()
        resp_or_generator = self._client.acreate(  # type: ignore
            model=model_id,
            prompt_or_messages=messages,
            stream=stream,
            extra_headers=extra_headers,
            **kwargs,
        )
        if stream:
            return resp_or_generator  # type: ignore
        else:
            return await resp_or_generator  # type: ignore


class Chat:
    def __init__(self, llm: "LLM", model):
        self.completions = ChatCompletion(llm)


class LLM:

    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = "https://api.fireworks.ai/inference/v1",
    ):
        self._client = FireworksClient(api_key=api_key, base_url=base_url)
        if not model.startswith("accounts/fireworks/models/"):
            self._model = f"accounts/fireworks/models/{model}"
        else:
            self._model = model
        self.chat = Chat(self, self._model)
        self._api_key = api_key
        self._gateway = Gateway(api_key=api_key)

        # aggressive defaults for experimentation to save on cost
        self._autoscaling_policy: AutoscalingPolicy = AutoscalingPolicy(
            scale_up_window=timedelta(seconds=1),
            scale_down_window=timedelta(minutes=1),
            scale_to_zero_window=timedelta(minutes=5),
        )

    async def is_serverless(self):
        return await self._is_available_on_serverless()

    @async_lru_cache()
    async def _is_available_on_serverless(self):
        logger.debug(f"Checking if {self._model} is available on serverless")
        models = await self._gateway.list_models(parent="accounts/fireworks", include_deployed_model_refs=True)

        # find model in models
        model = next((m for m in models if m.name == self._model), None)
        if model is None:
            raise ValueError(
                f"Model {self._model} not available on Fireworks. See https://fireworks.ai/models for available models."
            )
        logger.debug(f"Found model {self._model} on under fireworks account")
        is_serverless = self._is_model_on_serverless_account(model)
        logger.debug(f"Model {self._model} is {'serverless' if is_serverless else 'not serverless'}")
        return is_serverless

    @staticmethod
    def _is_model_on_serverless_account(model: Model) -> bool:
        """
        Check if the model is deployed on a serverless-enabled account.

        Args:
            model: The model object to check

        Returns:
            bool: True if the model is deployed on a supported serverless account, False otherwise
        """
        if model.deployed_model_refs:
            for ref in model.deployed_model_refs:
                if (
                    hasattr(ref, "state")
                    and (ref.state == DeployedModelState.DEPLOYED or ref.state == "DEPLOYED")
                    and hasattr(ref, "deployment")
                    and ref.deployment
                ):
                    # Check if deployment is on a supported account
                    if (
                        ref.deployment.startswith("accounts/fireworks/")
                        or ref.deployment.startswith("accounts/yi-01-ai/")
                        or ref.deployment.startswith("accounts/sentientfoundation/")
                    ):
                        return True
        return False

    async def _query_existing_deployment(self):
        """
        Queries all deployments for the model and returns the first one (for now).
        TODO: should only return the deployment with the same configurations that affect quality and performance.
        """
        deployments = await self._gateway.list_deployments(filter=f'base_model="{self._model}"')
        if len(deployments) == 0:
            return None
        # TODO: filter by configurations that affect quality (like quantization) and performance (like speculative decoding, replicas, ngram speculation, etc.)
        return deployments[0]

    async def _ensure_deployment_ready(self) -> None:
        """
        If a deployment is inferred for this LLM, ensure it's deployed and
        ready. A deployment is required if the model is not available on
        serverless or this LLM has custom configurations.
        """
        if await self._is_available_on_serverless():
            return

        logger.debug(f"Model {self._model} is not available on serverless, checking for existing deployment")
        deployment = await self._query_existing_deployment()

        if deployment is None:
            logger.debug(f"No existing deployment found, creating deployment for {self._model}")
            deployment = await self._gateway.create_deployment(self._model, self._autoscaling_policy)

            # poll deployment status until it's ready
            while deployment.state != DeploymentState.READY:
                # wait for 1 second
                await asyncio.sleep(1)
                deployment = await self._gateway.get_deployment(deployment.name)

            logger.debug(f"Deployment {deployment.name} is ready, using deployment")
        else:
            logger.debug(f"Deployment {deployment.name} already exists, checking if it needs to be scaled up")
            # if autoscaling policy is not equal, update it
            if not self._is_autoscaling_policy_equal(deployment):
                logger.debug(f"Updating autoscaling policy for {deployment.name}")
                start_time = asyncio.get_event_loop().time()

                await self._gateway.update_deployment(deployment.name, self._autoscaling_policy)

                # poll until deployment is ready
                while deployment.state != DeploymentState.READY:
                    await asyncio.sleep(1)
                    deployment = await self._gateway.get_deployment(deployment.name)

                elapsed_time = asyncio.get_event_loop().time() - start_time
                logger.debug(f"Deployment policy update completed in {elapsed_time:.2f} seconds")

            if deployment.replica_count == 0:
                logger.debug(f"Deployment {deployment.name} is not ready, scaling to 1 replica")
                start_time = asyncio.get_event_loop().time()
                await self._gateway.scale_deployment(deployment.name, 1)

                # Poll until deployment has at least one replica
                last_log_time = 0
                while deployment.replica_count == 0:
                    current_time = asyncio.get_event_loop().time()
                    await asyncio.sleep(1)
                    deployment = await self._gateway.get_deployment(deployment.name)
                    if current_time - last_log_time >= 10:
                        elapsed_so_far = current_time - start_time
                        logger.debug(
                            f"Waiting for deployment {deployment.name} to scale up, current replicas: {deployment.replica_count}, elapsed time: {elapsed_so_far:.2f}s"
                        )
                        last_log_time = current_time

                total_scale_time = asyncio.get_event_loop().time() - start_time
                logger.debug(f"Deployment {deployment.name} scaled up in {total_scale_time:.2f} seconds")
            logger.debug(f"Deployment {deployment.name} is ready, using deployment")

    async def scale_to_zero(self) -> Optional[Deployment]:
        """
        Sends a request to scale the deployment to 0 replicas but does not wait for it to complete.
        """
        deployment = await self.deployment()
        if deployment is None:
            return None
        await self._gateway.scale_deployment(deployment.name, 0)
        return deployment

    async def scale_to_1_replica(self):
        """
        Scales the deployment to at least 1 replica.
        """
        deployment = await self.deployment()
        if deployment is None:
            return
        await self._gateway.scale_deployment(deployment.name, 1)

    def _is_autoscaling_policy_equal(self, deployment: Deployment) -> bool:
        return (
            deployment.autoscaling_policy.scale_up_window == self._autoscaling_policy.scale_up_window
            and deployment.autoscaling_policy.scale_down_window == self._autoscaling_policy.scale_down_window
            and deployment.autoscaling_policy.scale_to_zero_window == self._autoscaling_policy.scale_to_zero_window
        )

    @async_lru_cache()
    async def deployment(self) -> Optional[Deployment]:
        await self._ensure_deployment_ready()
        deployment = await self._query_existing_deployment()
        return deployment

    @property
    def model(self):
        return self._model

    async def model_id(self):
        """
        Returns the model ID, which is the model name plus the deployment name
        if it exists. This is used for the "model" arg when calling the model.
        """
        if await self.is_serverless():
            return self.model
        deployment = await self.deployment()
        if deployment is None:
            return self.model
        return f"{self.model}#{deployment.name}"

    def __repr__(self):
        deployment = self.deployment.cache  # type: ignore
        if deployment is not None:
            return f"LLM(model={self.model}, deployment={deployment})"
        return f"LLM(model={self.model})"


class LLMConfig:
    model: str
    autoscaling_policy: Optional[AutoscalingPolicy] = None
