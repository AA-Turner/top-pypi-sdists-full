#!/bin/bash

# Copyright © 2015-2018 Collabora Ltd.
#
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

set -euo pipefail
set -x

NULL=

# ci_distro:
# OS distribution in which we are testing
# Typical values: ubuntu, debian; maybe fedora in future
: "${ci_distro:=debian}"

# ci_host:
# Either "native", or an Autoconf --host argument to cross-compile
# the package (not currently supported for dbus-python)
: "${ci_host:=native}"

# ci_suite:
# OS suite (release, branch) in which we are testing.
# Typical values for ci_distro=debian: sid, buster
# Typical values for ci_distro=fedora might be 25, rawhide
: "${ci_suite:=bookworm}"

if [ $(id -u) = 0 ]; then
    sudo=
else
    sudo=sudo
fi

have_system_meson=

if [ -n "${dbus_ci_system_python-}" ]; then
    if [ -z "${dbus_ci_system_python_module_suffix+set}" ]; then
        case "$dbus_ci_system_python}" in
            (*-dbg)
                dbus_ci_system_python_module_suffix=-dbg
                ;;
            (*)
                dbus_ci_system_python_module_suffix=
                ;;
        esac
    fi
fi

case "$ci_distro:$ci_suite" in
    (debian:bullseye)
        # Workaround for https://bugs.debian.org/1147093
        # Ideally we'd use archive.debian.org,
        # but we can't do that until https://bugs.debian.org/1147150
        # is solved
        sed -i -e '/bullseye-security/d' /etc/apt/sources.list
        echo "deb" \
            "[" \
            "signed-by=/usr/share/keyrings/debian-archive-keyring.gpg" \
            "check-valid-until=no" \
            "]" \
            "http://snapshot.debian.org/archive/debian-security/20260903T220410Z" \
            "bullseye-security main" \
            >> /etc/apt/sources.list.d/bullseye-security.list
        ;;
esac

case "$ci_distro" in
    (debian|ubuntu)
        # Don't ask questions, just do it
        sudo="$sudo env DEBIAN_FRONTEND=noninteractive"

        $sudo apt-get -y update

        $sudo apt-get -y install --no-install-recommends \
            ccache \
            debhelper \
            docbook-xml \
            docbook-xsl \
            gcc \
            git \
            gnome-desktop-testing \
            libdbus-1-dev \
            libglib2.0-dev \
            make \
            ninja-build \
            sudo \
            virtualenv \
            wget \
            xmlto \
            ${NULL}

        if [ -n "${dbus_ci_system_python-}" ]; then
              $sudo apt-get -y install \
                ${dbus_ci_system_python} \
                ${dbus_ci_system_python%-dbg}-dev \
                python3-docutils \
                python3-gi${dbus_ci_system_python_module_suffix} \
                python3-pip \
                python3-setuptools \
                python3-sphinx \
                python3-sphinx-rtd-theme \
                python3-tap \
                ${NULL}
        fi

        case "$ci_suite" in
            (buster|focal|bullseye)
                $sudo apt-get -y install dbus
                ;;

            (*)
                $sudo apt-get -y install dbus-daemon
                ;;
        esac

        case "$ci_suite" in
            (buster|focal|bullseye)
                ninja=ninja==1.10.2.4
                ;;

            (*)
                $sudo apt-get -y install meson
                ninja=ninja
                have_system_meson=true
                ;;
        esac

        # Needed for distcheck
        case "$ci_suite:$dbus_ci_system_python" in
            (buster:*|focal:*|bullseye:*|jammy:*)
                "${dbus_ci_system_python-python3}" -m pip install --user \
                    "pyproject_metadata==0.9.0" \
                    tomli \
                    ${NULL}
                ;;

            (*)
                $sudo apt-get -y install \
                    python3-pyproject-metadata \
                    ${NULL}
                ;;
        esac
        ;;

    (*)
        echo "Don't know how to set up ${ci_distro}" >&2
        exit 1
        ;;
esac

if [ -n "$have_system_meson" ]; then
    :
elif [ -n "${dbus_ci_system_python-}" ]; then
    "$dbus_ci_system_python" -m pip install --user meson $ninja
else
    pip install meson $ninja
fi

# vim:set sw=4 sts=4 et:
