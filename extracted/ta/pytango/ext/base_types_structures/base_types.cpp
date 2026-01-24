/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"
#include "pyutils.h"

//
// Necessary equality operators for having vectors exported to python
//

namespace Tango {

inline bool operator==(const Tango::DbDatum &dd1, const Tango::DbDatum &dd2) {
    return dd1.name == dd2.name && dd1.value_string == dd2.value_string;
}

inline bool operator==(const Tango::DbDevInfo &di1, const Tango::DbDevInfo &di2) {
    return di1.name == di2.name && di1._class == di2._class && di1.server == di2.server;
}

inline bool operator==(const Tango::DbDevImportInfo &dii1, const Tango::DbDevImportInfo &dii2) {
    return dii1.name == dii2.name && dii1.exported == dii2.exported && dii1.ior == dii2.ior &&
           dii1.version == dii2.version;
}

inline bool operator==(const Tango::DbDevExportInfo &dei1, const Tango::DbDevExportInfo &dei2) {
    return dei1.name == dei2.name && dei1.ior == dei2.ior && dei1.host == dei2.host && dei1.version == dei2.version &&
           dei1.pid == dei2.pid;
}

inline bool operator==(const Tango::DbHistory &dh1_, const Tango::DbHistory &dh2_) {
    auto &dh1 = const_cast<Tango::DbHistory &>(dh1_);
    auto &dh2 = const_cast<Tango::DbHistory &>(dh2_);

    return dh1.get_name() == dh2.get_name() && dh1.get_attribute_name() == dh2.get_attribute_name() &&
           dh1.is_deleted() == dh2.is_deleted();
}

inline bool operator==([[maybe_unused]] const Tango::GroupReply &dh1_, [[maybe_unused]] const Tango::GroupReply &dh2_) {
    /// @todo ?
    return false;
}

inline bool operator==(const Tango::TimeVal &tv1, const Tango::TimeVal &tv2) {
    return tv1.tv_sec == tv2.tv_sec && tv1.tv_usec == tv2.tv_usec && tv1.tv_nsec == tv2.tv_nsec;
}

inline bool operator==(const Tango::DeviceData &dd1_, const Tango::DeviceData &dd2_) {
    auto &dd1 = const_cast<Tango::DeviceData &>(dd1_);
    auto &dd2 = const_cast<Tango::DeviceData &>(dd2_);

    return // dh1.any == dh2.any &&
        dd1.exceptions() == dd2.exceptions();
}

inline bool operator==(const Tango::DeviceDataHistory &ddh1_, const Tango::DeviceDataHistory &ddh2_) {
    auto &ddh1 = const_cast<Tango::DeviceDataHistory &>(ddh1_);
    auto &ddh2 = const_cast<Tango::DeviceDataHistory &>(ddh2_);

    return operator==(static_cast<Tango::DeviceData>(ddh1),
                      static_cast<Tango::DeviceData>(ddh2)) &&
           ddh1.failed() == ddh2.failed() && ddh1.date() == ddh2.date();
    //&& ddh1.errors() == ddh2.errors();
}
} // namespace Tango

int raise_asynch_exception(long thread_id, py::object exp_klass) {
    return PyThreadState_SetAsyncExc(static_cast<unsigned long>(thread_id), exp_klass.ptr());
}

void export_base_types(py::module_ &m) {
    // See https://stackoverflow.com/a/60744217 and https://github.com/pybind/pybind11/issues/1940
    // we want StdStringVector to be opaque (for the cases were we pass-by-reference but also want
    // implicit conversions from list so that it is convenient
    py::bind_vector<StdStringVector>(m, "StdStringVector");
    py::implicitly_convertible<py::list, StdStringVector>();
    py::implicitly_convertible<py::tuple, StdStringVector>();

    py::bind_vector<StdLongVector>(m, "StdLongVector");
    py::implicitly_convertible<py::list, StdLongVector>();
    py::implicitly_convertible<py::tuple, StdLongVector>();

    py::bind_vector<StdDoubleVector>(m, "StdDoubleVector");
    py::implicitly_convertible<py::list, StdDoubleVector>();
    py::implicitly_convertible<py::tuple, StdDoubleVector>();

    m.def("raise_asynch_exception", &raise_asynch_exception);

    m.def("_get_tango_lib_release", &Tango::_convert_tango_lib_release);
}

void export_complicated_types(py::module_ &m) {
    // these vectors must be exported after the individual classes are exported,
    // otherwise pybind11-stubgen cannot parce them

    py::bind_vector<Tango::AttributeInfoList>(m, "AttributeInfoList");

    py::bind_vector<Tango::AttributeInfoListEx>(m, "AttributeInfoListEx");

    py::bind_vector<Tango::CommandInfoList>(m, "CommandInfoList");

    py::bind_vector<Tango::DeviceDataHistoryList>(m, "DeviceDataHistoryList");

    py::bind_vector<Tango::DbData>(m, "DbData");

    py::bind_vector<Tango::DbDevExportInfos>(m, "DbDevExportInfos");

    py::bind_vector<Tango::DbDevImportInfos>(m, "DbDevImportInfos");

    py::bind_vector<Tango::DbDevInfos>(m, "DbDevInfos");

    py::bind_vector<std::vector<Tango::DbHistory>>(m, "DbHistoryList");

    py::bind_vector<std::vector<Tango::DeviceData>>(m, "DeviceDataList");

    py::bind_vector<Tango::EventDataList>(m, "EventDataList");

    py::bind_vector<StdNamedDevFailedVector>(m, "StdNamedDevFailedVector");
}
