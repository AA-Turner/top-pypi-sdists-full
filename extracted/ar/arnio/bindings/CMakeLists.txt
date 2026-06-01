pybind11_add_module(_arnio_cpp bind_arnio.cpp)

target_link_libraries(_arnio_cpp PRIVATE arnio_core)

install(TARGETS _arnio_cpp DESTINATION arnio)
