/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

bool IS_BIGENDIAN() {
    const int n = 1;
    return (*(reinterpret_cast<const char *>(&n)) == 0);
}

namespace PyEncodedAttribute {
void encode_image(
    Tango::EncodedAttribute &self,
    py::object py_value,
    int &w,
    int &h,
    EncodingType encoding,
    double quality = 0.0 // Default value for quality (only used for JPEG encodings)
) {
    switch(encoding) {
    case EncodingType::GRAY8:
    case EncodingType::JPEG_GRAY8:
    case EncodingType::GRAY16:
    case EncodingType::RGB24:
    case EncodingType::JPEG_RGB24:
    case EncodingType::JPEG_RGB32:
        break;
    default:
        return;
    }

    void *buffer = nullptr;
    int bytes_per_pixel = 0;
    bool is_jpeg = false;

    // Determine bytes per pixel and if encoding is JPEG based on encoding type
    switch(encoding) {
    case EncodingType::GRAY8:
        bytes_per_pixel = 1;
        break;
    case EncodingType::JPEG_GRAY8:
        bytes_per_pixel = 1;
        is_jpeg = true;
        break;
    case EncodingType::GRAY16:
        bytes_per_pixel = 2;
        break;
    case EncodingType::RGB24:
        bytes_per_pixel = 3;
        break;
    case EncodingType::JPEG_RGB24:
        bytes_per_pixel = 3;
        is_jpeg = true;
        break;
    case EncodingType::JPEG_RGB32:
        bytes_per_pixel = 4;
        is_jpeg = true;
        break;
    }

    // Handle py::bytes and py::array inputs
    if(py::isinstance<py::bytes>(py_value)) {
        py::bytes py_bytes = py_value.cast<py::bytes>();
        const char *data = PyBytes_AsString(py_bytes.ptr());
        buffer = const_cast<char *>(data);

        switch(encoding) {
        case EncodingType::GRAY8:
            self.encode_gray8(static_cast<unsigned char *>(buffer), w, h);
            break;
        case EncodingType::JPEG_GRAY8:
            self.encode_jpeg_gray8(static_cast<unsigned char *>(buffer), w, h, quality);
            break;
        case EncodingType::RGB24:
            self.encode_rgb24(static_cast<unsigned char *>(buffer), w, h);
            break;
        case EncodingType::JPEG_RGB24:
            self.encode_jpeg_rgb24(static_cast<unsigned char *>(buffer), w, h, quality);
            break;
        case EncodingType::JPEG_RGB32:
            self.encode_jpeg_rgb32(static_cast<unsigned char *>(buffer), w, h, quality);
            break;
        case EncodingType::GRAY16:
            self.encode_gray16(static_cast<unsigned short *>(buffer), w, h);
            break;
        }
        return;
    } else if(py::isinstance<py::array>(py_value)) {
        py::array arr = py_value.cast<py::array>();

        if(arr.ndim() < 2) {
            throw py::type_error("Numpy array must have at least 2 dimensions");
        }

        w = static_cast<int>(arr.shape(1));
        h = static_cast<int>(arr.shape(0));

        if(encoding == EncodingType::GRAY16) {
            buffer = arr.mutable_data();
        } else {
            buffer = arr.mutable_data();
        }

        switch(encoding) {
        case EncodingType::GRAY8:
            self.encode_gray8(static_cast<unsigned char *>(buffer), w, h);
            break;
        case EncodingType::JPEG_GRAY8:
            self.encode_jpeg_gray8(static_cast<unsigned char *>(buffer), w, h, quality);
            break;
        case EncodingType::RGB24:
            self.encode_rgb24(static_cast<unsigned char *>(buffer), w, h);
            break;
        case EncodingType::JPEG_RGB24:
            self.encode_jpeg_rgb24(static_cast<unsigned char *>(buffer), w, h, quality);
            break;
        case EncodingType::JPEG_RGB32:
            self.encode_jpeg_rgb32(static_cast<unsigned char *>(buffer), w, h, quality);
            break;
        case EncodingType::GRAY16:
            self.encode_gray16(static_cast<unsigned short *>(buffer), w, h);
            break;
        }
        return;
    }

    // Handle Python sequences
    const int length = w * h;
    int total_bytes = bytes_per_pixel * length;
    std::unique_ptr<unsigned char[]> buffer_ptr(new unsigned char[static_cast<size_t>(total_bytes)]);
    buffer = buffer_ptr.get();
    unsigned char *p = static_cast<unsigned char *>(buffer);

    py::sequence seq = py_value.cast<py::sequence>();

    for(size_t y = 0; y < static_cast<size_t>(h); ++y) {
        py::object row_obj = seq[y];
        if(!py::isinstance<py::sequence>(row_obj)) {
            throw py::type_error("Expected sequence inside a sequence");
        }

        if(py::isinstance<py::bytes>(row_obj)) {
            py::bytes row_bytes = row_obj.cast<py::bytes>();
            int row_len = static_cast<int>(py::len(row_bytes));
            if(row_len != bytes_per_pixel * w) {
                throw py::type_error("All sequences inside a sequence must have the same size");
            }
            const char *row_data = PyBytes_AsString(row_bytes.ptr());
            memcpy(p, row_data, static_cast<size_t>(bytes_per_pixel) * static_cast<size_t>(w));
            p += bytes_per_pixel * w;
        } else {
            py::sequence row_seq = row_obj.cast<py::sequence>();
            if(static_cast<int>(py::len(row_seq)) != w) {
                throw py::type_error("All sequences inside a sequence must have the same size");
            }

            for(unsigned long x = 0; x < static_cast<unsigned long>(w); ++x) {
                py::object cell_obj = row_seq[x];
                if(py::isinstance<py::bytes>(cell_obj)) {
                    py::bytes cell_bytes = cell_obj.cast<py::bytes>();
                    if((encoding == EncodingType::RGB24 || encoding == EncodingType::JPEG_RGB24) && py::len(cell_bytes) != 3) {
                        throw py::type_error("All byte items must have length three for RGB24 encodings");
                    } else if(encoding == EncodingType::JPEG_RGB32 && py::len(cell_bytes) != 4) {
                        throw py::type_error("All byte items must have length four for JPEG_RGB32 encodings");
                    } else if(encoding == EncodingType::GRAY8 && py::len(cell_bytes) != 1) {
                        throw py::type_error("All byte items must have length one for GRAY8 encoding");
                    } else if(encoding == EncodingType::GRAY16 && py::len(cell_bytes) != 2) {
                        throw py::type_error("All byte items must have length two for GRAY16 encoding");
                    }

                    const char *cell_data = PyBytes_AsString(cell_bytes.ptr());
                    memcpy(p, cell_data, static_cast<size_t>(bytes_per_pixel));
                    p += bytes_per_pixel;
                } else if(py::isinstance<py::int_>(cell_obj)) {
                    if(encoding == EncodingType::GRAY16) {
                        uint16_t value_16 = cell_obj.cast<uint16_t>();
                        memcpy(p, &value_16, 2);
                        p += 2;
                    } else if(encoding == EncodingType::RGB24 || encoding == EncodingType::JPEG_RGB24 ||
                              encoding == EncodingType::JPEG_RGB32) {
                        uint32_t value32 = cell_obj.cast<uint32_t>();
                        if(encoding == EncodingType::RGB24 || encoding == EncodingType::JPEG_RGB24) {
                            uint8_t r, g, b;
                            if(IS_BIGENDIAN()) {
                                r = static_cast<uint8_t>((value32 >> 16) & 0xFFu);
                                g = static_cast<uint8_t>((value32 >> 8) & 0xFFu);
                                b = static_cast<uint8_t>(value32 & 0xFFu);
                            } else {
                                b = static_cast<uint8_t>((value32 >> 16) & 0xFFu);
                                g = static_cast<uint8_t>((value32 >> 8) & 0xFFu);
                                r = static_cast<uint8_t>(value32 & 0xFFu);
                            }
                            *p++ = r;
                            *p++ = g;
                            *p++ = b;
                        } else if(encoding == EncodingType::JPEG_RGB32) {
                            uint8_t r, g, b, a;
                            if(IS_BIGENDIAN()) {
                                r = static_cast<uint8_t>((value32 >> 24) & 0xFFu);
                                g = static_cast<uint8_t>((value32 >> 16) & 0xFFu);
                                b = static_cast<uint8_t>((value32 >> 8) & 0xFFu);
                                a = static_cast<uint8_t>(value32 & 0xFFu);
                            } else {
                                a = static_cast<uint8_t>((value32 >> 24) & 0xFFu);
                                b = static_cast<uint8_t>((value32 >> 16) & 0xFFu);
                                g = static_cast<uint8_t>((value32 >> 8) & 0xFFu);
                                r = static_cast<uint8_t>(value32 & 0xFFu);
                            }
                            *p++ = r;
                            *p++ = g;
                            *p++ = b;
                            *p++ = a;
                        }
                    } else if(encoding == EncodingType::GRAY8) {
                        uint8_t value_8 = cell_obj.cast<uint8_t>();
                        *p++ = value_8;
                    }
                } else {
                    throw py::type_error("Unsupported data type in array element");
                }
            }
        }
    }

    // Call the appropriate encode function
    if(is_jpeg) {
        switch(encoding) {
        case EncodingType::JPEG_GRAY8:
            self.encode_jpeg_gray8(static_cast<unsigned char *>(buffer), w, h, quality);
            break;
        case EncodingType::JPEG_RGB24:
            self.encode_jpeg_rgb24(static_cast<unsigned char *>(buffer), w, h, quality);
            break;
        case EncodingType::JPEG_RGB32:
            self.encode_jpeg_rgb32(static_cast<unsigned char *>(buffer), w, h, quality);
            break;
        default:
            throw py::type_error("Unsupported JPEG encoding type");
        }
    } else {
        switch(encoding) {
        case EncodingType::GRAY8:
            self.encode_gray8(static_cast<unsigned char *>(buffer), w, h);
            break;
        case EncodingType::GRAY16:
            self.encode_gray16(static_cast<unsigned short *>(buffer), w, h);
            break;
        case EncodingType::RGB24:
            self.encode_rgb24(static_cast<unsigned char *>(buffer), w, h);
            break;
        default:
            throw py::type_error("Unsupported encoding type");
        }
    }
}

py::object decode_image(
    Tango::EncodedAttribute &self,
    Tango::DeviceAttribute *attr,
    PyTango::ExtractAs extract_as,
    EncodingType decode_type) {
    py::object ret;

    switch(decode_type) {
    case EncodingType::GRAY8:
    case EncodingType::GRAY16:
    case EncodingType::JPEG_RGB32:
        break;
    default: // we support only three for now
        return ret;
    }

    int width = 0, height = 0;

    // Buffer pointers
    unsigned char *buffer_char = nullptr;
    unsigned short *buffer_short = nullptr;

    // Determine the decoding method and buffer type
    switch(decode_type) {
    case EncodingType::GRAY8:
        self.decode_gray8(attr, &width, &height, &buffer_char);
        break;
    case EncodingType::GRAY16:
        self.decode_gray16(attr, &width, &height, &buffer_short);
        break;
    case EncodingType::JPEG_RGB32:
        self.decode_rgb32(attr, &width, &height, &buffer_char);
        break;
    default:
        throw std::invalid_argument("Unsupported decode_type");
    }

    // Handle extraction based on the desired format
    try {
        // to avoid a lot of static_cast
        unsigned long uheight = static_cast<unsigned long>(height);
        unsigned long uwidth = static_cast<unsigned long>(width);

        switch(extract_as) {
        case PyTango::ExtractAsNumpy: {
            // Create the NumPy array
            py::dtype dt;
            void *data_ptr;

            switch(decode_type) {
            case EncodingType::GRAY8:
                dt = py::dtype::of<unsigned char>();
                data_ptr = static_cast<void *>(buffer_char);
                break;
            case EncodingType::GRAY16:
                dt = py::dtype::of<unsigned short>();
                data_ptr = static_cast<void *>(buffer_short);
                break;
            case EncodingType::JPEG_RGB32:
                dt = py::dtype::of<uint32_t>();
                data_ptr = static_cast<void *>(buffer_char);
                break;
            default:
                throw std::invalid_argument("Unsupported decode_type");
            }

            // Define the dimensions for the NumPy array
            std::vector<std::size_t> dims = {uheight, uwidth};

            // Create a capsule to manage the buffer's memory
            py::capsule free_when_done;

            switch(decode_type) {
            case EncodingType::GRAY8:
            case EncodingType::JPEG_RGB32:
                free_when_done = py::capsule(buffer_char, [](void *p) {
                    unsigned char *buf = reinterpret_cast<unsigned char *>(p);
                    delete[] buf;
                });
                break;
            case EncodingType::GRAY16:
                free_when_done = py::capsule(buffer_short, [](void *p) {
                    unsigned short *buf = reinterpret_cast<unsigned short *>(p);
                    delete[] buf;
                });
                break;
            default:
                throw std::invalid_argument("Unsupported decode_type");
            }

            // Create the NumPy array
            py::array ret_array(dt, dims, data_ptr, free_when_done);

            ret = ret_array;

            break;
        }

        case PyTango::ExtractAsString: {
            int nb_bytes;
            const char *buffer_str_ptr;

            switch(decode_type) {
            case EncodingType::GRAY8:
            case EncodingType::JPEG_RGB32:
                nb_bytes = (decode_type == EncodingType::JPEG_RGB32) ? (width * height * 4) : (width * height);
                buffer_str_ptr = reinterpret_cast<const char *>(buffer_char);
                break;
            case EncodingType::GRAY16:
                nb_bytes = width * height * static_cast<int>(sizeof(unsigned short));
                buffer_str_ptr = reinterpret_cast<const char *>(buffer_short);
                break;
            default:
                throw std::invalid_argument("Unsupported decode_type");
            }

            py::bytes buffer_str(buffer_str_ptr, static_cast<size_t>(nb_bytes));

            ret = py::make_tuple(width, height, buffer_str);

            // Free the buffer
            if(decode_type == EncodingType::GRAY8 || decode_type == EncodingType::JPEG_RGB32) {
                delete[] buffer_char;
            } else if(decode_type == EncodingType::GRAY16) {
                delete[] buffer_short;
            }

            break;
        }

        case PyTango::ExtractAsTuple: {
            // Create a tuple of tuples representing each row
            py::tuple ret_tuple(height);

            for(unsigned long y = 0; y < uheight; ++y) {
                py::tuple row_tuple(width);

                switch(decode_type) {
                case EncodingType::GRAY8: {
                    for(unsigned long x = 0; x < uwidth; ++x) {
                        unsigned char pixel = buffer_char[(y * uwidth) + x];
                        py::bytes pixel_bytes(reinterpret_cast<const char *>(&pixel), 1);
                        row_tuple[x] = pixel_bytes;
                    }
                    break;
                }
                case EncodingType::GRAY16: {
                    for(unsigned long x = 0; x < uwidth; ++x) {
                        unsigned short pixel = buffer_short[(y * uwidth) + x];
                        row_tuple[x] = py::int_(pixel);
                    }
                    break;
                }
                case EncodingType::JPEG_RGB32: {
                    for(unsigned long x = 0; x < uwidth; ++x) {
                        uint32_t data;
                        unsigned long idx = 4 * (y * uwidth + x);
                        if(IS_BIGENDIAN()) {
                            data = (static_cast<uint32_t>(buffer_char[idx]) << 24) |
                                   (static_cast<uint32_t>(buffer_char[idx + 1]) << 16) |
                                   (static_cast<uint32_t>(buffer_char[idx + 2]) << 8) |
                                   (static_cast<uint32_t>(buffer_char[idx + 3]));
                        } else {
                            data = (static_cast<uint32_t>(buffer_char[idx + 3]) << 24) |
                                   (static_cast<uint32_t>(buffer_char[idx + 2]) << 16) |
                                   (static_cast<uint32_t>(buffer_char[idx + 1]) << 8) |
                                   (static_cast<uint32_t>(buffer_char[idx]));
                        }

                        row_tuple[x] = py::int_(data);
                    }
                    break;
                }
                default:
                    throw std::invalid_argument("Unsupported decode_type");
                }
                ret_tuple[y] = row_tuple;
            }

            ret = ret_tuple;

            // Free the buffer
            if(decode_type == EncodingType::GRAY8 || decode_type == EncodingType::JPEG_RGB32) {
                delete[] buffer_char;
            } else if(decode_type == EncodingType::GRAY16) {
                delete[] buffer_short;
            }

            break;
        }

        case PyTango::ExtractAsPyTango3:
        case PyTango::ExtractAsList: {
            // Create a list of lists representing each row
            py::list ret_list(height);

            for(unsigned long y = 0; y < uheight; ++y) {
                py::list row_list(width);

                switch(decode_type) {
                case EncodingType::GRAY8: {
                    for(unsigned long x = 0; x < uwidth; ++x) {
                        unsigned char pixel = buffer_char[(y * uwidth) + x];
                        py::bytes pixel_bytes(reinterpret_cast<const char *>(&pixel), 1);
                        row_list[x] = pixel_bytes;
                    }
                    break;
                }
                case EncodingType::GRAY16: {
                    for(unsigned long x = 0; x < uwidth; ++x) {
                        unsigned short pixel = buffer_short[(y * uwidth) + x];
                        row_list[x] = py::int_(pixel);
                    }
                    break;
                }
                case EncodingType::JPEG_RGB32: {
                    for(unsigned long x = 0; x < uwidth; ++x) {
                        uint32_t data;
                        unsigned long idx = 4 * (y * uwidth + x);
                        if(IS_BIGENDIAN()) {
                            data = (static_cast<uint32_t>(buffer_char[idx]) << 24) |
                                   (static_cast<uint32_t>(buffer_char[idx + 1]) << 16) |
                                   (static_cast<uint32_t>(buffer_char[idx + 2]) << 8) |
                                   (static_cast<uint32_t>(buffer_char[idx + 3]));
                        } else {
                            data = (static_cast<uint32_t>(buffer_char[idx + 3]) << 24) |
                                   (static_cast<uint32_t>(buffer_char[idx + 2]) << 16) |
                                   (static_cast<uint32_t>(buffer_char[idx + 1]) << 8) |
                                   (static_cast<uint32_t>(buffer_char[idx]));
                        }

                        row_list[x] = py::int_(data);
                    }
                    break;
                }
                default:
                    throw std::invalid_argument("Unsupported decode_type");
                }

                ret_list[y] = row_list;
            }

            ret = ret_list;

            // Free the buffer
            if(decode_type == EncodingType::GRAY8 || decode_type == EncodingType::JPEG_RGB32) {
                delete[] buffer_char;
            } else if(decode_type == EncodingType::GRAY16) {
                delete[] buffer_short;
            }

            break;
        }
        default:
            throw std::invalid_argument("Unsupported extract_as");
        }
    } catch([[maybe_unused]] const std::exception &e) {
        delete[] buffer_char;
        delete[] buffer_short;

        throw; // Re-throw the exception
    }

    return ret;
}

} // namespace PyEncodedAttribute

void export_encoded_attribute(py::module &m) {
    py::class_<Tango::EncodedAttribute>(m, "EncodedAttribute")
        .def(py::init<>())
        .def(py::init<int, bool>(),
             py::arg("buf_pool_size"),
             py::arg("serialization") = false)
        .def("_encode_gray8",
             [](Tango::EncodedAttribute &self, py::object py_value, int w, int h) {
                 PyEncodedAttribute::encode_image(self, py_value, w, h, EncodingType::GRAY8);
             })
        .def("_encode_jpeg_gray8",
             [](Tango::EncodedAttribute &self, py::object py_value, int w, int h, double quality) {
                 PyEncodedAttribute::encode_image(self, py_value, w, h, EncodingType::JPEG_GRAY8, quality);
             })
        .def("_encode_gray16",
             [](Tango::EncodedAttribute &self, py::object py_value, int w, int h) {
                 PyEncodedAttribute::encode_image(self, py_value, w, h, EncodingType::GRAY16);
             })

        .def("_encode_rgb24",
             [](Tango::EncodedAttribute &self, py::object py_value, int w, int h) {
                 PyEncodedAttribute::encode_image(self, py_value, w, h, EncodingType::RGB24);
             })
        .def("_encode_jpeg_rgb24",
             [](Tango::EncodedAttribute &self, py::object py_value, int w, int h, double quality) {
                 PyEncodedAttribute::encode_image(self, py_value, w, h, EncodingType::JPEG_RGB24, quality);
             })
        .def("_encode_jpeg_rgb32",
             [](Tango::EncodedAttribute &self, py::object py_value, int w, int h, double quality) {
                 PyEncodedAttribute::encode_image(self, py_value, w, h, EncodingType::JPEG_RGB32, quality);
             })
        .def("_decode_gray8",
             [](Tango::EncodedAttribute &self, Tango::DeviceAttribute *attr, PyTango::ExtractAs extract_as) {
                 return PyEncodedAttribute::decode_image(self, attr, extract_as, EncodingType::GRAY8);
             })
        .def("_decode_gray16",
             [](Tango::EncodedAttribute &self, Tango::DeviceAttribute *attr, PyTango::ExtractAs extract_as) {
                 return PyEncodedAttribute::decode_image(self, attr, extract_as, EncodingType::GRAY16);
             })
        .def("_decode_rgb32",
             [](Tango::EncodedAttribute &self, Tango::DeviceAttribute *attr, PyTango::ExtractAs extract_as) {
                 return PyEncodedAttribute::decode_image(self, attr, extract_as, EncodingType::JPEG_RGB32);
             });
}
