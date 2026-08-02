import dtt
import time
from queue import Queue


m_queue = Queue()

def callback(m):
    #print(f"Queueing {m} in python")
    m_queue.put(m)


def harness():
    return

def test_init():
    d = dtt.init(callback)
    d.close_scope_view(0)
    x = m_queue.get(timeout=1.0)
    #print(x)

## Scope view tests
def test_get_data():
    d = dtt.init(callback)
    cache = dtt.NDS2Cache(dtt.DataFlow.Unordered, 1<<30, "")
    d.set_data_source(cache.as_ref())
    span_pip = dtt.PipDuration.from_seconds(10 * 60.0)
    print(f"span_pip = {span_pip.to_seconds()}")
    channels = [
        #dtt.Channel("H1:GDS-CALIB_STRAIN", dtt.NDSDataType.Float64, 2**14),
        dtt.Channel("H1:ALS-X_REFL_CTRL_OUT_DQ", dtt.NDSDataType.Float32, 2**14),
    ]
    channels = dtt.ViewSet.from_channels(channels)
    d.new_online_scope_view(0, span_pip, channels)
    last_m = None
    count = 0
    start = time.time()
    while True:
        try:
            m = m_queue.get()
            now = time.time()
        except:
            break
        if type(m) == dtt.ResponseToUser.ScopeViewResult:
            last_m = m
            r = m.result
            start_gps = r.value.start_gps_pip.to_gpst_seconds()
            end_gps = r.value.end_gps_pip().to_gpst_seconds()
            if count == 0:
                first_start = start_gps
                delta = now - end_gps
            diff_s = now - end_gps - delta
            print(f"Time = {now - start}\tDelta = {diff_s}\tStart = {start_gps - first_start} end = {end_gps - first_start}")
            count += 1
        else:
            print(m)

if __name__ == "__main__":
    last_m = test_get_data()
