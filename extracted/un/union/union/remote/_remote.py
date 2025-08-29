from __future__ import annotations

import asyncio
import datetime
import logging
import os
import typing
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from functools import partial
from typing import AsyncGenerator, List, Optional, Union

import grpc
from flyteidl.core import artifact_id_pb2 as art_id
from flyteidl.event.cloudevents_pb2 import CloudEventNodeExecution, CloudEventTaskExecution, CloudEventWorkflowExecution
from flyteidl.service.identity_pb2 import UserInfoRequest, UserInfoResponse
from flyteidl.service.identity_pb2_grpc import IdentityServiceStub
from flytekit import BlobType, ImageSpec, Resources
from flytekit.clients.friendly import SynchronousFlyteClient
from flytekit.configuration import Config
from flytekit.core.artifact import ArtifactQuery, Partitions, TimePartition
from flytekit.core.type_engine import LiteralsResolver, TypeEngine
from flytekit.exceptions import user as user_exceptions
from flytekit.exceptions.user import FlyteEntityNotExistException, FlyteInvalidInputException
from flytekit.models.literals import Blob, BlobMetadata, Literal, Scalar
from flytekit.remote import FlyteRemote
from flytekit.remote.entities import FlyteLaunchPlan, FlyteTask, FlyteWorkflow
from flytekit.remote.executions import FlyteNodeExecution, FlyteTaskExecution, FlyteWorkflowExecution
from flytekit.tools.interactive import ipython_check
from flytekit.tools.translator import Options
from grpc import Channel

from union._config import (
    _DEFAULT_DOMAIN,
    _DEFAULT_PROJECT_BYOC,
    ConfigSource,
    ConfigWithSource,
    _config_from_api_key,
    _get_config_obj,
    _get_default_project,
    _get_env_var,
    _get_organization,
)
from union._interceptor import update_client_with_interceptor
from union.app._models import App
from union.artifacts import Artifact
from union.artifacts._utils import construct_search_artifact_request
from union.internal.app.app_definition_pb2 import App as AppIDL
from union.internal.artifacts import artifacts_pb2, artifacts_pb2_grpc
from union.internal.authorizer.authorizer_pb2_grpc import AuthorizerServiceStub
from union.internal.hooks.hooks_pb2_grpc import HooksServiceStub
from union.internal.hooks.payload_pb2 import (
    AcknowledgeEventRequest,
    AcknowledgeEventResponse,
    EventFilters,
    EventType,
    StreamEventsRequest,
    StreamEventsResponse,
)
from union.internal.identity import user_service_pb2_grpc
from union.internal.identity.app_service_pb2_grpc import AppsServiceStub
from union.internal.identity.user_service_pb2_grpc import UserServiceStub
from union.internal.imagebuilder import definition_pb2 as image_definition__pb2
from union.internal.imagebuilder import payload_pb2 as image_payload__pb2
from union.internal.imagebuilder import service_pb2_grpc as image_service_pb2_grpc
from union.internal.secret.definition_pb2 import Secret, SecretIdentifier
from union.internal.secret.payload_pb2 import GetSecretRequest, ListSecretsRequest
from union.internal.secret.secret_pb2_grpc import SecretServiceStub
from union.remote._app_template_factory import AppTemplate, HuggingFaceModelInfo, get_app_templates_for_model

logger = logging.getLogger(__name__)

SERVERLESS_VANITY_URLS = {
    "https://serverless-1.us-east-2.s.union.ai": "https://serverless.union.ai",
    "https://serverless-preview.canary.unionai.cloud": "https://serverless.canary.union.ai",
    "https://serverless-gcp.cloud-staging.union.ai": "https://serverless.staging.union.ai",
}


@dataclass
class DeployableModel:
    artifact: Artifact
    app_templates: List[AppTemplate]


_hf_download_image = ImageSpec(
    name="hfhub-cache",
    builder="union",
    packages=["huggingface_hub[hf_transfer]==0.33.2", "union[vllm]>=0.1.190"],
    apt_packages=["build-essential", "gcc"],
)


_PROJECT_ENV_VARS = ["UNION_CURRENT_PROJECT", "FLYTE_INTERNAL_EXECUTION_PROJECT"]
_DOMAIN_ENV_VARS = ["UNION_CURRENT_DOMAIN", "FLYTE_INTERNAL_EXECUTION_DOMAIN"]

_get_default_project_from_env = partial(_get_env_var, env_vars=_PROJECT_ENV_VARS)
_get_default_domain_from_env = partial(_get_env_var, env_vars=_DOMAIN_ENV_VARS)


class UnionRemote(FlyteRemote):
    def __init__(
        self,
        config: typing.Optional[Union[Config, str]] = None,
        default_project: typing.Optional[str] = None,
        default_domain: typing.Optional[str] = None,
        data_upload_location: str = "flyte://my-s3-bucket/",
        interactive_mode_enabled: typing.Optional[bool] = None,
        **kwargs,
    ):
        from union._config import _get_image_builder_priority
        from union.ucimage._image_builder import _register_union_image_builder

        if config is None:
            config = _get_config_obj(config, default_to_union_semantics=True)
        else:
            config_with_source = ConfigWithSource(config=config, source=ConfigSource.REMOTE)
            config = _get_config_obj(config_with_source, default_to_union_semantics=True)

        # Creating a UnionRemote within a task uses the execution's project and domain
        # We use the internal environment variables here, so that it works without a flytekit entrypoint. For example,
        # serving does not use a flyte entrypoint.
        if default_project is None:
            default_project, _ = _get_default_project_from_env()
            if default_project is None:
                default_project = _get_default_project(_DEFAULT_PROJECT_BYOC, cfg_obj=config)

        if default_domain is None:
            default_domain, _ = _get_default_domain_from_env()

        if default_domain is None:
            default_domain = _DEFAULT_DOMAIN

        # register Union image builder when getting remote so it's available for
        # jupyter notebook task and workflow execution.
        _register_union_image_builder(_get_image_builder_priority(config.platform.endpoint))

        # We set `interactive_mode_enabled=False` here and then adjust interactive_mode_enabled
        # mode afterwards to avoid the "Jupyter notebook and interactive task support is still alpha."
        # warning
        super().__init__(
            config=config,
            default_project=default_project,
            default_domain=default_domain,
            data_upload_location=data_upload_location,
            interactive_mode_enabled=False,
            **kwargs,
        )
        if interactive_mode_enabled is None:
            interactive_mode_enabled = ipython_check()
        self._interactive_mode_enabled = interactive_mode_enabled

        self._artifacts_client = None
        self._images_client = None
        self._secret_client = None
        self._users_client = None
        self._apps_service_client = None
        self._hooks_sync_client = None
        self._hooks_async_client = None
        self._authorizer_service_client = None
        self._user_service_client = None

        from union.remote._app_remote import AppRemote

        self._app_remote = AppRemote(union_remote=self, default_project=default_project, default_domain=default_domain)

    @classmethod
    def from_api_key(
        cls,
        api_key: str,
        default_project: typing.Optional[str] = None,
        default_domain: typing.Optional[str] = _DEFAULT_DOMAIN,
        data_upload_location: str = "flyte://my-s3-bucket/",
        **kwargs,
    ) -> "UnionRemote":
        """Call this if you want to directly instantiate a UnionRemote from an API key"""
        return cls(
            config=_config_from_api_key(api_key),
            default_project=default_project,
            default_domain=default_domain,
            data_upload_location=data_upload_location,
            **kwargs,
        )

    @property
    def client(self) -> SynchronousFlyteClient:
        """Return a SynchronousFlyteClient for additional operations."""
        if not self._client_initialized:
            client = SynchronousFlyteClient(self.config.platform, **self._kwargs)
            org = _get_organization(self.config.platform, channel=client._channel)
            self._client = update_client_with_interceptor(client, org)
            self._client_initialized = True

        return self._client

    @property
    def sync_channel(self) -> Channel:
        """Return channel from client. This channel already has the org passed in dynamically by the interceptor."""
        return self.client._channel

    def async_channel(self) -> grpc.aio.Channel:
        from union.filesystems._endpoint import _create_secure_channel_from_config

        try:
            return self._async_channel
        except AttributeError:
            self._async_channel = _create_secure_channel_from_config(
                self.config.platform,
                self.client._channel,
            )
            return self._async_channel

    @property
    def hooks_sync_client(self) -> HooksServiceStub:
        if self._hooks_sync_client:
            return self._hooks_sync_client

        self._hooks_sync_client = HooksServiceStub(self.sync_channel)
        return self._hooks_sync_client

    @property
    def hooks_async_client(self) -> HooksServiceStub:
        if self._hooks_async_client:
            return self._hooks_async_client

        self._hooks_async_client = HooksServiceStub(self.async_channel)
        return self._hooks_async_client

    def _get_stream(self, event_types: EventFilters) -> AsyncGenerator[StreamEventsResponse, None]:
        request = StreamEventsRequest(filters=event_types)
        return self.hooks_async_client.StreamEvents(request)

    def _ack_event(self, event_id: str) -> AcknowledgeEventResponse:
        ack_request = AcknowledgeEventRequest(id=event_id)
        return self.hooks_sync_client.AcknowledgeEvent(ack_request)

    def generate_console_http_domain(self) -> str:
        default_console_http_domain = super().generate_console_http_domain()
        return SERVERLESS_VANITY_URLS.get(default_console_http_domain, default_console_http_domain)

    def generate_console_url(
        self,
        entity: typing.Union[
            FlyteWorkflowExecution,
            FlyteNodeExecution,
            FlyteTaskExecution,
            FlyteWorkflow,
            FlyteTask,
            FlyteLaunchPlan,
            Artifact,
        ],
    ):
        """
        Generate a UnionAI console URL for the given Flyte remote endpoint.
        It will also handle Union AI specific entities like Artifacts.

        This will automatically determine if this is an execution or an entity
        and change the type automatically.
        """
        org = _get_organization(self.config.platform)
        if isinstance(entity, Artifact):
            url = f"{self.generate_console_http_domain()}/console/projects/{entity.project}/domains/{entity.domain}/artifacts/{entity.name}/versions/{entity.version}"  # noqa: E501
        else:
            url = super().generate_console_url(entity)
        if org is None:
            return url

        console_http_domain = self.generate_console_http_domain()
        old_prefix = f"{console_http_domain}/console/"
        new_prefix = f"{console_http_domain}/org/{org}/"

        return url.replace(old_prefix, new_prefix)

    @property
    def artifacts_client(self) -> artifacts_pb2_grpc.ArtifactRegistryStub:
        if self._artifacts_client:
            return self._artifacts_client

        self._artifacts_client = artifacts_pb2_grpc.ArtifactRegistryStub(self.sync_channel)
        return self._artifacts_client

    @property
    def users_client(self) -> user_service_pb2_grpc.UserServiceStub:
        if self._users_client:
            return self._users_client

        self._users_client = user_service_pb2_grpc.UserServiceStub(self.sync_channel)
        return self._users_client

    def search_artifacts(
        self,
        project: typing.Optional[str] = None,
        domain: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
        artifact_key: typing.Optional[art_id.ArtifactKey] = None,
        query: typing.Optional[ArtifactQuery] = None,
        partitions: typing.Optional[Union[Partitions, typing.Dict[str, str]]] = None,
        time_partition: typing.Optional[Union[datetime.datetime, TimePartition]] = None,
        group_by_key: bool = False,
        limit: int = 100,
    ) -> typing.List[Artifact]:
        if limit > 500:
            raise ValueError("Limit cannot exceed 500")

        union_artifacts = []
        next_token = None
        while len(union_artifacts) < limit:
            search_request = construct_search_artifact_request(
                project=project or self.default_project,
                domain=domain or self.default_domain,
                name=name,
                artifact_key=artifact_key,
                query=query,
                partitions=partitions,
                time_partition=time_partition,
                group_by_key=group_by_key,
                limit=100,
                token=next_token,
            )
            search_response = self.artifacts_client.SearchArtifacts(search_request)
            artifact_list = search_response.artifacts
            next_token = search_response.token

            if len(artifact_list) == 0:
                break

            for al in artifact_list:
                ua = Artifact.from_flyte_idl(al)
                # assigned here because the resolver has an implicit dependency on the remote's context
                # can move into artifact if we are okay just using the current context.
                ua.resolver = LiteralsResolver(literals={ua.name: ua.literal}, variable_map=None, ctx=self.context)
                union_artifacts.append(ua)

        return union_artifacts

    def _get_latest_artifact_uri(self, artifact_key: art_id.ArtifactKey) -> str:
        """Gets the latest artifact URI for the given artifact key."""
        req = artifacts_pb2.SearchArtifactsRequest(artifact_key=artifact_key, limit=1)
        resp = self.artifacts_client.SearchArtifacts(req)
        assert len(resp.artifacts) == 1, f"Expected 1 artifact, got {len(resp.artifacts)}"
        return resp.artifacts[0].metadata.uri

    def get_artifact(
        self,
        uri: typing.Optional[str] = None,
        artifact_key: typing.Optional[art_id.ArtifactKey] = None,
        artifact_id: typing.Optional[art_id.ArtifactID] = None,
        query: typing.Optional[typing.Union[art_id.ArtifactQuery, ArtifactQuery]] = None,
        get_details: bool = False,
    ) -> typing.Optional[Artifact]:
        """
        Get the specified artifact.

        :param uri: An artifact URI.
        :param artifact_key: An artifact key.
        :param artifact_id: The artifact ID.
        :param query: An artifact query.
        :param get_details: A bool to indicate whether or not to return artifact details.
        :return: The artifact as persisted in the service.
        """

        if query:
            if isinstance(query, ArtifactQuery):
                query_idl = query.to_flyte_idl()
            else:
                query_idl = query

            query_idl = art_id.ArtifactQuery(uri=self._get_latest_artifact_uri(query_idl.artifact_id.artifact_key))
        elif uri:
            query_idl = art_id.ArtifactQuery(uri=uri)
        elif artifact_key:
            query_idl = art_id.ArtifactQuery(uri=self._get_latest_artifact_uri(artifact_key))
        elif artifact_id:
            query_idl = art_id.ArtifactQuery(artifact_id=artifact_id)
        else:
            raise ValueError("One of uri, key, id")
        req = artifacts_pb2.GetArtifactRequest(query=query_idl, details=get_details)
        resp = self.artifacts_client.GetArtifact(req)
        a = Artifact.from_flyte_idl(resp.artifact)
        if a.literal and a.name:
            # assigned here because the resolver has an implicit dependency on the remote's context
            # can move into artifact if we are okay just using the current context.
            a.set_resolver(LiteralsResolver(literals={a.name: a.literal}, variable_map=None, ctx=self.context))
        return a

    def _execute(
        self,
        entity: typing.Union[FlyteTask, FlyteWorkflow, FlyteLaunchPlan],
        inputs: typing.Dict[str, typing.Any],
        project: typing.Optional[str] = None,
        domain: typing.Optional[str] = None,
        execution_name: typing.Optional[str] = None,
        execution_name_prefix: typing.Optional[str] = None,
        options: typing.Optional[Options] = None,
        wait: bool = False,
        type_hints: typing.Optional[typing.Dict[str, typing.Type]] = None,
        overwrite_cache: typing.Optional[bool] = None,
        envs: typing.Optional[typing.Dict[str, str]] = None,
        tags: typing.Optional[typing.List[str]] = None,
        cluster_pool: typing.Optional[str] = None,
        **kwargs,
    ) -> FlyteWorkflowExecution:
        resolved_inputs = {}
        for k, v in inputs.items():
            if isinstance(v, artifacts_pb2.Artifact):
                lit = v.spec.value
                resolved_inputs[k] = lit
            elif isinstance(v, Artifact):
                if v.literal is not None:
                    lit = v.literal
                elif v.to_id_idl() is not None:
                    fetched_artifact = self.get_artifact(artifact_id=v.concrete_artifact_id)
                    if not fetched_artifact:
                        raise user_exceptions.FlyteValueException(
                            v.concrete_artifact_id, "Could not find artifact with ID given"
                        )
                    lit = fetched_artifact.literal
                else:
                    raise user_exceptions.FlyteValueException(
                        v, "When binding input to Artifact, either the Literal or the ID must be set"
                    )
                resolved_inputs[k] = lit
            else:
                resolved_inputs[k] = v

        return super()._execute(
            entity,
            resolved_inputs,
            project=project,
            domain=domain,
            execution_name=execution_name,
            execution_name_prefix=execution_name_prefix,
            options=options,
            wait=wait,
            type_hints=type_hints,
            overwrite_cache=overwrite_cache,
            envs=envs,
            tags=tags,
            cluster_pool=cluster_pool,
            **kwargs,
        )

    def create_artifact(self, artifact: Artifact) -> Artifact:
        """
        Create an artifact in FlyteAdmin.

        :param artifact: The artifact to create.
        :return: The artifact as persisted in the service.
        """
        # Two things can happen here -
        #  - the call to to_literal may upload something, in the case of an offloaded data type.
        #    - if this happens, the upload request should already return the created Artifact object.
        if artifact.literal is None:
            with self.remote_context() as ctx:
                lt = artifact.literal_type or TypeEngine.to_literal_type(artifact.python_type)
                lit = TypeEngine.to_literal(ctx, artifact.python_val, artifact.python_type, lt)
                artifact.literal_type = lt.to_flyte_idl()
                if artifact.card:
                    card_key, card_val = artifact.card.serialize_to_string(ctx, artifact.name)
                    lit.set_metadata({card_key: card_val})
                artifact.literal = lit.to_flyte_idl()
        else:
            if artifact.literal_type is None:
                raise ValueError("Cannot create an artifact without a literal type set and a literal value present.")

        if artifact.project is None:
            artifact.project = self.default_project
        if artifact.domain is None:
            artifact.domain = self.default_domain
        create_request = Artifact.to_create_request(artifact)
        logging.debug(f"CreateArtifact request {create_request}")
        resp = self.artifacts_client.CreateArtifact(create_request)
        logging.debug(f"CreateArtifact response {resp}")
        # TODO artifact does not de-dupe on version, simply creates a new one, even for exact same partitions and data
        return Artifact.from_flyte_idl(resp.artifact)

    def deploy_app(self, app: App, project: Optional[str] = None, domain: Optional[str] = None) -> AppIDL:
        """
        Deploy an application.

        :param app: Application to deploy.
        :param project: Project name. If None, uses default_project.
        :param project: Domain name. If None, uses default_domain.
        :return: The App IDL for the deployed application.
        """
        return self._app_remote.deploy(app, project=project, domain=domain)

    def stop_app(self, name: str, project: Optional[str] = None, domain: Optional[str] = None):
        """
        Stop an application.

        :param name: Name of application to stop.
        :param project: Project name. If None, uses default_project.
        :param project: Domain name. If None, uses default_domain.
        :return: The App IDL for the stopped application.
        """
        return self._app_remote.stop(name=name, project=project, domain=domain)

    def _has_file_extension(self, file_path) -> bool:
        _, ext = os.path.splitext(file_path)
        return bool(ext)

    def get(self, uri: typing.Optional[str] = None) -> typing.Optional[typing.Union[LiteralsResolver, Literal, bytes]]:
        if not uri.startswith("union://"):
            # Assume this is the default behavior and this function is being called with a flyte uri
            return super().get(uri)
        if self._has_file_extension(uri):
            blob_dimensionality = BlobType.BlobDimensionality.SINGLE
        else:
            blob_dimensionality = BlobType.BlobDimensionality.MULTIPART
        return Literal(
            scalar=Scalar(
                blob=Blob(
                    metadata=BlobMetadata(
                        type=BlobType(
                            format="",
                            dimensionality=blob_dimensionality,
                        ),
                    ),
                    uri=uri,
                )
            )
        )

    def _create_model_from_hf(
        self,
        *,
        info: HuggingFaceModelInfo,
        hf_token_key: str,
        union_api_key: str,
        project: typing.Optional[str] = None,
        domain: typing.Optional[str] = None,
        retry: int = 0,
        resources: Optional[Resources] = None,
        accelerator: Optional[str] = None,
    ) -> FlyteWorkflowExecution:
        """
        This executes a background task to cache a model from Hugging Face and returns the handle to the execution.

        :param info: The model info.
        :param project: The project where the model will be stored.
        :param domain: The domain where the model will be stored.
        :param retry: This can be used to force a new artifact to be created with the same name and an incremented
            version,
        :param resources: Specify compute resource requests for your task.
        :param accelerator: The accelerator to use for downloading, (optionally) sharding, and caching hugging face
            model.
        :return: The model artifact.
        """
        # TODO maybe we should verify all requirements are met - 1. validate model 2. validate token exists
        # and launch the execution with name=commit
        if project is None:
            project = self.default_project
        if domain is None:
            domain = self.default_domain

        if not self._secret_exists(union_api_key, project=project, domain=domain):
            msg = f"Secret named: {union_api_key} does not exist. Please create one with `union create secret`"
            raise ValueError(msg)

        from union.remote._cache_model import create_hf_model_cache_workflow

        image = self._get_hf_hub_download_image()
        model_cache_wf, source_path, additional_context = create_hf_model_cache_workflow(
            image, hf_token_key, union_api_key, resources=resources, accelerator=accelerator
        )

        mod_name = ".".join(model_cache_wf.name.split(".")[:-1])

        # TODO: Once with_overrides supports `secret_requests` in the model_cache_wf defined in
        # create_hf_model_cache_workflow, with a workflow using `with_overrides` on
        # requests and secret_requests. and remove this dynamic patch.
        with self._patch_version_from_hash(additional_context):
            wf = self.register_script(model_cache_wf, module_name=mod_name, source_path=source_path)

        inputs = {"info": info}
        inputs["retry"] = retry or 0
        inputs["hf_token_key"] = hf_token_key

        return self.execute(wf, inputs=inputs, project=project, domain=domain)

    @contextmanager
    def _patch_version_from_hash(self, additional_context: list[str]):
        """Patches _version_from_hash to provide additional context."""
        _version_from_hash = self._version_from_hash

        def _patch_version_from_hash(*args, **kwargs):
            return _version_from_hash(*args, *additional_context, **kwargs)

        self._version_from_hash = _patch_version_from_hash
        yield
        self._version_from_hash = _version_from_hash

    @property
    def images_client(self) -> image_service_pb2_grpc.ImageServiceStub:
        if self._images_client:
            return self._images_client

        self._images_client = image_service_pb2_grpc.ImageServiceStub(self.sync_channel)
        return self._images_client

    @property
    def secret_client(self) -> SecretServiceStub:
        if self._secret_client:
            return self._secret_client

        self._secret_client = SecretServiceStub(self.sync_channel)
        return self._secret_client

    @property
    def apps_service_client(self) -> AppsServiceStub:
        if self._apps_service_client:
            return self._apps_service_client

        self._apps_service_client = AppsServiceStub(self.sync_channel)
        return self._apps_service_client

    @property
    def authorizer_service_client(self) -> AuthorizerServiceStub:
        if self._authorizer_service_client:
            return self._authorizer_service_client

        self._authorizer_service_client = AuthorizerServiceStub(self.sync_channel)
        return self._authorizer_service_client

    @property
    def user_service_client(self) -> UserServiceStub:
        if self._user_service_client:
            return self._user_service_client

        self._user_service_client = UserServiceStub(self.sync_channel)
        return self._user_service_client

    def _get_secrets(self, project: Optional[str] = None, domain: Optional[str] = None) -> List[Secret]:
        per_cluster_tokens, has_next = None, True
        stub = self.secret_client

        secrets = []

        # There are tenants that do not org scoped secrets, so error we assume there are no
        # secrets in that scope
        with suppress(FlyteInvalidInputException):
            while has_next:
                request = ListSecretsRequest(domain=domain, project=project, limit=20)
                if per_cluster_tokens:
                    request.per_cluster_tokens.update(per_cluster_tokens)
                response = stub.ListSecrets(request)
                per_cluster_tokens = response.per_cluster_tokens
                has_next = any(v for _, v in per_cluster_tokens.items() if v)

                secrets.extend(response.secrets)

        return secrets

    def _secret_exists(self, name: str, project: Optional[str] = None, domain: Optional[str] = None) -> bool:
        """
        Return True if secret name exists that accepts project and domain.
        """
        stub = self.secret_client

        if project is None and domain is None:
            project_domain_pairs = [(None, None)]
        elif project is not None:
            project_domain_pairs = [(None, None), (project, None)]
        else:
            project_domain_pairs = [(None, None), (project, None), (project, domain)]

        for project_, domain_ in project_domain_pairs:
            request = GetSecretRequest(id=SecretIdentifier(name=name, project=project_, domain=domain_))
            try:
                stub.GetSecret(request)
                return True
            except Exception:
                continue

        return False

    def _get_image_fqin(self, name: str) -> str:
        if self.config.platform.endpoint.startswith("localhost"):
            # For sandbox testing, assume that we always want to rebuild
            raise FlyteEntityNotExistException("Running in sandbox")
        image_id = image_definition__pb2.ImageIdentifier(name=name)
        org = _get_organization(self.config.platform, channel=self.sync_channel)
        req = image_payload__pb2.GetImageRequest(id=image_id, organization=org)
        resp = self.images_client.GetImage(req)
        return resp.image.fqin

    def _get_hf_hub_download_image(self) -> ImageSpec:
        # TODO: The backend should provide the hfhub-cache image
        return _hf_download_image

    def _get_deployable_engine_container(self, engine) -> str:
        # TODO The backend should provide the serving image
        supported_engines = {"vllm": "ghcr.io/unionai-oss/serving-vllm:0.1.16"}
        if engine not in supported_engines:
            concat_supported_engines = ", ".join(supported_engines)
            msg = f"Supported engines are: {concat_supported_engines}. Got: {engine}"
            raise ValueError(msg)

        return supported_engines[engine]

    def _get_deployable_model(self, uri: str) -> DeployableModel:
        """
        Get a deployable model artifact from Union. This will return the model artifact object.

        :param uri: The URI of the model artifact.
        :return: The DeployableModel object, which contains AppTemplates and the model artifact.
        """
        artifact = self.get_artifact(uri=uri)
        if artifact is None:
            raise ValueError(f"Model artifact not found at URI: {uri}")
        app_templates = get_app_templates_for_model(model=artifact)
        return DeployableModel(artifact=artifact, app_templates=app_templates)

    def _user_info(self) -> UserInfoResponse:
        """
        Query the user info.
        """
        client = IdentityServiceStub(self.sync_channel)
        return client.UserInfo(UserInfoRequest())

    async def stream_execution_events(
        self,
        event_count: Optional[int] = None,
        include_workflow_executions: bool = False,
        include_task_executions: bool = False,
        include_node_executions: bool = False,
    ) -> AsyncGenerator[Union[CloudEventWorkflowExecution, CloudEventNodeExecution, CloudEventTaskExecution], None]:
        """
        Stream execution events from the given tenant. This is a generator that yields events as they are received.

        Events are guaranteed to be delivered at least once, and clients must implement handling for potentially
        out-of-order event processing. Events will be retransmitted until acknowledged, with acknowledgment occurring
        automatically upon normal return from the caller.
        Note: if an exception is raised during event processing, the acknowledgment will not occur, and the event
        will be redelivered in a subsequent transmission.

        Args:
            event_count: Number of events to receive before closing the stream. If None, receive unlimited events.
            include_workflow_executions: Whether to include workflow execution events
            include_task_executions: Whether to include task execution events
            include_node_executions: Whether to include node execution events

        Returns:
            An async generator that yields execution events of the specified types
        """
        event_types = []
        if include_workflow_executions:
            event_types.append(EventType.WORKFLOW_EXECUTION)
        if include_task_executions:
            event_types.append(EventType.TASK_EXECUTION)
        if include_node_executions:
            event_types.append(EventType.NODE_EXECUTION)

        stream = self._get_stream(EventFilters(event_types=event_types))

        # Convert None to -1 to represent infinite events
        remaining = -1 if event_count is None else event_count

        try:
            async for response in stream:
                if remaining == 0:
                    break

                # Pull event from response object and yield it
                if response.HasField("workflow_execution"):
                    yield response.workflow_execution
                elif response.HasField("node_execution"):
                    yield response.node_execution
                elif response.HasField("task_execution"):
                    yield response.task_execution
                else:
                    logger.error("Received an unknown event type")

                # Acknowledge the event
                # N.B.: since this is a blocking call happening inside a generator, we
                # need to execute the ack_event call in a separate thread.
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, lambda: self._ack_event(response.id))

                # Decrement counter if we're tracking a specific count
                if remaining > 0:
                    remaining -= 1

        except Exception as e:
            logger.warning(f"Error streaming events: {e}")
            raise
