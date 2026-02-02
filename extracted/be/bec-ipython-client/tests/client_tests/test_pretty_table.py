from bec_ipython_client.prettytable import PrettyTable


def test_get_header():
    header = ["header1", "header2", "header3"]
    pt = PrettyTable(header)
    assert pt.get_header() == "|      header1     |      header2     |      header3     |"


def test_get_row():
    header = ["header1", "header2", "header3"]
    pt = PrettyTable(header)
    row = pt.get_row("row1", "row2", "row3")
    assert row == "|       row1       |       row2       |       row3       |"
