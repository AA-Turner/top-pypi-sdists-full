import importlib
import os
import re
from ctypes import (
    c_void_p,
    cdll,
)
from pathlib import Path
from typing import cast

from more_itertools import (
    mark_ends,
)
from tree_sitter import (
    Language,
    Node,
    Parser,
    Tree,
)

TREE_SITTER_PARSERS_PATH = os.environ.get("TREE_SITTER_PARSERS")
TREE_SITTER_LANGUAGE_CONVERSION = {
    "csharp": "c_sharp",
    "razor": "c_sharp",
    "tsx": "typescript",
}

TREE_SITTER_SUPPORTED_IMPERATIVE_LANGUAGES = {
    ".aspx": "c_sharp",
    ".cs": "c_sharp",
    ".cshtml": "razor",
    ".dart": "dart",
    ".go": "go",
    ".java": "java",
    ".js": "javascript",
    ".mjs": "javascript",
    ".jsp": "java",
    ".jsx": "jsx",
    ".kt": "kotlin",
    ".php": "php",
    ".py": "python",
    ".razor": "razor",
    ".rb": "ruby",
    ".scala": "scala",
    ".swift": "swift",
    ".ts": "typescript",
    ".tsx": "typescript",
}

TREE_SITTER_SUPPORTED_DECLARATIVE_LANGUAGES = {
    ".tf": "hcl",
    ".hcl": "hcl",
    ".html": "html",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".xml": "xml",
    "dockerfile": "dockerfile",
    ".json": "json",
}

TREE_SITTER_SUPPORTED_LANGUAGES = {
    **TREE_SITTER_SUPPORTED_IMPERATIVE_LANGUAGES,
    **TREE_SITTER_SUPPORTED_DECLARATIVE_LANGUAGES,
}


TREE_SITTER_IMPORTS_DECLARATIONS_MAP: dict[str, tuple[str, ...]] = {
    "java": ("import_declaration",),
    "c_sharp": ("using_directive",),
    "dart": ("import_specification",),
    "go": ("import_declaration",),
    "javascript": ("import_statement",),
    "kotlin": ("import_header",),
    "php": ("use_declaration", "namespace_use_declaration"),
    "python": ("import_statement", "import_from_statement"),
    "scala": ("import_declaration",),
    "swift": ("import_declaration",),
    "typescript": ("import_statement",),
}

TREE_SITTER_FUNCTION_DECLARATION_MAP: dict[str, tuple[str, ...]] = {
    "c_sharp": (
        "constructor_declaration",
        "conversion_operator_declaration",
        "destructor_declaration",
        "method_declaration",
    ),
    "dart": (
        "function_signature",
        "function_body",
        "getter_signature",
        "setter_signature",
        "method_signature",
    ),
    "dockerfile": (
        "from_instruction",
        "workdir_instruction",
        "comment",
        "copy_instruction",
        "run_instruction",
        "expose_instruction",
        "user_instruction",
        "cmd_instruction",
    ),
    "go": (
        "function_declaration",
        "method_declaration",
    ),
    "html": (
        "document",
        "element",
        "style_element",
        "script_element",
    ),
    "java": (
        "constructor_declaration",
        "method_declaration",
        "record_declaration",
    ),
    "javascript": (
        "arrow_function",
        "generator_function",
        "generator_function_declaration",
        "method_definition",
        "function_expression",
        "function_declaration",
    ),
    "json": (
        "object",
        "array",
    ),
    "kotlin": (
        "function_declaration",
        "primary_constructor",
        "getter",
        "setter",
    ),
    "php": (
        "function_definition",
        "function_static_declaration",
        "method_declaration",
    ),
    "python": ("function_definition",),
    "ruby": (
        "method",
        "singleton_method",
        "setter",
    ),
    "scala": (
        "function_declaration",
        "function_definition",
    ),
    "swift": (
        "function_declaration",
        "protocol_function_declaration",
    ),
    "typescript": (
        "function_declaration",
        "generator_function_declaration",
        "method_definition",
        "function_expression",
        "arrow_function",
        "function_signature",
        "function_type",
    ),
    "hcl": ("block",),
    "yaml": (
        "block_mapping_pair",
        "block_mapping",
        "block_sequence",
        "block_sequence_item",
    ),
    "yml": (
        "block_mapping_pair",
        "block_mapping",
        "block_sequence",
        "block_sequence_item",
    ),
    "xml": ("element",),
}

TREE_SITTER_FUNCTION_IDENTIFIER = {
    "python": {
        "function_definition": "name",
    },
    "bash": {
        "function_definition": "name",
    },
    "c_sharp": {
        "constructor_declaration": "name",
        "conversion_operator_declaration": "type",
        "destructor_declaration": "name",
        "method_declaration": "name",
    },
    "dart": {
        "function_signature": "name",
        "getter_signature": "name",
        "setter_signature": "name",
        "method_signature": "name",
    },
    "go": {
        "function_declaration": "name",
        "method_declaration": "name",
    },
    "java": {
        "constructor_declaration": "name",
        "method_declaration": "name",
        "record_declaration": "name",
    },
    "javascript": {
        "generator_function": "name",
        "generator_function_declaration": "name",
        "method_definition": "name",
        "function_expression": "name",
        "function_declaration": "name",
    },
    "kotlin": {
        "function_declaration": "identifier",
    },
    "php": {
        "function_definition": "name",
        "function_static_declaration": "name",
        "method_declaration": "name",
    },
    "ruby": {
        "method": "name",
        "singleton_method": "name",
        "setter": "name",
    },
    "scala": {
        "function_declaration": "name",
        "function_definition": "name",
    },
    "swift": {
        "function_declaration": "name",
        "protocol_function_declaration": "name",
    },
    "typescript": {
        "function_declaration": "name",
        "generator_function_declaration": "name",
        "method_definition": "name",
        "function_expression": "name",
    },
}
TREE_SITTER_REQUIRES_SEQUENCE = {
    "dart": ("function_signature", "function_body"),
}


class InvalidFileType(Exception):
    """Exception to control file type."""

    def __init__(self, detail: str = "") -> None:
        msg = "Exception - Invalid file type"
        if detail:
            msg += f": {detail}"
        super().__init__(msg)


def ignore_advisories(where: str | None) -> str:
    if where is not None:
        where = re.sub(r"(\s+\(.*\))?(\s+\[.*\])?", "", where)
    return str(where)


def get_node_content(source_code: bytes, node: Node) -> str:
    """Extract text content from a tree-sitter node."""
    return source_code[node.start_byte : node.end_byte].decode("utf-8")


def get_language_from_path(path: str) -> str | None:
    path = ignore_advisories(path)
    language = TREE_SITTER_SUPPORTED_LANGUAGES.get(Path(path).suffix, "")
    language = language or TREE_SITTER_SUPPORTED_LANGUAGES.get(Path(path).name, "")
    if not language:
        return None
    return language


def get_language_for_tree(language: str) -> Language:
    try:
        language_module = importlib.import_module(f"tree_sitter_{language}")
        function_name = {
            "php": "language_php",
            "tsx": "language_tsx",
            "typescript": "language_tsx",
            "xml": "language_xml",
        }.get(language, "language")
        language_so = Language(getattr(language_module, function_name)())
    except (ImportError, ModuleNotFoundError) as exc:
        so_library_path: str = os.path.join(TREE_SITTER_PARSERS_PATH or "", f"{language}.so")
        if not Path(so_library_path).exists():
            raise InvalidFileType(so_library_path) from exc

        lib = cdll.LoadLibrary(os.fspath(so_library_path))
        language_function = getattr(lib, f"tree_sitter_{language}")
        language_function.restype = c_void_p
        language_ptr = language_function()
        language_so = Language(language_ptr)

    return language_so


def parse_content_tree_sitter(
    content: bytes,
    language: str,
) -> Tree:
    language_so = get_language_for_tree(language)

    parser: Parser = Parser(language_so)
    return parser.parse(content)


def query_nodes_by_language(
    language: str,
    tree: Tree,
    queries_map: dict[str, tuple[str, ...]],
) -> dict[str, list[Node]]:
    try:
        language_parser = get_language_for_tree(language)
    except OSError as exc:
        raise InvalidFileType from exc
    query = "\n".join(f"({item}) @{item}" for item in queries_map.get(language, []))
    return language_parser.query(query).captures(tree.root_node)


def query_function_by_name(
    language: str,
    tree: Tree,
    function_node_type: str,
    node_identifier_name: str,
    function_name: str,
) -> list[Node]:
    language_parser = get_language_for_tree(language)
    query = f"""({function_node_type}
        name: ({node_identifier_name}) @name
        (#eq? @name "{function_name}")
    ) @{function_node_type}"""
    result = language_parser.query(query).captures(tree.root_node)
    return [node for key, nodes in result.items() for node in nodes if key == function_node_type]


def find_function_expression_by_query(
    language: str,
    original_node: Node,
    desired_line: int,
) -> Node | None:
    language_parser = get_language_for_tree(language)
    target_nodes: tuple[str, ...] = TREE_SITTER_FUNCTION_DECLARATION_MAP.get(language, ())
    query = "([" + (" ".join(f"({item})" for item in target_nodes)) + "] @target )"
    result = language_parser.query(query).captures(original_node)

    nodes = [node for _, nodes in result.items() for node in nodes]
    candidates = [
        x
        for x in sorted(
            nodes,
            key=lambda node: node.end_byte - node.start_byte,
        )
        if x.start_point[0] <= desired_line - 1 <= x.end_point[0]
    ]
    if not candidates:
        return None

    final_candidate = candidates[0]
    for node in candidates:
        if (node.end_byte - node.start_byte) < 500:
            final_candidate = node
            continue
        return node

    return final_candidate


def find_function_expression(original_node: Node | None, language: str) -> Node | None:
    target_nodes: tuple[str, ...] = TREE_SITTER_FUNCTION_DECLARATION_MAP.get(language, ())
    node = original_node
    while node:
        for node_name in target_nodes:
            if node_name == node.type:
                return node
        node = node.parent

    return None


def extract_function_nodes(
    source_code: bytes,
    desired_line: int,
    *,
    language: str,
) -> list[Node]:
    language = TREE_SITTER_LANGUAGE_CONVERSION.get(language) or language

    if language not in TREE_SITTER_FUNCTION_DECLARATION_MAP:
        raise InvalidFileType
    try:
        tree = parse_content_tree_sitter(source_code, language)
    except OSError:
        return []
    root_node = tree.root_node

    captures = query_nodes_by_language(
        language=language,
        tree=tree,
        queries_map=TREE_SITTER_FUNCTION_DECLARATION_MAP,
    )

    if language in TREE_SITTER_REQUIRES_SEQUENCE and captures:
        return _process_sequence(captures, desired_line)

    return _process_non_sequence(source_code, desired_line, root_node, language)


def _process_sequence(
    captures: dict[str, list[Node]],
    desired_line: int,
) -> list[Node]:
    for items in zip(*captures.values(), strict=False):
        if items[0].start_point[0] <= desired_line - 1 <= items[-1].end_point[0]:
            return cast("list[Node]", list(items))
    return []


def _process_non_sequence(
    source_code: bytes,
    desired_line: int,
    root_node: Node,
    language: str,
) -> list[Node]:
    lines = source_code.splitlines()
    if not lines:
        return []

    function_node = find_function_expression_by_query(language, root_node, desired_line)

    return [function_node] if function_node else []


def _process_hierarchical_candidates(
    language: str,
    root_node: Node,
    desired_line: int,
) -> list[Node]:
    """Find all nodes containing the target line, sorted by specificity.

    Returns:
        List of nodes ordered from most specific to most general

    """
    language_parser = get_language_for_tree(language)
    target_nodes: tuple[str, ...] = TREE_SITTER_FUNCTION_DECLARATION_MAP.get(language, ())
    query = "([" + (" ".join(f"({item})" for item in target_nodes)) + "] @target )"
    result = language_parser.query(query).captures(root_node)

    nodes = [node for _, nodes in result.items() for node in nodes]
    candidates = [
        node
        for node in sorted(
            nodes,
            key=lambda node: node.end_byte - node.start_byte,  # More specific first
        )
        if node.start_point[0] <= desired_line - 1 <= node.end_point[0]
    ]
    return candidates


def extract_hierarchical_nodes(
    source_code: bytes,
    desired_line: int,
    language: str,
) -> list[Node]:
    """Extract hierarchical nodes containing the specified line.

    Returns:
        List of tree-sitter nodes in hierarchical order from most specific to most general

    """
    language = TREE_SITTER_LANGUAGE_CONVERSION.get(language) or language

    try:
        tree = parse_content_tree_sitter(source_code, language)
    except OSError:
        return []

    hierarchical_candidates = _process_hierarchical_candidates(
        language=language,
        root_node=tree.root_node,
        desired_line=desired_line,
    )

    return hierarchical_candidates


def _calculate_positions(lines: list[bytes], desired_line: int) -> tuple[int | None, int | None]:
    try:
        start_position = 0
        blank_spaces = 0
        for _, last, index in mark_ends(range(desired_line)):
            if last and (match := re.match(r"^ *", lines[index].decode())):
                blank_spaces = len(match.group(0))
                start_position += blank_spaces
            else:
                start_position += len(lines[index]) + 1
        end_position = start_position + len(lines[desired_line - 1]) - blank_spaces
    except IndexError:
        return None, None
    else:
        return start_position, end_position


def extract_function_start_end_bytes(
    source_code: bytes,
    desired_line: int,
    *,
    language: str,
) -> tuple[int, int] | None:
    language = TREE_SITTER_LANGUAGE_CONVERSION.get(language) or language

    if language not in TREE_SITTER_FUNCTION_DECLARATION_MAP:
        raise InvalidFileType

    func_nodes = extract_function_nodes(source_code, desired_line, language=language)
    if not func_nodes:
        return None

    return (func_nodes[0].start_byte, func_nodes[-1].end_byte)


def extract_imports(source_code: str, language: str) -> tuple[Node, ...]:
    language = TREE_SITTER_LANGUAGE_CONVERSION.get(language) or language
    if language not in TREE_SITTER_IMPORTS_DECLARATIONS_MAP:
        return ()

    tree = parse_content_tree_sitter(source_code.encode("utf-8"), language)
    result = query_nodes_by_language(language, tree, TREE_SITTER_IMPORTS_DECLARATIONS_MAP)
    response = tuple(node for nodes in result.values() for node in nodes)
    return response


def indent_function(file_content_bytes: bytes, new_function: str, function_location: int) -> str:
    indentation = (
        file_content_bytes[
            function_location
            - next(
                (
                    index
                    for index, character in enumerate(
                        reversed(file_content_bytes[:function_location]),
                    )
                    if character
                    not in (
                        10,  # newline
                        32,  # space
                    )
                ),
                0,
            ) : function_location
        ]
        .decode(encoding="utf-8")
        .replace("\n", "")
    )
    return "\n".join([indentation + line if line else line for line in new_function.splitlines()])
