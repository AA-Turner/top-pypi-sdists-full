import logging
import os
from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")


logger = logging.getLogger(__name__)


class FileUtil:
    """File operation utilities"""

    @staticmethod
    async def get_line_count(file_path: str) -> int:
        """Get the number of lines in a file"""
        with open(file_path, encoding="utf-8") as f:
            return sum(1 for _ in f)

    @staticmethod
    async def split_file(file_path: str, dest_file_num: int, dest_dir: str):
        """Split a file into multiple parts

        Args:
            file_path: Path to the source file
            dest_file_num: Number of destination files
            dest_dir: Directory to store split files
        """
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        line_count = await FileUtil.get_line_count(file_path)
        line_per_file, remain_line = divmod(line_count, dest_file_num)
        logger.info(f"line_count: {line_count}, line_per_file: {line_per_file}, remain_line {remain_line}")

        with open(file_path, encoding="utf-8") as f:
            for i in range(dest_file_num):
                dest_file_name = os.path.join(dest_dir, f"{i}.jsonl")
                with open(dest_file_name, "w", encoding="utf-8") as f_out:
                    dest_file_line_count = line_per_file + 1 if i < remain_line else line_per_file
                    logger.info(f"file {dest_file_name}, lines: {dest_file_line_count}")
                    for _ in range(dest_file_line_count):
                        f_out.write(f.readline())


class ListUtil:
    """List operation utilities"""

    @classmethod
    async def get_unique_list(cls, input_list: list[str]) -> list[str]:
        """Remove duplicates from a list while preserving order"""
        return list(dict.fromkeys(input_list))
