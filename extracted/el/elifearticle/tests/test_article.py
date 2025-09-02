import unittest
import warnings
import time
from elifearticle import article as ea


def generate_date(date_string="2013-10-03", date_format="%Y-%m-%d"):
    return time.strptime(date_string, date_format)


class TestArticle(unittest.TestCase):
    def setUp(self):
        self.article = ea.Article()

    def add_dates(self):
        "for reuse in testing add_date and get_date, add these dates"
        date_accepted = ea.ArticleDate("accepted", generate_date("2017-07-02"))
        date_received = ea.ArticleDate("received", generate_date("2017-07-04"))
        self.article.add_date(date_accepted)
        self.article.add_date(date_received)

    def add_datasets(self):
        "for reuse in testing add_dataset and get_datasets, add these datasets"
        for dataset_type in ["datasets", "prev_published_datasets"]:
            dataset = ea.Dataset()
            dataset.dataset_type = dataset_type
            self.article.add_dataset(dataset)

    def test_article_init(self):
        self.assertEqual(self.article.article_type, "research-article")
        self.assertEqual(self.article.publication_state, None)

    def test_add_contributor(self):
        contributor = None
        self.article.add_contributor(contributor)
        self.assertEqual(len(self.article.contributors), 1)

    def test_add_research_organism(self):
        research_organism = None
        self.article.add_research_organism(research_organism)
        self.assertEqual(len(self.article.research_organisms), 1)

    def test_add_date(self):
        self.add_dates()
        self.assertEqual(len(self.article.dates), 2)

    def test_get_date(self):
        self.add_dates()
        date_accepted = self.article.get_date("accepted")
        date_received = self.article.get_date("received")
        not_a_date = self.article.get_date("not_a_date")
        self.assertEqual(date_accepted.date, generate_date("2017-07-02"))
        self.assertEqual(date_received.date, generate_date("2017-07-04"))
        self.assertEqual(not_a_date, None)

    def test_get_display_channel(self):
        self.assertEqual(self.article.get_display_channel(), None)

    def test_add_article_category(self):
        category = None
        self.article.add_article_category(category)
        self.assertEqual(len(self.article.article_categories), 1)

    def test_has_contributor_conflict(self):
        self.assertEqual(self.article.has_contributor_conflict(), False)
        author = ea.Contributor("author", "Insect", "Amber")
        author.set_conflict("A conflict")
        self.article.add_contributor(author)
        self.assertEqual(self.article.has_contributor_conflict(), True)

    def test_add_ethic(self):
        ethic = None
        self.article.add_ethic(ethic)
        self.assertEqual(len(self.article.ethics), 1)

    def test_add_author_keyword(self):
        keyword = None
        self.article.add_author_keyword(keyword)
        self.assertEqual(len(self.article.author_keywords), 1)

    def test_add_dataset(self):
        self.add_datasets()
        self.assertEqual(len(self.article.datasets), 2)

    def test_get_datasets(self):
        self.add_datasets()
        self.assertEqual(len(self.article.get_datasets()), 2)
        self.assertEqual(len(self.article.get_datasets("datasets")), 1)
        self.assertEqual(len(self.article.get_datasets("prev_published_datasets")), 1)

    def test_add_funding_award(self):
        funding_award = None
        self.article.add_funding_award(funding_award)
        self.assertEqual(len(self.article.funding_awards), 1)

    def test_unicode(self):
        "for test coverage of lists and dict"
        self.article.datasets = []
        self.article.license = {}
        self.assertIsNotNone(str(self.article))

    def test_add_self_uri(self):
        uri = ea.Uri()
        self.article.add_self_uri(uri)
        self.assertEqual(len(self.article.self_uri_list), 1)

    def test_get_self_uri(self):
        uri = ea.Uri()
        self.article.add_self_uri(uri)
        uri2 = ea.Uri()
        uri2.content_type = "pdf"
        self.article.add_self_uri(uri2)
        self.assertIsNotNone(self.article.get_self_uri(None))
        self.assertIsNotNone(self.article.get_self_uri("pdf"))
        self.assertIsNone(self.article.get_self_uri("not_a_valid_type"))


class TestArticleDate(unittest.TestCase):
    def test_article_date_init(self):
        article_date = ea.ArticleDate("test", generate_date())
        self.assertEqual(article_date.date_type, "test")


class TestContributor(unittest.TestCase):
    def setUp(self):
        self.contributor = ea.Contributor("author", "Insect", "Amber")

    def test_contributor_init(self):
        self.assertEqual(self.contributor.contrib_type, "author")

    def test_set_affiliation(self):
        affiliation = None
        self.contributor.set_affiliation(affiliation)
        self.assertEqual(len(self.contributor.affiliations), 1)

    def test_set_conflict(self):
        conflict = "A conflict"
        self.contributor.set_conflict(conflict)
        self.assertEqual(self.contributor.conflict, [conflict])
        # add another one
        self.contributor.set_conflict(conflict)
        self.assertEqual(self.contributor.conflict, [conflict, conflict])


class TestAffiliation(unittest.TestCase):
    def setUp(self):
        self.affiliation = ea.Affiliation()

    def test_affilation_init(self):
        self.assertIsNotNone(self.affiliation)


class TestRole(unittest.TestCase):
    def test_role_init(self):
        text = "Reviewing Editor"
        specific_use = "editor"
        role = ea.Role(text, specific_use)
        expected = {"text": text, "specific_use": specific_use}
        self.assertEqual(str(role), str(expected))


class TestDataset(unittest.TestCase):
    def setUp(self):
        self.dataset = ea.Dataset()

    def test_dataset_init(self):
        self.assertIsNotNone(self.dataset)

    def test_add_author(self):
        author = None
        self.dataset.add_author(author)
        self.assertEqual(len(self.dataset.authors), 1)


class TestAward(unittest.TestCase):
    def setUp(self):
        self.award = ea.Award()

    def test_award_init(self):
        self.assertIsNotNone(self.award)


class TestFundingAward(unittest.TestCase):
    def setUp(self):
        self.funding_award = ea.FundingAward()

    def test_funding_award_init(self):
        self.assertIsNotNone(self.funding_award)

    def test_add_principal_award_recipient(self):
        principal_award_recipient = None
        self.funding_award.add_principal_award_recipient(principal_award_recipient)
        self.assertEqual(len(self.funding_award.principal_award_recipients), 1)

    def test_get_funder_identifier(self):
        institution_id = "http://dx.doi.org/10.13039/100004440"
        self.funding_award.institution_id = institution_id
        self.assertEqual(self.funding_award.get_funder_identifier(), "100004440")

    def test_get_funder_identifier_fail(self):
        # test failure
        institution_id = 1
        self.funding_award.institution_id = institution_id
        self.assertEqual(self.funding_award.get_funder_identifier(), None)

        # test success
        institution_id = "http://dx.doi.org/10.13039/100004440"
        self.funding_award.institution_id = institution_id
        self.assertEqual(self.funding_award.get_funder_identifier(), "100004440")

    def test_get_funder_name(self):
        institution_name = "institution_name"
        self.funding_award.institution_name = institution_name
        self.assertEqual(self.funding_award.get_funder_name(), institution_name)


class TestLicense(unittest.TestCase):
    def setUp(self):
        self.license = ea.License()

    def test_license_init(self):
        self.assertIsNotNone(self.license)

    def test_license_1(self):
        license_object = ea.License(1)
        self.assertIsNotNone(license_object)

    def test_license_2(self):
        license_object = ea.License(2)
        self.assertIsNotNone(license_object)


class TestCitation(unittest.TestCase):
    def setUp(self):
        self.citation = ea.Citation()

    def test_citation_init(self):
        self.assertIsNotNone(self.citation)

    def test_add_author(self):
        author = None
        self.citation.add_author(author)
        self.assertEqual(len(self.citation.authors), 1)

    def test_get_journal_title(self):
        source = "source_name"
        self.citation.source = source
        self.assertEqual(self.citation.get_journal_title(), source)


class TestComponent(unittest.TestCase):
    def setUp(self):
        self.component = ea.Component()

    def test_component_init(self):
        self.assertIsNotNone(self.component)


class TestRelatedArticle(unittest.TestCase):
    def setUp(self):
        self.related_article = ea.RelatedArticle()

    def test_related_article_init(self):
        self.assertIsNotNone(self.related_article)


class TestContentBlock(unittest.TestCase):
    def test_content_block(self):
        """test blank content block"""
        content_block = ea.ContentBlock()
        self.assertEqual(content_block.attr_names(), [])

    def test_content_block_attr(self):
        """test attributes function"""
        content_block = ea.ContentBlock(
            "disp-quote", None, {"content-type": "editor-comment"}
        )
        content_block.attr["escaped"] = '"'
        self.assertEqual(
            sorted(content_block.attr_names()), ["content-type", "escaped"]
        )
        self.assertEqual(
            content_block.attr_string(),
            ' content-type="editor-comment" escaped="&quot;"',
        )


if __name__ == "__main__":
    unittest.main()
