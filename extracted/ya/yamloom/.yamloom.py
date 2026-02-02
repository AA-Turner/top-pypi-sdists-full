from yamloom.actions.toolchains.rust import SetupRust
from dataclasses import dataclass
from yamloom.actions.github.artifacts import DownloadArtifact, UploadArtifact
from yamloom.actions.github.release import ReleasePlease
from yamloom.actions.packaging.python import Maturin
from yamloom.actions.toolchains.python import SetupPython, SetupUV
from yamloom.actions.github.scm import Checkout
from yamloom.expressions import context
from yamloom import (
    Workflow,
    Events,
    PushEvent,
    PullRequestEvent,
    WorkflowDispatchEvent,
    Permissions,
    Job,
    Matrix,
    Strategy,
    script,
    Environment,
)


@dataclass
class Target:
    runner: str
    target: str
    skip_python_versions: list[str] | None = None


DEFAULT_PYTHON_VERSIONS = [
    '3.9',
    '3.10',
    '3.11',
    '3.12',
    '3.13',
    '3.13t',
    '3.14',
    '3.14t',
    'pypy3.11',
]


def resolve_python_versions(skip: list[str] | None) -> list[str]:
    if not skip:
        return DEFAULT_PYTHON_VERSIONS
    skipped = set(skip)
    return [version for version in DEFAULT_PYTHON_VERSIONS if version not in skipped]


def create_build_job(
    job_name: str, name: str, targets: list[Target], *, needs: list[str]
) -> Job:
    def platform_entry(target: Target) -> dict[str, object]:
        entry = {
            'runner': target.runner,
            'target': target.target,
            'python_versions': resolve_python_versions(target.skip_python_versions),
        }
        python_arch = (
            ('arm64' if target.target == 'aarch64' else target.target)
            if name == 'windows'
            else None
        )
        if python_arch is not None:
            entry['python_arch'] = python_arch
        return entry

    return Job(
        steps=[
            Checkout(),
            script(
                f'printf "%s\n" {context.matrix.platform.python_versions.as_array().join(" ")} >> version.txt',
            ),
            SetupPython(
                python_version_file='version.txt',
                architecture=context.matrix.platform.python_arch.as_str()
                if name == 'windows'
                else None,
            ),
            Maturin(
                name='Build wheels',
                target=context.matrix.platform.target.as_str(),
                args=f'--release --out dist --interpreter {context.matrix.platform.python_versions.as_array().join(" ")}',
                sccache=~context.github.ref.startswith('refs/tags/'),
                manylinux='musllinux_1_2'
                if name == 'musllinux'
                else ('auto' if name == 'linux' else None),
            ),
            UploadArtifact(
                path='dist',
                artifact_name=f'wheels-{name}-{context.matrix.platform.target}',
            ),
        ],
        runs_on=context.matrix.platform.runner.as_str(),
        strategy=Strategy(
            fast_fail=False,
            matrix=Matrix(
                platform=[platform_entry(target) for target in targets],
            ),
        ),
        needs=needs,
        condition=context.github.ref.startswith('refs/tags/')
        | (context.github.event_name == 'workflow_dispatch'),
    )


release_workflow = Workflow(
    name='Build and Release',
    on=Events(
        push=PushEvent(branches=['main'], tags=['*']),
        pull_request=PullRequestEvent(),
        workflow_dispatch=WorkflowDispatchEvent(),
    ),
    jobs={
        'build-test-check': Job(
            steps=[
                Checkout(),
                SetupRust(components=['clippy']),
                SetupUV(python_version='3.9'),
                script('cargo clippy'),
                script('cargo test'),
                script(
                    'uv venv',
                    '. .venv/bin/activate',
                    'echo PATH=$PATH >> $GITHUB_ENV',
                    'uvx maturin develop --uv',
                ),
                script('uv pip install pytest'),
                script('uvx ruff check'),
                script('uvx ty check'),
                script('uv run pytest'),
            ],
            runs_on='ubuntu-latest',
        ),
        'linux': create_build_job(
            'Build Linux Wheels',
            'linux',
            [
                Target(
                    'ubuntu-22.04',
                    target,
                )
                for target in [
                    'x86_64',
                    'x86',
                    'aarch64',
                    'armv7',
                    's390x',
                    'ppc64le',
                ]
            ],
            needs=['build-test-check'],
        ),
        'musllinux': create_build_job(
            'Build (musl) Linux Wheels',
            'musllinux',
            [
                Target(
                    'ubuntu-22.04',
                    target,
                )
                for target in [
                    'x86_64',
                    'x86',
                    'aarch64',
                    'armv7',
                ]
            ],
            needs=['build-test-check'],
        ),
        'windows': create_build_job(
            'Build Windows Wheels',
            'windows',
            [
                Target(
                    'windows-latest',
                    'x64',
                ),
                Target('windows-latest', 'x86', ['pypy3.11']),
                Target(
                    'windows-11-arm',
                    'aarch64',
                    ['3.9', '3.10', '3.11', '3.13t', '3.14t', 'pypy3.11'],
                ),
            ],
            needs=['build-test-check'],
        ),
        'macos': create_build_job(
            'Build macOS Wheels',
            'macos',
            [
                Target(
                    'macos-15-intel',
                    'x86_64',
                ),
                Target(
                    'macos-latest',
                    'aarch64',
                ),
            ],
            needs=['build-test-check'],
        ),
        'sdist': Job(
            steps=[
                Checkout(),
                Maturin(name='Build sdist', command='sdist', args='--out dist'),
                UploadArtifact(path='dist', artifact_name='wheels-sdist'),
            ],
            name='Build Source Distribution',
            runs_on='ubuntu-22.04',
            needs=['build-test-check'],
            condition=context.github.ref.startswith('refs/tags/')
            | (context.github.event_name == 'workflow_dispatch'),
        ),
        'release': Job(
            steps=[
                DownloadArtifact(),
                SetupUV(),
                script(
                    'uv publish --trusted-publishing always wheels-*/*',
                    permissions=Permissions(id_token='write', contents='write'),
                ),
            ],
            name='Release',
            runs_on='ubuntu-22.04',
            condition=context.github.ref.startswith('refs/tags/')
            | (context.github.event_name == 'workflow_dispatch'),
            needs=['linux', 'musllinux', 'windows', 'macos', 'sdist'],
            environment=Environment('pypi'),
        ),
    },
)

version_workflow = Workflow(
    name='Release Please',
    on=Events(
        push=PushEvent(
            branches=['main'],
        ),
    ),
    jobs={
        'release-please': Job(
            steps=[
                ReleasePlease(
                    token=context.secrets.RELEASE_PLEASE,
                    config_file='release-please-config.json',
                    manifest_file='.release-please-manifest.json',
                )
            ],
            runs_on='ubuntu-latest',
        )
    },
)


if __name__ == '__main__':
    release_workflow.dump('.github/workflows/release.yml')
    version_workflow.dump('.github/workflows/release-please.yml')
