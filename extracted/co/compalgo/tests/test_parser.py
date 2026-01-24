"""
Tests for PyTeal and TEAL parsers
"""
from compalgo.analyzer.parser import PyTealParser
from compalgo.analyzer.teal_parser import parse_teal_signals


def test_pyteal_parser_extract_signals():
    """Test PyTeal parser extracts key signals"""
    code = '''
from pyteal import *

def app():
    on_delete = Seq([
        App.globalDel(Bytes("owner")),
        Approve()
    ])
    return Cond(
        [Txn.on_completion() == OnComplete.DeleteApplication, on_delete]
    )
'''
    parser = PyTealParser()
    signals = parser.extract_signals(code)
    assert "has_delete_application" in signals
    assert signals["has_delete_application"] is True
    assert "has_global_del" in signals
    assert signals["has_global_del"] is True


def test_teal_parser_extract_opcodes():
    """Test TEAL parser detects opcodes"""
    teal = '''
txn OnCompletion
int DeleteApplication
==
bnz delete_branch
delete_branch:
byte "key"
app_global_del
int 1
return
'''
    signals = parse_teal_signals(teal)
    assert signals["has_delete_application"] is True
    assert signals["has_global_del"] is True


def test_teal_parser_rekey_detection():
    """Test TEAL parser detects RekeyTo usage"""
    teal = '''
txn RekeyTo
global ZeroAddress
==
assert
'''
    signals = parse_teal_signals(teal)
    assert signals["has_rekey_to_check"] is True


if __name__ == "__main__":
    test_pyteal_parser_extract_signals()
    test_teal_parser_extract_opcodes()
    test_teal_parser_rekey_detection()
    print("All parser tests passed!")
