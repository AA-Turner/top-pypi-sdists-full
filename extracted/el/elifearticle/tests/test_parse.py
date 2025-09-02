import unittest
import os
from collections import OrderedDict
from elifearticle import parse
from elifearticle.article import Preprint
from tests import XLS_PATH


class TestParseXml(unittest.TestCase):
    def setUp(self):
        self.passes = []
        self.passes.append(os.path.join(XLS_PATH, "elife-02935-v2.xml"))
        self.passes.append(os.path.join(XLS_PATH, "elife-04637-v2.xml"))
        self.passes.append(os.path.join(XLS_PATH, "elife-15743-v1.xml"))
        self.passes.append(os.path.join(XLS_PATH, "elife-02043-v2.xml"))
        self.passes.append(os.path.join(XLS_PATH, "elife-14003.xml"))
        self.passes.append(os.path.join(XLS_PATH, "elife-00666.xml"))
        self.passes.append(os.path.join(XLS_PATH, "cstp77-jats.xml"))

    def test_parse(self):
        articles = parse.build_articles_from_article_xmls(self.passes)
        self.assertEqual(len(articles), 7)

    def test_parse_build_parts_default(self):
        "test parse build parts"

        def check_article(article):
            "function for repeatable article assertions for the two builds"
            self.assertNotEqual(article.abstract, "")
            self.assertNotEqual(article.elocation_id, "")
            self.assertGreater(len(article.article_categories), 0)
            self.assertGreater(len(article.component_list), 0)
            self.assertGreater(len(article.contributors), 0)
            self.assertGreater(len(article.funding_awards), 0)
            self.assertGreater(len(article.dates), 0)
            self.assertIsNotNone(article.get_date("received"))
            self.assertIsNotNone(article.is_poa)
            self.assertGreater(len(article.author_keywords), 0)
            self.assertIsNotNone(article.get_date("pub"))

        def check_article_15743(article):
            "function for repeatable article assertions for the two builds"
            self.assertGreater(len(article.related_articles), 0)

        # first, default build parts should build all parts
        article_xmls = [os.path.join(XLS_PATH, "elife-02043-v2.xml")]
        article = parse.build_articles_from_article_xmls(article_xmls)[0]
        check_article(article)
        # also check building an article with a related article
        article_xmls = [os.path.join(XLS_PATH, "elife-15743-v1.xml")]
        article = parse.build_articles_from_article_xmls(article_xmls)[0]
        check_article_15743(article)
        # second, set all the build parts and the result should be the same
        detail = "full"
        build_parts = [
            "abstract",
            "basic",
            "categories",
            "components",
            "contributors",
            "datasets",
            "funding",
            "history",
            "is_poa",
            "keywords",
            "license",
            "pub_dates",
            "references",
            "related_articles",
            "research_organisms",
            "volume",
            "sub_articles",
        ]
        article_xmls = [os.path.join(XLS_PATH, "elife-02043-v2.xml")]
        article = parse.build_articles_from_article_xmls(
            article_xmls, detail, build_parts
        )[0]
        check_article(article)
        # also check building an article with a related article
        article_xmls = [os.path.join(XLS_PATH, "elife-15743-v1.xml")]
        article = parse.build_articles_from_article_xmls(
            article_xmls, detail, build_parts
        )[0]
        check_article_15743(article)

    def test_parse_build_parts_basic(self):
        "test building with very basic build parts"
        detail = "brief"
        build_parts = ["basic"]
        article_xmls = [os.path.join(XLS_PATH, "elife-02043-v2.xml")]
        article = parse.build_articles_from_article_xmls(
            article_xmls, detail, build_parts
        )[0]
        # check the result
        # elocation_id will exist, but not other parts we check
        self.assertNotEqual(article.elocation_id, "")
        self.assertEqual(article.abstract, "")
        self.assertEqual(len(article.article_categories), 0)
        self.assertIsNone(article.display_channel)
        self.assertEqual(len(article.component_list), 0)
        self.assertEqual(len(article.contributors), 0)
        self.assertEqual(len(article.funding_awards), 0)
        self.assertEqual(article.dates, {})
        self.assertIsNone(article.get_date("received"))
        self.assertIsNone(article.is_poa)
        self.assertEqual(len(article.author_keywords), 0)
        self.assertIsNone(article.get_date("pub"))
        self.assertEqual(len(article.related_articles), 0)
        # also check building an article with a related article
        article_xmls = [os.path.join(XLS_PATH, "elife-15743-v1.xml")]
        article = parse.build_articles_from_article_xmls(
            article_xmls, detail, build_parts
        )[0]
        self.assertEqual(len(article.related_articles), 0)


class TestBuildContributors(unittest.TestCase):
    def test_build_contributors(self):
        "test for when a contributor has no surname"
        authors = [{"given-name": "Foo"}]
        contrib_type = "author"
        self.assertEqual(parse.build_contributors(authors, contrib_type), [])

    def test_build_contributors_affiliations(self):
        "test for contributor with affiliations"
        aff = {
            "dept": "A Test Department",
            "institution": "School of Biological Sciences, University of Bristol",
            "city": "Bristol",
            "country": "United Kingdom",
            "ror": "https://ror.org/0524sp257",
        }
        authors = [
            {
                "surname": "Bar",
                "affiliations": [aff],
            }
        ]
        contrib_type = "author"
        contributors = parse.build_contributors(authors, contrib_type)
        affiliation_object = contributors[0].affiliations[0]
        self.assertEqual(getattr(affiliation_object, "department"), aff.get("dept"))
        self.assertEqual(
            getattr(affiliation_object, "institution"), aff.get("institution")
        )
        self.assertEqual(getattr(affiliation_object, "city"), aff.get("city"))
        self.assertEqual(getattr(affiliation_object, "country"), aff.get("country"))
        self.assertEqual(getattr(affiliation_object, "ror"), aff.get("ror"))
        self.assertEqual(
            getattr(affiliation_object, "text"),
            "%s, %s, %s, %s"
            % (
                aff.get("dept"),
                aff.get("institution"),
                aff.get("city"),
                aff.get("country"),
            ),
        )

    def test_build_anonymous_contributor(self):
        "test for an anonymous contributor"
        authors = [{"anonymous": True, "role": "Reviewer", "type": "author"}]
        contrib_type = "author"
        contributors = parse.build_contributors(authors, contrib_type)
        self.assertEqual(contributors[0].anonymous, True)
        self.assertEqual(contributors[0].surname, None)
        self.assertEqual(contributors[0].roles, [])


class TestBuildPreprint(unittest.TestCase):
    def test_build_preprint_no_events(self):
        events = []
        self.assertIsNone(parse.build_preprint(events))

    def test_build_preprint_no_event_type(self):
        events = [OrderedDict([("uri", "https://not-a-print.example.org")])]
        self.assertIsNone(parse.build_preprint(events))

    def test_build_preprint_not_preprint(self):
        events = [
            OrderedDict(
                [
                    ("event_type", "not_a_preprint"),
                    ("uri", "https://not-a-print.example.org"),
                ]
            )
        ]
        self.assertIsNone(parse.build_preprint(events))

    def test_build_preprint_uri(self):
        uri = "https://example.org/preprint/"
        events = [OrderedDict([("event_type", "preprint"), ("uri", uri)])]
        expected = Preprint(uri=uri)
        self.assertEqual(str(parse.build_preprint(events)), str(expected))

    def test_build_preprint_doi(self):
        "use an eLife article DOI as the preprint doi for testing purposes"
        doi = "10.7554/eLife.00666"
        uri = "https://doi.org/%s" % doi
        events = [OrderedDict([("event_type", "preprint"), ("uri", uri)])]
        expected = Preprint(uri=uri, doi=doi)
        self.assertEqual(str(parse.build_preprint(events)), str(expected))

    def test_build_preprint_two_preprints(self):
        uri_one = "https://example.org/preprint_one/"
        uri_two = "https://example.org/preprint_one/"
        events = [
            OrderedDict([("event_type", "preprint"), ("uri", uri_one)]),
            OrderedDict([("event_type", "preprint"), ("uri", uri_two)]),
        ]
        expected = Preprint(uri=uri_one)
        self.assertEqual(str(parse.build_preprint(events)), str(expected))
