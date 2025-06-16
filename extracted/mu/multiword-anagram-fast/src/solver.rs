use std::cmp::Ordering;
use std::collections::{HashMap, HashSet}; // Keep these for SolverConstraints
use std::fs::File; // <--- Add for file operations
use std::io::Write;
use std::time::Instant;

use super::char_utils::CharCounts;
use super::trie::{Trie, TrieNode};

// Preprocessed pattern structure
#[derive(Clone, Debug)] // Added Clone and Debug
pub struct ProcessedPattern {
    pub text: String, // Normalized text of the pattern
    pub counts: CharCounts,
    // original_index: usize, // If needed for mapping back
}

pub struct SolverInternalState {
    pub start_time: Instant,
    pub timed_out: bool,
    pub solutions_found_count: usize,
    pub patterns_satisfied_mask: Option<Vec<bool>>,
}

#[derive(Debug)]
pub struct SolverConstraints {
    pub must_start_with: Option<HashMap<char, usize>>,
    pub can_only_ever_start_with: Option<HashSet<char>>,
    pub must_not_start_with: Option<HashSet<char>>,
    pub max_words: Option<usize>,
    pub min_word_length: Option<usize>,
    pub timeout_seconds: Option<f64>,
    pub max_solutions: Option<usize>,
    pub contains_patterns: Option<Vec<ProcessedPattern>>,
}

impl SolverConstraints {
    fn is_valid_start_char(&self, c: char) -> bool {
        if let Some(disallowed) = &self.must_not_start_with {
            if disallowed.contains(&c) {
                return false;
            }
        }
        if let Some(allowed) = &self.can_only_ever_start_with {
            if !allowed.contains(&c) {
                return false;
            }
        }
        true
    }
}

const DEBUG_LOG_FILE: &str = "anagram_solver_debug.log";

pub struct AnagramSolver {
    trie: Trie,
}

impl AnagramSolver {
    pub fn new() -> Self {
        AnagramSolver { trie: Trie::new() }
    }

    pub fn load_dictionary_from_words(&mut self, words: &[String]) {
        for word in words {
            self.trie.insert(word);
        }
    }

    pub fn load_dictionary_from_text(&mut self, text_content: &str) {
        for line in text_content.lines() {
            self.trie.insert(line);
        }
    }

    pub fn add_word(&mut self, word: &str) {
        self.trie.insert(word);
    }

    #[allow(clippy::too_many_arguments)]
    pub fn solve(&self, phrase: &str, constraints: &SolverConstraints) -> Vec<Vec<String>> {
        // You run your Python script like: ANAGRAM_DEBUG_LOG=1 python your_script.py to enable logging.

        let enable_logging = std::env::var("ANAGRAM_DEBUG_LOG").is_ok();
        let mut log_file: Option<std::fs::File> = if enable_logging {
            std::fs::File::create(DEBUG_LOG_FILE)
                .map_err(|e| {
                    eprintln!("Failed to create log file {}: {}", DEBUG_LOG_FILE, e);
                    e
                })
                .ok()
        } else {
            None
        };

        //// ---> Open Log File <---
        //let mut log_file = File::create(DEBUG_LOG_FILE)
        //    .map_err(|e| {
        //        eprintln!("Failed to create log file {}: {}", DEBUG_LOG_FILE, e);
        //        e // Propagate error if you want to handle it more gracefully, or just let it be
        //    })
        //    .ok(); // Continue even if log file fails, by making it an Option<File>
        if let Some(file) = log_file.as_mut() {
            writeln!(file, "--- Solving for phrase: '{}' ---", phrase)
                .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
            writeln!(file, "Constraints: {:?}", constraints) // Need Debug on SolverConstraints
                .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
        }

        let target_counts = match CharCounts::from_str(phrase) {
            Ok(counts) => counts,
            Err(_) => return Vec::new(),
        };

        if target_counts.is_empty() || self.trie.get_min_word_len() == 0 {
            return Vec::new();
        }

        let mut solutions_set: HashSet<Vec<String>> = HashSet::new();
        let mut current_path: Vec<String> = Vec::new();
        let mut current_char_counts = target_counts.clone();

        let initial_patterns_mask = constraints
            .contains_patterns
            .as_ref()
            .map(|patterns| vec![false; patterns.len()]);

        let mut internal_state = SolverInternalState {
            start_time: Instant::now(),
            timed_out: false,
            solutions_found_count: 0,
            patterns_satisfied_mask: initial_patterns_mask,
        };

        self.backtrack(
            &mut current_path,
            &mut current_char_counts,
            &self.trie.root,
            constraints,
            &mut solutions_set,
            &mut internal_state,
            log_file.as_mut(),
        );
        if let Some(file) = log_file.as_mut() {
            writeln!(file, "--- Solve function finished ---")
                .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
        }

        let mut final_solutions: Vec<Vec<String>> = solutions_set.into_iter().collect();

        final_solutions.sort_by(|a, b| {
            let len_cmp = a.len().cmp(&b.len());
            if len_cmp != Ordering::Equal {
                return len_cmp;
            }
            let min_len_a = a.iter().map(|w| w.len()).min().unwrap_or(0);
            let min_len_b = b.iter().map(|w| w.len()).min().unwrap_or(0);
            min_len_b.cmp(&min_len_a).then_with(|| a.cmp(b))
        });

        final_solutions
    }

    #[allow(clippy::too_many_arguments)]
    fn backtrack(
        &self,
        current_path: &mut Vec<String>,
        remaining_counts: &mut CharCounts,
        _start_node_for_this_level: &TrieNode,
        constraints: &SolverConstraints,
        solutions_set: &mut HashSet<Vec<String>>,
        internal_state: &mut SolverInternalState,
        mut log_file: Option<&mut File>,
    ) {
        if let Some(file) = log_file.as_deref_mut() {
            // as_deref_mut for Option<&mut T> -> Option<&mut T>
            writeln!(
                file,
                "BACKTRACK ENTRY: path={:?}, remaining_total={}, timed_out={}, solutions_found={}",
                current_path,
                remaining_counts.total(),
                internal_state.timed_out,
                internal_state.solutions_found_count
            )
            .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
            if let Some(mask) = &internal_state.patterns_satisfied_mask {
                writeln!(file, "  Mask: {:?}", mask)
                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
            }
        }

        if internal_state.timed_out {
            if let Some(file) = log_file.as_deref_mut() {
                writeln!(file, "  Pruned: Timed out. Path: {:?}", current_path)
                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
            }
            return;
        }
        if let Some(timeout_sec) = constraints.timeout_seconds {
            if internal_state.start_time.elapsed().as_secs_f64() > timeout_sec {
                internal_state.timed_out = true;
                if let Some(file) = log_file.as_deref_mut() {
                    writeln!(
                        file,
                        "  Pruned: Timeout triggered NOW. Path: {:?}",
                        current_path
                    )
                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }
                return;
            }
        }
        if let Some(max_sol) = constraints.max_solutions {
            if internal_state.solutions_found_count >= max_sol {
                if let Some(file) = log_file.as_deref_mut() {
                    writeln!(
                        file,
                        "  Pruned: Max solutions reached. Path: {:?}",
                        current_path
                    )
                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }
                return;
            }
        }
        // Pattern-based pruning
        if let Some(patterns_to_satisfy) = &constraints.contains_patterns {
            if let Some(satisfied_mask) = &internal_state.patterns_satisfied_mask {
                let mut num_unsatisfied = 0;
                for (i, pattern_proc) in patterns_to_satisfy.iter().enumerate() {
                    if !satisfied_mask[i] {
                        num_unsatisfied += 1;
                        if !remaining_counts.can_subtract(&pattern_proc.counts) {
                            if let Some(file) = log_file.as_deref_mut() {
                                writeln!(file, "  Pruned PATTERN: Cannot form pattern '{}' (idx {}). Path: {:?}", pattern_proc.text, i, current_path
                                    ).unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                            }
                            return;
                        }
                    }
                }
                // If there are unsatisfied patterns but no letters left, or no more words allowed.
                if num_unsatisfied > 0 && remaining_counts.is_empty() {
                    if let Some(file) = log_file.as_deref_mut() {
                        writeln!(file, "  Pruned PATTERN: Unsatisfied patterns but no letters left. Path: {:?}", current_path
                            ).unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                    }
                    return;
                }
                if num_unsatisfied > 0
                    && constraints.max_words.is_some()
                    && current_path.len() >= constraints.max_words.unwrap()
                {
                    if let Some(file) = log_file.as_deref_mut() {
                        writeln!(file, "  Pruned PATTERN: Unsatisfied patterns but max_words reached. Path: {:?}", current_path
                            ).unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                    }
                    return;
                }
            }
        }

        // Pruning: Max words
        if let Some(max_w) = constraints.max_words {
            if current_path.len() > max_w {
                if let Some(file) = log_file.as_deref_mut() {
                    writeln!(
                        file,
                        "  Pruned: Path len {} > max_words {}. Path: {:?}",
                        current_path.len(),
                        max_w,
                        current_path
                    )
                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }
                return;
            }
        }
        if let Some(file) = log_file.as_deref_mut() {
            writeln!(
                file,
                "  Pre-base-case: path={:?}, remaining_total={}",
                current_path,
                remaining_counts.total()
            )
            .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
        }

        // Base Case: All characters used up

        if remaining_counts.is_empty() {
            if let Some(file) = log_file.as_deref_mut() {
                writeln!(
                    file,
                    "  REACHED BASE CASE (remaining_counts is empty). Path: {:?}",
                    current_path
                )
                .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
            }
            if !current_path.is_empty() {
                if let Some(file) = log_file.as_deref_mut() {
                    writeln!(file, "    Current path is not empty: {:?}", current_path)
                        .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }

                // Check max_words constraint for the formed solution
                if let Some(max_w) = constraints.max_words {
                    if current_path.len() > max_w {
                        if let Some(file) = log_file.as_deref_mut() {
                            writeln!(file, "    PRUNED BASE CASE: Solution path len {} > max_words {}. Path: {:?}", current_path.len(), max_w, current_path).unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                        }
                        return;
                    }
                }

                // Check must_start_with constraint
                if let Some(required_starts_map) = &constraints.must_start_with {
                    let mut actual_starts_counts: HashMap<char, usize> = HashMap::new();
                    for word in current_path.iter() {
                        if let Some(first_char) = word.chars().next() {
                            // Ensure first_char is lowercase for consistent map keys,
                            // assuming words in path are already lowercase.
                            // If not, first_char.to_ascii_lowercase()
                            *actual_starts_counts.entry(first_char).or_insert(0) += 1;
                        }
                    }

                    let mut must_start_with_satisfied = true;
                    for (req_char, req_count) in required_starts_map.iter() {
                        if actual_starts_counts.get(req_char).unwrap_or(&0) < req_count {
                            must_start_with_satisfied = false;
                            if let Some(file) = log_file.as_deref_mut() {
                                writeln!(file, "    PRUNED BASE CASE: must_start_with: char '{}' needed {} times, found {} times. Path: {:?}", 
                                        req_char, req_count, actual_starts_counts.get(req_char).unwrap_or(&0), current_path)
                                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                            }
                            break; // No need to check further required starts for this solution
                        }
                    }
                    if !must_start_with_satisfied {
                        return; // Constraint not met, discard this solution path
                    }
                    if let Some(file) = log_file.as_deref_mut() {
                        writeln!(
                            file,
                            "    must_start_with constraint SATISFIED. Path: {:?}",
                            current_path
                        )
                        .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                    }
                } else if let Some(file) = log_file.as_deref_mut() {
                    writeln!(
                        file,
                        "    No must_start_with constraint active. Path: {:?}",
                        current_path
                    )
                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }

                // FINAL PATTERN CHECK FOR SOLUTION
                if let Some(satisfied_mask) = &internal_state.patterns_satisfied_mask {
                    if !satisfied_mask.iter().all(|&s| s) {
                        if let Some(file) = log_file.as_deref_mut() {
                            writeln!(file, "    PRUNED BASE CASE: Patterns not satisfied. Mask: {:?}. Path: {:?}", satisfied_mask, current_path
                            ).unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                        }
                        return;
                    }
                    if let Some(file) = log_file.as_deref_mut() {
                        writeln!(file, "    Patterns satisfied (or no pattern constraint). Mask: {:?}. Path: {:?}", satisfied_mask, current_path
                            ).unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                    }
                } else if let Some(file) = log_file.as_deref_mut() {
                    writeln!(
                        file,
                        "    No pattern constraint active in base case. Path: {:?}",
                        current_path
                    )
                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }

                let mut solution_candidate = current_path.clone();
                solution_candidate.sort_unstable();
                if let Some(file) = log_file.as_deref_mut() {
                    writeln!(
                        file,
                        "    Attempting to insert solution: {:?}",
                        solution_candidate
                    )
                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }
                if solutions_set.insert(solution_candidate.clone()) {
                    internal_state.solutions_found_count += 1;
                    if let Some(file) = log_file.as_deref_mut() {
                        writeln!(
                            file,
                            "    Solution ADDED. New count: {}. Set size: {}. Path: {:?}",
                            internal_state.solutions_found_count,
                            solutions_set.len(),
                            current_path
                        )
                        .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                    }
                    if let Some(max_sol) = constraints.max_solutions {
                        if internal_state.solutions_found_count >= max_sol {
                            if let Some(file) = log_file.as_deref_mut() {
                                writeln!(
                                    file,
                                    "    Max solutions reached after adding. Path: {:?}",
                                    current_path
                                )
                                .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                            }
                            return;
                        }
                    }
                } else if let Some(file) = log_file.as_deref_mut() {
                    writeln!(file, "    Solution DUPLICATE. Path: {:?}", current_path)
                        .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }
            } else if let Some(file) = log_file.as_deref_mut() {
                writeln!(
                    file,
                    "    Current path IS EMPTY in base case. Path: {:?}",
                    current_path
                )
                .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
            }
            if let Some(file) = log_file.as_deref_mut() {
                writeln!(file, "  Returning from BASE CASE. Path: {:?}", current_path)
                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
            }
            return;
        }

        if let Some(file) = log_file.as_deref_mut() {
            writeln!(
                file,
                "  Did not hit base case (remaining_counts_total = {}). Path: {:?}",
                remaining_counts.total(),
                current_path
            )
            .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
        }

        if remaining_counts.total() < self.trie.get_min_word_len() {
            if let Some(file) = log_file.as_deref_mut() {
                writeln!(
                    file,
                    "  Pruned: remaining_total {} < min_dict_word_len {}. Path: {:?}",
                    remaining_counts.total(),
                    self.trie.get_min_word_len(),
                    current_path
                )
                .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
            }
            return;
        }
        // Check if remaining letters can form a word of min_len
        if let Some(min_len) = constraints.min_word_length {
            if !current_path.is_empty() && remaining_counts.total() < min_len {
                if let Some(file) = log_file.as_deref_mut() {
                    writeln!(
                        file,
                        "  Pruned: remaining_total {} < min_word_len {}. Path: {:?}",
                        remaining_counts.total(),
                        min_len,
                        current_path
                    )
                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }
                return;
            }
        }

        if let Some(max_w) = constraints.max_words {
            if current_path.len() == max_w && !remaining_counts.is_empty() {
                if let Some(file) = log_file.as_deref_mut() {
                    writeln!(
                        file,
                        "  Pruned: Path len {} == max_words {} but letters remain. Path: {:?}",
                        current_path.len(),
                        max_w,
                        current_path
                    )
                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }
                return;
            }
        }

        let mut word_buffer = String::new();
        if let Some(file) = log_file.as_deref_mut() {
            writeln!(
                file,
                "  Calling find_one_word_recursive for path: {:?}",
                current_path
            )
            .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
        }
        self.find_one_word_recursive(
            &self.trie.root,
            &mut word_buffer,
            remaining_counts,
            current_path,
            constraints,
            solutions_set,
            internal_state,
            log_file.as_deref_mut(), // Pass log_file
        );

        //if let Some(file) = log_file.as_deref_mut() {
        if let Some(file) = log_file {
            writeln!(file, "BACKTRACK EXIT: path={:?}", current_path)
                .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
        }
    }

    #[allow(clippy::too_many_arguments)]
    fn find_one_word_recursive(
        &self,
        current_trie_node: &TrieNode,
        word_so_far: &mut String,
        current_overall_counts: &mut CharCounts,
        path: &mut Vec<String>,
        constraints: &SolverConstraints,
        solutions_set: &mut HashSet<Vec<String>>,
        internal_state: &mut SolverInternalState,
        mut log_file: Option<&mut File>,
    ) {
        if let Some(file) = log_file.as_deref_mut() {
            writeln!(file, "  FOWR ENTRY: word_so_far='{}', path={:?}, current_overall_counts_total={}, node_is_word={}",
                    word_so_far, path, current_overall_counts.total(), current_trie_node.is_end_of_word)
                .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
        }

        // REMOVE THIS SPECIFIC DEBUG
        //if word_so_far == "eleven" {
        //    // Example specific debug
        //    if let Some(file) = log_file.as_deref_mut() {
        //        writeln!(
        //            file,
        //            "    FOWR: word_so_far IS 'eleven'. current_trie_node.is_end_of_word = {}",
        //            current_trie_node.is_end_of_word
        //        )
        //        .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
        //    }
        //}

        // Limit checks
        if internal_state.timed_out {
            if let Some(file) = log_file.as_deref_mut() {
                writeln!(file, "    FOWR Pruned: Timed out.")
                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
            }
            return;
        }
        if let Some(max_sol) = constraints.max_solutions {
            if internal_state.solutions_found_count >= max_sol {
                if let Some(file) = log_file.as_deref_mut() {
                    writeln!(file, "    FOWR Pruned: Max solutions.")
                        .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }
                return;
            }
        }

        if current_trie_node.is_end_of_word && !word_so_far.is_empty() {
            if let Some(file) = log_file.as_deref_mut() {
                writeln!(
                    file,
                    "    FOWR: Found candidate word: '{}'. Path before push: {:?}",
                    word_so_far, path
                )
                .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
            }

            let mut passes_min_length = true;
            if let Some(min_len) = constraints.min_word_length {
                if word_so_far.len() < min_len {
                    passes_min_length = false;
                }
            }

            if passes_min_length {
                if let Some(file) = log_file.as_deref_mut() {
                    writeln!(
                        file,
                        "      FOWR: '{}' passes min_length (len {}). Path: {:?}",
                        word_so_far,
                        word_so_far.len(),
                        path
                    )
                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }

                let mut original_mask_states_for_changed_indices = Vec::new();
                if let Some(patterns_to_satisfy) = &constraints.contains_patterns {
                    if let Some(current_mask) = internal_state.patterns_satisfied_mask.as_mut() {
                        if let Some(file) = log_file.as_deref_mut() {
                            writeln!(
                                file,
                                "      FOWR: Checking patterns. Word: '{}'. Mask before: {:?}",
                                word_so_far, current_mask
                            )
                            .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                        }
                        for (idx, pattern_proc) in patterns_to_satisfy.iter().enumerate() {
                            if !current_mask[idx] && word_so_far.contains(&pattern_proc.text) {
                                original_mask_states_for_changed_indices
                                    .push((idx, current_mask[idx]));
                                current_mask[idx] = true;
                                if let Some(file) = log_file.as_deref_mut() {
                                    writeln!(file, "        FOWR: Pattern '{}' (idx {}) satisfied by '{}'. Mask now: {:?}", 
                                        pattern_proc.text, idx, word_so_far, current_mask).unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                                }
                            }
                        }
                    }
                }

                path.push(word_so_far.clone());

                if let Some(file) = log_file.as_deref_mut() {
                    writeln!(file, "      FOWR: Pushed '{}'. Path is now: {:?}. Calling backtrack with remaining_counts_total: {}",
                            word_so_far, path, current_overall_counts.total())
                        .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }

                self.backtrack(
                    path,
                    current_overall_counts,
                    &self.trie.root,
                    constraints,
                    solutions_set,
                    internal_state,
                    log_file.as_deref_mut(),
                );

                path.pop();

                if let Some(file) = log_file.as_deref_mut() {
                    writeln!(
                        file,
                        "      FOWR: Popped '{}'. Path is now: {:?}",
                        word_so_far, path
                    )
                    .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }

                // Revert mask changes to their original state before this word was considered
                if let Some(current_mask) = internal_state.patterns_satisfied_mask.as_mut() {
                    if !original_mask_states_for_changed_indices.is_empty() && log_file.is_some() {
                        writeln!(log_file.as_deref_mut().unwrap(), "      FOWR: Reverting mask changes for word '{}'. Mask before revert: {:?}", word_so_far, current_mask
                            ).unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                    }
                    for (idx, original_state) in &original_mask_states_for_changed_indices {
                        current_mask[*idx] = *original_state;
                    }
                    if !current_mask.is_empty()
                        && log_file.is_some()
                        && !original_mask_states_for_changed_indices.is_empty()
                    {
                        // only log if changes were made
                        writeln!(
                            log_file.as_deref_mut().unwrap(),
                            "      FOWR: Mask after revert: {:?}",
                            current_mask
                        )
                        .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                    }
                }

                // Check limits again
                if internal_state.timed_out {
                    return;
                } // Re-check after backtrack
                if let Some(max_sol) = constraints.max_solutions {
                    if internal_state.solutions_found_count >= max_sol {
                        return;
                    }
                }
            } else if let Some(file) = log_file.as_deref_mut() {
                writeln!(
                    file,
                    "      FOWR: '{}' FAILED min_length (len {}). Path: {:?}",
                    word_so_far,
                    word_so_far.len(),
                    path
                )
                .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
            }
        }

        if word_so_far.len() >= self.trie.max_word_len {
            // Use >= because if len == max_word_len, can't extend
            if word_so_far.len() > self.trie.max_word_len {
                // Log only if strictly greater
                if let Some(file) = log_file.as_deref_mut() {
                    writeln!(file, "    FOWR Pruned (B): Word prefix '{}' (len {}) > max_dict_len {}. Cannot extend.", 
                            word_so_far, word_so_far.len(), self.trie.max_word_len
                        ).unwrap_or_else(|e| eprintln!("Log write error: {}", e));
                }
            }
            // If word_so_far.len() == self.trie.max_word_len, it cannot be extended further to find longer words.
            // It might BE a word of max_word_len itself (handled by is_end_of_word check earlier).
            // But we can't loop to find children to make it *longer*.
            return;
        }

        for (key_ref_char_code, value_ref_next_node) in current_trie_node.children.iter() {
            let ch: char = *key_ref_char_code;
            if current_overall_counts.get(ch).unwrap_or(0) > 0 {
                if word_so_far.is_empty() && !constraints.is_valid_start_char(ch) {
                    continue;
                }

                current_overall_counts.decrement_char(ch).unwrap();
                word_so_far.push(ch);

                self.find_one_word_recursive(
                    value_ref_next_node,
                    word_so_far,
                    current_overall_counts,
                    path,
                    constraints,
                    solutions_set,
                    internal_state,
                    log_file.as_deref_mut(),
                );

                word_so_far.pop();
                current_overall_counts.increment_char(ch).unwrap();

                if internal_state.timed_out {
                    return;
                }
                if let Some(max_sol) = constraints.max_solutions {
                    if internal_state.solutions_found_count >= max_sol {
                        return;
                    }
                }
            }
        }
        //if let Some(file) = log_file.as_deref_mut() {
        if let Some(file) = log_file {
            writeln!(file, "  FOWR EXIT: word_so_far='{}'", word_so_far)
                .unwrap_or_else(|e| eprintln!("Log write error: {}", e));
        }
    }
}
