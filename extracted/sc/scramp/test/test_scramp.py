import hashlib
from collections import OrderedDict
from ssl import SSLObject, SSLSocket

import pytest

from scramp import (
    ScramClient,
    ScramException,
    ScramMechanism,
)
from scramp.core import (
    MECHS,
    AuthFn,
    CBindData,
    CbName,
    ChannelBinding,
    ClientFinal,
    Gs2Header,
    IterationCount,
    Message,
    Nonce,
    Password,
    Salt,
    ServerError,
    ServerFinal,
    ServerFirst,
    ServerStage,
    Username,
    _check_client_key,
    _check_stage,
    _get_client_final,
    _get_client_first,
    _get_server_final,
    _get_server_first,
    _make_auth_message,
    _set_client_final,
    _set_client_first,
    _set_server_final,
    _set_server_first,
    _username_unescape,
)
from scramp.utils import b64dec, b64enc


@pytest.mark.parametrize(
    "msg,att_strs,result",
    [
        ["c=jk,i=5000", ["ci"], OrderedDict(c="jk", i=IterationCount(5000))],
        ["c=jk,i=4096", ["abc", "ci"], OrderedDict(c="jk", i=IterationCount(4096))],
        ["c=b", ["c"], OrderedDict(c="b")],
        ["k=k,c=b", ["*c"], OrderedDict(k="k", c="b")],
    ],
)
def test_Message_init(msg, att_strs, result):
    msg = Message(msg, "trial", *att_strs)
    assert msg._msg == result


@pytest.mark.parametrize(
    "msg,att_seqs,error_msg",
    [
        [
            "junk",
            ["abc"],
            (
                "Malformed trial message. Attributes must be separated by a ',' "
                "and each attribute must start with a letter followed by a '=': "
                "other-error"
            ),
        ],
        [
            "",
            ["abc"],
            (
                "Malformed trial message. Attributes must be separated by a ',' and "
                "each attribute must start with a letter followed by a '=': other-error"
            ),
        ],
        [
            "c=jk,d=kln",
            ["abc"],
            (
                "Malformed trial message. Expected the attribute str to be one of "
                "['abc'] but found 'c*' (where '*' is unrecognised attributes): "
                "other-error"
            ),
        ],
        [
            "c=jk,c=kln",
            ["c"],
            "Duplicate attributes not allowed in message: other-error",
        ],
        [
            "e=error",
            ["c"],
            (
                "Malformed trial message. Expected the attribute str to be one of "
                "['c'] but found 'e': other-error"
            ),
        ],
        [
            "e=\x00",
            ["e"],
            (
                "Malformed trial message. Attribute values can't contain the NUL "
                "character: other-error"
            ),
        ],
        [
            "r=a,x=b,p=c,y=d",
            ["r*p"],
            (
                "Malformed trial message. Expected the attribute str to be one of "
                "['r*p'] but found 'r*p*' (where '*' is unrecognised attributes): "
                "other-error"
            ),
        ],
        [
            b"c=jk,i=kln",
            ["r*p"],
            "A message must be of type str: other-error",
        ],
        # Malformed iteration count in server first
        [
            (
                "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
                "s=W22ZaJ0SNY7soEsUEjb6gQ==,i=not_an_integer"
            ),
            ["rsi"],
            "The iteration count can only contain ASCII digits: other-error",
        ],
        # Server signature contains invalid base 64 encoding
        [
            ("v=é"),
            ["v"],
            "Invalid base 64 encoding: invalid-encoding",
        ],
    ],
)
def test_Message_init_error(msg, att_seqs, error_msg):
    with pytest.raises(ScramException) as exc_info:
        Message(msg, "trial", *att_seqs)

    assert str(exc_info.value) == error_msg


@pytest.mark.parametrize(
    "i,error_msg,server_error",
    [
        [
            True,
            "The value must be an int: other-error",
            ServerError.OTHER_ERROR,
        ],
    ],
)
def test_IterationCount_init_error(i, error_msg, server_error):
    with pytest.raises(ScramException) as exc_info:
        IterationCount(i)

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


@pytest.mark.parametrize(
    "i,error_msg,server_error",
    [
        [
            "",
            "The iteration count must not be empty: other-error",
            ServerError.OTHER_ERROR,
        ],
    ],
)
def test_IterationCount_from_str_error(i, error_msg, server_error):
    with pytest.raises(ScramException) as exc_info:
        IterationCount.from_str(i)

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


def test_IterationCount_lt_error():
    IterationCount(4096).__lt__(5000)
    with pytest.raises(TypeError) as exc_info:
        _ = IterationCount(4096) < 5000

    assert (
        str(exc_info.value)
        == "'<' not supported between instances of 'IterationCount' and 'int'"
    )


@pytest.mark.parametrize(
    "username, expected_username",
    [
        # RFC 5802, section 5.1
        ["u=3Dse=2Cr", "u=se,r"],
    ],
)
def test_username_unescape(username, expected_username):
    actual_username = _username_unescape(username)
    assert actual_username == expected_username


@pytest.mark.parametrize(
    "username,error_msg,server_error",
    [
        # RFC 5802, section 5.1
        [
            "=",
            (
                "An '=' in a username must be followed by '3D', or  '2C': "
                "invalid-username-encoding"
            ),
            ServerError.INVALID_USERNAME_ENCODING,
        ],
    ],
)
def test_username_unescape_error(username, error_msg, server_error):
    with pytest.raises(ScramException) as exc_info:
        _username_unescape(username)

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


@pytest.mark.parametrize(
    "data,error_msg,server_error",
    [
        [
            b"",
            "Problem loading certificate from DER: other-error",
            ServerError.OTHER_ERROR,
        ],
    ],
)
def test_CBindData_from_der_error(data, error_msg, server_error):
    with pytest.raises(ScramException) as exc_info:
        CBindData.from_der(data)

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


@pytest.mark.parametrize(
    "cb,use_binding",
    [
        [
            ChannelBinding(CbName("tls-unique"), CBindData(b"bee")),
            True,
        ],
    ],
)
def test_Gs2Header_from_binding(cb, use_binding):
    Gs2Header.from_binding(cb, True)


@pytest.mark.parametrize(
    "header_str,error_msg,server_error",
    [
        [
            "p=an=ame,,",
            (
                "The channel binding name must contain only ASCII characters that are "
                "alphabetic or a digit or '.' or '-': other-error"
            ),
            ServerError.OTHER_ERROR,
        ],
        [
            "p=tls-unique,,trailing",  # No traling characters after the last comma
            "The gs2-header can't have characters after the last comma: other-error",
            ServerError.OTHER_ERROR,
        ],
    ],
)
def test_Gs2Header_from_str_error(header_str, error_msg, server_error):
    with pytest.raises(ScramException) as exc_info:
        Gs2Header.from_str(header_str)
    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


@pytest.mark.parametrize(
    "gs2_char,cb_name,expected",
    [
        ["p", CbName("tls-unique"), "p=tls-unique,,"],
    ],
)
def test_Gs2Header_str(gs2_char, cb_name, expected):
    gs2_header = Gs2Header(gs2_char, cb_name)
    assert str(gs2_header) == expected


@pytest.mark.parametrize(
    "gs2_char,cb_name",
    [
        ["p", CbName("tls-unique")],
    ],
)
def test_Gs2Header_eq(gs2_char, cb_name):
    gs2_header_a = Gs2Header(gs2_char, cb_name)
    gs2_header_b = Gs2Header(gs2_char, cb_name)
    assert gs2_header_a == gs2_header_b


@pytest.mark.parametrize(
    "username,error_msg,server_error",
    [
        [
            "",
            "The username cannot be empty: other-error",
            ServerError.OTHER_ERROR,
        ],
        [
            "\u00ad",
            "The username cannot be empty: other-error",
            ServerError.OTHER_ERROR,
        ],
    ],
)
def test_Username_init_error(username, error_msg, server_error):
    with pytest.raises(ScramException) as exc_info:
        Username(username)

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


@pytest.mark.parametrize(
    "salt,error_msg,server_error",
    [
        [
            "",  # Must be bytes
            (
                "The 'salt' must be of type bytes, but found type <class 'str'>: "
                "other-error"
            ),
            ServerError.OTHER_ERROR,
        ],
    ],
)
def test_Salt_init_error(salt, error_msg, server_error):
    with pytest.raises(ScramException) as exc_info:
        Salt(salt)

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


@pytest.mark.parametrize(
    "salt_str,error_msg,server_error",
    [
        [
            "!!!",
            "Invalid base 64 encoding: invalid-encoding",
            ServerError.INVALID_ENCODING,
        ],
    ],
)
def test_Salt_from_str_error(salt_str, error_msg, server_error):
    with pytest.raises(ScramException) as exc_info:
        Salt.from_str(salt_str)

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


@pytest.mark.parametrize(
    "nonce,error_msg,server_error",
    [
        [
            b"",  # Must be str
            (
                "The 'nonce' must be of type str, but found type <class 'bytes'>: "
                "other-error"
            ),
            ServerError.OTHER_ERROR,
        ],
        [
            "",  # Can't be empty
            "An empty string isn't allowed: other-error",
            ServerError.OTHER_ERROR,
        ],
    ],
)
def test_Nonce_init_error(nonce, error_msg, server_error):
    with pytest.raises(ScramException) as exc_info:
        Nonce(nonce)

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


@pytest.mark.parametrize(
    "name,error_msg,server_error",
    [
        [
            "bogus",
            (
                "The channel binding type is not recognised by Scramp. The recognised "
                "types are ['tls-exporter', 'tls-server-end-point', 'tls-unique', "
                "'tls-unique-for-telnet']: unsupported-channel-binding-type"
            ),
            ServerError.UNSUPPORTED_CHANNEL_BINDING_TYPE,
        ],
        [
            "tls-exporter",
            (
                "The channel binding types ['tls-exporter'] are not supported by "
                "Scramp. Please see the README for details: "
                "unsupported-channel-binding-type"
            ),
            ServerError.UNSUPPORTED_CHANNEL_BINDING_TYPE,
        ],
    ],
)
def test_CbName_init_error(name, error_msg, server_error):
    with pytest.raises(ScramException) as exc_info:
        CbName(name)

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


def test_AuthFn_init_callable():
    class Auth:
        def __call__(self, _):
            pass

    AuthFn(Auth())


@pytest.mark.parametrize(
    "return_value,error_msg,server_error",
    [
        [
            "",
            "auth_fun must return None or a tuple: other-error",
            ServerError.OTHER_ERROR,
        ],
        [
            (),
            "auth_fun must return a tuple with exactly four items: other-error",
            ServerError.OTHER_ERROR,
        ],
    ],
)
def test_AuthFn_call_error(return_value, error_msg, server_error):
    class Auth:
        def __call__(self, _):
            return return_value

    auth_fn = AuthFn(Auth())

    with pytest.raises(ScramException) as exc_info:
        auth_fn("pencil")

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


@pytest.mark.parametrize(
    "mechanism_name",
    ["SCRAM-SHA-256", "SCRAM-SHA-512-PLUS", "SCRAM-SHA3-512-PLUS"],
)
def test_ScramMechanism_init(mechanism_name):
    mechanism = ScramMechanism(mechanism_name)
    mech_data = MECHS[mechanism_name]

    assert mechanism.strength == mech_data.strength
    assert mechanism.iteration_count == mech_data.iteration_count


@pytest.mark.parametrize(
    "mechanism_name,password,iteration_count,salt",
    [
        [
            "SCRAM-SHA3-512",
            "pencil",
            50000,
            b"aaaaaaaaaaaaaaaa",
        ],
        [
            "SCRAM-SHA3-512",
            "pencil",
            20000,
            b"xxxxxxxxxxxxxxxx",
        ],
        [
            "SCRAM-SHA-512-PLUS",
            "pencil",
            50000,
            b"aaaaaaaaaaaaaaaa",
        ],
        [
            "SCRAM-SHA3-512-PLUS",
            "pencil",
            20000,
            b"xxxxxxxxxxxxxxxx",
        ],
    ],
)
def test_ScramMechanism_make_auth_info(mechanism_name, password, iteration_count, salt):
    m = ScramMechanism(mechanism=mechanism_name)
    m.make_auth_info(password, iteration_count, salt)


@pytest.mark.parametrize(
    "mechanism_name,password,iteration_count,salt,error_msg,server_error",
    [
        [
            "SCRAM-SHA3-512",
            "pencil",
            1,
            b"aaaaaaaaaaaaaaaa",
            "The value must not be < 4096: other-error",
            ServerError.OTHER_ERROR,
        ],
        [
            "SCRAM-SHA3-512",
            "pencil",
            20000,
            "",
            (
                "The 'salt' must be of type bytes, but found type "
                "<class 'str'>: other-error"
            ),
            ServerError.OTHER_ERROR,
        ],
    ],
)
def test_ScramMechanism_make_auth_info_error(
    mechanism_name, password, iteration_count, salt, error_msg, server_error
):
    m = ScramMechanism(mechanism=mechanism_name)
    with pytest.raises(ScramException) as exc_info:
        m.make_auth_info(password, iteration_count, salt)

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


@pytest.mark.parametrize(
    "ssl_socket_class",
    [
        SSLSocket,
        SSLObject,
    ],
)
def test_ScramMechanism_make_server_tls_unique_ssl_socket(mocker, ssl_socket_class):
    m = ScramMechanism()

    def auth_fn(_):
        return None

    cb_name = "tls-unique"
    cb_data = b"x"
    ssl_socket = mocker.create_autospec(ssl_socket_class, instance=True)
    ssl_socket.get_channel_binding.return_value = cb_data

    channel_binding = cb_name, ssl_socket
    server = m.make_server(auth_fn, channel_binding=channel_binding)

    ssl_socket.get_channel_binding.assert_called_once_with(cb_name)
    assert server.cb == ChannelBinding(CbName(cb_name), CBindData(cb_data))


@pytest.mark.parametrize(
    "mechanism,username,password,channel_binding,msg",
    [
        [
            "SCRAM-SHA-512-PLUS",
            "max",
            "pencil",
            ("c", "d"),
            (
                "The channel binding type is not recognised by Scramp. The recognised "
                "types are ['tls-exporter', 'tls-server-end-point', 'tls-unique', "
                "'tls-unique-for-telnet']: unsupported-channel-binding-type"
            ),
        ],
        # Non-ascii character in cert file str
        [
            "SCRAM-SHA-512-PLUS",
            "max",
            "pencil",
            ("tls-server-end-point", "Æ"),
            (
                "The PEM encoded certificate str must only contain ASCII characters: "
                "other-error"
            ),
        ],
        # Cert file str is empty
        [
            "SCRAM-SHA-512-PLUS",
            "max",
            "pencil",
            ("tls-server-end-point", ""),
            "The PEM encoded certificate str doesn't seem to be valid: other-error",
        ],
    ],
)
def test_ScramMechanism_make_server_error(
    mechanism, username, password, channel_binding, msg
):
    with pytest.raises(ScramException) as exc_info:
        m = ScramMechanism(mechanism=mechanism)

        def auth_fn(_):
            return None

        m.make_server(auth_fn, channel_binding=channel_binding)

    assert str(exc_info.value) == msg


@pytest.mark.parametrize(
    "hf,stored_key, auth_msg, proof, msg",
    [
        # Client signature and proof of different lengths, so xor() should fail
        [
            hashlib.sha256,
            b64dec(
                "7tmSwbz0qdlCWaMqA8gm8gNQ3VHbW1zEKpX+ST1QX5RzBefTHhYe3"
                "EtogaGggZioWX1pp471+gbmGOn31w5iTg=="
            ),
            b"n=user,r=fyko+d2lbbFgONRv9qkxdawL,",
            b"W22ZaJ0SNY7soEsUEjb6gQ==",
            "Can't create client key.: invalid-proof",
        ],
    ],
)
def test_check_client_key_fail(hf, stored_key, auth_msg, proof, msg):
    with pytest.raises(ScramException) as exc_info:
        _check_client_key(hf, stored_key, auth_msg, proof)

    assert str(exc_info.value) == msg
    assert exc_info.value.server_error == ServerError.INVALID_PROOF


EXCHANGE_SCRAM_SHA_256 = {
    "username": "user",
    "password": "pencil",
    "c_mechanisms": ["SCRAM-SHA-256"],
    "s_mechanism": "SCRAM-SHA-256",
    "cfirst": "n,,n=user,r=rOprNGfwEbeRWgbNEkqO",
    "sfirst": "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
    "s=W22ZaJ0SNY7soEsUEjb6gQ==,i=4096",
    "cfinal": "c=biws,r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
    "p=dHzbZapWIk4jUhN+Ute9ytag9zjfMHgsqmmiz7AndVQ=",
    "cfinal_without_proof": "c=biws,"
    "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
    "sfinal": "v=6rriTRBi23WpRR/wtup+mMhUZUn/dB5nLTJRsjl95G4=",
    "cfirst_bare": "n=user,r=rOprNGfwEbeRWgbNEkqO",
    "c_nonce": "rOprNGfwEbeRWgbNEkqO",
    "s_nonce": "%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
    "nonce": "rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
    "auth_message": b"n=user,r=rOprNGfwEbeRWgbNEkqO,"
    b"r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
    b"s=W22ZaJ0SNY7soEsUEjb6gQ==,i=4096,c=biws,"
    b"r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
    "salt": "W22ZaJ0SNY7soEsUEjb6gQ==",
    "iterations": 4096,
    "server_signature": "6rriTRBi23WpRR/wtup+mMhUZUn/dB5nLTJRsjl95G4=",
    "hf": hashlib.sha256,
    "stored_key": "WG5d8oPm3OtcPnkdi4Uo7BkeZkBFzpcXkuLmtbsT4qY=",
    "server_key": "wfPLwcE6nTWhTAmQ7tl2KeoiWGPlZqQxSrmfPwDl2dU=",
    "c_use_binding": False,
    "s_init_use_binding": False,
    "s_use_binding": False,
    "c_channel_binding": None,
    "s_channel_binding": None,
}

EXCHANGE_SCRAM_SHA_256_PLUS = {
    "username": "user",
    "password": "pencil",
    "c_mechanisms": ["SCRAM-SHA-256-PLUS"],
    "s_mechanism": "SCRAM-SHA-256-PLUS",
    "cfirst": "p=tls-unique,,n=user,r=rOprNGfwEbeRWgbNEkqO",
    "sfirst": "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
    "s=W22ZaJ0SNY7soEsUEjb6gQ==,i=4096",
    "cfinal": "c=cD10bHMtdW5pcXVlLCx4eHg=,"
    "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
    "p=v0J7PaQUPWowoTrwRLCKLzIZBpNUhWFlTrUKI1j9DpM=",
    "cfinal_without_proof": "c=cD10bHMtdW5pcXVlLCx4eHg=,"
    "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
    "sfinal": "v=XjAev9iHBOvTxT+eNzBaFmP1IrqWah2PpZAa0wQrfY4=",
    "cfirst_bare": "n=user,r=rOprNGfwEbeRWgbNEkqO",
    "c_nonce": "rOprNGfwEbeRWgbNEkqO",
    "s_nonce": "%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
    "nonce": "rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
    "auth_message": b"n=user,r=rOprNGfwEbeRWgbNEkqO,"
    b"r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
    b"s=W22ZaJ0SNY7soEsUEjb6gQ==,i=4096,c=cD10bHMtdW5pcXVlLCx4eHg=,"
    b"r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
    "salt": "W22ZaJ0SNY7soEsUEjb6gQ==",
    "iterations": 4096,
    "server_signature": "XjAev9iHBOvTxT+eNzBaFmP1IrqWah2PpZAa0wQrfY4=",
    "hf": hashlib.sha256,
    "stored_key": "WG5d8oPm3OtcPnkdi4Uo7BkeZkBFzpcXkuLmtbsT4qY=",
    "server_key": "wfPLwcE6nTWhTAmQ7tl2KeoiWGPlZqQxSrmfPwDl2dU=",
    "c_use_binding": True,
    "s_init_use_binding": True,
    "s_use_binding": True,
    "c_channel_binding": ("tls-unique", b"xxx"),
    "s_channel_binding": ("tls-unique", b"xxx"),
}


params = [
    # Standard SCRAM_SHA_1
    {
        "username": "user",
        "password": "pencil",
        "c_mechanisms": ["SCRAM-SHA-1"],
        "s_mechanism": "SCRAM-SHA-1",
        "cfirst": "n,,n=user,r=fyko+d2lbbFgONRv9qkxdawL",
        "cfirst_bare": "n=user,r=fyko+d2lbbFgONRv9qkxdawL",
        "sfirst": "r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        "s=QSXCR+Q6sek8bf92,i=4096",
        "cfinal": "c=biws,r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        "p=v0X8v3Bz2T0CJGbJQyF0X+HI4Ts=",
        "cfinal_without_proof": "c=biws,r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "sfinal": "v=rmF9pqV8S7suAoZWja4dJRkFsKQ=",
        "c_nonce": "fyko+d2lbbFgONRv9qkxdawL",
        "s_nonce": "3rfcNHYJY1ZVvWVs7j",
        "nonce": "fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "auth_message": b"n=user,r=fyko+d2lbbFgONRv9qkxdawL,"
        b"r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        b"s=QSXCR+Q6sek8bf92,i=4096,c=biws,"
        b"r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "salt": "QSXCR+Q6sek8bf92",
        "iterations": 4096,
        "server_signature": "rmF9pqV8S7suAoZWja4dJRkFsKQ=",
        "hf": hashlib.sha1,
        "stored_key": "6dlGYMOdZcOPutkcNY8U2g7vK9Y=",
        "server_key": "D+CSWLOshSulAsxiupA+qs2/fTE=",
        "c_use_binding": False,
        "s_init_use_binding": False,
        "s_use_binding": False,
        "c_channel_binding": None,
        "s_channel_binding": None,
    },
    # SCRAM_SHA_1 where the client supports channel binding but the server does not
    {
        "username": "user",
        "password": "pencil",
        "c_mechanisms": ["SCRAM-SHA-1"],
        "s_mechanism": "SCRAM-SHA-1",
        "cfirst": "y,,n=user,r=fyko+d2lbbFgONRv9qkxdawL",
        "sfirst": "r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        "s=QSXCR+Q6sek8bf92,i=4096",
        "cfinal": "c=eSws,r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        "p=BjZF5dV+EkD3YCb3pH3IP8riMGw=",
        "cfinal_without_proof": "c=eSws,r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "sfinal": "v=dsprQ5R2AGYt1kn4bQRwTAE0PTU=",
        "cfirst_bare": "n=user,r=fyko+d2lbbFgONRv9qkxdawL",
        "c_nonce": "fyko+d2lbbFgONRv9qkxdawL",
        "s_nonce": "3rfcNHYJY1ZVvWVs7j",
        "nonce": "fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "auth_message": b"n=user,r=fyko+d2lbbFgONRv9qkxdawL,"
        b"r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        b"s=QSXCR+Q6sek8bf92,i=4096,c=eSws,"
        b"r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "salt": "QSXCR+Q6sek8bf92",
        "iterations": 4096,
        "server_signature": "dsprQ5R2AGYt1kn4bQRwTAE0PTU=",
        "hf": hashlib.sha1,
        "stored_key": "6dlGYMOdZcOPutkcNY8U2g7vK9Y=",
        "server_key": "D+CSWLOshSulAsxiupA+qs2/fTE=",
        "c_use_binding": False,
        "s_init_use_binding": False,
        "s_use_binding": False,
        "c_channel_binding": ("tls-unique", b"xxx"),
        "s_channel_binding": None,
    },
    # Standard SCRAM_SHA_1_PLUS
    {
        "username": "user",
        "password": "pencil",
        "c_mechanisms": ["SCRAM-SHA-1-PLUS"],
        "s_mechanism": "SCRAM-SHA-1-PLUS",
        "cfirst": "p=tls-unique,,n=user,r=fyko+d2lbbFgONRv9qkxdawL",
        "sfirst": "r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        "s=QSXCR+Q6sek8bf92,i=4096",
        "cfinal": "c=cD10bHMtdW5pcXVlLCx4eHg=,"
        "r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        "p=/63TtbB5lIS6610+k4/luJMJqAI=",
        "cfinal_without_proof": "c=cD10bHMtdW5pcXVlLCx4eHg=,"
        "r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "sfinal": "v=GCPHy5gy1sRwXTCbwNhiiWIzLtU=",
        "cfirst_bare": "n=user,r=fyko+d2lbbFgONRv9qkxdawL",
        "c_nonce": "fyko+d2lbbFgONRv9qkxdawL",
        "s_nonce": "3rfcNHYJY1ZVvWVs7j",
        "nonce": "fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "auth_message": b"n=user,r=fyko+d2lbbFgONRv9qkxdawL,"
        b"r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        b"s=QSXCR+Q6sek8bf92,i=4096,c=cD10bHMtdW5pcXVlLCx4eHg=,"
        b"r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "salt": "QSXCR+Q6sek8bf92",
        "iterations": 4096,
        "server_signature": "GCPHy5gy1sRwXTCbwNhiiWIzLtU=",
        "hf": hashlib.sha1,
        "stored_key": "6dlGYMOdZcOPutkcNY8U2g7vK9Y=",
        "server_key": "D+CSWLOshSulAsxiupA+qs2/fTE=",
        "c_use_binding": True,
        "s_init_use_binding": True,
        "s_use_binding": True,
        "c_channel_binding": ("tls-unique", b"xxx"),
        "s_channel_binding": ("tls-unique", b"xxx"),
    },
    EXCHANGE_SCRAM_SHA_256,
    EXCHANGE_SCRAM_SHA_256_PLUS,
    # Standard SCRAM_SHA_1 with username that needs escaping
    {
        "username": "u=se,r",
        "password": "pencil",
        "c_mechanisms": ["SCRAM-SHA-1"],
        "s_mechanism": "SCRAM-SHA-1",
        "cfirst": "n,,n=u=3Dse=2Cr,r=fyko+d2lbbFgONRv9qkxdawL",
        "cfirst_bare": "n=u=3Dse=2Cr,r=fyko+d2lbbFgONRv9qkxdawL",
        "sfirst": "r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        "s=QSXCR+Q6sek8bf92,i=4096",
        "cfinal": "c=biws,r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        "p=vqBTKFd8G1j1sueD4sUotSjIYfs=",
        "cfinal_without_proof": "c=biws,r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "sfinal": "v=ySs7A8qkVwzSKc4pAqR/R4+/50g=",
        "c_nonce": "fyko+d2lbbFgONRv9qkxdawL",
        "s_nonce": "3rfcNHYJY1ZVvWVs7j",
        "nonce": "fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "auth_message": b"n=u=3Dse=2Cr,r=fyko+d2lbbFgONRv9qkxdawL,"
        b"r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        b"s=QSXCR+Q6sek8bf92,i=4096,c=biws,"
        b"r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "salt": "QSXCR+Q6sek8bf92",
        "iterations": 4096,
        "server_signature": "ySs7A8qkVwzSKc4pAqR/R4+/50g=",
        "hf": hashlib.sha1,
        "stored_key": "6dlGYMOdZcOPutkcNY8U2g7vK9Y=",
        "server_key": "D+CSWLOshSulAsxiupA+qs2/fTE=",
        "c_use_binding": False,
        "s_init_use_binding": False,
        "s_use_binding": False,
        "c_channel_binding": None,
        "s_channel_binding": None,
    },
    # SCRAM_SHA3_512
    {
        "username": "user",
        "password": "pencil",
        "c_mechanisms": ["SCRAM-SHA3-512"],
        "s_mechanism": "SCRAM-SHA3-512",
        "cfirst": "n,,n=user,r=fyko+d2lbbFgONRv9qkxdawL",
        "cfirst_bare": "n=user,r=fyko+d2lbbFgONRv9qkxdawL",
        "sfirst": "r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        "s=QSXCR+Q6sek8bf92,i=10000",
        "cfinal": "c=biws,r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        "p=KOkd92LduC09A+RDxbTvgxH9Nn6efom/uAy6U5/fqpwLH1J+wQnZcKx5W1zd"
        "7YMPU8PrusBUK5RgRk4yHx+3Mg==",
        "cfinal_without_proof": "c=biws,r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "sfinal": "v=L8sKlyFigUkpTO8I3eaJSyuQhsDynb2eD1MWl+2ELjw7fJkbzr"
        "8N6Z41pkOAfjzuW/sT6+UElBTt5WbaxZ8oag==",
        "c_nonce": "fyko+d2lbbFgONRv9qkxdawL",
        "s_nonce": "3rfcNHYJY1ZVvWVs7j",
        "nonce": "fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "auth_message": b"n=user,r=fyko+d2lbbFgONRv9qkxdawL,"
        b"r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,"
        b"s=QSXCR+Q6sek8bf92,i=10000,c=biws,"
        b"r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j",
        "salt": "QSXCR+Q6sek8bf92",
        "iterations": 10000,
        "server_signature": "L8sKlyFigUkpTO8I3eaJSyuQhsDynb2eD1MWl+"
        "2ELjw7fJkbzr8N6Z41pkOAfjzuW/sT6+UElBTt5WbaxZ8oag==",
        "hf": hashlib.sha3_512,
        "stored_key": "7tmSwbz0qdlCWaMqA8gm8gNQ3VHbW1zEKpX+ST1QX5RzBefTHhYe3"
        "EtogaGggZioWX1pp471+gbmGOn31w5iTg==",
        "server_key": "lLR0hmplzlAmeKBf3SO/jzdaPse5fUr+phiGcjHEq84uBSsC"
        "yaP21OIWheSKAGSIRiXVztaC3hBde0ZM/Ae/Ug==",
        "c_use_binding": False,
        "s_init_use_binding": False,
        "s_use_binding": False,
        "c_channel_binding": None,
        "s_channel_binding": None,
    },
]


@pytest.mark.parametrize("x", params)
def test_get_client_first(x):
    channel_binding = x["c_channel_binding"]
    if channel_binding is None:
        cb = None
    else:
        cb_name, cb_data = channel_binding
        cb = ChannelBinding(CbName(cb_name), CBindData(cb_data))
    gs2_header = Gs2Header.from_binding(cb, x["c_use_binding"])
    cfirst_bare, cfirst = _get_client_first(
        Username(x["username"]), x["c_nonce"], gs2_header
    )

    assert cfirst_bare == x["cfirst_bare"]
    assert cfirst == x["cfirst"]


@pytest.mark.parametrize("x", params)
def test_make_auth_message(x):
    auth_msg = _make_auth_message(
        x["cfirst_bare"],
        x["sfirst"],
        x["cfinal_without_proof"],
    )
    assert auth_msg == x["auth_message"]


@pytest.mark.parametrize("x", params)
def test_get_client_final(x):
    channel_binding = x["c_channel_binding"]
    if channel_binding is None:
        cb = None
    else:
        cb_name, cb_data = channel_binding
        cb = ChannelBinding(CbName(cb_name), CBindData(cb_data))
    gs2_header = Gs2Header.from_binding(cb, x["c_use_binding"])
    salt = Salt.from_str(x["salt"])
    password = Password(x["password"])
    server_signature, cfinal = _get_client_final(
        x["hf"],
        password,
        salt,
        x["iterations"],
        x["nonce"],
        x["cfirst_bare"],
        x["sfirst"],
        cb,
        gs2_header,
    )

    assert server_signature == b64dec(x["server_signature"])
    assert cfinal == x["cfinal"]


@pytest.mark.parametrize("x", params)
def test_client_order(x):
    c = ScramClient(
        x["c_mechanisms"],
        x["username"],
        x["password"],
        channel_binding=x["c_channel_binding"],
    )

    with pytest.raises(ScramException):
        c.set_server_first(x["sfirst"])


@pytest.mark.parametrize("x", params)
def test_client(x):
    c = ScramClient(
        x["c_mechanisms"],
        x["username"],
        x["password"],
        channel_binding=x["c_channel_binding"],
        c_nonce=x["c_nonce"],
    )

    assert c.get_client_first() == x["cfirst"]

    c.set_server_first(x["sfirst"])

    assert c.get_client_final() == x["cfinal"]


@pytest.mark.parametrize("x", params)
def test_set_client_first(x):
    m = ScramMechanism(mechanism=x["s_mechanism"])
    salt_in = Salt.from_str(x["salt"])
    s_channel_binding = x["s_channel_binding"]
    if s_channel_binding is None:
        s_cb = None
    else:
        cb_name, cb_data = s_channel_binding
        s_cb = ChannelBinding(CbName(cb_name), CBindData(cb_data))

    def auth_fn(username):
        lookup = {
            x["username"]: m.make_auth_info(
                x["password"],
                salt=bytes(salt_in),
                iteration_count=x["iterations"],
            )
        }
        return lookup[username]

    (
        nonce,
        cfirst_bare,
        upgrade_mechanism,
        gs2_header,
        salt,
        stored_key,
        server_key,
        i,
    ) = _set_client_first(
        x["cfirst"],
        Nonce(x["s_nonce"]),
        s_cb,
        x["s_init_use_binding"],
        AuthFn(auth_fn),
    )

    assert nonce == Nonce(x["nonce"])
    assert cfirst_bare == x["cfirst_bare"]
    assert upgrade_mechanism == (x["s_init_use_binding"] != x["s_use_binding"])
    c_channel_binding = x["c_channel_binding"]
    if c_channel_binding is None:
        c_cb = None
    else:
        cb_name, cb_data = c_channel_binding
        c_cb = ChannelBinding(CbName(cb_name), CBindData(cb_data))
    expected_gs2_header = Gs2Header.from_binding(c_cb, x["c_use_binding"])
    assert type(expected_gs2_header) == type(gs2_header)
    assert gs2_header.cb_name == expected_gs2_header.cb_name
    assert gs2_header.gs2_char == expected_gs2_header.gs2_char
    assert gs2_header == expected_gs2_header
    assert salt == salt_in
    assert b64enc(stored_key) == x["stored_key"]
    assert b64enc(server_key) == x["server_key"]
    assert i == IterationCount(x["iterations"])


@pytest.mark.parametrize("x", params)
def test_get_server_first(x):
    sfirst = _get_server_first(x["nonce"], x["salt"], x["iterations"])

    assert sfirst == x["sfirst"]


@pytest.mark.parametrize("x", params)
def test_set_client_final(x):
    channel_binding = x["c_channel_binding"]
    if channel_binding is None:
        cb = None
    else:
        cb_name, cb_data = channel_binding
        cb = ChannelBinding(CbName(cb_name), CBindData(cb_data))
    gs2_header = Gs2Header.from_binding(cb, x["c_use_binding"])
    server_signature = _set_client_final(
        x["hf"],
        ClientFinal(x["cfinal"]),
        Nonce(x["nonce"]),
        b64dec(x["stored_key"]),
        b64dec(x["server_key"]),
        x["cfirst_bare"],
        x["sfirst"],
        cb,
        gs2_header,
    )

    assert server_signature == b64dec(x["server_signature"])


@pytest.mark.parametrize("x", params)
def test_get_server_final(x):
    server_final = _get_server_final(b64dec(x["server_signature"]), None)
    assert server_final == x["sfinal"]


def test_get_server_final_error():
    sig = b64dec("6rriTRBi23WpRR/wtup+mMhUZUn/dB5nLTJRsjl95G4=")
    server_final = _get_server_final(sig, ServerError.INVALID_PROOF)
    assert server_final == "e=invalid-proof"


@pytest.mark.parametrize("x", params)
def test_server_order(x):
    m = ScramMechanism(mechanism=x["s_mechanism"])

    def auth_fn(username):
        lookup = {
            x["username"]: m.make_auth_info(
                x["password"], salt=x["salt"], iteration_count=x["iterations"]
            )
        }
        return lookup[username]

    s = m.make_server(auth_fn, channel_binding=x["s_channel_binding"])

    with pytest.raises(ScramException):
        s.set_client_final(x["cfinal"])


@pytest.mark.parametrize("x", params)
def test_server(x):
    m = ScramMechanism(mechanism=x["s_mechanism"])

    def auth_fn(username):
        lookup = {
            x["username"]: m.make_auth_info(
                x["password"], salt=b64dec(x["salt"]), iteration_count=x["iterations"]
            )
        }
        return lookup[username]

    s = m.make_server(
        auth_fn, channel_binding=x["s_channel_binding"], s_nonce=x["s_nonce"]
    )

    s.set_client_first(x["cfirst"])

    assert s.get_server_first() == x["sfirst"]

    s.set_client_final(x["cfinal"])

    assert s.get_server_final() == x["sfinal"]


def test_check_stage():
    with pytest.raises(
        ScramException,
        match="The next method to be called is get_server_first, not this method.",
    ):
        _check_stage(
            ServerStage,
            ServerStage.set_client_first,
            ServerStage.get_server_final,
        )


@pytest.mark.parametrize(
    "client_first,s_nonce,channel_binding,use_binding,error_msg,server_error",
    [
        # Client requires channel binding but the server doesn't
        [
            "p=tls-unique,,n=user,r=rOprNGfwEbeRWgbNEkqO",
            Nonce("%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0"),
            None,
            False,
            (
                "Received GS2 flag 'p' which indicates that the client "
                "requires channel binding, but the server does not: "
                "channel-binding-not-supported"
            ),
            ServerError.CHANNEL_BINDING_NOT_SUPPORTED,
        ],
        # Client first is invalid
        [
            "junk",
            Nonce("%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0"),
            None,
            False,
            "The client sent a malformed first message: other-error",
            ServerError.OTHER_ERROR,
        ],
        # Client first bare message malformed
        [
            "n,,junk",
            Nonce("%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0"),
            None,
            False,
            (
                "Malformed client_first_bare message. Attributes must be separated by "
                "a ',' and each attribute must start with a letter followed by a '=': "
                "other-error"
            ),
            ServerError.OTHER_ERROR,
        ],
        # authzid must be empty
        [
            "n,anid,n=user,r=rOprNGfwEbeRWgbNEkqO",
            Nonce("%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0"),
            None,
            False,
            "The GS2 authzid must be empty: other-error",
            ServerError.OTHER_ERROR,
        ],
        # gs2-cbind-flag must be valid
        [
            "n=invalid,,n=user,r=rOprNGfwEbeRWgbNEkqO",
            Nonce("%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0"),
            None,
            False,
            "GS2 flag must be one of ('y', 'n', 'p='): other-error",
            ServerError.OTHER_ERROR,
        ],
    ],
)
def test_set_client_first_error(
    client_first, s_nonce, channel_binding, use_binding, error_msg, server_error
):

    salt, stored_key, server_key = b"a", b"b", b"c"

    def auth_fn(username):
        lookup = {"user": (salt, stored_key, server_key)}
        return lookup[username]

    with pytest.raises(ScramException) as exc_info:
        _set_client_first(client_first, s_nonce, channel_binding, use_binding, auth_fn)

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


def test_set_client_first_error_unknown_user():

    def auth_fn(_):
        return None

    with pytest.raises(ScramException) as exc_info:
        _set_client_first(
            "n,,n=user,r=rOprNGfwEbeRWgbNEkqO",
            Nonce("%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0"),
            None,
            False,
            AuthFn(auth_fn),
        )

    assert str(exc_info.value) == "Unknown user: unknown-user"
    assert exc_info.value.server_error == ServerError.UNKNOWN_USER


def test_set_client_first_error_auth_fn():

    def auth_fn(_):
        raise Exception()  # noqa: TRY002

    with pytest.raises(ScramException) as exc_info:
        _set_client_first(
            "n,,n=user,r=rOprNGfwEbeRWgbNEkqO",
            Nonce("%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0"),
            None,
            False,
            AuthFn(auth_fn),
        )

    assert str(exc_info.value) == "auth_fn exception: no-resources"
    assert exc_info.value.server_error == ServerError.NO_RESOURCES


@pytest.mark.parametrize(
    "hf,client_final,nonce,stored_key,server_key,client_first_bare,server_first,"
    "channel_binding,use_binding,error_msg,server_error",
    [
        # Invalid client final
        [
            hashlib.sha256,
            ClientFinal(
                "c=biws,r=invalid,p=dHzbZapWIk4jUhN+Ute9ytag9zjfMHgsqmmiz7AndVQ="
            ),
            "%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
            b64dec("WG5d8oPm3OtcPnkdi4Uo7BkeZkBFzpcXkuLmtbsT4qY="),
            b64dec("wfPLwcE6nTWhTAmQ7tl2KeoiWGPlZqQxSrmfPwDl2dU="),
            "n=user,r=rOprNGfwEbeRWgbNEkqO",
            (
                "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
                "s=W22ZaJ0SNY7soEsUEjb6gQ==,i=4096"
            ),
            None,
            Gs2Header("n", None),
            "Server nonce doesn't match.: other-error",
            ServerError.OTHER_ERROR,
        ],
        # Channel has invalid base 64 encoding, so b64dec() should fail
        [
            hashlib.sha256,
            ClientFinal(
                "c=!!!,r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
                "p=dHzbZapWIk4jUhN+Ute9ytag9zjfMHgsqmmiz7AndVQ="
            ),
            "%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
            b64dec("WG5d8oPm3OtcPnkdi4Uo7BkeZkBFzpcXkuLmtbsT4qY="),
            b64dec("wfPLwcE6nTWhTAmQ7tl2KeoiWGPlZqQxSrmfPwDl2dU="),
            "n=user,r=rOprNGfwEbeRWgbNEkqO",
            (
                "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
                "s=W22ZaJ0SNY7soEsUEjb6gQ==,i=4096"
            ),
            None,
            Gs2Header("n", None),
            (
                "The channel binding isn't correctly encoded: Invalid base 64 "
                "encoding: invalid-encoding: invalid-encoding"
            ),
            ServerError.INVALID_ENCODING,
        ],
        # Even if channel binding isn't used, check it's valid
        [
            hashlib.sha256,
            ClientFinal(
                "c=rOprNGfwEbeRWgbNEkqO,"
                "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
                "p=dHzbZapWIk4jUhN+Ute9ytag9zjfMHgsqmmiz7AndVQ="
            ),
            "rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
            b64dec("WG5d8oPm3OtcPnkdi4Uo7BkeZkBFzpcXkuLmtbsT4qY="),
            b64dec("wfPLwcE6nTWhTAmQ7tl2KeoiWGPlZqQxSrmfPwDl2dU="),
            "n=user,r=rOprNGfwEbeRWgbNEkqO",
            (
                "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
                "s=W22ZaJ0SNY7soEsUEjb6gQ==,i=4096"
            ),
            None,
            Gs2Header("n", None),
            "The channel bindings don't match.: channel-bindings-dont-match",
            ServerError.CHANNEL_BINDINGS_DONT_MATCH,
        ],
    ],
)
def test_set_client_final_error(
    hf,
    client_final,
    nonce,
    stored_key,
    server_key,
    client_first_bare,
    server_first,
    channel_binding,
    use_binding,
    error_msg,
    server_error,
):
    with pytest.raises(ScramException) as exc_info:
        _set_client_final(
            hf,
            client_final,
            nonce,
            stored_key,
            server_key,
            client_first_bare,
            server_first,
            channel_binding,
            use_binding,
        )

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


@pytest.mark.parametrize(
    "server_first,c_nonce",
    [
        [
            ServerFirst(
                "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
                "s=W22ZaJ0SNY7soEsUEjb6gQ==,i=4096"
            ),
            Nonce("rOprNGfwEbeRWgbNEkqO"),
        ],
    ],
)
def test_set_server_first(server_first, c_nonce):
    _set_server_first(server_first, c_nonce)


@pytest.mark.parametrize(
    "server_first,c_nonce,error_msg",
    [
        # Error from server
        [
            ServerFirst("e=other-error"),
            Nonce("fyko+d2lbbFgONRv9qkxdawL"),
            "The server returned an error: other-error",
        ],
        # The nonce must be longer than the c_nonce
        [
            ServerFirst("r=fyko+d2lbbFgONRv9qkxdawL,s=W22ZaJ0SNY7soEsUEjb6gQ==,i=5000"),
            Nonce("fyko+d2lbbFgONRv9qkxdawL"),
            "The nonce must be longer than the client nonce: other-error",
        ],
        [
            ServerFirst("e=other-error,x=a"),
            Nonce("fyko+d2lbbFgONRv9qkxdawL"),
            "The server returned an error: other-error",
        ],
    ],
)
def test_set_server_first_error(server_first, c_nonce, error_msg):
    with pytest.raises(ScramException) as exc_info:
        _set_server_first(server_first, c_nonce)

    assert str(exc_info.value) == error_msg


@pytest.mark.parametrize(
    "msg,server_signature",
    [
        [
            ServerFinal("v=6rriTRBi23WpRR/wtup+mMhUZUn/dB5nLTJRsjl95G4="),
            b64dec("6rriTRBi23WpRR/wtup+mMhUZUn/dB5nLTJRsjl95G4="),
        ]
    ],
)
def test_set_server_final(msg, server_signature):
    _set_server_final(msg, server_signature)


def test_ScramClient_init_error_no_cert(mocker):
    mechanisms = ["SCRAM-SHA-256-PLUS"]
    username = "max"
    password = "pencil"
    sock = mocker.MagicMock(spec=SSLSocket)
    sock.getpeercert.return_value = None
    channel_binding = "tls-server-end-point", sock
    c_nonce = Nonce("rOprNGfwEbeRWgbNEkqO")
    with pytest.raises(ScramException) as exc_info:
        ScramClient(
            mechanisms,
            username,
            password,
            channel_binding=channel_binding,
            c_nonce=c_nonce,
        )
    expected_error_msg = "There is no peer certificate for the SSL socket: other-error"
    assert str(exc_info.value) == expected_error_msg


@pytest.mark.parametrize(
    "mechanisms,username,password,channel_binding,c_nonce",
    [
        [
            ["SCRAM-SHA-256-PLUS"],
            "max",
            "pencil",
            ("tls-unique", b"xxx"),
            "rOprNGfwEbeRWgbNEkqO",
        ],
    ],
)
def test_ScramClient_init(
    mocker, mechanisms, username, password, channel_binding, c_nonce
):
    ScramClient(
        mechanisms,
        username,
        password,
        channel_binding=channel_binding,
        c_nonce=c_nonce,
    )


@pytest.mark.parametrize(
    "ssl_socket_class",
    [
        SSLSocket,
        SSLObject,
    ],
)
def test_ScramClient_init_tls_server_end_point(mocker, ssl_socket_class):
    mechanisms = ["SCRAM-SHA-512-PLUS"]
    username = "max"
    password = "pencil"

    ssl_socket = mocker.create_autospec(ssl_socket_class, instance=True)
    ssl_socket.getpeercert = mocker.Mock(return_value=b"cafe")
    mock_cert = mocker.Mock()
    mock_cert.hash_algo = "sha512"
    mocker.patch("scramp.core.Certificate.load", return_value=mock_cert)
    channel_binding = "tls-server-end-point", ssl_socket
    c_nonce = None

    client = ScramClient(
        mechanisms, username, password, channel_binding=channel_binding, c_nonce=c_nonce
    )
    assert client.cb == ChannelBinding(
        CbName("tls-server-end-point"),
        CBindData(
            b"5\x9dQ\xe2\xc4a\x17g\x1bK\xeci\x98\x9e\x16R\x96}\xe4~D\x15\xfb\xb3\x1fn]="
            b"\re?s\x10\xf2\xf8\xa6+\x91i\x9d\x84,iO\x8emDu\xb4\x19\x06i\xa7\x1a\xf1i\xc6"
            b"K\x81\xcbp\xd1\xaf\xd7"
        ),
    )


@pytest.mark.parametrize(
    "ssl_socket_class",
    [
        SSLSocket,
        SSLObject,
    ],
)
def test_ScramClient_init_tls_unique_ssl_socket(mocker, ssl_socket_class):
    mechanisms = ["SCRAM-SHA-512-PLUS"]
    username = "max"
    password = "pencil"
    cb_name = "tls-unique"
    cb_data = b"x"
    ssl_socket = mocker.create_autospec(ssl_socket_class, instance=True)
    ssl_socket.get_channel_binding.return_value = cb_data

    channel_binding = "tls-unique", ssl_socket
    client = ScramClient(
        mechanisms,
        username=username,
        password=password,
        channel_binding=channel_binding,
    )

    ssl_socket.get_channel_binding.assert_called_once_with(cb_name)
    assert client.cb == ChannelBinding(CbName(cb_name), CBindData(cb_data))


@pytest.mark.parametrize(
    "mechanisms,username,password,channel_binding,msg",
    [
        [
            ["SCRAM-SHA-512-PLUS"],
            "max",
            "pencil",
            ("c", "d"),
            (
                "The channel binding type is not recognised by Scramp. The recognised "
                "types are ['tls-exporter', 'tls-server-end-point', 'tls-unique', "
                "'tls-unique-for-telnet']: unsupported-channel-binding-type"
            ),
        ],
    ],
)
def test_ScramClient_init_error(mechanisms, username, password, channel_binding, msg):
    with pytest.raises(ScramException) as exc_info:
        ScramClient(mechanisms, username, password, channel_binding=channel_binding)

    assert str(exc_info.value) == msg


def test_ScramClient_set_server_final_missing_param():
    x = EXCHANGE_SCRAM_SHA_256
    c = ScramClient(
        x["c_mechanisms"],
        x["username"],
        x["password"],
        c_nonce=x["c_nonce"],
    )
    c.get_client_first()
    c.set_server_first(x["sfirst"])
    c.get_client_final()
    with pytest.raises(
        ScramException,
        match="Malformed server final message. Attributes must be separated by a ',' "
        "and each attribute must start with a letter followed by a '=': other-error",
    ):
        c.set_server_final("junk")
