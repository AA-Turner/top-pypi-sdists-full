import os
from typing import List, Optional, Dict, Set

# This will be the Rust extension module. Name depends on maturin config.
# from .core import Solver as CoreSolver 
# For now, let's assume maturin makes it available as:
from multiword_anagram_fast.core import Solver as CoreSolver


class AnagramSolver:
    def __init__(self, default_dictionary_path: Optional[str] = ""):
        self._solver = CoreSolver()
        self._bundled_dict_path = os.path.join(
            os.path.dirname(__file__), "dictionaries"
        )

        if default_dictionary_path:
            if default_dictionary_path.lower() == "default": # example bundled
                self.load_dictionary_file(os.path.join(self._bundled_dict_path, "ACDLC0A.txt"))
            # Add more bundled dicts here
            else: # Assumed to be a custom path
                self.load_dictionary_file(default_dictionary_path)
        else: #load a default bundled dictionary if desired, e.g. dictionaryA.txt
            self.load_dictionary_file(os.path.join(self._bundled_dict_path, "ACDLC0A.txt"))
            
    def load_dictionary_file(self, path: str):
        """Loads words from a .txt file into the solver's dictionary."""
        try:
            #print("loading from: ",self._bundled_dict_path)
            self._solver.load_dictionary_from_path(path)
        except Exception as e:
            #print(self._bundled_dict_path)
            raise IOError(f"Failed to load dictionary from {path}: {e}")

    def add_words(self, words: List[str]):
        """Adds a list of words to the solver's dictionary."""
        self._solver.load_dictionary_from_words(words)
        
    def add_word(self, word: str):
        """Adds a single word to the solver's dictionary."""
        self._solver.add_word(word)


    def _solve(
        self,
        phrase: str,
        must_start_with: Optional[str] = None,
        can_only_ever_start_with: Optional[str] = None,
        must_not_start_with: Optional[str] = None,
        contains_patterns: Optional[List[str]] = None,
        max_words: Optional[int] = 4,
        min_word_length: Optional[int] = 2,
        timeout_seconds: Optional[float] = 30, 
        max_solutions: Optional[int] = 20000,
        output_file: Optional[str] = None,
    ) -> List[List[str]]:
        """
        Finds multi-word anagrams for the given phrase.

        Args:
            phrase: The input string of letters to anagram.
            must_start_with: A string of characters (e.g., "TRT"). Solutions must contain
                             words starting with these characters, matching counts (e.g., two Ts, one R).
            can_only_ever_start_with: A string of characters (e.g., "ABC"). All words in any
                                      solution must start with one of these characters.
            contains_patterns: A list of strings. Answers must contain ALL of these patterns
                at least ONCE at any point. Spaces are not ignored when apttern matching.
            must_not_start_with: A string of characters (e.g., "XYZ"). No word in any solution
                                 may start with one of these characters.
            max_words: The maximum number of words allowed in a solution.
            min_word_length: Dont allow smaller words if you dont want them.
            timeout_seconds: Stop it from running forever on huge anagrams.
            max_solutions: Stop at 20000 solutions. Its not like you are reading all those...
            output_file: If provided, results are saved to this file. Set to None to disable.

        Returns:
            A string that is path to results txt file.
            Solutions are sorted by quality (fewest words first, then by max length of shortest word).
        """

        results = self._solver.solve(
            phrase,
            must_start_with,
            can_only_ever_start_with,
            must_not_start_with,
            max_words,
            min_word_length,
            timeout_seconds, 
            max_solutions,   
            contains_patterns,
        )

        return results

    def solve(
        self,
        phrase: str,
        must_start_with: Optional[str] = None,
        can_only_ever_start_with: Optional[str] = None,
        must_not_start_with: Optional[str] = None,
        contains_patterns: Optional[List[str]] = None,
        max_words: Optional[int] = 4,
        min_word_length: Optional[int] = 2,
        timeout_seconds: Optional[float] = 30, 
        max_solutions: Optional[int] = 20000,
        output_file: Optional[str] = None,
    ) -> str: #     -> List[List[str]]:
        """
        Finds multi-word anagrams for the given phrase.

        Args:
            phrase: The input string of letters to anagram.
            must_start_with: A string of characters (e.g., "TRT"). Solutions must contain
                             words starting with these characters, matching counts (e.g., two Ts, one R).
            can_only_ever_start_with: A string of characters (e.g., "ABC"). All words in any
                                      solution must start with one of these characters.
            contains_patterns: A list of strings. Answers must contain ALL of these patterns
                at least ONCE at any point. Spaces are not ignored when apttern matching.
            must_not_start_with: A string of characters (e.g., "XYZ"). No word in any solution
                                 may start with one of these characters.
            max_words: The maximum number of words allowed in a solution.
            min_word_length: Dont allow smaller words if you dont want them.
            timeout_seconds: Stop it from running forever on huge anagrams.
            max_solutions: Stop at 20000 solutions. Its not like you are reading all those...
            output_file: If provided, results are saved to this file. Set to None to disable.

        Returns:
            A string that is path to results txt file.
            Solutions are sorted by quality (fewest words first, then by max length of shortest word).
        """

        if not phrase:
            return []
        phrase = phrase.replace(" ","")
        
        if output_file is None:
            # create a descriptive file name
            output_file = f"anagram_{phrase}"
            if must_start_with is not None: output_file += f"_must{must_start_with.upper()}"
            if can_only_ever_start_with is not None:  output_file += f"_only{can_only_ever_start_with.upper()}"
            if must_not_start_with is not None:  output_file += f"_not{must_not_start_with.upper()}"
            if max_words is not None: output_file += f"_maxW{max_words}"
            if min_word_length is not None: output_file += f"_minL{min_word_length}"
            if contains_patterns is not None:
                for pat in contains_patterns:
                    if pat: output_file += f"_pat{pat.upper()}"
            output_file += ".txt"

        # test we can even write to file at all before doing all the processing.
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(" ")
            #print(f"Solutions saved to {os.path.join(os.getcwd(), output_file)}")
        except IOError as e:
            print(f"Warning: Could not write to file {output_file}: {e}")
            print("Aborting.")
            return ""
        
        # get results
        results = self._solve(
            phrase, must_start_with, can_only_ever_start_with, 
            must_not_start_with, contains_patterns, max_words, min_word_length, 
            timeout_seconds, max_solutions, output_file,  
        )
        
        # write results to output file
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                for sol_list in results:
                    f.write(" ".join(sol_list) + "\n")
            print(f"{len(results)} solutions saved to {os.path.join(os.getcwd(), output_file)}")
        except IOError as e:
            print(f"Warning: Could not write solutions to file {output_file}: {e}")
        
        return output_file


    def get_bundled_dictionary_path(self, name: str = "ACDLC0A.txt") -> str:
        """Returns the path to a bundled dictionary."""
        path = os.path.join(self._bundled_dict_path, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Bundled dictionary '{name}' not found at {path}")
        return path