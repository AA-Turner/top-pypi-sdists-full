#!/bin/bash

function create_venv {
    venv_name=$1
    datahub_version="$2"
    plugins="$3"  # comma-separated list of plugins
    tmp_dir="$4"

    venv_dir="$tmp_dir/venv-$venv_name"

    echo 'Obtaining venv creation lock...'
    (
        flock --exclusive 200
        # TODO: When we move this to Python, we can use the `filelock` library.
        echo 'Acquired venv creation lock'
        SECONDS=0
        VENV_IS_REINSTALL=""

        if [ ! -d "$venv_dir" ]; then
            echo "venv doesn't exist.. minting.."
            uv venv $venv_dir
            source "$venv_dir/bin/activate"
            uv pip install --upgrade pip wheel setuptools
        else
            source "$venv_dir/bin/activate"
            VENV_IS_REINSTALL=1
        fi

        # we always install datahub-rest and datahub-kafka in addition to the plugin
        VENV_IS_REINSTALL=$VENV_IS_REINSTALL ./install_acryl_datahub.sh --version "$datahub_version" --plugin datahub-rest --plugin datahub-kafka --plugin "$plugins"

        echo "venv setup time = $SECONDS sec"
    ) 200>"$venv_dir.lock"

    # The setup happens in a subshell, so we need to re-activate the venv.
    source "$venv_dir/bin/activate"
}
