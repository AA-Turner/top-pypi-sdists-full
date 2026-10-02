from freemailchecker import is_free_email


# Test known free email domains
def test_free_email_domains():
    assert is_free_email("example@gmail.com")
    assert is_free_email("example@yahoo.com")
    assert is_free_email("example@hotmail.com")


# Test known non-free email domains
def test_non_free_email_domains():
    assert not is_free_email("example@privatecompany.com")
    assert not is_free_email("example@university.edu")


# Test handling of invalid email formats
def test_invalid_email_formats():
    assert not is_free_email("example.com")
    assert not is_free_email("example@.com")
    assert not is_free_email("@example.com")
    assert not is_free_email("")


# Test case insensitivity
def test_case_insensitivity():
    assert is_free_email("EXAMPLE@GMAIL.COM")
    assert not is_free_email("EXAMPLE@PRIVATECOMPANY.COM")


# Test whitespace stripping
def test_whitespace_stripping():
    assert is_free_email("  example@gmail.com  ")
    assert not is_free_email("  example@privatecompany.com  ")
