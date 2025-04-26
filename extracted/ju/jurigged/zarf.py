import re
from collections import deque

ANSI_ESCAPE = re.compile(r"(\x1b\[[;\d]*[A-Za-z])")


lines = ["hello" * 100, "wowie"]


# def breakline(line, limit=10):
#     parts = re.split(pattern=ANSI_ESCAPE, string=line)
#     lines = [["", 0]]
#     avail = limit
#     for i, part in enumerate(parts):
#         if i % 2:
#             lines[-1][0] += part
#         else:
#             if not avail:
#                 ok, extra = "", part
#             else:
#                 ok, extra = part[:avail], part[avail:]
#             avail -= len(ok)
#             lines[-1][0] += ok
#             lines[-1][1] = limit - avail
#             if extra:
#                 lines.append([extra, len(extra)])
#                 avail = limit

#     print(lines)


# def breakline(line, limit=10):
#     parts = [
#         (x, i % 2 == 1)
#         for i, x in enumerate(re.split(pattern=ANSI_ESCAPE, string=line))
#     ]
#     lines = [["", 0]]
#     avail = limit
#     work = deque(parts)
#     while work:
#         part, escape = work.popleft()
#         if escape:
#             lines[-1][0] += part
#         else:
#             if not avail:
#                 ok, extra = "", part
#             else:
#                 ok, extra = part[:avail], part[avail:]
#             avail -= len(ok)
#             lines[-1][0] += ok
#             lines[-1][1] = limit - avail
#             if extra:
#                 work.appendleft((extra, False))
#                 lines.append(["", 0])
#                 avail = limit
#     for l in lines:
#         print(l[0])


def breakline(line, limit=10):
    parts = [
        (x, i % 2 == 1)
        for i, x in enumerate(re.split(pattern=ANSI_ESCAPE, string=line))
    ]
    current_line = ""
    avail = limit
    work = deque(parts)
    while work:
        part, escape = work.popleft()
        if escape:
            current_line += part
        else:
            if not avail:
                ok, extra = "", part
            else:
                ok, extra = part[:avail], part[avail:]
            avail -= len(ok)
            current_line += ok
            if extra:
                work.appendleft((extra, False))
                yield current_line, limit - avail
                current_line = ""
                avail = limit
    if current_line:
        yield current_line, limit - avail


def main():
    # s = "\x1b[31mhey\x1b[0mbob\x1b[33mwhat up to all my good friends here that slap it"
    # for a, b in breakline(s):
    #     print(a, b)
    print("hello" * 100)
    print("hi there " * 100)
    print(list(range(1000)))


if __name__ == "__main__":
    main()
