/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"
#include "convertors/type_casters.h"

#include "types_structs_macros.h"

extern const char *value_attr_name;
extern const char *w_value_attr_name;
extern const char *type_attr_name;
extern const char *is_empty_attr_name;
extern const char *has_failed_attr_name;

namespace PyDeviceAttribute {

/// @name Types
/// @{
typedef std::unique_ptr<std::vector<Tango::DeviceAttribute>> AutoDevAttrVector;
/// @}

/// Set the value of a DeviceAttribute from python (useful for write*)
void reset(Tango::DeviceAttribute &self,
           const Tango::AttributeInfo &attr_info,
           py::object py_value);

void reset(Tango::DeviceAttribute &self,
           const std::string &attr_name,
           Tango::DeviceProxy &dev_proxy,
           py::object py_value);

void attribute_values_from_cpp_into_python(Tango::DeviceAttribute &self,
                                           py::object &py_value,
                                           PyTango::ExtractAs extract_as = PyTango::ExtractAsNumpy);

template <typename TDeviceAttribute>
void update_data_format(Tango::DeviceProxy &dev_proxy, TDeviceAttribute *first, size_t nelems) {
    // Older devices do not send arg_format. So we try to discover it from
    // dim_x and dim_y. It is not perfect, sometimes we will get SCALAR for
    // SPECTRUM with size 1 for example. In that case, we must ask tango
    // for the actual value.
    TDeviceAttribute *p = first;
    std::vector<std::string> attr_names;
    for(size_t n = 0; n < nelems; ++n, ++p) {
        if((p->data_format != Tango::FMT_UNKNOWN) || (p->has_failed())) {
            continue;
        }
        if((p->get_dim_x() == 1) && (p->get_dim_y() == 0)) {
            attr_names.push_back(p->name);
        } else if(p->get_dim_y() == 0) {
            p->data_format = Tango::SPECTRUM;
        } else {
            p->data_format = Tango::IMAGE;
        }
    }
    if(attr_names.size()) {
        std::unique_ptr<Tango::AttributeInfoListEx> attr_infos;
        {
            py::gil_scoped_release no_gil;
            p = first;
            try {
                attr_infos.reset(dev_proxy.get_attribute_config_ex(attr_names));
                for(size_t n = 0, m = 0; n < nelems; ++n, ++p) {
                    if((p->data_format == Tango::FMT_UNKNOWN) && (!p->has_failed())) {
                        p->data_format = (*attr_infos)[m++].data_format;
                    }
                }
            } catch(Tango::DevFailed &) {
                // if we fail to get info about the missing attributes from
                // the server (because it as shutdown, for example) we assume
                // that they are SCALAR since dim_x is 1
                for(size_t n = 0; n < nelems; ++n, ++p) {
                    if((p->data_format == Tango::FMT_UNKNOWN) && (!p->has_failed())) {
                        p->data_format = Tango::SCALAR;
                    }
                }
            }
        }
    }
}

/// @param self The DeviceAttribute instance that the new python object
/// will represent. It must be allocated with new. The new python object
/// will handle it's destruction. There's never any reason to delete it
/// manually after a call to this: Even if this function fails, the
/// responsibility of destroying it will already be in py_value side or
/// the object will already be destroyed.
template <typename TDeviceAttribute>
py::object convert_to_python(TDeviceAttribute *self, PyTango::ExtractAs extract_as) {
    py::object py_value;
    try {
        py_value = py::cast(self, py::return_value_policy::take_ownership);
    } catch(...) {
        delete self;
        throw;
    }

    attribute_values_from_cpp_into_python(*self, py_value, extract_as);
    return py_value;
}

/// See the other convert_to_python version. Here we get a vector of
/// DeviceAttributes. The responsibility to deallocate it is always from
/// the caller (we will make a copy). This responsibility is unavoidable
/// as we get a reference to auto_ptr -> the caller must use an auto_ptr,
/// so the memory will finally be deleted.
template <typename TDeviceAttribute>
py::object convert_to_python(const std::unique_ptr<std::vector<TDeviceAttribute>> &dev_attr_vec,
                             Tango::DeviceProxy &dev_proxy,
                             PyTango::ExtractAs extract_as) {
    // Sometimes CppTango returns a nullptr instead of an empty vector
    // We convert it to None in python
    if(dev_attr_vec == nullptr) {
        py::object none;
        return none;
    }

    if(dev_attr_vec->empty()) {
        py::list ls;
        return ls;
    }

    update_data_format(dev_proxy, &(*dev_attr_vec)[0], dev_attr_vec->size());

    // Convert the c++ vector of DeviceAttribute into a pythonic list
    py::list ls;
    typename std::vector<TDeviceAttribute>::const_iterator i, e = dev_attr_vec->end();
    for(i = dev_attr_vec->begin(); i != e; ++i) {
        ls.append(convert_to_python(new TDeviceAttribute(*i), extract_as));
    }
    return ls;
}

/// Convert a DeviceAttribute to python (useful for read*)
/// @param dev_attr Should be a pointer allocated with new. You can forget
///                 about deallocating this object (python will do it) even
///                 if the call to convert_to_python fails.
/// @param dev_proxy Device proxy where the value was got. DeviceAttribute
///                 sent by older tango versions do not have all the
///                 necessary information to extract the values, so we
///                 may need to ask.
/// @param extract_as See ExtractAs enum.
template <typename TDeviceAttribute>
py::object convert_to_python(TDeviceAttribute *dev_attr, Tango::DeviceProxy &dev_proxy, PyTango::ExtractAs extract_as) {
    update_data_format(dev_proxy, dev_attr, 1);
    return convert_to_python(dev_attr, extract_as);
}
} // namespace PyDeviceAttribute
