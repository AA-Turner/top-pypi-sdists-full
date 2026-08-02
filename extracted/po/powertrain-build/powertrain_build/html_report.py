# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module for html report generation."""
from string import Template


class HtmlReport:
    """Generate template html report. Extend this class to add content.

    TODO: Refactor common parts from derived report classes to this class.
    """

    __html_head = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {
        counter-reset: h2;
        font-family:"Segoe UI","Segoe",Tahoma,Helvetica,Arial,sans-serif;
    }
    h1 {text-align: center}
    h2 {counter-reset: h3}
    h3 {counter-reset: h4}
    h4 {counter-reset: h5}
    h5 {counter-reset: h6}
    h2:before {counter-increment: h2; content: counter(h2) ". "}
    h3:before {counter-increment: h3; content: counter(h2) "." counter(h3) ". "}
    h4:before {counter-increment: h4; content: counter(h2) "." counter(h3) "." counter(h4) ". "}
    h5:before {counter-increment: h5; content: counter(h2) "." counter(h3) "." counter(h4) "." counter(h5) ". "}
    h6:before {
      counter-increment: h6; content: counter(h2) "." counter(h3) "." counter(h4) "." counter(h5) "." counter(h6) ". "
    }
    h2.nocount:before, h3.nocount:before, h4.nocount:before, h5.nocount:before, h6.nocount:before {
      content: ""; counter-increment: none
    }
    p {
        padding-left:5mm;
    }
    table {
        width:95%;
        margin-left:5mm
    }
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    th, td {
        padding: 5px;
        text-align: left;
    }
    table tr:nth-child(even) {
        background-color: #eee;
    }
    table tr:nth-child(odd) {
        background-color:#fff;
    }
    table th {
        background-color: black;
        color: white;
    }
    ol {
        list-style-type: none;
        counter-reset: item;
        margin: 0;
        padding-left:5mm;
    }
    ol > li {
        display: table;
        counter-increment: item;
        margin-bottom: 0.6em;
    }
    ol > li:before {
        content: counters(item, ".") ". ";
        display: table-cell;
        padding-right: 0.6em;
    }
    li ol > li {
        margin: 0;
    }
    li ol > li:before {
        content: counters(item, ".") " ";
    }
</style>
<title>$title</title>
</head>
<body>
<h1>$title</h1>
"""

    __html_end = """</body>
</html>
"""

    def __init__(self, title):
        """Initialize report title.

        Args:
            title (str): The report title
        """
        super().__init__()
        self._title = title

    def _gen_header(self):
        """Generate html header."""
        return Template(self.__html_head).substitute(title=self._title)

    @staticmethod
    def gen_contents():
        """Generate report contents.

        Override this method to add report contents.
        Contents should start with a <h2> header.
        """
        return '<h2>Template report</h2>'

    def _gen_end(self):
        """Generate the end of the body and html document."""
        return self.__html_end

    def generate_report_string(self):
        """Generate a html report as string."""
        html = []
        html += self._gen_header()
        html += self.gen_contents()
        html += self._gen_end()
        return ''.join(html)

    def generate_report_file(self, filename):
        """Generate a html report and save to file."""
        with open(filename, 'w', encoding="utf-8") as fhndl:
            fhndl.write(self.generate_report_string())
