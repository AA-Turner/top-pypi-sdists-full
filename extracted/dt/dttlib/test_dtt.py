# import dttlib
# import time
# from queue import Queue
#
#
# m_queue = Queue()
#
# def callback(m):
#     m_queue.put(m)
#
#
# def harness():
#     return
#
# def test_init():
#     d = dttlib.init(callback)
#     d.close_scope_view(0)
#     x = m_queue.get(timeout=1.0)
#
# ## Scope view tests
# def test_get_past_data():
#     d = dttlib.init(callback)
#     cache = dttlib.NDS2Cache(dttlib.DataFlow.Unordered, 1<<30, "")
#     d.set_data_source(cache.as_ref())
#     start_gps_sec = dttlib.PipInstant.from_gpst_seconds(1403722629)
#     end_gps_sec = dttlib.PipInstant.from_gpst_seconds(1403722639)
#     channels = [dttlib.Channel("H1:GDS-CALIB_STRAIN", dttlib.NDSDataType.Float64, 2**14)]
#
#     channels = dttlib.ViewSet.from_channels(channels)
#     d.new_fixed_scope_view(0, start_gps_sec, end_gps_sec, channels)
#     last_m = None
#     while True:
#         try:
#             m = m_queue.get(timeout=5.0)
#             print(m)
#         except:
#             break
#         if type(m) == dttlib.ResponseToUser.ScopeViewResult:
#             last_m = m
#
#     assert(last_m is not None)
#     assert(last_m.id == 0)
#     r = last_m.result
#     assert(r.channel.channel_name == "H1:GDS-CALIB_STRAIN")
#
#     # Always returns a minimum of 64 seconds of data
#     # this channel is 2^14 Hz
#     assert(len(r.value.data) == 10 * 2**14)
#     assert(r.value.data[0] == 7.952822151470825e-18)
#
# def test_live_get_data():
#     d = dttlib.init(callback)
#     cache = dttlib.NDS2Cache(dttlib.DataFlow.Unordered, 1<<30, "")
#     d.set_data_source(cache.as_ref())
#     span_pip = dttlib.PipDuration.from_seconds(60 * 60.0)
#     print(f"span_pip = {span_pip.to_seconds()}")
#     channels = [dttlib.Channel("H1:GDS-CALIB_STRAIN", dttlib.NDSDataType.Float64, 2**14)]
#
#     channels = dttlib.ViewSet.from_channels(channels)
#     d.new_online_scope_view(0, span_pip, channels)
#     last_m = None
#     count = 0
#     start = time.time()
#     while True:
#         try:
#             m = m_queue.get(timeout=5.0)
#             now = time.time()
#         except:
#             break
#         if type(m) == dttlib.ResponseToUser.ScopeViewResult:
#             last_m = m
#             r = m.result
#             start_gps = r.value.start_gps_pip.to_gpst_seconds()
#             end_gps = r.value.end_gps_pip().to_gpst_seconds()
#             if count == 0:
#                 first_start = start_gps
#                 delta = now - end_gps
#             diff_s = now - end_gps - delta
#             print(f"Time = {now - start}\tDelta = {diff_s}\tStart = {start_gps - first_start} end = {end_gps - first_start}")
#             count += 1
#             if count > 30: break
#         else:
#             print(m)
#
#     assert(last_m is not None)
#     assert(last_m.id == 0)
#     r = last_m.result
#     assert(r.channel.channel_name == "H1:GDS-CALIB_STRAIN")
#     assert(len(r.value.data) >= 2**14)
#     assert(False)