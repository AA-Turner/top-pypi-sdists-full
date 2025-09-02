import unittest
from elifetools import utils as etoolsutils
from elifearticle import parse
from tests import XLS_PATH


class TestParseDeep(unittest.TestCase):
    def test_parse_article_02935_simple(self):
        "some simple comparisons and count list items"
        article_object, error_count = parse.build_article_from_xml(
            XLS_PATH + "elife-02935-v2.xml", detail="full"
        )
        # test pretty method for test coverage
        self.assertIsNotNone(article_object.pretty())
        # list of individual comparisons of interest
        self.assertEqual(article_object.doi, "10.7554/eLife.02935")
        self.assertEqual(article_object.version_doi, None)
        self.assertEqual(article_object.journal_issn, "2050-084X")
        # count contributors
        self.assertEqual(len(article_object.contributors), 180)
        self.assertEqual(
            len([c for c in article_object.contributors if c.contrib_type == "author"]),
            53,
        )
        self.assertEqual(
            len(
                [
                    c
                    for c in article_object.contributors
                    if c.contrib_type == "author non-byline"
                ]
            ),
            127,
        )
        self.assertEqual(
            len([c for c in article_object.contributors if c.collab is not None]), 3
        )
        # first contributor has no suffix
        self.assertEqual(article_object.contributors[0].suffix, None)
        # first contributor did not contribute equally
        self.assertEqual(article_object.contributors[0].equal_contrib, False)
        # first contributor affiliation
        self.assertEqual(
            article_object.contributors[0].affiliations[0].text,
            "Cancer Genome Project, Wellcome Trust Sanger Institute, Hinxton, United Kingdom",
        )
        # anonymous value
        self.assertEqual(article_object.contributors[0].anonymous, None)
        # count editors
        self.assertEqual(len(article_object.editors), 1)
        # first editor
        self.assertEqual(article_object.editors[0].contrib_type, "editor")
        self.assertEqual(article_object.editors[0].surname, "Golub")
        self.assertEqual(article_object.editors[0].given_name, "Todd")
        self.assertEqual(
            article_object.editors[0].affiliations[0].text,
            "Broad Institute, United States",
        )
        # ethics - not parsed yet
        self.assertEqual(len(article_object.ethics), 0)
        # compare dates
        self.assertEqual(
            article_object.dates.get("received").date,
            etoolsutils.date_struct(2014, 3, 28),
        )
        self.assertEqual(
            article_object.dates.get("accepted").date,
            etoolsutils.date_struct(2014, 9, 26),
        )
        self.assertEqual(
            article_object.dates.get("pub").date, etoolsutils.date_struct(2014, 10, 1)
        )
        self.assertEqual(article_object.dates.get("pub").day, "01")
        self.assertEqual(article_object.dates.get("pub").month, "10")
        self.assertEqual(article_object.dates.get("pub").year, "2014")
        self.assertEqual(
            article_object.dates.get("pub").publication_format, "electronic"
        )
        # datasets
        self.assertEqual(len(article_object.datasets), 2)
        self.assertEqual(article_object.datasets[0].accession_id, "EGAS00001000968")
        # review_articles
        self.assertEqual(len(article_object.review_articles), 2)
        # review_article 1
        self.assertEqual(
            article_object.review_articles[0].doi, "10.7554/eLife.02935.027"
        )
        self.assertEqual(
            article_object.review_articles[0].article_type, "article-commentary"
        )
        self.assertEqual(
            article_object.review_articles[0].publication_state, None
        )
        self.assertEqual(article_object.review_articles[0].id, "SA1")
        self.assertEqual(article_object.review_articles[0].title, "Decision letter")
        self.assertEqual(
            article_object.review_articles[0].license.href,
            "http://creativecommons.org/publicdomain/zero/1.0/",
        )
        self.assertEqual(len(article_object.review_articles[0].contributors), 1)
        self.assertEqual(
            article_object.review_articles[0].contributors[0].surname, "Golub"
        )
        self.assertEqual(
            article_object.review_articles[0].contributors[0].given_name, "Todd"
        )
        self.assertEqual(
            article_object.review_articles[0].contributors[0].contrib_type, "editor"
        )
        self.assertEqual(
            article_object.review_articles[0].contributors[0].affiliations[0].text,
            "Broad Institute, United States",
        )
        self.assertEqual(
            article_object.review_articles[0].related_articles[0].doi,
            "10.7554/eLife.02935",
        )
        self.assertEqual(
            article_object.review_articles[0].related_articles[0].article_type,
            "research-article",
        )
        # review_articles 2
        self.assertEqual(
            article_object.review_articles[1].doi, "10.7554/eLife.02935.028"
        )
        self.assertEqual(article_object.review_articles[1].article_type, "reply")
        self.assertEqual(article_object.review_articles[1].id, "SA2")
        self.assertEqual(article_object.review_articles[1].title, "Author response")
        # related_articles
        self.assertEqual(len(article_object.related_articles), 0)
        # funding
        self.assertEqual(len(article_object.funding_awards), 16)
        # award
        self.assertEqual(
            article_object.funding_awards[5].awards[0].award_id, "ALTF 1203_2012"
        )
        # keywords
        self.assertEqual(len(article_object.author_keywords), 6)
        # categories
        self.assertEqual(len(article_object.article_categories), 1)
        # display channel
        self.assertEqual(article_object.display_channel, "Research Article")
        # research organism
        self.assertEqual(len(article_object.research_organisms), 1)
        # components
        self.assertEqual(len(article_object.component_list), 28)
        # refs
        self.assertEqual(len(article_object.ref_list), 59)
        # self_uri_list
        self.assertEqual(len(article_object.self_uri_list), 1)
        self.assertIsNotNone(article_object.get_self_uri("pdf"))
        self.assertEqual(
            article_object.get_self_uri("pdf").xlink_href, "elife-02935-v2.pdf"
        )
        # version
        self.assertEqual(article_object.version, 2)
        # publisher_name
        self.assertEqual(
            article_object.publisher_name, "eLife Sciences Publications, Ltd"
        )
        # issue
        self.assertEqual(article_object.issue, None)
        # license
        self.assertEqual(
            article_object.license.href,
            "http://creativecommons.org/publicdomain/zero/1.0/",
        )
        self.assertEqual(article_object.license.copyright_statement, None)
        # elocation_id
        self.assertEqual(article_object.elocation_id, "e02935")
        # manuscript
        self.assertEqual(article_object.manuscript, "02935")
        # publisher_id pii
        self.assertEqual(article_object.pii, "02935")

    def test_parse_article_00666_simple(self):
        "some simple comparisons and count list items"
        article_object, error_count = parse.build_article_from_xml(
            XLS_PATH + "elife-00666.xml", detail="full"
        )
        # list of individual comparisons of interest
        self.assertEqual(article_object.doi, "10.7554/eLife.00666")
        self.assertEqual(article_object.journal_issn, "2050-084X")
        # count contributors
        self.assertEqual(len(article_object.contributors), 14)
        self.assertEqual(
            len([c for c in article_object.contributors if c.contrib_type == "author"]),
            4,
        )
        self.assertEqual(
            len(
                [
                    c
                    for c in article_object.contributors
                    if c.contrib_type == "on-behalf-of"
                ]
            ),
            1,
        )
        self.assertEqual(
            len(
                [
                    c
                    for c in article_object.contributors
                    if c.contrib_type == "author non-byline"
                ]
            ),
            9,
        )
        self.assertEqual(
            len([c for c in article_object.contributors if c.collab is not None]), 3
        )
        # first contributor has a suffix
        self.assertEqual(article_object.contributors[0].suffix, "Jnr")
        # first contributor contributed equally
        self.assertEqual(article_object.contributors[0].equal_contrib, True)
        # first contributor has one conflict of interest
        self.assertEqual(len(article_object.contributors[0].conflict), 1)
        self.assertEqual(article_object.contributors[0].conflict, ["Chair of JATS4R"])
        # first contributor affiliation
        self.assertEqual(
            article_object.contributors[0].affiliations[0].department,
            "Department of Production",
        )
        self.assertEqual(
            article_object.contributors[0].affiliations[0].institution,
            "eLife",
        )
        self.assertEqual(
            article_object.contributors[0].affiliations[0].city,
            "Cambridge",
        )
        self.assertEqual(
            article_object.contributors[0].affiliations[0].country,
            "United Kingdom",
        )
        self.assertEqual(
            article_object.contributors[0].affiliations[0].ror,
            None,
        )
        self.assertEqual(
            article_object.contributors[0].affiliations[0].text,
            "Department of Production, eLife, Cambridge, United Kingdom",
        )
        # ethics - not parsed yet
        self.assertEqual(len(article_object.ethics), 0)
        # compare dates
        self.assertEqual(
            article_object.dates.get("received").date,
            etoolsutils.date_struct(2016, 3, 1),
        )
        self.assertEqual(
            article_object.dates.get("accepted").date,
            etoolsutils.date_struct(2016, 4, 1),
        )
        self.assertEqual(
            article_object.dates.get("publication").date,
            etoolsutils.date_struct(2016, 4, 25),
        )
        self.assertEqual(article_object.dates.get("publication").day, "25")
        self.assertEqual(article_object.dates.get("publication").month, "04")
        self.assertEqual(article_object.dates.get("publication").year, "2016")
        self.assertEqual(
            article_object.dates.get("publication").publication_format, "electronic"
        )
        # datasets
        self.assertEqual(len(article_object.datasets), 3)
        self.assertEqual(len(article_object.get_datasets("datasets")), 1)
        self.assertEqual(len(article_object.get_datasets("prev_published_datasets")), 2)
        self.assertEqual(len(article_object.datasets[0].authors), 2)
        self.assertEqual(article_object.datasets[0].dataset_type, "datasets")
        self.assertEqual(article_object.datasets[0].year, "2016")
        self.assertEqual(article_object.datasets[0].title, "xml-mapping")
        self.assertEqual(
            article_object.datasets[0].comment, "Publicly available on GitHub"
        )
        self.assertEqual(
            article_object.datasets[0].uri,
            "https://github.com/elifesciences/XML-mapping/blob/master/elife-00666.xml",
        )
        self.assertEqual(article_object.datasets[0].assigning_authority, None)
        self.assertEqual(article_object.datasets[2].doi, "10.5061/dryad.cv323")
        self.assertEqual(
            article_object.datasets[2].assigning_authority, "Dryad Digital Repository"
        )
        # review_articles
        self.assertEqual(len(article_object.review_articles), 2)
        self.assertEqual(
            article_object.review_articles[0].doi, "10.7554/eLife.00666.029"
        )
        self.assertEqual(
            article_object.review_articles[1].doi, "10.7554/eLife.00666.030"
        )
        # review_article 1
        self.assertEqual(len(article_object.review_articles[0].contributors), 3)
        self.assertEqual(
            article_object.review_articles[0].contributors[0].surname, "Collings"
        )
        self.assertEqual(
            article_object.review_articles[0].contributors[0].contrib_type, "editor"
        )
        self.assertEqual(
            article_object.review_articles[0].contributors[1].surname, "Darian-Smith"
        )
        self.assertEqual(
            article_object.review_articles[0].contributors[1].contrib_type, "reviewer"
        )
        self.assertEqual(
            article_object.review_articles[0].contributors[2].surname, "Smith"
        )
        self.assertEqual(
            article_object.review_articles[0].contributors[2].contrib_type, "reviewer"
        )
        # related_articles
        self.assertEqual(len(article_object.related_articles), 0)
        # funding
        self.assertEqual(len(article_object.funding_awards), 2)
        self.assertEqual(
            article_object.funding_awards[0].institution_name,
            "Howard Hughes Medical Institute",
        )
        self.assertEqual(
            article_object.funding_awards[0].institution_id,
            "https://dx.doi.org/10.13039/100000011",
        )
        self.assertEqual(
            article_object.funding_awards[0].institution_id_type, "FundRef"
        )
        # keywords
        self.assertEqual(len(article_object.author_keywords), 4)
        # categories
        self.assertEqual(len(article_object.article_categories), 2)
        # display channel
        self.assertEqual(article_object.display_channel, "Research Article")
        # research organism
        self.assertEqual(len(article_object.research_organisms), 2)
        # components
        self.assertEqual(len(article_object.component_list), 39)
        # component id examples
        self.assertEqual(article_object.component_list[0].id, None)
        self.assertEqual(article_object.component_list[2].id, "table1")
        # component type examples
        self.assertEqual(article_object.component_list[0].type, "abstract")
        self.assertEqual(article_object.component_list[2].type, "table-wrap")
        self.assertEqual(
            article_object.component_list[5].type, "supplementary-material"
        )
        self.assertEqual(article_object.component_list[9].type, "fig")
        self.assertEqual(article_object.component_list[13].type, "media")
        self.assertEqual(
            article_object.component_list[15].type, "supplementary-material"
        )
        self.assertEqual(article_object.component_list[19].type, "boxed-text")
        self.assertEqual(
            article_object.component_list[22].type, "supplementary-material"
        )
        self.assertEqual(article_object.component_list[34].type, "sub-article")
        self.assertEqual(article_object.component_list[35].type, "sub-article")
        # component asset examples
        self.assertEqual(article_object.component_list[0].asset, None)
        self.assertEqual(article_object.component_list[2].asset, None)
        self.assertEqual(article_object.component_list[5].asset, "data")
        self.assertEqual(article_object.component_list[9].asset, "figsupp")
        self.assertEqual(article_object.component_list[13].asset, "media")
        self.assertEqual(article_object.component_list[15].asset, "code")
        self.assertEqual(article_object.component_list[19].asset, None)
        self.assertEqual(article_object.component_list[22].asset, "supp")
        self.assertEqual(article_object.component_list[34].asset, "dec")
        self.assertEqual(article_object.component_list[35].asset, "resp")
        # refs
        self.assertEqual(len(article_object.ref_list), 54)
        # license
        self.assertEqual(
            article_object.license.href, "http://creativecommons.org/licenses/by/4.0/"
        )
        self.assertEqual(
            article_object.license.copyright_statement, "\u00a9 2016, Harrison et al"
        )
        # elocation_id
        self.assertEqual(article_object.elocation_id, "e00666")
        # manuscript
        self.assertEqual(article_object.manuscript, "00666")
        # publisher_id pii
        self.assertEqual(article_object.pii, "00666")

    def test_parse_article_cstp77_simple(self):
        "some simple comparisons and count list items"
        article_object, error_count = parse.build_article_from_xml(
            XLS_PATH + "cstp77-jats.xml"
        )
        # list of individual comparisons of interest
        self.assertEqual(article_object.doi, "10.5334/cstp.77")
        self.assertEqual(article_object.journal_issn, "2057-4991")
        self.assertEqual(
            article_object.journal_title, "Citizen Science: Theory and Practice"
        )
        # count contributors
        self.assertEqual(len(article_object.contributors), 4)
        self.assertEqual(
            len([c for c in article_object.contributors if c.contrib_type == "author"]),
            4,
        )

        # compare dates
        self.assertEqual(
            article_object.dates.get("received").date,
            etoolsutils.date_struct(2016, 8, 11),
        )
        self.assertEqual(
            article_object.dates.get("accepted").date,
            etoolsutils.date_struct(2017, 3, 28),
        )
        self.assertEqual(
            article_object.dates.get("pub").date, etoolsutils.date_struct(2017, 7, 4)
        )
        self.assertEqual(article_object.dates.get("pub").day, "04")
        self.assertEqual(article_object.dates.get("pub").month, "07")
        self.assertEqual(article_object.dates.get("pub").year, "2017")
        self.assertEqual(
            article_object.dates.get("pub").publication_format, "electronic"
        )
        # keywords
        self.assertEqual(len(article_object.author_keywords), 4)
        # refs
        self.assertEqual(len(article_object.ref_list), 36)
        # publisher_name
        self.assertEqual(article_object.publisher_name, "Ubiquity Press")
        # issue
        self.assertEqual(article_object.issue, "1")
        # elocation_id
        self.assertEqual(article_object.elocation_id, "3")
        # manuscript
        self.assertEqual(article_object.manuscript, "77")
        # publisher_id pii
        self.assertEqual(article_object.pii, None)
        # review_articles, should be empty
        self.assertEqual(len(article_object.review_articles), 0)

    def test_parse_article_1234567890_simple(self):
        "some simple comparisons and count list items"
        article_object, error_count = parse.build_article_from_xml(
            XLS_PATH + "elife-1234567890-v2.xml", detail="full"
        )
        # list of individual comparisons of interest
        self.assertEqual(article_object.doi, "10.7554/eLife.1234567890")
        self.assertEqual(article_object.journal_issn, "2050-084X")
        self.assertEqual(article_object.journal_title, "eLife")
        # count contributors
        self.assertEqual(len(article_object.contributors), 7)
        self.assertEqual(
            len([c for c in article_object.contributors if c.contrib_type == "author"]),
            6,
        )

        # compare dates
        self.assertEqual(
            article_object.dates.get("received"),
            None,
        )
        self.assertEqual(
            article_object.dates.get("accepted"),
            None,
        )
        self.assertEqual(
            article_object.dates.get("publication").date,
            etoolsutils.date_struct(2023, 10, 22),
        )
        self.assertEqual(article_object.dates.get("publication").day, "22")
        self.assertEqual(article_object.dates.get("publication").month, "10")
        self.assertEqual(article_object.dates.get("publication").year, "2023")
        self.assertEqual(
            article_object.dates.get("publication").publication_format, "electronic"
        )
        # keywords
        self.assertEqual(len(article_object.author_keywords), 6)
        # refs
        self.assertEqual(len(article_object.ref_list), 18)
        # publisher_name
        self.assertEqual(
            article_object.publisher_name, "eLife Sciences Publications, Ltd"
        )
        # issue
        self.assertEqual(article_object.issue, None)
        # elocation_id
        self.assertEqual(article_object.elocation_id, "RP1234567890")
        # manuscript
        self.assertEqual(article_object.manuscript, "1234567890")
        # publisher_id pii
        self.assertEqual(article_object.pii, "1234567890")
        # review_articles
        self.assertEqual(len(article_object.review_articles), 8)
        # preprint
        self.assertIsNotNone(article_object.preprint)
        self.assertEqual(
            article_object.preprint.uri, "https://doi.org/10.1101/2021.11.09.467796"
        )
        self.assertEqual(article_object.preprint.doi, "10.1101/2021.11.09.467796")
        # publication history events
        self.assertEqual(len(article_object.publication_history), 4)
        self.assertEqual(
            article_object.publication_history[0].uri,
            "https://doi.org/10.1101/2021.11.09.467796",
        )
        self.assertEqual(
            article_object.publication_history[0].doi, "10.1101/2021.11.09.467796"
        )
        self.assertEqual(
            article_object.publication_history[1].uri,
            "https://doi.org/10.7554/eLife.1234567890.1",
        )
        self.assertEqual(
            article_object.publication_history[1].doi, "10.7554/eLife.1234567890.1"
        )
        self.assertEqual(
            article_object.publication_history[1].event_type, "reviewed-preprint"
        )
        self.assertEqual(
            article_object.publication_history[1].event_desc,
            "This manuscript was published as a reviewed preprint.",
        )
        self.assertEqual(
            article_object.publication_history[1].date,
            etoolsutils.date_struct(2023, 4, 15),
        )
