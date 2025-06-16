use pyo3::prelude::*;
#[allow(unused_imports)]
use std::collections::{HashMap, HashSet}; // These ARE needed for char_utils return types

mod char_utils;
mod solver;
mod trie;

use char_utils::CharCounts as RustCharCounts;
use solver::{
    AnagramSolver as RustAnagramSolver, ProcessedPattern as RustProcessedPattern,
    SolverConstraints as RustSolverConstraints,
};

#[pyclass(name = "Solver")]
struct PySolver {
    solver: RustAnagramSolver,
}

#[pymethods]
impl PySolver {
    #[new]
    fn new() -> Self {
        PySolver {
            solver: RustAnagramSolver::new(),
        }
    }

    fn load_dictionary_from_words(&mut self, words: Vec<String>) {
        self.solver.load_dictionary_from_words(&words);
    }

    fn load_dictionary_from_path(&mut self, path: String) -> PyResult<()> {
        let content = std::fs::read_to_string(path).map_err(|e| {
            PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                "Failed to read dictionary: {}",
                e
            ))
        })?;
        self.solver.load_dictionary_from_text(&content);
        Ok(())
    }

    fn add_word(&mut self, word: String) {
        self.solver.add_word(&word);
    }

    #[allow(clippy::too_many_arguments)]
    #[pyo3(signature = (
        phrase,
        must_start_with=None,
        can_only_ever_start_with=None,
        must_not_start_with=None,
        max_words=None,
        min_word_length=None,
        timeout_seconds=None,
        max_solutions=None,
        contains_patterns=None
    ))]
    fn solve(
        &self,
        phrase: String,
        must_start_with: Option<String>,
        can_only_ever_start_with: Option<String>,
        must_not_start_with: Option<String>,
        max_words: Option<usize>,
        min_word_length: Option<usize>,
        timeout_seconds: Option<f64>,
        max_solutions: Option<usize>,
        contains_patterns: Option<Vec<String>>,
    ) -> PyResult<Vec<Vec<String>>> {
        let processed_patterns_opt: Option<Vec<RustProcessedPattern>> =
            contains_patterns.map(|patterns_vec| {
                patterns_vec
                    .into_iter()
                    .filter_map(|p_str| {
                        let normalized_text = char_utils::normalize_word(&p_str); // Use char_utils directly
                        if normalized_text.is_empty() {
                            None // Skip empty patterns
                        } else {
                            // It's better if CharCounts::from_str ignores non-alphabetic
                            // or if normalize_word ensures only alphabetic.
                            // Assuming normalize_word ensures pattern is only alphabetic.
                            match RustCharCounts::from_str(&normalized_text) {
                                Ok(counts) => Some(RustProcessedPattern {
                                    text: normalized_text,
                                    counts,
                                }),
                                Err(_) => None, // Should not happen if normalized_text is good
                            }
                        }
                    })
                    .collect()
            });

        // These parse functions return Option<HashMap/HashSet> so those types need to be in scope
        let rust_constraints = RustSolverConstraints {
            must_start_with: char_utils::parse_char_list_to_counts(must_start_with.as_deref()),
            can_only_ever_start_with: char_utils::parse_char_list_to_set(
                can_only_ever_start_with.as_deref(),
            ),
            must_not_start_with: char_utils::parse_char_list_to_set(must_not_start_with.as_deref()),
            max_words,
            min_word_length,
            timeout_seconds,
            max_solutions,
            contains_patterns: processed_patterns_opt,
        };

        let solutions = self.solver.solve(&phrase, &rust_constraints);
        Ok(solutions)
    }
}

#[pymodule]
fn core(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PySolver>()?;
    Ok(())
}
