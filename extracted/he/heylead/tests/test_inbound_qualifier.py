"""Tests for inbound qualification fast-path vendor pitch detection."""

from __future__ import annotations

from heylead.ai.inbound_qualifier import _classify_fast


class TestClassifyFastVendorHeadline:
    """Vendor headline keyword detection."""

    def test_account_executive(self):
        result = _classify_fast("Account Executive at SalesTech", "")
        assert result is not None
        assert result.intent == "vendor_pitch"
        assert result.recommended_action == "ignore"
        assert result.confidence == 0.85

    def test_business_development_representative(self):
        result = _classify_fast("Business Development Representative | SaaS", "")
        assert result is not None
        assert result.intent == "vendor_pitch"

    def test_sales_director(self):
        result = _classify_fast("Sales Director at CloudStaff", "")
        assert result is not None
        assert result.intent == "vendor_pitch"

    def test_talent_operations(self):
        """Blu Forero's exact headline keyword."""
        result = _classify_fast(
            "I lead talent operations for a marketplace built on quality", ""
        )
        assert result is not None
        assert result.intent == "vendor_pitch"

    def test_outsourcing(self):
        result = _classify_fast("Outsourcing Solutions for Tech Teams", "")
        assert result is not None
        assert result.intent == "vendor_pitch"

    def test_normal_headline_not_caught(self):
        """VP Engineering should NOT be caught as vendor."""
        result = _classify_fast("VP Engineering at Stripe", "")
        assert result is None

    def test_cto_not_caught(self):
        result = _classify_fast("CTO & Co-Founder | Building the future of AI", "")
        assert result is None


class TestClassifyFastVendorMessagePatterns:
    """Vendor message pattern detection (requires 2+ matches)."""

    def test_two_patterns_detected(self):
        msg = "Check out our platform. We can help you hire fast."
        result = _classify_fast("", msg)
        assert result is not None
        assert result.intent == "vendor_pitch"
        assert result.confidence == 0.80

    def test_single_pattern_falls_through(self):
        """Single vendor pattern should NOT trigger (ambiguous)."""
        msg = "Happy to help with anything you need."
        result = _classify_fast("", msg)
        assert result is None

    def test_booking_link_plus_pitch(self):
        msg = "Book a demo at meetings.hubspot.com/mylink to see how we help teams scale."
        result = _classify_fast("", msg)
        assert result is not None
        assert result.intent == "vendor_pitch"

    def test_calendly_plus_our_solution(self):
        msg = "Would love to show you our solution. Here's my calendly.com/john"
        result = _classify_fast("", msg)
        assert result is not None
        assert result.intent == "vendor_pitch"

    def test_blu_forero_message(self):
        """Blu Forero's actual messages combined."""
        msg = (
            "If you ever want to hire fast, this might be useful. "
            "Instead of guessing from resumes, our candidates show you on video. "
            "You can browse remote candidates anytime at cloudtask.com. "
            "If this is not the right time, no worries."
        )
        result = _classify_fast("", msg)
        assert result is not None
        assert result.intent == "vendor_pitch"
        assert result.recommended_action == "ignore"

    def test_legitimate_lead_not_caught(self):
        """A genuine lead mentioning scheduling should not be caught."""
        msg = "Loved your post about scaling SDR teams. Happy to chat about our challenges."
        result = _classify_fast("", msg)
        assert result is None


class TestClassifyFastBluForeroFullScenario:
    """End-to-end test with Blu Forero's exact profile + messages."""

    def test_headline_alone_catches(self):
        result = _classify_fast(
            "I lead talent operations for a marketplace built on quality",
            "Denys, thanks for connecting!",
        )
        assert result is not None
        assert result.intent == "vendor_pitch"
        assert result.recommended_action == "ignore"

    def test_message_alone_catches(self):
        result = _classify_fast(
            "Some other headline",
            "If you ever want to hire fast, this might be useful. "
            "You can browse remote candidates anytime at cloudtask.com",
        )
        assert result is not None
        assert result.intent == "vendor_pitch"


class TestClassifyFastNoRegression:
    """Ensure existing spam/recruiter detection still works."""

    def test_recruiter_headline(self):
        result = _classify_fast("Senior Recruiter at BigCorp", "")
        assert result is not None
        assert result.intent == "job_seeking"

    def test_spam_message(self):
        result = _classify_fast("", "We have an amazing opportunity for you")
        assert result is not None
        assert result.intent == "spam"

    def test_job_seeking_content(self):
        result = _classify_fast("", "I am looking for opportunities in tech")
        assert result is not None
        assert result.intent == "job_seeking"
