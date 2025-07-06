#!/bin/bash -l

#-------------------------------------------------------------------------------
# Copyright (C) 2018, 2020, 2021 Maximilian Stahlberg
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

#-------------------------------------------------------------------------------
# This script builds Conda packages for all relevant platforms and uploads them
# to Anaconda Cloud. To use the script, you need a working Conda distribution
# and an Anaconda user account that has access to the ${grpname} account.
#-------------------------------------------------------------------------------

set -e
cd "$(dirname "${BASH_SOURCE[0]}")"


if [ $# -ne 1 ]; then
	echo "usage: $0 (build | upload)"
	exit 1
fi


# Platforms to upload packages for.
platforms="linux-32 linux-64 win-32 win-64 osx-64"

# Name of the Anaconda user or group account to publish at.
grpname="picos"

# Output directory for built packages, relative to the recipe directory.
builddir="build"

# The platform that packages are originally built for.
platform="linux-64"

# Name of the temporary conda environment.
buildenv="picos-build"

# Additional channel to look for packages.
channel="conda-forge"


exitcode=0

echo ">>> Creating the temporary build environment."
# HACK: Use Python 3.8 to work around an upload failure:
#       https://github.com/Anaconda-Platform/anaconda-client/issues/555
conda create -y -n "${buildenv}" python=3.8 git conda-build anaconda-client

echo ">>> Activating the build environment."
conda activate "${buildenv}"

condaargs="-c ${channel} --no-anaconda-upload --output-folder ${builddir}"
condacmd="conda build . ${condaargs}"

if [ "$1" = "build" ]; then
	echo ">>> Building the packages."
	${condacmd}
fi

if [ ! -d "${builddir}/${platform}/" ]; then
	echo "(E) No ${platform} build directory found."
	exit 1
fi

echo ">>> Collecting ${platform} packages."
#startpkgfiles="$(${condacmd} --output)" # This takes ages.
startpkgfiles="$(ls -c1 ${builddir}/${platform}/picos-*.tar.bz2)"
echo "${startpkgfiles}"

if [ "$1" = "build" ]; then
	echo ">>> Converting the packages for other OS."
	for pkgfile in ${startpkgfiles}; do
		conda convert ${pkgfile} -p all -o "${builddir}"
	done
fi

echo ">>> Collecting packages for all supported platforms."
pkgfiles=""
for pkgfile in ${startpkgfiles}; do
	pkgfilename="$(basename "${pkgfile}")"
	for platform in ${platforms}; do
		new="${builddir}/${platform}/${pkgfilename}"
		ls "${new}"
		pkgfiles+=" ${new}"
	done
done

if [ "${pkgfiles}" = "" ]; then
	echo "(E) No packages found."
	exitcode=1
elif [ "$1" = "upload" ]; then
	echo ">>> Uploading the packages to Anaconda Cloud."
	if anaconda upload -u "${grpname}" ${pkgfiles}; then
		echo "(-) Upload successful."
	else
		echo "(E) Upload failed."
		exitcode=1
	fi
fi

echo ">>> Deactivating the build environment."
conda deactivate

exit ${exitcode}
