from __future__ import annotations


from bs4 import BeautifulSoup


class MainContentFinder:
    """
    Finds the main content block of a page.

    Strategy:
    1. Try known CSS selectors (main, article, #content, etc.)
    2. Fall back to scoring all div/section/article/main blocks by text length
    3. Fall back to body
    """

    _DEFAULT_SELECTORS = [
        "main",
        "article",
        "#content",
        "#main-content",
        "div.wrapper",
        "div.content",
        "div#main",
        "div.main-content",
        "section.main-content",
        "div.article-body",
    ]
    _DEFAULT_BLOCKS = ["div", "section", "article", "main"]

    def __init__(
        self,
        override: bool = False,
        add_selectors: list[str] | None = None,
        remove_selectors: list[str] | None = None,
        add_blocks: list[str] | None = None,
        remove_blocks: list[str] | None = None,
        clear_selectors: bool = False,
    ):
        self.override = override
        base_selectors = [] if clear_selectors else list(self._DEFAULT_SELECTORS)
        self.selectors = self._build_list(base_selectors, add_selectors, remove_selectors)
        self.blocks = self._build_list(list(self._DEFAULT_BLOCKS), add_blocks, remove_blocks)

    def _build_list(
        self, base: list[str], add: list[str] | None, remove: list[str] | None
    ) -> list[str]:
        if not self.override:
            return base
        result = list(base)
        if add:
            result.extend(item for item in add if item not in result)
        if remove:
            result = [item for item in result if item not in remove]
        return result or base

    def find_main_content(self, soup: BeautifulSoup) -> BeautifulSoup:
        selected = []
        for selector in self.selectors:
            for item in soup.select(selector):
                selected.append(item)
                item.extract()

        if selected:
            combined = "".join(str(el) for el in selected)
            return BeautifulSoup(combined, "lxml")

        return self._score_blocks(soup)

    def _score_blocks(self, soup: BeautifulSoup) -> BeautifulSoup:
        blocks = soup.find_all(self.blocks)
        if not blocks:
            return soup.body or soup

        best = max(blocks, key=lambda b: len(b.get_text(strip=True)))
        return BeautifulSoup(str(best), "lxml")
