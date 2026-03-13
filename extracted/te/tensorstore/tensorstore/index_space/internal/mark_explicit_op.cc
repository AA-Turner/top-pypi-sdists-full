// Copyright 2020 The TensorStore Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "tensorstore/index_space/internal/mark_explicit_op.h"

#include <utility>

#include "absl/status/status.h"
#include "absl/strings/str_format.h"
#include "tensorstore/container_kind.h"
#include "tensorstore/index.h"
#include "tensorstore/index_space/dimension_index_buffer.h"
#include "tensorstore/index_space/index_transform.h"
#include "tensorstore/index_space/internal/transform_rep.h"
#include "tensorstore/index_space/output_index_method.h"
#include "tensorstore/util/result.h"

namespace tensorstore {
namespace internal_index_space {

Result<IndexTransform<>> ApplyChangeImplicitState(
    IndexTransform<> transform, DimensionIndexBuffer* dimensions, bool implicit,
    bool lower, bool upper, bool domain_only) {
  if (!lower && !upper) {
    return transform;
  }
  TransformRep::Ptr<> rep = MutableRep(
      TransformAccess::rep_ptr<container>(std::move(transform)), domain_only);
  if (implicit) {
    // Verify that there are no index array maps that are indexed by a dimension
    // in `*dimensions`.
    for (DimensionIndex output_dim = 0, output_rank = rep->output_rank;
         output_dim < output_rank; ++output_dim) {
      auto& map = rep->output_index_maps()[output_dim];
      if (map.method() != OutputIndexMethod::array) continue;
      auto& index_array_data = map.index_array_data();
      for (DimensionIndex input_dim : *dimensions) {
        if (index_array_data.byte_strides[input_dim] != 0) {
          return absl::InvalidArgumentError(absl::StrFormat(
              "Cannot mark input dimension %d as having implicit bounds "
              "because it indexes the index array "
              "map for output dimension %d",
              input_dim, output_dim));
        }
      }
    }
  }
  for (DimensionIndex input_dim : *dimensions) {
    const auto d = rep->input_dimension(input_dim);
    if (lower) d.implicit_lower_bound() = implicit;
    if (upper) d.implicit_upper_bound() = implicit;
  }
  if (!implicit && IsDomainExplicitlyEmpty(rep.get())) {
    ReplaceAllIndexArrayMapsWithConstantMaps(rep.get());
  }
  internal_index_space::DebugCheckInvariants(rep.get());
  return TransformAccess::Make<IndexTransform<>>(std::move(rep));
}

}  // namespace internal_index_space
}  // namespace tensorstore
