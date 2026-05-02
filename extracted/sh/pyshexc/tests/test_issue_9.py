import os

from pyshexc.parser_impl.generate_shexj import generate


def test_fhir_uri():
    """ Test that parser can process a URI """
    assert generate('https://raw.githubusercontent.com/shexSpec/shexTest/main/doc/ShExR.shex -nr -nj')


def test_fhir_local_file():
    """ Test the schema that has UTF8 BOM """
    datafile = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'observation.shex'))
    assert generate([datafile, '-nr', '-nj'])


def test_shextest_uri():
    assert generate('https://raw.githubusercontent.com/shexSpec/shexTest/master/schemas/1dotNS2.shex -nr -nj')
