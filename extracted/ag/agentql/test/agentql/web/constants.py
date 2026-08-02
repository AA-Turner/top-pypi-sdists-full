HTML = """
    <html>
        <head/>
        <body>
            <div id="test">
                <button>Test</button>
                <input type="text" />
            </div>
        </body>
    </html>
"""

ELEMENTS_QUERY = """
{
    test_btn
    input_box
}
"""

ELEMENTS_RESPONSE = {
    "response": {
        "test_btn": {
            "role": "button",
            "tf623_id": "4",
            "html_tag": "button",
            "name": "Test",
            "attributes": {},
        },
        "input_box": {
            "role": "textbox",
            "tf623_id": "5",
            "html_tag": "input",
            "name": "",
            "attributes": {"type": "text"},
        },
    },
    "request_id": "1",
}

RESPONSE = {
    "response": {
        "page_element": {
            "role": "button",
            "name": "Test",
            "tf623_id": "1",
        },
    },
    "request_id": "1",
}

NO_RESULT_QUERY = """
{
    error_test_btn
}
"""

NONE_RESPONSE = {"response": {"error_test_btn": None}, "request_id": None}

QUERY_DATA_HTML = """
    <html>
        <head/>
        <body>
            <div id="test">
                <p id="description">here is the description!</p>
                <a href="https://google.com">My Link</a>
            </div>
        </body>
    </html>
"""

QUERY_DATA_QUERY = """
{
    description
    my_link
}
"""

QUERY_DATA_RESPONSE_CLEANED = {
    "description": "here is the description!",
    "my_link": "https://google.com",
}

QUERY_DATA_RESPONSE = {
    "response": {
        "description": "here is the description!",
        "my_link": "https://google.com",
    },
    "request_id": "1",
}

QUERY_DATA_ERROR_RESPONSE = {
    "response": {"error_test_btn": None},
    "request_id": "1",
}

DOCUMENT_PATH = "test_assets/pdf_test.pdf"

QUERY_DOCUMENT_QUERY = " { name } "

QUERY_DOCUMENT_PROMPT = "What is the name of the person in the document?"

INVALID_QUERY = "invalid query"


QUERY_DOCUMENT_RESPONSE_CLEANED = {
    "name": "Jaime L. Chase",
}

QUERY_DOCUMENT_RESPONSE = {
    "data": {
        "name": "Jaime L. Chase",
    },
    "metadata": {"request_id": "1"},
}

QUERY_DOCUMENT_ERROR_RESPONSE = {
    "data": {"name": None},
    "metadata": {"request_id": "1"},
}
