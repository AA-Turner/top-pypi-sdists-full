from giving import give, given

# 1. Use give() in the main code


def binary_search(arr, key):
    give(arr, key)  # <== emit {"arr": arr, "key": key}

    lo = -1
    hi = len(arr)

    while lo < hi - 1:
        mid = lo + (hi - lo) // 2
        give(mid)  # <== emit {"mid": mid}

        if give(arr[mid]) > key:
            hi = mid
            give()  # <== emit {"hi": hi}

        else:
            lo = mid
            give()  # <== emit {"lo": lo}

    return lo + 1


# 2. Use given() to compute and do things

with given() as gv:
    # Print all the raw data
    gv.display()

    # Get the minimum and maximum of some data
    gv["?mid"].min().print("min(mid): {}")
    gv["?mid"].max().print("max(mid): {}")

    # Accumulate into a list for later processing
    trajectory = gv["?mid"].accum()

    # Merge successive entries with kscan and do more complex things
    gv.kscan().print("{lo} <= {mid} <= {hi}", skip_missing=True)

    # You can assert conditions
    gv.kscan().where("lo", "hi").kfilter(lambda lo, hi: lo > hi).fail()

    # Call the function after setting up the pipeline
    print("result:", binary_search(list(range(100)), 30))

print(f"{trajectory=}")


# from giving import give, given

# def bisect(arr, key):
#     lo = -1
#     hi = len(arr)
#     while lo < hi - 1:
#         mid = lo + (hi - lo) // 2
#         give(mid)                # push {"mid": mid}
#         if arr[mid] > key:
#             hi = mid
#             give()               # push {"hi": hi}
#         else:
#             lo = mid
#             give()               # push {"lo": lo}
#     return lo + 1


# with given() as gv:
#     # gv.print()
#     gv["?mid"].min().print("min(mid): {}")
#     # gv["?mid"].max().print("max(mid): {}")
#     # (gv["?mid"].min().as_("min") | gv["?mid"].max().as_("max")).kmerge().print()
#     gv.kmerge(scan=True).print("{lo} <= {mid} <= {hi}", skip_missing=True)
#     gv.kmerge(scan=True).where("lo", "hi").kfilter(lambda lo, hi: lo > hi).breakpoint()

#     # Put the values in an array
#     mids = gv["?mid"].accum()

#     bisect(list(range(10)), 3)

# print(mids)
