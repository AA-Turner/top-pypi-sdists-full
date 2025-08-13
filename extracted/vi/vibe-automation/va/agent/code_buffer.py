import logging

log = logging.getLogger(__name__)


class CodeModificationBuffer:
    """Buffer that handles sequential code insertions, deletions and replacements properly."""

    def __init__(self, original_code: str):
        self.lines = original_code.split("\n")
        self.insertions = []  # List of (line_num, code) tuples
        self.deletions = []  # List of (start_line, end_line) tuples
        self.replacements = []  # List of (start_line, end_line, new_code) tuples
        self.modifications_applied = False

    def queue_insertion(self, line_num: int, code: str):
        """Queue an insertion - don't apply immediately"""
        self.insertions.append((line_num, code))
        log.info(f"Queued insertion at line {line_num}: {code}")

    def queue_deletion(self, start_line: int, end_line: int):
        """Queue a deletion of lines from start_line to end_line (inclusive, 1-based)"""
        self.deletions.append((start_line, end_line))
        log.info(f"Queued deletion of lines {start_line}-{end_line}")

    def queue_replacement(self, start_line: int, end_line: int, new_code: str):
        """Queue a replacement of lines from start_line to end_line with new_code"""
        self.replacements.append((start_line, end_line, new_code))
        log.info(
            f"Queued replacement of lines {start_line}-{end_line} with: {new_code}"
        )

    def apply_all_modifications(self) -> str:
        """Apply all queued modifications in the correct order"""
        if not self.insertions and not self.deletions and not self.replacements:
            return "\n".join(self.lines)

        # If modifications have already been applied, just return the current state
        if self.modifications_applied:
            return "\n".join(self.lines)

        # Apply modifications in order: replacements first, then deletions, then insertions
        # All sorted by line number (descending) to avoid line number shifts

        # 1. Apply replacements (delete + insert in one operation)
        sorted_replacements = sorted(self.replacements, key=lambda x: -x[0])
        for start_line, end_line, new_code in sorted_replacements:
            # Convert to 0-based indexing
            start_idx = max(0, start_line - 1)
            end_idx = min(len(self.lines), end_line)

            # Replace the range with new code
            del self.lines[start_idx:end_idx]
            self.lines.insert(start_idx, new_code)

        # 2. Apply deletions
        sorted_deletions = sorted(self.deletions, key=lambda x: -x[0])
        for start_line, end_line in sorted_deletions:
            # Convert to 0-based indexing
            start_idx = max(0, start_line - 1)
            end_idx = min(len(self.lines), end_line)

            # Delete the range
            del self.lines[start_idx:end_idx]

        # 3. Apply insertions
        sorted_insertions = sorted(
            enumerate(self.insertions),
            key=lambda x: (
                -x[1][0],
                -x[0],
            ),  # Sort by line_num desc, then by insertion order reversed
        )

        for original_index, (line_num, code) in sorted_insertions:
            # Insert before the target line (line_num is 1-based, convert to 0-based)
            insert_index = max(0, line_num - 1)
            self.lines.insert(insert_index, code)

        # Mark modifications as applied
        self.modifications_applied = True
        return "\n".join(self.lines)

    def get_modification_summary(self) -> str:
        """Get a summary of all queued modifications"""
        if not self.insertions and not self.deletions and not self.replacements:
            return "No modifications queued."

        summary = "Queued modifications:\n"
        mod_count = 1

        # Show replacements
        for start_line, end_line, new_code in self.replacements:
            summary += (
                f"{mod_count}. Replace lines {start_line}-{end_line} with: {new_code}\n"
            )
            mod_count += 1

        # Show deletions
        for start_line, end_line in self.deletions:
            summary += f"{mod_count}. Delete lines {start_line}-{end_line}\n"
            mod_count += 1

        # Show insertions
        for line_num, code in self.insertions:
            summary += f"{mod_count}. Insert at line {line_num}: {code}\n"
            mod_count += 1

        return summary
