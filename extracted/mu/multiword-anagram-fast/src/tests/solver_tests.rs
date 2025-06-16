use multiword_anagram_fast_core::solver::{AnagramSolver, SolverConstraints, ProcessedPattern};
use multiword_anagram_fast_core::char_utils::CharCounts; // If needed for setup
use std::collections::{HashMap, HashSet}; // For constraints

fn create_solver_with_basic_dict() -> AnagramSolver {
    let mut solver = AnagramSolver::new();
    solver.add_word("eleven");
    solver.add_word("ate");
    solver.add_word("eat");
    solver.add_word("tea");
    solver.add_word("ten");
    solver.add_word("eel");
    solver.add_word("even");
    solver.add_word("net");
    solver.add_word("lane");
    solver.add_word("vat");
    solver.add_word("van");
    solver
}

fn process_patterns(patterns: Option<Vec<&str>>) -> Option<Vec<ProcessedPattern>> {
    patterns.map(|ps| {
        ps.into_iter()
            .map(|s| {
                let text = multiword_anagram_fast_core::char_utils::normalize_word(s);
                let counts = CharCounts::from_str(&text).unwrap();
                ProcessedPattern { text, counts }
            })
            .collect()
    })
}


#[test]
fn test_solve_eleven_exact_match() {
    let solver = create_solver_with_basic_dict();
    let constraints = SolverConstraints {
        must_start_with: None,
        can_only_ever_start_with: None,
        must_not_start_with: None,
        max_words: None,
        min_word_length: None,
        timeout_seconds: None,
        max_solutions: None,
        contains_patterns: None,
    };
    let solutions = solver._solve("eleven", &constraints);
    assert!(solutions.contains(&vec!["eleven".to_string()]), "Solution 'eleven' missing for input 'eleven'");
}

#[test]
fn test_solve_eleven_ate() {
    let solver = create_solver_with_basic_dict();
    let constraints = SolverConstraints { /* ... all None ... */ };
    let solutions = solver._solve("elevenate", &constraints); // Normalized input
    
    // Check for a few expected solutions (order within inner vec matters due to sort)
    let expected_solution1 = vec!["ate".to_string(), "eleven".to_string()];
    let mut found_expected1 = false;
    for sol in &solutions {
        let mut sorted_sol = sol.clone();
        sorted_sol.sort(); // Sort to make comparison order-independent for the set of words
        if sorted_sol == expected_solution1 {
            found_expected1 = true;
            break;
        }
    }
    assert!(found_expected1, "Solution ['ate', 'eleven'] missing for 'elevenate'. Solutions found: {:?}", solutions);
}

#[test]
fn test_solve_with_min_word_length() {
    let solver = create_solver_with_basic_dict();
    let constraints = SolverConstraints {
        min_word_length: Some(4),
        // ... rest None ...
    };
    let solutions = solver._solve("elevenate", &constraints);
    for sol in &solutions {
        for word in sol {
            assert!(word.len() >= 4, "Word '{}' in solution {:?} is too short", word, sol);
        }
    }
    // Check that "eleven" (len 6) + "ate" (len 3) is NOT a solution
    // but "even" (len 4) + "lane" (len 4) + "t" (len 1, but filtered by min_len) might be part of path
    // For "elevenate", "eleven" + "ate" -> ate is < 4, so this pair won't appear.
    // Possible: "lane" + "even" + "t" (if t existed, but it's filtered)
    // "eleven" is >=4, "ate" is not. So ["eleven", "ate"] should not be there.
    // Only ["eleven"] could be a sub-part if the remaining letters for "ate" can't form word >=4
}

#[test]
fn test_solve_with_contains_pattern() {
    let solver = create_solver_with_basic_dict();
    let constraints = SolverConstraints {
        contains_patterns: process_patterns(Some(vec!["VEN"])),
        // ... rest None ...
    };
    let solutions = solver._solve("elevenate", &constraints); // eleven, ate
    assert!(!solutions.is_empty(), "Should find solutions for 'elevenate' with pattern 'VEN'");
    for sol in &solutions {
        let mut pattern_found_in_solution = false;
        for word in sol {
            if word.contains("ven") { // Normalized pattern
                pattern_found_in_solution = true;
                break;
            }
        }
        assert!(pattern_found_in_solution, "Pattern 'VEN' not found in solution {:?}", sol);
    }
}