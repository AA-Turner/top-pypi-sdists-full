from abstra_internals.entities.agents.memory_manager import MemoryManager, MemoryReducer


class TestMemoryManager:
    def test_add_fact(self):
        mm = MemoryManager()
        mm.add_fact("The login page is at /auth")
        assert len(mm.key_facts) == 1
        assert mm.key_facts[0] == "The login page is at /auth"

    def test_add_fact_dedup(self):
        mm = MemoryManager()
        mm.add_fact("User is admin")
        mm.add_fact("User is admin")
        assert len(mm.key_facts) == 1

    def test_add_multiple_facts(self):
        mm = MemoryManager()
        mm.add_fact("fact1")
        mm.add_fact("fact2")
        mm.add_fact("fact3")
        assert len(mm.key_facts) == 3

    def test_get_facts_context_empty(self):
        mm = MemoryManager()
        assert mm.get_facts_context() == ""

    def test_get_facts_context_with_facts(self):
        mm = MemoryManager()
        mm.add_fact("Database is PostgreSQL")
        mm.add_fact("API key is required")
        context = mm.get_facts_context()
        assert "Long-term Memory" in context
        assert "- Database is PostgreSQL" in context
        assert "- API key is required" in context


class TestMemoryReducer:
    def test_create_step_entry(self):
        mr = MemoryReducer()
        entry = mr.create_step_entry(
            1, "navigate", "https://example.com", "Page loaded"
        )
        assert "Step 1" in entry
        assert "navigate" in entry
        assert "https://example.com" in entry
        assert "Page loaded" in entry

    def test_create_step_entry_truncates_long_observation(self):
        mr = MemoryReducer()
        long_obs = "x" * 200
        entry = mr.create_step_entry(1, "extract_text", "{}", long_obs)
        assert "..." in entry
        assert len(entry) < len(long_obs) + 100

    def test_create_step_entry_truncates_long_input(self):
        mr = MemoryReducer()
        long_input = "y" * 200
        entry = mr.create_step_entry(1, "type_text", long_input, "ok")
        assert "[truncated]" in entry

    def test_update_accumulates_entries(self):
        mr = MemoryReducer()
        mr.update(1, "navigate", "url", "ok")
        mr.update(2, "click", "5", "clicked")
        assert "Step 1" in mr.summary
        assert "Step 2" in mr.summary

    def test_update_returns_summary(self):
        mr = MemoryReducer()
        result = mr.update(1, "navigate", "url", "ok")
        assert result == mr.summary
        assert "Step 1" in result

    def test_compress_preserves_first_and_last(self):
        mr = MemoryReducer()
        # Force enough content to trigger compression
        for i in range(1, 30):
            mr.update(i, "action", f"input_{i}", "observation " * 20)
        summary = mr.summary
        assert "Step 1" in summary
        assert "earlier steps summarized" in summary

    def test_summary_initially_empty(self):
        mr = MemoryReducer()
        assert mr.summary == ""

    def test_summarization_threshold(self):
        assert MemoryReducer.SUMMARIZATION_THRESHOLD == 1500
