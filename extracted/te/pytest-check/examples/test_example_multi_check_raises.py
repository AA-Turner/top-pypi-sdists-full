def test_multi_check_raises(check):
    # Intentionally type-invalid indexing to raise exceptions and exercise
    # multi-failure aggregation/traceback output behavior.
    lst_1 = []
    with check:
        assert lst_1["N/A"] == "Fail 1"
    with check:
        assert lst_1[-1] == "Fail 2"
    lst_2 = ["Success"]
    lst_3 = []
    with check:
        assert lst_2[-1] == "Success"
    with check:
        assert lst_3[-1] == "Success"
