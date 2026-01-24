/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

// Helper function to serialize DeviceAttributeConfig
py::tuple get_state_DeviceAttributeConfig(const Tango::DeviceAttributeConfig &self) {
    return py::make_tuple(
        self.name,
        self.writable,
        self.data_format,
        self.data_type,
        self.max_dim_x,
        self.max_dim_y,
        self.description,
        self.label,
        self.unit,
        self.standard_unit,
        self.display_unit,
        self.format,
        self.min_value,
        self.max_value,
        self.min_alarm,
        self.max_alarm,
        self.writable_attr_name,
        pickle_stdstringvector(self.extensions));
}

// Helper function to serialize AttributeInfo
py::tuple get_state_AttributeInfo(const Tango::AttributeInfo &self) {
    // Serialize the base class part
    py::tuple config = get_state_DeviceAttributeConfig(self);
    return py::make_tuple(config, self.disp_level);
}

// Helper function to deserialize DeviceAttributeConfig
Tango::DeviceAttributeConfig set_state_DeviceAttributeConfig(py::tuple py_tuple) {
    if(py_tuple.size() != 18) {
        throw std::runtime_error("Invalid state!");
    }

    Tango::DeviceAttributeConfig config;

    config.name = py_tuple[0].cast<std::string>();
    config.writable = py_tuple[1].cast<Tango::AttrWriteType>();
    config.data_format = py_tuple[2].cast<Tango::AttrDataFormat>();
    config.data_type = py_tuple[3].cast<int>();
    config.max_dim_x = py_tuple[4].cast<int>();
    config.max_dim_y = py_tuple[5].cast<int>();
    config.description = py_tuple[6].cast<std::string>();
    config.label = py_tuple[7].cast<std::string>();
    config.unit = py_tuple[8].cast<std::string>();
    config.standard_unit = py_tuple[9].cast<std::string>();
    config.display_unit = py_tuple[10].cast<std::string>();
    config.format = py_tuple[11].cast<std::string>();
    config.min_value = py_tuple[12].cast<std::string>();
    config.max_value = py_tuple[13].cast<std::string>();
    config.min_alarm = py_tuple[14].cast<std::string>();
    config.max_alarm = py_tuple[15].cast<std::string>();
    config.writable_attr_name = py_tuple[16].cast<std::string>();
    config.extensions = unpickled_stdstringvector(py_tuple[17]);
    return config;
}

// Helper function to deserialize AttributeInfo
Tango::AttributeInfo set_state_AttributeInfo(py::tuple py_tuple) {
    if(py_tuple.size() != 2) {
        throw std::runtime_error("Invalid state!");
    }

    // Deserialize the base class part
    py::tuple py_config = py_tuple[0].cast<py::tuple>();
    Tango::DeviceAttributeConfig config = set_state_DeviceAttributeConfig(py_config);

    Tango::AttributeInfo info;

    // Copy base class attributes
    static_cast<Tango::DeviceAttributeConfig &>(info) = config;

    info.disp_level = py_tuple[1].cast<Tango::DispLevel>();

    return info;
}

void export_attribute_config_and_info(py::module &m) {
    py::class_<Tango::DeviceAttributeConfig>(m,
                                             "DeviceAttributeConfig",
                                             R"doc(
    A base structure containing available information for an attribute
    with the following members:

        - name : (str) attribute name
        - writable : (AttrWriteType) write type (R, W, RW, R with W)
        - data_format : (AttrDataFormat) data format (SCALAR, SPECTRUM, IMAGE)
        - data_type : (int) attribute type (float, string,..)
        - max_dim_x : (int) first dimension of attribute (spectrum or image attributes)
        - max_dim_y : (int) second dimension of attribute(image attribute)
        - description : (int) attribute description
        - label : (str) attribute label (Voltage, time, ...)
        - unit : (str) attribute unit (V, ms, ...)
        - standard_unit : (str) standard unit
        - display_unit : (str) display unit
        - format : (str) how to display the attribute value (ex: for floats could be '%6.2f')
        - min_value : (str) minimum allowed value
        - max_value : (str) maximum allowed value
        - min_alarm : (str) low alarm level
        - max_alarm : (str) high alarm level
        - writable_attr_name : (str) name of the writable attribute
        - extensions : (StdStringVector) extensions (currently not used)
)doc")
        .def(py::init<>())
        .def(py::init<const Tango::DeviceAttributeConfig &>())
        .def(py::pickle(
            &get_state_DeviceAttributeConfig,
            &set_state_DeviceAttributeConfig))
        .def_readwrite("name", &Tango::DeviceAttributeConfig::name)
        .def_readwrite("writable", &Tango::DeviceAttributeConfig::writable)
        .def_readwrite("data_format", &Tango::DeviceAttributeConfig::data_format)
        .def_readwrite("data_type", &Tango::DeviceAttributeConfig::data_type)
        .def_readwrite("max_dim_x", &Tango::DeviceAttributeConfig::max_dim_x)
        .def_readwrite("max_dim_y", &Tango::DeviceAttributeConfig::max_dim_y)
        .def_readwrite("description", &Tango::DeviceAttributeConfig::description)
        .def_readwrite("label", &Tango::DeviceAttributeConfig::label)
        .def_readwrite("unit", &Tango::DeviceAttributeConfig::unit)
        .def_readwrite("standard_unit", &Tango::DeviceAttributeConfig::standard_unit)
        .def_readwrite("display_unit", &Tango::DeviceAttributeConfig::display_unit)
        .def_readwrite("format", &Tango::DeviceAttributeConfig::format)
        .def_readwrite("min_value", &Tango::DeviceAttributeConfig::min_value)
        .def_readwrite("max_value", &Tango::DeviceAttributeConfig::max_value)
        .def_readwrite("min_alarm", &Tango::DeviceAttributeConfig::min_alarm)
        .def_readwrite("max_alarm", &Tango::DeviceAttributeConfig::max_alarm)
        .def_readwrite("writable_attr_name", &Tango::DeviceAttributeConfig::writable_attr_name)
        .def_readwrite("extensions", &Tango::DeviceAttributeConfig::extensions);

    py::class_<Tango::AttributeInfo, Tango::DeviceAttributeConfig>(m,
                                                                   "AttributeInfo",
                                                                   R"doc(
    A structure (inheriting from :class:`DeviceAttributeConfig`) containing
    available information for an attribute with the following members:

        - disp_level : (DispLevel) display level (OPERATOR, EXPERT)

        Inherited members are:

            - name : (str) attribute name
            - writable : (AttrWriteType) write type (R, W, RW, R with W)
            - data_format : (AttrDataFormat) data format (SCALAR, SPECTRUM, IMAGE)
            - data_type : (int) attribute type (float, string,..)
            - max_dim_x : (int) first dimension of attribute (spectrum or image attributes)
            - max_dim_y : (int) second dimension of attribute(image attribute)
            - description : (int) attribute description
            - label : (str) attribute label (Voltage, time, ...)
            - unit : (str) attribute unit (V, ms, ...)
            - standard_unit : (str) standard unit
            - display_unit : (str) display unit
            - format : (str) how to display the attribute value (ex: for floats could be '%6.2f')
            - min_value : (str) minimum allowed value
            - max_value : (str) maximum allowed value
            - min_alarm : (str) low alarm level
            - max_alarm : (str) high alarm level
            - writable_attr_name : (str) name of the writable attribute
            - extensions : (StdStringVector) extensions (currently not used)
)doc")
        .def(py::init<>())
        .def(py::init<const Tango::AttributeInfo &>())
        .def(py::pickle(
            &get_state_AttributeInfo,
            &set_state_AttributeInfo))
        .def_readwrite("disp_level", &Tango::AttributeInfo::disp_level);

    py::class_<Tango::AttributeInfoEx, Tango::AttributeInfo>(m,
                                                             "AttributeInfoEx",
                                                             R"doc(
    A structure (inheriting from :class:`AttributeInfo`) containing
    available information for an attribute with the following members:

        - alarms : object containing alarm information (see AttributeAlarmInfo).
        - events : object containing event information (see AttributeEventInfo).
        - sys_extensions : StdStringVector

        Inherited members are:

            - name : (str) attribute name
            - writable : (AttrWriteType) write type (R, W, RW, R with W)
            - data_format : (AttrDataFormat) data format (SCALAR, SPECTRUM, IMAGE)
            - data_type : (int) attribute type (float, string,..)
            - max_dim_x : (int) first dimension of attribute (spectrum or image attributes)
            - max_dim_y : (int) second dimension of attribute(image attribute)
            - description : (int) attribute description
            - label : (str) attribute label (Voltage, time, ...)
            - unit : (str) attribute unit (V, ms, ...)
            - standard_unit : (str) standard unit
            - display_unit : (str) display unit
            - format : (str) how to display the attribute value (ex: for floats could be '%6.2f')
            - min_value : (str) minimum allowed value
            - max_value : (str) maximum allowed value
            - min_alarm : (str) low alarm level
            - max_alarm : (str) high alarm level
            - writable_attr_name : (str) name of the writable attribute
            - extensions : (StdStringVector) extensions (currently not used)
            - disp_level : (DispLevel) display level (OPERATOR, EXPERT)
)doc")
        .def(py::init<>())
        .def(py::init<const Tango::AttributeInfoEx &>())
        .def(py::pickle(
            [](const Tango::AttributeInfoEx &self) { // __getstate__
                // Serialize the base class part
                py::tuple info = get_state_AttributeInfo(self);
                return py::make_tuple(info,
                                      self.root_attr_name,
                                      self.memorized,
                                      pickle_stdstringvector(self.enum_labels),
                                      self.alarms,
                                      self.events,
                                      pickle_stdstringvector(self.sys_extensions));
            },
            [](py::tuple py_tuple) { // __setstate__
                if(py_tuple.size() != 7) {
                    throw std::runtime_error("Invalid state!");
                }

                // Deserialize the base class part
                py::tuple py_info = py_tuple[0].cast<py::tuple>();
                Tango::AttributeInfo info = set_state_AttributeInfo(py_info);

                Tango::AttributeInfoEx info_ex;

                // Copy base class attributes
                static_cast<Tango::AttributeInfo &>(info_ex) = info;

                info_ex.root_attr_name = py_tuple[1].cast<std::string>();
                info_ex.memorized = py_tuple[2].cast<Tango::AttrMemorizedType>();
                info_ex.enum_labels = unpickled_stdstringvector(py_tuple[3]);
                info_ex.alarms = py_tuple[4].cast<Tango::AttributeAlarmInfo>();
                info_ex.events = py_tuple[5].cast<Tango::AttributeEventInfo>();
                info_ex.sys_extensions = unpickled_stdstringvector(py_tuple[6]);

                return info_ex;
            }))

        .def_readwrite("root_attr_name", &Tango::AttributeInfoEx::root_attr_name)
        .def_readwrite("memorized", &Tango::AttributeInfoEx::memorized)
        .def_readwrite("enum_labels", &Tango::AttributeInfoEx::enum_labels)
        .def_readwrite("alarms", &Tango::AttributeInfoEx::alarms)
        .def_readwrite("events", &Tango::AttributeInfoEx::events)
        .def_readwrite("sys_extensions", &Tango::AttributeInfoEx::sys_extensions);
}
