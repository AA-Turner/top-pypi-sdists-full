from bs4 import BeautifulSoup
from typing import Any, Dict, List, Optional
import requests
from .get_ua import *



def get_source_code(url: str, session: Optional[requests.Session] = None) -> str:
    session = session or get_session(url)
    return fetch_html(url=url, session=session)


def get_soup(url: str, session: Optional[requests.Session] = None) -> BeautifulSoup:
    source_code = get_source_code(url, session=session)
    return BeautifulSoup(source_code, "html.parser")


def get_soup_text(url: str, session: Optional[requests.Session] = None) -> str:
    source_soup = get_soup(url, session=session)
    return source_soup.get_text(separator="\n", strip=True)


def get_meta_tags_from_soup(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """
    Return every <meta> tag as a dictionary.

    Example output:
    [
        {"name": "description", "content": "..."},
        {"property": "og:title", "content": "..."},
        {"charset": "utf-8"}
    ]
    """
    return [dict(tag.attrs) for tag in soup.find_all("meta")]

def get_meta_tags_from_url(url,session: Optional[requests.Session] = None) -> Dict[str, str]:
    soup = get_soup(url=url, session=session)
    return get_meta_tags_from_soup(soup)
def get_meta_map_from_soup(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Return useful meta tags keyed by name/property/http-equiv/charset.

    Example:
    {
        "description": "...",
        "og:title": "...",
        "twitter:card": "...",
        "charset": "utf-8"
    }
    """
    meta_map = {}

    for tag in soup.find_all("meta"):
        attrs = dict(tag.attrs)

        key = (
            attrs.get("name")
            or attrs.get("property")
            or attrs.get("http-equiv")
            or attrs.get("charset")
        )

        if not key:
            continue

        if "content" in attrs:
            meta_map[str(key)] = attrs["content"]
        else:
            meta_map[str(key)] = ""

    return meta_map

def get_meta_map_from_url(url,session: Optional[requests.Session] = None) -> Dict[str, str]:
    soup = get_soup(url=url, session=session)
    return get_meta_map_from_soup(soup)
def get_body_from_soup(soup: BeautifulSoup, as_text: bool = False) -> str:
    body = soup.body

    if body is None:
        return ""

    if as_text:
        return body.get_text(separator="\n", strip=True)

    return str(body)
def get_body_from_url(url,session: Optional[requests.Session] = None) -> Dict[str, str]:
    soup = get_soup(url=url, session=session)
    return get_body_from_soup(soup)

def get_title_from_soup(soup: BeautifulSoup) -> str:
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return ""
def get_title_from_url(url,session: Optional[requests.Session] = None) -> Dict[str, str]:
    soup = get_soup(url=url, session=session)
    return get_title_from_soup(soup)

def get_desired_content_from_soup(
    soup: BeautifulSoup,
    selectors: Optional[List[str]] = None,
    remove_selectors: Optional[List[str]] = None,
    as_text: bool = True,
) -> Dict[str, Any]:
    """
    Pull useful page content.

    selectors lets you target desired areas:
        ["article", "main", ".content", "#post"]

    remove_selectors strips junk:
        ["script", "style", "nav", "footer", "header", "aside"]
    """

    remove_selectors = remove_selectors or [
        "script",
        "style",
        "noscript",
        "svg",
        "nav",
        "footer",
        "header",
        "aside",
        "form",
    ]

    for selector in remove_selectors:
        for tag in soup.select(selector):
            tag.decompose()

    selected_blocks = []

    if selectors:
        for selector in selectors:
            selected_blocks.extend(soup.select(selector))
    else:
        selected_blocks = (
            soup.select("article")
            or soup.select("main")
            or soup.select("[role='main']")
            or [soup.body]
        )

    content_parts = []

    for block in selected_blocks:
        if not block:
            continue

        if as_text:
            content_parts.append(block.get_text(separator="\n", strip=True))
        else:
            content_parts.append(str(block))

    return {
        "title": get_title_from_soup(soup),
        "meta": get_meta_map_from_soup(soup),
        "meta_tags": get_meta_tags_from_soup(soup),
        "content": "\n\n".join(part for part in content_parts if part),
    }

def get_desired_content_from_url(url,session: Optional[requests.Session] = None) -> Dict[str, str]:
    soup = get_soup(url=url, session=session)
    return get_desired_content_from_soup(soup)
def extract_page_content(
    url: str,
    session: Optional[requests.Session] = None,
    selectors: Optional[List[str]] = None,
    as_text: bool = True,
) -> Dict[str, Any]:
    soup = get_soup(url, session=session)

    return {
        "url": url,
        "title": get_title_from_soup(soup),
        "meta": get_meta_map_from_soup(soup),
        "meta_tags": get_meta_tags_from_soup(soup),
        "body": get_body_from_soup(soup, as_text=as_text),
        "desired": get_desired_content_from_soup(
            soup,
            selectors=selectors,
            as_text=as_text,
        ),
    }
