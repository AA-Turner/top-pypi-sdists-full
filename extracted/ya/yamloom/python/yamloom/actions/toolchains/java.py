from __future__ import annotations
from yamloom import Permissions
from yamloom.actions.utils import validate_choice

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

__all__ = ['SetupJava']


class SetupJava(ActionStep):
    """Set up a specific version of the Java JDK and add tools to PATH.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    java_version
        The Java version to set up. Takes a whole or semver Java version.
    java_version_file
        Path to the ``.java-version`` file.
    distribution
        Java distribution (required).
    java_package
        The package type (``jdk``, ``jre``, ``jdk+fx``, ``jre+fx``).
    architecture
        The architecture of the package.
    jdk_file
        Path to where the compressed JDK is located.
    check_latest
        Check for the latest available version that satisfies the version spec.
    server_id
        ID of the distributionManagement repository in the pom.xml file.
    server_username
        Environment variable name for the username for authentication to the
        Apache Maven repository.
    server_password
        Environment variable name for password or token for authentication to
        the Apache Maven repository.
    settings_path
        Path to where the settings.xml file will be written.
    overwrite_settings
        Overwrite the settings.xml file if it exists.
    gpg_private_key
        GPG private key to import.
    gpg_passphrase
        Environment variable name for the GPG private key passphrase.
    cache
        Name of the build platform to cache dependencies (``maven``, ``gradle``,
        ``sbt``).
    cache_dependency_path
        Path to a dependency file such as pom.xml, build.gradle, build.sbt, etc.
        Supports wildcards or a list of file names for caching multiple
        dependencies.
    mvn_toolchain_id
        Name of Maven Toolchain ID if the default name is not wanted.
    mvn_toolchain_vendor
        Name of Maven Toolchain Vendor if the default name is not wanted.
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
        The generated setup-java step.

    See Also
    --------
    GitHub repository: https://github.com/actions/setup-java
    """

    recommended_permissions = Permissions(contents='read')

    @classmethod
    def distribution(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.distribution

    @classmethod
    def java_version(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['java-version']

    @classmethod
    def java_home(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['java-home']

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v5',
        distribution: Ostrlike = None,
        java_version_file: Ostrlike = None,
        java_version: Ostrlike = None,
        java_package: Ostrlike = None,
        check_latest: Oboollike = None,
        architecture: Ostrlike = None,
        jdk_file: Ostrlike = None,
        cache: Ostrlike = None,
        cache_dependency_path: Ostrlike = None,
        overwrite_settings: Oboollike = None,
        server_id: Ostrlike = None,
        server_username: Ostrlike = None,
        server_password: Ostrlike = None,
        settings_path: Ostrlike = None,
        gpg_private_key: Ostrlike = None,
        gpg_passphrase: Ostrlike = None,
        mvn_toolchain_id: Ostrlike = None,
        mvn_toolchain_vendor: Ostrlike = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> SetupJava:
        options: dict[str, object] = {
            'java-version': java_version,
            'java-version-file': java_version_file,
            'distribution': distribution,
            'java-package': validate_choice(
                'java_package', java_package, ['jdk', 'jre', 'jdk+fx', 'jre+fx']
            ),
            'check-latest': check_latest,
            'architecture': validate_choice(
                'architecture',
                architecture,
                ['x86', 'x64', 'armv7', 'aarch64', 'ppc64le'],
            ),
            'jdkFile': jdk_file,
            'cache': validate_choice('cache', cache, ['maven', 'gradle', 'sbt']),
            'cache-dependency-path': cache_dependency_path,
            'overwrite-settings': overwrite_settings,
            'server-id': server_id,
            'server-username': server_username,
            'server-password': server_password,
            'settings-path': settings_path,
            'gpg-private-key': gpg_private_key,
            'gpg-passphrase': gpg_passphrase,
            'mvn-toolchain-id': mvn_toolchain_id,
            'mvn-toolchain-vendor': mvn_toolchain_vendor,
        }
        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            name = 'Setup Java'

        return super().__new__(
            cls,
            name,
            'actions/setup-java',
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
