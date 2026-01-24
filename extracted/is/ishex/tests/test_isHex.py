from isHex import isHex, isHexLower, isHexUpper

def test_isHex_valid_lowercase_chars():
    assert isHex("abcdef") == True

def test_isHex_valid_uppercase_chars():
    assert isHex("ABCDEF") == True

def test_isHex_valid_mixed_chars():
    assert isHex("aBcDeF") == True

def test_isHex_valid_numbers():
    assert isHex("1234567890") == True

def test_isHex_mixed_numbers_and_chars():
    assert isHex("1234567890aBcDeF") == True

def test_isHex_invalid_chars():
    assert isHex("abcdefg") == False

def test_isHex_invalid_mixed_numbers_and_chars():
    assert isHex("97863hgfe347") == False

##

def test_isHexLower_valid_lowercase_chars():
    assert isHexLower("abcdef") == True

def test_isHexLower_valid_uppercase_chars():
    assert isHexLower("ABCDEF") == False

def test_isHexLower_valid_mixed_chars():
    assert isHexLower("aBcDeF") == False

def test_isHexLower_valid_numbers():
    assert isHexLower("1234567890") == True

def test_isHexLower_mixed_numbers_and_chars():
    assert isHexLower("1234567890aBcDeF") == False

def test_isHexLower_invalid_chars():
    assert isHex("abcdefg") == False

def test_isHexLower_invalid_mixed_numbers_and_chars():
    assert isHexLower("97863hgfe347") == False
    
##

def test_isHexUpper_valid_lowercase_chars():
    assert isHexUpper("abcdef") == False

def test_isHexUpper_valid_uppercase_chars():
    assert isHexUpper("ABCDEF") == True

def test_isHexUpper_valid_mixed_chars():
    assert isHexUpper("aBcDeF") == False

def test_isHexUpper_valid_numbers():
    assert isHexUpper("1234567890") == True

def test_isHexUpper_mixed_numbers_and_chars():
    assert isHexUpper("1234567890aBcDeF") == False

def test_isHexUpper_invalid_chars():
    assert isHexUpper("abcdefg") == False

def test_isHexUpper_invalid_mixed_numbers_and_chars():
    assert isHexUpper("97863hgfe347") == False