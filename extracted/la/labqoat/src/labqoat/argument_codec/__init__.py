"""Function-compatible typed workflow codec entrypoints."""

from labqoat.argument_codec.argument_codec import ArgumentCodec

decode_arguments = ArgumentCodec.decode_arguments
decode_result = ArgumentCodec.decode_result
encode_result = ArgumentCodec.encode_result

__all__ = ["ArgumentCodec", "decode_arguments", "decode_result", "encode_result"]
