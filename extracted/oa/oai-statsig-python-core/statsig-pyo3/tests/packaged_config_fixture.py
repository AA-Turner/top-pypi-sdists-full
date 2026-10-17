"""Lightweight importable config packages matching the writer's resource layout."""

import importlib
import json
import sys


def packaged_config(
    tmp_path,
    monkeypatch,
    document,
    *,
    name="test_config_package",
    generated=False,
):
    content = document if isinstance(document, str) else json.dumps(document)
    source = tmp_path
    package = source / name
    package.mkdir(parents=True)
    if generated:
        from google.protobuf.descriptor_pb2 import FileDescriptorProto

        # Match the writer's protobuf namespace and Config re-export. The builder
        # calls below are the same ones emitted in generated *_pb2.py modules.
        proto_package = f"oaiproto.statsig_configs.{name}"
        descriptor = FileDescriptorProto(
            name=f"oaiproto/statsig_configs/{name}/config.proto",
            package=proto_package,
            syntax="proto3",
        )
        message = descriptor.message_type.add(name="Config")
        message.field.add(name="number", number=1, type=5, label=1)
        proto_dir = source / "oaiproto" / "statsig_configs" / name
        proto_dir.mkdir(parents=True)
        (proto_dir / "config_pb2.py").write_text(
            "from google.protobuf import descriptor_pool\n"
            "from google.protobuf.internal import builder\n"
            f"DESCRIPTOR = descriptor_pool.Default().AddSerializedFile({descriptor.SerializeToString()!r})\n"
            "builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())\n"
            "builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, __name__, globals())\n"
        )
        (package / "__init__.py").write_text(
            f"from {proto_package}.config_pb2 import Config as Config\n"
        )
        monkeypatch.delitem(sys.modules, proto_package, raising=False)
        monkeypatch.delitem(sys.modules, f"{proto_package}.config_pb2", raising=False)
    else:
        (package / "__init__.py").write_text(
            "from google.protobuf.struct_pb2 import Struct as Config\n"
        )
    (package / "fallback.json").write_text(content)
    monkeypatch.syspath_prepend(str(source))
    monkeypatch.delitem(sys.modules, name, raising=False)
    return importlib.import_module(name)
