#!/bin/bash

# Copies everything Swift's demangler needs into this repository.
#
# Derived from https://github.com/nico/demumble/blob/main/scripts/copy-swift-demangle.sh.

set -eu

# Adjust these to match your local swift and llvm checkouts.

SWIFT_SRC=$HOME/src/swift
LLVM_SRC=$HOME/src/llvm-project/llvm

cd "$(dirname "$0")"/..

SWIFT_INC_SRC=$SWIFT_SRC/include/swift
SWIFT_SHIMS_SRC=$SWIFT_SRC/stdlib/public/SwiftShims/swift
LLVM_INC_SRC=$LLVM_SRC/include/llvm


SWIFT_DST=src/third_party/swift
SWIFT_INC_DST=$SWIFT_DST/include/swift
LLVM_DST=src/third_party/llvm
LLVM_INC_DST=$LLVM_DST/include/llvm

rm -rf $LLVM_INC_DST/ADT
rm -rf $LLVM_INC_DST/Support
rm -rf $LLVM_DST/include/llvm-c
rm -rf $SWIFT_DST

mkdir -p $LLVM_INC_DST/ADT
cp "$LLVM_INC_SRC"/ADT/ADL.h $LLVM_INC_DST/ADT
cp "$LLVM_INC_SRC"/ADT/DenseMapInfo.h $LLVM_INC_DST/ADT
cp "$LLVM_INC_SRC"/ADT/Hashing.h $LLVM_INC_DST/ADT
cp "$LLVM_INC_SRC"/ADT/STLExtras.h $LLVM_INC_DST/ADT
cp "$LLVM_INC_SRC"/ADT/STLForwardCompat.h $LLVM_INC_DST/ADT
cp "$LLVM_INC_SRC"/ADT/STLFunctionalExtras.h $LLVM_INC_DST/ADT
cp "$LLVM_INC_SRC"/ADT/StringRef.h $LLVM_INC_DST/ADT
cp "$LLVM_INC_SRC"/ADT/StringSwitch.h $LLVM_INC_DST/ADT
cp "$LLVM_INC_SRC"/ADT/bit.h $LLVM_INC_DST/ADT
cp "$LLVM_INC_SRC"/ADT/iterator.h $LLVM_INC_DST/ADT
cp "$LLVM_INC_SRC"/ADT/iterator_range.h $LLVM_INC_DST/ADT

mkdir -p $LLVM_INC_DST/Support
cp "$LLVM_INC_SRC"/Support/Casting.h $LLVM_INC_DST/Support
cp "$LLVM_INC_SRC"/Support/Compiler.h $LLVM_INC_DST/Support
cp "$LLVM_INC_SRC"/Support/DataTypes.h $LLVM_INC_DST/Support
cp "$LLVM_INC_SRC"/Support/ErrorHandling.h $LLVM_INC_DST/Support
cp "$LLVM_INC_SRC"/Support/SwapByteOrder.h $LLVM_INC_DST/Support
cp "$LLVM_INC_SRC"/Support/type_traits.h $LLVM_INC_DST/Support

mkdir -p $LLVM_DST/include/llvm-c
cp "$LLVM_SRC"/include/llvm-c/DataTypes.h $LLVM_DST/include/llvm-c

mkdir -p $SWIFT_DST
cp "$SWIFT_SRC"/LICENSE.txt $SWIFT_DST

mkdir -p $SWIFT_INC_DST
cp -R "$SWIFT_INC_SRC"/Demangling $SWIFT_INC_DST
cp "$SWIFT_INC_SRC"/Strings.h $SWIFT_INC_DST

mkdir -p $SWIFT_INC_DST/ABI
cp "$SWIFT_INC_SRC"/ABI/InvertibleProtocols.def $SWIFT_INC_DST/ABI

mkdir -p $SWIFT_INC_DST/AST
cp "$SWIFT_INC_SRC"/AST/Ownership.h $SWIFT_INC_DST/AST
cp "$SWIFT_INC_SRC"/AST/ReferenceStorage.def $SWIFT_INC_DST/AST

mkdir -p $SWIFT_INC_DST/Basic
cp "$SWIFT_INC_SRC"/Basic/Assertions.h $SWIFT_INC_DST/Basic
cp "$SWIFT_INC_SRC"/Basic/InlineBitfield.h $SWIFT_INC_DST/Basic
cp "$SWIFT_INC_SRC"/Basic/LLVM.h $SWIFT_INC_DST/Basic
cp "$SWIFT_INC_SRC"/Basic/MacroRoles.def $SWIFT_INC_DST/Basic
cp "$SWIFT_INC_SRC"/Basic/STLExtras.h $SWIFT_INC_DST/Basic

mkdir -p $SWIFT_DST/lib
cp -R "$SWIFT_SRC"/lib/Demangling $SWIFT_DST/lib
rm -f $SWIFT_DST/lib/Demangling/CMakeLists.txt

# Additional shared LLVM headers pulled in by newer Swift.
cp "$LLVM_INC_SRC"/ADT/PointerIntPair.h $LLVM_INC_DST/ADT
cp "$LLVM_INC_SRC"/ADT/SmallVector.h $LLVM_INC_DST/ADT
cp "$LLVM_INC_SRC"/Support/MathExtras.h $LLVM_INC_DST/Support
cp "$LLVM_INC_SRC"/Support/PointerLikeTypeTraits.h $LLVM_INC_DST/Support
cp "$LLVM_INC_SRC"/Support/xxhash.h $LLVM_INC_DST/Support

# swift/shims/* lives outside include/ in the swift tree.
mkdir -p $SWIFT_INC_DST/shims
cp "$SWIFT_SHIMS_SRC"/shims/Visibility.h $SWIFT_INC_DST/shims
