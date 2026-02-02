import unicodedata
import stringprep
import enum
import functools

SPACE = 0x0020

MAPPED_TO_NOTHING = {
	# SOFT HYPHEN (U+00AD)
	0x00AD,
	# MONGOLIAN TODO SOFT HYPHEN (U+1806)
	0x1806,
	# COMBINING GRAPHEME JOINER (U+034F)
	0x034F,
	# VARIATION SELECTORs (U+180B-180D, FF00-FE0F)
	0x180B, 0x180C, 0x180D,
	0xFE00, 0xFE01, 0xFE02, 0xFE03, 0xFE04, 0xFE05, 0xFE06, 0xFE07, 0xFE08,
	0xFE09, 0xFE0A, 0xFE0B, 0xFE0C, 0xFE0D, 0xFE0E, 0xFE0F,
	# OBJECT REPLACEMENT CHARACTER (U+FFFC)
	0xFFFC,
	# ZERO WIDTH SPACE (U+200B)
	0x200B,
}

MAPPED_TO_SPACE = {
	# CHARACTER TABULATION (U+0009)
	0x0009,
	# LINE FEED (LF) (U+000A)
	0x000A,
	# LINE TABULATION (U+000B)
	0x000B,
	# FORM FEED (FF) (U+000C)
	0x000C,
	# CARRIAGE RETURN (CR) (U+000D)
	0x000D,
	# NEXT LINE (NEL) (U+0085)
	0x0085,
	# All other control code (e.g., Cc) points or code points with a
	# control function (e.g., Cf)
	0x0000, 0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006, 0x0007, 0x0008,
	0x000E, 0x000F, 0x0010, 0x0011, 0x0012, 0x0013, 0x0014, 0x0015, 0x0016,
	0x0017, 0x0018, 0x0019, 0x001A, 0x001B, 0x001C, 0x001D, 0x001E, 0x001F,
	0x007F, 0x0080, 0x0081, 0x0082, 0x0083, 0x0084,
	0x0086, 0x0087, 0x0088, 0x0089, 0x008A, 0x008B, 0x008C, 0x008D, 0x008E,
	0x008F, 0x0090, 0x0091, 0x0092, 0x0093, 0x0094, 0x0095, 0x0096, 0x0097,
	0x0098, 0x0099, 0x009A, 0x009B, 0x009C, 0x009D, 0x009E, 0x009F,
	0x06DD,
	0x070F,
	0x180E,
	0x200C, 0x200D, 0x200E, 0x200F,
	0x202A, 0x202B, 0x202C, 0x202D, 0x202E,
	0x2060, 0x2061, 0x2062, 0x2063,
	0x206A, 0x206B, 0x206C, 0x206D, 0x206E, 0x206F,
	0xFEFF,
	0xFFF9, 0xFFFA, 0xFFFB,
	0x1D173, 0x1D174, 0x1D175, 0x1D176, 0x1D177, 0x1D178, 0x1D179, 0x1D17A,
	0xE0001,
	0xE0020, 0xE0021, 0xE0022, 0xE0023, 0xE0024, 0xE0025, 0xE0026, 0xE0027,
	0xE0028, 0xE0029, 0xE002A, 0xE002B, 0xE002C, 0xE002D, 0xE002E, 0xE002F,
	0xE0030, 0xE0031, 0xE0032, 0xE0033, 0xE0034, 0xE0035, 0xE0036, 0xE0037,
	0xE0038, 0xE0039, 0xE003A, 0xE003B, 0xE003C, 0xE003D, 0xE003E, 0xE003F,
	0xE0040, 0xE0041, 0xE0042, 0xE0043, 0xE0044, 0xE0045, 0xE0046, 0xE0047,
	0xE0048, 0xE0049, 0xE004A, 0xE004B, 0xE004C, 0xE004D, 0xE004E, 0xE004F,
	0xE0050, 0xE0051, 0xE0052, 0xE0053, 0xE0054, 0xE0055, 0xE0056, 0xE0057,
	0xE0058, 0xE0059, 0xE005A, 0xE005B, 0xE005C, 0xE005D, 0xE005E, 0xE005F,
	0xE0060, 0xE0061, 0xE0062, 0xE0063, 0xE0064, 0xE0065, 0xE0066, 0xE0067,
	0xE0068, 0xE0069, 0xE006A, 0xE006B, 0xE006C, 0xE006D, 0xE006E, 0xE006F,
	0xE0070, 0xE0071, 0xE0072, 0xE0073, 0xE0074, 0xE0075, 0xE0076, 0xE0077,
	0xE0078, 0xE0079, 0xE007A, 0xE007B, 0xE007C, 0xE007D, 0xE007E, 0xE007F,
}

# unicodedata.combining does not seem to reflect this table and the RFC
# says the embedded table is definitive.
COMBINING_MARKS = {
	0x0300, 0x0301, 0x0302, 0x0303, 0x0304, 0x0305, 0x0306, 0x0307, 0x0308,
	0x0309, 0x030A, 0x030B, 0x030C, 0x030D, 0x030E, 0x030F, 0x0310, 0x0311,
	0x0312, 0x0313, 0x0314, 0x0315, 0x0316, 0x0317, 0x0318, 0x0319, 0x031A,
	0x031B, 0x031C, 0x031D, 0x031E, 0x031F, 0x0320, 0x0321, 0x0322, 0x0323,
	0x0324, 0x0325, 0x0326, 0x0327, 0x0328, 0x0329, 0x032A, 0x032B, 0x032C,
	0x032D, 0x032E, 0x032F, 0x0330, 0x0331, 0x0332, 0x0333, 0x0334, 0x0335,
	0x0336, 0x0337, 0x0338, 0x0339, 0x033A, 0x033B, 0x033C, 0x033D, 0x033E,
	0x033F, 0x0340, 0x0341, 0x0342, 0x0343, 0x0344, 0x0345, 0x0346, 0x0347,
	0x0348, 0x0349, 0x034A, 0x034B, 0x034C, 0x034D, 0x034E, 0x034F, 0x0360,
	0x0361, 0x0362, 0x0363, 0x0364, 0x0365, 0x0366, 0x0367, 0x0368, 0x0369,
	0x036A, 0x036B, 0x036C, 0x036D, 0x036E, 0x036F, 0x0483, 0x0484, 0x0485,
	0x0486, 0x0488, 0x0489, 0x0591, 0x0592, 0x0593, 0x0594, 0x0595, 0x0596,
	0x0597, 0x0598, 0x0599, 0x059A, 0x059B, 0x059C, 0x059D, 0x059E, 0x059F,
	0x05A0, 0x05A1, 0x05A3, 0x05A4, 0x05A5, 0x05A6, 0x05A7, 0x05A8, 0x05A9,
	0x05AA, 0x05AB, 0x05AC, 0x05AD, 0x05AE, 0x05AF, 0x05B0, 0x05B1, 0x05B2,
	0x05B3, 0x05B4, 0x05B5, 0x05B6, 0x05B7, 0x05B8, 0x05B9, 0x05BB, 0x05BC,
	0x05BF, 0x05C1, 0x05C2, 0x05C4, 0x064B, 0x064C, 0x064D, 0x064E, 0x064F,
	0x0650, 0x0651, 0x0652, 0x0653, 0x0654, 0x0655, 0x0670, 0x06D6, 0x06D7,
	0x06D8, 0x06D9, 0x06DA, 0x06DB, 0x06DC, 0x06DE, 0x06DF, 0x06E0, 0x06E1,
	0x06E2, 0x06E3, 0x06E4, 0x06E7, 0x06E8, 0x06EA, 0x06EB, 0x06EC, 0x06ED,
	0x0711, 0x0730, 0x0731, 0x0732, 0x0733, 0x0734, 0x0735, 0x0736, 0x0737,
	0x0738, 0x0739, 0x073A, 0x073B, 0x073C, 0x073D, 0x073E, 0x073F, 0x0740,
	0x0741, 0x0742, 0x0743, 0x0744, 0x0745, 0x0746, 0x0747, 0x0748, 0x0749,
	0x074A, 0x07A6, 0x07A7, 0x07A8, 0x07A9, 0x07AA, 0x07AB, 0x07AC, 0x07AD,
	0x07AE, 0x07AF, 0x07B0, 0x0901, 0x0902, 0x0903, 0x093C, 0x093E, 0x093F,
	0x0940, 0x0941, 0x0942, 0x0943, 0x0944, 0x0945, 0x0946, 0x0947, 0x0948,
	0x0949, 0x094A, 0x094B, 0x094C, 0x094D, 0x094E, 0x094F, 0x0951, 0x0952,
	0x0953, 0x0954, 0x0962, 0x0963, 0x0981, 0x0982, 0x0983, 0x09BC, 0x09BE,
	0x09BF, 0x09C0, 0x09C1, 0x09C2, 0x09C3, 0x09C4, 0x09C7, 0x09C8, 0x09CB,
	0x09CC, 0x09CD, 0x09D7, 0x09E2, 0x09E3, 0x0A02, 0x0A3C, 0x0A3E, 0x0A3F,
	0x0A40, 0x0A41, 0x0A42, 0x0A47, 0x0A48, 0x0A4B, 0x0A4C, 0x0A4D, 0x0A70,
	0x0A71, 0x0A81, 0x0A82, 0x0A83, 0x0ABC, 0x0ABE, 0x0ABF, 0x0AC0, 0x0AC1,
	0x0AC2, 0x0AC3, 0x0AC4, 0x0AC5, 0x0AC7, 0x0AC8, 0x0AC9, 0x0ACB, 0x0ACC,
	0x0ACD, 0x0B01, 0x0B02, 0x0B03, 0x0B3C, 0x0B3E, 0x0B3F, 0x0B40, 0x0B41,
	0x0B42, 0x0B43, 0x0B47, 0x0B48, 0x0B4B, 0x0B4C, 0x0B4D, 0x0B56, 0x0B57,
	0x0B82, 0x0BBE, 0x0BBF, 0x0BC0, 0x0BC1, 0x0BC2, 0x0BC6, 0x0BC7, 0x0BC8,
	0x0BCA, 0x0BCB, 0x0BCC, 0x0BCD, 0x0BD7, 0x0C01, 0x0C02, 0x0C03, 0x0C3E,
	0x0C3F, 0x0C40, 0x0C41, 0x0C42, 0x0C43, 0x0C44, 0x0C46, 0x0C47, 0x0C48,
	0x0C4A, 0x0C4B, 0x0C4C, 0x0C4D, 0x0C55, 0x0C56, 0x0C82, 0x0C83, 0x0CBE,
	0x0CBF, 0x0CC0, 0x0CC1, 0x0CC2, 0x0CC3, 0x0CC4, 0x0CC6, 0x0CC7, 0x0CC8,
	0x0CCA, 0x0CCB, 0x0CCC, 0x0CCD, 0x0CD5, 0x0CD6, 0x0D02, 0x0D03, 0x0D3E,
	0x0D3F, 0x0D40, 0x0D41, 0x0D42, 0x0D43, 0x0D46, 0x0D47, 0x0D48, 0x0D4A,
	0x0D4B, 0x0D4C, 0x0D4D, 0x0D57, 0x0D82, 0x0D83, 0x0DCA, 0x0DCF, 0x0DD0,
	0x0DD1, 0x0DD2, 0x0DD3, 0x0DD4, 0x0DD6, 0x0DD8, 0x0DD9, 0x0DDA, 0x0DDB,
	0x0DDC, 0x0DDD, 0x0DDE, 0x0DDF, 0x0DF2, 0x0DF3, 0x0E31, 0x0E34, 0x0E35,
	0x0E36, 0x0E37, 0x0E38, 0x0E39, 0x0E3A, 0x0E47, 0x0E48, 0x0E49, 0x0E4A,
	0x0E4B, 0x0E4C, 0x0E4D, 0x0E4E, 0x0EB1, 0x0EB4, 0x0EB5, 0x0EB6, 0x0EB7,
	0x0EB8, 0x0EB9, 0x0EBB, 0x0EBC, 0x0EC8, 0x0EC9, 0x0ECA, 0x0ECB, 0x0ECC,
	0x0ECD, 0x0F18, 0x0F19, 0x0F35, 0x0F37, 0x0F39, 0x0F3E, 0x0F3F, 0x0F71,
	0x0F72, 0x0F73, 0x0F74, 0x0F75, 0x0F76, 0x0F77, 0x0F78, 0x0F79, 0x0F7A,
	0x0F7B, 0x0F7C, 0x0F7D, 0x0F7E, 0x0F7F, 0x0F80, 0x0F81, 0x0F82, 0x0F83,
	0x0F84, 0x0F86, 0x0F87, 0x0F90, 0x0F91, 0x0F92, 0x0F93, 0x0F94, 0x0F95,
	0x0F96, 0x0F97, 0x0F99, 0x0F9A, 0x0F9B, 0x0F9C, 0x0F9D, 0x0F9E, 0x0F9F,
	0x0FA0, 0x0FA1, 0x0FA2, 0x0FA3, 0x0FA4, 0x0FA5, 0x0FA6, 0x0FA7, 0x0FA8,
	0x0FA9, 0x0FAA, 0x0FAB, 0x0FAC, 0x0FAD, 0x0FAE, 0x0FAF, 0x0FB0, 0x0FB1,
	0x0FB2, 0x0FB3, 0x0FB4, 0x0FB5, 0x0FB6, 0x0FB7, 0x0FB8, 0x0FB9, 0x0FBA,
	0x0FBB, 0x0FBC, 0x0FC6, 0x102C, 0x102D, 0x102E, 0x102F, 0x1030, 0x1031,
	0x1032, 0x1036, 0x1037, 0x1038, 0x1039, 0x1056, 0x1057, 0x1058, 0x1059,
	0x1712, 0x1713, 0x1714, 0x1732, 0x1733, 0x1734, 0x1752, 0x1753, 0x1772,
	0x1773, 0x17B4, 0x17B5, 0x17B6, 0x17B7, 0x17B8, 0x17B9, 0x17BA, 0x17BB,
	0x17BC, 0x17BD, 0x17BE, 0x17BF, 0x17C0, 0x17C1, 0x17C2, 0x17C3, 0x17C4,
	0x17C5, 0x17C6, 0x17C7, 0x17C8, 0x17C9, 0x17CA, 0x17CB, 0x17CC, 0x17CD,
	0x17CE, 0x17CF, 0x17D0, 0x17D1, 0x17D2, 0x17D3, 0x180B, 0x180C, 0x180D,
	0x18A9, 0x20D0, 0x20D1, 0x20D2, 0x20D3, 0x20D4, 0x20D5, 0x20D6, 0x20D7,
	0x20D8, 0x20D9, 0x20DA, 0x20DB, 0x20DC, 0x20DD, 0x20DE, 0x20DF, 0x20E0,
	0x20E1, 0x20E2, 0x20E3, 0x20E4, 0x20E5, 0x20E6, 0x20E7, 0x20E8, 0x20E9,
	0x20EA, 0x302A, 0x302B, 0x302C, 0x302D, 0x302E, 0x302F, 0x3099, 0x309A,
	0xFB1E, 0xFE00, 0xFE01, 0xFE02, 0xFE03, 0xFE04, 0xFE05, 0xFE06, 0xFE07,
	0xFE08, 0xFE09, 0xFE0A, 0xFE0B, 0xFE0C, 0xFE0D, 0xFE0E, 0xFE0F, 0xFE20,
	0xFE21, 0xFE22, 0xFE23, 0x1D165, 0x1D166, 0x1D167, 0x1D168, 0x1D169,
	0x1D16D, 0x1D16E, 0x1D16F, 0x1D170, 0x1D171, 0x1D172, 0x1D17B, 0x1D17C,
	0x1D17D, 0x1D17E, 0x1D17F, 0x1D180, 0x1D181, 0x1D182, 0x1D185, 0x1D186,
	0x1D187, 0x1D188, 0x1D189, 0x1D18A, 0x1D18B, 0x1D1AA, 0x1D1AB, 0x1D1AC,
	0x1D1AD,
}

class MatchingType(enum.Enum):
	CASE_IGNORE_STRING = enum.auto()
	EXACT_STRING = enum.auto()
	NUMERIC_STRING = enum.auto()
	TELEPHONE_NUMBER = enum.auto()

class SubstringType(enum.Enum):
	NONE = enum.auto()
	INITIAL = enum.auto()
	ANY = enum.auto()
	FINAL = enum.auto()

@functools.lru_cache(maxsize=128, typed=False)
def prepare(value, matching_type=MatchingType.EXACT_STRING,
            substring_type=SubstringType.NONE):
	# Algortihm according to RFC 4518
	#
	# 1) Transcode: value is already a Unicode string, no transcoding needed
	# 2) Map
	value = prepare_map(value, matching_type=matching_type)
	# 3) Normalize
	value = prepare_normalize(value)
	# 4) Prohibit
	if prepare_check_prohibited(value):
		raise ValueError('Stringprep "prohibit" stage rejected input')
	# 5) Check bidi: Bidirectional characters are ignored.
	# 6) Insignificant Character Handling
	value = prepare_insignificant_characters(value, matching_type=matching_type,
	                                         substring_type=substring_type)
	return value

def prepare_map(value, matching_type=MatchingType.EXACT_STRING):
	# 2.2.  Map
	#
	# SOFT HYPHEN (U+00AD) and MONGOLIAN TODO SOFT HYPHEN (U+1806) code
	# points are mapped to nothing.  COMBINING GRAPHEME JOINER (U+034F) and
	# VARIATION SELECTORs (U+180B-180D, FF00-FE0F) code points are also
	# mapped to nothing.  The OBJECT REPLACEMENT CHARACTER (U+FFFC) is
	# mapped to nothing.
	#
	# CHARACTER TABULATION (U+0009), LINE FEED (LF) (U+000A), LINE
	# TABULATION (U+000B), FORM FEED (FF) (U+000C), CARRIAGE RETURN (CR)
	# (U+000D), and NEXT LINE (NEL) (U+0085) are mapped to SPACE (U+0020).
	#
	# All other control code (e.g., Cc) points or code points with a
	# control function (e.g., Cf) are mapped to nothing.  The following is
	# a complete list of these code points: U+0000-0008, 000E-001F, 007F-
	# 0084, 0086-009F, 06DD, 070F, 180E, 200C-200F, 202A-202E, 2060-2063,
	# 206A-206F, FEFF, FFF9-FFFB, 1D173-1D17A, E0001, E0020-E007F.
	#
	# ZERO WIDTH SPACE (U+200B) is mapped to nothing.  All other code
	# points with Separator (space, line, or paragraph) property (e.g., Zs,
	# Zl, or Zp) are mapped to SPACE (U+0020).  The following is a complete
	# list of these code points: U+0020, 00A0, 1680, 2000-200A, 2028-2029,
	# 202F, 205F, 3000.
	#
	# For case ignore, numeric, and stored prefix string matching rules,
	# characters are case folded per B.2 of [RFC3454].
	#
	# The output is the mapped string.
	new_value = ''
	for char in value:
		if ord(char) in MAPPED_TO_NOTHING:
			continue
		if ord(char) in MAPPED_TO_SPACE:
			char = ' '
		# No idea what "stored prefix string matching" is supposed to be
		if matching_type in (MatchingType.CASE_IGNORE_STRING,
		                     MatchingType.NUMERIC_STRING):
			char = stringprep.map_table_b2(char)
		new_value += char
	return new_value

def prepare_normalize(value):
	# 2.3.  Normalize
	#
	# The input string is to be normalized to Unicode Form KC
	# (compatibility composed) as described in [UAX15].  The output is the
	# normalized string.
	return unicodedata.normalize('NFKC', value)

def prepare_check_prohibited(value):
	# 2.4.  Prohibit
	#
	# All Unassigned code points are prohibited.  Unassigned code points
	# are listed in Table A.1 of [RFC3454].
	#
	# Characters that, per Section 5.8 of [RFC3454], change display
	# properties or are deprecated are prohibited.  These characters are
	# listed in Table C.8 of [RFC3454].
	#
	# Private Use code points are prohibited.  These characters are listed
	# in Table C.3 of [RFC3454].
	#
	# All non-character code points are prohibited.  These code points are
	# listed in Table C.4 of [RFC3454].
	#
	# Surrogate codes are prohibited.  These characters are listed in Table
	# C.5 of [RFC3454].
	#
	# The REPLACEMENT CHARACTER (U+FFFD) code point is prohibited.
	#
	# The step fails if the input string contains any prohibited code
	# point.  Otherwise, the output is the input string.
	for char in value:
		# pylint: disable=too-many-boolean-expressions
		if stringprep.in_table_a1(char) or \
		   stringprep.in_table_c8(char) or \
		   stringprep.in_table_c3(char) or \
		   stringprep.in_table_c4(char) or \
		   stringprep.in_table_c5(char) or \
		   ord(char) == 0xFFFD:
			return True
	return False

def prepare_insignificant_characters(value,
                                     matching_type=MatchingType.EXACT_STRING,
                                     substring_type=SubstringType.NONE):
	# 2.6.  Insignificant Character Handling
	#
	# In this step, the string is modified to ensure proper handling of
	# characters insignificant to the matching rule.  This modification
	# differs from matching rule to matching rule.
	#
	# Section 2.6.1 applies to case ignore and exact string matching.
	# Section 2.6.2 applies to numericString matching.
	# Section 2.6.3 applies to telephoneNumber matching.
	if matching_type in (MatchingType.CASE_IGNORE_STRING,
	                     MatchingType.EXACT_STRING):
		return prepare_insignificant_space(value, substring_type=substring_type)
	if matching_type == MatchingType.NUMERIC_STRING:
		return prepare_insignificant_numeric_string(value)
	if matching_type == MatchingType.TELEPHONE_NUMBER:
		return prepare_insignificant_telephone_number(value)
	raise ValueError('Invalid matching type')

def prepare_insignificant_space(value, substring_type=SubstringType.NONE):
	# 2.6.1.  Insignificant Space Handling
	#
	# For the purposes of this section, a space is defined to be the SPACE
	# (U+0020) code point followed by no combining marks.
	#
	#     NOTE - The previous steps ensure that the string cannot contain
	#            any code points in the separator class, other than SPACE
	#            (U+0020).
	#
	# For input strings that are attribute values or non-substring
	# assertion values:  If the input string contains no non-space
	# character, then the output is exactly two SPACEs.  Otherwise (the
	# input string contains at least one non-space character), the string
	# is modified such that the string starts with exactly one space
	# character, ends with exactly one SPACE character, and any inner
	# (non-empty) sequence of space characters is replaced with exactly two
	# SPACE characters.  For instance, the input strings
	# "foo<SPACE>bar<SPACE><SPACE>", result in the output
	# "<SPACE>foo<SPACE><SPACE>bar<SPACE>".
	#
	# For input strings that are substring assertion values: If the string
	# being prepared contains no non-space characters, then the output
	# string is exactly one SPACE.  Otherwise, the following steps are
	# taken:
	#
	# - Any inner (non-empty) sequence of space characters is replaced
  # with exactly two SPACE characters; [ERRATA 1757]
	#
	# -  If the input string is an initial substring, it is modified to
	# start with exactly one SPACE character;
	#
	# -  If the input string is an initial or an any substring that ends in
	# one or more space characters, it is modified to end with exactly
	# one SPACE character;
	#
	# -  If the input string is an any or a final substring that starts in
	# one or more space characters, it is modified to start with exactly
	# one SPACE character; and
	#
	# -  If the input string is a final substring, it is modified to end
	# with exactly one SPACE character.
	#
	# For instance, for the input string "foo<SPACE>bar<SPACE><SPACE>" as
	# an initial substring, the output would be
	# "<SPACE>foo<SPACE><SPACE>bar<SPACE>".  As an any or final substring,
	# the same input would result in "foo<SPACE><SPACE>bar<SPACE>".
	# [ERRATA 1758]

	# First we replace all spaces followed by no combining mark with U+FFFD.
	# U+FFFD is used because is it one of the prohibited characters.
	# Additionally we collapse all sequences of one or more SPACEs into
	# exactly two SPACEs.
	PLACEHOLDER = '\uFFFD' # pylint: disable=invalid-name
	new_value = ''
	for i, char in enumerate(value):
		if ord(char) != SPACE:
			new_value += char
		elif i + 1 < len(value) and ord(value[i + 1]) in COMBINING_MARKS:
			new_value += ' '
		elif not new_value or new_value[-1] != PLACEHOLDER:
			new_value += 2*PLACEHOLDER
	value = new_value
	if substring_type == SubstringType.NONE:
		value = PLACEHOLDER + value.strip(PLACEHOLDER) + PLACEHOLDER
	else:
		if substring_type == SubstringType.INITIAL:
			value = PLACEHOLDER + value.lstrip(PLACEHOLDER)
		if substring_type in (SubstringType.INITIAL, SubstringType.ANY) and value.endswith(PLACEHOLDER):
			value = value.rstrip(PLACEHOLDER) + PLACEHOLDER
		if substring_type in (SubstringType.ANY, SubstringType.FINAL) and value.startswith(PLACEHOLDER):
			value = PLACEHOLDER + value.lstrip(PLACEHOLDER)
		if substring_type == SubstringType.FINAL:
			value = value.rstrip(PLACEHOLDER) + PLACEHOLDER
	return value.replace(PLACEHOLDER, ' ')

def prepare_insignificant_numeric_string(value):
	# 2.6.2.  numericString Insignificant Character Handling
	#
	# For the purposes of this section, a space is defined to be the SPACE
	# (U+0020) code point followed by no combining marks.
	#
	# All spaces are regarded as insignificant and are to be removed.
	#
	# For example, removal of spaces from the Form KC string:
	#     "<SPACE><SPACE>123<SPACE><SPACE>456<SPACE><SPACE>"
	# would result in the output string:
	#     "123456"
	# and the Form KC string:
	#     "<SPACE><SPACE><SPACE>"
	# would result in the output string:
	#     "" (an empty string).
	new_value = ''
	# pylint: disable=consider-using-enumerate
	for i in range(len(value)):
		if ord(value[i]) == SPACE:
			if i + 1 >= len(value) or ord(value[i + 1]) not in COMBINING_MARKS:
				continue
		new_value += value[i]
	return new_value

def prepare_insignificant_telephone_number(value):
	# 2.6.3.  telephoneNumber Insignificant Character Handling
	#
	# For the purposes of this section, a hyphen is defined to be a
	# HYPHEN-MINUS (U+002D), ARMENIAN HYPHEN (U+058A), HYPHEN (U+2010),
	# NON-BREAKING HYPHEN (U+2011), MINUS SIGN (U+2212), SMALL HYPHEN-MINUS
	# (U+FE63), or FULLWIDTH HYPHEN-MINUS (U+FF0D) code point followed by
	# no combining marks and a space is defined to be the SPACE (U+0020)
	# code point followed by no combining marks.
	#
	# All hyphens and spaces are considered insignificant and are to be
	# removed.
	#
	# For example, removal of hyphens and spaces from the Form KC string:
	#     "<SPACE><HYPHEN>123<SPACE><SPACE>456<SPACE><HYPHEN>"
	# would result in the output string:
	#     "123456"
	# and the Form KC string:
	#     "<HYPHEN><HYPHEN><HYPHEN>"
	# would result in the (empty) output string:
	#     "".
	hyphen_chars = {0x002D, 0x058A, 0x2010, 0x2011, 0x2212, 0xFE63, 0xFF0D}
	new_value = ''
	# pylint: disable=consider-using-enumerate
	for i in range(len(value)):
		if ord(value[i]) == SPACE or ord(value[i]) in hyphen_chars:
			if i + 1 >= len(value) or ord(value[i + 1]) not in COMBINING_MARKS:
				continue
		new_value += value[i]
	return new_value
