#!/bin/bash

set -euo pipefail

# Usage: install_acryl_datahub.sh [--version <version>] [--plugin <plugin>]*
# Also supports PIP_EXTRA_ARGS, PIP_EXTRA_PLUGINS, and PIP_EXTRA_PACKAGES environment variables.
# And the PIP_GLOBAL_EXTRA_PLUGINS and PIP_GLOBAL_EXTRA_PACKAGES environment variables, which can be set at the container level.
# Will skip if VENV_IS_REINSTALL is set to 1 and this package doesn't need to be reinstalled every time.
PACKAGE=${PIP_ACRYL_DATAHUB_PACKAGE_NAME:-acryl-datahub}

# Parse arguments.
version=""
while [[ $# -gt 0 ]]; do
	key="$1"
	case $key in
		--version)
			version="$2"
			shift
			shift
			;;
		--plugin)
			plugins+=("$2")
			shift
			shift
			;;
		*)
			echo "Unknown argument: $key"
			exit 1
			;;
	esac
done

# Construct the pip install command.
package_suffix=""
if [[ -n "$version" ]]; then
	if [[ "$version" == http* ]]; then
		# If it's a URL to a .whl file, we install it directly.
		if [[ "$version" == *.whl ]]; then
			package_suffix=" @ ${version}"
		else
			# Otherwise, we assume it's an exact link to our vercel / docs site.
			package_suffix=" @ ${version}/artifacts/wheels/acryl_datahub-0.0.0.dev1-py3-none-any.whl"
		fi
		# Some URLs always point to the latest version, so we need to clear the pip cache
		# so that they are re-downloaded.
		pip cache remove -qqq 'acryl*' || true
		VENV_FORCE_REINSTALL=1
	elif [[ "$version" == v* ]]; then
		# If version begins with a v, strip it.
		package_suffix="==${version:1}"
	elif [[ "$version" == latest ]]; then
		# If it's "latest", we need to upgrade the package.
		PIP_EXTRA_ARGS="${PIP_EXTRA_ARGS:-} --upgrade"
		VENV_FORCE_REINSTALL=1
	else
		# Otherwise, assume it's a version number.
		package_suffix="==${version}"
	fi
fi

# Construct the extras string. Package extras can come from:
# - The --plugin arguments
# - The PIP_EXTRA_PLUGINS environment variable
# - The PIP_GLOBAL_EXTRA_PLUGINS environment variable
package_extras=""  # comma-separated list of extras to install
for plugin in "${plugins[@]+"${plugins[@]}"}"; do  # see https://stackoverflow.com/a/61551944
	# Merge the plugins array into a comma-separated string. The weirdness of the for
	# loop is to avoid an "unset variable" error, since empty arrays are considered unset.
	package_extras="${package_extras:+$package_extras,}${plugin}"
done
if [[ -n "${PIP_EXTRA_PLUGINS:-}" ]]; then
	package_extras="${package_extras:+$package_extras,}$PIP_EXTRA_PLUGINS"
fi
if [[ -n "${PIP_GLOBAL_EXTRA_PLUGINS:-}" ]]; then
	package_extras="${package_extras:+$package_extras,}$PIP_GLOBAL_EXTRA_PLUGINS"
fi

# Install the package.
if [[ -n "${VENV_IS_REINSTALL:-}" && -z "${VENV_FORCE_REINSTALL:-}" ]]; then
	echo "venv is already set up"
	exit 0
fi

# The final command will look like one of these:
# uv pip install "acryl-datahub[datahub-rest,datahub-kafka,snowflake,my-custom-extra] @ https://something.vercel.com/artifacts/wheels/acryl_datahub-0.0.0.dev1-py3-none-any.whl" extra_package extra_package2
# uv pip install "acryl-datahub[datahub-rest,datahub-kafka,snowflake,my-custom-extra]==0.10.2" extra_package extra_package2
# uv pip install --upgrade "acryl-datahub[datahub-rest,datahub-kafka,snowflake,my-custom-extra]" extra_package extra_package2
set -x  # print the final pip install command
uv pip install ${PIP_EXTRA_ARGS:-} "${PACKAGE}${package_extras:+[$package_extras]}${package_suffix}" ${PIP_EXTRA_PACKAGES:-} ${PIP_GLOBAL_EXTRA_PACKAGES:-}
