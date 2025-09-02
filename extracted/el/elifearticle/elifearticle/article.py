"""
Article object definitions
"""

from collections import OrderedDict
from elifearticle import utils


class BaseObject:
    "base object for shared functions"

    def __str__(self):
        """
        Return `str` representation of the simple object properties,
        if there is a list or dict just return an empty representation
        for easier viewing and test case scenario writing
        """
        _dict = {}
        for key in self.__dict__:
            if isinstance(self.__dict__.get(key), list):
                _dict[key] = []
            elif isinstance(self.__dict__.get(key), dict):
                _dict[key] = {}
            else:
                _dict[key] = str(self.__dict__.get(key))
        return str(_dict)


class Article(BaseObject):
    """
    We include some boiler plate in the init, namely article_type
    """

    contributors = []

    def __init__(self, doi=None, title=None):
        self.article_type = "research-article"
        self.publication_state = None
        self.display_channel = None
        self.doi = doi
        self.version_doi = None
        self.id = None
        self.contributors = []
        self.editors = []
        self.title = title
        self.abstract = ""
        self.abstract_json = None
        self.abstract_xml = None
        self.digest = None
        self.research_organisms = []
        self.manuscript = None
        self.dates = {}
        self.license = None
        self.article_categories = []
        self.conflict_default = None
        self.ethics = []
        self.author_keywords = []
        self.funding_awards = []
        self.ref_list = []
        self.component_list = []
        # For PubMed function a hook to specify if article was ever through PoA pipeline
        self.was_ever_poa = None
        self.is_poa = None
        self.volume = None
        self.elocation_id = None
        self.pii = None
        self.related_articles = []
        self.version = None
        self.datasets = []
        self.data_availability = None
        self.funding_awards = []
        self.funding_note = None
        self.journal_issn = None
        self.journal_title = None
        self.self_uri_list = []
        self.version = None
        self.publisher_name = None
        self.issue = None
        self.review_articles = []
        self.clinical_trials = []
        self.preprint = None
        self.related_objects = []
        self.publication_history = []
        # group_title for use in posted_content Crossref deposits of preprints
        self.group_title = None

    def add_contributor(self, contributor):
        self.contributors.append(contributor)

    def add_research_organism(self, research_organism):
        self.research_organisms.append(research_organism)

    def add_date(self, date):
        self.dates[date.date_type] = date

    def get_date(self, date_type):
        "get date by date type"
        try:
            return self.dates[date_type]
        except (KeyError, TypeError):
            return None

    def get_display_channel(self):
        "display-channel string partly relates to the article_type"
        return self.display_channel

    def add_article_category(self, article_category):
        self.article_categories.append(article_category)

    def has_contributor_conflict(self):
        # Return True if any contributors have a conflict
        for contributor in self.contributors:
            if contributor.conflict:
                return True
        return False

    def add_ethic(self, ethic):
        self.ethics.append(ethic)

    def add_author_keyword(self, author_keyword):
        self.author_keywords.append(author_keyword)

    def add_dataset(self, dataset):
        self.datasets.append(dataset)

    def get_datasets(self, dataset_type=None):
        if dataset_type:
            return [d for d in self.datasets if d.dataset_type == dataset_type]
        return self.datasets

    def add_funding_award(self, funding_award):
        self.funding_awards.append(funding_award)

    def add_self_uri(self, uri):
        self.self_uri_list.append(uri)

    def get_self_uri(self, content_type):
        "return the first self uri with the content_type"
        try:
            return [
                self_uri
                for self_uri in self.self_uri_list
                if self_uri.content_type == content_type
            ][0]
        except IndexError:
            return None

    def pretty(self):
        "sort values and format output for viewing and comparing in test scenarios"
        pretty_obj = OrderedDict()
        for key, value in sorted(self.__dict__.items()):
            if value is None:
                pretty_obj[key] = None
            elif isinstance(value, str):
                pretty_obj[key] = self.__dict__.get(key)
            elif isinstance(value, list):
                pretty_obj[key] = []
            elif isinstance(value, dict):
                pretty_obj[key] = {}
            else:
                pretty_obj[key] = str(value)
        return pretty_obj


class ArticleDate(BaseObject):
    """
    A struct_time date and a date_type
    """

    date_type = None
    date = None
    pub_type = None
    publication_format = None
    day = None
    month = None
    year = None

    def __init__(self, date_type, date):
        self.date_type = date_type
        # Date as a time.struct_time
        self.date = date


class Contributor(BaseObject):
    """
    Currently we are not sure that we can get an auth_id for
    all contributors, so this attribute remains an optional attribute.
    """

    corresp = False
    equal_contrib = False

    contrib_type = None
    auth_id = None
    orcid = None
    orcid_authenticated = None  # True or False for ORCID authenticated status
    surname = None
    given_name = None
    suffix = None
    collab = None
    conflict = []
    group_author_key = None
    anonymous = None
    roles = []

    def __init__(self, contrib_type, surname, given_name, collab=None):
        self.contrib_type = contrib_type
        self.surname = surname
        self.given_name = given_name
        self.affiliations = []
        self.conflict = []
        self.collab = collab

    def set_affiliation(self, affiliation):
        self.affiliations.append(affiliation)

    def set_conflict(self, conflict):
        self.conflict.append(conflict)


class Affiliation(BaseObject):
    phone = None
    fax = None
    email = None
    department = None
    institution = None
    city = None
    country = None
    ror = None
    text = None

    def __init__(self):
        pass


class Role(BaseObject):
    def __init__(self, text=None, specific_use=None):
        self.text = text
        self.specific_use = specific_use


class Dataset(BaseObject):
    """
    Article component representing a dataset
    """

    def __init__(self):
        self.dataset_type = None
        self.authors = []
        # source_id is the uri in PoA generation
        # todo: refactor PoA use the uri attribute then delete the source_id attribute here
        self.source_id = None
        self.year = None
        self.title = None
        self.license_info = None
        self.accession_id = None
        self.assigning_authority = None
        self.doi = None
        self.uri = None
        self.comment = None

    def add_author(self, author):
        self.authors.append(author)


class Award(BaseObject):
    "an Award, part of a FundingAward"

    def __init__(self):
        self.award_id = None
        self.award_id_type = None


class FundingAward(BaseObject):
    """
    An award group as part of a funding group
    """

    def __init__(self):
        self.award_group_id = None
        self.institution_name = None
        self.institution_id = None
        self.institution_id_type = None
        self.principal_award_recipients = []
        self.awards = []

    def add_award(self, award):
        self.awards.append(award)

    def add_principal_award_recipient(self, contributor):
        "Accepts an instance of Contributor"
        self.principal_award_recipients.append(contributor)

    def get_funder_identifier(self):
        "Funder identifier is the unique id found in the institution_id DOI"
        try:
            return self.institution_id.split("/")[-1]
        except AttributeError:
            return None

    def get_funder_name(self):
        "Alias for institution_name parsed from the XML"
        return self.institution_name


class License(BaseObject):
    """
    License with some preset values by license_id
    """

    license_id = None
    license_type = None
    copyright = False
    copyright_statement = None
    href = None
    name = None
    paragraph1 = None
    paragraph2 = None

    def __init__(self, license_id=None):
        self.license_id = license_id


class Citation(BaseObject):
    """
    A ref or citation in the article to support crossref VOR deposits initially
    """

    def __init__(self):
        self.publication_type = None
        self.id = None
        self.authors = []
        # For journals
        self.article_title = None
        self.source = None
        self.volume = None
        self.issue = None
        self.fpage = None
        self.lpage = None
        self.elocation_id = None
        self.doi = None
        self.uri = None
        self.pmid = None
        self.isbn = None
        self.year = None
        self.year_iso_8601_date = None
        self.year_numeric = None
        self.date_in_citation = None
        self.publisher_loc = None
        self.publisher_name = None
        self.edition = None
        self.version = None
        self.comment = None
        self.data_title = None
        self.conf_name = None
        # For patents
        self.patent = None
        self.country = None
        # For books
        self.volume_title = None
        self.chapter_title = None
        # For data
        self.accession = None

    def add_author(self, author):
        "Author is a dict of values"
        self.authors.append(author)

    def get_journal_title(self):
        "Alias for source"
        return self.source


class Component(BaseObject):
    """
    An article component with a component DOI, primarily for crossref VOR deposits
    """

    def __init__(self):
        self.id = None
        self.type = None
        self.asset = None
        self.title = None
        self.subtitle = None
        self.mime_type = None
        self.doi = None
        self.doi_resource = None
        self.permissions = None


class RelatedArticle(BaseObject):
    """
    Related article tag data as an object
    """

    def __init__(self):
        self.xlink_href = None
        self.related_article_type = None
        self.ext_link_type = None


class Uri(BaseObject):
    "A URI, initially created for holding self-uri data"

    def __init__(self):
        self.xlink_href = None
        self.content_type = None


class RelatedObject(BaseObject):
    def __init__(self):
        self.id = None
        self.xlink_href = None
        self.link_type = None


class ClinicalTrial(BaseObject):
    def __init__(self):
        self.id = None
        self.content_type = None
        self.document_id = None
        self.document_id_type = None
        self.source_id = None
        self.source_id_type = None
        self.source_type = None
        self.text = None
        self.xlink_href = None
        self.registry_doi = None

    def get_registry_doi(self, registry_name_to_doi_map=None):
        """return the DOI for the registry"""
        if self.registry_doi:
            return self.registry_doi
        if (
            self.source_id_type
            and self.source_id
            and self.source_id_type == "crossref-doi"
        ):
            return self.source_id
        if (
            registry_name_to_doi_map
            and self.source_id_type
            and self.source_id
            and self.source_id_type == "registry-name"
        ):
            # look for the DOI value in the name to DOI map
            if self.source_id in registry_name_to_doi_map:
                return registry_name_to_doi_map[self.source_id]
        return None


class Preprint(BaseObject):
    def __init__(self, uri=None, doi=None):
        self.uri = uri
        self.doi = doi


class Event(BaseObject):
    def __init__(self):
        self.uri = None
        self.doi = None
        self.event_type = None
        self.event_desc = None
        self.date = None


class ContentBlock:
    def __init__(self, block_type=None, content=None, attr=None):
        self.block_type = block_type
        self.content = content
        self.content_blocks = []
        self.attr = {}
        if attr:
            self.attr = attr

    def attr_names(self):
        """list of tag attribute names"""
        return utils.attr_names(self.attr)

    def attr_string(self):
        """tag attributes formatted as a string"""
        return utils.attr_string(self.attr)
