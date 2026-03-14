import pathlib
import sys


ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from nsj_rest_lib2.compiler.util.relation_ref import RelationRefParser


def test_relation_ref_parser_accepts_hierarchical_scope():
    relation_ref = RelationRefParser.parse("RH.JOR.PNT/regra")

    assert relation_ref is not None
    assert relation_ref.ref_type == "external"
    assert relation_ref.scope == "RH.JOR.PNT"
    assert relation_ref.entity == "regra"
    assert relation_ref.components == []


def test_relation_ref_parser_accepts_hierarchical_scope_with_components():
    relation_ref = RelationRefParser.parse(
        "GVN.INF.MDG/pessoa/documentos/identidade"
    )

    assert relation_ref is not None
    assert relation_ref.ref_type == "external_component"
    assert relation_ref.scope == "GVN.INF.MDG"
    assert relation_ref.entity == "pessoa"
    assert relation_ref.components == ["documentos", "identidade"]
