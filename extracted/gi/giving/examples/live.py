import time

from rich.live import Live
from rich.pretty import Pretty
from rich.table import Table

from giving import give, given

# progress = Progress()
# task = progress.add_task("Progress", total=1000)


def dict_to_table(d):
    table = Table.grid(padding=(0, 3, 0, 0))
    table.add_column("key", style="bold green")
    # table.add_row("progress", progress)
    for k, v in d.items():
        table.add_row(k, Pretty(v))
    # return Group(table, progress)
    return table


def bisect(arr, key):
    lo = -1
    hi = len(arr)
    give(lo, hi)  # push {"lo": lo, "hi": hi}
    while lo < hi - 1:
        mid = lo + (hi - lo) // 2
        give(mid)  # push {"mid": mid}
        if arr[mid] > key:
            hi = mid
            give()  # push {"hi": hi}
        else:
            lo = mid
            give()  # push {"lo": lo}
    return lo + 1


def main():
    bisect(list(range(1000)), 742)
    # for i in range(100):
    #     time.sleep(0.1)
    #     give(i=i)
    #     give(ii=i * i)


# if __name__ == "__main__":
#     with given() as gv:
#         live = Live(refresh_per_second=4)
#         gv.wrap("main", live)

#         @gv.where("mid").ksubscribe
#         def _(mid):
#             time.sleep(1)
#             progress.update(task, completed=mid)

#         @gv.kscan().subscribe
#         def _(data):
#             live.update(dict_to_table(data))

#         with give.wrap("main"):
#             main()


if __name__ == "__main__":
    with given() as gv:
        live = Live(refresh_per_second=4)
        gv.wrap("main", live)

        @gv.kscan().subscribe
        def _(data):
            time.sleep(1)  # So that we can see the values change
            live.update(dict_to_table(data))

        with give.wrap("main"):
            main()


# import time

# from rich.live import Live
# from rich.progress import Progress
# from rich.table import Table
# from rich.pretty import Pretty

# progress = Progress()
# task = progress.add_task("", total=100)

# def dict_to_table(d):
#     table = Table.grid(padding=(0, 3, 0, 0))
#     table.add_column("key", style="bold green")
#     table.add_row("progress", progress)
#     for k, v in d.items():
#         table.add_row(k, Pretty(v))
#     return table

# def main():
#     with Live(refresh_per_second=4) as live:
#         for i in range(100):
#             time.sleep(0.1)
#             progress.advance(task, 1)
#             live.update(dict_to_table({"i": i, "ii": i * i}))

# if __name__ == "__main__":
#     main()
