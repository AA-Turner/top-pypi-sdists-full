#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##  Copyright 2017-2021 garrick. Some rights reserved.
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.

##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Springheel -- a static site generator for webcomics."""

name = "springheel"
author = "gargargarrick"
__version__ = "7.0.2"

import springheel.classes
import springheel.genchars
import springheel.generatearchive
import springheel.generatenav
import springheel.genmultipleindex
import springheel.gentrans
import springheel.genrss
import springheel.gentopnav
import springheel.gettemplatenames
import springheel.parsemeta
import springheel.parsetranscript
import springheel.springheelinit
import springheel.genextra
import springheel.socialbuttons
import springheel.genmultilang
import springheel.genjsonfeed
import springheel.genchbook
import springheel.splitseps
import springheel.metatag
import springheel.genabout
import springheel.copystuff
import springheel.slugurl
import springheel.wraptag
import springheel.acopy
from springheel.classes import Site, Config, Tag, Strip, Comic, Chapter, Arrow, EXpage
import springheel.addimg
import springheel.renameimgs
import springheel.webtoon
import springheel.genstatline
from springheel.tl import gettext as _

import shutil, logging, textwrap, asyncio, glob, hashlib
import configparser, os, datetime, sys
from operator import itemgetter
import html, json
from tqdm.asyncio import tqdm
from typing import Union, Tuple, List
from PIL import Image


def getTags(
    meta: dict, all_tags: List[Tag], translated_strings: dict
) -> Tuple[str, List[Tag], List[Tag]]:
    """
    Get and process a strip's tags.

    Notes
    -----

    Retrieve a strip's used tags, add new ones to the list of all
    known tags, and create a line that indicates the strip's tags with
    hyperlinks to those tags' indices.

    Parameters
    ----------
    meta : dict
        The strips metadata.
    all_tags : list of Tag
        The "list of all known tags" to which tags should be added.
    translated_strings : dict
        The translation file contents for this site.

    Returns
    -------
    tagline : str
        HTML links to the index pages of the strip's tags. Separated by
        commas.
    this_strips_tags : list of Tag
        The Tags used by this strip.
    """
    tags_raw = meta["tags"]
    # Tags may be a list already in JSON mode
    try:
        tags_sep = tags_raw.split(", ")
    except AttributeError:
        tags_sep = tags_raw
    this_strips_tags = []
    this_strips_wraps = []

    for tag in tags_sep:
        tago = classes.Tag(name=tag)
        tago.gen_links(translated_strings)
        if tag not in set(n.name for n in all_tags):
            all_tags.append(tago)
        this_strips_tags.append(tago)
        this_strips_wraps.append(tago.link)
    tagline = ", ".join(this_strips_wraps)
    return (tagline, this_strips_tags)


def getComics(i_path: str, m_ext: str, t_ext: str) -> Tuple[List[Strip], dict]:
    """
    Find comic strips in the input folder.

    Parameters
    ----------
    i_path : str
        The path to the input directory. Should be "./input".
    m_ext : str
        File extension for metadata files. Will be either ".meta" or
        ".meta.json".
    t_ext : str
        File extension for transcript files. Will be either
        ".transcript" or ".transcript.json".

    Returns
    -------
    comics : list of springheel.Strip
        All comics detected in the current mode.
    image_dimensions : dict
        A dictionary mapping image filenames to (width, height) in
        pixels.
    """

    logmesg = _("Finding images...")
    logging.info(logmesg)

    # Get lists of images, meta files, and transcripts.
    image_extensions = {"*.png", "*.gif", "*.jpg", "*.jpeg", "*.svg", "*.webp"}
    image_glob_patterns = [os.path.join(i_path, item) for item in image_extensions]
    images = [
        iset
        for results in [glob.glob(pat) for pat in image_glob_patterns]
        for iset in results
    ]
    if not images:
        logging.error(_("No images found in input."))
        return False
    meta_glob = "".join(["*", ".", m_ext])
    transcript_glob = "".join(["*", ".", t_ext])
    meta_paths = glob.glob(os.path.join(i_path, meta_glob))
    trans_paths = glob.glob(os.path.join(i_path, transcript_glob))
    image_dimensions = dict()

    comics = []
    # Find images that have matching metadata files.
    for i in tqdm(images):
        noext, ext = os.path.splitext(i)
        transcr = "".join([noext, ".", t_ext])
        meta = "".join([noext, ".", m_ext])
        basename = os.path.basename(i)
        retainDimensions(basename, i_path, image_dimensions)
        logmesg = _("{basename} dimensions: {dimensions}").format(
            basename=basename, dimensions=" x ".join(image_dimensions[basename])
        )
        logging.debug(logmesg)
        if transcr in trans_paths and meta in meta_paths:
            logmesg = _("Metadata and transcript found for {image}.").format(
                image=basename
            )
            logging.debug(logmesg)
            comic = classes.Strip(imagef=i, transf=transcr, metaf=meta)
            comics.append(comic)
        elif meta in meta_paths and transcr not in trans_paths:
            logmesg = _(
                "Metadata found, but no transcript for {image}. Please create {transcr}"
            ).format(image=basename, transcr=transcr)
            logging.debug(logmesg)
            comic = classes.Strip(imagef=i, transf=False, metaf=meta)
            comics.append(comic)
        elif transcr in trans_paths and meta not in meta_paths:
            logmesg = _(
                "Transcript found, but no metadata for {image}. I can't build the page without metadata. Please create {meta}"
            ).format(image=basename, meta=meta)
            logging.error(logmesg)
            return False
        else:
            logmesg = _(
                "{image} doesn't seem to be a comic, as it is missing a transcript and metadata."
            ).format(image=basename)
            logging.debug(logmesg)
    if not comics:
        logmesg = _(
            "The comics list is empty. Please add some comics and then try to build again."
        )
        logging.error(logmesg)
        return False

    return comics, image_dimensions


def getChapters(chapter_file: str) -> List[dict]:
    """
    Get numbers and titles from a chapter file.

    Parameters
    ----------
    chapter_file : str
        The path to the chapter file to read.

    Returns
    -------
    list of dict
        The chapter data extracted from the file. Comprises dicts with
        "num" for the chapter number (an int), and optionally "title":
        chapter title (a str).
    """
    with open(chapter_file, "r", encoding="utf-8") as f:
        chapter_raws = f.read().splitlines()
    chapters = []
    for line in chapter_raws:
        if line:
            split_line = line.split(" = ", 1)
            try:
                d = {"num": int(split_line[0]), "title": split_line[1]}
            except IndexError:
                d = {"num": int(split_line[0])}
            chapters.append(d)
    return chapters


def checkExtremes(sorted_ints: List[int]) -> Tuple[int, int]:
    """
    Find the highest and lowest values in a sorted list of integers.

    Notes
    -----
    Used instead of min(l), max(l) because e.g. page number lists may
    contain various different types. This simply returns the first and
    last values in a list that has already been sorted, under the
    assumption that what I've already done to sort the list is enough.

    Parameters
    ----------
    sorted_ints : list of int
        A sorted list of integers.

    Returns
    -------
    highest : int
        The highest value in the list.
    lowest : int
        The lowest value in the list.
    """
    highest = sorted_ints[-1]
    lowest = sorted_ints[0]
    return (highest, lowest)


def makeFilename(series_slug: str, page: str) -> str:
    """
    Combine a series slug and page number into an HTML filename.

    Parameters
    ----------
    series_slug : str
        The series slug to use.
    page : str
        The page number. Expected to be zero-padded, etc., already.

    Returns
    -------
    str
        The HTML filename.
    """
    # Pattern: series_slug_page.html
    file_name_components = [series_slug, page]
    file_name = "".join(["_".join(file_name_components), ".html"])
    return file_name


def mixNum(num: List[str]) -> Tuple[int, str, str]:
    """
    Generate a sort key to use for lists of page numbers.

    Parameters
    ----------
    num : list of str
        The page number to use.

    Returns
    -------
    tuple of 0, str, empty str
        The sort key.
    """
    ele = str(num)
    return (0, ele, "")


def realMixNum(num: Union[int, float, tuple]) -> Tuple[int, Union[int, float], str]:
    """
    Generate a sort key to use for lists of int/float page numbers.

    Parameters
    ----------
    num : int, float, or tuple
        The page number(s) to use.

    Returns
    -------
    tuple of int, int or float, str
        The sort key, comprising 0, the lowest value present in the
        num parameter (which will be simply the value itself if it is a
        float or int), and an empty string.
    """
    if type(num) == tuple:
        ele = min(num)
    else:
        ele = num
    return (0, ele, "")


def padNum(
    page: str, zero_padding: Union[int, bool]
) -> Tuple[Union[int, float, tuple], str]:
    """
    Pad page number(s) with zeroes, as desired.

    Parameters
    ----------
    page : str
        The page number or numbers to pad. Will still work even with
        page ranges or fractional pages.
    zero_padding : int or False
        Whether to pad the page number with zeroes, and if so, by how much.

    Raises
    ------
    UnboundLocalError :
        If the page number is not convertible to any usable format.

    Returns
    -------
    page_real_num : int, float, or tuple
        The "real" page number, in the sense that you can do math with
        it. May be an integer, a float, or a tuple containing either.
    page_padded : str
        The page number(s) padded with zeroes to the desired length.
    """
    try:
        page_real_num = int(page)
        if zero_padding:
            page_padded = "{page:0{zero_padding}}".format(
                page=page_real_num, zero_padding=zero_padding
            )
        else:
            page_padded = page
    except ValueError:
        double_seps = ["-", "–"]
        page = page.replace(" ", "")
        page_separator = [item for item in double_seps if item in page]
        if len(page_separator) > 0:
            page_separator = page_separator[0]
            each_page = page.split(page_separator, 1)
            rpages = []
            fpages = []
            for p in each_page:
                # Fractional double page!
                if "." in p:
                    page_f = float(p)
                    rpages.append(page_f)
                    if zero_padding:
                        formatted = fracPage(p, zero_padding)
                    else:
                        formatted = p
                    fpages.append(formatted)
                else:
                    page_int = int(p)
                    rpages.append(page_int)
                    if zero_padding:
                        formatted = "{page:0{zero_padding}}".format(
                            page=page_int, zero_padding=zero_padding
                        )
                    else:
                        formatted = p
                    fpages.append(formatted)
            page_real_num = tuple(rpages)
            page_padded = page_separator.join(fpages)
        # Fractional page
        elif "." in page:
            page_real_num = float(page)
            page_padded = fracPage(page_real_num, zero_padding)
    try:
        return (page_real_num, page_padded)
    except UnboundLocalError:
        logmesg = _(
            'Unable to convert page number(s) "{page}" to a usable format.'
        ).format(page=page)
        logging.error(logmesg)
        return False, False


def fracPage(page: float, zero_padding: Union[int, bool]) -> str:
    """
    Pad the whole part of a decimal page number with zeroes.

    Parameters
    ----------
    page : float
        A fractional page number (e.g. 3.5).
    zero_padding : int or False
        The desired amount of zero padding according to site settings.

    Returns
    -------
    str
        The padded number.
    """
    # This seems to be the safest way to work with floats for our
    # purposes (without rounding errors).
    page = str(page)
    split = page.split(".", 1)
    page_int = int(split[0])
    formatted = "{page_int:0{zero_padding}}.{split}".format(
        page_int=page_int, zero_padding=zero_padding, split=split[1]
    )
    return formatted


def strBool(str_to_check: str) -> bool:
    """
    Convert a string "True"/"False" to boolean without ast.

    Parameters
    ----------
    str_to_check : str
        The string to check. Expected to be either "True" or "False".

    Returns
    -------
    bool
        Whether the string is not "False".
    """
    return str_to_check != "False"


def getDimensions(img_path: str) -> Tuple[str, str]:
    """
    Get the pixel dimensions of an image file.

    Parameters
    ----------
    img_path : str
        The full path to the image.

    Returns
    -------
    width : str
        The width of the image.
    height : str
        The height of the image.
    """
    with Image.open(img_path) as im:
        width, height = im.size
    return str(width), str(height)


def retainDimensions(img_fn: str, i_path: str, images: dict) -> None:
    """
    Save image dimensions so they don't need to be recalculated.

    Parameters
    ----------
    img_fn : str
        The image filename to check.
    i_path : str
        The path to the input directory.
    images : dict
        A dictionary mapping image filenames to (width, height) in
        pixels.
    """
    try:
        w, h = images[img_fn]
        return images
    except KeyError:
        width, height = getDimensions(os.path.join(i_path, img_fn))
        images[img_fn] = (width, height)


async def imageChecksum(img_path: str) -> str:
    """
    Get the SHA-256 checksum for an image file.

    Parameters
    ----------
    img_path : str
        The path to the image.

    Returns
    -------
    str
        The checksum.
    """
    with open(img_path, "rb") as fin:
        imgbytes = fin.read()
    return hashlib.sha256(imgbytes).hexdigest()


async def build():
    """
    Generate a Springheel site.
    """
    tasks = []
    copyfile = springheel.acopy.wrap(shutil.copyfile)
    site = classes.Site()
    sep = os.linesep
    falses = {
        False,
        None,
        "False",
        "None",
        "Disable",
        "Null",
        "false",
        "none",
        "disable",
        "null",
    }
    config = classes.Config("conf.ini")
    site.config = config
    image_rename_pattern = site.config.image_rename_pattern
    starttime = datetime.datetime.now().timestamp()

    site.jsonpoints = {
        "generated_on": starttime,
        "springheel_version": __version__,
        **config.dict,
        "archive_page": "".join([site.config.base_url, "archive.html"]),
        "categories": [],
    }

    # Initialize log to avoid confusion
    logfile = os.path.join(".", "springheel.log")
    pil_logger = logging.getLogger("PIL")
    pil_logger.setLevel(logging.ERROR)
    try:
        logging_level = sys.argv[1] == "--logging"
        logging.basicConfig(
            handlers=[logging.FileHandler(logfile, "w", "utf-8")],
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)-8s %(message)s",
        )
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(levelname)-8s %(asctime)s.%(msecs)03d: %(message)s", datefmt="%H:%M:%S"
        )
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger("").addHandler(console)
    except IndexError:
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)-8s %(asctime)s.%(msecs)03d: %(message)s",
            datefmt="%H:%M:%S",
        )
    logging.debug(_("Starting Springheel build"))
    (
        c_path,
        o_path,
        pages_path,
        assets_path,
        arrows_path,
        socialbuttons_path,
    ) = springheelinit.makeOutput()
    i_path = os.path.join(c_path, "input")
    site.c_path = c_path
    site.i_path = i_path
    site.o_path = o_path
    site.config.base_url = "/".join(i.strip("/") for i in [site.config.base_url, ""])

    try:
        zero_padding = site.config.zero_padding
    except AttributeError:
        zero_padding = False
        logmesg = _(
            "There is no config value for {field}. Please update your conf.ini."
        )
        logging.warning(logmesg.format(field="zero_padding"))
    if zero_padding:
        zero_padding = int(zero_padding)
    try:
        multilang = site.config.multilang
    except AttributeError:
        multilang = False
    try:
        json_mode = site.config.json_mode
    except AttributeError:
        json_mode = False
        logging.warning(logmesgformat(field="json_mode"))
    try:
        gen_about = site.config.about
    except AttributeError:
        gen_about = False
        logging.warning(logmesg.format(field="about"))

    # Get some config variables

    (
        c_path,
        o_path,
        pages_path,
        assets_path,
        arrows_path,
        socialbuttons_path,
    ) = springheel.springheelinit.makeOutput()

    i_path = os.path.join(c_path, "input")
    site_theme_path = os.path.join(c_path, "themes", site.config.site_style)
    new_site_theme_path = os.path.join(o_path, assets_path)
    print_ipath = os.path.join(c_path, "themes", "print.css")

    old_buttons_path = os.path.join(c_path, "socialbuttons")

    old_header_path = os.path.join(i_path, site.config.header_filename)
    new_header_path = os.path.join(o_path, site.config.header_filename)

    html_filenames = []
    c_year = datetime.datetime.now().year
    if json_mode:
        m_ext = "meta.json"
        t_ext = "transcript.json"
    else:
        m_ext = "meta"
        t_ext = "transcript"
    # Get a list of dictionaries that map image files to metadata
    try:
        comics_base, site.images = getComics(i_path, m_ext, t_ext)
    except TypeError:
        return False
    if not comics_base:
        return False

    # Get template paths
    (
        base_t,
        chars_t,
        archive_t,
        index_t,
        extra_t,
        chapter_t,
        strings_path,
    ) = gettemplatenames.getTemplateNames()

    all_pages_raw = set()
    all_pages_real = set()
    all_page_nums = set()
    site.author = site.config.site_author
    site.authors = []
    themes = {site.config.site_style}
    # Select the right template for the specific site type we have
    if site.config.site_type == "single":
        single = True
    else:
        single = False
    site.single = single

    # Get translation strings, too.
    translated_strings = gentrans.generateTranslations(
        site.config.language, strings_path
    )
    if not translated_strings:
        logmesg = _(
            "Unable to load translation strings! The translation file strings.json is missing or invalid. Please repair it and try again."
        )
        logging.error(logmesg)
        return False
    language_names = translated_strings["language_names"]
    icons = "".join(socialbuttons.getButtons(site, translated_strings)[1])
    if multilang:
        other_langs = springheel.genmultilang.genMultiLang(multilang, language_names)
        icons = " ".join([icons, other_langs])
    logmesg = _("Loading translation strings for {lang}...").format(
        lang=site.config.language
    )
    logging.debug(logmesg)

    # Copy assets from the Springheel installation directory.
    existing_files = glob.glob(f"{o_path}/*")
    tasks.append(
        springheel.copystuff.copyTheme(
            site_theme_path, new_site_theme_path, print_ipath
        )
    )
    tasks.append(
        springheel.copystuff.copyButtons(
            site, old_buttons_path, socialbuttons_path, translated_strings
        )
    )
    file_exists_s = _(
        "Output file {outf} requested by {var} already exists; not adding to the copying queue, so it won't be overwritten."
    )
    if new_header_path not in existing_files:
        tasks.append(springheel.copystuff.copyHeader(old_header_path, new_header_path))
        existing_files.append(new_header_path)
    else:
        logging.debug(
            file_exists_s.format(
                outf=os.path.relpath(new_header_path), var="header_filename"
            )
        )

    base_template_name = base_t
    base_template_path = os.path.join(c_path, base_template_name)

    with open(base_template_path) as f:
        base_template = f.read()

    # Get basic info first.
    logmesg = _("Initializing strips...")
    logging.info(logmesg)
    configs = []
    for strip in tqdm(comics_base):
        file_name = os.path.join(i_path, strip.metaf)
        meta, commentary, raw_comments = parsemeta.parseMetadata(
            file_name, translated_strings, json_mode
        )
        strip.populate(meta, commentary, raw_comments, configs, site)
        all_pages_raw.add(strip.page)
        all_pages_real.add(strip.page_real_num)
        all_page_nums.add(strip.page_padded)
        retainDimensions(strip.imagef, i_path, site.images)

    cats_raw = set()
    cats_w_pages = []
    comics = []
    ccomics = []
    for strip in comics_base:
        cats_raw.add(strip.category)
    for cat in cats_raw:
        c = classes.Comic(cat)
        (conf,) = [item for item in configs if item["category"] == cat]
        c.conf_c = conf
        c.authors = []
        c.populate(site, comics_base)

        try:
            category_theme = conf["category_theme"]
            themes.add(category_theme)
        except KeyError:
            category_theme = False
        if category_theme != site.config.site_style:
            c.category_theme = category_theme

        old_banner_path = os.path.join(c_path, "input", c.banner)
        new_banner_path = os.path.join(o_path, c.banner)
        if new_banner_path not in existing_files:
            tasks.append(
                springheel.copystuff.copyHeader(old_banner_path, new_banner_path)
            )
            existing_files.append(new_banner_path)
        else:
            logging.debug(
                file_exists_s.format(
                    outf=os.path.relpath(new_banner_path), var=f"{c.category} banner"
                )
            )
        retainDimensions(c.header, i_path, site.images)
        retainDimensions(c.banner, i_path, site.images)
        c.headerw, c.headerh = site.images[c.header]
        c.bannerw, c.bannerh = site.images[c.banner]

        ccomics.append(c)
        if not [
            item for item in site.jsonpoints["categories"] if item["category"] == cat
        ]:
            site.jsonpoints["categories"].append(
                {s: getattr(c, s) for s in c.__slots__ if hasattr(c, s)}
            )
    ccomics.sort(key=lambda k: k.category)

    # Get other pages.
    characters_page = site.config.characters_page
    extras_page = site.config.extras_page
    store_page = site.config.store_page

    site.jsonpoints["characters_page"] = characters_page
    site.jsonpoints["extras_page"] = extras_page
    site.jsonpoints["store_page"] = store_page

    # why did I already use "top_nav" smh
    site_nav_raw = gentopnav.genTopNav(
        characters_page, extras_page, store_page, translated_strings, gen_about
    )
    top_site_nav = sep.join(site_nav_raw)

    cpages = []
    chapters_list = []
    all_tags = []
    years = set()
    if json_mode:
        transcr_file_ext = "JSON"
        meta_file_ext = "JSON"
    else:
        transcr_file_ext = "TXT"
        meta_file_ext = "YAML"

    logmesg = _("Processing comic pages...")
    logging.info(logmesg)
    nocomment_test = springheel.wraptag.wrapWithTag(
        translated_strings["no_comment"], "p"
    )
    for strip in tqdm(comics_base):
        commentary = strip.commentary
        if commentary == nocomment_test:
            comment_header = translated_strings["meta_s"]
            commentary = ""
        else:
            comment_header = translated_strings["caption_s"]
        try:
            transcript_file = os.path.join(i_path, strip.transf)
            transcript = parsetranscript.makeTranscript(transcript_file, json_mode)
            strip.transcript_c = transcript
        except TypeError:
            transcript = ""
            transcript_file = ""
            no_transcr = springheel.wraptag.wrapWithTag(
                translated_strings["no_transcript"], "p"
            )
            strip.transcript_c = no_transcr
        match = strip.get_matching(ccomics)

        strip.lang = strip.conf_c["language"]
        author_email = strip.conf_c["email"]
        mode = strip.conf_c["mode"]
        banner = match.banner
        header = match.header
        if characters_page and strip.conf_c["chars"]:
            match.chars_file = strip.conf_c["chars"]
        else:
            match.chars_file = False
        strip_id = match.known_pages.index(strip.page_padded)

        strip.title = html.escape(strip.metadata["title"])
        strip.populate_authors(site)
        strip.title_slug = strip.metadata["title_slug"]
        strip.series_slug = match.slug
        strip.slugs = [strip.title_slug, strip.series_slug]
        date = datetime.datetime.strptime(strip.metadata["date"], "%Y-%m-%d")
        year = date.year
        years.add(date.year)
        # If the strip isn't from the current year, create a year range
        # between its original publication and now.
        try:
            (year_range,) = {str(date.year), str(c_year)}
        except ValueError:
            year_range = "&ndash;".join([str(date.year), str(c_year)])
        width, height = site.images[strip.imagef]
        try:
            alt_text = html.escape(strip.metadata["alt"])
        except KeyError:
            alt_text = False
        try:
            strip.source = strip.metadata["source"]
        except KeyError:
            pass

        strip.mode = mode
        strip.height = height
        strip.width = width

        if match.chapters:
            site.jsonpoints.setdefault("chapter_info", dict())
            chapters_dicts = getChapters(match.chapters_file)
            match.chapters_dicts = chapters_dicts
            if match.category not in site.jsonpoints["chapter_info"].keys():
                site.jsonpoints["chapter_info"][match.category] = match.chapters_dicts
            if not hasattr(match, "chapters_list"):
                match.chapters_list = []
            for chapter in chapters_dicts:
                # Check if chapter exists already
                try:
                    (chap_check,) = [
                        item
                        for item in match.chapters_list
                        if item.chap_number == chapter["num"]
                    ]
                except ValueError:
                    try:
                        chap = classes.Chapter(
                            match.category, chapter["num"], chap_title=chapter["title"]
                        )
                    except KeyError:
                        chap = classes.Chapter(match.category, chapter["num"])
                    match.chapters_list.append(chap)
                    # Zero-pad if needed
                    try:
                        chap_padded = "{chap:0{zero_padding}}".format(
                            chap=chap.chap_number, zero_padding=zero_padding
                        )
                    except ValueError:
                        chap_padded = chap.chap_number
                    chap.ch_outfn = "{catslug}_c{padded_num}.html".format(
                        catslug=match.slug, padded_num=chap_padded
                    )
        else:
            match.chapters_list = []

        # Make hte license
        clicense = match.clicense

        if not hasattr(site, "license"):
            site.license = site.config.license
        if not hasattr(match, "license"):
            # Default
            license_c = site.license
            license_s = site.license
            # It's easiest to use raw HTML if it exists
            try:
                license_c = match.conf_c["license_html"]
                strip.copyright_statement = (
                    "<p>&copy; {year} {author}. {clicense}</p>".format(
                        year=year_range, author=strip.author, clicense=license_c
                    )
                )
            except KeyError:
                try:
                    license_uri = match.conf_c["license_uri"]
                    if match.publicdomain:
                        # Creative Commons Public Domain Waiver
                        ccpdw = translated_strings["ccpdw"]
                        license_c = ccpdw.format(
                            site_url=site.config.base_url,
                            author=" &amp; ".join(match.authors),
                            site_title=strip.category,
                            author_country=site.config.country,
                        )
                        license_s = ccpdw.format(
                            site_url=site.config.base_url,
                            author=strip.author,
                            site_title=strip.category,
                            author_country=site.config.country,
                        )
                        strip.copyright_statement = springheel.wraptag.wrapWithTag(
                            license_s, "p"
                        )
                    elif "creativecommons.org/licenses/by" in license_uri:
                        cc = translated_strings["cc"]
                        license_c = cc.format(
                            license_uri=license_uri,
                            clicense=clicense,
                            author=" &amp; ".join(match.authors),
                            category=strip.category,
                            base_url=site.config.base_url,
                        )
                        license_s = cc.format(
                            license_uri=license_uri,
                            clicense=clicense,
                            author=strip.author,
                            category=strip.category,
                            base_url=site.config.base_url,
                        )
                        strip.copyright_statement = (
                            "<p>&copy; {year} {author}. {clicense}</p>".format(
                                year=year_range, author=strip.author, clicense=license_s
                            )
                        )
                except KeyError:
                    license_c = clicense
                    license_s = clicense
                    strip.copyright_statement = (
                        "<p>&copy; {year} {author}. {clicense}</p>".format(
                            year=year_range, author=strip.author, clicense=license_s
                        )
                    )
            match.license = license_c
        else:
            license_c = match.license
            license_s = match.license
            strip.copyright_statement = (
                "<p>&copy; {year} {author}. {clicense}</p>".format(
                    year=year_range, author=strip.author, clicense=license_s
                )
            )
        strip.license = license_s

        img_path = os.path.join(i_path, strip.imagef)
        try:
            chapter = strip.metadata["chapter"]
        except KeyError:
            chapter = False
        strip.sha256 = await imageChecksum(img_path)

        last_page = match.last_page
        first_page = match.first_page

        final = True if strip.page_real_num == last_page else False
        first = True if strip.page_real_num == first_page else False

        strip.date = date
        date_format = translated_strings["date_format"]
        strip.date_s = datetime.datetime.strftime(date, "%Y-%m-%d")
        strip.date_fmt = datetime.datetime.strftime(
            date, translated_strings["strf_format"]
        ).format(y=date_format[0], m=date_format[1], d=date_format[2])
        strip.year = year
        strip.chapter = chapter if chapter else False
        if not alt_text:
            strip.alt_text = ""
            strip.figcaption = ""
        else:
            strip.alt_text = alt_text
            strip.figcaption = "<figcaption>{alt_text}</figcaption>".format(
                alt_text=alt_text
            )

        try:
            style = (
                match.category_theme if match.category_theme else site.config.site_style
            )
        except AttributeError:
            style = site.config.site_style

        # Get arrow sizes
        for direction in {"first", "prev", "next", "last"}:
            arrow_fn = f"{style}_{direction}.png"
            retainDimensions(arrow_fn, "arrows", site.images)
        navblock, linkrels = generatenav.navGen(
            site.config.navdirection,
            strip.page_padded,
            first_page,
            last_page,
            first,
            final,
            strip.series_slug,
            style,
            translated_strings,
            match.known_pages,
            match.known_pages_real,
            strip_id,
            images=site.images,
        )

        top_nav = springheel.wraptag.wrapWithComment(
            navblock.format(boxlocation="topbox"), "TOP NAVIGATION"
        )
        bottom_nav = springheel.wraptag.wrapWithComment(
            navblock.format(boxlocation="botbox"), "BOTTOM NAVIGATION"
        )

        h1_title = translated_strings["h1_s"].format(
            category=html.escape(strip.metadata["category"]),
            page=strip.metadata["page"],
            title=html.escape(strip.metadata["title"]),
        )
        header_title = h1_title
        strip.h1_title = h1_title
        strip.header_title = header_title

        try:
            tagsline, these_tags = getTags(strip.metadata, all_tags, translated_strings)
            strip.tags = these_tags
            for tag in strip.tags:
                (tag_match,) = [item for item in all_tags if item.name == tag.name]
                tag_match.strips.append(strip)
                tag_match.strips.sort(key=lambda x: (x.category, x.page_padded))
            strip.tline = "{tags_s}: {tags}{sep}".format(
                sep=translated_strings["statline_separator"],
                tags_s=translated_strings["tags_s"],
                tags=tagsline,
            )
        except KeyError:
            strip.tline = ""

        if all_tags:
            site.jsonpoints.setdefault("tags", [])
        for tag in all_tags:
            if not [
                item for item in site.jsonpoints["tags"] if item["name"] == tag.name
            ]:
                site.jsonpoints["tags"].append(
                    {"name": tag.name, "url": "".join([site.config.base_url, tag.rurl])}
                )

        if transcript:
            transcript_block = [
                '<section id="transcript"><h2>{transcript_s}</h2>'.format(
                    transcript_s=translated_strings["transcript_s"]
                )
            ]

            transcript_block.append(transcript)
            transcript_block.append("</section>")
            strip.transcript_block = transcript_block

            tb = os.linesep.join(transcript_block)
            strip.tb = tb
        else:
            transcript_block = []
            strip.transcript_block = []
            tb = ""
            strip.tb = ""

        statuses = {
            "in-progress": translated_strings["inprogress_s"],
            "complete": translated_strings["complete_s"],
            "hiatus": translated_strings["hiatus_s"],
        }

        try:
            status = statuses[match.status]
        except KeyError:
            status = _(
                "Status Not Found - Please add one of 'in-progress', 'complete', or 'hiatus' to this comic's .conf file!"
            )

        match.statuss = springheel.wraptag.wrapWithTag(status, "strong")
        logging.debug(
            _("Generating page for {page}...").format(
                page=os.path.basename(strip.metaf)
            )
        )
        #######################################################################
        # Generate the actual page!
        #######################################################################

        html_filename = makeFilename(strip.series_slug, strip.page_padded)
        strip.html_filename = html_filename
        strip.slug = "_".join([strip.series_slug, strip.page_padded])
        html_filenames.append(html_filename)
        out_file = os.path.join(o_path, html_filename)
        page_url = "".join([site.config.base_url, html_filename])
        strip.page_url = page_url

        (
            renamed_fn,
            renamed_path,
            new_meta,
            new_transcr,
        ) = springheel.renameimgs.renameImages(
            site, strip, pages_path, m_ext, t_ext, image_rename_pattern
        )
        tasks.append(copyfile(img_path, os.path.join(pages_path, renamed_fn)))
        tasks.append(
            copyfile(
                os.path.join(i_path, strip.metaf), os.path.join(pages_path, new_meta)
            )
        )
        if strip.transf:
            tasks.append(
                copyfile(
                    os.path.join(i_path, transcript_file),
                    os.path.join(pages_path, new_transcr),
                )
            )
            # Link to metadata and transcript file in statline
            meta_trans = """<a href="{metadatafile}">{metadata_s}</a>{statline_separator}<a href="{transcriptfile}">{transcript_s}</a>""".format(
                statline_separator=translated_strings["statline_separator"],
                metadatafile="".join(["pages/", new_meta]),
                transcriptfile="".join(["pages/", new_transcr]),
                metadata_s=translated_strings["meta_link_s"].format(
                    file_ext=meta_file_ext
                ),
                transcript_s=translated_strings["transcript_link_s"].format(
                    file_ext=transcr_file_ext
                ),
            )
        else:
            # Leave off transcript file if we don't need it
            meta_trans = """<a href="{metadatafile}">{metadata_s}</a>""".format(
                statline_separator=translated_strings["statline_separator"],
                metadatafile="".join(["pages/", new_meta]),
                metadata_s=translated_strings["meta_link_s"].format(
                    file_ext=meta_file_ext
                ),
            )
        strip.permalink = (
            """<a href="{url}" class="permalink">{permalink_s}</a></p>""".format(
                url=page_url, permalink_s=translated_strings["permalink_s"]
            )
        )
        strip.img = renamed_fn
        strip.new_meta = new_meta
        strip.new_transcr = new_transcr

        img_url = "".join([site.config.base_url, "pages/", strip.img])
        if strip.alt_text:
            meta_comment = strip.alt_text
        else:
            try:
                meta_comment = strip.raw_comments[0]
            except IndexError:
                meta_comment = match.description
        meta_tags = metatag.genMetaTags(
            textwrap.shorten(strip.h1_title, 90),
            strip.page_url,
            textwrap.shorten(meta_comment, 200),
            img_url,
        )
        meta_tags_ready = "\n".join(meta_tags)

        statline = springheel.genstatline.genStatline(
            strip,
            match.chapters,
            match.chapters_list,
            translated_strings,
            strip.tline,
            meta_trans,
        )
        strip.statline = statline
        strip.stat_noperma = "".join([statline, meta_trans, "</p>"])

        jsoncat = [
            item
            for item in site.jsonpoints["categories"]
            if item["category"] == strip.category
        ][0]
        strips = jsoncat.setdefault("strips", [])
        forbiddened = {
            "page_real_num",
            "conf_c",
            "metadata",
            "transcript_block",
            "tb",
            "date",
            "date_s",
            "year",
            "tags",
        }
        dictified_strip = {
            s: getattr(strip, s)
            for s in strip.__slots__
            if hasattr(strip, s) and s not in forbiddened
        }
        dictified_strip["url"] = page_url
        dictified_strip["date"] = strip.date_s
        dictified_strip["year"] = str(strip.year)

        # Clear filenames for privacy reasons
        del dictified_strip["imagef"]
        del dictified_strip["metaf"]
        del dictified_strip["transf"]
        try:
            dictified_strip["tags"] = [tag.name for tag in strip.tags if tag.name]
            test_tag = dictified_strip["tags"][0]
        except AttributeError:
            pass
        except IndexError:
            try:
                del dictified_strip["tags"]
            except KeyError:
                pass
        jsoncat["strips"].append(dictified_strip)
        try:
            del jsoncat["chapters_file"]
        except KeyError:
            pass

        skiplink = "#comic"

        # Webtoon mode
        if all(pref == "webtoon" for pref in {mode, strip.metadata["mode"]}):
            try:
                if json_mode:
                    pieces = strip.metadata["pieces"]
                else:
                    pieces = strip.metadata["pieces"].split(", ")
            except KeyError:
                logging.warning(
                    _(
                        "{fn} is marked as a webtoon, but is missing a pieces field."
                    ).format(fn=strip.metaf)
                )
                img = """<img src="{img_path}" alt="{page_alt}" width="{width}" height="{height}">""".format(
                    img_path="".join(["pages/", renamed_fn]),
                    height=height,
                    width=width,
                    page_alt=translated_strings["page_alt_s"],
                )
                modeclass = ""
                strip.pieces = img
                continue
            pieces_d = []
            for pid, piece in enumerate(pieces):
                prn_fn, prn_path = springheel.renameimgs.renamePieces(
                    site,
                    strip,
                    pid,
                    piece,
                    pages_path,
                    image_rename_pattern,
                    site.images,
                )
                pieces_d.append(
                    {
                        "img": piece,
                        "pid": pid + 1,
                        "prn_fn": prn_fn,
                        "prn_path": prn_path,
                    }
                )
                tasks.append(
                    copyfile(
                        os.path.join(i_path, piece), os.path.join(pages_path, prn_fn)
                    )
                )
            piece_imgs = springheel.webtoon.webtoon(
                strip, pieces_d, site.images, translated_strings
            )
            img = "".join(piece_imgs)
            modeclass = " webtoon"
        else:
            img = """<img src="{img_path}" alt="{page_alt}" width="{width}" height="{height}">""".format(
                img_path="".join(["pages/", renamed_fn]),
                height=height,
                width=width,
                page_alt=translated_strings["page_alt_s"],
            )
            modeclass = ""
        strip.pieces = img

        n_string = base_template.format(
            lang=strip.lang,
            site_style=style,
            header_title=header_title,
            meta_tags=meta_tags_ready,
            linkrels=linkrels,
            header=header,
            headerw=match.headerw,
            headerh=match.headerh,
            category=html.escape(strip.category),
            top_site_nav=top_site_nav,
            h1_title=h1_title,
            alt_text=strip.figcaption,
            top_nav=top_nav,
            img=img,
            modeclass=modeclass,
            bottom_nav=bottom_nav,
            commentary=commentary,
            statline=strip.statline,
            tb=tb,
            year=year,
            author=author,
            icons=icons,
            home_s=translated_strings["home_s"],
            archive_s=translated_strings["archive_s"],
            caption_s=comment_header,
            copyright_statement=strip.copyright_statement,
            stylesheet_name_s=translated_strings["stylesheet_name_s"],
            skiplink=skiplink,
            skip_s=translated_strings["skip_s"],
            page_s=translated_strings["page_s"],
            meta_s=translated_strings["meta_s"],
            generator_s=translated_strings["generator_s"].format(
                version=springheel.__version__
            ),
            goarchive_s=translated_strings["goarchive_s"],
            url=page_url,
        )

        with open(out_file, "w+", encoding="utf-8") as fout:
            fout.write(n_string)
        modified_time = datetime.datetime.strftime(
            datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),
            "%Y-%m-%dT%H:%M:%S.%fZ",
        )
        sitemap_loc = {"loc": page_url, "lastmod": modified_time}
        site.sitemap.append(sitemap_loc)
        logging.debug(_("Page generated."))
        #######################################################################

        strip.clicense = clicense
        strip.file_name = renamed_fn
        if match.chapters not in falses:
            strip.chapter = chapter
        header = site.config.header_filename
    site_header_w, site_header_h = getDimensions(
        os.path.join(i_path, site.config.header_filename)
    )
    for jsoncat in site.jsonpoints["categories"]:
        jsoncat["authors"] = sorted(
            list({author for strip in jsoncat["strips"] for author in strip["authors"]})
        )

    # Comic-wide copyright statement
    for comic in ccomics:
        # Overwrite
        clicense = comic.clicense
        # It's easiest to use raw HTML if it exists
        try:
            license_c = comic.license_html
        except AttributeError:
            try:
                if len(comic.authors) > 1:
                    authors = " &amp; ".join(comic.authors)
                else:
                    authors = comic.author
                if comic.publicdomain:
                    # Creative Commons Public Domain Waiver
                    ccpdw = translated_strings["ccpdw"]
                    license_c = ccpdw.format(
                        site_url=site.config.base_url,
                        author=authors,
                        site_title=comic.category,
                        author_country=site.config.country,
                    )
                elif "creativecommons.org/licenses/by" in comic.license_uri:
                    cc = translated_strings["cc"]
                    license_c = cc.format(
                        license_uri=comic.license_uri,
                        clicense=comic.clicense,
                        author=authors,
                        category=comic.category,
                        base_url=site.config.base_url,
                    )
            except AttributeError:
                license_c = comic.clicense
                license_s = comic.clicense
        comic.copyright_statement = license_c
        jsoncat = [
            item
            for item in site.jsonpoints["categories"]
            if item["category"] == comic.category
        ][0]
        jsoncat["copyright_statement"] = comic.copyright_statement

    # Sitewide copyright statement
    years = list(years)
    years.sort()
    if not hasattr(site, "copyright_statement"):
        if set([item.publicdomain for item in ccomics]) == {True}:
            copyright_statement = springheel.wraptag.wrapWithTag(site.license, "p")
        else:
            first_year = min(years)
            if first_year == c_year:
                copyright_year = first_year
            else:
                copyright_year = "{fy}&ndash;{ly}".format(fy=first_year, ly=c_year)
            # All site authors should be listed in site.author
            authors = site.author
            copyright_statement = "<p>&copy; {year} {author}. {clicense}</p>".format(
                year=copyright_year,
                author=authors,
                clicense=site.license,
            )
        site.copyright_statement = copyright_statement
    site.jsonpoints["copyright_statement"] = site.copyright_statement

    for a_theme in themes:
        tasks.append(
            springheel.copystuff.copyArrows(
                a_theme, os.path.join(c_path, "arrows"), os.path.join(o_path, "arrows")
            )
        )
    # If there are multiple series that have separate themes,
    # time 2 concatenate the stylesheets.
    if len(themes) > 1:
        logmesg = _("Categories have separate themes. Concatenating stylesheets...")
        logging.debug(logmesg)
        tasks.append(
            springheel.copystuff.copyMultiThemes(themes, c_path, o_path, assets_path)
        )

    # Generate archives
    logmesg = _("Generating archives...")
    logging.info(logmesg)

    # Some things are done by page and some things are done by year.

    cpages_by_page = sorted(comics_base, key=lambda x: x.page_padded)
    cpages_by_date = sorted(comics_base, key=lambda x: x.date)

    archives_r = []

    # Get all pages for each series.
    for cat in cats_raw:
        cur_cat = []
        match = [item for item in ccomics if item.category == cat][0]
        for page in cpages_by_page:
            if page.category == cat:
                cur_cat.append(page)
        match.pbp = cur_cat

        cur_cat = []
        for page in cpages_by_date:
            if page.category == cat:
                cur_cat.append(page)
        match.pbd = cur_cat

        allp = len(match.pbd) - 1

        match.fbp_link = match.pbp[0].html_filename
        match.lbp_link = match.pbp[allp].html_filename

        match.fbd_link = match.pbd[0].html_filename
        match.lbd_link = match.pbd[allp].html_filename

    sdate_comics = cpages_by_date
    spage_comics = cpages_by_page

    ex_by_page = []
    ex_by_date = []
    for comic in ccomics:

        first_bypage = comic.fbp_link
        last_bypage = comic.lbp_link

        d = {
            "category": comic.category,
            "first_bypage": first_bypage,
            "last_bypage": last_bypage,
        }
        ex_by_page.append(d)

    for comic in ccomics:

        first_bydate = comic.fbd_link
        last_bydate = comic.lbd_link

        d = {
            "category": comic.category,
            "first_bydate": first_bydate,
            "last_bydate": last_bydate,
        }
        ex_by_date.append(d)

    archive_d_secs = []
    site.jsonpoints["site_authors"] = site.authors

    logmesg = _("Got first and last strips for each series.")
    logging.debug(logmesg)

    logmesg = _("Generating archive pages...")
    logging.debug(logmesg)
    # Generate table of contents
    ccomic_chapters = [item.chapters for item in ccomics]
    no_chapters = all(item in falses for item in ccomic_chapters)
    if not single:
        toc_heading = "<h2>{toc_s}</h2>".format(toc_s=translated_strings["toc_s"])
        toc_elements = [
            """<nav class="archive toc" id="toc" role="directory">""",
            toc_heading,
            """<ol class="chapterarch">""",
        ]
        for comic in ccomics:
            if comic.chapters not in falses:
                c_toc_heading = """<li><a href="#id-{slug}">{category}</a>""".format(
                    slug=comic.slug, category=comic.category
                )
            else:
                c_toc_heading = (
                    """<li><a href="#id-{slug}">{category}</a></li>""".format(
                        slug=comic.slug, category=comic.category
                    )
                )
            toc_elements.append(c_toc_heading)
            if comic.chapters:
                chapter_toc = ["""<ol class="chapterarch">"""]
                for chapter in comic.chapters_list:
                    try:
                        chapter_s = translated_strings["chapter_s"].format(
                            chapter=chapter.chap_number,
                            chapter_title=chapter.chap_title,
                        )
                    except AttributeError:
                        chapter_s = translated_strings["notitle_chapter_s"].format(
                            chapter=chapter.chap_number
                        )
                    chapter_heading = translated_strings["category_chapter_s"].format(
                        category=comic.category, chapter_s=chapter_s
                    )
                    chapter_slug = slugurl.slugify_url(chapter_heading)
                    escaped_chap_slug = html.escape(chapter_slug)
                    chapter.slug = "id-{slug}".format(slug=escaped_chap_slug)
                    chapter_link = """<li><a href="#{slug}">{title}</a></li>""".format(
                        slug=chapter.slug, title=chapter_heading
                    )
                    chapter_toc.append(chapter_link)
                chapter_toc.append("</ol></li>")
                toc_elements.append("".join(chapter_toc))
            else:
                logmesg = _(
                    "Not generating table of contents, because I couldn't find any chapters."
                )
                logging.debug(logmesg)
        if all_tags:
            toc_elements.append(
                f"""<li><a href="#tags">{translated_strings["tags_s"]}</a></li>"""
            )
        toc_elements.append("</ol></nav>")
        toc = "".join(toc_elements)
    else:
        for comic in ccomics:
            if comic.chapters:
                toc_heading = "<h2>{toc_s}</h2>".format(
                    toc_s=translated_strings["toc_s"]
                )
                toc_elements = [
                    """<nav class="archive toc" id="toc" role="directory">""",
                    toc_heading,
                    """<ol class="chapterarch">""",
                ]
                for chapter in comic.chapters_list:
                    try:
                        chapter_s = translated_strings["chapter_s"].format(
                            chapter=chapter.chap_number,
                            chapter_title=chapter.chap_title,
                        )
                    except AttributeError:
                        chapter_s = translated_strings["notitle_chapter_s"].format(
                            chapter=chapter.chap_number
                        )
                    chapter_heading = translated_strings["category_chapter_s"].format(
                        category=comic.category, chapter_s=chapter_s
                    )
                    chapter_slug = slugurl.slugify_url(chapter_heading)
                    escaped_chap_slug = html.escape(chapter_slug)
                    chapter.slug = "id-{slug}".format(slug=escaped_chap_slug)
                    chapter_link = """<li><a href="#{slug}">{title}</a></li>""".format(
                        slug=chapter.slug, title=chapter_heading
                    )
                    toc_elements.append(chapter_link)
                if all_tags:
                    toc_elements.append(
                        f"""<li><a href="#tags">{translated_strings["tags_s"]}</a></li>"""
                    )
                toc_elements.append("</ol></nav>")
                toc = "".join(toc_elements)
            else:
                toc = ""
                logmesg = _(
                    "Not generating table of contents, because I couldn't find any chapters."
                )
                logging.debug(logmesg)

    for comic in tqdm(ccomics):
        category = comic.category
        status = comic.statuss
        comic_header = comic.header
        desc = comic.desc
        logmesg = _("Currently working on {category}.").format(category=category)
        logging.debug(logmesg)

        # Get the comic-specific header.
        old_cheader_path = os.path.join(c_path, "input", comic_header)
        new_cheader_path = os.path.join(o_path, comic_header)

        if new_cheader_path not in existing_files:
            tasks.append(
                springheel.copystuff.copyHeader(old_cheader_path, new_cheader_path)
            )
            existing_files.append(new_cheader_path)
        else:
            logging.debug(
                file_exists_s.format(
                    outf=os.path.relpath(new_cheader_path),
                    var=f"{comic.category} header",
                )
            )
        # For ease of code reuse ;;
        match = comic

        archive_links_page = []
        archive_links_date = []
        for i in comic.pbp:
            archive_link = generatearchive.getLinks(i, translated_strings)
            i.archive_link = archive_link
            if archive_link not in archive_links_page:
                archive_links_page.append(archive_link)
        for i in comic.pbd:
            if not hasattr(i, "archive_link"):
                archive_link = generatearchive.getLinks(i, translated_strings)
                i.archive_link = archive_link
            if archive_link not in archive_links_date:
                archive_links_date.append(archive_link)
        if comic.chapters in falses:
            non_chaptered_archives = generatearchive.generateSeriesArchives(
                comic.category_escaped, status, archive_links_page, comic.slug
            )
            archives_r.append(non_chaptered_archives)

        if comic.chapters not in falses:
            for page in comic.pbp:
                # Make sure there aren't unchaptered pages in chapter
                if hasattr(page, "chapter") and page.chapter not in falses:
                    match = page.get_matching(ccomics)
                    cho = [
                        item
                        for item in match.chapters_list
                        if item.chap_number == int(page.chapter)
                    ][0]
                    cho.pages.append(page)
                else:
                    logmesg = _(
                        "Comic {cate} expects a chapter, but page #{page} doesn't have one. Please add a chapter to {pagemeta}."
                    ).format(cate=match.category, page=page.page, pagemeta=page.metaf)
                    logging.error(logmesg)
                    return False
        if comic.chapters not in falses:
            chapter_sections = []
            for chapi in match.chapters_list:
                in_this_chapter = []
                if not hasattr(chapi, "authors"):
                    chapi.authors = set([item.author for item in chapi.pages])
                if not hasattr(chapi, "years"):
                    chapi.years = set([item.year for item in chapi.pages])
                for page in chapi.pages:
                    in_this_chapter.append(page.archive_link)
                if single:
                    header_level = "2"
                else:
                    header_level = "3"
                archive_list = generatearchive.generateChapArchList(
                    in_this_chapter, chapi, translated_strings, header_level
                )
                chapter_sections.append(archive_list)
            chapter_sections_j = sep.join(chapter_sections)
            if not single:
                chapter_archives_r = sep.join(
                    [
                        '<section class="archive">',
                        '<h2 id="id-{slug}">{category}</h2>',
                        '<p class="status">{status}</p>',
                        chapter_sections_j,
                        "</section>",
                    ]
                )
            else:
                chapter_archives_r = sep.join(
                    [
                        '<section class="archive">',
                        '<p class="status">{status}</p>',
                        chapter_sections_j,
                        "</section>",
                    ]
                )
            chapter_archives = chapter_archives_r.format(
                slug=comic.slug, category=comic.category_escaped, status=comic.statuss
            )
            archives_r.append(chapter_archives)

    archives = sep.join(archives_r)

    if all_tags:
        tags_sorted = sorted(all_tags, key=lambda x: x.name)
        tag_section_content = [
            """<section class="archive" id="tags">""",
            "<h2>{tags_s}</h2>".format(tags_s=translated_strings["tags_s"]),
            """<ul class="tagslist">""",
        ]
        for tag in tags_sorted:
            tag_count = len(tag.strips)
            tag_section_content.append(
                "<li>{link} ({tag_count})</li>".format(
                    link=tag.link, tag_count=tag_count
                )
            )
        tag_section_content.append("</ul>")
        tag_section_content.append("</section>")
        tag_sectionn = sep.join(tag_section_content)
    else:
        tag_sectionn = ""

    arch_template_fn = os.path.join(c_path, archive_t)

    link_rel_l = [
        '<link rel="alternate" type="application/rss+xml" title="{rss_s}" href="feed.xml">'.format(
            rss_s=translated_strings["rss_s"]
        ),
        '<link rel="alternate" type="application/json" title="{jsonfeed_name}" href="feed.json">'.format(
            jsonfeed_name=translated_strings["jsonfeed_name"]
        ),
    ]
    link_rel = sep.join(link_rel_l)

    out_file = os.path.join(o_path, "archive.html")

    archive_header_title = "{site_title} - {archive_s}".format(
        site_title=site.config.site_title, archive_s=translated_strings["archive_s"]
    )
    archive_url = "".join([site.config.base_url, "archive.html"])
    site_img_url = "".join([site.config.base_url, site.config.header_filename])
    meta_tags = metatag.genMetaTags(
        archive_header_title, archive_url, site.config.description, site_img_url
    )
    meta_tags_ready = "\n".join(meta_tags)

    with open(arch_template_fn) as f:
        arch_template = f.read()

    arch_string = arch_template.format(
        lang=site.config.language,
        site_style=site.config.site_style,
        banneralt=site.config.site_title,
        headerw=site_header_w,
        headerh=site_header_h,
        header_title=archive_header_title,
        h1_title=archive_header_title,
        meta_tags=meta_tags_ready,
        linkrels=link_rel,
        header=site.config.header_filename,
        status=status,
        top_site_nav=top_site_nav,
        toc=toc,
        archive_sections=archives,
        tag_section=tag_sectionn,
        year=year_range,
        author=site.config.site_author,
        copyright_statement=copyright_statement,
        icons=icons,
        home_s=translated_strings["home_s"],
        archive_s=translated_strings["archive_s"],
        stylesheet_name_s=translated_strings["stylesheet_name_s"],
        skip_s=translated_strings["skip_s"],
        page_s=translated_strings["page_s"],
        meta_s=translated_strings["meta_s"],
        generator_s=translated_strings["generator_s"].format(
            version=springheel.__version__
        ),
        goarchive_s=translated_strings["goarchive_s"],
        url=archive_url,
    )

    logmesg = _("Writing {archive}...").format(archive="archive.html")
    logging.debug(logmesg)
    with open(out_file, "w+", encoding="utf-8") as fout:
        fout.write(arch_string)
    logmesg = _("{archive} written.").format(archive="archive.html")
    logging.debug(logmesg)
    modified_time = datetime.datetime.strftime(
        datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),
        "%Y-%m-%dT%H:%M:%S.%fZ",
    )
    sitemap_loc = {
        "loc": archive_url,
        "lastmod": modified_time,
    }
    site.sitemap.append(sitemap_loc)

    chapter_template_fn = os.path.join(c_path, chapter_t)
    # Generate chapter pages
    with open(chapter_template_fn) as f:
        chap_template = f.read()
    logmesg = _("Generating chapter pages...")
    logging.info(logmesg)
    for comic in tqdm(ccomics):
        if comic.chapters:
            all_chapter_nums = [item.chap_number for item in comic.chapters_list]
            all_ch_padded = [padNum(item, zero_padding)[1] for item in all_chapter_nums]
            all_chapter_nums.sort()
            all_ch_padded.sort()
            try:
                if comic.category_theme:
                    theme_2_use = comic.category_theme
                else:
                    theme_2_use = site.config.site_style
            except AttributeError:
                theme_2_use = site.config.site_style
            for chapi_id, chapi in enumerate(comic.chapters_list):
                if len(chapi.pages) == 0:
                    logmesg = _(
                        "There aren't any comics in {category} Chapter {chap}. I can't create a chapter without pages."
                    ).format(category=comic.category, chap=chapi.chap_number)
                    logging.error(logmesg)
                    return False

                try:
                    chapter_s = translated_strings["chapter_s"].format(
                        chapter=chapi.chap_number,
                        chapter_title=chapi.chap_title_escaped.strip(),
                    )
                except AttributeError:
                    chapter_s = translated_strings["notitle_chapter_s"].format(
                        chapter=chapi.chap_number
                    )
                ch_h1_s = translated_strings["category_chapter_s"].format(
                    category=comic.category,
                    chapter_s=chapter_s,
                )
                if comic.mode == "webtoon":
                    modeclass = " webtoon"
                else:
                    modeclass = ""
                chapter_page_contents = genchbook.genChapBook(
                    translated_strings,
                    chapi,
                    nocomment_test,
                    modeclass,
                    meta_file_ext,
                    transcr_file_ext,
                )
                ch_padded = padNum(chapi.chap_number, zero_padding)
                outfn = chapi.ch_outfn
                out_path = os.path.join("output", outfn)
                ch_url = "".join([site.config.base_url, outfn])
                meta_tags = metatag.genMetaTags(
                    "{ch_h1_s} | {site_title}".format(
                        site_title=site.config.site_title, ch_h1_s=ch_h1_s
                    ),
                    ch_url,
                    comic.desc,
                    site_img_url,
                )
                meta_tags_ready = "\n".join(meta_tags)
                ch_navblock, ch_linkrels = generatenav.navGen(
                    site.config.navdirection,
                    ch_padded[1],
                    all_ch_padded[0],
                    all_ch_padded[-1],
                    first,
                    final,
                    comic.slug,
                    theme_2_use,
                    translated_strings,
                    all_ch_padded,
                    all_chapter_nums,
                    chapi_id,
                    site.images,
                    chapter_mode=True,
                )
                if not comic.publicdomain:
                    clyears = list(chapi.years)
                    ch_first_year = min(clyears)
                    if ch_first_year == c_year:
                        ch_copyright_year = ch_first_year
                    else:
                        ch_copyright_year = "{fy}&ndash;{ly}".format(
                            fy=ch_first_year, ly=c_year
                        )
                    if len(chapi.authors) > 1:
                        authors = " &amp; ".join(chapi.authors)
                    else:
                        (authors,) = chapi.authors
                    ch_copyright_statement = (
                        "<p>&copy; {year} {author}. {clicense}</p>".format(
                            year=ch_copyright_year,
                            author=authors,
                            clicense=comic.license,
                        )
                    )
                else:
                    ch_copyright_statement = springheel.wraptag.wrapWithTag(
                        license_c, "p"
                    )

                ch_top_nav = springheel.wraptag.wrapWithComment(
                    ch_navblock.format(boxlocation="topbox"), "TOP NAVIGATION"
                )
                ch_bottom_nav = springheel.wraptag.wrapWithComment(
                    ch_navblock.format(boxlocation="botbox"), "BOTTOM NAVIGATION"
                )
                ch_main_classes = []
                if site.config.navdirection == "rtl":
                    ch_main_classes.append("rtl")
                if modeclass:
                    ch_main_classes.append("webtoon")
                ch_main_class = (
                    f""" class="{" ".join(ch_main_classes)}\""""
                    if ch_main_classes
                    else ""
                )

                chap_string = chap_template.format(
                    lang=comic.language,
                    site_style=theme_2_use,
                    header_title=ch_h1_s,
                    stylesheet_name_s=translated_strings["stylesheet_name_s"],
                    meta_tags=meta_tags_ready,
                    linkrels=ch_linkrels,
                    skiplink="#chapbook",
                    skip_s=translated_strings["skip_s"],
                    header=comic.header,
                    headerw=comic.headerw,
                    headerh=comic.headerh,
                    mainclass=ch_main_class,
                    modeclass=modeclass,
                    category=comic.category_escaped,
                    top_site_nav=top_site_nav,
                    top_nav=ch_top_nav,
                    h1_title=ch_h1_s,
                    chapter_sections=chapter_page_contents,
                    bottom_nav=ch_bottom_nav,
                    author=author,
                    icons=icons,
                    home_s=translated_strings["home_s"],
                    archive_s=translated_strings["archive_s"],
                    caption_s=translated_strings["caption_s"],
                    metadata_s=translated_strings["meta_s"],
                    copyright_statement=ch_copyright_statement,
                    page_s=translated_strings["page_s"],
                    meta_s=translated_strings["meta_s"],
                    generator_s=translated_strings["generator_s"].format(
                        version=springheel.__version__
                    ),
                    goarchive_s=translated_strings["goarchive_s"],
                    url=ch_url,
                )

                logmesg = _("Writing {outfn}...").format(outfn=outfn)
                logging.debug(logmesg)
                with open(out_path, "w+", encoding="utf-8") as fout:
                    fout.write(chap_string)
                modified_time = datetime.datetime.strftime(
                    datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                )
                sitemap_loc = {"loc": ch_url, "lastmod": modified_time}
                site.sitemap.append(sitemap_loc)
        else:
            pass

    ##Generate feed

    base_url = site.config.base_url

    rssmeta = {
        "author": site.config.site_author_email,
        "email": site.config.site_author_email,
        "language": site.config.language,
        "link": site.config.base_url,
        "desc": site.config.description,
        "title": site.config.site_title,
    }

    rss = genrss.generateFeed(site.config.base_url, rssmeta, comics_base, o_path)

    # Generate characters page if necessary.
    if characters_page:
        site.jsonpoints["characters_page"] = "".join(
            [site.config.base_url, "characters.html"]
        )
        chartasks = springheel.genchars.saveCharsPage(
            ccomics,
            site,
            chars_t,
            translated_strings,
            site_img_url,
            year_range,
            top_site_nav,
            falses,
            link_rel,
            icons,
            sep,
        )
        tasks += chartasks

    # Generate main page
    index_url = "".join([site.config.base_url, "index.html"])
    meta_tags = metatag.genMetaTags(
        site.config.site_title, index_url, site.config.description, site_img_url
    )
    meta_tags_ready = "\n".join(meta_tags)
    multi_secs = genmultipleindex.genMultipleIndex(
        ccomics,
        characters_page,
        translated_strings,
        site.config.description,
        site.images,
    )
    secs = sep.join(multi_secs)

    template = os.path.join(c_path, index_t)

    out_file = os.path.join(o_path, "index.html")

    with open(template) as f:
        index_template = f.read()

    n_string = index_template.format(
        lang=site.config.language,
        site_style=site.config.site_style,
        header_title=site.config.site_title,
        meta_tags=meta_tags_ready,
        linkrels=link_rel,
        header=site.config.header_filename,
        headerw=site_header_w,
        headerh=site_header_h,
        site_title=site.config.site_title,
        category=site.config.site_title,
        top_site_nav=top_site_nav,
        multi_secs=secs,
        year=year,
        author=site.config.site_author,
        copyright_statement=copyright_statement,
        icons=icons,
        home_s=translated_strings["home_s"],
        archive_s=translated_strings["archive_s"],
        stylesheet_name_s=translated_strings["stylesheet_name_s"],
        skip_s=translated_strings["skip_s"],
        page_s=translated_strings["page_s"],
        meta_s=translated_strings["meta_s"],
        generator_s=translated_strings["generator_s"].format(
            version=springheel.__version__
        ),
        goarchive_s=translated_strings["goarchive_s"],
        url=index_url,
    )

    logmesg = _("Writing {indexh}...").format(indexh="index.html")
    logging.debug(logmesg)
    with open(out_file, "w+", encoding="utf-8") as fout:
        fout.write(n_string)
    modified_time = datetime.datetime.strftime(
        datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),
        "%Y-%m-%dT%H:%M:%S.%fZ",
    )
    sitemap_loc = {
        "loc": index_url,
        "lastmod": modified_time,
    }
    site.sitemap.append(sitemap_loc)

    # Generate extras page if necessary.
    extras_j = os.path.join(i_path, "Extra.json")
    if extras_page and os.path.exists(extras_j):
        extras, j, extra_copyq = genextra.gen_extra(
            i_path, o_path, extras_j, translated_strings, site.images
        )
        tasks.append(genextra.copyExtras(extra_copyq))

        if j:

            site.jsonpoints["extras"] = j

            extr_title = " - ".join(
                [site.config.site_title, translated_strings["extra_s"]]
            )

            ex_html_filename = "extras.html"
            out_file = os.path.join(o_path, ex_html_filename)
            site.jsonpoints["extras_page"] = "".join([base_url, ex_html_filename])

            meta_tags = metatag.genMetaTags(
                "{page_title} | {site_title}".format(
                    site_title=site.config.site_title, page_title=extr_title
                ),
                site.jsonpoints["extras_page"],
                site.config.description,
                site_img_url,
            )
            meta_tags_ready = "\n".join(meta_tags)

            with open(extra_t) as f:
                extra_template = f.read()

            extras_html = extra_template.format(
                lang=site.config.language,
                site_style=site.config.site_style,
                header_title=extr_title,
                meta_tags=meta_tags_ready,
                h1_title=translated_strings["extra_s"],
                stylesheet_name_s=translated_strings["stylesheet_name_s"],
                home_s=translated_strings["home_s"],
                linkrels=linkrels,
                skip_s=translated_strings["skip_s"],
                header=site.config.header_filename,
                headerw=site_header_w,
                headerh=site_header_h,
                site_title=site.config.site_title,
                top_site_nav=top_site_nav,
                extras=extras.content,
                copyright_statement=copyright_statement,
                generator_s=translated_strings["generator_s"].format(
                    version=springheel.__version__
                ),
                icons=icons,
            )

            with open(out_file, "w", encoding="utf-8") as fout:
                fout.write(extras_html)
            logmesg = _("Extras page written to {out_file}.").format(
                out_file="extras.html"
            )
            logging.debug(logmesg)
            modified_time = datetime.datetime.strftime(
                datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),
                "%Y-%m-%dT%H:%M:%S.%fZ",
            )
            sitemap_loc = {
                "loc": site.jsonpoints["extras_page"],
                "lastmod": modified_time,
            }
            site.sitemap.append(sitemap_loc)
        else:
            logmesg = _(
                "Extra pages are supposed to be generated, but I couldn't load input/Extra.json as valid JSON. Check it for errors and try again."
            )
            logging.error(logmesg)
    else:
        logmesg = _(
            "Not generating extras page (extras_page set to False or input/Extra.json not found)."
        )
        logging.debug(logmesg)

    ###########################################################################
    # Generate tags pages if necessary
    if len(all_tags):
        logmesg = _("Generating tag indices...")
        logging.info(logmesg)

        for tag in tqdm(all_tags):
            tags_links_page = ["""<ol class="tagslist">"""]
            tag_outn = "tag-{tag_slug}.html".format(tag_slug=tag.slug)
            tag_outf = os.path.join(o_path, tag_outn)
            tag_h = "{tags_s}: {tag}".format(
                tags_s=translated_strings["tags_s"], tag=tag.name
            )
            for strip in tag.strips:
                tag_l = translated_strings["h1_s"].format(
                    category=strip.category, title=strip.title, page=strip.page
                )
                link_format = """<li><a href="{html_filename}">{tag_l}</a></li>"""
                tag_link = link_format.format(
                    html_filename=strip.html_filename, tag_l=tag_l
                )
                tags_links_page.append(tag_link)
            tags_links_page.append("</ol>")
            tag_section = sep.join(tags_links_page)

            link_rel_l = [
                '<link rel="alternate" type="application/rss+xml" title="{rss_s}" href="feed.xml">'.format(
                    rss_s=translated_strings["rss_s"]
                )
            ]
            link_rel = sep.join(link_rel_l)
            tag_url = "".join([site.config.base_url, tag_outn])
            tag_remote_title = " | ".join([tag_h, site.config.site_title])
            meta_tags = metatag.genMetaTags(
                tag_remote_title, tag_url, site.config.description, site_img_url
            )
            meta_tags_ready = "\n".join(meta_tags)

            tag_template_name = archive_t
            tag_template = os.path.join(c_path, tag_template_name)

            with open(tag_template) as f:
                tag_template = f.read()

            tag_html = tag_template.format(
                lang=site.config.language,
                site_style=site.config.site_style,
                banneralt=site.config.site_title,
                header_title=" | ".join([tag_h, site.config.site_title]),
                h1_title=tag_h,
                meta_tags=meta_tags_ready,
                linkrels=link_rel,
                header=site.config.header_filename,
                headerw=site_header_w,
                headerh=site_header_h,
                status=status,
                top_site_nav=top_site_nav,
                toc="",
                archive_sections=tag_section,
                tag_section="",
                year=year,
                author=site.config.site_author,
                copyright_statement=copyright_statement,
                icons=icons,
                home_s=translated_strings["home_s"],
                archive_s=translated_strings["archive_s"],
                stylesheet_name_s=translated_strings["stylesheet_name_s"],
                skip_s=translated_strings["skip_s"],
                page_s=translated_strings["page_s"],
                meta_s=translated_strings["meta_s"],
                generator_s=translated_strings["generator_s"].format(
                    version=springheel.__version__
                ),
                goarchive_s=translated_strings["goarchive_s"],
                url=tag_url,
            )

            with open(tag_outf, "w", encoding="utf-8") as fout:
                fout.write(tag_html)
            logmesg = _("Tag page written to {out_file}.").format(out_file=tag_outn)
            logging.debug(logmesg)
            modified_time = datetime.datetime.strftime(
                datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),
                "%Y-%m-%dT%H:%M:%S.%fZ",
            )
            sitemap_loc = {
                "loc": tag_url,
                "lastmod": modified_time,
            }
            site.sitemap.append(sitemap_loc)

    if gen_about:
        logging.debug(_("Generating about page..."))
        about_elements, about_meta_tags = genabout.makeAbout(
            ccomics, translated_strings, single, site, site.images
        )
        about_url = "".join([site.config.base_url, "about.html"])

        with open(arch_template_fn) as fin:
            about_template = fin.read()
        about_string = about_template.format(
            lang=site.config.language,
            site_style=site.config.site_style,
            banneralt=site.config.site_title,
            header_title=" | ".join(
                [translated_strings["about_s"], site.config.site_title]
            ),
            archive_s=translated_strings["about_s"],
            h1_title=translated_strings["about_s"],
            meta_tags=about_meta_tags,
            linkrels=link_rel,
            header=site.config.header_filename,
            headerw=site_header_w,
            headerh=site_header_h,
            category="",
            top_site_nav=top_site_nav,
            toc="",
            archive_sections="\n".join(about_elements),
            tag_section="",
            year=year,
            author=site.config.site_author,
            copyright_statement=copyright_statement,
            icons=icons,
            home_s=translated_strings["home_s"],
            stylesheet_name_s=translated_strings["stylesheet_name_s"],
            skip_s=translated_strings["skip_s"],
            page_s=translated_strings["page_s"],
            meta_s=translated_strings["meta_s"],
            generator_s=translated_strings["generator_s"].format(
                version=springheel.__version__
            ),
            goarchive_s=translated_strings["goarchive_s"],
            url=about_url,
            skiplink=skiplink,
        )
        logmesg = _("Writing {about}...").format(about="about.html")
        logging.debug(logmesg)
        out_file = os.path.join(o_path, "about.html")
        with open(out_file, "w+", encoding="utf-8") as fout:
            fout.write(about_string)
        logmesg = _("{about} written.").format(about="about.html")
        logging.debug(logmesg)
        modified_time = datetime.datetime.strftime(
            datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),
            "%Y-%m-%dT%H:%M:%S.%fZ",
        )
        sitemap_loc = {
            "loc": about_url,
            "lastmod": modified_time,
        }
        site.sitemap.append(sitemap_loc)

    # Generate sitemap
    sitemap_close = "</urlset>"
    sitemap_sorted = sorted(site.sitemap, key=lambda k: k["loc"])
    # Move index to the beginning
    for sitepage in sitemap_sorted:
        if sitepage["loc"][-11:] == "/index.html":
            smap_index_ind = sitemap_sorted.index(sitepage)
    sitemap_sorted.insert(0, sitemap_sorted.pop(smap_index_ind))
    formatted_sitemap = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for sitepage in sitemap_sorted:
        smap_entry = "<url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>".format(
            loc=sitepage["loc"], lastmod=sitepage["lastmod"]
        )
        formatted_sitemap.append(smap_entry)
    formatted_sitemap.append("</urlset>")
    sitemap = os.linesep.join(formatted_sitemap)
    sitemap_xml_fn = "sitemap.xml"
    sitemap_out = os.path.join(o_path, sitemap_xml_fn)
    with open(sitemap_out, "w", encoding="utf-8") as fout:
        fout.write(sitemap)
    logmesg = _("Generated sitemap at {sitemap_fn}.").format(sitemap_fn=sitemap_xml_fn)
    logging.debug(logmesg)

    # Generate JSON endpoints file

    json_fn = "site.json"
    jsonpoints_out = os.path.join(o_path, json_fn)
    with open(jsonpoints_out, "w", encoding="utf-8") as fout:
        json.dump(site.jsonpoints, fout)
    logmesg = _("Generated JSON endpoints file at {json_fn}.").format(json_fn=json_fn)
    logging.debug(logmesg)

    # Generate JSON Feed
    json_feed_contents = springheel.genjsonfeed.genJsonFeed(
        site.jsonpoints, translated_strings
    )
    jsonfeed_fn = "feed.json"
    jsonfeed_out = os.path.join(o_path, jsonfeed_fn)
    with open(jsonfeed_out, "w", encoding="utf-8") as fout:
        json.dump(json_feed_contents, fout)
    logmesg = _("Generated JSON Feed at {jsonfeed_fn}.").format(jsonfeed_fn=jsonfeed_fn)
    logging.debug(logmesg)
    logging.info(_("Copying files..."))
    for task in tqdm.as_completed(tasks):
        await task
    logging.debug(_("Copying complete."))

    logmesg = _("Springheel compilation complete! ^_^")
    logging.info(logmesg)


async def init():
    """Initialize a Springheel project."""
    logfile = os.path.join(".", "springheel.log")
    try:
        logging_level = sys.argv[1] == "--logging"
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)-8s %(message)s",
            filename=logfile,
            filemode="w",
        )
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(levelname)-8s %(asctime)s.%(msecs)03d: %(message)s", datefmt="%H:%M:%S"
        )
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger("").addHandler(console)
    except IndexError:
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)-8s %(asctime)s.%(msecs)03d: %(message)s",
            datefmt="%H:%M:%S",
        )
    logging.info(
        _("Initializing Springheel site at {dire}.").format(dire=os.path.abspath("."))
    )
    await springheelinit.copyAssets()


def version():
    """Print version information."""
    print(
        "{name} {version} copyright 2017-2021 {author}. Some rights reserved. See LICENSE.".format(
            name=springheel.name,
            author=springheel.author,
            version=springheel.__version__,
        )
    )
    print(_("Installed to {dir}.").format(dir=sys.modules["springheel"].__path__[0]))
    print(
        _(
            "Run springheel-init to create a new site in the current directory, or springheel-build to regenerate the site."
        )
    )
