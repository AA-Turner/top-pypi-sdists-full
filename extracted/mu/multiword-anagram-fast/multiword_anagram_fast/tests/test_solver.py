import pytest
from multiword_anagram_fast import AnagramSolver 
import os

# Fixture to create a solver instance with a test dictionary
@pytest.fixture
def solver_with_test_dict(tmp_path): # tmp_path is a pytest fixture for temporary dirs
    solver = AnagramSolver()
    dict_content = "eleven\nate\neat\ntea\nten\neel\neven\nnet\nlane\nvat\nvan\nlisten\nsilent\n"
    dict_file = tmp_path / "test_dict.txt"
    dict_file.write_text(dict_content)
    solver.load_dictionary_file(str(dict_file))
    return solver

def test_solve_eleven_exact_match_python(solver_with_test_dict):
    solutions = solver_with_test_dict._solve("eleven",contains_patterns=["LEV"])
    # Convert solution lists to sets of frozensets for order-independent comparison
    solution_sets = {frozenset(s) for s in solutions}
    assert frozenset({'eleven'}) in solution_sets

def test_solve_eleven_ate_python(solver_with_test_dict):
    solutions = solver_with_test_dict._solve("elevenate",min_word_length=3) # normalized input
    solution_sets = {frozenset(s) for s in solutions}
    
    expected_sets = [
        frozenset(["eleven", "ate"]),
        frozenset(["eleven", "eat"]),
        frozenset(["eleven", "tea"]),
    ]
    # Check if at least one of the expected angrams for "ate" is present with "eleven"
    found = any(es in solution_sets for es in expected_sets)
    assert found, f"Expected anagrams for 'elevenate' not found. Got: {solutions}"

def test_solve_with_min_word_length_python(solver_with_test_dict):
    solutions = solver_with_test_dict._solve("elevenate", min_word_length=4)
    for sol in solutions:
        for word in sol:
            assert len(word) >= 4
    # Check that ["eleven", "ate"] is NOT a solution because "ate" is too short
    solution_tuples = {tuple(sorted(s)) for s in solutions} # For easier checking
    assert tuple(sorted(["eleven", "ate"])) not in solution_tuples

def test_solve_with_contains_pattern_python(solver_with_test_dict):
    solutions = solver_with_test_dict._solve("elevenate", contains_patterns=["VEN"])
    assert len(solutions) > 0, "Should find solutions with pattern VEN"
    for sol in solutions:
        assert any("ven" in word for word in sol), f"Pattern 'ven' not found in {sol}"


def test_solve_start_with_only_n(solver_with_test_dict):
    solutions = solver_with_test_dict._solve("ten", must_start_with="n") # normalized input
    solution_sets = {frozenset(s) for s in solutions}
    
    expected_sets = [
        frozenset(["net"]),
    ]
    # Check if at least one of the expected angrams for "ate" is present with "eleven"
    found = any(es in solution_sets for es in expected_sets)
    assert found, f"Expected anagrams for 'ten' beginning with n were not found. Got: {solutions}"


def test_solve_listen_silent_regression(solver_with_test_dict):
    # A known regression test case
    solutions = solver_with_test_dict._solve("listensilent", 
                                can_only_ever_start_with="sl",min_word_length=4) # 12 letters
    solution_sets = {frozenset(s) for s in solutions}
    
    expected_core_anagrams = [
        frozenset(["listen", "silent"]),
        # Add other known 2-word solutions if they exist in your small test_dict
    ]
    # Depending on dictionary, could also be 3 words etc.
    # This test is for the basic 2-word anagram.
    found = any(es in solution_sets for es in expected_core_anagrams)
    assert found, f"Expected 'listen silent' anagrams not found. Got: {solutions}"
