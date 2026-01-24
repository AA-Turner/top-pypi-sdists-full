from collections.abc import Iterable, Iterator
from typing import IO, TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

CustomAttributesHeader = str
EnableExplanationsHeader = str
EndpointName = str
ErrorCode = str
Header = str
InferenceComponentHeader = str
InferenceId = str
InputLocationHeader = str
InvocationTimeoutSecondsHeader = int
LogStreamArn = str
Message = str
NewSessionResponseHeader = str
RequestTTLSecondsHeader = int
SessionIdHeader = str
SessionIdOrNewSessionConstantHeader = str
StatusCode = int
TargetContainerHostnameHeader = str
TargetModelHeader = str
TargetVariantHeader = str


class InternalDependencyException(ServiceException):
    """Your request caused an exception with an internal dependency. Contact
    customer support.
    """

    code: str = "InternalDependencyException"
    sender_fault: bool = False
    status_code: int = 530


class InternalFailure(ServiceException):
    """An internal failure occurred."""

    code: str = "InternalFailure"
    sender_fault: bool = False
    status_code: int = 500


class InternalStreamFailure(ServiceException):
    """The stream processing failed because of an unknown error, exception or
    failure. Try your request again.
    """

    code: str = "InternalStreamFailure"
    sender_fault: bool = False
    status_code: int = 400


class ModelError(ServiceException):
    """Model (owned by the customer in the container) returned 4xx or 5xx error
    code.
    """

    code: str = "ModelError"
    sender_fault: bool = False
    status_code: int = 424
    OriginalStatusCode: StatusCode | None
    OriginalMessage: Message | None
    LogStreamArn: LogStreamArn | None


class ModelNotReadyException(ServiceException):
    """Either a serverless endpoint variant's resources are still being
    provisioned, or a multi-model endpoint is still downloading or loading
    the target model. Wait and try your request again.
    """

    code: str = "ModelNotReadyException"
    sender_fault: bool = False
    status_code: int = 429


class ModelStreamError(ServiceException):
    """An error occurred while streaming the response body. This error can have
    the following error codes:

    ModelInvocationTimeExceeded
       The model failed to finish sending the response within the timeout
       period allowed by Amazon SageMaker AI.

    StreamBroken
       The Transmission Control Protocol (TCP) connection between the client
       and the model was reset or closed.
    """

    code: str = "ModelStreamError"
    sender_fault: bool = False
    status_code: int = 400
    ErrorCode: ErrorCode | None


class ServiceUnavailable(ServiceException):
    """The service is unavailable. Try your call again."""

    code: str = "ServiceUnavailable"
    sender_fault: bool = False
    status_code: int = 503


class ValidationError(ServiceException):
    """Inspect your request and try again."""

    code: str = "ValidationError"
    sender_fault: bool = False
    status_code: int = 400


BodyBlob = bytes


class InvokeEndpointAsyncInput(ServiceRequest):
    EndpointName: EndpointName
    ContentType: Header | None
    Accept: Header | None
    CustomAttributes: CustomAttributesHeader | None
    InferenceId: InferenceId | None
    InputLocation: InputLocationHeader
    RequestTTLSeconds: RequestTTLSecondsHeader | None
    InvocationTimeoutSeconds: InvocationTimeoutSecondsHeader | None


class InvokeEndpointAsyncOutput(TypedDict, total=False):
    InferenceId: Header | None
    OutputLocation: Header | None
    FailureLocation: Header | None


class InvokeEndpointInput(ServiceRequest):
    Body: IO[BodyBlob]
    EndpointName: EndpointName
    ContentType: Header | None
    Accept: Header | None
    CustomAttributes: CustomAttributesHeader | None
    TargetModel: TargetModelHeader | None
    TargetVariant: TargetVariantHeader | None
    TargetContainerHostname: TargetContainerHostnameHeader | None
    InferenceId: InferenceId | None
    EnableExplanations: EnableExplanationsHeader | None
    InferenceComponentName: InferenceComponentHeader | None
    SessionId: SessionIdOrNewSessionConstantHeader | None


class InvokeEndpointOutput(TypedDict, total=False):
    Body: BodyBlob | IO[BodyBlob] | Iterable[BodyBlob]
    ContentType: Header | None
    InvokedProductionVariant: Header | None
    CustomAttributes: CustomAttributesHeader | None
    NewSessionId: NewSessionResponseHeader | None
    ClosedSessionId: SessionIdHeader | None


class InvokeEndpointWithResponseStreamInput(ServiceRequest):
    Body: IO[BodyBlob]
    EndpointName: EndpointName
    ContentType: Header | None
    Accept: Header | None
    CustomAttributes: CustomAttributesHeader | None
    TargetVariant: TargetVariantHeader | None
    TargetContainerHostname: TargetContainerHostnameHeader | None
    InferenceId: InferenceId | None
    InferenceComponentName: InferenceComponentHeader | None
    SessionId: SessionIdHeader | None


PartBlob = bytes


class PayloadPart(TypedDict, total=False):
    """A wrapper for pieces of the payload that's returned in response to a
    streaming inference request. A streaming inference response consists of
    one or more payload parts.
    """

    Bytes: PartBlob | None


class ResponseStream(TypedDict, total=False):
    """A stream of payload parts. Each part contains a portion of the response
    for a streaming inference request.
    """

    PayloadPart: PayloadPart | None
    ModelStreamError: ModelStreamError | None
    InternalStreamFailure: InternalStreamFailure | None


class InvokeEndpointWithResponseStreamOutput(TypedDict, total=False):
    Body: Iterator[ResponseStream]
    ContentType: Header | None
    InvokedProductionVariant: Header | None
    CustomAttributes: CustomAttributesHeader | None


class SagemakerRuntimeApi:
    service: str = "sagemaker-runtime"
    version: str = "2017-05-13"

    @handler("InvokeEndpoint")
    def invoke_endpoint(
        self,
        context: RequestContext,
        endpoint_name: EndpointName,
        body: IO[BodyBlob],
        content_type: Header | None = None,
        accept: Header | None = None,
        custom_attributes: CustomAttributesHeader | None = None,
        target_model: TargetModelHeader | None = None,
        target_variant: TargetVariantHeader | None = None,
        target_container_hostname: TargetContainerHostnameHeader | None = None,
        inference_id: InferenceId | None = None,
        enable_explanations: EnableExplanationsHeader | None = None,
        inference_component_name: InferenceComponentHeader | None = None,
        session_id: SessionIdOrNewSessionConstantHeader | None = None,
        **kwargs,
    ) -> InvokeEndpointOutput:
        """After you deploy a model into production using Amazon SageMaker AI
        hosting services, your client applications use this API to get
        inferences from the model hosted at the specified endpoint.

        For an overview of Amazon SageMaker AI, see `How It
        Works <https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works.html>`__.

        Amazon SageMaker AI strips all POST headers except those supported by
        the API. Amazon SageMaker AI might add additional headers. You should
        not rely on the behavior of headers outside those enumerated in the
        request syntax.

        Calls to ``InvokeEndpoint`` are authenticated by using Amazon Web
        Services Signature Version 4. For information, see `Authenticating
        Requests (Amazon Web Services Signature Version
        4) <https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-authenticating-requests.html>`__
        in the *Amazon S3 API Reference*.

        A customer's model containers must respond to requests within 60
        seconds. The model itself can have a maximum processing time of 60
        seconds before responding to invocations. If your model is going to take
        50-60 seconds of processing time, the SDK socket timeout should be set
        to be 70 seconds.

        Endpoints are scoped to an individual account, and are not public. The
        URL does not contain the account ID, but Amazon SageMaker AI determines
        the account ID from the authentication token that is supplied by the
        caller.

        :param endpoint_name: The name of the endpoint that you specified when you created the
        endpoint using the
        `CreateEndpoint <https://docs.
        :param body: Provides input data, in the format specified in the ``ContentType``
        request header.
        :param content_type: The MIME type of the input data in the request body.
        :param accept: The desired MIME type of the inference response from the model
        container.
        :param custom_attributes: Provides additional information about a request for an inference
        submitted to a model hosted at an Amazon SageMaker AI endpoint.
        :param target_model: The model to request for inference when invoking a multi-model endpoint.
        :param target_variant: Specify the production variant to send the inference request to when
        invoking an endpoint that is running two or more variants.
        :param target_container_hostname: If the endpoint hosts multiple containers and is configured to use
        direct invocation, this parameter specifies the host name of the
        container to invoke.
        :param inference_id: If you provide a value, it is added to the captured data when you enable
        data capture on the endpoint.
        :param enable_explanations: An optional JMESPath expression used to override the
        ``EnableExplanations`` parameter of the ``ClarifyExplainerConfig`` API.
        :param inference_component_name: If the endpoint hosts one or more inference components, this parameter
        specifies the name of inference component to invoke.
        :param session_id: Creates a stateful session or identifies an existing one.
        :returns: InvokeEndpointOutput
        :raises InternalFailure:
        :raises ServiceUnavailable:
        :raises ValidationError:
        :raises ModelError:
        :raises InternalDependencyException:
        :raises ModelNotReadyException:
        """
        raise NotImplementedError

    @handler("InvokeEndpointAsync")
    def invoke_endpoint_async(
        self,
        context: RequestContext,
        endpoint_name: EndpointName,
        input_location: InputLocationHeader,
        content_type: Header | None = None,
        accept: Header | None = None,
        custom_attributes: CustomAttributesHeader | None = None,
        inference_id: InferenceId | None = None,
        request_ttl_seconds: RequestTTLSecondsHeader | None = None,
        invocation_timeout_seconds: InvocationTimeoutSecondsHeader | None = None,
        **kwargs,
    ) -> InvokeEndpointAsyncOutput:
        """After you deploy a model into production using Amazon SageMaker AI
        hosting services, your client applications use this API to get
        inferences from the model hosted at the specified endpoint in an
        asynchronous manner.

        Inference requests sent to this API are enqueued for asynchronous
        processing. The processing of the inference request may or may not
        complete before you receive a response from this API. The response from
        this API will not contain the result of the inference request but
        contain information about where you can locate it.

        Amazon SageMaker AI strips all POST headers except those supported by
        the API. Amazon SageMaker AI might add additional headers. You should
        not rely on the behavior of headers outside those enumerated in the
        request syntax.

        Calls to ``InvokeEndpointAsync`` are authenticated by using Amazon Web
        Services Signature Version 4. For information, see `Authenticating
        Requests (Amazon Web Services Signature Version
        4) <https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-authenticating-requests.html>`__
        in the *Amazon S3 API Reference*.

        :param endpoint_name: The name of the endpoint that you specified when you created the
        endpoint using the
        `CreateEndpoint <https://docs.
        :param input_location: The Amazon S3 URI where the inference request payload is stored.
        :param content_type: The MIME type of the input data in the request body.
        :param accept: The desired MIME type of the inference response from the model
        container.
        :param custom_attributes: Provides additional information about a request for an inference
        submitted to a model hosted at an Amazon SageMaker AI endpoint.
        :param inference_id: The identifier for the inference request.
        :param request_ttl_seconds: Maximum age in seconds a request can be in the queue before it is marked
        as expired.
        :param invocation_timeout_seconds: Maximum amount of time in seconds a request can be processed before it
        is marked as expired.
        :returns: InvokeEndpointAsyncOutput
        :raises InternalFailure:
        :raises ServiceUnavailable:
        :raises ValidationError:
        """
        raise NotImplementedError

    @handler("InvokeEndpointWithResponseStream")
    def invoke_endpoint_with_response_stream(
        self,
        context: RequestContext,
        endpoint_name: EndpointName,
        body: IO[BodyBlob],
        content_type: Header | None = None,
        accept: Header | None = None,
        custom_attributes: CustomAttributesHeader | None = None,
        target_variant: TargetVariantHeader | None = None,
        target_container_hostname: TargetContainerHostnameHeader | None = None,
        inference_id: InferenceId | None = None,
        inference_component_name: InferenceComponentHeader | None = None,
        session_id: SessionIdHeader | None = None,
        **kwargs,
    ) -> InvokeEndpointWithResponseStreamOutput:
        """Invokes a model at the specified endpoint to return the inference
        response as a stream. The inference stream provides the response payload
        incrementally as a series of parts. Before you can get an inference
        stream, you must have access to a model that's deployed using Amazon
        SageMaker AI hosting services, and the container for that model must
        support inference streaming.

        For more information that can help you use this API, see the following
        sections in the *Amazon SageMaker AI Developer Guide*:

        -  For information about how to add streaming support to a model, see
           `How Containers Serve
           Requests <https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-inference-code.html#your-algorithms-inference-code-how-containe-serves-requests>`__.

        -  For information about how to process the streaming response, see
           `Invoke real-time
           endpoints <https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints-test-endpoints.html>`__.

        Before you can use this operation, your IAM permissions must allow the
        ``sagemaker:InvokeEndpoint`` action. For more information about Amazon
        SageMaker AI actions for IAM policies, see `Actions, resources, and
        condition keys for Amazon SageMaker
        AI <https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonsagemaker.html>`__
        in the *IAM Service Authorization Reference*.

        Amazon SageMaker AI strips all POST headers except those supported by
        the API. Amazon SageMaker AI might add additional headers. You should
        not rely on the behavior of headers outside those enumerated in the
        request syntax.

        Calls to ``InvokeEndpointWithResponseStream`` are authenticated by using
        Amazon Web Services Signature Version 4. For information, see
        `Authenticating Requests (Amazon Web Services Signature Version
        4) <https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-authenticating-requests.html>`__
        in the *Amazon S3 API Reference*.

        :param endpoint_name: The name of the endpoint that you specified when you created the
        endpoint using the
        `CreateEndpoint <https://docs.
        :param body: Provides input data, in the format specified in the ``ContentType``
        request header.
        :param content_type: The MIME type of the input data in the request body.
        :param accept: The desired MIME type of the inference response from the model
        container.
        :param custom_attributes: Provides additional information about a request for an inference
        submitted to a model hosted at an Amazon SageMaker AI endpoint.
        :param target_variant: Specify the production variant to send the inference request to when
        invoking an endpoint that is running two or more variants.
        :param target_container_hostname: If the endpoint hosts multiple containers and is configured to use
        direct invocation, this parameter specifies the host name of the
        container to invoke.
        :param inference_id: An identifier that you assign to your request.
        :param inference_component_name: If the endpoint hosts one or more inference components, this parameter
        specifies the name of inference component to invoke for a streaming
        response.
        :param session_id: The ID of a stateful session to handle your request.
        :returns: InvokeEndpointWithResponseStreamOutput
        :raises InternalFailure:
        :raises ServiceUnavailable:
        :raises ValidationError:
        :raises ModelError:
        :raises ModelStreamError:
        :raises InternalStreamFailure:
        """
        raise NotImplementedError
