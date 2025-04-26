import six
import pytest
import varint

from multiaddr import exceptions, protocols


def test_code_to_varint():
    vi = varint.encode(5)
    assert vi == b'\x05'
    vi = varint.encode(150)
    assert vi == b'\x96\x01'


def test_varint_to_code():
    cc = varint.decode_bytes(b'\x05')
    assert cc == 5
    cc = varint.decode_bytes(b'\x96\x01')
    assert cc == 150


@pytest.fixture
def valid_params():
    return {'code': protocols.P_IP4,
            'name': 'ipb4',
            'codec': 'ipb'}


def test_valid(valid_params):
    proto = protocols.Protocol(**valid_params)
    for key in valid_params:
        assert getattr(proto, key) == valid_params[key]


@pytest.mark.parametrize("invalid_code", ['abc'])
def test_invalid_code(valid_params, invalid_code):
    valid_params['code'] = invalid_code
    with pytest.raises(TypeError):
        protocols.Protocol(**valid_params)


@pytest.mark.parametrize("invalid_name", [123, 1.0])
def test_invalid_name(valid_params, invalid_name):
    valid_params['name'] = invalid_name
    with pytest.raises(TypeError):
        protocols.Protocol(**valid_params)


@pytest.mark.skipif(six.PY2, reason="Binary strings are allowed on Python 2")
@pytest.mark.parametrize("invalid_codec", [b"ip4", 123, 0.123])
def test_invalid_codec(valid_params, invalid_codec):
    valid_params['codec'] = invalid_codec
    with pytest.raises(TypeError):
        protocols.Protocol(**valid_params)


@pytest.mark.parametrize("name", ["foo-str", u"foo-u"])
def test_valid_names(valid_params, name):
    valid_params['name'] = name
    test_valid(valid_params)


@pytest.mark.parametrize("codec", ["ip4", u"ip6"])
def test_valid_codecs(valid_params, codec):
    valid_params['codec'] = codec
    test_valid(valid_params)


def test_protocol_with_name():
    proto = protocols.protocol_with_name('ip4')
    assert proto.name == 'ip4'
    assert proto.code == protocols.P_IP4
    assert proto.size == 32
    assert proto.vcode == varint.encode(protocols.P_IP4)
    assert hash(proto) == protocols.P_IP4

    with pytest.raises(exceptions.ProtocolNotFoundError):
        proto = protocols.protocol_with_name('foo')


def test_protocol_with_code():
    proto = protocols.protocol_with_code(protocols.P_IP4)
    assert proto.name == 'ip4'
    assert proto.code == protocols.P_IP4
    assert proto.size == 32
    assert proto.vcode == varint.encode(protocols.P_IP4)
    assert hash(proto) == protocols.P_IP4

    with pytest.raises(exceptions.ProtocolNotFoundError):
        proto = protocols.protocol_with_code(1234)


def test_protocol_equality():
    proto1 = protocols.protocol_with_name('ip4')
    proto2 = protocols.protocol_with_code(protocols.P_IP4)
    proto3 = protocols.protocol_with_name('onion')
    proto4 = protocols.protocol_with_name('onion3')

    assert proto1 == proto2
    assert proto1 != proto3
    assert proto3 != proto4
    assert proto1 is not None
    assert proto2 != str(proto2)


@pytest.mark.parametrize("names", [['ip4'],
                                   ['ip4', 'tcp'],
                                   ['ip4', 'tcp', 'udp']])
def test_protocols_with_string(names):
    expected = [protocols.protocol_with_name(name) for name in names]
    ins = "/".join(names)
    assert protocols.protocols_with_string(ins) == expected
    assert protocols.protocols_with_string("/" + ins) == expected
    assert protocols.protocols_with_string("/" + ins + "/") == expected


@pytest.mark.parametrize("invalid_name", ["", "/", "//"])
def test_protocols_with_string_invalid(invalid_name):
    assert protocols.protocols_with_string(invalid_name) == []


def test_protocols_with_string_mixed():
    names = ['ip4']
    ins = "/".join(names)
    test_protocols_with_string(names)
    with pytest.raises(exceptions.ProtocolNotFoundError):
        names.append("foo")
        ins = "/".join(names)
        protocols.protocols_with_string(ins)


# add_protocol is stateful, so we need to mock out
# multiaddr.protocols.PROTOCOLS
@pytest.fixture()
def patch_protocols(monkeypatch):
    monkeypatch.setattr(protocols, 'PROTOCOLS', [])
    monkeypatch.setattr(protocols, '_names_to_protocols', {})
    monkeypatch.setattr(protocols, '_codes_to_protocols', {})


def test_add_protocol(patch_protocols, valid_params):
    proto = protocols.Protocol(**valid_params)
    protocols.add_protocol(proto)
    assert protocols.PROTOCOLS == [proto]
    assert proto.name in protocols._names_to_protocols
    assert proto.code in protocols._codes_to_protocols
    proto = protocols.Protocol(protocols.P_TCP, "tcp", "uint16be")


def test_add_protocol_twice(patch_protocols, valid_params):
    proto = protocols.Protocol(**valid_params)
    protocols.add_protocol(proto)
    with pytest.raises(exceptions.ProtocolExistsError):
        protocols.add_protocol(proto)
    del protocols._names_to_protocols[proto.name]
    with pytest.raises(exceptions.ProtocolExistsError):
        protocols.add_protocol(proto)
    del protocols._codes_to_protocols[proto.code]
    protocols.add_protocol(proto)
    assert protocols.PROTOCOLS == [proto, proto]


def test_protocol_repr():
    proto = protocols.protocol_with_name('ip4')
    assert "Protocol(code=4, name='ip4', codec='ip4')" == repr(proto)
