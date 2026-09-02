from rook.protobuf import protoc

if protoc == "protoc311":
    from rook.protobuf.protoc311.variant_pb2 import *
elif protoc == "protoc319":
    from rook.protobuf.protoc319.variant_pb2 import *
