import unittest
import os
from tavily import AsyncTavilyClient, MissingAPIKeyError, InvalidAPIKeyError
from urllib.parse import urlparse
import asyncio

from unit_tests import cases
class SearchTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.tavily_client = AsyncTavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    # Every single search result should have these properties
    def common_search_result_properties(self, result) -> None:
        self.assertIsInstance(result, dict)
        self.assertIn("title", result)
        self.assertIn("url", result)
        self.assertIn("content", result)
        self.assertIn("score", result)

    # General search results should have these properties
    def general_search_result_properties(self, result) -> None:
        self.common_search_result_properties(result)
        self.assertIn("raw_content", result)

    # News search results should have these properties
    def news_search_result_properties(self, result) -> None:
        self.common_search_result_properties(result)
        self.assertIn("published_date", result)

    # Topic-specific properties
    def topic_specific_properties(self, result, **params) -> None:
        if params.get("topic", "general") == "general":
            self.assertIn("raw_content", result)
        elif params.get("topic", "general") == "news":
            self.assertIn("published_date", result)

    # Domain inclusion/exclusion-dependent properties
    def domain_dependent_properties(self, response, **params) -> None:
        if params.get("topic", "general") != "general":
            return

        if params.get("include_domains", False) and len(params["include_domains"]) > 0:
            for result in response["results"]:
                self.assertTrue(any(domain in urlparse(result["url"]).netloc for domain in params["include_domains"]))

        if params.get("exclude_domains", False) and len(params["exclude_domains"]) > 0:
            for result in response["results"]:
                self.assertFalse(any(domain in urlparse(result["url"]).netloc for domain in params["exclude_domains"]))

    # Image-dependent properties
    def image_properties(self, response, **params) -> None:
        if params.get("topic", "general") == "general" and params.get("include_images", False):
            self.assertIsNotNone(response["images"])
            self.assertIsInstance(response["images"], list)
            for image in response["images"]:
                self.assertIsInstance(image, str)

    # Answer-dependent properties
    def answer_properties(self, response, **params) -> None:
        if params.get("include_answer", False):
            self.assertIn("answer", response)
            self.assertIsInstance(response["answer"], str)


    # Every single search response should have these properties
    def common_response_properties(self, response) -> None:
        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertIn("answer", response)
        self.assertIn("query", response)
        self.assertIn("results", response)
        self.assertIn("images", response)
        self.assertIn("response_time", response)
        self.assertIn("follow_up_questions", response)

        self.assertIsNotNone(response["query"])
        self.assertIsNotNone(response["results"])
        self.assertIsNotNone(response["response_time"])
        self.assertIsNotNone(response["images"])

        self.assertIsInstance(response["query"], str)
        self.assertIsInstance(response["results"], list)
        self.assertIsInstance(response["response_time"], float)
        self.assertIsInstance(response["images"], list)

    # Search responses also have properties that depend on the request params
    def custom_response_properties(self, response, **params) -> None:
        self.domain_dependent_properties(response, **params)
        self.image_properties(response, **params)
        self.answer_properties(response, **params)
        for result in response["results"]:
            self.topic_specific_properties(result, **params)

    def test_internal_search(self) -> None:
        for test_case in cases:
            with self.subTest(msg=test_case["name"]):
                response = asyncio.run(self.tavily_client._search(**test_case["params"]))
                self.common_response_properties(response)
                if test_case["params"].get("topic", "general") == "general":
                    for search_result in response["results"]:
                        self.general_search_result_properties(search_result)
                elif test_case["params"].get("topic", "general") == "news":
                    for search_result in response["results"]:
                        self.news_search_result_properties(search_result)
                self.custom_response_properties(response, **test_case["params"])

    def test_external_search(self) -> None:
        for test_case in cases:
            with self.subTest(msg=test_case["name"]):
                response = asyncio.run(self.tavily_client.search(**test_case["params"]))
                self.common_response_properties(response)
                if test_case["params"].get("topic", "general") == "general":
                    for search_result in response["results"]:
                        self.general_search_result_properties(search_result)
                elif test_case["params"].get("topic", "general") == "news":
                    for search_result in response["results"]:
                        self.news_search_result_properties(search_result)
                self.custom_response_properties(response, **test_case["params"])

class QNASearchTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.tavily_client = AsyncTavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_qna_search(self) -> None:
        for test_case in cases:
            if "include_answer" in test_case["params"]:
                del test_case["params"]["include_answer"]
            if "include_raw_content" in test_case["params"]:
                del test_case["params"]["include_raw_content"]
            if "include_images" in test_case["params"]:
                del test_case["params"]["include_images"]
            with self.subTest(msg=test_case["name"]):
                response = asyncio.run(self.tavily_client.qna_search(**test_case["params"]))
                self.assertIsNotNone(response)
                self.assertIsInstance(response, str)
                self.assertTrue(len(response) > 0)

class CompanyInfoSearchTest(unittest.TestCase):

    def setUp(self) -> None:
        self.tavily_client = AsyncTavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    # Every single search result should have these properties
    def common_search_result_properties(self, result) -> None:
        self.assertIsInstance(result, dict)
        self.assertIn("title", result)
        self.assertIn("url", result)
        self.assertIn("content", result)
        self.assertIn("score", result)
    
    def test_company_info_search(self) -> None:
        for test_case in cases:
            if "topic" in test_case["params"]:
                del test_case["params"]["topic"]
            if "include_domains" in test_case["params"]:
                del test_case["params"]["include_domains"]
            if "exclude_domains" in test_case["params"]:
                del test_case["params"]["exclude_domains"]
            if "include_raw_content" in test_case["params"]:
                del test_case["params"]["include_raw_content"]
            if "include_images" in test_case["params"]:
                del test_case["params"]["include_images"]
            if "include_answer" in test_case["params"]:
                del test_case["params"]["include_answer"]
            if "use_cache" in test_case["params"]:
                del test_case["params"]["use_cache"]
            with self.subTest(msg=test_case["name"]):
                response = asyncio.run(self.tavily_client.get_company_info(**test_case["params"]))
                self.assertIsNotNone(response)
                self.assertIsInstance(response, list)
                self.assertTrue(len(response) > 0)
                for search_result in response:
                    self.common_search_result_properties(search_result)
            
class ErrorTest(unittest.TestCase):
    
    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    # This test is here to ensure that no MissingAPIKeyError is raised when the API key is in the environment
    def test_load_key_from_env(self) -> None:
        self.assertIn('results', asyncio.run(AsyncTavilyClient().search("Why is Tavily the best search API?")))
    
    def test_missing_api_key(self) -> None:
        with self.assertRaises(MissingAPIKeyError):
            AsyncTavilyClient(api_key='')
        
        old_key = os.getenv("TAVILY_API_KEY")
        del os.environ["TAVILY_API_KEY"]
        with self.assertRaises(MissingAPIKeyError):
            AsyncTavilyClient()
            
        os.environ["TAVILY_API_KEY"] = old_key


    def test_invalid_api_key(self) -> None:
        with self.assertRaises(InvalidAPIKeyError):
            asyncio.run(AsyncTavilyClient(api_key="invalid_api_key").search("Why is Tavily the best search API?"))

if __name__ == "__main__":

    unittest.main()