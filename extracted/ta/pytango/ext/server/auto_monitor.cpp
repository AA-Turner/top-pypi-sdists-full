/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"

namespace PyTango {

class AutoTangoMonitor {
    Tango::AutoTangoMonitor *mon;
    Tango::DeviceImpl *dev;
    Tango::DeviceClass *klass;

  public:
    AutoTangoMonitor(Tango::DeviceImpl *dev_arg) :
        mon(),
        dev(),
        klass() {
        dev = dev_arg;
    }

    AutoTangoMonitor(Tango::DeviceClass *klass_arg) :
        mon(),
        dev(),
        klass() {
        klass = klass_arg;
    }

    void acquire() {
        if(mon != nullptr) {
            return;
        }
        if(dev != nullptr) {
            py::gil_scoped_release no_gil;
            mon = new Tango::AutoTangoMonitor(dev);
        } else if(klass != nullptr) {
            py::gil_scoped_release no_gil;
            mon = new Tango::AutoTangoMonitor(klass);
        }
    }

    void release() {
        if(mon != nullptr) {
            delete mon;
            mon = nullptr;
        }
    }

    ~AutoTangoMonitor() {
        release();
    }
};

class AutoTangoAllowThreads {
  public:
    AutoTangoAllowThreads(Tango::DeviceImpl *dev) {
        Tango::Util *util = Tango::Util::instance();
        Tango::SerialModel ser = util->get_serial_model();

        switch(ser) {
        case Tango::BY_DEVICE:
            mon = &(dev->get_dev_monitor());
            break;
        case Tango::BY_CLASS:
            // mon = &(dev->device_class->ext->only_one);
            break;
        case Tango::BY_PROCESS:
            // mon = &(util->ext->only_one);
            break;
        default:
            mon = nullptr;
        }
        release();
    }

    void acquire() {
        if(mon == nullptr) {
            return;
        }

        py::gil_scoped_release no_gil;
        for(int i = 0; i < count; ++i) {
            mon->get_monitor();
        }
    }

  protected:
    void release() {
        if(mon == nullptr) {
            return;
        }

        int cur_thread = omni_thread::self()->id();
        int mon_thread = mon->get_locking_thread_id();

        // do something only if the monitor was taken by the current thread
        if(mon_thread == cur_thread) {
            do {
                mon->rel_monitor();
                mon_thread = mon->get_locking_thread_id();
                count++;
            } while(mon_thread == cur_thread);
        } else {
            mon = nullptr;
        }
    }

  private:
    Tango::TangoMonitor *mon{nullptr};
    int count{0};
    omni_thread::ensure_self auto_self;
};

} // namespace PyTango

void export_auto_tango_monitor(py::module &m) {
    py::class_<PyTango::AutoTangoMonitor>(m,
                                          "AutoTangoMonitor",
                                          R"doc(
    In a tango server, guard the tango monitor within a python context::

        with AutoTangoMonitor(dev):
            # code here is protected by the tango device monitor
            do something
)doc")
        .def(py::init<Tango::DeviceImpl *>())
        .def(py::init<Tango::DeviceClass *>())
        .def("_acquire", &PyTango::AutoTangoMonitor::acquire)
        .def("_release", &PyTango::AutoTangoMonitor::release);

    py::class_<PyTango::AutoTangoAllowThreads>(m,
                                               "AutoTangoAllowThreads",
                                               R"doc(
    In a tango server, free the tango monitor within a context:

        with AutoTangoAllowThreads(dev):
            # code here is not under the tango device monitor
            do something
)doc")
        .def(py::init<Tango::DeviceImpl *>(), py::arg("device"))
        .def("_acquire", &PyTango::AutoTangoAllowThreads::acquire);
}
