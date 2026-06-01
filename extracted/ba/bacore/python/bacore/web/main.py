"""BACore documentation with FastHTML.

# App:
- `live`: Start the app with `live=True`, to reload the webpage in the browser on any code change.

# Resources:
- FastHTML uses [Pico CSS](https://picocss.com).
"""

from bacore.domain.source_code import DirectoryModel, ModuleModel
from bacore.interfaces.fasthtml.common import (
    Documentation,
    MarkdownFT,
    doc_page,
    flexboxgrid,
)
from fasthtml.common import (
    A,
    Aside,
    Details,
    Div,
    # FastHTML,
    FastHTMLWithLiveReload,
    HighlightJS,
    Li,
    MarkdownJS,
    Nav,
    Strong,
    Summary,
    Titled,
    Ul,
    picolink,
    serve,
)
from pathlib import Path

tests_docs = Documentation(path=Path("tests"), package_root="tests")

headers = (
    flexboxgrid,
    HighlightJS(langs=["python", "html", "css"]),
    MarkdownJS(),
    picolink,
)
app = FastHTMLWithLiveReload(hdrs=headers)


class NavTop:
    """Top and main navigation."""

    def __ft__(self):
        return Nav(
            Ul(Li(A(Strong("HOME"), href="/"))),
            Ul(
                Li(A(Strong("Docs"), href="/docs/")),
                Li(A(Strong("Github"), href="https://github.com/bacoredev/bacore/")),
                Li(A(Strong("PyPi"), href="https://pypi.org/project/bacore/")),
            ),
        )


class NavDocs(DirectoryModel):
    @staticmethod
    def uri_to_url(module: ModuleModel):
        """Convert module URI to a URL path.

        `package_offset` is increased by one to remove the leading slash from the module path.
        """
        package_root = module.package_root or ""
        package_offset = len(package_root) + 1 if package_root != "" else 0
        return module.uri[package_offset:].replace("__init__", "").replace("_", "-").replace(".", "/")

    def __ft__(self):
        return Aside(
            Nav(
                Ul(
                    Li(
                        Details(
                            Summary(A("Domain", href="/docs/domain/")),
                            Ul(
                                Li(A("Errors", href="/docs/domain/errors")),
                                Li(A("Files", href="/docs/domain/files")),
                                Li(A("Measurements", href="/docs/domain/measurements")),
                                Li(A("Protocols", href="/docs/domain/protocols")),
                                Li(A("Responses", href="/docs/domain/responses")),
                                Li(A("Settings", href="/docs/domain/settings")),
                                Li(A("Source Code", href="/docs/domain/source-code")),
                                Li(A("System", href="/docs/domain/system")),
                                Li(A("Testdata", href="/docs/domain/testdata")),
                            ),
                        )
                    ),
                    Li(
                        Details(
                            Summary(A("Interactors", href="/docs/interactors/")),
                            Ul(
                                Li(
                                    A(
                                        "File Handler",
                                        href="/docs/interactors/file-handler",
                                    )
                                ),
                                Li(
                                    A(
                                        "Network Handler",
                                        href="/docs/interactors/network-handler",
                                    )
                                ),
                                Li(
                                    A(
                                        "OS Handler",
                                        href="/docs/interactors/os-handler",
                                    )
                                ),
                                Li(
                                    A(
                                        "Source Code Reader",
                                        href="/docs/interactors/source-code-reader",
                                    )
                                ),
                            ),
                        )
                    ),
                    Li(
                        Details(
                            Summary(A("Interfaces", href="/docs/interfaces/")),
                            Ul(
                                Li(
                                    Details(
                                        Summary(
                                            A(
                                                "FastHTML",
                                                href="/docs/interfaces/fasthtml/",
                                            )
                                        ),
                                        Ul(
                                            Li(
                                                A(
                                                    "Common",
                                                    href="/docs/interfaces/fasthtml/common",
                                                )
                                            ),
                                            Li(
                                                A(
                                                    "Docs",
                                                    href="/docs/interfaces/fasthtml/docs",
                                                )
                                            ),
                                        ),
                                    )
                                ),
                                Li(A("CLI Git", href="/docs/interfaces/cli-git")),
                                Li(A("CLI Typer", href="/docs/interfaces/cli-typer")),
                                Li(
                                    A(
                                        "Power Point",
                                        href="/docs/interfaces/power-point",
                                    )
                                ),
                            ),
                        ),
                    ),
                    Li(
                        Details(
                            Summary(A("Web", href="/docs/web/")),
                            Ul(Li(A("Main", href="/docs/web/main"))),
                        )
                    ),
                )
            ),
            cls="col-xs-2",
        )


@app.get("/")
def home():
    return Titled(
        "BACore",
        NavTop(),
        MarkdownFT(path=Path("README.md"), skip_title=True),
    )


@app.get("/docs/{path:path}")
def docs(path: str):
    return Titled(
        "Documentation",
        NavTop(),
        Div(
            NavDocs(path=Path("python/bacore"), package_root="bacore"),
            Div(
                doc_page(
                    doc_source=Documentation(path=Path("python/bacore"), package_root="bacore"),
                    url=path,
                ),
                cls="col-xs-10",
            ),
            cls="row",
        ),
    )


@app.route("/tests/{path:path}", methods="get")
def tests(path: str):
    """Test case pages."""
    return doc_page(doc_source=tests_docs, url=path)


serve(port=7001)
