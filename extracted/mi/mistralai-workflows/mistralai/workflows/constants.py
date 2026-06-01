# Temporal has a 2MB payload limit. We use 1.9MB to leave headroom for metadata and headers.
MAX_INPUT_SIZE_BYTES = int(1.9 * 1024 * 1024)

INTERNAL_METADATA_PREFIX = "__internal_"
