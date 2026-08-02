// This file is part of PIQP.
//
// Copyright (c) 2025 EPFL
//
// This source code is licensed under the BSD 2-Clause License found in the
// LICENSE file in the root directory of this source tree.

#include "piqp/kkt_system.hpp"
#include "piqp/kkt_system.tpp"

namespace piqp
{

template class KKTSystem<common::Scalar, common::StorageIndex, PIQP_DENSE>;
template class KKTSystem<common::Scalar, common::StorageIndex, PIQP_SPARSE>;

} // namespace piqp
