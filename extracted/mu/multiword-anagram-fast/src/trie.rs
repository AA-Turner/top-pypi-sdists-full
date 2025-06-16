use std::collections::HashMap;
// Removed CharCounts, index_to_char as they are not directly used here.
// char_to_index was also removed as it was for direct access, normalize_word handles char properties.
use super::char_utils::normalize_word;

#[derive(Default)]
pub struct TrieNode {
    pub children: HashMap<char, TrieNode>,
    pub is_end_of_word: bool,
}

pub struct Trie {
    pub root: TrieNode,
    pub min_word_len: usize, // Made public
    pub max_word_len: usize, // Made public
}

impl Trie {
    pub fn new() -> Self {
        Trie {
            root: TrieNode::default(),
            min_word_len: usize::MAX,
            max_word_len: 0,
        }
    }

    pub fn insert(&mut self, word: &str) {
        let normalized = normalize_word(word);
        if normalized.is_empty() {
            return;
        }

        let len = normalized.len();
        self.min_word_len = self.min_word_len.min(len);
        self.max_word_len = self.max_word_len.max(len);

        let mut current_node = &mut self.root;
        for c in normalized.chars() {
            current_node = current_node.children.entry(c).or_default();
        }
        current_node.is_end_of_word = true;
    }

    pub fn get_min_word_len(&self) -> usize {
        if self.min_word_len == usize::MAX {
            0
        } else {
            self.min_word_len
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_trie_insert_and_is_end_of_word() {
        let mut trie = Trie::new();
        trie.insert("apple");
        trie.insert("apply");

        // Helper to check if a word exists (is_end_of_word at its node)
        fn check_word(node: &TrieNode, word: &str) -> bool {
            let mut current = node;
            for c in word.chars() {
                if let Some(next_node) = current.children.get(&c) {
                    current = next_node;
                } else {
                    return false;
                }
            }
            current.is_end_of_word
        }

        assert!(check_word(&trie.root, "apple"));
        assert!(check_word(&trie.root, "apply"));
        assert!(!check_word(&trie.root, "app")); // Prefix, not full word
        assert!(!check_word(&trie.root, "apples"));
    }

    #[test]
    fn test_trie_min_max_len() {
        let mut trie = Trie::new();
        assert_eq!(trie.get_min_word_len(), 0); // Before any inserts
        trie.insert("a");
        trie.insert("banana");
        trie.insert("cat");
        assert_eq!(trie.min_word_len, 1);
        assert_eq!(trie.max_word_len, 6);
        assert_eq!(trie.get_min_word_len(), 1);
    }
}
