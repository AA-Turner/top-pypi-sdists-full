# Copyright 2022 Collabora Ltd.
# SPDX-License-Identifier: MIT

doc_sources = files(
    'API_CHANGES.txt',
    'conf.py',
    'dbus.bus.rst',
    'dbus.connection.rst',
    'dbus.decorators.rst',
    'dbus.exceptions.rst',
    'dbus.gi_service.rst',
    'dbus.glib.rst',
    'dbus.gobject_service.rst',
    'dbus.lowlevel.rst',
    'dbus.mainloop.rst',
    'dbus.proxies.rst',
    'dbus.rst',
    'dbus.server.rst',
    'dbus.service.rst',
    'dbus.types.rst',
    'index.rst',
    'news.rst',
    'PY3PORT.txt',
    'tutorial.txt',
    )

sphinx = custom_target(
    'sphinx',
    command: [
        py.full_path(),
        '-m', 'sphinx',
        '-b', 'html',
        meson.current_source_dir(),
        '@OUTPUT@',
    ],
    depends: [
        dbus_bindings,
        dbus_glib_bindings,
    ],
    input: python_sources + doc_sources,
    output: 'html',
    build_by_default: true,
    install: true,
    install_dir: get_option('datadir') / 'doc' / meson.project_name(),
    install_tag: 'doc',
)

custom_target(
    'maintainer-update-website',
    command: [
        'env',
        '--chdir', '@BUILD_ROOT@',
        files('maintainer-update-website.sh'),
    ],
    depends: [sphinx],
    output: '_uploaded',
)
