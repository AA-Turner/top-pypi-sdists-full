from agentic_devtools.ai_providers import copilot as copilot_module


def test_is_valid_hostname_accepts_standard_dns_name() -> None:
    assert copilot_module._is_valid_hostname("api.github.com")


def test_is_valid_hostname_rejects_labels_with_leading_or_trailing_dash() -> None:
    assert not copilot_module._is_valid_hostname("-api.github.com")
    assert not copilot_module._is_valid_hostname("api-.github.com")


def test_is_valid_hostname_rejects_hostname_over_253_chars() -> None:
    hostname = ".".join(["a" * 63, "b" * 63, "c" * 63, "d" * 62, "com"])

    assert len(hostname) > 253
    assert not copilot_module._is_valid_hostname(hostname)
