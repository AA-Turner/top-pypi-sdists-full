/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

// this is a code, I do not understand, where should be used

/**
 * Convert a python sequence into a C++ container
 * The C++ container must have the push_back method
 */
template <typename ContainerType = StdStringVector>
struct from_sequence {
    /**
     * Convert a python dictionary to a Tango::DbData. The dictionary keys must
     * be strings representing the DbDatum name. The dictionary value can be
     * be one of the following:
     * - Tango::DbDatum : in this case the key is not used, and the
     *   item inserted in DbData will be a copy of the value
     * - sequence : it is translated into an array of strings and
     *   the DbDatum inserted in DbData will have name as the dict key and value
     *   the sequence of strings
     * - python object : its string representation is used
     *   as a DbDatum to be inserted
     *
     * @param[in] d the python dictionary to be translated
     * @param[out] db_data the array of DbDatum to be filled
     */
    static inline void convert(py::dict dict_in, Tango::DbData &db_data) {
        for(auto item : dict_in) {
            py::object key = item.first;
            py::object value = item.second;

            try {
                Tango::DbDatum db_datum = value.cast<Tango::DbDatum>();
                db_data.push_back(db_datum);
            } catch(const py::cast_error &) {
                std::string key_str = py::str(key);
                Tango::DbDatum db_datum(key_str.c_str());

                if(py::isinstance<py::str>(value)) {
                    db_datum.value_string.push_back(value.cast<const char *>());
                } else if(py::isinstance<py::sequence>(value) && !py::isinstance<py::str>(value)) {
                    db_datum.value_string = value.cast<StdStringVector>();
                } else {
                    py::object str_value = value.attr("__str__")();
                    db_datum.value_string.push_back(str_value.cast<const char *>());
                }

                db_data.push_back(db_datum);
            }
        }
    }
};
