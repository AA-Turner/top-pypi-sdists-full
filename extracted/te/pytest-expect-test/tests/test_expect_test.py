def cumulative_sum(nums):
    cum_sum = 0
    result = []
    for num in nums:
        result.append(num+cum_sum)
        cum_sum += num
    return result


def test_simple(expect):
    print(cumulative_sum([2, 3, 5]))
    expect("""\
[2, 5, 10]
""")
    print(cumulative_sum([1, 5, 9]))
    expect("""\
[1, 6, 15]
""")
