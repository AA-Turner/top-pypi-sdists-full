import yaml
from semver4 import Version4, SemVersion


def get_representer(dumper: yaml.SafeDumper, version: Version4|SemVersion) -> yaml.ScalarNode:
    return dumper.represent_str(str(version))


def get_version4_dumper() -> yaml.SafeDumper:
    safe_dumper = yaml.SafeDumper
    safe_dumper.add_representer(Version4, get_representer)
    return safe_dumper


def get_semversion_dumper() -> yaml.SafeDumper:
    safedumper = yaml.SafeDumper
    safedumper.add_representer(SemVersion, get_representer)
    return safedumper


def get_version4_loader() -> yaml.SafeLoader:
    def constructor(loader: yaml.SafeLoader, node: yaml.nodes.ScalarNode) -> str:
        if Version4.validate(node.value):
            return Version4(node.value)
        return loader.construct_yaml_str(node)

    safeloader = yaml.SafeLoader
    safeloader.add_constructor('tag:yaml.org,2002:str', constructor)
    return safeloader


def get_semversion_loader() -> yaml.SafeLoader:
    def constructor(loader: yaml.SafeLoader, node: yaml.nodes.ScalarNode) -> str:
        if SemVersion.validate(node.value):
            return SemVersion(node.value)
        return loader.construct_yaml_str(node)

    safeloader = yaml.SafeLoader
    safeloader.add_constructor('tag:yaml.org,2002:str', constructor)
    return safeloader
