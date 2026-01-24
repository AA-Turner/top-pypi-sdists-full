#!/bin/bash
#
# Check for no pykern in package and run ci
#
set -euo pipefail

test_err() {
    echo "$@" 1>&2
    return 1
}

test_main() {
    if grep -r -i pykern chronver; then
        test_err "chronver python files may not use/mention pykern"
    fi
    if ! pip show pykern >& /dev/null; then
        pip install pykern
    fi
    pykern ci run
}

test_main "$@"
