"""
Provides classes and utilities to allow you to interact with an instance of the Kodexa
platform.
"""

from __future__ import annotations

import io
import json
import logging
import os
import time
from json import JSONDecodeError
from typing import Dict

import requests

from kodexa_document import Document
from kodexa_document.model.objects import (
    AssistantEvent,
    ChannelEvent,
    ContentEvent,
    ContentObject,
    DataObjectEvent,
    DocumentFamilyEvent,
    ExecutionEvent,
    ScheduledEvent,
    TaskEvent,
    WorkspaceEvent,
)
from kodexa_document.platform.client import KodexaClient, process_response

logger = logging.getLogger()


class PipelineStatistics:
    """A class to represent the statistics for processed documents."""

    def __init__(self):
        self.documents_processed = 0

    def processed_document(self, document):
        """Updates statistics based on this document completing processing."""
        self.documents_processed += 1


class PipelineContext:
    """Pipeline context provides access to information about pipeline execution.

    Attributes:
        execution_id (str): Unique identifier for the execution.
        statistics (PipelineStatistics): Statistics related to the pipeline.
        output_document: The final output document from the pipeline.
        content_objects (List): List of content objects.
        content_provider: Provider for the content.
        context (Dict): Contextual information.
        stop_on_exception (bool): Flag to indicate whether to stop on exception.
        current_document: The current document being processed in the pipeline.
        document_family: The document family.
        content_object: The content object.
        document_store: The document store.
        status_handler (function): Handler for status updates.
        cancellation_handler (function): Handler for cancellation requests.
    """

    def __init__(
        self,
        content_provider=None,
        existing_content_objects=None,
        context=None,
        execution_id=None,
        status_handler=None,
        cancellation_handler=None,
    ):
        if context is None:
            context = {}
        if existing_content_objects is None:
            existing_content_objects = []

        import uuid
        self.execution_id = str(uuid.uuid4()) if execution_id is None else execution_id
        self.statistics = PipelineStatistics()
        self.output_document = None
        self.content_objects = existing_content_objects
        self.content_provider = content_provider
        self.context = context
        self.stop_on_exception = True
        self.current_document = None
        self.document_family = None
        self.content_object = None
        self.document_store = None
        self.status_handler = status_handler
        self.cancellation_handler = cancellation_handler

    def set_output_document(self, output_document):
        """Sets the output document from the pipeline."""
        self.output_document = output_document

    def get_context(self):
        """Gets the context dictionary."""
        return self.context

    def update_status(self, status_message: str, progress=None, progress_max=None):
        """Updates the status of the pipeline.

        Args:
            status_message (str): The status message.
            progress (int, optional): The progress of the pipeline. Defaults to None.
            progress_max (int, optional): The maximum progress of the pipeline. Defaults to None.
        """
        if self.status_handler is not None:
            self.status_handler(status_message, progress, progress_max)

    def is_cancelled(self) -> bool:
        """Checks if the pipeline is cancelled.

        Returns:
            bool: True if cancelled, False otherwise.
        """
        if self.cancellation_handler is not None:
            return self.cancellation_handler()
        return False


class KodexaPlatform:
    """
    The KodexaPlatform object allows you to work with an instance of the Kodexa platform, allowing you to list, view and deploy
    components. Configure access using environment variables KODEXA_ACCESS_TOKEN and KODEXA_URL.
    """

    @staticmethod
    def get_client():
        """
        Get a Kodexa client.

        Returns:
            KodexaClient: An instance of the Kodexa client.
        """
        from kodexa_document.platform.client import KodexaClient

        return KodexaClient(KodexaPlatform.get_url(), KodexaPlatform.get_access_token())

    @staticmethod
    def get_access_token() -> str:
        """
        Get the access token from the KODEXA_ACCESS_TOKEN environment variable.

        Returns:
            str: The access token.

        Raises:
            Exception: If KODEXA_ACCESS_TOKEN is not set.
        """
        access_token = os.getenv("KODEXA_ACCESS_TOKEN")
        if access_token is None:
            raise Exception("No access token set, please set KODEXA_ACCESS_TOKEN environment variable")
        return access_token

    @staticmethod
    def get_url() -> str:
        """
        Get the URL to use to access a Kodexa Platform from the KODEXA_URL environment variable.

        Returns:
            str: The platform URL.

        Raises:
            Exception: If KODEXA_URL is not set.
        """
        url = os.getenv("KODEXA_URL")
        if url is None:
            raise Exception("No URL set, please set KODEXA_URL environment variable")
        return url

    @staticmethod
    def set_access_token(access_token: str):
        """
        Set the access token via the KODEXA_ACCESS_TOKEN environment variable.

        Args:
            access_token (str): The access token to use.
        """
        if access_token is not None:
            os.environ["KODEXA_ACCESS_TOKEN"] = access_token

    @staticmethod
    def set_url(url: str):
        """
        Set the platform URL via the KODEXA_URL environment variable.

        Args:
            url (str): The platform URL.
        """
        if url is not None:
            os.environ["KODEXA_URL"] = url

    @staticmethod
    def resolve_ref(ref: str):
        """
        Resolve the reference.

        Args:
            ref (str): The reference to resolve.

        Returns:
            list: A list containing the organization slug, slug, and version.
        """

        org_slug = ref.split("/")[0]
        slug = ref.split("/")[1].split(":")[0]

        version = None

        if len(ref.split("/")[1].split(":")) == 2:
            version = ref.split("/")[1].split(":")[1]

        return [org_slug, slug, version]

    @classmethod
    def get_server_info(cls):
        """
        Get server information.

        Returns:
            dict: The server information.
        """
        r = requests.get(
            f"{KodexaPlatform.get_url()}/api/overview",
            headers={
                "x-access-token": KodexaPlatform.get_access_token(),
                "cf-access-token": os.environ.get("CF_TOKEN", ""),
                "content-type": "application/json",
            },
        )
        if r.status_code == 401:
            raise Exception("Your access token was not authorized")
        if r.status_code == 200:
            try:
                return r.json()
            except JSONDecodeError:
                raise Exception("Unable to decode server information, check your access token")

        logger.warning(r.text)
        raise Exception(
            "Unable to get server information, check your platform settings"
        )

    @classmethod
    def get_tempdir(cls):
        """
        Get the temporary directory.

        Returns:
            str: The path to the temporary directory.
        """
        import tempfile

        return os.getenv("KODEXA_TMP", tempfile.gettempdir())


class RemoteSession:
    """A Session on the Kodexa platform for leveraging pipelines and services"""

    """A Session on the Kodexa platform for leveraging pipelines and services"""

    def __init__(self, session_type, slug):
        self.session_type = session_type
        self.slug = slug
        self.cloud_session = None

    def get_action_metadata(self, ref):
        """
        Download metadata for a specific action.

        Args:
            ref (str): The reference of the action.

        Returns:
            dict: The metadata of the action if the request is successful.
        """
        logger.debug(f"Downloading metadata for action {ref}")
        r = requests.get(
            f"{KodexaPlatform.get_url()}/api/actions/{ref.replace(':', '/')}",
            headers={"x-access-token": KodexaPlatform.get_access_token(),
                     "cf-access-token": os.environ.get("CF_TOKEN", "")},
        )
        if r.status_code == 401:
            raise Exception("Your access token was not authorized")
        if r.status_code == 200:
            return r.json()

        logger.warning(r.text)
        raise Exception(
            "Unable to get action metadata, check your reference and platform settings"
        )

    def start(self):
        """
        Start the session.
        """
        logger.info(f"Creating session {self.slug} ({KodexaPlatform.get_url()})")
        r = requests.post(
            f"{KodexaPlatform.get_url()}/api/sessions",
            params={self.session_type: self.slug},
            headers={"x-access-token": KodexaPlatform.get_access_token(),
                     "cf-access-token": os.environ.get("CF_TOKEN", "")},
        )

        process_response(r)

        self.cloud_session = json.loads(r.text)

    def execution_action(self, document, options, attach_source, context):
        """
        Execute an action in the session.

        Args:
            document (Document): The document to be processed.
            options (dict): The options for the action.
            attach_source (bool): Whether to attach the source to the call.
            context (Context): The context of the execution.

        Returns:
            dict: The execution result.
        """
        files = {}
        if attach_source:
            raise NotImplementedError("attach_source is not supported without connectors")
        else:
            files["document"] = document.to_kddb()

        data = {
            "options": json.dumps(options),
            "document_metadata_json": json.dumps(document.metadata),
            "context": json.dumps(context.context),
        }

        logger.info(f"Executing session {self.cloud_session.id}")
        r = requests.post(
            f"{KodexaPlatform.get_url()}/api/sessions/{self.cloud_session.id}/execute",
            params={self.session_type: self.slug, "documentVersion": document.version},
            data=data,
            headers={"x-access-token": KodexaPlatform.get_access_token(),
                     "cf-access-token": os.environ.get("CF_TOKEN", "")},
            files=files,
        )
        try:
            if r.status_code == 200:
                execution = json.loads(r.text)
            else:
                logger.warning(
                    "Execution creation failed ["
                    + r.text
                    + "], response "
                    + str(r.status_code)
                )
                raise Exception(
                    "Execution creation failed ["
                    + r.text
                    + "], response "
                    + str(r.status_code)
                )
        except JSONDecodeError:
            logger.warning(
                "Unable to handle response ["
                + r.text
                + "], response "
                + str(r.status_code)
            )
            raise

        return execution

    def wait_for_execution(self, execution):
        """
        Wait for the execution to finish.

        Args:
            execution (dict): The execution to wait for.

        Returns:
            dict: The execution result.
        """
        status = execution.status
        while execution.status == "PENDING" or execution.status == "RUNNING":
            r = requests.get(
                f"{KodexaPlatform.get_url()}/api/sessions/{self.cloud_session.id}/executions/{execution.id}",
                headers={"x-access-token": KodexaPlatform.get_access_token(),
                         "cf-access-token": os.environ.get("CF_TOKEN", "")},
            )
            try:
                execution = json.loads(r.text)
            except JSONDecodeError:
                logger.warning("Unable to handle response [" + r.text + "]")
                raise

            if status != execution.status:
                logger.info(f"Status changed from {status} -> {execution.status}")
                status = execution.status

            time.sleep(5)

        if status == "FAILED":
            logger.warning("Execution has failed")
            for step in execution.steps:
                if step.status == "FAILED":
                    logger.warning(
                        f"Step {step.name} has failed. {step.exceptionDetails.message}."
                    )

                    if step.exceptionDetails.errorType == "Validation":
                        logger.warning(
                            "Additional validation information has been provided:"
                        )
                        for validation_error in step.exceptionDetails.validationErrors:
                            logger.warning(
                                f"- {validation_error.option} : {validation_error.message}"
                            )

                    if step.exceptionDetails.help:
                        logger.warning(
                            f"Additional help is available:\n\n{step.exceptionDetails.help}"
                        )

                    raise Exception(f"Processing has failed on step {step.name}")

            raise Exception("Processing has failed, no steps seem to have failed")

        return execution

    def get_output_document(self, execution):
        """
        Get the output document from a given execution.

        Args:
            execution (dict): The execution holding the document.

        Returns:
            Document: The output document (or None if there isn't one).
        """
        if execution.outputId:
            logger.info(f"Downloading output document [{execution.outputId}]")
            doc = requests.get(
                f"{KodexaPlatform.get_url()}/api/sessions/{self.cloud_session.id}/executions/{execution.id}/objects/{execution.outputId}",
                headers={"x-access-token": KodexaPlatform.get_access_token(),
                         "cf-access-token": os.environ.get("CF_TOKEN", "")},
            )
            return Document.from_kddb(doc.content)

        logger.info("No output document")
        return None


class RemoteStep:
    """Allows you to interact with a step that has been deployed in the Kodexa platform"""

    """Allows you to interact with a step that has been deployed in the Kodexa platform"""

    def __init__(self, ref, step_type="ACTION", attach_source=False, options=None, conditional=None):
        if options is None:
            options = {}
        self.ref = ref
        self.step_type = step_type
        self.attach_source = attach_source
        self.options = options
        self.conditional = conditional

    def to_dict(self):
        """Converts the RemoteStep object to a dictionary.

        Returns:
            dict: Dictionary representation of the RemoteStep object.
        """
        return {"ref": self.ref, "step_type": self.step_type, "options": self.options, "conditional": self.conditional}

    def get_name(self):
        """Generates a name for the RemoteStep object.

        Returns:
            str: Name of the RemoteStep object.
        """
        return f"Remote Action ({self.ref})"

    def process(self, document, context):
        """Processes the document and context using the RemoteStep.

        Args:
            document (Document): The document to be processed.
            context (Context): The context for processing.

        Returns:
            Document: The processed document.
        """
        cloud_session = RemoteSession("service", self.ref)
        cloud_session.start()

        logger.info(f"Loading metadata for {self.ref}")
        action_metadata = cloud_session.get_action_metadata(self.ref)

        requires_source = False
        if "requiresSource" in action_metadata["metadata"]:
            requires_source = action_metadata["metadata"]["requiresSource"]

        execution = cloud_session.execution_action(
            document,
            self.options,
            self.attach_source if self.attach_source else requires_source,
            context,
        )

        logger.debug("Waiting for remote execution")
        execution = cloud_session.wait_for_execution(execution)

        logger.debug("Downloading the result document")
        result_document = cloud_session.get_output_document(execution)

        logger.debug("Set the context to match the context from the execution")
        context.context = execution.context

        return result_document if result_document else document

    def to_configuration(self):
        """Returns a dictionary representing the configuration information for the step.

        Returns:
            dict: Dictionary representing the configuration of the step.
        """
        return {"ref": self.ref, "options": self.options, "conditional": self.conditional}


class EventHelper:
    """Helper class for handling events.

    Attributes:
        event (ExecutionEvent): The execution event instance.
    """

    def __init__(self, event: ExecutionEvent):
        self.event: ExecutionEvent = event

    @staticmethod
    def get_base_event(event_dict: Dict):
        """Returns the base event based on the event type.

        Args:
            event_dict (Dict): The event dictionary.

        Raises:
            Exception: If the event type is unknown.
        """
        if event_dict["type"] == "assistant":
            return AssistantEvent(**event_dict)
        if event_dict["type"] == "content":
            return ContentEvent(**event_dict)
        if event_dict["type"] == "scheduled":
            return ScheduledEvent(**event_dict)
        if event_dict["type"] == "channel":
            return ChannelEvent(**event_dict)
        if event_dict["type"] == "documentFamily":
            return DocumentFamilyEvent(**event_dict)
        if event_dict["type"] == "dataObject":
            return DataObjectEvent(**event_dict)
        if event_dict["type"] == "workspace":
            return WorkspaceEvent(**event_dict)
        if event_dict["type"] == "task":
            return TaskEvent(**event_dict)

        raise f"Unknown event type {event_dict}"

    def log(self, message: str):
        """Logs a message to the Kodexa platform.

        Args:
            message (str): The message to log.
        """
        response = requests.post(
            f"{KodexaPlatform.get_url()}/api/sessions/{self.event.session_id}/executions/{self.event.execution.id}/logs",
            json=[{"entry": message}],
            headers={"x-access-token": KodexaPlatform.get_access_token(),
                     "cf-access-token": os.environ.get("CF_TOKEN", "")},
            timeout=300,
        )
        if response.status_code != 200:
            print(f"Logging failed {response.status_code}", flush=True)

    def get_content_object(self, content_object_id: str):
        """Gets a content object from the Kodexa platform.

        Args:
            content_object_id (str): The ID of the content object.

        Raises:
            Exception: If the content object cannot be found.

        Returns:
            io.BytesIO: The content object.
        """
        logger.info(
            f"Getting content object {content_object_id} in event {self.event.id} in execution {self.event.execution.id}"
        )

        co_response = requests.get(
            f"{KodexaPlatform.get_url()}/api/sessions/{self.event.session_id}/executions/{self.event.execution.id}/objects/{content_object_id}",
            headers={"x-access-token": KodexaPlatform.get_access_token(),
                     "cf-access-token": os.environ.get("CF_TOKEN", "")},
            timeout=300
        )
        process_response(co_response)
        return io.BytesIO(co_response.content)

    def put_content_object(
            self, content_object: ContentObject, content
    ) -> ContentObject:
        """Puts a content object to the Kodexa platform.

        Args:
            content_object (ContentObject): The content object.
            content: The content.

        Raises:
            Exception: If the content object cannot be posted back.

        Returns:
            ContentObject: The posted content object.
        """
        import time
        
        # Calculate content size for logging
        content_size = 0
        if hasattr(content, 'seek') and hasattr(content, 'tell'):
            # File-like object - get size without consuming
            current_pos = content.tell()
            content.seek(0, 2)  # Seek to end
            content_size = content.tell()
            content.seek(current_pos)  # Restore position
        elif hasattr(content, '__len__'):
            content_size = len(content)
        
        files = {"content": content}
        content_object_json = json.dumps(content_object.model_dump(by_alias=True))
        data = {"contentObjectJson": content_object_json}
        
        url = f"{KodexaPlatform.get_url()}/api/sessions/{self.event.session_id}/executions/{self.event.execution.id}/objects"
        
        logger.info(
            f"Posting content object to execution - "
            f"session_id={self.event.session_id}, "
            f"execution_id={self.event.execution.id}, "
            f"content_size={content_size} bytes ({content_size / 1024 / 1024:.2f} MB), "
            f"content_object_json_size={len(content_object_json)} bytes"
        )
        logger.debug(f"PUT content object URL: {url}")
        
        start_time = time.time()
        co_response = requests.post(
            url,
            data=data,
            headers={"x-access-token": KodexaPlatform.get_access_token(),
                     "cf-access-token": os.environ.get("CF_TOKEN", "")},
            files=files,
            timeout=300
        )
        elapsed_time = time.time() - start_time

        logger.info(
            f"Content object POST response - "
            f"status_code={co_response.status_code}, "
            f"response_size={len(co_response.content)} bytes, "
            f"elapsed_time={elapsed_time:.2f}s"
        )
        
        process_response(co_response)

        logger.info("Content object posted successfully")

        return ContentObject.model_validate(co_response.json())

    def build_pipeline_context(self, event) -> PipelineContext:
        """Builds a pipeline context.

        Returns:
            PipelineContext: The pipeline context.
        """
        context = PipelineContext(
            context={}, content_provider=self, execution_id=self.event.execution.id
        )

        if isinstance(event, dict):
            event = self.get_base_event(event)

        if isinstance(event, DocumentFamilyEvent):
            # Can we get the document family
            dfe:DocumentFamilyEvent = self.event
            if dfe.document_family:
                logger.info(f"Setting document family for context: {dfe.document_family}")
                context.document_family = dfe.document_family
                logger.info(f"Getting document store for family: {context.document_family.store_ref}")
                context.document_store = KodexaClient().get_object_by_ref("store", context.document_family.store_ref)
        if isinstance(event, ContentEvent):
            ce:ContentEvent = self.event
            if ce.content_object:
                logger.info(f"Setting content object for context: {ce.content_object}")
                context.content_object = ce.content_object
                context.document_family = ce.document_family
                logger.info(f"Getting document store for content object: {context.content_object.store_ref}")
                context.document_store = KodexaClient().get_object_by_ref("store", context.content_object.store_ref)
        logger.info("Returning context")
        return context

    def get_input_document(self, context):
        """Gets the input document.

        Args:
            context: The context.

        Returns:
            Document: The input document.
        """
        for content_object in self.event.execution.content_objects:
            if content_object.id == self.event.input_id:
                input_document_bytes = self.get_content_object(self.event.input_id)
                logger.info("Loading KDDB document")
                input_document = Document.from_kddb(input_document_bytes.read())
                logger.info("Loaded KDDB document")
                context.content_object = content_object
                input_document.uuid = context.content_object.id

                if content_object.store_ref is not None:
                    context.document_store = KodexaClient().get_object_by_ref(
                        "store", content_object.store_ref
                    )

                return input_document
