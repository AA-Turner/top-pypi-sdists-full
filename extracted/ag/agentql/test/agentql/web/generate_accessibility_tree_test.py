import pytest
from playwright.sync_api import Page, sync_playwright

import agentql
from agentql.ext.playwright.sync_api._utils_sync import get_accessibility_tree


@pytest.fixture
def page():
    with sync_playwright() as playwright, playwright.chromium.launch(headless=True) as browser:
        page = agentql.wrap(browser.new_page())
        yield page


def test_iframe_accessibility_tree_generation(page: Page):
    """
    Test to ensure that accessibility tree generation works for iframes.
    """
    html = """
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Nested Iframes Example</title>
        </head>
        <body>
            <h1>Main Page</h1>
            <iframe id="iframe1" srcdoc="
                <!DOCTYPE html>
                <html>
                <body>
                    <h2>First Level Iframe</h2>
                    <iframe id='iframe2' srcdoc='
                        <!DOCTYPE html>
                        <html>
                        <body>
                            <input/>
                            <h3>Iframe 1: Second Level Iframe </h3>
                            <div>Target Element</div>
                        </body>
                        </html>
                    '></iframe>
                </body>
                </html>
            "></iframe>
        </body>
        </html>
    """
    expected_accessibility_tree = {
        "role": "webArea",
        "name": "Nested Iframes Example",
        "attributes": {"html_tag": "title", "tf623_id": "1"},
        "children": [
            {
                "role": "generic",
                "name": "",
                "attributes": {"html_tag": "html", "lang": "en", "tf623_id": "2"},
                "children": [
                    {
                        "role": "document",
                        "name": "",
                        "attributes": {"html_tag": "body", "tf623_id": "3"},
                        "children": [
                            {
                                "role": "heading",
                                "name": "Main Page",
                                "attributes": {"html_tag": "h1", "tf623_id": "4"},
                            },
                            {
                                "role": "generic",
                                "name": "",
                                "attributes": {
                                    "html_tag": "iframe",
                                    "id": "iframe1",
                                    "tf623_id": "5",
                                },
                                "children": [
                                    {
                                        "role": "generic",
                                        "name": "",
                                        "attributes": {
                                            "html_tag": "html",
                                            "iframe_path": "5",
                                            "tf623_id": "6",
                                        },
                                        "children": [
                                            {
                                                "role": "document",
                                                "name": "",
                                                "attributes": {
                                                    "html_tag": "body",
                                                    "iframe_path": "5",
                                                    "tf623_id": "7",
                                                },
                                                "children": [
                                                    {
                                                        "role": "heading",
                                                        "name": "First Level Iframe",
                                                        "attributes": {
                                                            "html_tag": "h2",
                                                            "iframe_path": "5",
                                                            "tf623_id": "8",
                                                        },
                                                    },
                                                    {
                                                        "role": "generic",
                                                        "name": "",
                                                        "attributes": {
                                                            "html_tag": "iframe",
                                                            "id": "iframe2",
                                                            "iframe_path": "5",
                                                            "tf623_id": "9",
                                                        },
                                                        "children": [
                                                            {
                                                                "role": "generic",
                                                                "name": "",
                                                                "attributes": {
                                                                    "html_tag": "html",
                                                                    "iframe_path": "5.9",
                                                                    "tf623_id": "10",
                                                                },
                                                                "children": [
                                                                    {
                                                                        "role": "document",
                                                                        "name": "",
                                                                        "attributes": {
                                                                            "html_tag": "body",
                                                                            "iframe_path": "5.9",
                                                                            "tf623_id": "11",
                                                                        },
                                                                        "children": [
                                                                            {
                                                                                "role": "textbox",
                                                                                "name": "",
                                                                                "attributes": {
                                                                                    "html_tag": "input",
                                                                                    "iframe_path": "5.9",
                                                                                    "tf623_id": "12",
                                                                                },
                                                                            },
                                                                            {
                                                                                "role": "heading",
                                                                                "name": "Iframe 1: Second Level Iframe ",
                                                                                "attributes": {
                                                                                    "html_tag": "h3",
                                                                                    "iframe_path": "5.9",
                                                                                    "tf623_id": "13",
                                                                                },
                                                                            },
                                                                            {
                                                                                "role": "text",
                                                                                "name": "Target Element",
                                                                                "attributes": {
                                                                                    "html_tag": "div",
                                                                                    "iframe_path": "5.9",
                                                                                    "tf623_id": "14",
                                                                                },
                                                                            },
                                                                        ],
                                                                    }
                                                                ],
                                                            }
                                                        ],
                                                    },
                                                ],
                                            }
                                        ],
                                    }
                                ],
                            },
                        ],
                    }
                ],
            }
        ],
    }

    page.set_content(html)

    accessibility_tree = get_accessibility_tree(page, include_hidden=False)

    assert accessibility_tree == expected_accessibility_tree


def test_name_trimming(page: Page):
    html = """
    <html>
        <head/>
        <body>
            <div id="test">
                Text before link <a href="https://example.com">Example Link</a> Text after link
            </div>
        </body>
    </html>
    """

    expected_accessibility_tree = {
        "role": "generic",
        "name": "",
        "attributes": {"html_tag": "html", "tf623_id": "1"},
        "children": [
            {
                "role": "document",
                "name": "",
                "attributes": {"html_tag": "body", "tf623_id": "2"},
                "children": [
                    {
                        "role": "generic",
                        "name": "",
                        "attributes": {"html_tag": "div", "id": "test", "tf623_id": "3"},
                        "children": [
                            {
                                "role": "text",
                                "name": " Text before link ",
                                "attributes": {"html_tag": "span", "tf623_id": "4"},
                            },
                            {
                                "role": "link",
                                "name": "Example Link",
                                "attributes": {
                                    "html_tag": "a",
                                    "href": "https://example.com",
                                    "tf623_id": "5",
                                },
                            },
                            {
                                "role": "text",
                                "name": " Text after link ",
                                "attributes": {"html_tag": "span", "tf623_id": "6"},
                            },
                        ],
                    }
                ],
            }
        ],
    }
    page.set_content(html)
    accessibility_tree = get_accessibility_tree(page, include_hidden=False)
    assert accessibility_tree == expected_accessibility_tree


def test_iframe_no_document_accessibility_tree_generation(page: Page):
    """
    Test to ensure that accessibility tree generation can handle iframes without document.
    """
    html = """
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Iframe Without Document Example</title>
        </head>
        <body>
            <h1>Main Page</h1>
            <iframe></iframe>
        </body>
        </html>
    """

    expected_accessibility_tree = {
        "role": "webArea",
        "name": "Iframe Without Document Example",
        "attributes": {"html_tag": "title", "tf623_id": "1"},
        "children": [
            {
                "role": "generic",
                "name": "",
                "attributes": {"html_tag": "html", "lang": "en", "tf623_id": "2"},
                "children": [
                    {
                        "role": "document",
                        "name": "",
                        "attributes": {"html_tag": "body", "tf623_id": "3"},
                        "children": [
                            {
                                "role": "heading",
                                "name": "Main Page",
                                "attributes": {"html_tag": "h1", "tf623_id": "4"},
                            },
                            {
                                "role": "generic",
                                "name": "",
                                "attributes": {"html_tag": "iframe", "tf623_id": "5"},
                            },
                        ],
                    }
                ],
            }
        ],
    }

    page.set_content(html)

    accessibility_tree = get_accessibility_tree(page, include_hidden=False)

    assert accessibility_tree == expected_accessibility_tree


def test_simple_shadow_dom_accessibility_tree_generation(page: Page):
    """
    Test to ensure that accessibility tree generation works for a simple shadow DOM.
    """
    html = """
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Shadow DOM Example</title>
        </head>
        <body>
            <h1>Main Page</h1>
            <div id="shadow-host"></div>
            <script>
                const shadowHost = document.getElementById('shadow-host');
                const shadowRoot = shadowHost.attachShadow({mode: 'open'});
                shadowRoot.innerHTML = `
                    <div id="shadow-div">
                        <h2>Shadow DOM</h2>
                        <input/>
                        <div>Target Element</div>
                    </div>
                `;
            </script>
        </body>
        </html>
    """
    expected_accessibility_tree = {
        "role": "webArea",
        "name": "Shadow DOM Example",
        "attributes": {"html_tag": "title", "tf623_id": "1"},
        "children": [
            {
                "role": "generic",
                "name": "",
                "attributes": {"html_tag": "html", "lang": "en", "tf623_id": "2"},
                "children": [
                    {
                        "role": "document",
                        "name": "",
                        "attributes": {"html_tag": "body", "tf623_id": "3"},
                        "children": [
                            {
                                "role": "heading",
                                "name": "Main Page",
                                "attributes": {"html_tag": "h1", "tf623_id": "4"},
                            },
                            {
                                "role": "generic",
                                "name": "",
                                "attributes": {
                                    "html_tag": "div",
                                    "id": "shadow-host",
                                    "tf623_id": "5",
                                },
                                "children": [
                                    {
                                        "role": "generic",
                                        "name": "",
                                        "attributes": {
                                            "html_tag": "div",
                                            "id": "shadow-div",
                                            "tf623_id": "6",
                                        },
                                        "children": [
                                            {
                                                "role": "heading",
                                                "name": "Shadow DOM",
                                                "attributes": {"html_tag": "h2", "tf623_id": "7"},
                                            },
                                            {
                                                "role": "textbox",
                                                "name": "",
                                                "attributes": {
                                                    "html_tag": "input",
                                                    "tf623_id": "8",
                                                },
                                            },
                                            {
                                                "role": "text",
                                                "name": "Target Element",
                                                "attributes": {"html_tag": "div", "tf623_id": "9"},
                                            },
                                        ],
                                    }
                                ],
                            },
                        ],
                    }
                ],
            }
        ],
    }

    page.set_content(html)

    accessibility_tree = get_accessibility_tree(page, include_hidden=False)

    assert accessibility_tree == expected_accessibility_tree


def test_slot_tag_in_custom_tag_elements_accessibility_tree_generation(page: Page):
    """
    Test to ensure that accessibility tree generation works for custom elements with slot tags.
    """
    html = """
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Custom Elements Slot Tag Example</title>
        </head>
        <body>
            <h1>Main Page</h1>
            <custom-element>
                <div slot="slot1">Slot 1</div>
                <div slot="slot2">Slot 2</div>
            </custom-element>
            <script>
                class CustomElement extends HTMLElement {
                    constructor() {
                        super();
                        const shadowRoot = this.attachShadow({mode: 'open'});
                        shadowRoot.innerHTML = `
                            <div id="shadow-div">
                                <h2>Shadow DOM</h2>
                                <slot name="slot1"></slot>
                                <slot name="slot2"></slot>
                            </div>
                        `;
                    }
                }
                customElements.define('custom-element', CustomElement);
            </script>
        </body>
        </html>
    """
    expected_accessibility_tree = {
        "role": "webArea",
        "name": "Custom Elements Slot Tag Example",
        "attributes": {"html_tag": "title", "tf623_id": "1"},
        "children": [
            {
                "role": "generic",
                "name": "",
                "attributes": {"html_tag": "html", "lang": "en", "tf623_id": "2"},
                "children": [
                    {
                        "role": "document",
                        "name": "",
                        "attributes": {"html_tag": "body", "tf623_id": "3"},
                        "children": [
                            {
                                "role": "heading",
                                "name": "Main Page",
                                "attributes": {"html_tag": "h1", "tf623_id": "4"},
                            },
                            {
                                "role": "generic",
                                "name": "",
                                "attributes": {"html_tag": "custom-element", "tf623_id": "5"},
                                "children": [
                                    {
                                        "role": "generic",
                                        "name": "",
                                        "attributes": {
                                            "html_tag": "div",
                                            "id": "shadow-div",
                                            "tf623_id": "6",
                                        },
                                        "children": [
                                            {
                                                "role": "heading",
                                                "name": "Shadow DOM",
                                                "attributes": {"html_tag": "h2", "tf623_id": "7"},
                                            },
                                            {
                                                "role": "generic",
                                                "name": "slot1",
                                                "attributes": {
                                                    "html_tag": "slot",
                                                    "name": "slot1",
                                                    "tf623_id": "8",
                                                },
                                                "children": [
                                                    {
                                                        "role": "text",
                                                        "name": "Slot 1",
                                                        "attributes": {
                                                            "html_tag": "div",
                                                            "slot": "slot1",
                                                            "tf623_id": "9",
                                                        },
                                                    }
                                                ],
                                            },
                                            {
                                                "role": "generic",
                                                "name": "slot2",
                                                "attributes": {
                                                    "html_tag": "slot",
                                                    "name": "slot2",
                                                    "tf623_id": "10",
                                                },
                                                "children": [
                                                    {
                                                        "role": "text",
                                                        "name": "Slot 2",
                                                        "attributes": {
                                                            "html_tag": "div",
                                                            "slot": "slot2",
                                                            "tf623_id": "11",
                                                        },
                                                    }
                                                ],
                                            },
                                        ],
                                    }
                                ],
                            },
                        ],
                    }
                ],
            }
        ],
    }

    page.set_content(html)

    accessibility_tree = get_accessibility_tree(page, include_hidden=False)

    assert accessibility_tree == expected_accessibility_tree


def test_id_the_same_with_multiple_accessibility_tree_generation_for_the_same_page(page: Page):
    """
    Test to ensure that id stay the same for the same elements across multiple accessibility tree generation
    """
    html = """
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Id Generation Example</title>
        </head>
        <body>
            <h1>Heading 1</h1>
            <p>Paragraph</p>
            <textarea placeholder="Search here"></textarea>
            <div id="test">
                <button onclick="addNewElement()">Add element</button>
                <script>
                    function addNewElement() {
                        var newElem = document.createElement('div');
                        newElem.textContent = 'New Element';
                        for (var i = 0; i < 3; i++) {
                            var newChildren = document.createElement('div');
                            newChildren.textContent = 'New Children';
                            newElem.appendChild(newChildren);
                        }
                        document.querySelector('#test').appendChild(newElem);
                    }
                </script>
            </div>
        </body>
        </html>
    """

    expected_accessibility_tree = {
        "role": "webArea",
        "name": "Id Generation Example",
        "attributes": {"html_tag": "title", "tf623_id": "1"},
        "children": [
            {
                "role": "generic",
                "name": "",
                "attributes": {"html_tag": "html", "lang": "en", "tf623_id": "2"},
                "children": [
                    {
                        "role": "document",
                        "name": "",
                        "attributes": {"html_tag": "body", "tf623_id": "3"},
                        "children": [
                            {
                                "role": "heading",
                                "name": "Heading 1",
                                "attributes": {"html_tag": "h1", "tf623_id": "4"},
                            },
                            {
                                "role": "text",
                                "name": "Paragraph",
                                "attributes": {"html_tag": "p", "tf623_id": "5"},
                            },
                            {
                                "role": "textbox",
                                "name": "Search here",
                                "attributes": {
                                    "html_tag": "textarea",
                                    "placeholder": "Search here",
                                    "tf623_id": "6",
                                },
                            },
                            {
                                "role": "generic",
                                "name": "",
                                "attributes": {"html_tag": "div", "id": "test", "tf623_id": "7"},
                                "children": [
                                    {
                                        "role": "button",
                                        "name": "Add element",
                                        "attributes": {
                                            "html_tag": "button",
                                            "onclick": "addNewElement()",
                                            "tf623_id": "8",
                                        },
                                    }
                                ],
                            },
                        ],
                    }
                ],
            }
        ],
    }

    expected_accessibility_tree_after_new_element = {
        "role": "webArea",
        "name": "Id Generation Example",
        "attributes": {"html_tag": "title", "tf623_id": "1"},
        "children": [
            {
                "role": "generic",
                "name": "",
                "attributes": {"html_tag": "html", "lang": "en", "tf623_id": "2"},
                "children": [
                    {
                        "role": "document",
                        "name": "",
                        "attributes": {"html_tag": "body", "tf623_id": "3"},
                        "children": [
                            {
                                "role": "heading",
                                "name": "Heading 1",
                                "attributes": {"html_tag": "h1", "tf623_id": "4"},
                            },
                            {
                                "role": "text",
                                "name": "Paragraph",
                                "attributes": {"html_tag": "p", "tf623_id": "5"},
                            },
                            {
                                "role": "textbox",
                                "name": "Search here",
                                "attributes": {
                                    "html_tag": "textarea",
                                    "placeholder": "Search here",
                                    "tf623_id": "6",
                                },
                            },
                            {
                                "role": "generic",
                                "name": "",
                                "attributes": {"html_tag": "div", "id": "test", "tf623_id": "7"},
                                "children": [
                                    {
                                        "role": "button",
                                        "name": "Add element",
                                        "attributes": {
                                            "html_tag": "button",
                                            "onclick": "addNewElement()",
                                            "tf623_id": "8",
                                        },
                                    },
                                    {
                                        "role": "generic",
                                        "name": "",
                                        "attributes": {"html_tag": "div", "tf623_id": "9"},
                                        "children": [
                                            {
                                                "role": "text",
                                                "name": "New Element",
                                                "attributes": {
                                                    "html_tag": "span",
                                                    "tf623_id": "10",
                                                },
                                            },
                                            {
                                                "role": "text",
                                                "name": "New Children",
                                                "attributes": {
                                                    "html_tag": "div",
                                                    "tf623_id": "11",
                                                },
                                            },
                                            {
                                                "role": "text",
                                                "name": "New Children",
                                                "attributes": {
                                                    "html_tag": "div",
                                                    "tf623_id": "12",
                                                },
                                            },
                                            {
                                                "role": "text",
                                                "name": "New Children",
                                                "attributes": {
                                                    "html_tag": "div",
                                                    "tf623_id": "13",
                                                },
                                            },
                                        ],
                                    },
                                ],
                            },
                        ],
                    }
                ],
            }
        ],
    }

    page.set_content(html)

    accessibility_tree = get_accessibility_tree(page, include_hidden=True)
    assert accessibility_tree == expected_accessibility_tree

    # Trigger the button click to add a new element
    button = page.locator("button")
    button.click()

    accessibility_tree = get_accessibility_tree(page, include_hidden=True)
    assert accessibility_tree == expected_accessibility_tree_after_new_element


def test_accessibility_tree_with_aria_hidden_included(page: Page):
    """
    Test to ensure that accessibility tree generation works for elements with aria-hidden attribute if aria-hidden is included.
    """
    html = """
    <html>
        <head/>
        <body>
            <div id="test" aria-hidden="true">
                <button>Test</button>
                <input type="text" />
            </div>
        </body>
    </html>
        """

    expected_accessibility_tree = {
        "role": "generic",
        "name": "",
        "attributes": {"html_tag": "html", "tf623_id": "1"},
        "children": [
            {
                "role": "document",
                "name": "",
                "attributes": {"html_tag": "body", "tf623_id": "2"},
                "children": [
                    {
                        "role": "generic",
                        "name": "",
                        "attributes": {
                            "html_tag": "div",
                            "id": "test",
                            "aria-hidden": "true",
                            "tf623_id": "3",
                        },
                        "children": [
                            {
                                "role": "button",
                                "name": "Test",
                                "attributes": {"html_tag": "button", "tf623_id": "4"},
                            },
                            {
                                "role": "textbox",
                                "name": "",
                                "attributes": {
                                    "html_tag": "input",
                                    "tf623_id": "5",
                                    "type": "text",
                                },
                            },
                        ],
                    },
                ],
            },
        ],
    }

    page.set_content(html)

    accessibility_tree = get_accessibility_tree(page, include_hidden=True)

    assert accessibility_tree == expected_accessibility_tree


def test_accessibility_tree_parent_with_name_keeps_child(page: Page):
    """
    Test to ensure that accessibility tree generation works for parents of text children with useful attributes
    """
    html = """
    <html>
        <head/>
        <body>
            <div id="test">
                <span aria-label="useful">Test</span>
                <input type="text" />
            </div>
        </body>
    </html>
        """

    expected_accessibility_tree = {
        "role": "generic",
        "name": "",
        "attributes": {"html_tag": "html", "tf623_id": "1"},
        "children": [
            {
                "role": "document",
                "name": "",
                "attributes": {"html_tag": "body", "tf623_id": "2"},
                "children": [
                    {
                        "role": "generic",
                        "name": "",
                        "attributes": {
                            "html_tag": "div",
                            "id": "test",
                            "tf623_id": "3",
                        },
                        "children": [
                            {
                                "role": "text",
                                "name": "useful",
                                "attributes": {
                                    "html_tag": "span",
                                    "tf623_id": "4",
                                    "aria-label": "useful",
                                },
                                "children": [
                                    {
                                        "attributes": {
                                            "html_tag": "span",
                                            "tf623_id": "5",
                                        },
                                        "name": "Test",
                                        "role": "text",
                                    },
                                ],
                            },
                            {
                                "role": "textbox",
                                "name": "",
                                "attributes": {
                                    "html_tag": "input",
                                    "tf623_id": "6",
                                    "type": "text",
                                },
                            },
                        ],
                    },
                ],
            },
        ],
    }

    page.set_content(html)

    accessibility_tree = get_accessibility_tree(page, include_hidden=True)

    assert accessibility_tree == expected_accessibility_tree


def test_accessibility_tree_parent_no_name_dumps_child(page: Page):
    """
    Test to ensure that accessibility tree generation merges parent and child if parent has no useful attributes and children is text
    """
    html = """
    <html>
        <head/>
        <body>
            <div id="test">
                <span>Test</span>
                <input type="text" />
            </div>
        </body>
    </html>
        """

    expected_accessibility_tree = {
        "role": "generic",
        "name": "",
        "attributes": {"html_tag": "html", "tf623_id": "1"},
        "children": [
            {
                "role": "document",
                "name": "",
                "attributes": {"html_tag": "body", "tf623_id": "2"},
                "children": [
                    {
                        "role": "generic",
                        "name": "",
                        "attributes": {
                            "html_tag": "div",
                            "id": "test",
                            "tf623_id": "3",
                        },
                        "children": [
                            {
                                "role": "text",
                                "name": "Test",
                                "attributes": {"html_tag": "span", "tf623_id": "4"},
                            },
                            {
                                "role": "textbox",
                                "name": "",
                                "attributes": {
                                    "html_tag": "input",
                                    "tf623_id": "5",
                                    "type": "text",
                                },
                            },
                        ],
                    },
                ],
            },
        ],
    }

    page.set_content(html)

    accessibility_tree = get_accessibility_tree(page, include_hidden=True)

    assert accessibility_tree == expected_accessibility_tree


def test_accessibility_tree_parent_with_multiple_children_text_spans(page: Page):
    """
    Test to ensure that accessibility tree generation for parent containing multiple child text elements is processed correctly.
    """
    html = """
    <html>
        <head/>
        <body>
            <div id="test">
                <span>Test<b>Many</b><i>Text</i></span>
                <input type="text" />
            </div>
        </body>
    </html>
        """

    expected_accessibility_tree = {
        "role": "generic",
        "name": "",
        "attributes": {"html_tag": "html", "tf623_id": "1"},
        "children": [
            {
                "role": "document",
                "name": "",
                "attributes": {"html_tag": "body", "tf623_id": "2"},
                "children": [
                    {
                        "role": "generic",
                        "name": "",
                        "attributes": {
                            "html_tag": "div",
                            "id": "test",
                            "tf623_id": "3",
                        },
                        "children": [
                            {
                                "role": "text",
                                "attributes": {"html_tag": "span", "tf623_id": "4"},
                                "name": "",
                                "children": [
                                    {
                                        "attributes": {
                                            "html_tag": "span",
                                            "tf623_id": "5",
                                        },
                                        "name": "Test",
                                        "role": "text",
                                    },
                                    {
                                        "attributes": {
                                            "html_tag": "b",
                                            "tf623_id": "6",
                                        },
                                        "name": "Many",
                                        "role": "text",
                                    },
                                    {
                                        "attributes": {
                                            "html_tag": "i",
                                            "tf623_id": "7",
                                        },
                                        "name": "Text",
                                        "role": "text",
                                    },
                                ],
                            },
                            {
                                "role": "textbox",
                                "name": "",
                                "attributes": {
                                    "html_tag": "input",
                                    "tf623_id": "8",
                                    "type": "text",
                                },
                            },
                        ],
                    },
                ],
            },
        ],
    }

    page.set_content(html)

    accessibility_tree = get_accessibility_tree(page, include_hidden=True)

    assert accessibility_tree == expected_accessibility_tree


def test_accessibility_tree_with_aria_hidden_excluded(page: Page):
    """
    Test to ensure that accessibility tree generation works for elements with aria-hidden attribute if aria-hidden is excluded.
    """
    html = """
    <html>
        <head/>
        <body>
            <div id="test" aria-hidden="true">
                <button>Test</button>
                <input type="text" />
            </div>
        </body>
    </html>
        """

    expected_accessibility_tree = {
        "role": "generic",
        "name": "",
        "attributes": {"html_tag": "html", "tf623_id": "1"},
        "children": [
            {
                "role": "document",
                "name": "",
                "attributes": {"html_tag": "body", "tf623_id": "2"},
            },
        ],
    }

    page.set_content(html)

    accessibility_tree = get_accessibility_tree(page, include_hidden=False)

    assert accessibility_tree == expected_accessibility_tree
