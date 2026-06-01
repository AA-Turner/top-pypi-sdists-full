"""FastHTML web interface.

# FastHTML and JS
Refer to this example for understanding on how to
[write JavaScript with FastHTML](https://github.com/AnswerDotAI/fasthtml/blob/main/fasthtml/js.py).

- [Rendering markdown after processing](https://docs.fastht.ml/tutorials/by_example.html#custom-scripts-and-styling).
"""

from bacore.domain.files import MarkdownFile
from bacore.domain.source_code import (
    ClassModel,
    DirectoryModel,
    FunctionModel,
    ModuleModel,
)
from fasthtml.common import (
    A,
    Aside,
    Div,
    H1,
    H2,
    H3,
    H4,
    Li,
    Link,
    Nav,
    P,
    Ul,
    Titled,
)
from pathlib import Path

flexboxgrid = Link(
    rel="stylesheet",
    href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css",
    type="text/css",
)


class MarkdownFT(MarkdownFile):
    """Markdown class."""

    def __ft__(self):
        """Markdown file renedered as HTML."""
        return Div(self.read(), cls="marked")


class FuncFT(FunctionModel):
    """Function class."""

    def __ft__(self):
        """Function model rendered as HTML."""
        return Div(self.doc, cls="marked")


class ClassFT(ClassModel):
    """Class model class."""

    def __ft__(self):
        """Class docstrings rendered as HTML."""
        return Div(self.doc, cls="marked")


class ModuleFT(ModuleModel):
    """Module model class."""

    def __ft__(self):
        """Module docstring rendered as HTML."""
        return Div(self.doc, cls="marked")

    def classes(self):
        return Div("# Heading of classes\nSome text", cls="marked")


def uri_to(module: ModuleModel) -> str:
    """Uniform resource identifier for module.

    `package_offset` is increased by one to remove the leading slash from the module path.
    """
    package_root = module.package_root or ""
    package_offset = len(package_root) + 1 if package_root != "" else 0

    return module.uri[package_offset:].replace("__init__", "").replace("_", "-").replace(".", "/")


def map_uri_to_module(
    directory_model: DirectoryModel,
) -> dict[str, ModuleModel]:
    """Collect all modules with their paths relative to the package_root.

    Parameters
        directory_model: The directory model to traverse
        package_root: The package to be considered as base package.
    """
    path_module_mappings = {uri_to(module): module.model_copy() for module in directory_model.modules}

    for subdirectory in directory_model.directories:
        path_module_mappings.update(map_uri_to_module(subdirectory))

    return path_module_mappings


class SrcDirFT(DirectoryModel):
    """Directory with Python source code.

    The tree should be ordered alphabetically (per default).
    The tree should follow the same branching structure as the folders have.

    The base is the a chosen markdown file. It makes sense to use the README.md file for that.
    Optionally should the tree contain more than one "roots". One root is the src tree and the other root is the tests
    tree.
    """

    # def generate_directory_tree(self, directory: DirectoryModel) -> Ul:
    #     """Recursively generate a nested <ul> structure for the directory tree."""

    #     for module in directory.modules:
    #         ul_tag += Li(A(module.name.title(), href=self.uri_to_url(module)))

    #     return ul_tag

    @staticmethod
    def url_to_module_tree(directory_model: DirectoryModel):
        url_to_module_mappings = Ul(
            *[Li(A(module.name.title(), href=SrcDirFT.uri_to_url(module))) for module in directory_model.modules],
            Ul(),
        )

        # for subdirectory in directory_model.directories:
        #     url_to_module_mappings.update("test")

        return Div(str(type(url_to_module_mappings)))


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
                    *[
                        Li(A(module.name.title(), href=self.uri_to_url(module)))
                        for directory in self.directories
                        for module in directory.modules
                    ]
                ),
            ),
            cls="col-xs-2",
        )


class Documentation(DirectoryModel):
    """Documentation pages for project."""

    def docs_tree(self) -> dict[str, ModuleModel]:
        return map_uri_to_module(directory_model=self)


def doc_page(doc_source: Documentation, url: str) -> Titled:
    """Dirty implementation of the Documentation (future) component.

    The **Module Classes** function has to be recursive in the same way as
    `map_path_to_module` in `interfaces/web_fasthtml` is.
    """
    module = doc_source.docs_tree().get(url)
    if module is None:
        raise ValueError(f'404 module "{url}" does not exist')

    funcs = module.functions()
    classes = module.classes()

    return Div(
        Div(module.doc, cls="marked"),
        (
            Div(
                H1("Module Functions"),
                Ul(*[Li(func.name.title()) for func in funcs]),
                Div(*[(H2(func.name.title()), P(func.doc, cls="marked")) for func in funcs]),
            )
            if funcs
            else ""
        ),
        (
            Div(
                H1("Module Classes"),
                Ul(*[Li(klass.name.title()) for klass in classes]),
                Div(
                    *[
                        (
                            H2(klass.name.title()),
                            P(klass.doc, cls="marked"),
                            (
                                Div(
                                    H3("Class Functions"),
                                    Ul(*[Li(class_func.name.title()) for class_func in klass.functions()]),
                                    Div(
                                        *[
                                            (
                                                H4(class_func.name.title()),
                                                P(class_func.doc, cls="marked"),
                                            )
                                            for class_func in klass.functions()
                                        ]
                                    ),
                                )
                                if klass.functions()
                                else ""
                            ),
                            (
                                Div(
                                    H3("Sub-Classes"),
                                    Ul(*[Li(sub_class.name.title()) for sub_class in klass.classes()]),
                                    Div(
                                        *[
                                            (
                                                H4(sub_class.name.title()),
                                                P(sub_class.doc, cls="marked"),
                                            )
                                            for sub_class in klass.classes()
                                        ]
                                    ),
                                )
                                if klass.classes()
                                else ""
                            ),
                        )
                        for klass in classes
                    ]
                ),
            )
            if classes
            else ""
        ),
    )


class DocsFT:
    """Creates a navigation menu as an aside.
    Creates a page for each source code file.
    The pages have:
    - the documentation string for the module.

    - A list of all classes
    - The documentation string for all classes
    - A list of all class methods.
    - The documentation string for all class methods.

    - A list of all module functions.
    - The documentation string for all the module functions.
    The classes source"""

    def __init__(self, src_package: Path, src_package_root, url: str):
        self.nav_docs = NavDocs(path=src_package, package_root=src_package_root)
        self.src_package = src_package
        self.src_package_root = src_package_root
        self.url = url

    def __ft__(self):
        return Div(
            self.nav_docs,
            Div(doc_page(doc_source=self.src_package, url=self.url), cls="col-xs-10"),
            cls="row",
        )
