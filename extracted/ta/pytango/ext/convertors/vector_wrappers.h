/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"

template <typename T>
class VectorWrapper {
  public:
    static_assert(std::is_class_v<T>, "T must be a class type");

    using PtrVector = std::vector<T *>;

    VectorWrapper(PtrVector *vec) :
        vec_ptr(vec) { }

    py::object get_item(size_t index) const {
        if(index >= vec_ptr->size()) {
            throw py::index_error();
        }
        return py::cast(vec_ptr->at(index), py::return_value_policy::reference);
    }

    void set_item(size_t index, py::object value) {
        if(index >= vec_ptr->size()) {
            throw py::index_error();
        }
        T *ptr = value.cast<T *>();
        vec_ptr->at(index) = ptr;
        // Manage the lifetime
        managed_objects.push_back(value);
    }

    void append(py::object value) {
        T *ptr = value.cast<T *>();
        vec_ptr->push_back(ptr);
        // Manage the lifetime
        managed_objects.push_back(value);
    }

    // not sure if cpp functionality is needed

    //    T* operator[](size_t index) {
    //        return (*vec_ptr)[index];
    //    }

    //    void append(T* item) {
    //        vec_ptr->push_back(item);
    //    }

    size_t size() const {
        return vec_ptr->size();
    }

    PtrVector *get_ptr() const {
        return vec_ptr;
    }

  private:
    PtrVector *vec_ptr;
    std::vector<py::object> managed_objects; // Keep references to Python objects
};
