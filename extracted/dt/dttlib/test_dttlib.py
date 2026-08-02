# test_dttlib.py
import pytest
from dttlib import (
    DTT, ViewSet, Channel, NDSDataType, ChannelType, PipDuration,
    PipInstant, InlineFFTParams, ChannelQuery, NDS2Cache,
    ResponseToUser, FFTWindow, TrendType, AnalysisId, AnalysisNameId,
    ChannelName
)

# Helper function to create a simple callback for DTT
def response_callback(response):
    if isinstance(response, ResponseToUser.AllMessages):
        print("Got messages:", response._0)
    elif isinstance(response, ResponseToUser.ChannelQueryResult):
        print("Got channel query result:", response.channels)
    elif isinstance(response, ResponseToUser.ScopeViewResult):
        print(f"Got scope view result for id {response.id}:", response.result)

@pytest.fixture
def dtt():
    """Fixture to create a DTT instance with test callback"""
    return DTT(response_callback)

@pytest.fixture
def test_channel():
    """Fixture for a test channel"""
    return Channel("TEST-CHANNEL", NDSDataType.Float64, PipDuration.freq_hz_to_period(16384.0))

def test_dtt_initialization(dtt):
    """Test that DTT can be initialized"""
    assert dtt is not None
    dtt.no_op()  # Test basic communication

def test_channel_creation():
    """Test Channel object creation and properties"""
    channel = Channel("TEST-CHANNEL", NDSDataType.Float64, PipDuration.freq_hz_to_period(16384.0))
    assert channel.name == "TEST-CHANNEL"
    assert channel.data_type == NDSDataType.Float64
    assert channel.rate_hz == 16384.0
    assert channel.channel_type == ChannelType.Raw  # Default value

def test_view_set_creation(test_channel):
    """Test ViewSet creation and methods"""
    # Test creation from channels
    channels = [test_channel]
    view_set = ViewSet.from_channels(channels)
    assert not view_set.has_unresolved_channels()
    
    # Test creation from channel names
    channel_names = ["TEST-CHANNEL-1", "TEST-CHANNEL-2"]
    view_set = ViewSet.from_channel_names(channel_names, TrendType.Raw)
    assert view_set.has_unresolved_channels()
    assert set(view_set.to_resolved_channel_names()) == set(channel_names)

def test_pip_duration_and_instant():
    """Test PipDuration and PipInstant functionality"""
    # Test PipDuration
    duration = PipDuration.from_seconds(1.0)
    assert duration.to_seconds() == 1.0
    
    # Test PipInstant
    instant = PipInstant.from_gpst_seconds(1000.0)
    assert instant.to_gpst_seconds() == 1000.0
    
    # Test arithmetic
    new_instant = instant + duration
    assert new_instant.to_gpst_seconds() == 1001.0

def test_inline_fft_params():
    """Test InlineFFTParams creation and properties"""
    params = InlineFFTParams()
    params.bandwidth_hz = 1.0
    params.overlap = 0.5
    params.window = FFTWindow.Hann
    params.start_pip = PipInstant.from_gpst_seconds(1000.0)
    params.end_pip = PipInstant.from_gpst_seconds(1001.0)
    
    assert params.bandwidth_hz == 1.0
    assert params.overlap == 0.5
    assert params.window == FFTWindow.Hann

def test_channel_query():
    """Test ChannelQuery creation and properties"""
    query = ChannelQuery(
        pattern="TEST-*",
        channel_types=[ChannelType.Raw],
        data_types=[NDSDataType.Float64],
        min_sample_rate=1.0,
        max_sample_rate=16384.0
    )
    assert query is not None

# def test_scope_view_creation(dtt, test_channel):
#     """Test scope view creation and updates"""
#     view_set = ViewSet.from_channels([test_channel])
#     span = PipDuration.from_seconds(10.0)
#
#     # Test online scope view
#     online_view = dtt.new_online_scope_view(view_set, span)
#     assert online_view.id >= 0
#
#     # Test fixed scope view
#     start = PipInstant.from_gpst_seconds(1000.0)
#     end = PipInstant.from_gpst_seconds(1010.0)
#     fixed_view = dtt.new_fixed_scope_view(view_set, start, end)
#     assert fixed_view.id >= 0
#
#     # Test view updates
#     fft_params = InlineFFTParams()
#     fft_params.bandwidth_hz = 1.0
#     fft_params.overlap = 0.5
#     online_view.set_fft_params(fft_params)
#
#     # Test span update
#     new_span = PipDuration.from_seconds(20.0)
#     online_view.update(span_pip=new_span)

def test_nds_cache():
    """Test NDS2Cache creation"""
    cache = NDS2Cache(size_bytes=1024*1024, default_file_path="/tmp/test_cache")
    data_source = cache.as_ref()
    assert data_source is not None

def test_find_channels(dtt):
    """Test channel finding functionality"""
    query = ChannelQuery(pattern="TEST-*")
    dtt.find_channels(query)  # Results will come through callback

def test_analysis_id(test_channel):
    id1 = AnalysisId.from_channel(test_channel)
    id2 = AnalysisId.from_channel(test_channel)
    assert id1 == id2
    s = set([id1, id2])
    assert len(s) == 1
    id3 = AnalysisId("f", [id1])
    id4 = AnalysisId("f", [id2])
    assert id3 == id4
    s = set([id3, id4])
    assert len(s) == 1

    txt = str(id3)
    assert txt == "f(TEST-CHANNEL)"

def test_analysis_name_id():
    c1 = ChannelName("TEST-CHANNEL")
    c2 = ChannelName("TEST-CHANNEL")
    id1 = AnalysisNameId.from_channel(c1)
    id2 = AnalysisNameId.from_channel(c2)
    assert id1 == id2
    s = set([id1, id2])
    assert len(s) == 1
    id3 = AnalysisNameId("f", [id1])
    id4 = AnalysisNameId("f", [id2])
    assert id3 == id4
    s = set([id3, id4])
    assert len(s) == 1

    txt = str(id3)
    assert txt == "f(TEST-CHANNEL)"    