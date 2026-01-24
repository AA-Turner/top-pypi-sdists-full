"""Tests for Leo parser."""

import pytest
from comp_leo.analyzer.parser import LeoParser


def test_parse_simple_program():
    """Test parsing a simple Leo program."""
    source = """
program simple.aleo {
    transition hello() {
        return;
    }
}
"""
    
    parser = LeoParser()
    program = parser.parse_source(source, "test.leo")
    
    assert program.name == "simple"
    assert len(program.transitions) == 1
    assert program.transitions[0].name == "hello"


def test_parse_struct():
    """Test parsing struct definitions."""
    source = """
program test.aleo {
    struct Entry {
        hash: field,
        value: u64,
    }
}
"""
    
    parser = LeoParser()
    program = parser.parse_source(source)
    
    assert len(program.structs) == 1
    assert program.structs[0].name == "Entry"
    assert len(program.structs[0].fields) == 2


def test_parse_mapping():
    """Test parsing mapping definitions."""
    source = """
program test.aleo {
    mapping balances: address => u64;
}
"""
    
    parser = LeoParser()
    program = parser.parse_source(source)
    
    assert len(program.mappings) == 1
    assert program.mappings[0].name == "balances"
    assert program.mappings[0].key_type == "address"
    assert program.mappings[0].value_type == "u64"


def test_parse_transition_with_params():
    """Test parsing transition with parameters."""
    source = """
program test.aleo {
    transition transfer(public recipient: address, public amount: u64) {
        assert(amount > 0u64);
        return;
    }
}
"""
    
    parser = LeoParser()
    program = parser.parse_source(source)
    
    assert len(program.transitions) == 1
    transition = program.transitions[0]
    assert transition.name == "transfer"
    assert len(transition.parameters) == 2
    assert transition.parameters[0]["name"] == "recipient"
    assert transition.parameters[0]["type"] == "address"
    assert transition.has_assertions


def test_detect_state_mutation():
    """Test detection of state-mutating operations."""
    source = """
program test.aleo {
    mapping entries: field => u64;
    
    transition update(key: field, value: u64) {
        Mapping::set(entries, key, value);
    }
}
"""
    
    parser = LeoParser()
    program = parser.parse_source(source)
    
    assert program.transitions[0].modifies_state
    assert program.transitions[0].has_mappings
