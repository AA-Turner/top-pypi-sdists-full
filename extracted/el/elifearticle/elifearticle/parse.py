"""
Build article objects by parsing article XML
"""

from __future__ import print_function
from collections import OrderedDict

from elifetools import parseJATS as parser
from elifetools import utils as eautils
from elifearticle import article as ea
from elifearticle import utils


def build_contributors(authors, contrib_type, competing_interests=None):
    """
    Given a list of authors from the parser, instantiate contributors
    objects and build them
    """

    contributors = []

    for author in authors:
        contributor = None
        author_contrib_type = contrib_type

        surname = author.get("surname")
        given_name = author.get("given-names")
        collab = author.get("collab")

        # Small hack for on-behalf-of type when building authors
        #  use on-behalf-of as the contrib_type
        if author.get("type") and author.get("type") == "on-behalf-of":
            collab = author.get("on-behalf-of")
            author_contrib_type = "on-behalf-of"

        if surname or collab or author.get("anonymous"):
            contributor = ea.Contributor(
                author_contrib_type, surname, given_name, collab
            )
            contributor.anonymous = author.get("anonymous")
        else:
            # if no surname then do not add the contributor
            continue

        utils.set_attr_if_value(contributor, "suffix", author.get("suffix"))

        contributor.group_author_key = author.get("group-author-key")
        contributor.orcid = author.get("orcid")
        contributor.corresp = bool(author.get("corresp"))
        if author.get("equal-contrib") == "yes":
            contributor.equal_contrib = True

        # Add contributor affiliations
        for aff in author.get("affiliations", []):
            affiliation = ea.Affiliation()
            # set individual attributes
            utils.set_attr_if_value(affiliation, "city", aff.get("city"))
            utils.set_attr_if_value(affiliation, "country", aff.get("country"))
            utils.set_attr_if_value(affiliation, "department", aff.get("dept"))
            utils.set_attr_if_value(affiliation, "institution", aff.get("institution"))
            utils.set_attr_if_value(affiliation, "ror", aff.get("ror"))
            # generate text value
            affiliation.text = utils.text_from_affiliation_elements(
                aff.get("dept"),
                aff.get("institution"),
                aff.get("city"),
                aff.get("country"),
            )
            # fall back if no other fields are set take the text content
            if affiliation.text == "":
                affiliation.text = aff.get("text")
            contributor.set_affiliation(affiliation)

        # competing interests / conflicts
        if (
            competing_interests
            and author.get("references")
            and "competing-interest" in author.get("references")
        ):
            for ref_id in author["references"]["competing-interest"]:
                for competing_interest in competing_interests:
                    if (
                        competing_interest.get("text")
                        and competing_interest.get("id") == ref_id
                    ):
                        clean_text = utils.remove_tag(
                            "p", competing_interest.get("text")
                        )
                        contributor.set_conflict(clean_text)

        # Finally add the contributor to the list
        if contributor:
            contributors.append(contributor)

    return contributors


def build_funding(award_groups):
    """
    Given a funding data, format it
    """
    if not award_groups:
        return []

    funding_awards = []

    for award_groups_item in award_groups:
        for award_group_id, award_group in award_groups_item.items():
            award = ea.FundingAward()
            award.award_group_id = award_group_id
            award.institution_id = award_group.get("id")
            award.institution_id_type = award_group.get("id-type")

            award.institution_name = award_group.get("institution")

            # TODO !!! Check for multiple award_id, if exists
            if award_group.get("award-id"):
                # new Award logic
                award_object = ea.Award()
                award_object.award_id = award_group.get("award-id")
                award_object.award_id_type = award_group.get("award-id-type")
                award.add_award(award_object)

            funding_awards.append(award)

    return funding_awards


def build_datasets(datasets_json):
    """
    Given datasets in JSON format, build and return a list of dataset objects
    """
    if not datasets_json:
        return []

    datasets = []
    dataset_type_map = OrderedDict(
        [("generated", "datasets"), ("used", "prev_published_datasets")]
    )
    dataset_type_map_found = []
    # First look for the types of datasets present
    for dataset_key, dataset_type in dataset_type_map.items():
        if datasets_json.get(dataset_key):
            dataset_type_map_found.append(dataset_key)
    # Continue with the found dataset types
    for dataset_key in dataset_type_map_found:
        dataset_type = dataset_type_map.get(dataset_key)
        for dataset_values in datasets_json.get(dataset_key):
            dataset = ea.Dataset()
            utils.set_attr_if_value(dataset, "dataset_type", dataset_type)
            utils.set_attr_if_value(dataset, "year", dataset_values.get("date"))
            utils.set_attr_if_value(dataset, "title", dataset_values.get("title"))
            utils.set_attr_if_value(dataset, "comment", dataset_values.get("details"))
            utils.set_attr_if_value(dataset, "doi", dataset_values.get("doi"))
            utils.set_attr_if_value(dataset, "uri", dataset_values.get("uri"))
            utils.set_attr_if_value(
                dataset, "accession_id", dataset_values.get("dataId")
            )
            utils.set_attr_if_value(
                dataset, "assigning_authority", dataset_values.get("assigningAuthority")
            )
            # authors
            if dataset_values.get("authors"):
                # parse JSON format authors into author objects
                for author_json in dataset_values.get("authors"):
                    if utils.author_name_from_json(author_json):
                        dataset.add_author(utils.author_name_from_json(author_json))
            # Try to populate the doi attribute if the uri is a doi
            if not dataset.doi and dataset.uri:
                if dataset.uri != eautils.doi_uri_to_doi(dataset.uri):
                    dataset.doi = eautils.doi_uri_to_doi(dataset.uri)
            datasets.append(dataset)
    return datasets


def build_data_availability(datasets_json):
    """
    Given datasets in JSON format, get the data availability from it if present
    """
    data_availability = None
    if "availability" in datasets_json and datasets_json.get("availability"):
        # only expect one paragraph of text
        data_availability = datasets_json.get("availability")[0].get("text")
    return data_availability


def build_ref_list(refs):
    """
    Given parsed references build a list of ref objects
    """
    ref_list = []
    for reference in refs:
        ref = ea.Citation()
        # Publcation Type
        utils.set_attr_if_value(
            ref, "publication_type", reference.get("publication-type")
        )
        # id
        utils.set_attr_if_value(ref, "id", reference.get("id"))
        # Article title
        utils.set_attr_if_value(
            ref, "article_title", reference.get("full_article_title")
        )
        # Source
        utils.set_attr_if_value(ref, "source", reference.get("source"))
        # Volume
        utils.set_attr_if_value(ref, "volume", reference.get("volume"))
        # Issue
        utils.set_attr_if_value(ref, "issue", reference.get("issue"))
        # First page
        utils.set_attr_if_value(ref, "fpage", reference.get("fpage"))
        # Last page
        utils.set_attr_if_value(ref, "lpage", reference.get("lpage"))
        # DOI
        utils.set_attr_if_value(ref, "doi", reference.get("doi"))
        # Year
        utils.set_attr_if_value(ref, "year", reference.get("year"))
        # Year date in iso 8601 format
        utils.set_attr_if_value(
            ref, "year_iso_8601_date", reference.get("year-iso-8601-date")
        )
        # Can set the year_numeric now
        if ref.year_iso_8601_date is not None:
            # First preference take it from the iso 8601 date, if available
            try:
                ref.year_numeric = int(ref.year_iso_8601_date.split("-")[0])
            except ValueError:
                ref.year_numeric = None
        if ref.year_numeric is None:
            # Second preference, use the year value if it is entirely numeric
            if utils.is_year_numeric(ref.year):
                ref.year_numeric = ref.year
        # date-in-citation
        utils.set_attr_if_value(
            ref, "date_in_citation", reference.get("date-in-citation")
        )
        # elocation-id
        utils.set_attr_if_value(ref, "elocation_id", reference.get("elocation-id"))
        # uri
        utils.set_attr_if_value(ref, "uri", reference.get("uri"))
        if not ref.uri:
            # take uri value from uri_text
            utils.set_attr_if_value(ref, "uri", reference.get("uri_text"))
        # pmid
        utils.set_attr_if_value(ref, "pmid", reference.get("pmid"))
        # isbn
        utils.set_attr_if_value(ref, "isbn", reference.get("isbn"))
        # accession
        utils.set_attr_if_value(ref, "accession", reference.get("accession"))
        # patent
        utils.set_attr_if_value(ref, "patent", reference.get("patent"))
        # patent country
        utils.set_attr_if_value(ref, "country", reference.get("country"))
        # publisher-loc
        utils.set_attr_if_value(ref, "publisher_loc", reference.get("publisher_loc"))
        # publisher-name
        utils.set_attr_if_value(ref, "publisher_name", reference.get("publisher_name"))
        # edition
        utils.set_attr_if_value(ref, "edition", reference.get("edition"))
        # version
        utils.set_attr_if_value(ref, "version", reference.get("version"))
        # chapter-title
        utils.set_attr_if_value(ref, "chapter_title", reference.get("chapter-title"))
        # comment
        utils.set_attr_if_value(ref, "comment", reference.get("comment"))
        # data-title
        utils.set_attr_if_value(ref, "data_title", reference.get("data-title"))
        # conf-name
        utils.set_attr_if_value(ref, "conf_name", reference.get("conf-name"))
        # Authors
        if reference.get("authors"):
            for author in reference.get("authors"):
                ref_author = {}
                eautils.set_if_value(ref_author, "group-type", author.get("group-type"))
                eautils.set_if_value(ref_author, "surname", author.get("surname"))
                eautils.set_if_value(
                    ref_author, "given-names", author.get("given-names")
                )
                eautils.set_if_value(ref_author, "collab", author.get("collab"))
                if ref_author:
                    ref.add_author(ref_author)
        # Try to populate the doi attribute if the uri is a doi
        if not ref.doi and ref.uri:
            if ref.uri != eautils.doi_uri_to_doi(ref.uri):
                ref.doi = eautils.doi_uri_to_doi(ref.uri)
        # Append the reference to the list
        ref_list.append(ref)
    return ref_list


def component_title(component):
    """
    Label, title and caption
    Title is the label text plus the title text
    Title may contain italic tag, etc.
    """

    title = ""

    label_text = ""
    title_text = ""
    if component.get("label"):
        label_text = component.get("label")

    if component.get("title"):
        title_text = component.get("title")

    title = str(label_text)
    if label_text != "" and title_text != "":
        title += " "
    title += str(title_text)

    if component.get("type") == "abstract" and title == "":
        title = "Abstract"

    return title


def build_components(components):
    """
    Given parsed components build a list of component objects
    """
    component_list = []

    for comp in components:
        component = ea.Component()

        # id
        component.id = comp.get("id")

        # type
        component.type = comp.get("type")

        # asset, if available
        component.asset = comp.get("asset")

        # DOI
        component.doi = comp.get("doi")

        if component_title(comp) != "":
            component.title = component_title(comp)

        # Subtitle
        if comp.get("type") in ["supplementary-material", "fig"]:

            if comp.get("full_caption"):
                subtitle = comp.get("full_caption")
                subtitle = clean_abstract(subtitle)
                component.subtitle = subtitle

        # Mime type
        if comp.get("type") in [
            "abstract",
            "table-wrap",
            "sub-article",
            "chem-struct-wrap",
            "boxed-text",
        ]:
            component.mime_type = "text/plain"
        if comp.get("type") in ["fig"]:
            component.mime_type = "image/tiff"
        elif comp.get("type") in ["media", "supplementary-material"]:
            if comp.get("mimetype") and comp.get("mime-subtype"):
                component.mime_type = (
                    comp.get("mimetype") + "/" + comp.get("mime-subtype")
                )

        # Permissions
        component.permissions = comp.get("permissions")

        # Append it to our list of components
        component_list.append(component)

    return component_list


def build_review_articles(sub_articles):
    """populate an article review_articles property with data from sub_articles"""
    article_list = []
    for sub_article in sub_articles:
        article = ea.Article(sub_article.get("doi"), sub_article.get("article_title"))
        utils.set_attr_if_value(
            article, "article_type", sub_article.get("article_type")
        )
        utils.set_attr_if_value(article, "id", sub_article.get("id"))
        # contributors
        if sub_article.get("contributors"):
            for contributor in sub_article.get("contributors"):
                article.contributors += build_contributors(
                    [contributor], contributor.get("type")
                )
        # related objects
        if sub_article.get("related_objects"):
            for related_object in sub_article.get("related_objects"):
                related_object_object = ea.RelatedObject()
                utils.set_attr_if_value(
                    related_object_object, "id", related_object.get("id")
                )
                utils.set_attr_if_value(
                    related_object_object, "link_type", related_object.get("link_type")
                )
                utils.set_attr_if_value(
                    related_object_object,
                    "xlink_href",
                    related_object.get("xlink_href"),
                )
                article.related_objects.append(related_object_object)

        # use the parent article license as the sub article license
        license_object = None
        if sub_article.get("parent_license_url"):
            license_object = ea.License()
            license_object.href = sub_article.get("parent_license_url")
            article.license = license_object
        # make the parent article a related article, avoids circular references
        related_article = ea.Article(
            sub_article.get("parent_doi"), sub_article.get("parent_article_title")
        )
        utils.set_attr_if_value(
            related_article, "article_type", sub_article.get("parent_article_type")
        )
        if license_object:
            related_article.license = license_object
        article.related_articles.append(related_article)
        # append article to the list of review articles
        article_list.append(article)
    return article_list


def build_related_articles(related_articles):
    """
    Given parsed data build a list of related article objects
    """
    article_list = []

    for related_article in related_articles:
        article = ea.RelatedArticle()
        if related_article.get("xlink_href"):
            article.xlink_href = related_article.get("xlink_href")
        if related_article.get("related_article_type"):
            article.related_article_type = related_article.get("related_article_type")
        if related_article.get("ext_link_type"):
            article.ext_link_type = related_article.get("ext_link_type")

        # Append it to our list
        article_list.append(article)

    return article_list


def build_pub_dates(article, pub_dates):
    "convert pub_dates into ArticleDate objects and add them to article"
    for pub_date in pub_dates:
        # always want a date type, take it from pub-type if must
        if pub_date.get("date-type"):
            date_instance = ea.ArticleDate(
                pub_date.get("date-type"), pub_date.get("date")
            )
        elif pub_date.get("pub-type"):
            date_instance = ea.ArticleDate(
                pub_date.get("pub-type"), pub_date.get("date")
            )
        # Set more values
        utils.set_attr_if_value(date_instance, "pub_type", pub_date.get("pub-type"))
        utils.set_attr_if_value(
            date_instance, "publication_format", pub_date.get("publication-format")
        )
        utils.set_attr_if_value(date_instance, "day", pub_date.get("day"))
        utils.set_attr_if_value(date_instance, "month", pub_date.get("month"))
        utils.set_attr_if_value(date_instance, "year", pub_date.get("year"))
        article.add_date(date_instance)


def build_self_uri_list(self_uri_list):
    "parse the self-uri tags, build Uri objects"
    uri_list = []
    for self_uri in self_uri_list:
        uri = ea.Uri()
        utils.set_attr_if_value(uri, "xlink_href", self_uri.get("xlink_href"))
        utils.set_attr_if_value(uri, "content_type", self_uri.get("content-type"))
        uri_list.append(uri)
    return uri_list


def build_preprint(pub_history_events):
    preprint = ea.Preprint()
    for event in pub_history_events:
        if event.get("event_type") == "preprint":
            preprint.uri = event.get("uri")
            # Try to populate the doi attribute if the uri is a doi
            if preprint.uri and preprint.uri != eautils.doi_uri_to_doi(preprint.uri):
                preprint.doi = eautils.doi_uri_to_doi(preprint.uri)
            break
    if preprint.uri or preprint.doi:
        return preprint
    return None


def build_publication_history(pub_history_events):
    event_list = []
    for event in pub_history_events:
        event_object = ea.Event()
        event_object.uri = event.get("uri")
        # Try to populate the doi attribute if the uri is a doi
        if event_object.uri and event_object.uri != eautils.doi_uri_to_doi(
            event_object.uri
        ):
            event_object.doi = eautils.doi_uri_to_doi(event_object.uri)
        # more Event properties
        event_object.event_type = event.get("event_type")
        event_object.event_desc = event.get("event_desc")
        event_object.date = event.get("date")
        # add to the list of events
        event_list.append(event_object)
    return event_list


def build_clinical_trials(clinical_trials):
    clinical_trial_list = []
    for clinical_trial in clinical_trials:
        clinical_trial_object = ea.ClinicalTrial()
        attr_map = {
            "id": "id",
            "content-type": "content_type",
            "document-id": "document_id",
            "document-id-type": "document_id_type",
            "source-id": "source_id",
            "source-id-type": "source_id_type",
            "source-type": "source_type",
            "text": "text",
            "xlink_href": "xlink_href",
        }
        for dict_key, attr_name in attr_map.items():
            utils.set_attr_if_value(
                clinical_trial_object, attr_name, clinical_trial.get(dict_key)
            )
        clinical_trial_list.append(clinical_trial_object)
    return clinical_trial_list


def clean_abstract(abstract, remove_tags=None):
    """
    Remove unwanted tags from abstract string,
    parsing it as HTML, then only keep the body paragraph contents
    """
    if remove_tags is None:
        remove_tags = ["xref", "ext-link", "inline-formula", "mml:*"]
    if remove_tags:
        for tag_name in remove_tags:
            abstract = utils.remove_tag(tag_name, abstract)
    return abstract


def build_part_check(part, build_parts):
    """
    check if only specific parts were specified to be build when parsing
    if the list build_parts is empty, then all parts will be parsed
    """
    if not build_parts:
        return True
    return bool(part in build_parts)


def build_article_from_xml(
    article_xml_filename, detail="brief", build_parts=None, remove_tags=None
):
    """
    Parse JATS XML with elifetools parser, and populate an
    eLifePOA article object
    Basic data crossref needs: article_id, doi, title, contributors with names set
    detail="brief" is normally enough,
    detail="full" will populate all the contributor affiliations that are linked by xref tags
    """

    def build_part(part):
        return build_part_check(part, build_parts)

    error_count = 0

    soup = parser.parse_document(article_xml_filename)

    # Get DOI
    doi = parser.doi(soup)

    # Create the article object
    article = ea.Article(doi, title=None)

    # article version from the filename if possible
    utils.set_attr_if_value(
        article, "version", utils.version_from_xml_filename(article_xml_filename)
    )

    # version doi
    if build_part("basic"):
        article.version_doi = parser.version_doi(soup)

    # journal title
    if build_part("basic"):
        article.journal_title = parser.journal_title(soup)

    # issn
    if build_part("basic"):
        article.journal_issn = parser.journal_issn(soup, "electronic")
        if article.journal_issn is None:
            article.journal_issn = parser.journal_issn(soup)

    # Related articles
    if build_part("related_articles"):
        article.related_articles = build_related_articles(parser.related_article(soup))

    # Get publisher_id pii
    if build_part("basic"):
        article.pii = parser.publisher_id(soup)

    # set object manuscript value
    if build_part("basic"):
        manuscript = parser.publisher_id(soup)
        if not manuscript and doi:
            # try to get it from the DOI
            manuscript = doi.split(".")[-1]
        article.manuscript = manuscript

    # Set the articleType
    if build_part("basic"):
        article_type = parser.article_type(soup)
        if article_type:
            article.article_type = article_type

    # Set the publication_state
    if build_part("basic"):
        article.publication_state = parser.publication_state(soup)

    # title
    if build_part("basic"):
        article.title = parser.full_title(soup)
    # print article.title

    # publisher_name
    if build_part("basic"):
        article.publisher_name = parser.publisher(soup)

    # publisher_name
    if build_part("basic"):
        article.clinical_trials = build_clinical_trials(parser.clinical_trials(soup))

    # abstract
    if build_part("abstract"):
        article.abstract = clean_abstract(parser.full_abstract(soup), remove_tags)
        article.abstract_json = parser.abstract_json(soup)
        article.abstract_xml = parser.abstract_xml(soup)

    # digest
    if build_part("abstract"):
        article.digest = clean_abstract(parser.full_digest(soup), remove_tags)

    # elocation-id
    if build_part("basic"):
        article.elocation_id = parser.elocation_id(soup)

    # issue
    if build_part("basic"):
        article.issue = parser.issue(soup)

    # self-uri
    if build_part("basic"):
        article.self_uri_list = build_self_uri_list(parser.self_uri(soup))

    # preprint
    if build_part("basic"):
        article.preprint = build_preprint(parser.pub_history(soup))

    # publication history events
    if build_part("basic"):
        article.publication_history = build_publication_history(
            parser.pub_history(soup)
        )

    # contributors
    if build_part("contributors"):
        # get the competing interests if available
        competing_interests = parser.competing_interests(soup, None)
        all_contributors = parser.contributors(soup, detail)
        author_contributors = [
            con
            for con in all_contributors
            if con.get("type") in ["author", "on-behalf-of"]
        ]
        contrib_type = "author"
        contributors = build_contributors(
            author_contributors, contrib_type, competing_interests
        )

        contrib_type = "author non-byline"
        authors = parser.authors_non_byline(soup, detail)
        contributors_non_byline = build_contributors(
            authors, contrib_type, competing_interests
        )
        article.contributors = contributors + contributors_non_byline

        # also populate the editors when contributors flag is being built
        editor_contrib_types = ["assoc_ed", "editor", "reviewer", "senior_editor"]
        for contrib_type in editor_contrib_types:
            editor_contributors = [
                con for con in all_contributors if con.get("type") == contrib_type
            ]
            article.editors += build_contributors(editor_contributors, contrib_type)

    # license href
    if build_part("license"):
        license_object = ea.License()
        license_object.href = parser.license_url(soup)
        license_object.copyright_statement = parser.copyright_statement(soup)
        article.license = license_object

    # article_category
    if build_part("categories"):
        article.article_categories = parser.category(soup)

    # display channel
    if build_part("categories"):
        article.display_channel = eautils.firstnn(parser.display_channel(soup))

    # keywords
    if build_part("keywords"):
        article.author_keywords = parser.keywords(soup)

    # research organisms
    if build_part("research_organisms"):
        article.research_organisms = parser.research_organism(soup)

    # funding awards
    if build_part("funding"):
        article.funding_awards = build_funding(parser.full_award_groups(soup))

    # datasets
    if build_part("datasets"):
        datasets_json = parser.datasets_json(soup)
        article.datasets = build_datasets(datasets_json)
        article.data_availability = build_data_availability(datasets_json)

    # references or citations
    if build_part("references"):
        article.ref_list = build_ref_list(parser.refs(soup))

    # components with component DOI
    if build_part("components"):
        article.component_list = build_components(parser.components(soup))

    # History dates
    if build_part("history"):
        date_types = ["received", "accepted", "sent-for-review"]
        for date_type in date_types:
            history_date = parser.history_date(soup, date_type)
            if history_date:
                date_instance = ea.ArticleDate(date_type, history_date)
                article.add_date(date_instance)

    # Pub date
    if build_part("pub_dates"):
        build_pub_dates(article, parser.pub_dates(soup))

    # Set the volume if present
    if build_part("volume"):
        volume = parser.volume(soup)
        if volume:
            article.volume = volume

    if build_part("is_poa"):
        article.is_poa = parser.is_poa(soup)

    # peer review articles
    if build_part("sub_articles"):
        article.review_articles = build_review_articles(parser.sub_articles(soup))

    return article, error_count


def build_articles_from_article_xmls(
    article_xmls, detail="full", build_parts=None, remove_tags=None
):
    """
    Given a list of article XML filenames, convert to article objects
    """

    poa_articles = []

    for article_xml in article_xmls:
        print("working on ", article_xml)
        article, error_count = build_article_from_xml(
            article_xml, detail, build_parts, remove_tags
        )
        if error_count == 0:
            poa_articles.append(article)

    return poa_articles
