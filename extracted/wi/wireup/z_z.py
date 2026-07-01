# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

# free-prompt
# 1) What standard tool(s) might you use to accomplish the logical task this question asks about?
# rsync is a typical tool for this case.
# 2) What alternative algorithms might you use to determine whether a file should be synced and their pros/cons?
# <answer here>
from dataclasses import dataclass
from typing import Self


@dataclass
class File:
    permissions: str
    username: str
    size: int
    mod_time: str
    filename: str

    def __post_init__(self):
        self.is_readable = self.permissions[0] == "r"
        self.is_writeable = self.permissions[1] == "w"

    @classmethod
    def from_string(cls, contents: str) -> Self:
        # "rwx alex 2673422 05:04:03 somefilename.txt"
        parts = contents.split(" ", 4)

        return cls(permissions=parts[0], username=parts[1], size=int(parts[2]), mod_time=parts[3], filename=parts[4])


def file_needs_sync(src: File, dst: File) -> bool:
    return src.is_readable and dst.is_writeable and src != dst


def get_files_to_sync(src: list[File], dst: list[File]) -> list[File]:
    # naive approach. iterate src files, check against dst files -> return if needs sync
    # implement __hash__ on file class (done via dataclasses in this case) to determine if two files are equal.
    # needs sync = filename does not exist in dst. or metadata differs
    # considering this data struct
    # map<filename, File>
    # for dst.
    # then for each source file, we can quickly check existence in dst files.
    # then take into account the rules such as is readable in src and writeable in dst.
    dst_map = {f.filename: f for f in dst}
    res = []

    for src_file in src:
        missing_in_remote = src_file.filename not in dst_map

        if missing_in_remote or file_needs_sync(src_file, dst_map[src_file.filename]):
            res.append(src_file)

    return res


def solution(source_files, destination_files):
    src_files = [File.from_string(f) for f in source_files]
    dst_files = [File.from_string(f) for f in destination_files]

    return [f.filename for f in get_files_to_sync(src_files, dst_files)]


print(
    solution(
        ["rwx alex 2673422 05:04:03 somefilename.txt", "rwx alex 2673422 05:04:03 foobar.txt"],
        ["rwx alex 2673422 05:04:06 somefilename.txt"],
    )
)
