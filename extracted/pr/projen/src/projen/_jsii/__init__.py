from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from jsii._type_checking import cached_type_hints, check_type


import constructs._jsii

_SUBMODULE_FQN_MAP = {
    "projen.awscdk": "projen.awscdk",
    "projen.build": "projen.build",
    "projen.cdk": "projen.cdk",
    "projen.cdk8s": "projen.cdk8s",
    "projen.cdktf": "projen.cdktf",
    "projen.cdktn": "projen.cdktn",
    "projen.circleci": "projen.circleci",
    "projen.github": "projen.github",
    "projen.github.workflows": "projen.github.workflows",
    "projen.gitlab": "projen.gitlab",
    "projen.java": "projen.java",
    "projen.javascript": "projen.javascript",
    "projen.javascript.biome_config": "projen.javascript.biome_config",
    "projen.polaris": "projen.polaris",
    "projen.python": "projen.python",
    "projen.python.uvConfig": "projen.python.uv_config",
    "projen.release": "projen.release",
    "projen.sonarqube": "projen.sonarqube",
    "projen.typescript": "projen.typescript",
    "projen.vscode": "projen.vscode",
    "projen.web": "projen.web",
}

__jsii_assembly__ = jsii.JSIIAssembly.load(
    "projen", "0.103.18", __name__[0:-6], "projen@0.103.18.jsii.tgz"
)

__all__ = [
    "__jsii_assembly__",
]

publication.publish()
