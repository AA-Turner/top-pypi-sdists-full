from giving import give, given

with given() as gv:
    # gv.throttle(5).subscribe(lambda _: print("slept", time.sleep(1)))

    @gv.group_wrap("what").subscribe
    def _(obs):
        obs["?i"].sum().print()

    for j in range(3):
        with give.wrap("what"):
            for i in range(10):
                give(i)


# def hyena(x):
#     # y = give.line.time(x * x)
#     y = give(x * x)
#     return y

# def fox(n):
#     with give.wrap(wow=12):
#         for i in range(n):
#             j = hyena(i)
#             # zazz = give.line.time(i)
#             with give.wrap(wow=37):
#                 zazz = give(i)
#                 1 + 1

# def wolf(n):
#     for i in range(n):
#         give(i)

# with given() as gv:
#     # gvt = gv.tag()
#     gvt = gv["i"].average(scan=2)
#     gvt.display()
#     gvt.display()

#     wolf(10)

# # with given() as gv0:
# #     # gv.tag(group="wow").display(breakword=True)
# #     # # gv.subscribe(print)
# #     # tagged = gv.tag(group="wow")
# #     # tagged.display()
# #     # tagged.breakword()
# #     # # gv["?zazz"].filter(lambda x: x == 2).breakpoint()

# #     gv = gv0["?zazz"].average(scan=8)
# #     gv.as_("a").display()
# #     gv.as_("z").display()

# #     @gv0.where(wow=12).wrap
# #     def f(wow):
# #         print("ENTER", wow)
# #         yield
# #         print("EXIT", wow)

# #     fox(10)
