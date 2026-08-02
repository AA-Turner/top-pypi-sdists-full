set -e -x
cd /clang
cd llvm-project-llvmorg-20.1.5/llvm
mkdir .build
cd .build
cmake -DLLVM_ENABLE_PROJECTS="clang" -DCMAKE_BUILD_TYPE=Release ..
make -j 4 install
