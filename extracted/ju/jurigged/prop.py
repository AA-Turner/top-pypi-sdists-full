import sys

# from jurigged.dev import loop, loop_on_error
from rich.panel import Panel


def fact(n):
    if n == 1:
        return 1 / 0
    else:
        return n * fact(n - 1)


class Bob:
    # @__.xloop
    def foo(self, q):
        # give(xoxo=xoxo)
        # print(random.random())

        # for i in range(3):
        #     print(i)
        #     # give(i)
        #     # time.sleep(0.5)

        print("wow")
        # q = 1

        return 12345 / (q - 3)


# def main(vax):
#     b = Bob()
#     for i in range(10):
#         print(b.foo(i))
#     # b = Bob()
#     # while True:
#     #     time.sleep(0.1)
#     #     print(b.foo)
#     return "WORLD"

import re

import colorama
from rich.cells import cell_len
from rich.console import Console
from rich.panel import Panel
from rich.segment import Segment

F = colorama.Fore

ANSI_ESCAPE = re.compile(r"\x1b\[[;\d]*[A-Za-z]")


class RawSegment(Segment):
    @property
    def cell_length(self) -> int:
        """Get cell length of segment."""
        assert not self.control
        return cell_len(re.sub(ANSI_ESCAPE, "", self.text))


class TerminalLine:
    def __init__(self, text):
        self.text = text

    def __rich_console__(self, console, options):
        yield RawSegment(self.text)


from executing import Source


def zazz(xxx):
    return Source.executing(sys._getframe(1))


@__.loop(interface="rich")
def main(x):
    for i in range(100):
        print(i)
    print("the ende")
    return x * x


def foo(vax):
    # dest = io.StringIO()
    # con = Console(width=20, no_color=False, color_system="standard")
    # lines = [
    #     f"this is {F.CYAN}cool{F.RESET}{F.RED}ish{F.RESET} to the max",
    #     "this is [cyan]cool[/cyan][red]ish[/red] to the max",
    #     "this is coolish to the max",
    # ]
    # with con.capture() as cpt:
    #     for line in lines:
    #         con.print(line)
    #     con.print(Pretty({"a": 1}))
    #     # con.print(Panel("wow", title="cool", border_style="blue"))

    # # con.print(Pretty({"a": 1}))
    # print(cpt.get())
    # # print(repr(cpt.get()))

    con = Console(color_system="standard")
    con.print(
        Panel(
            TerminalLine(
                F.RED + "some red text" + F.BLUE + " and blue" + F.RESET
            ),
            width=50,
        )
    )

    # print(list(range(100)))

    # print("UH OH", file=sys.stderr)
    # print("GRR", file=sys.stderr)
    # print("oh I see", file=sys.stderr)
    # print("fuck", file=sys.stderr)

    node = zazz("www.cool.com")
    print(node)
    for k, v in vars(node).items():
        print(k, v)

    if node.node:
        print("====")
        for k, v in vars(node.node).items():
            print(k, v)
        print(vars(node.node.args[0]))

    # oof = 34
    # give()
    # wow = list(range(30))
    # give()
    # give(nixon=21, yourmom=33)

    for i in range(10):
        print(i)
        # give(i)
        # time.sleep(0.02)

    # try:
    #     1/0
    # except:
    #     raise Exception("no")

    # return fact(vax)
    return 9999


# def main(_):
#     console = Console()
#     zorg = colorama.Fore.RED + 'some red text' + colorama.Fore.RESET
#     console.print(Panel(zorg))

print(main(13))
