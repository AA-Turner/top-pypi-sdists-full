from chtoolset._query import replace_tables, \
    format, \
    tables, \
    table_if_is_simple_query, \
    query_get_type, \
    check_compatible_types, \
    check_valid_write_query, \
    get_left_table, \
    rewrite_aggregation_states, \
    parser_cache_info, \
    parser_cache_reset, \
    explain_ast, \
    create_row_binary_encoder, \
    apply_row_binary_encoder, \
    apply_row_binary_encoder_bytes, \
    delete_row_binary_encoder, \
    validate_row_binary_encoder_schema, \
    set_row_binary_encoder_buffer_config, \
    set_row_binary_encoder_thread_buffer_size


class RowBinaryEncoderError(Exception):
    """Custom exception for RowBinaryEncoder errors"""
    pass


class RowBinaryEncoder():
    def __init__(self, schema: str, legacy_conversion_mode: bool = True, max_json_row_size: int = 1000000, binary_json_as_string: bool = True):
        if not isinstance(schema, str):
            raise TypeError("Schema must be a string")

        try:
            self._encoder_ptr = create_row_binary_encoder(schema, legacy_conversion_mode, max_json_row_size, binary_json_as_string)
            if not self._encoder_ptr:
                raise RowBinaryEncoderError("Failed to create encoder")
        except Exception as e:
            raise RowBinaryEncoderError(f"Error initializing encoder: {str(e)}") from e

    def __enter__(self):
        if not self._encoder_ptr:
            raise RowBinaryEncoderError("Encoder was already closed")
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.close()

    def encode(self, block: str) -> bytes:
        if not isinstance(block, str):
            raise TypeError("Block must be a string")

        if not self._encoder_ptr:
            raise RowBinaryEncoderError("Encoder was already closed")

        try:
            result = apply_row_binary_encoder(self._encoder_ptr, block)
            return result
        except Exception as e:
            raise RowBinaryEncoderError(f"Error encoding block: {str(e)}") from e

    def encode_bytes(self, block: bytes) -> bytes:
        if not isinstance(block, bytes):
            raise TypeError("Block must be bytes")

        if not self._encoder_ptr:
            raise RowBinaryEncoderError("Encoder was already closed")

        try:
            result = apply_row_binary_encoder_bytes(self._encoder_ptr, block)
            return result
        except Exception as e:
            raise RowBinaryEncoderError(f"Error encoding block: {str(e)}") from e

    def close(self):
        if self._encoder_ptr:
            delete_row_binary_encoder(self._encoder_ptr)
            self._encoder_ptr = None
