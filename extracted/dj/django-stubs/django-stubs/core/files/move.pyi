def file_move_safe(
    old_file_name: str, new_file_name: str, chunk_size: int = 65536, allow_overwrite: bool = False
) -> None: ...

__all__ = ["file_move_safe"]
