#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Class Definitions
########
##  Copyright 2017–2021 garrick. Some rights reserved.
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.

##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU Lesser General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.

import html, configparser, datetime, os, logging
import springheel.slugurl
import springheel.splitseps
from springheel.tl import gettext as _


class Site:
    """
    A Springheel comic site.

    The top level of a Springheel instance. It contains all
    :class:`Comic` series and site-related metadata.

    Attributes
    ----------
    author : str
        A single-string version of authors, mostly for compatibility.
    authors : list of str
        A list of strings describing authors whose work appears on the
        site.
    c_path : str
        The current/root directory for this site.
    comics : list of Comic
        A list of :class:`Comic` series/categories.
    config : Config
        Sitewide configuration settings.
    copyright_statement : str
        A copyright statement for the site.
    i_path : str
        The path to the input directory for the site. Will generally be
        the equivalent of ``./input/``.
    images : dict
        A dictionary mapping image filenames to (width, height) in
        pixels.
    jsonpoints : dict
        Information about the site in JSON format.
    license : str
        The license of the overall site.
    o_path : str
        The output path for the site. Will generally be the equivalent
        of ``./output/``.
    processed_authors : dict of str
        Mapping between items from ``raw_authors`` and their processed
        equivalents.
    raw_authors : set of str
        Like ``authors``, but the set of unique author strings
        that appear in comic metadata (i.e. without processing for
        multiple authors, etc.).
    single : bool
        Whether the site is single-comic or not.
    sitemap : list of dict
        Dicts of HTML filenames and last-modified times for all pages.
    """

    __slots__ = [
        "author",
        "authors",
        "c_path",
        "comics",
        "config",
        "copyright_statement",
        "i_path",
        "images",
        "jsonpoints",
        "license",
        "o_path",
        "processed_authors",
        "raw_authors",
        "single",
        "sitemap",
    ]

    def __init__(self):
        """The constructor for the Site class."""
        self.comics = []
        self.sitemap = []
        self.raw_authors = set()
        self.processed_authors = dict()


class Config(object):
    """
    A set of various site preferences.

    Parameters
    ----------
    file_names : str, optional
        Filename of the configuration file.

    Attributes
    ----------
    about : bool, optional
        Whether or not to generate an "about" page describing each
        comic and link it in the top navigation.
    base_url : str
        The root URL for the site. All page URLs are considered relative
        to this.
    characters_page : str
        Whether or not to generate character pages. If "True", character
        file names can be specified in comic config files. If "False",
        they will be ignored.
    country : str
        The legal territory the site is operated from. Mostly used for
        copyright waivers.
    description : str
        A description of the site. Appears in feeds and the like.
    diaspora_url : str
        Social link. Diaspora* stream. This requires a full URL.
    dict : dict
        The original dictionary used to create this object. Based on
        :class:`configparser.ConfigParser`.
    extras_page : str
        If "True", Springheel will convert input/Extra.json to an extras
        page. If "False", it will be ignored.
    header_filename : str
        The name of an image file in `input/` that will appear at the
        top of various pages on the site.
    image_rename_pattern : str
        The pattern used for renaming images in output. Available
        replacement items: ``{titleslug}`` (slugified strip title),
        ``{author}``, ``{height}``, ``{width}``, and ``{ext}``. Defaults to
        "``{comic}_{page}_{titleslug}_{date}.{ext}``".
    json_mode : bool
        Whether to look for files ending in ".meta.json" and
        ".transcript.json" (True) or simply ".meta" and ".transcript"
        (False).
    language : str
        The language the site is in. An ISO 639-1 code (2 letters).
    liberapay_handle : str
        Social link. Liberapay handle. Applied in the form of
        ``https://liberapay.com/{liberapay_handle}``.
    license : str
        An overall copyright statement for the site. HTML accepted.
    mastodon_url : str
        Social link. Mastodon account. This requires a full URL.
    navdirection : str
        Either "ltr" or "rtl". Whether first/previous arrows should
        point to the left and next/last arrows to the right or vice-
        versa.
    patreon_handle : str
        Social link. Patreon handle. Applied in the form of
        ``https://www.patreon.com/{patreon_handle}``.
    pump_url : str
        Social link. Pump microblog. This requires a full URL.
    rename_images : str
        If "True", comic images are renamed according to
        ``image_rename_pattern``.
    site_author : str
        The person or people considered the owner(s) of the site.
    site_author_email : str
        The email address of the owner. Used for RSS feeds because they
        require it for some reason.
    site_style : str
        The name of a theme located in `themes/` that will be loaded as
        the overall site style.
    site_title : str
        The title of the site as a whole.
    site_type : str
        Either "single" or "multi". If single, only one :class:`Comic` is on the site. If multi, the site is a hub for multiple works.
    social_icons : str
        If "True", social media links whose configs aren't set to
        "False" will be displayed on the site. If "False", they will not
        be generated.
    store_page : str
        A URL to link to in the top menu as a store associated with the
        comic, such as a merchandise outlet.
    tumblr_handle : str
        Social link. Tumblr blog. Applied in the form of
        ``http://{tumblr_handle}.tumblr.com``.
    twitter_handle : str
        Social link. A Twitter handle. Applied in the form of
        ``http://twitter.com/{twitter_handle}``.
    zero_padding : str
        Either an integer indicating the number of digits page and
        chapter numbers should be padded to (defaulting to 4) or False
        to disable zero-padding.
    """

    __slots__ = [
        "about",
        "base_url",
        "characters_page",
        "country",
        "description",
        "diaspora_url",
        "dict",
        "extras_page",
        "header_filename",
        "image_rename_pattern",
        "json_mode",
        "language",
        "liberapay_handle",
        "license",
        "mastodon_url",
        "navdirection",
        "patreon_handle",
        "pump_url",
        "rename_images",
        "site_author",
        "site_author_email",
        "site_style",
        "site_title",
        "site_type",
        "social_icons",
        "store_page",
        "tumblr_handle",
        "twitter_handle",
        "zero_padding",
    ]

    def __init__(self, *file_names: str):
        """
        The constructor for the Config class.

        Parameters
        ----------
        file_names : str, optional
            Filename of the configuration file.
        """
        parser = configparser.ConfigParser()
        parser.optionxform = str
        found = parser.read(file_names, encoding="utf-8")
        if not found:
            raise ValueError("No cfg file")
        dictified = dict(parser.items("Config"))
        for k, v in dictified.items():
            try:
                v = parser.getboolean("Config", k)
            except ValueError:
                pass
            try:
                setattr(self, k, v)
            except AttributeError:
                logging.warning(
                    _("Unknown preference {k} found in config file").format(k=k)
                )
        setattr(self, "dict", dictified)


class Tag:
    """
    A tag that classifies comic strips.

    An optional element that can be applied to :class:`Strip` items. The
    most specific item available on a Springheel site.

    Parameters
    ----------
    name : str
        The name of the tag.

    Attributes
    ----------
    escaped : str
        An HTML-safe version of name (no &, <, or >).
    link : str
        HTML hyperlink to the tag index URL.
    name : str
        The name of the tag.
    rurl : str
        HTML filename for the tag index.
    slug : str
        name slugified for URLs.
    strips : list
        Strips to which the tag applies.

    Methods
    -------
    gen_links:
        Generate links for a Tag.
    """

    __slots__ = ["escaped", "link", "name", "rurl", "slug", "strips"]

    def __init__(self, name: str):
        """
        The constructor for Tag.

        Parameters
        ----------
        name : str
            The name of the tag.
        """
        self.name = name
        self.escaped = html.escape(name)
        self.slug = springheel.springheel.slugurl.slugify_url(name)
        self.strips = []

    def gen_links(self, translated_strings: dict) -> None:
        """
        Generate links for a Tag.

        Parameters
        ----------
        translated_strings : dict
            The translation file contents for this site.
        """
        self.rurl = "tag-{tag_slug}.html".format(tag_slug=self.slug)
        label = "{tag_s}: {tag}".format(
            tag_s=translated_strings["tag_s"], tag=self.name
        )
        self.link = """<a href="{rurl}" aria-label="{label}">{tag}</a>""".format(
            rurl=self.rurl, tag=self.escaped, label=label
        )


class Strip:
    """
    An individual comic page.

    Part of a :class:`Comic` and optionally a :class:`Chapter`
    as well.

    Parameters
    ----------
    imagef : str
        Filename of the strip image.
    metaf : str
        Filename of the strip's metadata file.
    transf : str
        Filename of the strip's transcript file.

    Attributes
    ----------
    alt_text : str, optional
        Extra text that displays below the strip. Despite the
        name, is not really used as alt text. A more accessible
        version of the title text some comics have.
    archive_link : str
        The text that will link to the strip on the Archives page.
    author : str
        The strip's credited author.
    author_email : str
        The strip's author's email address (for RSS feeds).
    authors : list
        All individuals involved with a strip. If multiple people are
        listed in the metadata file, separated by &, /, or +, they're
        added separately to this list.
    category : str
        The strip's category.
    chapter : int/bool
        The chapter number if a strip is part of a chapter. False if
        it is not.
    clicense : str
        The name of the strip's license.
    commentary : str
        The strip's creator commentary.
    conf_c : dict
        Contents of the strip's config file.
    copyright_statement : str
        The copyright information used in the footer of the page.
    date : datetime.datetime
        The upload date of the strip.
    date_fmt : str
        date formatted according to either ISO 8601 or a locale that
        is basically that, like Japanese. Used on archive pages.
    date_s : str
        date formatted according to ISO 8601 (YYYY-MM-dd).
    figcaption : str, optional
        alt_text wrapped in <figcaption> tags.
    file_name : str
        The output filename for the strip image (without "pages/").
    h1_title : str
        The title used as a top-level heading for the strip.
    header_title : str
        The string used as an HTML <title> element.
    height : str
        The height of the strip image in pixels.
    html_filename : str
        The text used as the output filename (ending in ".html").
    imagef : str
        Input filename of the strip image.
    img : str
        The output path of the strip image.
    lang : str
        ISO 639-1 code (2 letters) for the strip's language.
    license : str
        The copyright status of the strip.
    metadata : dict
        The strip's metadata.
    metaf : str
        Input filename of the strip's metadata file.
    mode : str
        Debug parameter that currently does nothing.
    new_meta : str
        The output filename for the metadata file.
    new_transcr : str
        The output filename for the transcript file.
    page : str
        The strip's page number (directly from the meta file).
    page_padded : str
        The strip's page number formatted with zero-padding.
    page_real_num : int, float, or tuple
        The strip's page number converted to a real number (or a tuple
        containing real numbers).
    page_url : str
        The strip's ultimate URL/permalink.
    permalink : str
        HTML permalink to the strip.
    pieces : str
        HTML ``<img>`` element(s) for this strip.
    raw_comments : list of str
        The strip's commentary without any HTML formatting, etc.
    series_slug : str
        URL-safe slug for the strip's category.
    sha256 : str
        SHA-256 checksum of the strip image. Included for API purposes.
    slug : str
        The HTML filename without the extension, for use as a slug.
    slugs : list
        Title and series slugs.
    source : str, optional
        If available, the URL of an original work on which this strip is
        based. For translations, freely-licensed comics, etc.
    statline : str
        The "posted by x on y date" type line that appears at the
        bottom of the commentary box. HTML paragraph.
    stat_noperma : str
        The statline without a "permalink", for chapter pages.
    tags : list, optional
        A list of :class:`Tag` items used by the strip.
    tb : str
        The formatted HTML transcript block, separated by newlines.
    title : str
        The title of the strip.
    title_slug : str
        URL-safe slug for the strip's title.
    tline : str
        HTML hyperlinked list of tags attached to the strip.
    transcript_block : list
        The <div> elements used to make the transcript block.
    transcript_c : str
        The HTML contents of the transcript (no heading, etc.).
    transf : str
        Input filename of the strip's transcript file.
    width : str
        The width of the strip image in pixels.
    year : int
        The year in which the strip was published.

    Methods
    -------
    get_matching:
        Find the Comic this Strip belongs to.
    populate:
        Add initial information to a comic Strip.
    populate_authors:
        Add author information for the Strip.
    """

    __slots__ = [
        "alt_text",
        "archive_link",
        "author",
        "author_email",
        "authors",
        "category",
        "chapter",
        "clicense",
        "commentary",
        "conf_c",
        "copyright_statement",
        "date",
        "date_fmt",
        "date_s",
        "figcaption",
        "file_name",
        "h1_title",
        "header_title",
        "height",
        "html_filename",
        "imagef",
        "img",
        "lang",
        "license",
        "metadata",
        "metaf",
        "mode",
        "new_meta",
        "new_transcr",
        "page",
        "page_padded",
        "page_real_num",
        "page_url",
        "permalink",
        "pieces",
        "raw_comments",
        "series_slug",
        "sha256",
        "slug",
        "slugs",
        "source",
        "statline",
        "stat_noperma",
        "tags",
        "tb",
        "title",
        "title_slug",
        "tline",
        "transcript_block",
        "transcript_c",
        "transf",
        "width",
        "year",
    ]

    def __init__(self, imagef: str, metaf: str, transf: str):
        """
        The constructor for Strip.

        Parameters
        ----------
        imagef : str
            Filename of the strip image.
        metaf : str
            Filename of the strip's metadata file.
        transf : str
            Filename of the strip's transcript file.
        """
        self.imagef = os.path.basename(imagef)
        self.metaf = metaf
        self.transf = transf
        self.tags = []

    def get_matching(self, ccomics):
        """
        Find the :class:`Comic` this Strip belongs to.

        Parameters
        ----------
        ccomics : list
            A list of Comic objects.

        Returns
        ----------
        Comic
            The matching Comic.
        """
        return [item for item in ccomics if item.category == self.category][0]

    def populate(
        self,
        meta: dict,
        commentary: str,
        raw_comments: list,
        configs: list,
        site: Site,
    ) -> None:
        """
        Add initial information to a comic Strip.

        Parameters
        ----------
        meta : dict
            Metadata about the strip.
        commentary : str
            The comic's commentary.
        raw_comments : list of str
            Raw commentary lines from the comic's metadata file.
        configs : list of dict
            Configuration files known to Springheel.
        site : Site
            The root site
        """
        self.page = meta["page"]
        self.page_real_num, self.page_padded = springheel.padNum(
            self.page, site.config.zero_padding
        )
        if not self.page_padded:
            logging.error(
                _("Unable to parse page number {page}").format(page=self.page)
            )
            return False
        self.metadata = meta
        self.commentary = commentary
        self.raw_comments = raw_comments
        self.category = self.metadata["category"]
        conf_file = os.path.join(site.i_path, self.metadata["conf"])

        try:
            (conf,) = [item for item in configs if item["category"] == self.category]
        except ValueError:
            conf = springheel.parseconf.comicCParse(conf_file)
            configs.append(conf)
        self.conf_c = conf

    def populate_authors(self, site: Site):
        """
        Add author information for the Strip.

        Parameters
        ----------
        site : Site
            The root site, which usually has author data.
        """
        author_dividers = {"&", "/", "+"}
        if self.metadata["author"] not in site.raw_authors:
            # Multiple authors
            i_raw_author = self.metadata["author"]
            site.raw_authors.add(i_raw_author)
            self.author = html.escape(i_raw_author)
            if any([div in i_raw_author for div in author_dividers]):
                self.authors = []
                raw_authors_split = springheel.splitseps.splitAtSeparators(
                    i_raw_author, author_dividers
                )
                for a in raw_authors_split:
                    cleaned_a = html.escape(a).strip()
                    self.authors.append(cleaned_a)
            else:
                self.authors = [self.author]
            site.processed_authors[i_raw_author] = self.authors
        else:
            self.author = self.metadata["author"]
            self.authors = site.processed_authors[self.metadata["author"]]
        self.author_email = self.metadata["email"]


class Comic:
    """
    A comic series or story.

    Initialized with just the name of the comic. The next broadest level
    after :class:`Site`.

    Parameters
    ----------
    category : str
        The name of the comic.
    publicdomain : bool, default: False
        Whether the comic is public domain or not. Necessary for some
        copyright-related stuff.

    Attributes
    ----------
    about : str, optional
        A longer description of the comic, used on about pages.
    author : str
        The comic's creator.
    authors : list
        A list of all authors associated with a comic. Used just in case
        multiple people worked on different strips of a category.
    banner : str
        The comic's banner that appears on the index page.
    headerh : str
        The height of the banner in pixels.
    headerw : str
        The width of the banner in pixels.
    category : str
        The name of the comic.
    category_escaped : str
        HTML-safe category, with entity characters escaped.
    category_theme : str, optional
        Theme used by the comic.
    chapters : bool
        True if the comic is chaptered, False if not.
    chapters_dicts : list, optional
        Dicts with chapter numbers and titles.
    chapters_file : str, optional
        If chapters is True, full path to the chapter file.
    chapters_list : list, optional
        List of Chapters in the comic.
    chars_file : str or None
        If present, the filename of the character file.
    chars_fn : str, optional
        The basename of the characters page, if it exists. Will be
        "characters.html" on single-comic sites and "{category-slug}-
        characters.html" on multiple-comic sites.
    clicense : str
        The original license name specified in the conf file.
    conf_c : dict
        Contents of the comic's config file.
    copyright_statement : str
        An HTML copyright statement.
    desc : str
        A description of the comic for the index.
    email : str
        The comic creator's email address, for RSS feeds.
    fbd_link : list
        HTML filename of the first strip by date.
    fbp_link : list
        HTML filename of the first strip by page number.
    first_page : int
        The first page of the comic.
    header : str
        Filename for the page header of the comic.
    headerh : str
        The height of the page header in pixels.
    headerw : str
        The width of the page header in pixels.
    known_pages : list
        A list of zero-padded page numbers for this category. Used for
        navigation generation.
    known_pages_raw : list
        A list of page numbers for this category. These are the raw
        numbers taken directly from metadata files, so they are strings.
        Some may not be convertible to integers.
    known_pages_real : list
        A list of page numbers for this category. These are real numbers
        -- ints, floats, or tuples containing ints and/or floats.
    language : str
        ISO 639-1 code (2 letters) for the comic's language.
    last_page : int
        The latest page of the comic.
    lbd_link : list
        HTML filename of the last strip by date.
    lbp_link : list
        HTML filename of the last strip by page number.
    license : str
        The comic's license.
    license_uri : str
        The license URI specified in the conf file.
    mode : str
        Debug parameter that currently does nothing.
    pbd : list
        all Strips in the comic, sorted by date.
    pbp : list
        all Strips in the comic, sorted by page number.
    publicdomain : bool
        Whether the comic is public domain or not. Necessary for some
        copyright-related stuff.
    slug : str
        category slugified for URLs.
    status : str
        Whether the comic is still updating or not.
    statuss : str
        status but wrapped in <strong> tags.

    Methods
    -------
    populate:
        Add initial information to a comic category.
    """

    __slots__ = [
        "about",
        "author",
        "authors",
        "banner",
        "bannerw",
        "bannerh",
        "category",
        "category_escaped",
        "category_theme",
        "chapters",
        "chapters_dicts",
        "chapters_file",
        "chapters_list",
        "chars_file",
        "chars_fn",
        "clicense",
        "conf_c",
        "copyright_statement",
        "desc",
        "email",
        "fbd_link",
        "fbp_link",
        "first_page",
        "header",
        "headerh",
        "headerw",
        "known_pages",
        "known_pages_raw",
        "known_pages_real",
        "language",
        "last_page",
        "lbd_link",
        "lbp_link",
        "license",
        "license_uri",
        "mode",
        "pbd",
        "pbp",
        "publicdomain",
        "slug",
        "status",
        "statuss",
    ]

    def __init__(self, category: str, publicdomain: bool = False):
        """
        The constructor for the Comic class.

        Initialized with just the name of the comic.

        Parameters
        ----------
        category : str
            The name of the comic.
        publicdomain : bool
            Whether the comic is public domain or not. Necessary for
            some copyright-related stuff.
        """
        self.category = category
        self.category_escaped = html.escape(category)
        self.publicdomain = publicdomain

    def populate(self, site, comics_base):
        """
        Add initial information to a comic category.

        Parameters
        ----------
        site : Site
            The root comic :class:`Site`.
        comics_base : list of Strip
            Strips known to Springheel.
        """
        self.known_pages = [
            page.page_padded for page in comics_base if page.category == self.category
        ]
        self.known_pages_raw = [
            page.page for page in comics_base if page.category == self.category
        ]
        if set([self.known_pages_raw.count(item) for item in self.known_pages_raw]) != {
            1
        }:
            dupes = set(
                [
                    item
                    for item in self.known_pages_raw
                    if self.known_pages_raw.count(item) > 1
                ]
            )
            logging.warning(
                _("Duplicate page numbers found in category {cat}: {dupes}").format(
                    cat=self.category, dupes=", ".join(dupes)
                )
            )
        self.known_pages_real = [
            page.page_real_num for page in comics_base if page.category == self.category
        ]
        self.known_pages.sort(key=springheel.mixNum)
        self.known_pages_raw.sort()
        self.known_pages_real.sort(key=springheel.realMixNum)
        self.last_page, self.first_page = springheel.checkExtremes(self.known_pages)
        raw_author = self.conf_c["author"]
        self.author = html.escape(raw_author)
        author_dividers = {"&", "/", "+"}
        if any([div in raw_author for div in author_dividers]):
            raw_authors_split = springheel.splitseps.splitAtSeparators(
                raw_author, author_dividers
            )
            for a in raw_authors_split:
                cleaned_a = html.escape(a).strip()
                if cleaned_a not in site.authors:
                    site.authors.append(cleaned_a)
                if cleaned_a not in self.authors:
                    self.authors.append(cleaned_a)
        else:
            if self.author not in site.authors:
                site.authors.append(self.author)
            if self.author not in self.authors:
                self.authors.append(self.author)
        for key in {
            "email",
            "header",
            "banner",
            "language",
            "mode",
            "status",
            "license_uri",
            "about",
        }:
            try:
                setattr(self, key, self.conf_c[key])
            except KeyError:
                logging.debug(
                    _("No value for {key} in the config file for {cat}.").format(
                        key=key, cat=self.category
                    )
                )
                continue
        self.clicense = self.conf_c["license"]
        try:
            if (
                self.conf_c["license"].lower() == "public domain"
                or "publicdomain" in self.conf_c["license_uri"]
            ):
                self.publicdomain = True
        except KeyError:
            self.publicdomain = False
        try:
            # Just to be absolutely sure the slug really is safe.
            self.slug = springheel.slugurl.slugify_url(self.conf_c["slug"])
        except KeyError:
            self.slug = springheel.slugurl.slugify_url(self.category)
        if self.conf_c["chapters"]:
            self.chapters = True
            self.chapters_file = os.path.join(site.i_path, self.conf_c["chapters"])
        else:
            self.chapters = False
        self.desc = html.escape(self.conf_c["desc"])


class Chapter:
    """
    A collection of related :class:`Strip` items.

    More specific than :class:`Comic`. Initialized with the chapter
    number and optionally the chapter title.

    Parameters
    ----------
    category : str
        The name of the :class:`Comic` this chapter belongs to.
    chap_number : int
        The number of the chapter.
    chap_title : str, optional
        The title of the chapter.

    Attributes
    ----------
    authors : set
        All authors associated with the chapter. Used for making
        copyright statements in chapter view, etc.
    category : str
        The name of the :class:`Comic` this chapter belongs to.
    ch_outfn : str
        The output filename for the chapter-view page. Formatted
        like "{series_slug}_c{padded_chap_number}.html".
    chap_number : int
        The number of the chapter.
    chap_title : str, optional
        The title of the chapter.
    chap_title_escaped : str, optional
        HTML-safe chap_title, with entity characters escaped.
    pages : list of Strip
        All Strips in the chapter.
    slug : str
        Slug used for the chapter in the archive table of contents.
    years : set
        Initial publication years of comics in this chapter.

    See Also
    --------
    Strip : The elements that `pages` comprises.
    """

    def __init__(self, category: str, chap_number: int, chap_title=False):
        """
        Constructor for the Chapter class.

        Initialized with the chapter number and optionally
        the chapter title.

        Parameters
        ----------
        category : str
            The name of the :class:`Comic` this chapter belongs to.
        chap_number : int
            The number of the chapter.
        chap_title : str, optional
            The title of the chapter.
        """
        self.category = category
        self.chap_number = chap_number
        if chap_title:
            self.chap_title = chap_title
            self.chap_title_escaped = html.escape(chap_title)
        self.pages = []


class Arrow:
    """
    A navigation element to go to another page.

    Parameters
    ----------
    relation : str
        The relationship between the target page and the current
        one. Will be first, prev, next, or last.
    page : str
        The page number for the target page.

    Attributes
    ----------
    long : str
        The long link text for this arrow, like "Previous Page - 3".
        (Translated into the site language, of course.) Mostly used by
        assistive technology, to make it easier to tell where a link
        goes without looking at the rest of the page.
    lrel : str
        Link relation for this arrow. Either "prev" or "next", as
        "first" and "last" are not part of the spec.
    page : str
        The page number for the target page.
    relation : str
        The relationship between the target page and the current one.
        Will be first, prev, next, or last.
    short : str
        Short link text for this arrow. "First", "Previous", "Next", or
        "Last" in the site language. Appears beneath arrow images.
    strings : dict
        Various strings used by this arrow. "rel", corresponding to
        self.relation; "long" link text (visible to screen readers),
        and "short" link text (below image).
    """

    __slots__ = ["long", "lrel", "page", "relation", "short", "strings"]

    def __init__(self, relation: str, page: str):
        """
        The constructor for the Arrow class.

        Parameters
        ----------
        relation : str
            The relationship between the target page and the current
            one. Will be first, prev, next, or last.
        page : str
            The page number for the target page.
        """
        self.relation = relation
        self.page = page


class EXpage:
    """
    An extras page.

    Attributes
    ----------
    headings : list of str
        The page's navigational headings.
    content : str
        The generated HTML for the extras page.
    """

    __slots__ = ["headings", "content"]

    def __init__(self):
        """Constructor for the EXpage class."""
        self.headings = []
