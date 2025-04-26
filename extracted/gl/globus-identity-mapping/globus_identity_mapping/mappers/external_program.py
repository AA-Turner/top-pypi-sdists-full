from __future__ import annotations

import logging
import shlex
import typing as t
from subprocess import PIPE, Popen

import marshmallow as ma
import marshmallow.validate
from typing_extensions import Self

from ..errors import IdentityMappingError, InvalidMappingError
from ..schema import IdentityMappingConfiguration
from .abstract import IdentityMapping


class MappingInputSchema(ma.Schema):
    _DATA_TYPE = "identity_mapping_input#1.0.0"
    DATA_TYPE = ma.fields.Str(
        dump_default=_DATA_TYPE, validate=[ma.validate.Equal(_DATA_TYPE)]
    )

    identities = ma.fields.List(ma.fields.Raw)


class MappingResultSchema(ma.Schema):
    id = ma.fields.UUID()
    output = ma.fields.Str()


class MappingOutputSchema(ma.Schema):
    _DATA_TYPE = "identity_mapping_output#1.0.0"
    DATA_TYPE = ma.fields.Str(
        dump_default=_DATA_TYPE, validate=[ma.validate.Equal(_DATA_TYPE)]
    )
    result = ma.fields.List(ma.fields.Nested(MappingResultSchema))


class ExternalMappingConfigurationDocument(IdentityMappingConfiguration):
    command: list[str | int | float]


identity_mapping_input_schema = MappingInputSchema()
identity_mapping_output_schema = MappingOutputSchema()


class ExternalIdentityMapping(IdentityMapping):
    """
    The ExternalIdentityMapping class implements an extension point for
    administrators to implement their own identity mapping algorithm as an
    external program.

    The GCS Manager will run the configured program and arguments in a sub
    process. In addition to any arguments specified in the configuration
    document, the following command-line options will be added:

    The `-c` option along with an argument which is the UUID of a
    GCS connector.

    The `-s` option along with its argument which is the UUID of the
    storage gateway mapping the identity.

    The `-a` command-line option indicates that the GCS Manager wants to
    receive output containing all mappings for the given identity set. If
    present, the program will receive an input containing at least one identity
    resource as input, and may return as many mappings as can be computed from
    the identities. If not present, the program will receive exactly one object
    in the identities orray and may only return a single mapping for that
    identity. If it returns multiple mappings, only the first is used by
    the GCS Manager.

    The GCS Manager communicates between the external program using
    JSON-formatted input and output data passed via stdin and stdout.

    Input consists of a JSON object containing two properties: `DATA_TYPE`
    which indicates the version of the input document, currently
    `identity_mapping_input#1.0.0` and `identities`, which contains a list of
    identity resource obtained from Globus Auth.

    For example:

    .. code-block:: json

        {
            "DATA_TYPE": "identity_mapping_input#1.0.0",
            "identities": [
                {
                    "id": "9cf5a1d2-41c4-4925-b0bb-f5e0a16c98ab",
                    "username": "user@example.com",
                    "identity_provider": "1f8ba017-6224-43ad-a42f-03059574ba38"
                },
                {
                    "id": "67c31064-1e5f-4d78-b687-5fbea3d3e05a",
                    "username": "user2@example.org",
                    "identity_provider": "05f6f886-9277-42b9-836e-81559f337ac3"
                },
                {
                    "id": "4787931e-b999-412e-97f9-a7a24c79ad71",
                    "username": "user3@example.info",
                    "identity_provider": "05f6f886-9277-42b9-836e-81559f337ac3"
                }
            ]
        }

    Output is an object containing two properties, `DATA_TYPE` which
    indicates the version of the output document, currently
    `identity_mapping_output#1.0.0`, and `result`, which contains a list of
    objects with the properties `id` and `output` The `id` is the value of one
    of the `id` properties of one of the input identities, and the `output` is
    a connector-specific user identifier that indicates the result of the
    mapping.

    For example:

    .. code-block:: json

        {
            "DATA_TYPE": "identity_mapping_output#1.0.0",
            "result": [
                {
                    "id": "67c31064-1e5f-4d78-b687-5fbea3d3e05a",
                    "output": "user3"
                },
            ]
        }
    """

    DATA_TYPE = "external_identity_mapping#1.0.0"
    mapping_timeout_s = 5  # (seconds) time limit for external program to respond

    def __init__(
        self,
        cmd: str,
        *cmd_args,
        storage_gateway: str,
        connector: str,
    ) -> None:
        """
        :param `*args`:
            List of strings which are the path to the external command and the
            command line arguments to pass to the module. Additional parameters
            `-s`, `-c`, and `-a` will be automatically added to this
            command-line as described in the class documentation.

        :param storage_gateway:
            String containing the UUID of the storage gateway to perform the
            mapping for.
        :param connector: String containing the UUID of the connector
            to perform the mapping for.
        """
        assert connector is not None
        assert storage_gateway is not None

        self._log: logging.Logger | None = None

        self.command = [str(cmd)]
        self.command.extend(map(str, cmd_args))
        self.connector = connector
        self.storage_gateway = storage_gateway

    def __repr__(self) -> str:
        args = "', '".join(self.command)
        sg, conn = self.storage_gateway, self.connector
        sg = "storage_gateway=None" if sg is None else f"storage_gateway='{sg}'"
        conn = "connector=None" if conn is None else f"connector='{conn}'"
        return f"{type(self).__name__}('{args}', {sg}, {conn})"

    @classmethod
    def _from_mapping_document(
        cls,
        mapping_document: ExternalMappingConfigurationDocument,
        connector: str | None = None,
        storage_gateway: str | None = None,
    ) -> Self:
        # The protocol allows for connector and storage_gateway to be None,
        # but this class demands it; so `assert` instead of changing the sig
        assert connector is not None, "Connector is required"
        assert storage_gateway is not None, "Connector is required"
        return cls(
            str(mapping_document["command"][0]),
            *mapping_document["command"][1:],
            connector=connector,  # noqa: arg-type
            storage_gateway=storage_gateway,
        )

    def map_identity(self, identity_data: t.Mapping[str, str]) -> str | None:
        """
        Map a single identity object to a username for this particular
        connector and storage gateway.

        :param identity_data:
            A dict containing the identity assertions from Globus Auth.

        :raises errors.InternalServerError:
            Error executing the external mapping program, or the output
            from the program is not in an understood format.
        """
        cmd = self.command + ["-c", self.connector, "-s", self.storage_gateway]
        cmd_str = shlex.join(cmd)
        p = Popen(cmd, universal_newlines=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)

        input_data = identity_mapping_input_schema.dumps(
            {"identities": [identity_data]}
        )

        stdout, stderr = p.communicate(input_data, timeout=self.mapping_timeout_s)
        self.log.debug(
            # fmt: off
            "\n  command: %s"
            "\n    stdin: %s"
            "\n   stdout: %s"
            "\n   stderr: %s",
            # fmt: on
            cmd_str,
            input_data,
            stdout,
            stderr,
        )

        if p.returncode != 0:
            msg = (
                "Error mapping identity\n"
                f"    command: {cmd_str}\n"
                f"  exit code: {p.returncode}\n"
                f"      stdin: {input_data}\n"
                f"     stdout: {stdout}\n"
                f"     stderr: {stderr}"
            )
            raise IdentityMappingError(msg)

        if stdout:
            try:
                output = identity_mapping_output_schema.loads(stdout)
            except Exception as e:
                msg = (
                    "The mapping application yielded an invalid result:\n"
                    f"  exception: ({type(e).__name__}) {e}\n"
                    f"    command: {cmd_str}\n"
                    f"      stdin: {input_data}\n"
                    f"     stdout: {stdout}\n"
                    f"     stderr: {stderr}"
                )
                raise IdentityMappingError(msg) from e

            if output["result"]:
                first_result = output["result"][0]
                if str(first_result["id"]) != identity_data["id"]:
                    msg = (
                        "Expected first result to match identity data (id field);"
                        " assuming response is invalid.\n"
                        f"  command: {cmd_str}\n"
                        f"   parsed: {output}"
                    )
                    raise InvalidMappingError(msg)

                return first_result["output"]

        return None

    def map_identities(
        self, identity_data: t.Iterable[t.Mapping[str, str]]
    ) -> list[dict[str, list[str]]]:
        """
        Map all identities from the associated input list to local usernames
        that can potentially access the configured Storage Gateway

        :param identity_data: List of identity assertions from Globus Auth

        :returns:
            List of mappings from the `id` property of the input data
            to a list of local username strings that the identity maps to.

        :raises errors.InternalServerError:
            Error executing the external mapping program, or the output
            from the program is not in an understood format.
        """
        results: list[dict[str, list[str]]] = []

        cmd = self.command + ["-c", self.connector, "-s", self.storage_gateway, "-a"]
        cmd_str = shlex.join(cmd)
        p = Popen(cmd, universal_newlines=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)

        input_data = identity_mapping_input_schema.dumps({"identities": identity_data})
        stdout, stderr = p.communicate(input_data, timeout=self.mapping_timeout_s)
        self.log.debug(
            # fmt: off
            "\n  command: %s"
            "\n    stdin: %s"
            "\n   stdout: %s"
            "\n   stderr: %s",
            # fmt: on
            cmd_str,
            input_data,
            stdout,
            stderr,
        )

        if p.returncode != 0:
            msg = (
                "Error mapping identities\n"
                f"    command: {cmd_str}\n"
                f"  exit code: {p.returncode}\n"
                f"      stdin: {input_data}\n"
                f"     stdout: {stdout}\n"
                f"     stderr: {stderr}"
            )
            raise IdentityMappingError(msg)

        if stdout:
            input_ids = tuple(i["id"] for i in identity_data)
            try:
                output = identity_mapping_output_schema.loads(stdout)
            except Exception as e:
                msg = (
                    "The mapping application yielded an invalid result:\n"
                    f"  exception: ({type(e).__name__}) {e}\n"
                    f"    command: {cmd_str}\n"
                    f"      stdin: {input_data}\n"
                    f"     stdout: {stdout}\n"
                    f"     stderr: {stderr}"
                )
                raise IdentityMappingError(msg) from e

            result: dict[str, list[str]] = {}

            for o in output["result"]:
                output_id = str(o["id"])
                if output_id not in input_ids:
                    raise InvalidMappingError("Invalid ID in result")
                if output_id not in result:
                    result[output_id] = []
                result[output_id].append(o["output"])
            results.append(result)
        return results

    @property
    def log(self) -> logging.Logger:
        if not self._log:
            self._log = logging.getLogger(__file__)
        return self._log

    @log.setter
    def log(self, logger: logging.Logger):
        self._log = logger

    @log.deleter
    def log(self):
        self._log = None
