# pylint disable=protected-access

import pytest
from mockito import mock, never, verify, verifyZeroInteractions, when
from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Locator as SyncLocator
from playwright.sync_api import Page as SyncPage

from agentql import AttributeNotFoundError, QueryParser
from agentql.ext.playwright.async_api.response_proxy import (
    AQLResponseProxy as AsyncAQLResponseProxy,
)
from agentql.ext.playwright.sync_api.response_proxy import AQLResponseProxy as SyncAQLResponseProxy

RESPONSE = {
    "search_box": {
        "role": "combobox",
        "name": "Search",
        "tf623_id": "APjFqb",
    },
    "search_btn": {
        "role": "button",
        "name": "Google Search",
        "tf623_id": "tf_194",
    },
    "footer": {
        "about": {
            "role": "link",
            "name": "About",
            "tf623_id": "tf_22",
        }
    },
    "alert": None,
}

RESPONSE_WITH_NESTED_LIST_TERMS = {
    "products": [
        {
            "name": {
                "role": "generic",
                "name": "TinyFish Sweatshirt",
                "tf623_id": "node_1",
            },
            "price": {
                "role": "generic",
                "name": "$10",
                "tf623_id": "node_2",
            },
            "reviews": [
                {
                    "role": "generic",
                    "name": "Good",
                    "tf623_id": "node_3",
                },
                {
                    "role": "generic",
                    "name": "Good",
                    "tf623_id": "node_4",
                },
            ],
        },
        {
            "name": {
                "role": "generic",
                "name": "TinyFish T-Shirt",
                "tf623_id": "node_5",
            },
            "price": {
                "role": "generic",
                "name": "$5",
                "tf623_id": "node_6",
            },
            "reviews": [
                {
                    "role": "generic",
                    "name": "Bad",
                    "tf623_id": "node_7",
                },
                {
                    "role": "generic",
                    "name": "Bad",
                    "tf623_id": "node_8",
                },
            ],
        },
    ]
}


def test_clickable_node_btn():
    """Test that the click method is present on the button node"""
    mock_locator = mock(SyncLocator, strict=False)
    mock_page = mock(SyncPage, strict=False)
    when(mock_page).locator(f"[tf623_id='{RESPONSE['search_btn']['tf623_id']}']").thenReturn(mock_locator)
    query = """
    {
        search_btn
    }
    """
    query_tree = QueryParser(query).parse()

    node = SyncAQLResponseProxy(RESPONSE, mock_page, query_tree)
    node.search_btn.click()
    verify(mock_locator, times=1).click()


def test_non_leaf_node():
    """Test if non-interactive node (hierarchy node) is properly handled"""
    mock_locator = mock(SyncLocator, strict=False)
    mock_page = mock(SyncPage, strict=False)
    query = """
    {
        footer {
            about
        }
    }
    """
    query_tree = QueryParser(query).parse()

    node = SyncAQLResponseProxy(RESPONSE, mock_page, query_tree)

    item = node.footer
    assert isinstance(item, SyncAQLResponseProxy)

    verify(mock_page, never).locator(any)
    verifyZeroInteractions(mock_locator)

    item = node.footer.about
    verify(mock_page, times=1).locator(f"[tf623_id='{RESPONSE['footer']['about']['tf623_id']}']")


def test_input_node_combobox():
    """Test that the input method is present on the combobox node"""
    mock_locator = mock(SyncLocator, strict=False)
    mock_page = mock(SyncPage, strict=False)
    when(mock_page).locator(f"[tf623_id='{RESPONSE['search_box']['tf623_id']}']").thenReturn(mock_locator)
    query = """
    {
        search_box
    }
    """
    query_tree = QueryParser(query).parse()

    node = SyncAQLResponseProxy(RESPONSE, mock_page, query_tree)
    node.search_box.fill("tinyfish")
    verify(mock_locator, times=1).fill("tinyfish")


def test_nested_list_terms_nodes():
    """Test that the response with nested lists is handled properly."""
    mock_locator = mock(SyncLocator, strict=False)
    mock_page = mock(SyncPage, strict=False)
    query = """
    {
        products[] {
            name
            price
            reviews[]
        }
    }
    """
    query_tree = QueryParser(query).parse()
    when(mock_page).locator(...).thenReturn(mock_locator)

    node = SyncAQLResponseProxy(RESPONSE_WITH_NESTED_LIST_TERMS, mock_page, query_tree)
    assert isinstance(node.products, SyncAQLResponseProxy)
    assert len(node.products) == 2
    for item in node.products:
        assert isinstance(item, SyncAQLResponseProxy)
        assert isinstance(item.name, SyncLocator)
        assert isinstance(item.price, SyncLocator)
        assert isinstance(item.reviews, SyncAQLResponseProxy)
        assert isinstance(item.reviews[0], SyncLocator)
        assert len(item.reviews) == 2


def test_typo_in_response_node():
    """We should properly flag there is a typo"""
    web_driver_mock = mock()
    query = """
    {
        search_box
        search_btn
        footer {
            about
        }
        alert
    }
    """
    query_tree = QueryParser(query).parse()

    node = SyncAQLResponseProxy(RESPONSE, web_driver_mock, query_tree)

    with pytest.raises(AttributeNotFoundError):
        node.alert2.click()


def test_interact_with_non_leaf():
    """Properly flag when trying to interact with non-leaf node"""
    mock_page = mock(SyncPage, strict=False)
    query = """
    {
        footer {
            about
        }
    }
    """
    query_tree = QueryParser(query).parse()

    node = SyncAQLResponseProxy(RESPONSE, mock_page, query_tree)

    with pytest.raises(AttributeNotFoundError):
        node.footer.click()


def test_node_with_none_value():
    """Test that the response with a None value is handled properly."""
    mock_page = mock(SyncPage, strict=False)
    query = """
    {
        alert
    }
    """
    query_tree = QueryParser(query).parse()
    node = SyncAQLResponseProxy(RESPONSE, mock_page, query_tree)
    assert node.alert is None


TO_DATA_RESPONSE_TEST_CASES = [
    {
        "query": "{sign_in_btn}",
        "response_data": {"sign_in_btn": {"role": "button", "name": "Sign In"}},
        "expected": {"sign_in_btn": "Sign In"},
    },
    {
        "query": "{header {search_box}}",
        "response_data": {"header": {"search_box": {"role": "button", "name": "Search Box"}}},
        "expected": {"header": {"search_box": "Search Box"}},
    },
    {
        "query": "{product {name price}}",
        "response_data": {
            "product": {
                "name": {"role": "button", "name": "Some Product"},
                "price": {"role": "link", "name": "$1"},
            }
        },
        "expected": {"product": {"name": "Some Product", "price": "$1"}},
    },
    {
        "query": "{comments[]}",
        "response_data": {"comments": [{"role": "button", "name": "Some Comment"}]},
        "expected": {"comments": ["Some Comment"]},
    },
    {
        "query": "{search_btn}",
        "response_data": {"search_btn": None},
        "expected": {"search_btn": None},
    },
    {
        "query": "{search_btn search_box}",
        "response_data": {"search_btn": {"role": "button", "name": "Search"}},
        "expected": {"search_btn": "Search"},
    },
    {
        "query": "{search_btn}",
        "response_data": {"search_btn": {"role": "button", "tf623_id": "94"}},
        "expected": {"search_btn": None},
    },
    {
        "query": "{comments[]}",
        "response_data": {"comments": [{"role": "button", "tf623_id": "94"}]},
        "expected": {"comments": []},
    },
]


@pytest.mark.parametrize("asset", TO_DATA_RESPONSE_TEST_CASES)
def test_to_data(asset):
    """Test that the to_data method returns the expected data."""
    mock_page = mock(SyncPage, strict=False)
    query_tree = QueryParser(asset["query"]).parse()
    node = SyncAQLResponseProxy(asset["response_data"], mock_page, query_tree)
    assert node.to_data() == asset["expected"]


@pytest.mark.parametrize("asset", TO_DATA_RESPONSE_TEST_CASES)
@pytest.mark.asyncio
async def test_to_data_async(asset):
    """Test that the to_data method returns the expected data."""
    mock_page = mock(AsyncPage, strict=False)
    query_tree = QueryParser(asset["query"]).parse()
    node = AsyncAQLResponseProxy(asset["response_data"], mock_page, query_tree)
    assert await node.to_data() == asset["expected"]


TO_DATA_RESPONSE_TEST_FALLBACK_CASES = [
    {
        "query": "{sign_in_btn}",
        "response_data": {"sign_in_btn": {"tf623_id": "1", "role": "button", "name": "Fallback Text Content"}},
        "expected": {"sign_in_btn": "Fallback Text Content"},
    },
]


@pytest.mark.parametrize("asset", TO_DATA_RESPONSE_TEST_FALLBACK_CASES)
def test_to_data_fallback(asset):
    """Test that the to_data method returns the expected data."""
    mock_page = mock(SyncPage, strict=False)
    query_tree = QueryParser(asset["query"]).parse()
    node = SyncAQLResponseProxy(asset["response_data"], mock_page, query_tree)
    assert node.to_data() == asset["expected"]


# Helper coroutine to simulate async return
async def _async_return(value: str) -> str:
    return value


@pytest.mark.parametrize("asset", TO_DATA_RESPONSE_TEST_FALLBACK_CASES)
@pytest.mark.asyncio
async def test_to_data_async_fallback(asset):
    """Test that the to_data method returns the expected data."""
    mock_page = mock(SyncPage, strict=False)
    query_tree = QueryParser(asset["query"]).parse()
    node = AsyncAQLResponseProxy(asset["response_data"], mock_page, query_tree)
    assert await node.to_data() == asset["expected"]
