COW = r"""
\
 \
   ^__^
   (oo)\_______
   (__)\       )\/\
       ||----w |
       ||     ||
"""

MAX_WIDTH = 40


def say(text: str) -> str:
    text = text or "Moo"
    lines_raw = [line.strip() for line in text.split("\n")]
    lines = [
        line_part
        for line in lines_raw
        for line_part in [
            line[i : i + MAX_WIDTH] for i in range(0, len(line), MAX_WIDTH)
        ]
        if line
    ]
    width = max([len(line) for line in lines])
    bubble = (
          ["┌─" + "─" * width + "┐"]
        + ["│" + line + " " * (width - len(line)) + " │" for line in lines]
        + ["└─" + "─" * width + "┘"]
    )
    cow_lines = [line for line in COW.split("\n") if len(line) != 0]
    cow = [" " * width + line for line in cow_lines]
    return "\n".join(bubble + cow)
