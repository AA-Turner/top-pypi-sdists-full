export PySpice_source_path=${PWD}
export PySpice_examples_path=${PySpice_source_path}/examples

source /opt/python-virtual-env/py38/bin/activate
append_to_python_path_if_not ${PySpice_source_path}
append_to_python_path_if_not ${PySpice_source_path}/tools
append_to_python_path_if_not ${PySpice_source_path}/KiCadTools

# inv ngspice.install
NGSPICE_VERSION=34
append_to_ld_library_path_if_not ${PWD}/ngspice-${NGSPICE_VERSION}/lib/

# append_to_path_if_not /usr/local/stow/ngspice-${NGSPICE_VERSION}/bin
# append_to_ld_library_path_if_not /usr/local/stow/ngspice-${NGSPICE_VERSION}/lib/

# skidl
export KICAD_SYMBOL_DIR="/usr/share/kicad/library"
# export KICAD_SYMBOL_DIR="/usr/share/kicad-nightly/library"
