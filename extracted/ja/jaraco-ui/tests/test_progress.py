import itertools

from jaraco.ui import progress


class TestSimpleProgress:
    def test_simple_progress_one(self, capsys):
        counter = itertools.count()
        bar = progress.SimpleProgressBar().iterate(counter)
        out, err = capsys.readouterr()
        # nothing is output until the iterable is entered
        assert out == ''
        next(bar)
        out, err = capsys.readouterr()
        # once the iterable is entered, it will output the 0th
        # item and then immediately the output for the first
        # item.
        expected = (
            '\r [                               |                               ] (0)'
            '\r [                               /                               ] (1)'
        )
        assert out == expected
