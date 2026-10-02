"""
Integration tests for gravitas-md2gdocs with actual Google Docs API.

These tests require:
1. Google OAuth credentials (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
2. The `google` extra: pip install gravitas-md2gdocs[google]

Run with: pytest tests/test_integration.py -v -s

Note: These tests create and delete real Google Docs in your account.
"""

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load .env file from project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Skip all tests if credentials aren't available
pytestmark = pytest.mark.skipif(
    not os.environ.get("GOOGLE_CLIENT_ID") or not os.environ.get("GOOGLE_CLIENT_SECRET"),
    reason="Google credentials not set (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)",
)

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False


# Scopes needed for Google Docs API and file management
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive.file",
]


@pytest.fixture(scope="module")
def docs_service():
    """Create a Google Docs service instance using OAuth."""
    if not GOOGLE_AVAILABLE:
        pytest.skip("google-api-python-client not installed")

    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

    if not client_id or not client_secret:
        pytest.skip("Google credentials not configured")

    # Check for cached token
    token_path = os.path.expanduser("~/.gravitas_md2gdocs_test_token.json")
    creds = None

    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request

            creds.refresh(Request())
        else:
            # Use manual OAuth flow with custom redirect URI
            import http.server
            import urllib.parse
            import webbrowser

            from google_auth_oauthlib.flow import Flow

            redirect_uri = "http://localhost:3000/auth/integrations/oauth_callback"
            client_config = {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri],
                }
            }

            flow = Flow.from_client_config(client_config, SCOPES, redirect_uri=redirect_uri)
            auth_url, _ = flow.authorization_url(prompt="consent")

            # Simple server to catch the OAuth callback
            authorization_code = None

            class OAuthHandler(http.server.BaseHTTPRequestHandler):
                def do_GET(self):
                    nonlocal authorization_code
                    parsed = urllib.parse.urlparse(self.path)
                    if parsed.path == "/auth/integrations/oauth_callback":
                        query = urllib.parse.parse_qs(parsed.query)
                        authorization_code = query.get("code", [None])[0]
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        self.wfile.write(
                            b"<html><body><h1>Success!</h1>"
                            b"<p>You can close this window.</p></body></html>"
                        )
                    else:
                        self.send_response(404)
                        self.end_headers()

                def log_message(self, format, *args):
                    pass  # Suppress logging

            server = http.server.HTTPServer(("localhost", 3000), OAuthHandler)
            server.timeout = 120

            print("\nOpening browser for Google authorization...")
            webbrowser.open(auth_url)

            server.handle_request()
            server.server_close()

            if not authorization_code:
                pytest.skip("OAuth authorization failed")

            flow.fetch_token(code=authorization_code)
            creds = flow.credentials

        # Save credentials for next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return build("docs", "v1", credentials=creds)


@pytest.fixture
def test_doc(docs_service):
    """Create a test document and clean it up after the test."""
    # Create a new document
    doc = (
        docs_service.documents().create(body={"title": "gravitas-md2gdocs Test Document"}).execute()
    )
    doc_id = doc["documentId"]

    yield doc_id

    # Clean up - delete the document
    try:
        from googleapiclient.discovery import build

        # Need Drive API to delete docs
        creds = docs_service._http.credentials
        drive_service = build("drive", "v3", credentials=creds)
        drive_service.files().delete(fileId=doc_id).execute()
    except Exception as e:
        print(f"Warning: Could not delete test document {doc_id}: {e}")


class TestGoogleDocsIntegration:
    """Integration tests that hit the real Google Docs API."""

    def test_to_requests_creates_valid_requests(self, docs_service, test_doc):
        """Test that to_requests generates valid API requests."""
        from gravitas_md2gdocs import to_requests

        markdown = "# Hello World\n\nThis is a test."
        requests = to_requests(markdown)

        # Execute the requests
        result = (
            docs_service.documents()
            .batchUpdate(documentId=test_doc, body={"requests": requests})
            .execute()
        )

        assert "replies" in result

        # Verify content was inserted
        doc = docs_service.documents().get(documentId=test_doc).execute()
        content = doc.get("body", {}).get("content", [])

        # Extract text from document
        text = ""
        for element in content:
            if "paragraph" in element:
                for elem in element["paragraph"].get("elements", []):
                    if "textRun" in elem:
                        text += elem["textRun"]["content"]

        assert "Hello World" in text
        assert "This is a test" in text

    def test_append_function(self, docs_service, test_doc):
        """Test the append helper function."""
        from gravitas_md2gdocs import append

        # Append content
        append(docs_service, test_doc, "# First Section\n\nSome content.")
        append(docs_service, test_doc, "\n## Second Section\n\nMore content.")

        # Verify both sections exist
        doc = docs_service.documents().get(documentId=test_doc).execute()
        content = doc.get("body", {}).get("content", [])

        text = ""
        for element in content:
            if "paragraph" in element:
                for elem in element["paragraph"].get("elements", []):
                    if "textRun" in elem:
                        text += elem["textRun"]["content"]

        assert "First Section" in text
        assert "Second Section" in text

    def test_replace_function(self, docs_service, test_doc):
        """Test the replace helper function."""
        from gravitas_md2gdocs import append, replace

        # Add initial content
        append(docs_service, test_doc, "# Original Title\n\nOriginal content.")

        # Replace with new content
        replace(docs_service, test_doc, "# New Title\n\nNew content.")

        # Verify replacement
        doc = docs_service.documents().get(documentId=test_doc).execute()
        content = doc.get("body", {}).get("content", [])

        text = ""
        for element in content:
            if "paragraph" in element:
                for elem in element["paragraph"].get("elements", []):
                    if "textRun" in elem:
                        text += elem["textRun"]["content"]

        assert "New Title" in text
        assert "New content" in text
        assert "Original" not in text

    def test_insert_at_function(self, docs_service, test_doc):
        """Test the insert_at helper function."""
        from gravitas_md2gdocs import append, insert_at

        # Add initial content
        append(docs_service, test_doc, "Start End")

        # Insert in the middle (after "Start ")
        insert_at(docs_service, test_doc, "**INSERTED** ", index=7)

        # Verify insertion
        doc = docs_service.documents().get(documentId=test_doc).execute()
        content = doc.get("body", {}).get("content", [])

        text = ""
        for element in content:
            if "paragraph" in element:
                for elem in element["paragraph"].get("elements", []):
                    if "textRun" in elem:
                        text += elem["textRun"]["content"]

        assert "INSERTED" in text

    def test_bold_formatting(self, docs_service, test_doc):
        """Test that bold formatting is applied correctly."""
        from gravitas_md2gdocs import append

        append(docs_service, test_doc, "This is **bold** text.")

        doc = docs_service.documents().get(documentId=test_doc).execute()
        content = doc.get("body", {}).get("content", [])

        # Find the bold text run
        found_bold = False
        for element in content:
            if "paragraph" in element:
                for elem in element["paragraph"].get("elements", []):
                    if "textRun" in elem:
                        text_run = elem["textRun"]
                        style = text_run.get("textStyle", {})
                        if "bold" in text_run["content"].lower():
                            # The word "bold" should have bold styling
                            found_bold = style.get("bold", False)

        assert found_bold, "Bold formatting was not applied"

    def test_bullet_list(self, docs_service, test_doc):
        """Test that bullet lists are created correctly."""
        from gravitas_md2gdocs import append

        append(docs_service, test_doc, "- Item 1\n- Item 2\n- Item 3")

        doc = docs_service.documents().get(documentId=test_doc).execute()
        content = doc.get("body", {}).get("content", [])

        # Check for bullet list
        has_bullets = False
        for element in content:
            if "paragraph" in element:
                para = element["paragraph"]
                if "bullet" in para:
                    has_bullets = True
                    break

        assert has_bullets, "Bullet list was not created"

    def test_numbered_list(self, docs_service, test_doc):
        """Test that numbered lists are created correctly."""
        from gravitas_md2gdocs import append

        append(docs_service, test_doc, "1. First\n2. Second\n3. Third")

        doc = docs_service.documents().get(documentId=test_doc).execute()
        content = doc.get("body", {}).get("content", [])

        # Check for numbered list
        has_numbers = False
        for element in content:
            if "paragraph" in element:
                para = element["paragraph"]
                if "bullet" in para:
                    has_numbers = True
                    break

        assert has_numbers, "Numbered list was not created"

    def test_link_formatting(self, docs_service, test_doc):
        """Test that links are created correctly."""
        from gravitas_md2gdocs import append

        append(docs_service, test_doc, "Click [here](https://example.com) for more.")

        doc = docs_service.documents().get(documentId=test_doc).execute()
        content = doc.get("body", {}).get("content", [])

        # Check for link
        found_link = False
        for element in content:
            if "paragraph" in element:
                for elem in element["paragraph"].get("elements", []):
                    if "textRun" in elem:
                        style = elem["textRun"].get("textStyle", {})
                        if "link" in style:
                            found_link = True
                            assert style["link"]["url"] == "https://example.com"

        assert found_link, "Link was not created"

    def test_heading_levels(self, docs_service, test_doc):
        """Test that heading levels are applied correctly."""
        from gravitas_md2gdocs import append

        append(docs_service, test_doc, "# H1\n## H2\n### H3")

        doc = docs_service.documents().get(documentId=test_doc).execute()
        content = doc.get("body", {}).get("content", [])

        heading_styles = []
        for element in content:
            if "paragraph" in element:
                para = element["paragraph"]
                style = para.get("paragraphStyle", {})
                named_style = style.get("namedStyleType", "")
                if named_style.startswith("HEADING"):
                    heading_styles.append(named_style)

        assert "HEADING_1" in heading_styles
        assert "HEADING_2" in heading_styles
        assert "HEADING_3" in heading_styles

    def test_complex_document(self, docs_service, test_doc):
        """Test creating a complex document with multiple formatting types."""
        from gravitas_md2gdocs import append

        markdown = """# Document Title

This is a paragraph with **bold**, *italic*, and `code` formatting.

## Section 1

- Bullet point 1
- Bullet point 2
- Bullet point 3

## Section 2

1. Numbered item 1
2. Numbered item 2
3. Numbered item 3

> This is a blockquote

### Code Example

```python
def hello():
    print("Hello, World!")
```

Visit [our website](https://example.com) for more info.
"""
        append(docs_service, test_doc, markdown)

        doc = docs_service.documents().get(documentId=test_doc).execute()
        content = doc.get("body", {}).get("content", [])

        # Extract all text
        text = ""
        for element in content:
            if "paragraph" in element:
                for elem in element["paragraph"].get("elements", []):
                    if "textRun" in elem:
                        text += elem["textRun"]["content"]

        # Verify key content is present
        assert "Document Title" in text
        assert "Section 1" in text
        assert "Section 2" in text
        assert "Bullet point" in text
        assert "Numbered item" in text
        assert "blockquote" in text
        assert "hello()" in text or "def hello" in text
