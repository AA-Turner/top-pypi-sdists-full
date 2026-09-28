# Copyright 2022-2026 Collabora Ltd.
# SPDX-License-Identifier: MIT

project(
    'dbus-python',
    'c',
    default_options: [
        'warning_level=2',
    ],
    meson_version: '>=0.60',
    version: '1.5.0',
)

pc_mod = import('pkgconfig')
py_mod = import('python')

project_include_directories = include_directories('include', 'dbus_bindings')

cc = meson.get_compiler('c')
compile_warnings = []
compile_warnings_c = []

if cc.get_id() != 'msvc'
  # -fno-common makes the linker more strict: on some systems the linker
  # is *always* this strict, so we want to behave like that everywhere.
  # We treat this like a warning, since that's basically how we're using it.
  compile_warnings += ['-fno-common']

  compile_warnings += [
      # Intentionally disabled: missing field initializers being implicitly
      # default-initialized is a feature, not a bug
      '-Wno-missing-field-initializers',

      # Unfortunately the Python headers trigger various warnings
      '-Wno-declaration-after-statement',
      '-Wno-inline',
      '-Wno-redundant-decls',
      '-Wno-switch-default',
      '-Wno-write-strings',

      # General warnings for both C and C++, excluding those that are part
      # of -Wall or -Wextra
      '-Wcast-align',
      '-Wdouble-promotion',
      '-Wduplicated-cond',
      '-Wfloat-equal',
      '-Wformat-nonliteral',
      '-Wformat-security',
      '-Wformat=2',
      '-Winit-self',
      '-Wlogical-op',
      '-Wmissing-declarations',
      '-Wmissing-format-attribute',
      '-Wmissing-include-dirs',
      '-Wmissing-noreturn',
      '-Wnull-dereference',
      '-Wpacked',
      '-Wpointer-arith',
      '-Wshadow',
      '-Wswitch-enum',
      '-Wundef',
      '-Wunused-but-set-variable',
  ]

  compile_warnings_c += [
      # Extra warnings just for C
      '-Wjump-misses-init',
      '-Wmissing-prototypes',
      '-Wnested-externs',
      '-Wold-style-definition',
      '-Wpointer-sign',
      '-Wstrict-prototypes',
  ]
endif

compile_warnings_c = cc.get_supported_arguments(compile_warnings + compile_warnings_c)
add_project_arguments(compile_warnings_c, language: 'c')

conf_data = configuration_data()
conf_data.set_quoted('PACKAGE_VERSION', meson.project_version())
configure_file(
    output : '_dbus-python-config.h',
    configuration: conf_data,
)
add_project_arguments(['-include', '_dbus-python-config.h'], language: 'c')

# Bring dbus-gmain into our namespace
redefine_dgmain_name = '_dbus_py_glib_ ## name'

add_project_arguments(
    '-DDBUS_GMAIN_FUNCTION_NAME(name)=' + redefine_dgmain_name,
    language: 'c',
)

dbus_gmain = subproject(
    'dbus-gmain',
    default_options: [
        'redefine_function_name=' + redefine_dgmain_name,
        'tests=false',
    ],
)
dbus_gmain_dep = dbus_gmain.get_variable('dbus_gmain_dep')

if get_option('python') == ''
    # This uses the same Python that was used to run Meson
    py = py_mod.find_installation()
else
    py = py_mod.find_installation(get_option('python'))
endif

dbus_dep = dependency('dbus-1', version: '>=1.8')

python_sources = files(
    'dbus/bus.py',
    'dbus/connection.py',
    'dbus/_compat.py',
    'dbus/_dbus.py',
    'dbus/decorators.py',
    'dbus/exceptions.py',
    'dbus/_expat_introspect_parser.py',
    'dbus/gi_service.py',
    'dbus/glib.py',
    'dbus/__init__.py',
    'dbus/lowlevel.py',
    'dbus/proxies.py',
    'dbus/server.py',
    'dbus/service.py',
    'dbus/types.py',
)
mainloop_sources = files(
    'dbus/mainloop/__init__.py',
    'dbus/mainloop/glib.py',
)

py.install_sources(
    python_sources,
    subdir: 'dbus',
    pure: false,
)
py.install_sources(
    mainloop_sources,
    subdir: 'dbus/mainloop',
    pure: false,
)

dbus_bindings = py.extension_module(
    '_dbus_bindings',
    sources: [
        'dbus_bindings/abstract.c',
        'dbus_bindings/bus.c',
        'dbus_bindings/bytes.c',
        'dbus_bindings/conn.c',
        'dbus_bindings/conn-methods.c',
        'dbus_bindings/containers.c',
        'dbus_bindings/debug.c',
        'dbus_bindings/exceptions.c',
        'dbus_bindings/float.c',
        'dbus_bindings/generic.c',
        'dbus_bindings/int.c',
        'dbus_bindings/unixfd.c',
        'dbus_bindings/libdbusconn.c',
        'dbus_bindings/mainloop.c',
        'dbus_bindings/message-append.c',
        'dbus_bindings/message.c',
        'dbus_bindings/message-get-args.c',
        'dbus_bindings/module.c',
        'dbus_bindings/pending-call.c',
        'dbus_bindings/server.c',
        'dbus_bindings/signature.c',
        'dbus_bindings/string.c',
        'dbus_bindings/validation.c',
    ],
    dependencies: [
        dbus_dep,
        py.dependency(),
    ],
    include_directories: project_include_directories,
    install: true,
)

dbus_glib_bindings = py.extension_module(
    '_dbus_glib_bindings',
    sources: [
        'dbus_glib_bindings/module.c',
    ],
    dependencies: [
        dbus_dep,
        dbus_gmain_dep,
        py.dependency(),
    ],
    include_directories: project_include_directories,
    install: true,
)

install_headers(
    'include/dbus/dbus-python.h',
    subdir: 'dbus-1.0/dbus',
)

pc_mod.generate(
    description: 'Python bindings for D-Bus',
    filebase: 'dbus-python',
    name: 'dbus-python',
    requires: ['dbus-1 >= 1.8'],
    subdirs: ['dbus-1.0'],
    variables: {
        'exec_prefix': '${prefix}',
        'datarootdir': '${prefix}' / get_option('datadir'),
    },
)

sphinx_dep = py_mod.find_installation(
    py.full_path(),
    modules: ['sphinx', 'sphinx_rtd_theme'],
    required: get_option('doc'),
)

if sphinx_dep.found()
    subdir('doc')
endif

dbus_run_session = find_program(
    'dbus-run-session',
    required: get_option('tests'),
)
gi_dep = py_mod.find_installation(
    py.full_path(),
    modules: ['gi'],
    required: get_option('tests').enabled(),
)

if dbus_run_session.found()
    subdir('test')
endif
