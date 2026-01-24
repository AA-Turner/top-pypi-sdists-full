from checkHash import *

def test_isMD2_valid():
    assert isMD2("1c8f1e6a94aaa7145210bf90bb52871a") == True

def test_isMD4_valid():
    assert isMD4("94e3cb0fa9aa7a5ee3db74b79e915989") == True

def test_isMD5_valid():
    assert isMD5("65a8e27d8879283831b664bd8b7f0ad4") == True

def test_isMD6128_valid():
    assert isMD6128("229b1e1e0a0725416b8ec8cc0911facf") == True

def test_isMD6256_valid():
    assert isMD6256("ce5effce32637e6b8edaacc9284b873c3fd4e66f9779a79df67eb4a82dda8230") == True

def test_isMD6512_valid():
    assert isMD6512("1333db8caf3c69ce346f2dacef9805803f9d4c8594e4b20856ce1b0a70ccb0e68028b0b749d4aa25cbe489a2eb51260c0d7bd16d32dd4d7bfbd1f3ae8aa03260") == True

def test_isSHA1_valid():
    assert isSHA1("0a0a9f2a6772942557ab5355d76af442f8f65e01") == True

def test_isSHA2224_valid():
    assert isSHA2224("72a23dfa411ba6fde01dbfabf3b00a709c93ebf273dc29e2d8b261ff") == True

def test_isSHA2256_valid():
    assert isSHA2256("dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f") == True

def test_isSHA2384_valid():
    assert isSHA2384("5485cc9b3365b4305dfb4e8337e0a598a574f8242bf17289e0dd6c20a3cd44a089de16ab4ab308f63e44b1170eb5f515") == True

def test_isSHA2512_valid():
    assert isSHA2512("374d794a95cdcfd8b35993185fef9ba368f160d8daf432d08ba9f1ed1e5abe6cc69291e0fa2fe0006a52570ef18c19def4e617c33ce52ef0a6e5fbe318cb0387") == True

def test_isSHA3224_valid():
    assert isSHA3224("853048fb8b11462b6100385633c0cc8dcdc6e2b8e376c28102bc84f2") == True

def test_isSHA3256_valid():
    assert isSHA3256("1af17a664e3fa8e419b8ba05c2a173169df76162a5a286e0c405b460d478f7ef") == True

def test_isSHA3384_valid():
    assert isSHA3384("aa9ad8a49f31d2ddcabbb7010a1566417cff803fef50eba239558826f872e468c5743e7f026b0a8e5b2d7a1cc465cdbe") == True

def test_isSHA3512_valid():
    assert isSHA3512("38e05c33d7b067127f217d8c856e554fcff09c9320b8a5979ce2ff5d95dd27ba35d1fba50c562dfd1d6cc48bc9c5baa4390894418cc942d968f97bcb659419ed") == True

def test_isNTLM_valid():
    assert isNTLM("A0D6DCCEBBC32FD38E7355AF9926A582") == True

def test_isOtherHash_valid():
    assert isOtherHash("abcdef1234567890", 16) == True

def test_isRipeMD128_valid():
    assert isRipeMD128("67f9fe75ca2886dc76ad00f7276bdeba") == True

def test_isRipeMD160_valid():
    assert isRipeMD160("527a6a4b9a6da75607546842e0e00105350b1aaf") == True

def test_isRipeMD256_valid():
    assert isRipeMD256("567750c6d34dcba7ae038a80016f3ca3260ec25bfdb0b68bbb8e730b00b2447d") == True

def test_isRipeMD320_valid():
    assert isRipeMD320("f9832e5bb00576fc56c2221f404eb77addeafe49843c773f0df3fc5a996d5934f3c96e94aeb80e89") == True

def test_isCRC16_valid():
    assert isCRC16("fa4d") == True

def test_isCRC32_valid():
    assert isCRC32("ec4ac3d0") == True

def test_isAdler32_valid():
    assert isAdler32("1f9e046a") == True

def test_isWhirlpool_valid():
    assert isWhirlpool("3d837c9ef7bb291bd1dcfc05d3004af2eeb8c631dd6a6c4ba35159b8889de4b1ec44076ce7a8f7bfa497e4d9dcb7c29337173f78d06791f3c3d9e00cc6017f0b") == True

##

def test_isMD2_toolong():
    assert isMD2("1c8f1e6a94aaa7145210bf90bb52871aa") == False

def test_isMD4_toolong():
    assert isMD4("94e3cb0fa9aa7a5ee3db74b79e915989a") == False

def test_isMD5_toolong():
    assert isMD5("65a8e27d8879283831b664bd8b7f0ad4a") == False

def test_isMD6128_toolong():
    assert isMD6128("229b1e1e0a0725416b8ec8cc0911facfa") == False

def test_isMD6256_toolong():
    assert isMD6256("ce5effce32637e6b8edaacc9284b873c3fd4e66f9779a79df67eb4a82dda8230a") == False

def test_isMD6512_toolong():
    assert isMD6512("1333db8caf3c69ce346f2dacef9805803f9d4c8594e4b20856ce1b0a70ccb0e68028b0b749d4aa25cbe489a2eb51260c0d7bd16d32dd4d7bfbd1f3ae8aa03260a") == False

def test_isSHA1_toolong():
    assert isSHA1("0a0a9f2a6772942557ab5355d76af442f8f65e01a") == False

def test_isSHA2224_toolong():
    assert isSHA2224("72a23dfa411ba6fde01dbfabf3b00a709c93ebf273dc29e2d8b261ffa") == False

def test_isSHA2256_toolong():
    assert isSHA2256("dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986fa") == False

def test_isSHA2384_toolong():
    assert isSHA2384("5485cc9b3365b4305dfb4e8337e0a598a574f8242bf17289e0dd6c20a3cd44a089de16ab4ab308f63e44b1170eb5f515a") == False

def test_isSHA2512_toolong():
    assert isSHA2512("374d794a95cdcfd8b35993185fef9ba368f160d8daf432d08ba9f1ed1e5abe6cc69291e0fa2fe0006a52570ef18c19def4e617c33ce52ef0a6e5fbe318cb0387a") == False

def test_isSHA3224_toolong():
    assert isSHA3224("853048fb8b11462b6100385633c0cc8dcdc6e2b8e376c28102bc84f2a") == False

def test_isSHA3256_toolong():
    assert isSHA3256("1af17a664e3fa8e419b8ba05c2a173169df76162a5a286e0c405b460d478f7efa") == False

def test_isSHA3384_toolong():
    assert isSHA3384("aa9ad8a49f31d2ddcabbb7010a1566417cff803fef50eba239558826f872e468c5743e7f026b0a8e5b2d7a1cc465cdbea") == False

def test_isSHA3512_toolong():
    assert isSHA3512("38e05c33d7b067127f217d8c856e554fcff09c9320b8a5979ce2ff5d95dd27ba35d1fba50c562dfd1d6cc48bc9c5baa4390894418cc942d968f97bcb659419eda") == False

def test_isNTLM_toolong():
    assert isNTLM("A0D6DCCEBBC32FD38E7355AF9926A582A") == False

def test_isOtherHash_toolong():
    assert isOtherHash("abcdef1234567890a", 16) == False

def test_isRipeMD128_toolong():
    assert isRipeMD128("67f9fe75ca2886dc76ad00f7276bdebaa") == False

def test_isRipeMD160_toolong():
    assert isRipeMD160("527a6a4b9a6da75607546842e0e00105350b1aafa") == False

def test_isRipeMD256_toolong():
    assert isRipeMD256("567750c6d34dcba7ae038a80016f3ca3260ec25bfdb0b68bbb8e730b00b2447da") == False

def test_isRipeMD320_toolong():
    assert isRipeMD320("f9832e5bb00576fc56c2221f404eb77addeafe49843c773f0df3fc5a996d5934f3c96e94aeb80e89a") == False

def test_isCRC16_toolong():
    assert isCRC16("fa4da") == False

def test_isCRC32_toolong():
    assert isCRC32("ec4ac3d0a") == False

def test_isAdler32_toolong():
    assert isAdler32("1f9e046aa") == False

def test_isWhirlpool_toolong():
    assert isWhirlpool("3d837c9ef7bb291bd1dcfc05d3004af2eeb8c631dd6a6c4ba35159b8889de4b1ec44076ce7a8f7bfa497e4d9dcb7c29337173f78d06791f3c3d9e00cc6017f0ba") == False

##

def test_isMD2_tooshort():
    assert isMD2("1c8f1e6a94aaa7145210bf90bb52871") == False

def test_isMD4_tooshort():
    assert isMD4("94e3cb0fa9aa7a5ee3db74b79e91598") == False

def test_isMD5_tooshort():
    assert isMD5("65a8e27d8879283831b664bd8b7f0ad") == False

def test_isMD6128_tooshort():
    assert isMD6128("229b1e1e0a0725416b8ec8cc0911fac") == False

def test_isMD6256_tooshort():
    assert isMD6256("ce5effce32637e6b8edaacc9284b873c3fd4e66f9779a79df67eb4a82dda823") == False

def test_isMD6512_tooshort():
    assert isMD6512("1333db8caf3c69ce346f2dacef9805803f9d4c8594e4b20856ce1b0a70ccb0e68028b0b749d4aa25cbe489a2eb51260c0d7bd16d32dd4d7bfbd1f3ae8aa0326") == False

def test_isSHA1_tooshort():
    assert isSHA1("0a0a9f2a6772942557ab5355d76af442f8f65e0") == False

def test_isSHA2224_tooshort():
    assert isSHA2224("72a23dfa411ba6fde01dbfabf3b00a709c93ebf273dc29e2d8b261f") == False

def test_isSHA2256_tooshort():
    assert isSHA2256("dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a3621829") == False

def test_isSHA2384_tooshort():
    assert isSHA2384("5485cc9b3365b4305dfb4e8337e0a598a574f8242bf17289e0dd6c20a3cd44a089de16ab4ab308f63e44b1170eb5f51") == False

def test_isSHA2512_tooshort():
    assert isSHA2512("374d794a95cdcfd8b35993185fef9ba368f160d8daf432d08ba9f1ed1e5abe6cc69291e0fa2fe0006a52570ef18c19def4e617c33ce52ef0a6e5fbe318cb038") == False

def test_isSHA3224_tooshort():
    assert isSHA3224("853048fb8b11462b6100385633c0cc8dcdc6e2b8e376c28102bc84f") == False

def test_isSHA3256_tooshort():
    assert isSHA3256("1af17a664e3fa8e419b8ba05c2a173169df76162a5a286e0c405b460d478f7e") == False

def test_isSHA3384_tooshort():
    assert isSHA3384("aa9ad8a49f31d2ddcabbb7010a1566417cff803fef50eba239558826f872e468c5743e7f026b0a8e5b2d7a1cc465cdb") == False

def test_isSHA3512_tooshort():
    assert isSHA3512("38e05c33d7b067127f217d8c856e554fcff09c9320b8a5979ce2ff5d95dd27ba35d1fba50c562dfd1d6cc48bc9c5baa4390894418cc942d968f97bcb659419e") == False

def test_isNTLM_tooshort():
    assert isNTLM("A0D6DCCEBBC32FD38E7355AF9926A58") == False

def test_isOtherHash_tooshort():
    assert isOtherHash("abcdef123456789", 16) == False

def test_isRipeMD128_tooshort():
    assert isRipeMD128("67f9fe75ca2886dc76ad00f7276bdeb") == False

def test_isRipeMD160_tooshort():
    assert isRipeMD160("527a6a4b9a6da75607546842e0e00105350b1aa") == False

def test_isRipeMD256_tooshort():
    assert isRipeMD256("567750c6d34dcba7ae038a80016f3ca3260ec25bfdb0b68bbb8e730b00b2447") == False

def test_isRipeMD320_tooshort():
    assert isRipeMD320("f9832e5bb00576fc56c2221f404eb77addeafe49843c773f0df3fc5a996d5934f3c96e94aeb80e8") == False

def test_isCRC16_tooshort():
    assert isCRC16("fa4") == False

def test_isCRC32_tooshort():
    assert isCRC32("ec4ac3d") == False

def test_isAdler32_tooshort():
    assert isAdler32("1f9e046") == False

def test_isWhirlpool_tooshort():
    assert isWhirlpool("3d837c9ef7bb291bd1dcfc05d3004af2eeb8c631dd6a6c4ba35159b8889de4b1ec44076ce7a8f7bfa497e4d9dcb7c29337173f78d06791f3c3d9e00cc6017f0") == False

##

def test_isNTLM_wrongcase():
    assert isNTLM("a0d6dccebbc32fd38e7355af9926a582") == False

##

def test_isMD2_invalidcharacter():
    assert isMD2("1c8f1e6a94aaa7145210bf90bb52871ag") == False

def test_isMD4_invalidcharacter():
    assert isMD4("94e3cb0fa9aa7a5ee3db74b79e915989g") == False

def test_isMD5_invalidcharacter():
    assert isMD5("65a8e27d8879283831b664bd8b7f0ad4g") == False

def test_isMD6128_invalidcharacter():
    assert isMD6128("229b1e1e0a0725416b8ec8cc0911facfg") == False

def test_isMD6256_invalidcharacter():
    assert isMD6256("ce5effce32637e6b8edaacc9284b873c3fd4e66f9779a79df67eb4a82dda8230g") == False

def test_isMD6512_invalidcharacter():
    assert isMD6512("1333db8caf3c69ce346f2dacef9805803f9d4c8594e4b20856ce1b0a70ccb0e68028b0b749d4aa25cbe489a2eb51260c0d7bd16d32dd4d7bfbd1f3ae8aa03260g") == False

def test_isSHA1_invalidcharacter():
    assert isSHA1("0a0a9f2a6772942557ab5355d76af442f8f65e01g") == False

def test_isSHA2224_invalidcharacter():
    assert isSHA2224("72a23dfa411ba6fde01dbfabf3b00a709c93ebf273dc29e2d8b261ffg") == False

def test_isSHA2256_invalidcharacter():
    assert isSHA2256("dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986fg") == False

def test_isSHA2384_invalidcharacter():
    assert isSHA2384("5485cc9b3365b4305dfb4e8337e0a598a574f8242bf17289e0dd6c20a3cd44a089de16ab4ab308f63e44b1170eb5f515g") == False

def test_isSHA2512_invalidcharacter():
    assert isSHA2512("374d794a95cdcfd8b35993185fef9ba368f160d8daf432d08ba9f1ed1e5abe6cc69291e0fa2fe0006a52570ef18c19def4e617c33ce52ef0a6e5fbe318cb0387g") == False

def test_isSHA3224_invalidcharacter():
    assert isSHA3224("853048fb8b11462b6100385633c0cc8dcdc6e2b8e376c28102bc84f2g") == False

def test_isSHA3256_invalidcharacter():
    assert isSHA3256("1af17a664e3fa8e419b8ba05c2a173169df76162a5a286e0c405b460d478f7efg") == False

def test_isSHA3384_invalidcharacter():
    assert isSHA3384("aa9ad8a49f31d2ddcabbb7010a1566417cff803fef50eba239558826f872e468c5743e7f026b0a8e5b2d7a1cc465cdbeg") == False

def test_isSHA3512_invalidcharacter():
    assert isSHA3512("38e05c33d7b067127f217d8c856e554fcff09c9320b8a5979ce2ff5d95dd27ba35d1fba50c562dfd1d6cc48bc9c5baa4390894418cc942d968f97bcb659419edg") == False

def test_isNTLM_invalidcharacter():
    assert isNTLM("A0D6DCCEBBC32FD38E7355AF9926A582G") == False

def test_isOtherHash_invalidcharacter():
    assert isOtherHash("abcdef01234567890g", 17) == False

def test_isRipeMD128_invalidcharacter():
    assert isRipeMD128("67f9fe75ca2886dc76ad00f7276bdebag") == False

def test_isRipeMD160_invalidcharacter():
    assert isRipeMD160("527a6a4b9a6da75607546842e0e00105350b1aafg") == False

def test_isRipeMD256_invalidcharacter():
    assert isRipeMD256("567750c6d34dcba7ae038a80016f3ca3260ec25bfdb0b68bbb8e730b00b2447dg") == False

def test_isRipeMD320_invalidcharacter():
    assert isRipeMD320("f9832e5bb00576fc56c2221f404eb77addeafe49843c773f0df3fc5a996d5934f3c96e94aeb80e89g") == False

def test_isCRC16_invalidcharacter():
    assert isCRC16("fa4dg") == False

def test_isCRC32_invalidcharacter():
    assert isCRC32("ec4ac3d0g") == False

def test_isAdler32_invalidcharacter():
    assert isAdler32("1f9e046ag") == False

def test_isWhirlpool_invalidcharacter():
    assert isWhirlpool("3d837c9ef7bb291bd1dcfc05d3004af2eeb8c631dd6a6c4ba35159b8889de4b1ec44076ce7a8f7bfa497e4d9dcb7c29337173f78d06791f3c3d9e00cc6017f0bg") == False
