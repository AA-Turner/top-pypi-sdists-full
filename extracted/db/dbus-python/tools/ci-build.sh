#!/bin/bash

# Copyright © 2016 Simon McVittie
#
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

set -e
set -x

NULL=
srcdir="$(pwd)"
prefix="$(mktemp -d -t "prefix.XXXXXX")"

if [ -z "$dbus_ci_parallel" ]; then
	dbus_ci_parallel=2
fi

if [ -n "$dbus_ci_system_python" ]; then
	# Reset to standard paths to use the Ubuntu version of python
	unset LDFLAGS
	unset PYTHONPATH
	unset PYTHON_CFLAGS
	unset PYTHON_CONFIGURE_OPTS
	unset VIRTUAL_ENV
	export PATH=/usr/bin:/bin
	export PYTHON="$(command -v "$dbus_ci_system_python")"
fi

export PATH="$HOME/.local/bin:$PATH"

meson setup \
	--prefix="$prefix" \
	-Ddoc=enabled \
	-Dinstalled_tests=true \
	-Dpython="${PYTHON:-python3}" \
	. build
meson compile -C build
meson test -C build
meson dist -C build

rm -fr "$prefix"
meson install -C build
( cd "$prefix" && find . -ls )

case "${PYTHON:-python3}" in
	(*3.[0-8]-dbg)
		# -dbg builds with Meson don't set the right ABI suffix in older Pythons
		test_meson=
		;;
	(*)
		test_meson=yes
		;;
esac

if [ -n "$test_meson" ]; then (
	dbus_ci_pyversion="$(${PYTHON:-python3} -c 'import sysconfig; print(sysconfig.get_config_var("VERSION"))')"
	export PYTHONPATH="$prefix/lib/python$dbus_ci_pyversion/site-packages:$prefix/lib/python3/dist-packages:$PYTHONPATH"
	export XDG_DATA_DIRS="$prefix/share:/usr/local/share:/usr/share"
	gnome-desktop-testing-runner dbus-python
); fi

# re-run the tests with dbus-python only installed via pip from Meson dist
rm -fr _venv
${PYTHON:-python3} -m virtualenv --python="${PYTHON:-python3}" _venv
if [ -n "$test_meson" ]; then (
	. _venv/bin/activate
	export PYTHON="$(pwd)/_venv/bin/python3"
	"$PYTHON" -m pip install -vvv build/meson-dist/dbus-python-*.tar.?z
	cp -a "$prefix/share" "$prefix/venv-meta"
	sed -E -i -e "/^Exec=/ s# (PYTHON=)?(/usr)?(/bin/)?python3[0-9.]*(-dbg)? # \\1$PYTHON #g" \
		"$prefix"/venv-meta/installed-tests/dbus-python/*.test
	head -n-0 -v "$prefix"/venv-meta/installed-tests/dbus-python/*.test
	find _venv -ls
	# not directly applicable for a venv
	rm -f "$prefix/venv-meta/installed-tests/dbus-python/test-import-repeatedly.test"
	export XDG_DATA_DIRS="$prefix/venv-meta:/usr/local/share:/usr/share"
	gnome-desktop-testing-runner dbus-python
); fi
