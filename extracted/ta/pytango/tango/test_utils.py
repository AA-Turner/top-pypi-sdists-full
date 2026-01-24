# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Test utilities"""

import enum
import time
from functools import wraps

import numpy as np

try:
    import numpy.typing as npt

    # in numpy 1.20 npt does not have npt.NDArray, so we cannot parce hits
    npt.NDArray
except (AttributeError, ImportError):
    npt = None

# Local imports
from tango import (
    DeviceProxy,
    DevState,
    GreenMode,
    AttrDataFormat,
    ExtractAs,
    DevFailed,
    DevVarLongStringArray,
    DevVarDoubleStringArray,
    SerialModel,
)
from tango.server import Device
from tango.test_context import (
    MultiDeviceTestContext,
    DeviceTestContext,
    get_server_port_via_pid,
)
from tango.utils import is_non_str_seq, FROM_TANGO_TO_NUMPY_TYPE
from tango import DeviceClass, LatestDeviceImpl, DevLong64, SCALAR, READ

# Conditional imports
try:
    import pytest
except ImportError:
    pytest = None

__all__ = [
    "MultiDeviceTestContext",
    "DeviceTestContext",
    "SimpleDevice",
    "ClassicAPISimpleDeviceImpl",
    "ClassicAPISimpleDeviceClass",
    "state",
    "command_typed_values",
    "attribute_typed_values",
    "dev_encoded_values",
    "server_green_mode",
    "attr_data_format",
    "convert_dtype_to_typing_hint",
    "assert_close",
    "general_decorator",
    "general_asyncio_decorator",
    "DEVICE_SERVER_ARGUMENTS",
    "wait_for_proxy",
    "wait_for_nodb_proxy_via_pid",
]

if npt:
    __all__ += [
        "command_numpy_typed_values",
        "attribute_numpy_typed_values",
        "attribute_wrong_numpy_typed",
    ]

UTF8_STRING = (
    r"""ăѣ𝔠ծềſģȟᎥ𝒋ǩľḿꞑȯ𝘱𝑞𝗋𝘴ȶ𝞄𝜈ψ𝒙𝘆𝚣1234567890!@#$%^&*()-_=+[{]};:'",<.>/?~𝘈Ḇ𝖢𝕯٤ḞԍНǏ𝙅ƘԸⲘ𝙉০Ρ𝗤Ɍ𝓢ȚЦ𝒱Ѡ𝓧ƳȤ"""
    r"""ả𝘢ѧᖯć𝗱ễ𝑓𝙜Ⴙ𝞲𝑗𝒌ļṃŉо𝞎𝒒ᵲꜱ𝙩ừ𝗏ŵ𝒙𝒚ź1234567890!@#$%^&*()-_=+[{]};:'",<.>/?~АḂⲤ𝗗𝖤𝗙ꞠꓧȊ𝐉𝜥ꓡ𝑀𝑵Ǭ𝙿𝑄Ŗ𝑆𝒯𝖴𝘝𝘞ꓫŸ𝜡"""
    r"""𝜶ƀ𝖼ḋếᵮℊ𝙝Ꭵ𝕛кιṃդⱺ𝓅𝘲𝕣𝖘ŧ𝑢ṽẉ𝘅ყž1234567890!@#$%^&*()-_=+[{]};:'",<.>/?~Ѧ𝙱ƇᗞΣℱԍҤ١𝔍К𝓛𝓜ƝȎ𝚸𝑄Ṛ𝓢ṮṺƲᏔꓫ𝚈𝚭"""
    r"""Ꮟçძ𝑒𝖿𝗀ḧ𝗂𝐣ҝɭḿ𝕟𝐨𝝔𝕢ṛ𝓼тú𝔳ẃ⤬𝝲𝗓1234567890!@#$%^&*()-_=+[{]};:'",<.>/?~𝖠Β𝒞𝘋𝙴𝓕ĢȞỈ𝕵ꓗʟ𝙼ℕ০𝚸𝗤ՀꓢṰǓⅤ𝔚Ⲭ𝑌𝙕𝘢𝕤"""
)

# char \x00 cannot be sent in a DevString. All other 1-255 chars can
ints = tuple(range(1, 256))
bytes_devstring = bytes(ints)
str_devstring = bytes_devstring.decode("latin-1")

# Test devices


class SimpleDevice(Device):
    def init_device(self):
        self.set_state(DevState.ON)


class ClassicAPISimpleDeviceImpl(LatestDeviceImpl):
    def __init__(self, cls, name):
        LatestDeviceImpl.__init__(self, cls, name)
        ClassicAPISimpleDeviceImpl.init_device(self)

    def init_device(self):
        self.get_device_properties(self.get_device_class())
        self.attr_attr1_read = 100

    def read_attr1(self, attr):
        attr.set_value(self.attr_attr1_read)


class ClassicAPISimpleDeviceClass(DeviceClass):
    attr_list = {"attr1": [[DevLong64, SCALAR, READ]]}


# Test enums


class GoodEnum(enum.IntEnum):
    START = 0
    MIDDLE = 1
    END = 2


class BadEnumNonZero(enum.IntEnum):
    START = 1
    MIDDLE = 2
    END = 3


class BadEnumSkipValues(enum.IntEnum):
    START = 0
    MIDDLE = 2
    END = 4


class BadEnumDuplicates(enum.IntEnum):
    START = 0
    MIDDLE = 1
    END = 1


# Helpers

# Note on Tango properties using the Tango File database:
# Tango file database cannot handle properties with '\n'. It doesn't
# handle '\' neither. And it cuts ASCII extended characters. That is
# why you will find that all property related tests are truncated to
# the first two values of the arrays below

GENERAL_TYPED_VALUES = {
    int: (1, 2, -65535, 23),
    float: (2.71, 3.14, -34.678e-10, 12.678e15),
    str: ("hey hey", "my my", bytes_devstring, str_devstring),
    bool: (False, True, True, False),
    (int,): (
        np.array([1, 2]),
        (1, 2, 3),
        [9, 8, 7],
        [-65535, 2224],
        [0, 0],
    ),
    (float,): (
        np.array([0.1, 0.2]),
        (0.1, 0.2, 0.3),
        [0.9, 0.8, 0.7],
        (-6.3232e-3, 1.234e4),
        [0.0, 12.56e12],
    ),
    (str,): (
        np.array(["foo", "bar"]),
        ("ab", "cd", "ef"),
        ["gh", "ij", "kl"],
        ("ab", "cd"),
        ["gh", "ij"],
        3 * [bytes_devstring],
        3 * [str_devstring],
    ),
    (bool,): (
        np.array([True, False]),
        (False, False, True),
        [True, False, False],
        (False, True),
        [True, False],
    ),
}

COMMAND_TYPED_VALUES = {
    DevVarLongStringArray: ([[1, 2, 3], ["foo", "bar", "hmm"]],),
    DevVarDoubleStringArray: ([[1.1, 2.2, 3.3], ["foo", "bar", "hmm"]],),
}

IMAGE_TYPED_VALUES = {
    ((int,),): (
        np.vstack((np.array([1, 2]), np.array([3, 4]))),
        ((1, 2, 3), (4, 5, 6), (7, 8, 9)),
        [[-65535, 2224, 23], [-6535, 224, 345], [-655, 24, 54]],
        ((1, 2, 3), (4, 5, 6)),
        [[-65535, 2224], [-65535, 2224]],
    ),
    ((float,),): (
        np.vstack((np.array([0.1, 0.2]), np.array([0.3, 0.4]))),
        ((0.1, 0.2, 0.3), (0.9, 0.8, 0.7), (0.5, 0.6, 0.7)),
        [[-6.3232e-3, 0.0], [0.0, 12.56e12], [23.4, 1.56e2]],
        ((0.1, 0.2, 0.3), (0.9, 0.8, 0.7)),
        [[-6.3232e-3, 0.0], [0.0, 12.56e12]],
    ),
    ((str,),): (
        np.vstack((np.array(["hi-hi", "ha-ha"]), np.array(["hu-hu", "yuhuu"]))),
        [["ab", "cd", "ef"], ["gh", "ij", "kl"], ["gh", "ij", "kl"]],
        (("ab", "cd", "ef"), ("gh", "ij", "kl"), ("gh", "ij", "kl")),
        [["ab", "cd"], ["ij", "kl"]],
        (("ab", "ef"), ("gh", "ij")),
        [3 * [bytes_devstring], 3 * [bytes_devstring]],
        [3 * [str_devstring], 3 * [str_devstring]],
    ),
    ((bool,),): (
        np.vstack((np.array([True, False]), np.array([False, True]))),
        [[False, False, True], [True, False, False], [True, False, False]],
        ((False, False, True), (True, False, False), (True, False, False)),
        [[False, True], [False, False]],
        ((False, True), (False, False)),
        [[False]],
        [[True]],
    ),
}

_numpy_hits_source = (
    ((np.bool_,), True, [True, False], [[True, False], [False, True]]),
    ((np.ubyte,), 1, [1, 2], [[1, 2], [3, 4]]),
    (
        (
            np.short,
            np.ushort,
            np.int32,
            np.uint32,
            np.int64,
            np.uint64,
        ),
        1,
        [1, 2],
        [[1, 2], [3, 4]],
    ),
    (
        (
            np.float64,
            np.float32,
        ),
        1.1,
        [1.1, 2.2],
        [[1.1, 2.2], [3.3, 4.4]],
    ),
)


if npt:
    NUMPY_GENERAL_TYPING_HINTS = []
    NUMPY_IMAGES_TYPING_HINTS = []
    for dtypes, scalar, spectrum, image in _numpy_hits_source:
        for dtype in dtypes:
            NUMPY_GENERAL_TYPING_HINTS.extend(
                [
                    [dtype, dtype, AttrDataFormat.SCALAR, scalar],
                    [dtype, npt.NDArray[dtype], AttrDataFormat.SPECTRUM, spectrum],
                ]
            )
            NUMPY_IMAGES_TYPING_HINTS.append(
                [dtype, npt.NDArray[dtype], AttrDataFormat.IMAGE, image]
            )

    WRONG_NUMPY_TYPING_HINTS = (  # dformat, max_x, max_y, value, error, match
        (None, None, None, None, RuntimeError, "AttrDataFormat has to be specified"),
        (
            AttrDataFormat.IMAGE,
            3,
            0,
            [[1, 2], [3, 4]],
            DevFailed,
            "Maximum y dim. wrongly defined",
        ),
        (
            AttrDataFormat.SPECTRUM,
            3,
            0,
            [[1, 2], [3, 4]],
            TypeError,
            "Expecting a integer type, but it is not",
        ),
    )

EXTRACT_AS = [
    (ExtractAs.Numpy, np.ndarray),
    (ExtractAs.Tuple, tuple),
    (ExtractAs.List, list),
    (ExtractAs.Bytes, bytes),
    (ExtractAs.ByteArray, bytearray),
    (ExtractAs.String, str),
]

BASE_TYPES = [float, int, str, bool]

# we also test a large dataset to force memory allocation from heap,
# to insure immediate segfault if we try to access data after dereferencing
LARGE_DATA_SIZE = 1 * 1024**2  # 1 Mb seems to be enough

DEV_ENCODED_DATA = {
    "str": UTF8_STRING,
    "bytes": UTF8_STRING.encode(),
    "bytearray": bytearray(UTF8_STRING.encode()),
}

# these sets to test Device Server input arguments

OS_SYSTEMS = ["linux", "win"]

#    os_system, in string, out arguments list, raised exception
DEVICE_SERVER_ARGUMENTS = (
    (
        ["linux", "win"],
        "MyDs instance --nodb --port 1234",
        ["MyDs", "instance", "-nodb", "-ORBendPoint", "giop:tcp:0.0.0.0:1234"],
    ),
    (
        ["linux", "win"],
        "MyDs -port 1234 -host myhost instance",
        ["MyDs", "instance", "-ORBendPoint", "giop:tcp:myhost:1234"],
    ),
    (
        ["linux", "win"],
        "MyDs instance --ORBendPoint giop:tcp::1234",
        ["MyDs", "instance", "-ORBendPoint", "giop:tcp::1234"],
    ),
    (
        ["linux", "win"],
        "MyDs instance -nodb -port 1000 -dlist a/b/c;d/e/f",
        [
            "MyDs",
            "instance",
            "-ORBendPoint",
            "giop:tcp:0.0.0.0:1000",
            "-nodb",
            "-dlist",
            "a/b/c;d/e/f",
        ],
    ),
    (
        ["linux", "win"],
        "MyDs instance -file a/b/c",
        ["MyDs", "instance", "-file=a/b/c"],
    ),
    ([], "MyDs instance -nodb", []),  # this test should always fail
    ([], "MyDs instance -dlist a/b/c;d/e/f", []),  # this test should always fail
    # the most complicated case: verbose
    (["linux", "win"], "MyDs instance -vvvv", ["MyDs", "instance", "-v4"]),
    (
        ["linux", "win"],
        "MyDs instance --verbose --verbose --verbose --verbose",
        ["MyDs", "instance", "-v4"],
    ),
    (["linux", "win"], "MyDs instance -v4", ["MyDs", "instance", "-v4"]),
    (["linux", "win"], "MyDs instance -v 4", ["MyDs", "instance", "-v4"]),
    # some options can be only in win, in linux should be error
    (
        ["win"],
        "MyDs instance -dbg -i -s -u",
        ["MyDs", "instance", "-dbg", "-i", "-s", "-u"],
    ),
    # variable ORB options
    (
        ["linux", "win"],
        "MyDs instance -ORBtest1 test1 --ORBtest2 test2",
        ["MyDs", "instance", "-ORBtest1", "test1", "-ORBtest2", "test2"],
    ),
    (
        ["linux", "win"],
        "MyDs ORBinstance -ORBtest myORBparam",
        ["MyDs", "ORBinstance", "-ORBtest", "myORBparam"],
    ),
    (
        ["linux", "win"],
        "MyDs instance -nodb -ORBendPoint giop:tcp:localhost:1234 -ORBendPointPublish giop:tcp:myhost.local:2345",
        [
            "MyDs",
            "instance",
            "-nodb",
            "-ORBendPoint",
            "giop:tcp:localhost:1234",
            "-ORBendPointPublish",
            "giop:tcp:myhost.local:2345",
        ],
    ),
    (
        [],
        "MyDs instance -ORBtest1 test1 --orbinvalid value",
        [],
    ),  # lowercase "orb" should fail
)


def convert_dtype_to_typing_hint(dtype):
    check_x_dim, check_y_dim = False, False
    if type(dtype) is tuple:
        dtype = dtype[0]
        check_x_dim = True
        if type(dtype) is tuple:
            dtype = dtype[0]
            check_y_dim = True
            tuple_hint = tuple[
                tuple[dtype, dtype, dtype],
                tuple[dtype, dtype, dtype],
                tuple[dtype, dtype, dtype],
                tuple[dtype, dtype, dtype],
            ]
            list_hint = list[list[dtype]]
        else:
            tuple_hint = tuple[dtype, dtype, dtype]
            list_hint = list[dtype]
    elif dtype == DevVarLongStringArray:
        tuple_hint = tuple[tuple[int], tuple[str]]
        list_hint = list[list[int], list[str]]
    elif dtype == DevVarDoubleStringArray:
        tuple_hint = tuple[tuple[float], tuple[str]]
        list_hint = list[list[float], list[str]]
    else:
        tuple_hint = dtype
        list_hint = dtype

    return tuple_hint, list_hint, check_x_dim, check_y_dim


def general_decorator(function=None):
    if function:

        @wraps(function)
        def _wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        return _wrapper
    else:
        return general_decorator


def general_asyncio_decorator(function=None):
    if function:

        @wraps(function)
        async def _wrapper(*args, **kwargs):
            return await function(*args, **kwargs)

        return _wrapper
    else:
        return general_asyncio_decorator


def repr_type(x):
    if isinstance(x, (list, tuple)):
        return f"({repr_type(x[0])},)"
    elif x == DevVarLongStringArray:
        return "DevVarLongStringArray"
    elif x == DevVarDoubleStringArray:
        return "DevVarDoubleStringArray"
    return f"{x.__name__}"


def repr_numpy_type(dtype, dformat):
    if dformat == AttrDataFormat.SCALAR:
        return f"{dtype.__name__}, SCALAR"
    elif dformat == AttrDataFormat.SPECTRUM:
        return f"np.NDarray[{dtype.__name__}], SPECTRUM"
    else:
        return f"np.n2array[{dtype.__name__}], IMAGE"


# helpers to test enums
def check_attr_type(read_attr, attr_data_format, desired_type):
    if attr_data_format == AttrDataFormat.SCALAR:
        assert isinstance(read_attr, desired_type)
    elif attr_data_format == AttrDataFormat.SPECTRUM:
        for state in read_attr:
            assert isinstance(state, desired_type)
    else:
        for state in read_attr:
            for stat in state:
                assert isinstance(stat, desired_type)


def assert_value_label(read_attr, value, label):
    assert read_attr.value == value
    assert read_attr.name == label


def check_read_attr(read_attr, attr_data_format, value, label):
    if attr_data_format == AttrDataFormat.SCALAR:
        assert_value_label(read_attr, value, label)
    elif attr_data_format == AttrDataFormat.SPECTRUM:
        for val in read_attr:
            assert_value_label(val, value, label)
    else:
        for val in read_attr:
            for v in val:
                assert_value_label(v, value, label)


def make_nd_value(value, attr_data_format):
    if attr_data_format == AttrDataFormat.SCALAR:
        return value
    elif attr_data_format == AttrDataFormat.SPECTRUM:
        return (value,)
    else:
        return ((value,),)


# Numpy helpers
if pytest:

    def __assert_all_types(a, b):
        if isinstance(a, str):
            assert a == b
            return
        elif isinstance(a, dict):
            for k, v in a.items():
                assert k in b
                assert_close(v, b[k])
            return
        elif isinstance(a, (np.bool_, bool)) or isinstance(b, (np.bool_, bool)):
            assert a == b
            return
        try:
            assert a == pytest.approx(b)
        except (ValueError, TypeError):
            np.testing.assert_allclose(a, b)

    def assert_close(a, b):
        if is_non_str_seq(a):
            assert len(a) == len(b)
            for _a, _b in zip(a, b):
                assert_close(_a, _b)
        else:
            __assert_all_types(a, b)

    def __convert_value(value):
        if isinstance(value, bytes):
            return value.decode("latin-1")
        return value

    def create_result(dtype, value):
        if isinstance(dtype, (list, tuple)):
            dtype = dtype[0]
            return [create_result(dtype, v) for v in value]
        elif dtype == DevVarLongStringArray:
            return [create_result(dtype, v) for v, dtype in zip(value, [int, str])]
        elif dtype == DevVarDoubleStringArray:
            return [create_result(dtype, v) for v, dtype in zip(value, [float, str])]

        return __convert_value(value)

    def convert_to_type(value, attr_type, expected_type):
        if expected_type in [tuple, list]:
            return expected_type(value)
        elif expected_type == np.ndarray:
            return np.array(value, dtype=FROM_TANGO_TO_NUMPY_TYPE[attr_type])
        elif expected_type in [bytes, bytearray, str]:
            value = np.array(value, dtype=FROM_TANGO_TO_NUMPY_TYPE[attr_type]).tobytes()
            if expected_type is bytearray:
                return bytearray(value)
            elif expected_type is str:
                return "".join([chr(b) for b in value])
            return value
        else:
            pytest.xfail("Unknown extract_as type")

    @pytest.fixture(params=list(DevState.values.values()), ids=str)
    def state(request):
        return request.param

    @pytest.fixture(
        params=list(GENERAL_TYPED_VALUES.items()), ids=lambda x: repr_type(x[0])
    )
    def general_typed_values(request):
        dtype, values = request.param
        expected = lambda v: create_result(dtype, v)
        return dtype, values, expected

    @pytest.fixture(
        params=list({**GENERAL_TYPED_VALUES, **COMMAND_TYPED_VALUES}.items()),
        ids=lambda x: repr_type(x[0]),
    )
    def command_typed_values(request):
        dtype, values = request.param
        expected = lambda v: create_result(dtype, v)
        return dtype, values, expected

    @pytest.fixture(
        params=list({**GENERAL_TYPED_VALUES, **IMAGE_TYPED_VALUES}.items()),
        ids=lambda x: repr_type(x[0]),
    )
    def attribute_typed_values(request):
        dtype, values = request.param
        expected = lambda v: create_result(dtype, v)
        return dtype, values, expected

    if npt:

        @pytest.fixture(
            params=NUMPY_GENERAL_TYPING_HINTS, ids=lambda x: repr_numpy_type(x[0], x[2])
        )
        def command_numpy_typed_values(request):
            dtype, type_hint, dformat, values = request.param
            expected = lambda v: create_result(dtype, v)
            return type_hint, dformat, values, expected

        @pytest.fixture(
            params=NUMPY_GENERAL_TYPING_HINTS + NUMPY_IMAGES_TYPING_HINTS,
            ids=lambda x: repr_numpy_type(x[0], x[2]),
        )
        def attribute_numpy_typed_values(request):
            dtype, type_hint, dformat, values = request.param
            expected = lambda v: create_result(dtype, v)
            return type_hint, dformat, values, expected

        @pytest.fixture(
            params=WRONG_NUMPY_TYPING_HINTS, ids=lambda x: f"{x[-2].__name__}: {x[-1]}"
        )
        def attribute_wrong_numpy_typed(request):
            return request.param

    else:

        @pytest.fixture
        def command_numpy_typed_values(request):
            raise RuntimeError(
                f"Numpy typing supported only for Numpy >= 1.20, "
                f"while current version is {np.version.version}"
            )

        @pytest.fixture
        def attribute_numpy_typed_values(request):
            raise RuntimeError(
                f"Numpy typing supported only for Numpy >= 1.20, "
                f"while current version is {np.version.version}"
            )

        @pytest.fixture
        def attribute_wrong_numpy_typed(request):
            raise RuntimeError(
                f"Numpy typing supported only for Numpy >= 1.20, "
                f"while current version is {np.version.version}"
            )

    @pytest.fixture(
        params=list(DEV_ENCODED_DATA.items()),
        ids=list(DEV_ENCODED_DATA.keys()),
    )
    def dev_encoded_values(request):
        return request.param

    @pytest.fixture(
        params=EXTRACT_AS, ids=[f"extract_as.{req_type}" for req_type, _ in EXTRACT_AS]
    )
    def extract_as(request):
        requested_type, expected_type = request.param
        return requested_type, expected_type

    @pytest.fixture(params=BASE_TYPES)
    def base_type(request):
        return request.param

    @pytest.fixture(params=list(GreenMode.values.values()), ids=str)
    def green_mode(request):
        return request.param

    @pytest.fixture(
        params=[GreenMode.Synchronous, GreenMode.Asyncio, GreenMode.Gevent], ids=str
    )
    def server_green_mode(request):
        return request.param

    @pytest.fixture(
        params=[AttrDataFormat.SCALAR, AttrDataFormat.SPECTRUM, AttrDataFormat.IMAGE],
        ids=str,
    )
    def attr_data_format(request):
        return request.param

    @pytest.fixture(
        params=[
            SerialModel.BY_DEVICE,
            SerialModel.BY_CLASS,
            SerialModel.BY_PROCESS,
            SerialModel.NO_SYNC,
        ],
        ids=str,
    )
    def server_serial_model(request):
        return request.param


def wait_for_proxy(
    dev_name: str,
    proxy_class: type[DeviceProxy] = DeviceProxy,
    retries: int = 600,
    delay: float = 0.02,
) -> DeviceProxy:
    """Create a new DeviceProxy, retrying until it is responding.

    The DeviceProxy will try to ping the device and read the state at least once.

    :param dev_name: device name for DeviceProxy connection string
    :param proxy_class: Type of DeviceProxy class to instantiate (could be synchronous,
                        asyncio, or gevent versions of the class).  If using asyncio,
                        then provide: ``partial(tango.asyncio.DeviceProxy, wait=True)``.
    :param retries: number of times to retry attempts, optional
    :param delay: time to wait (seconds) between retries, optional

    :returns: DeviceProxy object created to access the specified device

    :raises RuntimeError: If the device is not responding before the timeout

    .. versionadded:: 10.1.0
    """
    proxy = None
    last_error = ""
    count = 0
    while count < retries:
        try:
            proxy = proxy_class(dev_name)
            break
        except DevFailed as exc:
            last_error = str(exc)
            time.sleep(delay)
        count += 1
    if proxy is not None:
        while count < retries:
            try:
                proxy.ping()
                proxy.state()
                return proxy
            except DevFailed as exc:
                last_error = str(exc)
                time.sleep(delay)
            count += 1
    raise RuntimeError(
        f"Device at {dev_name} did not respond within {count * delay:.1f} sec!\n"
        f"Last error: {last_error}."
    )


def wait_for_nodb_proxy_via_pid(
    pid: int,
    host: str,
    dev_name: str,
    proxy_class: type[DeviceProxy],
    retries: int = 600,
    delay: float = 0.02,
) -> DeviceProxy:
    """Create new DeviceProxy, with retrying until it is ready and responding.

    The PID is used to get the process information and probe it to find the correct
    TCP port number to connect to.  Creation of the DeviceProxy is retried until
    the device is responding, or times out.  The DeviceProxy will ping the
    device and read the state.

    :param pid: operating system process identifier
    :param host: hostname/IP that device server is listening on.
    :param dev_name: device name for DeviceProxy connection string
    :param proxy_class: Type of DeviceProxy class to instantiate (could be synchronous,
                        asyncio, or gevent versions of the class).  If using asyncio,
                        then provide: ``partial(tango.asyncio.DeviceProxy, wait=True)``.
    :param retries: number of times to retry attempts, optional
    :param delay: time to wait (seconds) between retries, optional

    :returns: DeviceProxy object created to access the specified device

    :raises RuntimeError: If the GIOP port couldn't be identified, or proxy timed out

    .. seealso::
        :func:`tango.test_context.get_server_port_via_pid`

    .. versionadded:: 10.1.0
    """
    t0 = time.time()
    port = get_server_port_via_pid(pid, host, retries, delay)

    timeout = retries * delay
    elapsed = time.time() - t0
    time_left = timeout - elapsed
    retries_left = max(1, int(time_left / delay))
    trl = f"tango://{host}:{port}/{dev_name}#dbase=no"
    return wait_for_proxy(trl, proxy_class, retries_left, delay)
