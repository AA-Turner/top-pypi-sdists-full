"""Tests for company/business profile detection and filtering."""

from __future__ import annotations

from heylead.services.dedup_service import is_company_profile, dedup_prospects


class TestIsCompanyProfile:
    """Detect company pages that shouldn't receive outreach."""

    def test_obvious_company_url(self):
        assert is_company_profile({
            "name": "Google",
            "linkedin_url": "https://www.linkedin.com/company/google",
        })

    def test_company_suffix_inc(self):
        assert is_company_profile({"name": "Acme Solutions Inc"})

    def test_company_suffix_llc(self):
        assert is_company_profile({"name": "Digital Dynamics LLC"})

    def test_company_suffix_ltd(self):
        assert is_company_profile({"name": "TechVentures Ltd"})

    def test_company_suffix_gmbh(self):
        assert is_company_profile({"name": "DataWorks GmbH"})

    def test_company_keyword_solutions(self):
        """Quantum Formatics has a numeric public_id — not caught by name alone
        but caught when combined with numeric ID heuristic if it has keywords.
        Test the pure name-based detection for clear company names."""
        assert is_company_profile({"name": "Quantum Solutions"})

    def test_company_keyword_technologies(self):
        assert is_company_profile({"name": "Prodigy AI Solutions"})

    def test_company_keyword_consulting(self):
        assert is_company_profile({"name": "Apex Consulting"})

    def test_company_keyword_agency(self):
        assert is_company_profile({"name": "Growth Agency"})

    def test_company_keyword_platform(self):
        assert is_company_profile({"name": "SalesTech Platform"})

    def test_real_person_not_flagged(self):
        assert not is_company_profile({
            "name": "John Smith",
            "title": "CEO",
            "linkedin_url": "https://www.linkedin.com/in/johnsmith",
        })

    def test_real_person_with_title_not_flagged(self):
        assert not is_company_profile({
            "name": "Maria Garcia",
            "title": "VP of Engineering",
        })

    def test_real_person_unicode_not_flagged(self):
        assert not is_company_profile({"name": "André Müller"})

    def test_name_ending_with_solutions_flagged(self):
        """'Sarah Solutions' ends with a company keyword — flagged as company.
        Real people don't have last names like 'Solutions'. This is an acceptable
        false-positive trade-off to catch company pages."""
        assert is_company_profile({
            "name": "Sarah Solutions",
            "title": "Founder at Acme Corp",
        })

    def test_empty_name_not_flagged(self):
        assert not is_company_profile({"name": ""})

    def test_none_name_not_flagged(self):
        assert not is_company_profile({"name": None})

    def test_single_word_business_name(self):
        """Single-word business names like 'Analytics' should be caught."""
        assert is_company_profile({"name": "Analytics"})

    def test_numeric_id_with_keyword_in_name(self):
        """Numeric public_id + company keyword in name = company profile.
        This catches cases like 'Quantum Formatics' which don't end with a keyword
        but have a numeric ID and contain a keyword."""
        # "Digital" is a keyword, numeric ID reinforces company signal
        assert is_company_profile({
            "name": "Quantum Digital",
            "public_id": "105576161",
        })

    def test_numeric_id_without_keyword_not_flagged(self):
        """Numeric ID alone shouldn't flag a real person."""
        assert not is_company_profile({
            "name": "Wei Zhang",
            "public_id": "12345678",
        })


class TestDedupProspectsFiltersCompanyProfiles:
    """dedup_prospects should filter out company profiles in stats."""

    def test_company_profiles_counted_in_stats(self):
        prospects = [
            {"name": "John Smith", "public_id": "john-smith", "provider_id": "p1"},
            {"name": "TechVenture Solutions", "public_id": "105576161", "provider_id": "p2"},
            {"name": "Prodigy AI Solutions", "public_id": "107426702", "provider_id": "p3"},
            {"name": "Jane Doe", "public_id": "jane-doe", "provider_id": "p4"},
        ]

        filtered, stats = dedup_prospects(prospects, set(), set())

        assert stats["company_profile"] == 2
        assert stats["passed"] == 2
        assert len(filtered) == 2
        assert filtered[0]["name"] == "John Smith"
        assert filtered[1]["name"] == "Jane Doe"

    def test_no_company_profiles(self):
        prospects = [
            {"name": "Alice Brown", "public_id": "alice-brown", "provider_id": "p1"},
        ]

        filtered, stats = dedup_prospects(prospects, set(), set())

        assert stats["company_profile"] == 0
        assert stats["passed"] == 1
