from rdflib import Namespace

from ShExJSG import ShExJ

from pyshexc.parser_impl.generate_shexj import parse
from tests import git_branch

BASE = Namespace(f"https://raw.githubusercontent.com/shexSpec/shexTest/{git_branch}/validation/")
FOO = Namespace("/some/location/file/")
EX = Namespace("http://example.org/")


def test_no_base():
    shex_str = '<S1> {<p1> [<o1>]}'
    shex: ShExJ.Schema = parse(shex_str)
    assert "S1" == str(shex.shapes[0].id)
    assert "p1" == str(shex.shapes[0].expression.predicate)
    assert "o1" == str(shex.shapes[0].expression.valueExpr.values[0])


def test_default_base():
    shex_str = '<S1> {<p1> [<o1>]}'
    shex: ShExJ.Schema = parse(shex_str, str(BASE))
    assert str(BASE.S1) == str(shex.shapes[0].id)
    assert str(BASE.p1) == str(shex.shapes[0].expression.predicate)
    assert str(BASE.o1) == str(shex.shapes[0].expression.valueExpr.values[0])


def test_explicit_base():
    shex_str = f'BASE <{str(FOO)}>\n<S1> {{<p1> [<o1>]}}'
    shex: ShExJ.Schema = parse(shex_str, str(BASE))
    assert str(FOO.S1) == str(shex.shapes[0].id)
    assert str(FOO.p1) == str(shex.shapes[0].expression.predicate)
    assert str(FOO.o1) == str(shex.shapes[0].expression.valueExpr.values[0])


def test_explicit_uris():
    shex_str = f"""
BASE <{str(FOO)}>
PREFIX ex: <{EX}>

ex:S1 {{ex:p1 [ex:o1]}}"""
    shex: ShExJ.Schema = parse(shex_str, str(BASE))
    assert str(EX.S1) == str(shex.shapes[0].id)
    assert str(EX.p1) == str(shex.shapes[0].expression.predicate)
    assert str(EX.o1) == str(shex.shapes[0].expression.valueExpr.values[0])
