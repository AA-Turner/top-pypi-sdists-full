from rook.protobuf import protoc

if protoc == "protoc311":
    from rook.protobuf.protoc311.envelope_pb2 import *
elif protoc == "protoc319":
    from rook.protobuf.protoc319.envelope_pb2 import *
