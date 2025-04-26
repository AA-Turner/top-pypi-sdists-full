from google.protobuf import __version__ as protobuf_version

if protobuf_version < "4":
    protoc = "protoc311"
else:
    protoc = "protoc319"
