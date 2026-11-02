"""Typed root submission with automatic immutable publication."""

from collections.abc import Mapping
from dataclasses import replace
from typing import ParamSpec, TypeVar
from uuid import uuid4

from labqoat._generated.new_compute_run import NewComputeRun
from labqoat._generated.compute_publication import ComputePublication
from labqoat._generated.run import Run
from labqoat._generated.transport import Transport
from labqoat.assets_client import AssetsClient
from labqoat.base_client import BaseClient
from labqoat.compute.function import Function
from labqoat.compute.publication import Publication
from labqoat.compute.run_options import RunOptions
from labqoat.compute.upload_memo import UploadMemo
from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonValue
from labqoat.schemas.schema_document import SchemaDocument

P = ParamSpec("P")
R = TypeVar("R")


class Submission(BaseClient):
    """Accept one durable root invocation without waiting for its image build or execution."""

    def __init__(self, transport: Transport, uploads: UploadMemo | None = None) -> None:
        """Bind the explicit transport and an optional memory of archives the service already holds."""
        super().__init__(transport)
        self._uploads = uploads

    def submit(
        self, function: Function[P, R], args: tuple[object, ...], kwargs: Mapping[str, object], options: RunOptions
    ) -> Run:
        """Encode arguments before uploading source and retain one operation key through request transport."""
        arguments: dict[str, JsonValue] = function.encode(args, kwargs)
        function.capture_for(arguments)
        publisher = Publication(AssetsClient(self._transport), self._uploads)
        try:
            return self.accept(function, arguments, publisher.capture(function), options)
        except ApiError as error:
            if self._uploads is None or "source_not_available" not in str(error):
                raise
        self._uploads.forget()
        return self.accept(function, arguments, publisher.capture(function), options)

    @staticmethod
    def compose(
        function: Function[P, R],
        arguments: dict[str, JsonValue],
        publication: ComputePublication,
        options: RunOptions,
    ) -> NewComputeRun:
        """The run request for an invocation, as a submission sends it and an endpoint launches its replicas."""
        publication = replace(publication, function=function.capture_for(arguments))
        schema = SchemaDocument.capture(dict(publication.function.input_schema))
        return NewComputeRun(
            name=f"{function.app_name}/{publication.function.name}",
            publication=publication,
            arguments=arguments,
            input_schema_digest=schema.digest,
            seed=options.seed,
            location=options.location,
            resources=dict(options.resources.to_dict()) if options.resources is not None else None,
        )

    def accept(
        self,
        function: Function[P, R],
        arguments: dict[str, JsonValue],
        publication: ComputePublication,
        options: RunOptions,
    ) -> Run:
        """Accept a typed invocation against an already captured immutable publication."""
        request = Submission.compose(function, arguments, publication, options)
        path = "/api/v1/runs"
        response = self.send_json("POST", path, request.to_dict(), idempotency_key=options.key or str(uuid4()))
        return self.decode(response, path, Run.from_dict)
