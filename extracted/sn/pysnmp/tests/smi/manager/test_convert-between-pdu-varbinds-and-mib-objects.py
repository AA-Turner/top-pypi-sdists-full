import pytest
from unittest.mock import patch
from pysnmp.smi import builder, view, rfc1902, error


def test_add_asn1_mib_source():
    mibBuilder = builder.MibBuilder()
    mibView = view.MibViewController(mibBuilder)
    mibVar = rfc1902.ObjectIdentity("IF-MIB", "ifInOctets", 1)
    mibVar.add_asn1_mib_source("https://mibs.pysnmp.com/asn1/@mib@")
    identity = mibVar.resolve_with_mib(mibView)
    assert mibVar.prettyPrint() == "IF-MIB::ifInOctets.1"

    module, symbol, name = identity.get_mib_symbol()
    assert symbol == "ifInOctets"

    next_module = mibView.get_next_module_name("IF-MIB")
    assert next_module == "SNMPv2-CONF"

    oid, label, suffix = mibView.get_first_node_name()
    oid, label, suffix = mibView.get_next_node_name(oid)
    assert oid == (0, 0)
    assert label == ("itu-t", "zeroDotZero")
