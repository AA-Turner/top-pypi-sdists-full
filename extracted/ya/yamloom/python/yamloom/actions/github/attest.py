from __future__ import annotations
from yamloom import Permissions

from typing import TYPE_CHECKING

from ...expressions import context, StringExpression
from ..._yamloom import ActionStep
from ..types import (
    Oboollike,
    Oboolstr,
    Ointlike,
    Ostr,
    Ostrlike,
    StringLike,
)

if TYPE_CHECKING:
    from collections.abc import Mapping


__all__ = ['AttestBuildProvenance']


class AttestBuildProvenance(ActionStep):
    """Generate provenance attestations for build artifacts.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    subject_path
        Path to the artifact serving as the subject of the attestation. Must
        specify exactly one of ``subject_path``, ``subject_digest``, or
        ``subject_checksums``. May contain a glob pattern or list of paths (total
        subject count cannot exceed 1024).
    subject_digest
        Digest of the subject for which provenance will be generated. Must be in
        the form ``algorithm:hex_digest`` (e.g. ``sha256:abc123...``). Must specify
        exactly one of ``subject_path``, ``subject_digest``, or
        ``subject_checksums``.
    subject_name
        Subject name as it should appear in the attestation. Required when
        identifying the subject with ``subject_digest``.
    subject_checksums
        Path to checksums file containing digest and name of subjects for
        attestation. Must specify exactly one of ``subject_path``,
        ``subject_digest``, or ``subject_checksums``.
    push_to_registry
        Whether to push the provenance statement to the image registry. Requires
        that ``subject_name`` specify the fully-qualified image name and that
        ``subject_digest`` be specified. Defaults to false.
    create_storage_record
        Whether to create a storage record for the artifact. Requires that
        ``push_to_registry`` is set to true. Defaults to true.
    show_summary
        Whether to attach a list of generated attestations to the workflow run
        summary page. Defaults to true.
    github_token
        The GitHub token used to make authenticated API requests.
    args
        The inputs for a Docker container which are passed to the container's entrypoint.
        This is a subkey of the ``with`` key of the generated step.
    entrypoint
        Overrides the Docker ENTRYPOINT in the action's Dockerfile or sets one if it was not
        specified. Accepts a single string defining the executable to run (note that this is
        different from Docker's ENTRYPOINT instruction which has both a shell and exec form).
        This is a subkey of the ``with`` key of the generated step.
    condition
        A boolean expression which must be met for the step to run. Note that this represents
        the ``if`` key in the actual YAML file.
    id
        A unique identifier for the step which can be referenced in expressions.
    env
        Used to specify environment variables for the step.
    continue_on_error
        Prevents the job from failing if this step fails.
    timeout_minutes
        The maximum number of minutes to let the step run before GitHub automatically
        cancels it (defaults to 360 if not specified).

    Returns
    -------
    Step
        The generated attest build provenance step.

    See Also
    --------
    GitHub repository: https://github.com/actions/attest-build-provenance
    """

    recommended_permissions = Permissions(
        id_token='write', attestations='write', artifact_metadata='write'
    )

    @classmethod
    def bundle_path(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['bundle-path']

    @classmethod
    def attestation_id(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['attestation-id']

    @classmethod
    def attestation_url(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['attestation-url']

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v3',
        subject_path: Ostrlike = None,
        subject_digest: Ostrlike = None,
        subject_checksums: Ostrlike = None,
        subject_name: Ostrlike = None,
        push_to_registry: Oboollike = None,
        create_storage_record: Oboollike = None,
        show_summary: Oboollike = None,
        github_token: Ostrlike = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> AttestBuildProvenance:
        if (
            sum(
                value is not None
                for value in (subject_path, subject_digest, subject_checksums)
            )
            != 1
        ):
            raise ValueError(
                'Exactly one of subject_path, subject_digest, or subject_checksums must be set'
            )

        options: dict[str, object] = {
            'subject-path': subject_path,
            'subject-digest': subject_digest,
            'subject-checksums': subject_checksums,
            'subject-name': subject_name,
            'push-to-registry': push_to_registry,
            'create-storage-record': create_storage_record,
            'show-summary': show_summary,
            'github-token': github_token,
        }

        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            name = 'Create Attestation'

        return super().__new__(
            cls,
            name,
            'actions/attest-build-provenance',
            ref=version,
            with_opts=options or None,
            args=args,
            entrypoint=entrypoint,
            condition=condition,
            id=id,
            env=env,
            continue_on_error=continue_on_error,
            timeout_minutes=timeout_minutes,
            skip_recommended_permissions=skip_recommended_permissions,
            recommended_permissions=cls.recommended_permissions,
        )
