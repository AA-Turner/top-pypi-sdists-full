#!/bin/bash

# Copies LLVM's Itanium/Microsoft/Rust/D demangler into this repository.

set -eu

# Adjust to match your local llvm checkout.

LLVM_SRC=$HOME/src/llvm-project/llvm

cd "$(dirname "$0")"/..

LLVM_INC_SRC=$LLVM_SRC/include/llvm

LLVM_DST=src/third_party/llvm
LLVM_INC_DST=$LLVM_DST/include/llvm

rm -rf $LLVM_INC_DST/Demangle
rm -rf $LLVM_DST/lib

# Demangler headers + .def tables.
mkdir -p $LLVM_INC_DST
cp -R "$LLVM_INC_SRC"/Demangle $LLVM_INC_DST

# Demangler sources.
mkdir -p $LLVM_DST/lib
cp -R "$LLVM_SRC"/lib/Demangle $LLVM_DST/lib
rm -f $LLVM_DST/lib/Demangle/CMakeLists.txt

# License.
cp "$LLVM_SRC"/../LICENSE.TXT $LLVM_DST/LICENSE.txt
