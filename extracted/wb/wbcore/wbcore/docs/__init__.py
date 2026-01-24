import markdown
from django.conf import settings
from rest_framework.response import Response


def get_markdown_docs(docs):
    try:
        with open(docs, "r") as f:
            return Response(
                markdown.markdown(
                    f.read(),
                    extensions=settings.WBCORE_DEFAULT_MARKDOWN_EXTENSIONS,
                )
            )
    except FileNotFoundError:
        return Response(
            markdown.markdown(
                docs,
                extensions=settings.WBCORE_DEFAULT_MARKDOWN_EXTENSIONS,
            )
        )
    except AttributeError:
        return Response({"errors": "No documentation available."})
