import textwrap

import pytest

from fluidattacks_core.serializers.snippet import (
    SnippetViewport,
    extract_function,
    make_snippet,
    make_snippet_function,
)
from fluidattacks_core.serializers.syntax import (
    InvalidFileType,
    extract_function_start_end_bytes,
    extract_imports,
    parse_content_tree_sitter,
    query_function_by_name,
)


def _dedent(content: str) -> str:
    return textwrap.dedent(content)[1:-1]


@pytest.mark.parametrize(
    "content, viewport, expected",  # noqa: PT006
    [
        (
            """
            aaaaaaaaaabbbbbbbbbbcccccccccc
            ddddddddddeeeeeeeeeeffffffffff
            gggggggggghhhhhhhhhhiiiiiiiiii
            jjjjjjjjjjkkkkkkkkkkllllllllll
            """,
            None,
            """
            aaaaaaaaaabbbbbbbbbbcccccccccc
            ddddddddddeeeeeeeeeeffffffffff
            gggggggggghhhhhhhhhhiiiiiiiiii
            jjjjjjjjjjkkkkkkkkkkllllllllll
            """,
        ),
        (
            """
            aaaaaaaaaabbbbbbbbbbcccccccccc
            ddddddddddeeeeeeeeeeffffffffff
            gggggggggghhhhhhhhhhiiiiiiiiii
            jjjjjjjjjjkkkkkkkkkkllllllllll
            """,
            SnippetViewport(
                columns_per_line=20,
                column=10,
                line=2,
                line_context=1,
                wrap=True,
            ),
            """
                | ccccc
            > 2 | dddddeeeeeeeeee
                | fffff
                ^ Col 5
            """,
        ),
        (
            """
                1 center
                2
                3
                4
                5
                6
            """,
            SnippetViewport(column=10, line=1, line_context=2),
            """
                > 1 | 1 center
                  2 | 2
                  3 | 3
                  4 | 4
                  5 | 5
                    ^ Col 0
            """,
        ),
        (
            """
                1
                2 center
                3
                4
                5
                6
            """,
            SnippetViewport(column=10, line=2, line_context=2),
            """
                  1 | 1
                > 2 | 2 center
                  3 | 3
                  4 | 4
                  5 | 5
                    ^ Col 0
            """,
        ),
        (
            """
                1
                2
                3 center
                4
                5
                6
            """,
            SnippetViewport(column=10, line=3, line_context=2),
            """
                  1 | 1
                  2 | 2
                > 3 | 3 center
                  4 | 4
                  5 | 5
                    ^ Col 0
            """,
        ),
        (
            """
                1
                2
                3
                4 center
                5
                6
                7
                8
                9
            """,
            SnippetViewport(column=10, line=4, line_context=2),
            """
                  2 | 2
                  3 | 3
                > 4 | 4 center
                  5 | 5
                  6 | 6
                    ^ Col 0
            """,
        ),
        (
            """
                1
                2
                3
                4
                5 center
                6
            """,
            SnippetViewport(column=10, line=5, line_context=2),
            """
                  2 | 2
                  3 | 3
                  4 | 4
                > 5 | 5 center
                  6 | 6
                    ^ Col 0
            """,
        ),
        (
            """
                1
                2
                3
                4
                5
                6 center
            """,
            SnippetViewport(column=10, line=6, line_context=2),
            """
                  2 | 2
                  3 | 3
                  4 | 4
                  5 | 5
                > 6 | 6 center
                    ^ Col 0
            """,
        ),
    ],
)
def test_make_snippet(content: str, viewport: str, expected: str) -> None:
    result = make_snippet(content=_dedent(content), viewport=viewport)  # type: ignore[arg-type]
    assert result is not None
    assert result.content == _dedent(expected)


def test_make_snippet_function() -> None:
    item = _dedent("""
def get_tokens_per_message(message: ConverseMessage) -> int:
    token_params = get_token_params()
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")

    num_tokens = token_params.tokens_per_message
    for key, value in message._asdict().items():
        num_tokens += len(encoding.encode(str(value)))
        if key == "role":
            num_tokens += token_params.tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def build_lines_vuln(
    method: MethodInfo,
    what: str,
    where: str,
    metadata: SkimsVulnerabilityMetadata,
) -> Vulnerability:
    kind = VulnerabilityTechnique.SAST
    if method.technique == VulnerabilityTechnique.SCA:
        kind = VulnerabilityTechnique.SCA

    return Vulnerability(
        finding=method.finding,
        kind=kind,
        vulnerability_type=VulnerabilityType.LINES,
        namespace=ctx.SKIMS_CONFIG.namespace,
        what=what,
        where=where,
        skims_metadata=metadata,
    )

    """)
    result = make_snippet_function(
        file_content=item,
        language="python",
        viewport=SnippetViewport(
            column=10,
            line=22,
            line_context=2,
            show_line_numbers=False,
            highlight_line_number=False,
        ),
    )
    assert result is not None
    assert result.content == _dedent(
        """
def build_lines_vuln(
    method: MethodInfo,
    what: str,
    where: str,
    metadata: SkimsVulnerabilityMetadata,
) -> Vulnerability:
    kind = VulnerabilityTechnique.SAST
    if method.technique == VulnerabilityTechnique.SCA:
        kind = VulnerabilityTechnique.SCA

    return Vulnerability(
        finding=method.finding,
        kind=kind,
        vulnerability_type=VulnerabilityType.LINES,
        namespace=ctx.SKIMS_CONFIG.namespace,
        what=what,
        where=where,
        skims_metadata=metadata,
    )
""",
    )
    assert result is not None
    assert result.line_context == 8
    assert result.reshape(
        viewport=SnippetViewport(
            column=10,
            line=22,
            line_context=2,
            show_line_numbers=False,
            highlight_line_number=False,
        ),
    ).content == (
        """    kind = VulnerabilityTechnique.SAST
    if method.technique == VulnerabilityTechnique.SCA:
        kind = VulnerabilityTechnique.SCA

    return Vulnerability("""
    )

    assert (
        result.reshape(
            viewport=SnippetViewport(
                column=10,
                line=22,
                line_context=2,
                show_line_numbers=False,
                highlight_line_number=False,
            ),
        ).line_context
        == 2
    )

    assert result.reshape(
        viewport=SnippetViewport(
            column=10,
            line=22,
            line_context=2,
            show_line_numbers=True,
            highlight_line_number=True,
        ),
    ).content == (
        """  20 |     kind = VulnerabilityTechnique.SAST
  21 |     if method.technique == VulnerabilityTechnique.SCA:
> 22 |         kind = VulnerabilityTechnique.SCA
  23 |
  24 |     return Vulnerability(
     ^ Col 0"""
    )
    # Highlight the lines, but then remov
    assert result.reshape(
        viewport=SnippetViewport(
            column=10,
            line=22,
            line_context=2,
            show_line_numbers=True,
            highlight_line_number=True,
        ),
    ).reshape(
        viewport=SnippetViewport(
            column=10,
            line=22,
            line_context=2,
            show_line_numbers=False,
            highlight_line_number=False,
        ),
    ).content == (
        """    kind = VulnerabilityTechnique.SAST
    if method.technique == VulnerabilityTechnique.SCA:
        kind = VulnerabilityTechnique.SCA

    return Vulnerability("""
    )

    assert result.reshape(
        viewport=SnippetViewport(
            column=10,
            line=22,
            line_context=2,
            show_line_numbers=False,
            highlight_line_number=False,
        ),
    ).reshape(
        viewport=SnippetViewport(
            column=10,
            line=22,
            line_context=2,
            show_line_numbers=True,
            highlight_line_number=True,
        ),
    ).content == (
        """  20 |     kind = VulnerabilityTechnique.SAST
  21 |     if method.technique == VulnerabilityTechnique.SCA:
> 22 |         kind = VulnerabilityTechnique.SCA
  23 |
  24 |     return Vulnerability(
     ^ Col 0"""
    )


def test_make_snippet_function_1() -> None:
    a = _dedent("""
def get_tokens_per_message(message: ConverseMessage) -> int:
    token_params = get_token_params()
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")

    num_tokens = token_params.tokens_per_message
    for key, value in message._asdict().items():
        num_tokens += len(encoding.encode(str(value)))
        if key == "role":
            num_tokens += token_params.tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def build_lines_vuln(
    method: MethodInfo,
    what: str,
    where: str,
    metadata: SkimsVulnerabilityMetadata,
) -> Vulnerability:
    kind = VulnerabilityTechnique.SAST
    if method.technique == VulnerabilityTechnique.SCA:
        kind = VulnerabilityTechnique.SCA

    return Vulnerability(
        finding=method.finding,
        kind=kind,
        vulnerability_type=VulnerabilityType.LINES,
        namespace=ctx.SKIMS_CONFIG.namespace,
        what=what,
        where=where,
        skims_metadata=metadata,
    )

    """)
    result = make_snippet(
        content=a,
        viewport=SnippetViewport(
            column=10,
            line=22,
            line_context=2,
            show_line_numbers=False,
            highlight_line_number=True,
        ),
    )
    assert result.content == (
        """    kind = VulnerabilityTechnique.SAST
    if method.technique == VulnerabilityTechnique.SCA:
        kind = VulnerabilityTechnique.SCA

    return Vulnerability("""
    )


def test_extract_python_function() -> None:
    source = """
def sum(a, b):
    return a + b

def product(a, b):
    return a * b

async def product_async(a, b):
    return a * b
    """
    line = 3
    expected = "def sum(a, b):\n    return a + b"
    assert extract_function(source, line, language="python").content == expected  # type: ignore[union-attr]
    assert (
        extract_function(source, 9, language="python").content  # type: ignore[union-attr]
        == "async def product_async(a, b):\n    return a * b"
    )


def test_extract_java_method() -> None:
    source = """
public class Calculator {

    public int sum(int a, int b) {
        return a + b;
    }

    public int product(int a, int b) {
        return a * b;
    }

}
    """
    line = 5
    expected = "public int sum(int a, int b) {\n        return a + b;\n    }"
    result = extract_function(source, line, language="java")
    assert result is not None
    assert result.content == expected


def test_line_not_in_function() -> None:
    source = """
def sum(a, b):
    return a + b

print("Hello")
    """
    line = 4
    assert extract_function(source, line, language="python") is None


def test_invalid_language() -> None:
    source = "def sum(a, b):\\n    return a + b"
    line = 1
    with pytest.raises(InvalidFileType):
        extract_function(source, line, language="c")


def test_extract_csharp_method() -> None:
    source = """
public class Calculator {

  public int Sum(int a, int b)
  {
    return a + b;
  }

  public Calculator() {
    return 1;
  }

}
  """

    line = 6
    expected = "public int Sum(int a, int b)\n  {\n    return a + b;\n  }"

    result = extract_function(source, line, language="c_sharp")
    assert result is not None
    assert result.content == expected


@pytest.mark.skip(reason="The parser is not available")
def test_extract_dart_function() -> None:
    source = """
void main() {
  print("Hello, World!");
}
  """

    line = 3
    expected = 'void main() {\n  print("Hello, World!");\n}'
    result = extract_function(source, line, language="dart")
    assert result is not None
    assert result.content == expected


def test_extract_go_function() -> None:
    source = """
func sum(a, b int) int {
  return a + b
}

func printMessage() {
  fmt.Println("Hello")
}
  """

    line = 3
    expected = "func sum(a, b int) int {\n  return a + b\n}"

    result = extract_function(source, line, language="go")
    assert result is not None
    assert result.content == expected


def test_extract_javascript_function() -> None:
    source = """
const sum = (a, b) => {
  return a + b;
}

function printMessage() {
  console.log('Hello');
}
  """

    line = 3
    expected = "(a, b) => {\n  return a + b;\n}"
    result = extract_function(source, line, language="javascript")
    assert result is not None
    assert result.content == expected


@pytest.mark.skip(reason="The parser is not available")
def test_extract_kotlin_function() -> None:
    source = """
fun sum(a: Int, b: Int): Int {
  return a + b
}

fun printMessage() {
  print("Hello")
}
  """

    line = 3
    expected = "fun sum(a: Int, b: Int): Int {\n  return a + b\n}"

    result = extract_function(source, line, language="kotlin")
    assert result is not None
    assert result.content == expected


def test_extract_php_function() -> None:
    source = """
<?php
function sum($a, $b) {
  return $a + $b;
}

function printMessage() {
  echo "Hello";
}
?>
  """

    line = 4
    expected = "function sum($a, $b) {\n  return $a + $b;\n}"

    result = extract_function(source, line, language="php")
    assert result is not None
    assert result.content == expected


@pytest.mark.skip(reason="The parser is not available")
def test_extract_ruby_method() -> None:
    source = """
def sum(a, b)
  a + b
end

def print_message
  puts "Hello"
end
  """

    line = 3
    expected = "def sum(a, b)\n  a + b\nend"

    result = extract_function(source, line, language="ruby")
    assert result is not None
    assert result.content == expected


@pytest.mark.skip(reason="The parser is not available")
def test_extract_scala_function() -> None:
    source = """
def sum(a: Int, b: Int): Int = {
  a + b
}

def printMessage(): Unit = {
  println("Hello")
}
  """

    line = 3
    expected = "def sum(a: Int, b: Int): Int = {\n  a + b\n}"

    result = extract_function(source, line, language="scala")
    assert result is not None
    assert result.content == expected


@pytest.mark.skip(reason="The parser is not available")
def test_extract_swift_function() -> None:
    source = """
func sum(_ a: Int, _ b: Int) -> Int {
  return a + b
}

func printMessage() {
  print("Hello")
}
  """

    line = 3
    expected = "func sum(_ a: Int, _ b: Int) -> Int {\n  return a + b\n}"

    result = extract_function(source, line, language="swift")
    assert result is not None
    assert result.content == expected


@pytest.mark.skip(reason="The parser is not available")
def test_extract_tsx_function() -> None:
    source = """
const sum = (a: number, b: number) => {
  return a + b;
}

function printMessage() {
  console.log("Hello");
}
  """

    line = 3
    expected = "(a: number, b: number) => {\n  return a + b;\n}"

    result = extract_function(source, line, language="tsx")
    assert result is not None
    assert result.content == expected


@pytest.mark.skip(reason="The parser is not available")
def test_extract_terraform_function() -> None:
    source = """
resource "kubernetes_secret_v1" "name" {
  metadata {
    name      = "integrates"
    namespace = "name"
  }
  data = {
    "AUTH_TOKEN"  = "sensitive value"
  }
}
  """

    line = 8
    expected = (
        'resource "kubernetes_secret_v1" "name" {\n  metadata {\n    '
        'name      = "integrates"\n    namespace = "name"\n  }\n  data = {\n'
        '    "AUTH_TOKEN"  = "sensitive value"\n  }\n}'
    )

    result = extract_function(source, line, language="hcl")
    assert result is not None
    assert result.content == expected


def test_extract_yaml_function() -> None:
    source = """
aws_acces_key: xxxxxxxxxxx
aws_secret_access_key: xxxxxxxxxx"""

    line = 3
    expected = "aws_acces_key: xxxxxxxxxxx\naws_secret_access_key: xxxxxxxxxx"

    result = extract_function(source, line, language="yaml")
    assert result is not None
    assert result.content == expected


def test_extract_function_start_end_bytes() -> None:
    source = """
def sum(a, b):
    return a + b

def product(a, b):
    return a * b
    """
    line = 3
    assert extract_function_start_end_bytes(source.encode("utf-8"), line, language="python") == (
        1,
        32,
    )


def test_extract_imports_java() -> None:
    source = """
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
    """
    assert sorted(node.text.decode() for node in extract_imports(source, language="java")) == [  # type: ignore[union-attr]
        "import java.io.IOException;",
        "import javax.servlet.ServletException;",
        "import javax.servlet.annotation.WebServlet;",
        "import javax.servlet.http.HttpServlet;",
    ]


def test_extract_imports_c_sharp() -> None:
    source = """
using System;
using System.Collections.Generic;
    """
    assert sorted(node.text.decode() for node in extract_imports(source, language="c_sharp")) == [  # type: ignore[union-attr]
        "using System.Collections.Generic;",
        "using System;",
    ]


@pytest.mark.skip(reason="The parser is not available")
def test_extract_imports_dart() -> None:
    source = """
import 'package:test/test.dart';
import 'package:lib1/lib1.dart';
import 'package:lib2/lib2.dart' as lib2;
import 'package:lib1/lib1.dart' show foo;
import 'package:lib2/lib2.dart' hide foo;
import 'package:greetings/hello.dart' deferred as hello;
    """
    assert tuple(node.text.decode() for node in extract_imports(source, language="dart")) == (  # type: ignore[union-attr]
        "import 'package:test/test.dart';",
        "import 'package:lib1/lib1.dart';",
        "import 'package:lib2/lib2.dart' as lib2;",
        "import 'package:lib1/lib1.dart' show foo;",
        "import 'package:lib2/lib2.dart' hide foo;",
        "import 'package:greetings/hello.dart' deferred as hello;",
    )


@pytest.mark.skip(reason="The parser is not available")
def test_extract_imports_go() -> None:
    source = """
import "fmt"
import "math"

import(
    "fmt"
    "math"
)

import "math/rand"

import m "math"
import f "fmt"
    """
    assert tuple(node.text.decode() for node in extract_imports(source, language="go")) == (  # type: ignore[union-attr]
        'import "fmt"',
        'import "math"',
        'import(\n    "fmt"\n    "math"\n)',
        'import "math/rand"',
        'import m "math"',
        'import f "fmt"',
    )


def test_extract_imports_javascript() -> None:
    source = """
import defaultExport from "module-name";
import * as name from "module-name";
import { export1 as alias1 } from "module-name";
    """
    assert sorted(node.text.decode() for node in extract_imports(source, language="go")) == [  # type: ignore[union-attr]
        'import * as name from "module-name"',
        'import defaultExport from "module-name"',
        'import { export1 as alias1 } from "module-name"',
    ]


@pytest.mark.skip(reason="The parser is not available")
def test_extract_imports_kotlin() -> None:
    source = """
import org.example.Message
import org.test.Message as TestMessage
    """
    assert tuple(node.text.decode() for node in extract_imports(source, language="kotlin")) == (  # type: ignore[union-attr]
        "import org.example.Message",
        "import org.test.Message as TestMessage",
    )


def test_extract_imports_php() -> None:
    source = """
  <?php
use ArrayObject;
?>
    """
    assert tuple(node.text.decode() for node in extract_imports(source, language="php")) == (  # type: ignore[union-attr]
        "use ArrayObject;",
    )


def test_extract_imports_python() -> None:
    source = """
import math
from math import pi
from math import pi
    """
    assert tuple(node.text.decode() for node in extract_imports(source, language="python")) == (  # type: ignore[union-attr]
        "import math",
        "from math import pi",
        "from math import pi",
    )


@pytest.mark.skip(reason="The parser is not available")
def test_extract_imports_swift() -> None:
    source = """
import UIKit
/// or
import UIKit.UIViewController
    """
    assert tuple(node.text.decode() for node in extract_imports(source, language="swift")) == (  # type: ignore[union-attr]
        "import UIKit",
        "import UIKit.UIViewController",
    )


@pytest.mark.skip(reason="The parser is not available")
def test_extract_imports_scala() -> None:
    source = """
import users._  // import everything from the users package
import users.User  // import the class User
import users.{User, UserPreferences}  // Only imports selected members
import users.{UserPreferences => UPrefs}  // import and rename for convenience
import users.*  // import everything from the users package except given
import users.given // import all given from the users package
import users.User  // import the class User
import users.{User, UserPreferences}  // Only imports selected members
import users.UserPreferences as UPrefs  // import and rename for convenience
    """
    assert tuple(node.text.decode() for node in extract_imports(source, language="scala")) == (  # type: ignore[union-attr]
        "import users._",
        "import users.User",
        "import users.{User, UserPreferences}",
        "import users.{UserPreferences => UPrefs}",
        "import users.*",
        "import users.given",
        "import users.User",
        "import users.{User, UserPreferences}",
        "import users.UserPreferences as UPrefs",
    )


def test_extract_not_imports() -> None:
    source = """
user: 'jan doe'
    """
    assert tuple(node.text.decode() for node in extract_imports(source, language="yaml")) == ()  # type: ignore[union-attr]


def test_find_function_by_name() -> None:
    language = "python"
    source_code = """
def test() -> None:
    print("test")
    """
    tree = parse_content_tree_sitter(source_code.encode("utf-8"), language)
    result = query_function_by_name(
        language=language,
        tree=tree,
        function_node_type="function_definition",
        node_identifier_name="identifier",
        function_name="test",
    )
    assert len(result) == 1
