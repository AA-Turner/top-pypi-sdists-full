# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import pathlib
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from argparse import ArgumentParser


@dataclass
class Frame:
    index: int
    function: str
    directory: str
    filename: str
    line_no: int
    ip: str
    object: str

    @classmethod
    def from_element(cls, index, frame: ET.Element):
        return cls(
            index=index,
            function=get_element_text(frame, "fn"),
            directory=get_element_text(frame, "dir"),
            filename=get_element_text(frame, "file"),
            line_no=int(get_element_text(frame, "line", "0")),
            ip=get_element_text(frame, "ip"),
            object=get_element_text(frame, "obj", "???"),
        )

    def __str__(self):
        prefix = "at" if self.index == 0 else "by"
        function = short_function(self.function)
        object = short_path(self.object)
        source = f"{short_path(self.directory, self.filename)}:{self.line_no}"
        if function:
            return f"{prefix} {self.ip:>10}: {function} ({source} in {object})"
        else:
            return f"{prefix} {self.ip:>10}: ???"


def short_function(function):
    if len(function) > 100:
        function = f"{function[:40]}...{function[-40:]}"
    return function


def short_path(*paths):
    path = pathlib.Path(*paths)
    interesting_parts = path.parts[-4:]
    return pathlib.Path("...").joinpath(*interesting_parts)


@dataclass
class Stack:
    frames: list[Frame]

    @classmethod
    def from_element(cls, stack: ET.Element):
        frames = []
        for index, frame in enumerate(stack.findall("frame")):
            frame_data = Frame.from_element(index, frame)
            frames.append(frame_data)
        return cls(frames)


@dataclass
class XWhat:
    text: str
    leaked_bytes: int
    leaked_blocks: int

    @classmethod
    def from_element(cls, xwhat: ET.Element):
        return cls(
            text=get_element_text(xwhat, "text"),
            leaked_bytes=int(get_element_text(xwhat, "leakedbytes", "0")),
            leaked_blocks=int(get_element_text(xwhat, "leakedblocks", "0")),
        )


@dataclass
class LeakError:
    kind: str
    stack: Stack
    xwhat: XWhat

    @classmethod
    def from_element(cls, error: ET.Element):
        kind = error.find("kind")
        return cls(
            kind=kind.text,
            stack=Stack.from_element(error.find("stack")),
            xwhat=XWhat.from_element(error.find("xwhat")),
        )

    def __lt__(self, other):
        if not isinstance(other, LeakError):
            return NotImplemented
        return self.xwhat.leaked_bytes < other.xwhat.leaked_bytes


def get_element_text(parent: ET.Element, name: str, default: str = "") -> str:
    if parent is None:
        return default

    element = parent.find(name)
    if element is not None:
        return element.text
    else:
        return default


def get_leaks(root: ET.Element, kind: str) -> list[LeakError]:
    leaks = []
    for error_element in root.findall("error"):
        kind_element = error_element.find("kind")
        if kind_element is not None and kind_element.text == kind:
            leak = LeakError.from_element(error_element)
            leaks.append(leak)
    return leaks


def get_pytango_leaks(leaks: list[LeakError], max_blocks: int) -> list[LeakError]:
    pytango_leaks = []
    for leak in leaks:
        if leak.xwhat.leaked_blocks > max_blocks:
            if is_pytango_in_stack(leak):
                pytango_leaks.append(leak)
    return pytango_leaks


def is_pytango_in_stack(leak) -> bool:
    for frame in leak.stack.frames:
        filename = pathlib.Path(frame.object).name
        if filename.startswith("_tango") and filename.endswith(".so"):
            return True
    return False


def parse_input_file(filename: str) -> tuple[str, list[LeakError], list[LeakError]]:
    root = ET.parse(filename).getroot()
    header = get_header(root)
    definite_leaks = get_leaks(root, "Leak_DefinitelyLost")
    possible_leaks = get_leaks(root, "Leak_PossiblyLost")
    return header, definite_leaks, possible_leaks


def get_header(root: ET.Element) -> str:
    pid = root.find("pid")
    if pid is None:
        return ""
    ppid = root.find("ppid")
    if ppid is None:
        return ""
    args = root.find("args")
    if args is not None:
        argv = args.find("argv")
        if argv is not None:
            exe = argv.find("exe")
            if exe is None:
                return ""
            arg_list = []
            for arg in argv.findall("arg"):
                arg_list.append(arg.text)

    return f"ppid {ppid.text} -> pid {pid.text}: {exe.text} {' '.join(arg_list)}"


def report_pytango_leaks(label, leaks, max_blocks):
    pytango_leaks = get_pytango_leaks(leaks, max_blocks)
    print(
        f"PyTango {label} leaks larger than {max_blocks} block(s): {len(pytango_leaks)}"
    )
    print_leaks(pytango_leaks)
    return len(pytango_leaks)


def print_leaks(leaks: list[LeakError]):
    for count, leak in enumerate(sorted(leaks, reverse=True)):
        print(f"\n  Leak {count+1}:  {leak.xwhat.text}")
        for frame in leak.stack.frames:
            print(f"    {frame}")


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("file", help="Valgrind XML file to parse")
    parser.add_argument(
        "--max-blocks",
        help="Report leaks larger than this many blocks",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--no-error", action="store_true", help="Exit code 0, even if leaks found"
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    header, definite_leaks, possible_leaks = parse_input_file(args.file)
    print(
        f"Valgrind {header}:\n"
        f"\tfound {len(possible_leaks)} possible leaks, "
        f"and {len(definite_leaks)} definite leaks.\n"
    )

    max_blocks = args.max_blocks
    report_pytango_leaks("possible", possible_leaks, max_blocks)
    n_definite = report_pytango_leaks("definite", definite_leaks, max_blocks)

    # only definite leaks can cause an error on exit
    if n_definite > 0 and not args.no_error:
        print(f"\nError: definite leaks found in {args.file}!")
        sys.exit(1)
    else:
        print("\nDone")


if __name__ == "__main__":
    main()
