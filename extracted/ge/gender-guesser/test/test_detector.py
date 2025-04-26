# -*- coding: utf-8 -*-
import unittest
import gender_guesser.detector as d


class TestDetector(unittest.TestCase):

    def setUp(self):
        self.case = d.Detector()
        self.incase = d.Detector(case_sensitive=False)

    def test_gender(self):
        self.assertEqual(self.case.get_gender(u"Bob"), u"male")
        self.assertEqual(self.case.get_gender(u"Sally"), u"female")
        self.assertEqual(self.case.get_gender(u"Pauley"), u"andy")

    def test_unicode(self):
        self.assertEqual(self.case.get_gender(u"Álfrún"), u"female")
        self.assertEqual(self.case.get_gender(u"Ayşe"), u"female")
        self.assertEqual(self.case.get_gender(u"Gavriliţă"), u"female")
        self.assertEqual(self.case.get_gender(u"İsmet"), u"male")
        self.assertEqual(self.case.get_gender(u"Snæbjörn"), u"male")

    def test_country(self):
        self.assertEqual(self.case.get_gender(u"Jamie"), u"mostly_female")
        self.assertEqual(self.case.get_gender(u"Jamie", u"great_britain"),
                         u"mostly_male")
        self.assertEqual(self.case.get_gender(u"Alžbeta", "slovakia"), u"female")
        self.assertEqual(self.case.get_gender(u"Buğra", "turkey"), u"male")

    def test_case(self):
        self.assertEqual(self.incase.get_gender(u"sally"), u"female")
        self.assertEqual(self.incase.get_gender(u"Sally"), u"female")
        self.assertEqual(self.incase.get_gender(u"aydın"), u"male")
        self.assertEqual(self.incase.get_gender(u"Aydın"), u"male")

    def test_composite_name(self):
        self.assertEqual(self.case.get_gender(u"María del Rosario"), u"female")
        self.assertEqual(self.case.get_gender(u"Maria de Jesus"), u"female")
        self.assertEqual(self.case.get_gender(u"Maria"), u"female")

    def test_unknown(self):
        self.assertEqual(self.incase.get_gender(u"UnexistentName"), u"unknown")

if __name__ == '__main__':
    unittest.main()
