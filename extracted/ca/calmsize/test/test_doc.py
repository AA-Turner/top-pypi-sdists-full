import unittest, doctest

def test_suite():
    return unittest.TestSuite((
            doctest.DocFileSuite('../README.md'),
            #doctest.DocTestSuite('../calmsize/calmsize'),
        ))
