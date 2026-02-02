import re

from .utils import despace


def reduce_br(text: str) -> str:
    text = (
        text.replace("<br>", "<br/>")
        .replace("<p><br/>", "<p>")
        .replace("<br/></p>", "</p>")
    )
    text = re.sub(r"([^.>])<br/>([^(<br/>)])", r"\g<1> \g<2>", text)
    text = re.sub(r"(?:<br/>\s*)+([^(<br/>)])", r"<br/><br/>\g<1>", text)
    text = despace(text)
    return text


def remove_shit(soup):
    for script_tag in list(soup.select("script")):
        script_tag.unwrap()


def remove_chars(soup_str):
    soup_str = soup_str.replace("\ufeff", "").replace("\r\n", "\n")
    return soup_str


def canonize_tags(soup):
    for el in soup.find_all():
        if el.name == "span":
            el.unwrap()
        elif el.name == "em":
            el.name = "i"
        elif el.name == "italic":
            el.name = "i"
        elif el.name == "strong":
            el.name = "b"
        elif el.name == "sec":
            el.name = "section"
        elif el.name == "bold":
            el.name = "b"
        elif el.name == "p" and "ref" in el.attrs.get("class", []):
            el.name = "ref"
        elif el.name == "disp-formula":
            el.name = "formula"
    return soup
