import pytest

from yamloom import Job, Permissions, WorkflowInput, action, script
from yamloom.expressions import context


def test_job_requires_runs_on_or_uses() -> None:
    with pytest.raises(Exception):
        Job(steps=[script('echo hi')])


def test_job_rejects_runs_on_and_uses() -> None:
    with pytest.raises(Exception):
        Job(
            steps=[script('echo hi')],
            runs_on='ubuntu-latest',
            uses='org/repo/.github/workflows/reuse.yml@v1',
        )


def test_job_rejects_uses_with_steps() -> None:
    with pytest.raises(Exception):
        Job(
            steps=[script('echo hi')],
            uses='org/repo/.github/workflows/reuse.yml@v1',
        )


def test_job_rejects_runs_on_without_steps() -> None:
    with pytest.raises(Exception):
        Job(runs_on='ubuntu-latest')


def test_job_rejects_runs_on_with_empty_steps() -> None:
    with pytest.raises(Exception):
        Job(steps=[], runs_on='ubuntu-latest')


def test_job_rejects_runs_on_with_secrets_context() -> None:
    with pytest.raises(Exception):
        Job(steps=[script('echo hi')], runs_on=context.secrets.github_token)


def test_workflow_call_input_default_rejects_secrets() -> None:
    with pytest.raises(Exception):
        WorkflowInput.string(default=context.secrets.github_token)


def test_workflow_call_input_default_allows_github() -> None:
    WorkflowInput.string(default=context.github.actor)


def test_job_merges_recommended_permissions_when_not_skipped() -> None:
    job = Job(
        steps=[
            action(
                'checkout',
                'actions/checkout',
                recommended_permissions=Permissions(contents='read'),
            )
        ],
        runs_on='ubuntu-latest',
    )
    assert '\npermissions:\n  contents: read\n' in str(job)


def test_job_skips_recommended_permissions_when_opted_out() -> None:
    job = Job(
        steps=[
            action(
                'checkout',
                'actions/checkout',
                skip_recommended_permissions=True,
                recommended_permissions=Permissions(contents='read'),
            )
        ],
        runs_on='ubuntu-latest',
    )
    assert '\npermissions:\n' not in str(job)


def test_job_merges_user_and_recommended_permissions() -> None:
    job = Job(
        steps=[
            action(
                'oidc',
                'actions/checkout',
                recommended_permissions=Permissions(id_token='write'),
            )
        ],
        permissions=Permissions(contents='read'),
        runs_on='ubuntu-latest',
    )
    job_yaml = str(job)
    assert '\npermissions:\n' in job_yaml
    assert 'contents: read' in job_yaml
    assert 'id-token: write' in job_yaml


def test_script_permissions_merge_like_recommended_permissions() -> None:
    job = Job(
        steps=[script('echo hi', permissions=Permissions(contents='read'))],
        runs_on='ubuntu-latest',
    )
    assert '\npermissions:\n  contents: read\n' in str(job)
