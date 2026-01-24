/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

/// The following class ensures usage in a non-omniORB thread will
/// still get a dummy omniORB thread ID - cppTango requires threads to
/// be identifiable in this way.  It should only be acquired once for the
/// lifetime of the thread, and must be released before the thread is
/// cleaned up.
/// See https://github.com/tango-controls/pytango/issues/307
class EnsureOmniThread {
    omni_thread::ensure_self *ensure_self;

  public:
    EnsureOmniThread() {
        ensure_self = nullptr;
    }

    // since pybind11 does not have a direct analog of boost::noncopyable,
    // we have to delete copy constructors by ourself
    EnsureOmniThread(const EnsureOmniThread &) = delete;            // Delete copy constructor
    EnsureOmniThread &operator=(const EnsureOmniThread &) = delete; // Delete copy assignment operator

    void acquire() {
        if(ensure_self == nullptr) {
            ensure_self = new omni_thread::ensure_self;
        }
    }

    void release() {
        if(ensure_self != nullptr) {
            delete ensure_self;
            ensure_self = nullptr;
        }
    }

    ~EnsureOmniThread() {
        release();
    }
};

/**
 * Determines if the calling thread is (or looks like) an omniORB thread.
 *
 * @return returns true if the calling thread has an omniORB thread ID or false otherwise
 */
inline bool is_omni_thread() {
    omni_thread *thread_id = omni_thread::self();
    return (thread_id != nullptr);
}

void export_ensure_omni_thread(py::module_ &m) {
    py::class_<EnsureOmniThread>(m,
                                 "EnsureOmniThread",
                                 py::module_local(),
                                 R"doc(
            Tango servers and clients that start their own additional threads
            that will interact with Tango must guard these threads within this
            Python context.  This is especially important when working with
            event subscriptions, and pushing events.

            This context handler class ensures a non-omniORB thread will still
            get a dummy omniORB thread ID - cppTango requires threads to
            be identifiable in this way.  It should only be acquired once for
            the lifetime of the thread, and must be released before the thread
            is cleaned up.

            Here is an example::

                import tango
                from threading import Thread
                from time import sleep


                def my_thread_run():
                    with tango.EnsureOmniThread():
                        eid = dp.subscribe_event(
                            "double_scalar", tango.EventType.PERIODIC_EVENT, cb)
                        while running:
                            print(f"num events stored {len(cb.get_events())}")
                            sleep(1)
                        dp.unsubscribe_event(eid)


                cb = tango.utils.EventCallback()  # print events to stdout
                dp = tango.DeviceProxy("sys/tg_test/1")
                dp.poll_attribute("double_scalar", 1000)
                thread = Thread(target=my_thread_run)
                running = True
                thread.start()
                sleep(5)
                running = False
                thread.join()

            .. versionadded:: 9.3.2)doc")
        .def(py::init<>())
        .def("_acquire", &EnsureOmniThread::acquire)
        .def("_release", &EnsureOmniThread::release);

    m.def("is_omni_thread",
          is_omni_thread,
          R"doc(
            Determines if the calling thread is (or looks like) an omniORB thread.
            This includes user threads that have a dummy omniORB thread ID, such
            as that provided by EnsureOmniThread.

                Parameters : None

                Return     : (bool) True if the calling thread is an omnithread.

            New in PyTango 9.3.2)doc");
}
