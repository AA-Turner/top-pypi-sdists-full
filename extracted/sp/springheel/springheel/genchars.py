#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Generate characters page
########
##  Copyright 2017-2020 garrick. Some rights reserved.
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

"""Generate character pages."""

import json, os, logging, datetime
from springheel.splitseps import splitAtSeparators
from tqdm import tqdm
from typing import List, Union, Set
from springheel.tl import gettext as _
import springheel.metatag
from springheel.copystuff import copyfile
from springheel.classes import *
from asyncio import coroutine


def loadChars(fp: str, json_mode: bool) -> List[dict]:
    """Try to load a characters file.

    Parameters
    ----------
    fp : str
        The path to the file to open.
    json_mode : bool
        Whether to load the file as JSON (True) or plain text (False).

    Returns
    -------
    list of dict
        A list of dictionaries (parsed character file data).
    """
    if json_mode:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                characters_parsed = json.load(f)
        except json.decoder.JSONDecodeError:
            logmesg = _(
                "{fp} is supposed to be a JSON file, but I can't load it as one. It may be invalid. Trying as YAML..."
            ).format(fp=fp)
            logging.warning(logmesg)
            characters_parsed = loadChars(fp, False)
        return characters_parsed
    else:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                raw_text = f.read()
        except UnboundLocalError:
            logmesg = _(
                "An Unbound Local Error has occurred. I'm probably looking for a page that doesn't exist."
            )
            logging.warning(logmesg)
        except FileNotFoundError:
            logmesg = _(
                "The characters page couldn't be built because I couldn't find the characters file at {fp}."
            ).format(fp=fp)
            logging.warning(logmesg)
        characters_parsed = parseChars(raw_text)
        return characters_parsed


def parseChars(charfile: str) -> List[dict]:
    """
    Format the contents of a character file.

    Parameters
    ----------
    charfile : str
        The contents of a character file.

    Returns
    -------
    list of dict
        A list of character file elements formatted as dictionaries.
    """
    # Get character sections according to the dividers.
    separators = [
        "\r\n",
        "\r",
        "\n",
        "\v",
        "\f",
        "\x1c",
        "\x1d",
        "\x1e",
        "\x85",
        "\u2028",
        "\u2029",
    ]
    dividers = ["".join(["---", sep]) for sep in separators]
    sectioned = splitAtSeparators(charfile, dividers)
    resectioned = [item.splitlines() for item in sectioned]

    cl = []

    characters = resectioned[1:]

    for char in characters:
        char_attrs = {}
        for item in char:
            # Get character attributes.
            try:
                attr, val = item.split(": ", 1)
                char_attrs[attr] = val
            # Ignore attributes without a key: value syntax as they're
            # probably just "---" or whatever.
            except ValueError:
                pass
        if char_attrs != {}:
            cl.append(char_attrs)

    return cl


def genCharsPage(chars_list: List[dict], images: dict) -> str:
    """
    Create a characters page from a list of character elements.

    Parameters
    ----------
    chars_list : list of dict
        A list of character file elements.
    images : dict
        A dictionary mapping image filenames to (width, height) in
        pixels.

    Returns
    -------
    str
        The contents of the generated HTML characters page.
    """
    sep = os.linesep
    chars = []
    default_keys = {"name", "img", "desc"}
    for item in chars_list:
        char_elements = ['<div class="char">']
        try:
            title = """<h2 class="charname">{name}</h2>""".format(name=item["name"])
            char_elements.append(title)
            if item["img"] != "None":
                width, height = images[item["img"]]
                img = '<img src="{img}" class="charimg" alt="" width="{width}" height="{height}">'.format(
                    img=item["img"], width=width, height=height
                )
                char_elements.append(img)
            # We only need to worry about the DL element if there are custom attributes.
            if set(item.keys()) != default_keys:
                dls = []
                char_elements.append("""<dl class="chartraits">""")
                for attr, val in item.items():
                    if attr in default_keys:
                        pass
                    else:
                        line = "<dt>{attr}</dt>{sep}<dd>{val}</dd>".format(
                            attr=attr, val=val, sep=sep
                        )
                        dls.append(line)
                dl = sep.join(dls)
                char_elements.append(dl)
                char_elements.append("</dl>")
            char_elements.append('<div class="chartext">')
            desc = "<p>{desc}</p>".format(desc=item["desc"])
            char_elements.append(desc)
            char_elements.append("</div>")
            char_elements.append("</div>")
            char_fin = sep.join(char_elements)
            chars.append(char_fin)
        except TypeError:
            pass
        except KeyError:
            pass
    characters = sep.join(chars)
    return characters


def saveCharsPage(
    ccomics: List[Comic],
    site: Site,
    chars_t: str,
    translated_strings: dict,
    site_img_url: str,
    year: str,
    top_site_nav: str,
    falses: set,
    link_rel: str,
    icons: str,
    sep: str,
) -> List[coroutine]:
    """
    Create character pages for every category that should have one.

    Parameters
    ----------
    ccomics : list of Comic
        A list of :class:`Comic` series/categories to check.
    site : Site
        The :class:`Site` to make pages for.
    chars_t : str
        The path to the characters page template.
    translated_strings : dict
        The translation file contents for this site.
    site_img_url : str
        The full URL of an image that represents this site. Used for
        meta tags.
    year : str
        The year(s) to put in the copyright footer.
    top_site_nav : str
        The top navigation.
    falses : set
        A variety of different "negative" values, as a character image
        string might be False, None, Null, Disable, etc.
    link_rel : str
        Link rel values to put into page headers.
    icons : str
        Social icons to use in the footer.
    sep : str
        A line separator to use in output.

    Returns
    -------
    list of coroutine
        A list of asynchronous file-copying tasks.
    """

    character_pages = []
    tasks = []

    logmesg = _("Making character pages...")
    logging.info(logmesg)
    for comic in tqdm(ccomics):
        category = comic.category
        if comic.chars_file:
            fn = comic.chars_file
            fp = os.path.join(site.i_path, fn)
            logmesg = _("Loading characters file {fn}.").format(fn=fn)
            logging.debug(logmesg)
            characters_parsed = loadChars(fp, site.config.json_mode)
            # reset jsoncat
            jsoncat = [
                item
                for item in site.jsonpoints["categories"]
                if item["category"] == category
            ][0]
            chard_i = jsoncat.setdefault("characters", {})
            chard = chard_i.setdefault("items", characters_parsed)
            character_elements = genCharsPage(characters_parsed, site.images)

            # Get character images
            for char in characters_parsed:
                try:
                    if char["img"] not in falses:
                        img_source_path = os.path.join(site.i_path, char["img"])
                        img_out_path = os.path.join(site.o_path, char["img"])
                        tasks.append(copyfile(img_source_path, img_out_path))
                except AttributeError:
                    pass
                except TypeError:
                    pass
                except KeyError:
                    pass

            chars_template_path = os.path.join(site.c_path, chars_t)

            cat_slug = comic.slug

            if site.single:
                out_name = "characters.html"
            else:
                out_name = "".join([cat_slug, "-", "characters.html"])
                cpd = {"charpage": out_name, "category": category}
                character_pages.append(cpd)
            comic.chars_fn = out_name
            chars_url = chard_i.setdefault(
                "url", "".join([site.config.base_url, out_name])
            )
            out_file = os.path.join(site.o_path, out_name)

            chars_h1_line = " - ".join([category, translated_strings["char_s"]])
            chars_title_line = " | ".join([translated_strings["char_s"], category])
            if comic.category_theme:
                theme_2_use = comic.category_theme
            else:
                theme_2_use = site.config.site_style
            meta_tags = springheel.metatag.genMetaTags(
                chars_title_line, chars_url, site.config.description, site_img_url
            )
            meta_tags_ready = "\n".join(meta_tags)

            with open(chars_template_path) as f:
                chars_template = f.read()

            n_string = chars_template.format(
                lang=comic.language,
                site_style=theme_2_use,
                header_line=chars_h1_line,
                meta_tags=meta_tags_ready,
                linkrels=link_rel,
                header=comic.header,
                headerw=comic.headerw,
                headerh=comic.headerh,
                header_alt=category,
                title_line=chars_title_line,
                top_site_nav=top_site_nav,
                chars=character_elements,
                year=year,
                author=site.config.site_author,
                copyright_statement=site.copyright_statement,
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
                url=chars_url,
            )

            logmesg = _("Writing {out_name}...").format(out_name=out_name)
            logging.debug(logmesg)
            with open(out_file, "w", encoding="utf-8") as fout:
                fout.write(n_string)
            modified_time = datetime.datetime.strftime(
                datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),
                "%Y-%m-%dT%H:%M:%S.%fZ",
            )
            sitemap_loc = {
                "loc": chars_url,
                "lastmod": modified_time,
            }
            site.sitemap.append(sitemap_loc)
        else:
            logmesg = _("No character file found for {category}, skipping...").format(
                category=category
            )
            logging.debug(logmesg)

    if not site.single:
        out_name = "characters.html"
        out_file = os.path.join(site.o_path, out_name)
        chars_template_path = os.path.join(site.c_path, chars_t)

        chars_h1_line = " - ".join(
            [site.config.site_title, translated_strings["char_s"]]
        )
        chars_title_line = " | ".join(
            [translated_strings["char_s"], site.config.site_title]
        )

        charpage_elements = ['<div class="allchars">']

        logmesg = _("Character pages: {character_pages}").format(
            character_pages=character_pages
        )
        logging.debug(logmesg)
        for chpage in character_pages:
            character_page_line = [
                '<p><a href="',
                chpage["charpage"],
                '">',
                chpage["category"],
                "</a></p>",
            ]
            character_page_line = "".join(character_page_line)
            charpage_elements.append(character_page_line)
        charpage_elements.append("</div>")
        charpages = sep.join(charpage_elements)

        with open(chars_template_path) as f:
            chars_template = f.read()

        site_header_w, site_header_h = site.images[site.config.header_filename]

        n_string = chars_template.format(
            lang=site.config.language,
            site_style=site.config.site_style,
            header_line=chars_h1_line,
            meta_tags=meta_tags_ready,
            linkrels=link_rel,
            header=site.config.header_filename,
            headerw=site_header_w,
            headerh=site_header_h,
            header_alt=site.config.site_title,
            title_line=chars_title_line,
            top_site_nav=top_site_nav,
            chars=charpages,
            year=year,
            author=site.config.site_author,
            copyright_statement=site.copyright_statement,
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
            url="".join([site.config.base_url, out_name]),
        )

        logmesg = _("Writing {out_name}...").format(out_name=out_name)
        logging.debug(logmesg)
        with open(out_file, "w", encoding="utf-8") as fout:
            fout.write(n_string)
        modified_time = datetime.datetime.strftime(
            datetime.datetime.utcfromtimestamp(os.path.getmtime(out_file)),
            "%Y-%m-%dT%H:%M:%S.%fZ",
        )
        sitemap_loc = {
            "loc": "".join([site.config.base_url, out_name]),
            "lastmod": modified_time,
        }
        site.sitemap.append(sitemap_loc)
    return tasks
