import hashlib

import pytest

from scramp import (
    ScramClient,
    ScramException,
    ScramMechanism,
    core,
    make_channel_binding,
)
from scramp.core import (
    SERVER_ERROR_INVALID_PROOF,
    _check_client_key,
    _parse_message,
    _set_client_final,
    _set_client_first,
    _set_server_first,
    _validate_channel_binding,
)
from scramp.utils import b64dec


@pytest.mark.parametrize(
    "msg,att_sets,error_msg",
    [
        [
            "",
            [{"a", "b", "c"}],
            "Malformed trial message. Attributes must be separated by a ',' and each "
            "attribute must start with a letter followed by a '=': other-error",
        ],
        [
            "c=jk,d=kln",
            [{"a", "b", "c"}],
            "Malformed trial message. Expected the attribute set to be one of "
            "[{a, b, c}] but found {c, d}: extensions-not-supported",
        ],
        [
            "c=jk,c=kln",
            [{"c"}],
            "Duplicate attributes not allowed in message. The duplicated attribute "
            "is c. : other-error",
        ],
        [
            "e=error",
            [{"c"}],
            "Malformed trial message. Expected the attribute set to be one of [{c}] "
            "but found {e}: extensions-not-supported",
        ],
    ],
)
def test_parse_message_fail(msg, att_sets, error_msg):
    with pytest.raises(ScramException) as exc_info:
        _parse_message(msg, "trial", *att_sets)

    assert str(exc_info.value) == error_msg


@pytest.mark.parametrize(
    "msg,att_sets,result",
    [
        ["c=jk,d=kln", [{"c", "d"}], {"c": "jk", "d": "kln"}],
        ["c=jk,d=kln", [{"a", "b", "c"}, {"c", "d"}], {"c": "jk", "d": "kln"}],
        ["c=", [{"c"}], {"c": ""}],
    ],
)
def test_parse_message_succeed(msg, att_sets, result):
    assert _parse_message(msg, "trial", *att_sets) == result


@pytest.mark.parametrize(
    "cb,msg",
    [
        [
            ("c", "d"),
            "The channel_binding parameter must either be None or a "
            "tuple with the first element a str specifying one of the channel types "
            "('tls-server-end-point', 'tls-unique', 'tls-unique-for-telnet').",
        ],
    ],
)
def test_validate_channel_binding_fail(cb, msg):
    with pytest.raises(ScramException) as exc_info:
        _validate_channel_binding(cb)

    assert str(exc_info.value) == msg


@pytest.mark.parametrize(
    "password,iteration_count,salt,msg",
    [
        [
            "pencil",
            1,
            b"",
            "The iteration count is not valid: The value must not be < 10000",
        ],
    ],
)
def test_make_auth_info_fail(password, iteration_count, salt, msg):
    m = ScramMechanism(mechanism="SCRAM-SHA3-512")
    with pytest.raises(ScramException) as exc_info:
        m.make_auth_info(password, iteration_count, salt)

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
            "KOkd92LduC09A+RDxbTvgxH9Nn6efom/uAy6U5/fqpwLH1J+wQnZcKx5W1zd"
            "YMPU8PrusBUK5RgRk4yHx+3Mg==",
            "Can't create client key.: invalid-proof",
        ],
    ],
)
def test_check_client_key_fail(hf, stored_key, auth_msg, proof, msg):
    with pytest.raises(ScramException) as exc_info:
        _check_client_key(hf, stored_key, auth_msg, proof)

    assert str(exc_info.value) == msg
    assert str(exc_info.value.server_error) == SERVER_ERROR_INVALID_PROOF


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
    cfirst_bare, cfirst = core._get_client_first(
        x["username"], x["c_nonce"], x["c_channel_binding"], x["c_use_binding"]
    )

    assert cfirst_bare == x["cfirst_bare"]
    assert cfirst == x["cfirst"]


@pytest.mark.parametrize("x", params)
def test_make_auth_message(x):
    auth_msg = core._make_auth_message(
        x["cfirst_bare"],
        x["sfirst"],
        x["cfinal_without_proof"],
    )
    assert auth_msg == x["auth_message"]


@pytest.mark.parametrize("x", params)
def test_get_client_final(x):
    server_signature, cfinal = core._get_client_final(
        x["hf"],
        x["password"],
        x["salt"],
        x["iterations"],
        x["nonce"],
        x["cfirst_bare"],
        x["sfirst"],
        x["c_channel_binding"],
        x["c_use_binding"],
    )

    assert server_signature == x["server_signature"]
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
    nonce, user, cfirst_bare, upgrade_mechanism = core._set_client_first(
        x["cfirst"], x["s_nonce"], x["s_channel_binding"], x["s_init_use_binding"]
    )

    assert nonce == x["nonce"]
    assert user == x["username"]
    assert cfirst_bare == x["cfirst_bare"]
    assert upgrade_mechanism == (x["s_init_use_binding"] != x["s_use_binding"])


@pytest.mark.parametrize("x", params)
def test_get_server_first(x):
    sfirst = core._get_server_first(x["nonce"], x["salt"], x["iterations"])

    assert sfirst == x["sfirst"]


@pytest.mark.parametrize("x", params)
def test_set_client_final(x):
    server_signature = core._set_client_final(
        x["hf"],
        x["cfinal"],
        x["nonce"],
        b64dec(x["stored_key"]),
        b64dec(x["server_key"]),
        x["cfirst_bare"],
        x["sfirst"],
        x["s_channel_binding"],
        x["s_use_binding"],
    )

    assert server_signature == x["server_signature"]


@pytest.mark.parametrize("x", params)
def test_get_server_final(x):
    server_final = core._get_server_final(x["server_signature"], None)
    assert server_final == x["sfinal"]


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
        core._check_stage(
            core.ServerStage,
            core.ServerStage.set_client_first,
            core.ServerStage.get_server_final,
        )


@pytest.mark.parametrize(
    "client_first,s_nonce,channel_binding,use_binding,error_msg,server_error",
    [
        # Client requires channel binding but the server doesn't
        [
            "p=tls-unique,,n=user,r=rOprNGfwEbeRWgbNEkqO",
            "%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
            None,
            False,
            "Received GS2 flag 'p' which indicates that the client "
            "requires channel binding, but the server does not: "
            "channel-binding-not-supported",
            "channel-binding-not-supported",
        ],
        # Client first is invalid
        [
            "junk",
            "%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
            None,
            False,
            "The client sent a malformed first message: other-error",
            "other-error",
        ],
        # Client first bare message malformed
        [
            "n,,junk",
            "%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
            None,
            False,
            "Malformed client first bare message. Attributes must be separated by a "
            "',' and each attribute must start with a letter followed by a '=': "
            "other-error",
            "other-error",
        ],
        # authzid must be empty
        [
            "n,anid,n=user,r=rOprNGfwEbeRWgbNEkqO",
            "%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
            None,
            False,
            "The GS2 authzid anid must be empty: other-error",
            "other-error",
        ],
    ],
)
def test_set_client_first_error(
    client_first, s_nonce, channel_binding, use_binding, error_msg, server_error
):
    with pytest.raises(ScramException) as exc_info:
        _set_client_first(client_first, s_nonce, channel_binding, use_binding)

    assert str(exc_info.value) == error_msg
    assert str(exc_info.value.server_error) == server_error


@pytest.mark.parametrize(
    "hf,client_final,s_nonce,stored_key,server_key,client_first_bare,server_first,"
    "channel_binding,use_binding,error_msg,server_error",
    # Malformed client final message
    [
        [
            hashlib.sha256,
            "junk",
            "%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
            b64dec("WG5d8oPm3OtcPnkdi4Uo7BkeZkBFzpcXkuLmtbsT4qY="),
            b64dec("wfPLwcE6nTWhTAmQ7tl2KeoiWGPlZqQxSrmfPwDl2dU="),
            "n=user,r=rOprNGfwEbeRWgbNEkqO",
            "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
            "s=W22ZaJ0SNY7soEsUEjb6gQ==,i=4096",
            None,
            True,
            "Malformed client final message. Attributes must be separated by a ',' "
            "and each attribute must start with a letter followed by a '=': "
            "other-error",
            "other-error",
        ],
        # Invalid client final
        [
            hashlib.sha256,
            "c=biws,r=invalid,p=dHzbZapWIk4jUhN+Ute9ytag9zjfMHgsqmmiz7AndVQ=",
            "%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
            b64dec("WG5d8oPm3OtcPnkdi4Uo7BkeZkBFzpcXkuLmtbsT4qY="),
            b64dec("wfPLwcE6nTWhTAmQ7tl2KeoiWGPlZqQxSrmfPwDl2dU="),
            "n=user,r=rOprNGfwEbeRWgbNEkqO",
            "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
            "s=W22ZaJ0SNY7soEsUEjb6gQ==,i=4096",
            None,
            False,
            "Server nonce doesn't match.: other-error",
            "other-error",
        ],
        # Channel has invalid base 64 encoding, so b64dec() should fail
        [
            hashlib.sha256,
            "c=!!!,r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
            "p=dHzbZapWIk4jUhN+Ute9ytag9zjfMHgsqmmiz7AndVQ=",
            "%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0",
            b64dec("WG5d8oPm3OtcPnkdi4Uo7BkeZkBFzpcXkuLmtbsT4qY="),
            b64dec("wfPLwcE6nTWhTAmQ7tl2KeoiWGPlZqQxSrmfPwDl2dU="),
            "n=user,r=rOprNGfwEbeRWgbNEkqO",
            "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
            "s=W22ZaJ0SNY7soEsUEjb6gQ==,i=4096",
            None,
            True,
            "The channel binding isn't correctly b64 encoded: invalid-encoding",
            "invalid-encoding",
        ],
    ],
)
def test_set_client_final_error(
    hf,
    client_final,
    s_nonce,
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
            s_nonce,
            stored_key,
            server_key,
            client_first_bare,
            server_first,
            channel_binding,
            use_binding,
        )

    assert str(exc_info.value) == error_msg
    assert str(exc_info.value.server_error) == server_error


@pytest.mark.parametrize(
    "server_first,c_nonce,min_iteration_count,error_msg",
    [
        # Error from server
        [
            "e=other-error",
            "fyko+d2lbbFgONRv9qkxdawL",
            1000,
            "The server returned the error: other-error",
        ],
        # Malformed server first
        [
            "junk",
            "fyko+d2lbbFgONRv9qkxdawL",
            1000,
            "Malformed server first message. Attributes must be separated by a ',' "
            "and each attribute must start with a letter followed by a '=': "
            "other-error",
        ],
        # Malformed iteration count in server first
        [
            "r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,"
            "s=W22ZaJ0SNY7soEsUEjb6gQ==,i=not_an_integer",
            "fyko+d2lbbFgONRv9qkxdawL",
            1000,
            "Server iteration count not_an_integer is not valid",
        ],
    ],
)
def test_set_server_first_error(server_first, c_nonce, min_iteration_count, error_msg):
    with pytest.raises(ScramException) as exc_info:
        _set_server_first(server_first, c_nonce, min_iteration_count)
    assert str(exc_info.value) == error_msg


def test_set_server_final_missing_param():
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


def test_make_channel_binding_tls_server_end_point(mocker):
    ssl_socket = mocker.Mock()
    ssl_socket.getpeercert = mocker.Mock(return_value=b"cafe")
    mock_cert = mocker.Mock()
    mock_cert.hash_algo = "sha512"
    mocker.patch("scramp.core.Certificate.load", return_value=mock_cert)
    result = make_channel_binding("tls-server-end-point", ssl_socket)
    assert result == (
        "tls-server-end-point",
        b"5\x9dQ\xe2\xc4a\x17g\x1bK\xeci\x98\x9e\x16R\x96}\xe4~D\x15\xfb\xb3\x1fn]="
        b"\re?s\x10\xf2\xf8\xa6+\x91i\x9d\x84,iO\x8emDu\xb4\x19\x06i\xa7\x1a\xf1i\xc6"
        b"K\x81\xcbp\xd1\xaf\xd7",
    )
