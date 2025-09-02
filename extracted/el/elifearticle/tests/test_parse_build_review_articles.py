import unittest
from collections import OrderedDict
from elifearticle import parse


class TestParseBuildReviewArticles(unittest.TestCase):
    def setUp(self):
        pass

    def test_build_review_articles(self):
        "test building an editor's evaluation review article"
        sub_articles_data = [
            OrderedDict(
                [
                    ("doi", "10.7554/eLife.00666.sa0"),
                    ("article_type", "editor-report"),
                    ("id", "sa0"),
                    ("article_title", "Editor's evaluation"),
                    (
                        "contributors",
                        [
                            {
                                "type": "author",
                                "role": "Reviewing Editor",
                                "surname": "Ma",
                                "given-names": "Yuting",
                                "affiliations": [
                                    {
                                        "institution": "Suzhou Institute of Systems Medicine",
                                        "country": "China",
                                    }
                                ],
                            }
                        ],
                    ),
                    (
                        "related_objects",
                        [
                            OrderedDict(
                                [
                                    ("id", "ro1"),
                                    ("link_type", "continued-by"),
                                    (
                                        "xlink_href",
                                        "https://sciety.org/articles/activity/10.1101/2020.11.21.391326",
                                    ),
                                ]
                            )
                        ],
                    ),
                    ("parent_doi", "10.7554/eLife.00666"),
                    ("parent_article_type", "research-article"),
                    ("parent_article_title", "The eLife research article"),
                    (
                        "parent_license_url",
                        "http://creativecommons.org/licenses/by/4.0/",
                    ),
                ]
            )
        ]
        review_articles = parse.build_review_articles(sub_articles_data)
        self.assertEqual(review_articles[0].doi, "10.7554/eLife.00666.sa0")
        self.assertEqual(review_articles[0].title, "Editor's evaluation")
        self.assertEqual(review_articles[0].article_type, "editor-report")
        self.assertEqual(review_articles[0].id, "sa0")
        # contributor
        self.assertEqual(review_articles[0].contributors[0].contrib_type, "author")
        self.assertEqual(review_articles[0].contributors[0].surname, "Ma")
        self.assertEqual(review_articles[0].contributors[0].given_name, "Yuting")
        self.assertEqual(
            review_articles[0].contributors[0].affiliations[0].text,
            "Suzhou Institute of Systems Medicine, China",
        )
        # license
        self.assertEqual(
            review_articles[0].license.href,
            "http://creativecommons.org/licenses/by/4.0/",
        )
        # related objects
        self.assertEqual(review_articles[0].related_objects[0].id, "ro1")
        self.assertEqual(
            review_articles[0].related_objects[0].link_type, "continued-by"
        )
        self.assertEqual(
            review_articles[0].related_objects[0].xlink_href,
            "https://sciety.org/articles/activity/10.1101/2020.11.21.391326",
        )
        # related article
        self.assertEqual(
            review_articles[0].related_articles[0].article_type, "research-article"
        )
        self.assertEqual(
            review_articles[0].related_articles[0].doi, "10.7554/eLife.00666"
        )
