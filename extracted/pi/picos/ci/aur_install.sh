#!/bin/sh

#-------------------------------------------------------------------------------
# Copyright (C) 2021 Maximilian Stahlberg
#
# This file is part of PICOS Release Scripts.
#
# PICOS Release Scripts are free software: you can redistribute them and/or
# modify them under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# PICOS Release Scripts are distributed in the hope that they will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Install a package from the Arch User Repository (AUR).
# ------------------------------------------------------------------------------

# Obtain the snapshot.
cd /tmp
curl -O "https://aur.archlinux.org/cgit/aur.git/snapshot/${1}.tar.gz"
tar xf "${1}.tar.gz"
cd "${1}"

# Install dependencies. This does not work for AUR dependencies.
egrep '^[^a-z]*(make)?depends = ' .SRCINFO \
    | sed 's/.* = //' \
    | xargs pacman -S --noconfirm

# Prepare building as an unpriviledged user.
id -u makepkg &>/dev/null || useradd makepkg
chown makepkg .

# Build the package.
PKGEXT=".pkg.tar" su makepkg -c makepkg

# Install the package.
pacman -U --noconfirm "${1}"-*.pkg.tar
