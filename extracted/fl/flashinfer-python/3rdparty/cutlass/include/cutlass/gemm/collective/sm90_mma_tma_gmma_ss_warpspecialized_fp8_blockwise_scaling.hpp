/***************************************************************************************************
 * Copyright (c) 2023 - 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
 * SPDX-License-Identifier: BSD-3-Clause
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 **************************************************************************************************/

#pragma once

#include "cutlass/cutlass.h"
#include "cutlass/gemm/dispatch_policy.hpp"
#include "cutlass/trace.h"
#include "cutlass/numeric_types.h"

#include "cute/arch/cluster_sm90.hpp"
#include "cute/arch/copy_sm80.hpp"
#include "cute/arch/copy_sm90.hpp"
#include "cute/algorithm/functional.hpp"
#include "cute/atom/mma_atom.hpp"
#include "cute/algorithm/gemm.hpp"
#include "cute/tensor_predicate.hpp"
#include "cute/numeric/arithmetic_tuple.hpp"

/////////////////////////////////////////////////////////////////////////////////////////////////

namespace cutlass::gemm::collective {
using namespace cute;

/////////////////////////////////////////////////////////////////////////////////////////////////

// WarpSpecialized Mainloop
template <
  int Stages,
  class ClusterShape,
  class KernelSchedule,
  int ScaleGranularityM_,
  int ScaleGranularityN_,
  int ScalePromotionInterval_,
  class TileShape_,
  class ElementA_,
  class StrideA_,
  class ElementB_,
  class StrideB_,
  class TiledMma_,
  class GmemTiledCopyA_,
  class SmemLayoutAtomA_,
  class SmemCopyAtomA_,
  class TransformA_,
  class GmemTiledCopyB_,
  class SmemLayoutAtomB_,
  class SmemCopyAtomB_,
  class TransformB_>
struct CollectiveMma<
    MainloopSm90TmaGmmaWarpSpecializedBlockScalingFP8<Stages, ClusterShape, KernelSchedule, ScaleGranularityM_, ScaleGranularityN_, ScalePromotionInterval_>,
    TileShape_,
    ElementA_,
    StrideA_,
    ElementB_,
    StrideB_,
    TiledMma_,
    GmemTiledCopyA_,
    SmemLayoutAtomA_,
    SmemCopyAtomA_,
    TransformA_,
    GmemTiledCopyB_,
    SmemLayoutAtomB_,
    SmemCopyAtomB_,
    TransformB_>
{
  //
  // Type Aliases
  //
  using DispatchPolicy = MainloopSm90TmaGmmaWarpSpecializedBlockScalingFP8<Stages, ClusterShape, KernelSchedule, ScaleGranularityM_, ScaleGranularityN_, ScalePromotionInterval_>;
  using TileShape = TileShape_;
  using ElementA = ElementA_;
  using StrideA = StrideA_;
  using ElementB = ElementB_;
  using StrideB = StrideB_;
  using TiledMma = TiledMma_;
  using ElementAccumulator = typename TiledMma::ValTypeC;
  using ElementBlockScale = ElementAccumulator;
  using GmemTiledCopyA = GmemTiledCopyA_;
  using GmemTiledCopyB = GmemTiledCopyB_;
  using SmemLayoutAtomA = SmemLayoutAtomA_;
  using SmemLayoutAtomB = SmemLayoutAtomB_;
  using SmemCopyAtomA = SmemCopyAtomA_;
  using SmemCopyAtomB = SmemCopyAtomB_;
  using TransformA = TransformA_;
  using TransformB = TransformB_;
  using ArchTag = typename DispatchPolicy::ArchTag;

  using CtaShape_MNK = decltype(shape_div(TileShape{}, ClusterShape{}));
  using MainloopPipeline = cutlass::PipelineTmaAsync<DispatchPolicy::Stages>;
  using PipelineState = cutlass::PipelineState<DispatchPolicy::Stages>;
  using PipelineParams = typename MainloopPipeline::Params;

  // Two threads per CTA are producers (1 for operand tile `tma`, and 32 for scales `cp.async`)
  static constexpr int NumProducerThreadEvents = 33;

  static constexpr int ScaleGranularityM = ScaleGranularityM_ == 0 ? size<0>(TileShape{}) : ScaleGranularityM_;
  static constexpr int ScaleGranularityN = ScaleGranularityN_ == 0 ? size<1>(TileShape{}) : ScaleGranularityN_;
  static constexpr int ScalePromotionInterval = ScalePromotionInterval_;
  static_assert(ScalePromotionInterval % 4 == 0, "ScalePromotionInterval must be a multiple of 4.");
  static constexpr int ScaleMsPerTile = size<0>(TileShape{}) / ScaleGranularityM;
  static constexpr int ScaleNsPerTile = size<1>(TileShape{}) / ScaleGranularityN;

  static_assert(cute::rank(SmemLayoutAtomA{}) == 2, "SmemLayoutAtom must be rank 2 (M/N, K)");
  static_assert((size<0>(TileShape{}) % size<0>(SmemLayoutAtomA{})) == 0, "SmemLayoutAtom must evenly divide tile shape.");
  static_assert((size<2>(TileShape{}) % size<1>(SmemLayoutAtomA{})) == 0, "SmemLayoutAtom must evenly divide tile shape.");

  static_assert(cute::rank(SmemLayoutAtomB{}) == 2, "SmemLayoutAtom must be rank 2 (M/N, K)");
  static_assert((size<1>(TileShape{}) % size<0>(SmemLayoutAtomB{})) == 0, "SmemLayoutAtom must evenly divide tile shape.");
  static_assert((size<2>(TileShape{}) % size<1>(SmemLayoutAtomB{})) == 0, "SmemLayoutAtom must evenly divide tile shape.");

  static_assert((size<0>(TileShape{}) % ScaleGranularityM) == 0, "FP8 scaling granularity must evenly divide tile shape along M.");
  static_assert((size<1>(TileShape{}) % ScaleGranularityN) == 0, "FP8 scaling granularity must evenly divide tile shape along N.");

  // Tile along modes in a way that maximizes the TMA box size.
  using SmemLayoutA = decltype(tile_to_shape(
      SmemLayoutAtomA{},
      make_shape(shape<0>(TileShape{}), shape<2>(TileShape{}), Int<DispatchPolicy::Stages>{}),
      cute::conditional_t< ::cutlass::gemm::detail::is_major<0,StrideA>(), Step<_2,_1,_3>, Step<_1,_2,_3>>{}));
  using SmemLayoutB = decltype(tile_to_shape(
      SmemLayoutAtomB{},
      make_shape(shape<1>(TileShape{}), shape<2>(TileShape{}), Int<DispatchPolicy::Stages>{}),
      cute::conditional_t< ::cutlass::gemm::detail::is_major<0,StrideB>(), Step<_2,_1,_3>, Step<_1,_2,_3>>{}));

  // Block scaling gmem-to-smem copy atom 
  //  we can have partial tiles in M or N, so don't vectorize those loads
  using SmemBlockScalingCopyAtomA = Copy_Atom<SM80_CP_ASYNC_CACHEALWAYS<ElementBlockScale>, ElementBlockScale>;
  using SmemBlockScalingCopyAtomB = Copy_Atom<SM80_CP_ASYNC_CACHEALWAYS<ElementBlockScale>, ElementBlockScale>;

  // Block scaling smem layout
  using SmemLayoutScaleA = Layout<Shape<Int<ScaleMsPerTile>, Int<DispatchPolicy::Stages>>>;
  using SmemLayoutScaleB = Layout<Shape<Int<ScaleNsPerTile>, Int<DispatchPolicy::Stages>>>;

  static_assert(DispatchPolicy::Stages >= 2, "Specialization requires Stages set to value 1 or more.");
  static_assert(cute::is_base_of<cute::GMMA::DescriptorIterator, typename TiledMma::FrgTypeA>::value &&
                cute::is_base_of<cute::GMMA::DescriptorIterator, typename TiledMma::FrgTypeB>::value,
                "MMA atom must source both A and B operand from smem_desc for this mainloop.");
  static_assert(cute::is_same_v<GmemTiledCopyA, SM90_TMA_LOAD> || cute::is_same_v<GmemTiledCopyA, SM90_TMA_LOAD_MULTICAST>,
      "GmemTiledCopy - invalid SM90 TMA copy atom specified.");
  static_assert(cute::is_same_v<GmemTiledCopyB, SM90_TMA_LOAD> || cute::is_same_v<GmemTiledCopyB, SM90_TMA_LOAD_MULTICAST>,
      "GmemTiledCopy - invalid SM90 TMA copy atom specified.");
  static_assert(cute::is_same_v<ElementAccumulator, ElementBlockScale>,
             "ElementAccumulator and ElementBlockScale should be same datatype");

  struct SharedStorage
  {
    struct TensorStorage : cute::aligned_struct<128> {
      cute::array_aligned<typename TiledMma::ValTypeA, cute::cosize_v<SmemLayoutA>> smem_A;  // mxk
      cute::array_aligned<typename TiledMma::ValTypeB, cute::cosize_v<SmemLayoutB>> smem_B;  // nxk
      cute::array_aligned<ElementBlockScale, cute::cosize_v<SmemLayoutScaleA>> smem_scale_A; // ScaleMsPerTile x k
      cute::array_aligned<ElementBlockScale, cute::cosize_v<SmemLayoutScaleB>> smem_scale_B; // ScaleNsPerTile x k
    } tensors;

    using PipelineStorage = typename MainloopPipeline::SharedStorage;
    PipelineStorage pipeline;
  };
  using TensorStorage = typename SharedStorage::TensorStorage;
  using PipelineStorage = typename SharedStorage::PipelineStorage;

  // Host side kernel arguments
  struct Arguments {
    ElementA const* ptr_A;
    StrideA dA;
    ElementB const* ptr_B;
    StrideB dB;
    uint32_t mma_promotion_interval = 4;
    ElementBlockScale const* ptr_scale_A; 
    ElementBlockScale const* ptr_scale_B;
  };

  // Device side kernel params
  struct Params {
    // Assumption: StrideA is congruent with Problem_MK
    using TMA_A = decltype(make_tma_copy_A_sm90(
        GmemTiledCopyA{},
        make_tensor(static_cast<ElementA const*>(nullptr), repeat_like(StrideA{}, int32_t(0)), StrideA{}),
        SmemLayoutA{}(_,_,0),
        TileShape{},
        ClusterShape{}));
    // Assumption: StrideB is congruent with Problem_NK
    using TMA_B = decltype(make_tma_copy_B_sm90(
        GmemTiledCopyB{},
        make_tensor(static_cast<ElementB const*>(nullptr), repeat_like(StrideB{}, int32_t(0)), StrideB{}),
        SmemLayoutB{}(_,_,0),
        TileShape{},
        ClusterShape{}));
    TMA_A tma_load_a;
    TMA_B tma_load_b;
    uint32_t tma_transaction_bytes = TmaTransactionBytes;
    uint32_t tma_transaction_bytes_mk = TmaTransactionBytesMK;
    uint32_t tma_transaction_bytes_nk = TmaTransactionBytesNK;
    // Block scaling factors for A and B
    ElementBlockScale const* ptr_scale_A; 
    ElementBlockScale const* ptr_scale_B;
  };

  //
  // Methods
  //

  template <class ProblemShape>
  static constexpr Params
  to_underlying_arguments(ProblemShape const& problem_shape, Arguments const& args, void* workspace) {
    (void) workspace;

    // Optionally append 1s until problem shape is rank-4 (MNKL), in case it is only rank-3 (MNK)
    auto problem_shape_MNKL = append<4>(problem_shape, 1);
    auto [M,N,K,L] = problem_shape_MNKL;

    auto ptr_A = reinterpret_cast<ElementA const*>(args.ptr_A);
    auto ptr_B = reinterpret_cast<ElementB const*>(args.ptr_B);

    Tensor tensor_a = make_tensor(ptr_A, make_layout(make_shape(M,K,L), args.dA));
    Tensor tensor_b = make_tensor(ptr_B, make_layout(make_shape(N,K,L), args.dB));
    typename Params::TMA_A tma_load_a = make_tma_copy_A_sm90(
        GmemTiledCopyA{},
        tensor_a,
        SmemLayoutA{}(_,_,cute::Int<0>{}),
        TileShape{},
        ClusterShape{});
    typename Params::TMA_B tma_load_b = make_tma_copy_B_sm90(
        GmemTiledCopyB{},
        tensor_b,
        SmemLayoutB{}(_,_,cute::Int<0>{}),
        TileShape{},
        ClusterShape{});
    uint32_t transaction_bytes_mk = TmaTransactionBytesMK;
    uint32_t transaction_bytes_nk = TmaTransactionBytesNK;
    uint32_t transaction_bytes = transaction_bytes_mk + transaction_bytes_nk;

    return {
      tma_load_a,
      tma_load_b,
      transaction_bytes,
      transaction_bytes_mk,
      transaction_bytes_nk,
      args.ptr_scale_A,
      args.ptr_scale_B
    };
  }

  template<class ProblemShape>
  static bool
  can_implement(
      ProblemShape const& problem_shape,
      [[maybe_unused]] Arguments const& args) {
    constexpr int tma_alignment_bits = 128;
    auto problem_shape_MNKL = append<4>(problem_shape, 1);
    auto [M,N,K,L] = problem_shape_MNKL;

    bool implementable = true;
    constexpr int min_tma_aligned_elements_A = tma_alignment_bits / cutlass::sizeof_bits<ElementA>::value;
    implementable = implementable && cutlass::detail::check_alignment<min_tma_aligned_elements_A>(cute::make_shape(M,K,L), StrideA{});
    constexpr int min_tma_aligned_elements_B = tma_alignment_bits / cutlass::sizeof_bits<ElementB>::value;
    implementable = implementable && cutlass::detail::check_alignment<min_tma_aligned_elements_B>(cute::make_shape(N,K,L), StrideB{});

    /* MMA promotion interval should be a multiple of 4, since each mainloop iteration would issue 4 MMA instructions. */
    constexpr int pipe_k = size<2>(TileShape{}) / tile_size<2>(TiledMma{});
    implementable = implementable && (args.mma_promotion_interval % 4 == 0) && (args.mma_promotion_interval == ScalePromotionInterval);
    implementable = implementable && (pipe_k % 4 == 0) && (pipe_k <= args.mma_promotion_interval);

    // We expect full tiles in K
    implementable = implementable && (K % size<2>(TileShape{}) == 0);

    if (!implementable) {
      CUTLASS_TRACE_HOST("  CAN IMPLEMENT: Problem Size doesn't meet the minimum alignment requirements for TMA.\n");
    }
    return implementable;
  }

  static constexpr int K_PIPE_MAX = DispatchPolicy::Stages;
  static constexpr int K_PIPE_MMAS = 1;
  static constexpr uint32_t TmaTransactionBytesMK =
        cutlass::bits_to_bytes(size<0>(SmemLayoutA{}) * size<1>(SmemLayoutA{}) * static_cast<uint32_t>(sizeof_bits<ElementA>::value));
  static constexpr uint32_t TmaTransactionBytesNK =
        cutlass::bits_to_bytes(size<0>(SmemLayoutB{}) * size<1>(SmemLayoutB{}) * static_cast<uint32_t>(sizeof_bits<ElementB>::value));
  static constexpr uint32_t TmaTransactionBytes = TmaTransactionBytesMK + TmaTransactionBytesNK;

  /// Issue Tma Descriptor Prefetch -- ideally from a single thread for best performance
  CUTLASS_DEVICE
  static void prefetch_tma_descriptors(Params const& mainloop_params)
  {
    cute::prefetch_tma_descriptor(mainloop_params.tma_load_a.get_tma_descriptor());
    cute::prefetch_tma_descriptor(mainloop_params.tma_load_b.get_tma_descriptor());
  }

  /// Set up the data needed by this collective for load and mma.
  /// Returns a tuple of tensors. The collective and the kernel layer have the contract
  /// Returned tuple must contain at least two elements, with the first two elements being:
  /// gA_mkl - The tma tensor, A after a local tile so it has shape  (BLK_M,BLK_K,m,k,l)
  /// gB_nkl - The tma tensor, B after a local tile so it has shape  (BLK_N,BLK_K,n,k,l)
  template <class ProblemShape_MNKL>
  CUTLASS_DEVICE auto
  load_init(ProblemShape_MNKL const& problem_shape_MNKL, Params const& mainloop_params) const {
    using X = Underscore;
    // Separate out problem shape for convenience
    auto [M,N,K,L] = problem_shape_MNKL;

    // TMA requires special handling of strides to deal with coord codomain mapping
    // Represent the full tensors -- get these from TMA
    Tensor mA_mkl = mainloop_params.tma_load_a.get_tma_tensor(make_shape(M,K,L));                            // (m,k,l)
    Tensor mB_nkl = mainloop_params.tma_load_b.get_tma_tensor(make_shape(N,K,L));                            // (n,k,l)

    // Make tiled views, defer the slice
    Tensor gA_mkl = local_tile(mA_mkl, TileShape{}, make_coord(_,_,_), Step<_1, X,_1>{});        // (BLK_M,BLK_K,m,k,l)
    Tensor gB_nkl = local_tile(mB_nkl, TileShape{}, make_coord(_,_,_), Step< X,_1,_1>{});        // (BLK_N,BLK_K,n,k,l)

    auto tK = get<3>(gA_mkl.shape());

    // Make the tiled views of scale tensors
    auto scaleA_shape = make_shape(ceil_div(M, ScaleGranularityM), tK, L); // (scale_m,k,l)
    auto scaleA_layout = make_ordered_layout(scaleA_shape, Step<_0, _1, _2>{});
    auto scaleB_shape = make_shape(ceil_div(N, ScaleGranularityN), tK, L); // (scale_n,k,l)
    auto scaleB_layout = make_ordered_layout(scaleB_shape, Step<_0, _1, _2>{});

    // Note that mScaleA_mkl and mScaleB_nkl are already blocked tiled in the `m` host and
    // gScaleA_mkl and gScaleB_nkl in `g` global memory are same as mScaleA_mkl and mScaleB_nkl.
    Tensor mScaleA_mkl = make_tensor(make_gmem_ptr(mainloop_params.ptr_scale_A), scaleA_layout); // (scale_m,k,l)
    Tensor mScaleB_nkl = make_tensor(make_gmem_ptr(mainloop_params.ptr_scale_B), scaleB_layout); // (scale_n,k,l)

    return cute::make_tuple(gA_mkl, gB_nkl, mScaleA_mkl, mScaleB_nkl);
  }

  /// Perform a collective-scoped matrix multiply-accumulate
  /// Producer Perspective
  template <
    class TensorA, class TensorB,
    class TensorScaleA, class TensorScaleB,
    class KTileIterator, class BlockCoord
  >
  CUTLASS_DEVICE void
  load(
      Params const& mainloop_params,
      MainloopPipeline pipeline,
      PipelineState smem_pipe_write,
      cute::tuple<TensorA, TensorB, TensorScaleA, TensorScaleB> const& load_inputs,
      BlockCoord const& blk_coord,
      KTileIterator k_tile_iter, int k_tile_count,
      int thread_idx,
      uint32_t block_rank_in_cluster,
      TensorStorage& shared_tensors) {
    int lane_predicate = cute::elect_one_sync();
    // Blockscaling: Tma loads for load_input and CpAsync for load_scale
    Tensor sA = make_tensor(make_smem_ptr(shared_tensors.smem_A.data()), SmemLayoutA{});        // (BLK_M,BLK_K,PIPE)
    Tensor sB = make_tensor(make_smem_ptr(shared_tensors.smem_B.data()), SmemLayoutB{});        // (BLK_N,BLK_K,PIPE)
    Tensor sScaleA = make_tensor(cute::make_smem_ptr(shared_tensors.smem_scale_A.data()), SmemLayoutScaleA{}); // (ScaleMsPerTile,k)
    Tensor sScaleB = make_tensor(cute::make_smem_ptr(shared_tensors.smem_scale_B.data()), SmemLayoutScaleB{}); // (ScaleNsPerTile,k)

    //
    // Prepare the TMA loads for A and B
    //

    constexpr uint32_t cluster_shape_x = get<0>(ClusterShape());
    uint2 cluster_local_block_id = {block_rank_in_cluster % cluster_shape_x, block_rank_in_cluster / cluster_shape_x};

    Tensor gA_mkl = get<0>(load_inputs);
    Tensor gB_nkl = get<1>(load_inputs);

    auto block_tma_a = mainloop_params.tma_load_a.get_slice(cluster_local_block_id.y);
    auto block_tma_b = mainloop_params.tma_load_b.get_slice(cluster_local_block_id.x);

    // Partition the inputs based on the current block coordinates.
    auto [m_coord, n_coord, k_coord, l_coord] = blk_coord;
    Tensor gA = gA_mkl(_,_,m_coord,_,l_coord);                                                     // (BLK_M,BLK_K,k)
    Tensor gB = gB_nkl(_,_,n_coord,_,l_coord);                                                     // (BLK_N,BLK_K,k)


    // Block scaling: load_scale has scaling tensors in global memory which are not tiled
    Tensor mScaleA_mkl = get<2>(load_inputs);
    Tensor mScaleB_nkl = get<3>(load_inputs);
    auto scales_m = get<0>(mScaleA_mkl.shape());
    auto scales_n = get<0>(mScaleB_nkl.shape());

    Tensor cScaleA_mkl = make_identity_tensor(mScaleA_mkl.shape());
    Tensor cScaleB_nkl = make_identity_tensor(mScaleB_nkl.shape());

    Tensor gScaleA = local_tile(
      mScaleA_mkl, make_tile(Int<ScaleMsPerTile>{}),
      make_coord(m_coord,_,l_coord));                   // (ScaleMsPerTile,k,1)
    Tensor cScaleA = local_tile(
      cScaleA_mkl, make_tile(Int<ScaleMsPerTile>{}),
      make_coord(m_coord,_,l_coord));
    Tensor gScaleB = local_tile(
      mScaleB_nkl, make_tile(Int<ScaleNsPerTile>{}),
      make_coord(n_coord,_,l_coord));                   // (ScaleNsPerTile,k,1)
    Tensor cScaleB = local_tile(
      cScaleB_nkl, make_tile(Int<ScaleNsPerTile>{}),
      make_coord(n_coord,_,l_coord));

    TiledCopy scale_copy_a = make_tiled_copy(SmemBlockScalingCopyAtomA{},
      Layout<Shape<_32>>{}, Layout<Shape<_1>>{});
    TiledCopy scale_copy_b = make_tiled_copy(SmemBlockScalingCopyAtomB{}, 
      Layout<Shape<_32>>{}, Layout<Shape<_1>>{});
    ThrCopy thr_scale_copy_a = scale_copy_a.get_slice(threadIdx.x);
    ThrCopy thr_scale_copy_b = scale_copy_b.get_slice(threadIdx.x);

    Tensor tAgA_ScaleA = thr_scale_copy_a.partition_S(gScaleA);
    Tensor tAcA_ScaleA = thr_scale_copy_a.partition_S(cScaleA);
    Tensor tAsA_ScaleA = thr_scale_copy_a.partition_D(sScaleA);

    Tensor tBgB_ScaleB = thr_scale_copy_b.partition_S(gScaleB);
    Tensor tBcB_ScaleB = thr_scale_copy_b.partition_S(cScaleB);
    Tensor tBsB_ScaleB = thr_scale_copy_b.partition_D(sScaleB);

    // Applies the mapping from block_tma_a
    Tensor tAgA = block_tma_a.partition_S(gA);                                              // (TMA,TMA_M,TMA_K,k)
    Tensor tAsA = block_tma_a.partition_D(sA);                                              // (TMA,TMA_M,TMA_K,PIPE)

    Tensor tBgB = block_tma_b.partition_S(gB);                                              // (TMA,TMA_N,TMA_K,k)
    Tensor tBsB = block_tma_b.partition_D(sB);                                              // (TMA,TMA_N,TMA_K,PIPE)

    Tensor tApA_ScaleA = make_tensor<bool>(shape(tAsA_ScaleA(_,_,0)));
    Tensor tBpB_ScaleB = make_tensor<bool>(shape(tBsB_ScaleB(_,_,0)));

    #pragma unroll
    for (int i = 0; i < size(tApA_ScaleA); ++i) {
      tApA_ScaleA(i) = get<0>(tAcA_ScaleA(i)) <
        std::min(scales_m, (m_coord + 1) * ScaleMsPerTile);
    }

    #pragma unroll
    for (int i = 0; i < size(tBpB_ScaleB); ++i) {
      tBpB_ScaleB(i) = get<0>(tBcB_ScaleB(i)) <
        std::min(scales_n, (n_coord + 1) * ScaleNsPerTile);
    }

    uint16_t mcast_mask_a = 0;
    uint16_t mcast_mask_b = 0;

    // Issue TmaLoads for GEMM operands A/B and CpAsync for scale tensors
    // Maps the tile -> block, value
    if constexpr (cute::is_same_v<GmemTiledCopyA, SM90_TMA_LOAD_MULTICAST>) {
      auto block_layout = Layout<typename DispatchPolicy::ClusterShape>{};                       // (m,n) -> block_id
      for (int n = 0; n < size<1>(block_layout); ++n) {
        mcast_mask_a |= (uint16_t(1) << block_layout(cluster_local_block_id.x,n,Int<0>{}));
      }
    }

    if constexpr (cute::is_same_v<GmemTiledCopyB, SM90_TMA_LOAD_MULTICAST>) {
      auto block_layout = Layout<typename DispatchPolicy::ClusterShape>{};                       // (m,n) -> block_id
      for (int m = 0; m < size<0>(block_layout); ++m) {
        mcast_mask_b |= (uint16_t(1) << block_layout(m,cluster_local_block_id.y,Int<0>{}));
      }
    }

    // Mainloop
    CUTLASS_PRAGMA_NO_UNROLL
    for ( ; k_tile_count > 0; --k_tile_count) {
      // LOCK smem_pipe_write for _writing_
      pipeline.producer_acquire(smem_pipe_write);

      //
      // Copy gmem to smem for *k_tile_iter
      //
      int write_stage = smem_pipe_write.index();
      using BarrierType = typename MainloopPipeline::ProducerBarrierType;
      BarrierType* tma_barrier = pipeline.producer_get_barrier(smem_pipe_write);

      // Copy operands A and B from global memory to shared memory
      if (lane_predicate) copy(mainloop_params.tma_load_a.with(*tma_barrier, mcast_mask_a), tAgA(_,_,_,*k_tile_iter), tAsA(_,_,_,write_stage));
      if (lane_predicate) copy(mainloop_params.tma_load_b.with(*tma_barrier, mcast_mask_b), tBgB(_,_,_,*k_tile_iter), tBsB(_,_,_,write_stage));

      // Copy scale tensors from global memory to shared memory
      copy_if(scale_copy_a, tApA_ScaleA, tAgA_ScaleA(_,_,*k_tile_iter), tAsA_ScaleA(_,_,write_stage));
      copy_if(scale_copy_b, tBpB_ScaleB, tBgB_ScaleB(_,_,*k_tile_iter), tBsB_ScaleB(_,_,write_stage));
      pipeline.producer_commit(smem_pipe_write, cutlass::arch::cpasync_barrier_arrive_noinc);

      ++k_tile_iter;

      // Advance smem_pipe_write
      ++smem_pipe_write;
    }
  }

  /// Perform a Producer Epilogue to prevent early exit of blocks in a Cluster
  CUTLASS_DEVICE void
  load_tail(
      MainloopPipeline pipeline,
      PipelineState smem_pipe_write) {
    int lane_predicate = cute::elect_one_sync();

    // Issue the epilogue waits
    if (lane_predicate) {
      /* This helps avoid early exit of blocks in Cluster
       * Waits for all stages to either be released (all
       * Consumer UNLOCKs), or if the stage was never used
       * then would just be acquired since the phase was
       * still inverted from make_producer_start_state
       */
      pipeline.producer_tail(smem_pipe_write);
    }
  }

  template<
    class EngineAccum,
    class LayoutAccum,
    class ScaleFactor
  >
  CUTLASS_DEVICE
  void scale_if_needed(GmmaFP8Accumulation<EngineAccum, LayoutAccum>& accumulation, ScaleFactor scaleFactor) {
    if constexpr (ScalePromotionInterval != 4) {
      accumulation.scale_if_needed(scaleFactor);
    }
    else {
      // avoid unnecessary tests when granularity is the finnest
      accumulation.scale(scaleFactor);
    }
  }
  template<
    class EngineAccum,
    class LayoutAccum,
    class ScaleFactor1,
    class ScaleFactor2
  >
  CUTLASS_DEVICE
  void scale_if_needed(GmmaFP8Accumulation<EngineAccum, LayoutAccum>& accumulation, ScaleFactor1 scaleFactor1, ScaleFactor2 scaleFactor2) {
    if constexpr (ScalePromotionInterval != 4) {
      accumulation.scale_if_needed(scaleFactor1, scaleFactor2);
    }
    else {
      // avoid unnecessary tests when granularity is the finnest
      accumulation.scale(scaleFactor1, scaleFactor2);
    }
  }

  /// Perform a collective-scoped matrix multiply-accumulate
  /// Consumer Perspective
  template <
    class FrgTensorC
  >
  CUTLASS_DEVICE void
  mma(MainloopPipeline pipeline,
      PipelineState smem_pipe_read,
      FrgTensorC& accum,
      int k_tile_count,
      int thread_idx,
      TensorStorage& shared_tensors,
      Params const& mainloop_params) {


    static_assert(is_rmem<FrgTensorC>::value, "C tensor must be rmem resident.");
    static_assert(cute::rank(SmemLayoutA{}) == 3, "Smem layout must be rank 3.");
    static_assert(cute::rank(SmemLayoutB{}) == 3, "Smem layout must be rank 3.");
    static_assert(cute::is_void_v<SmemCopyAtomA>,
      "SM90 GMMA mainloops cannot have a non-void copy atom for smem sourced instructions.");
    static_assert(cute::is_void_v<SmemCopyAtomB>,
      "SM90 GMMA mainloops cannot have a non-void copy atom for smem sourced instructions.");

    Tensor sA = make_tensor(make_smem_ptr(shared_tensors.smem_A.data()), SmemLayoutA{});          // (BLK_M,BLK_K,PIPE)
    Tensor sB = make_tensor(make_smem_ptr(shared_tensors.smem_B.data()), SmemLayoutB{});          // (BLK_N,BLK_K,PIPE)

    // Block scaling
    Tensor sScaleAViewAsC = make_tensor(cute::make_smem_ptr(shared_tensors.smem_scale_A.data()),
      Layout<
        Shape<Shape<Int<ScaleGranularityM>, Int<ScaleMsPerTile>>, cute::tuple_element_t<1, TileShape>, Int<DispatchPolicy::Stages>>,
        Stride<Stride<_0, _1>, _0, Int<ScaleMsPerTile>>
      >{}); // ((ScaleGranularityM,ScaleMsPerTile),n,k)
    Tensor sScaleBViewAsC = make_tensor(cute::make_smem_ptr(shared_tensors.smem_scale_B.data()),
      Layout<
        Shape<cute::tuple_element_t<0, TileShape>, Shape<Int<ScaleGranularityN>, Int<ScaleNsPerTile>>, Int<DispatchPolicy::Stages>>,
        Stride<_0, Stride<_0, _1>, Int<ScaleNsPerTile>>
      >{}); // (m,(ScaleGranularityN,ScaleNsPerTile),k)

    //
    // Define C accumulators and A/B partitioning
    //

    // Layout of warp group to thread mapping

    static_assert(stride<0>(typename TiledMma::ALayout{}) == 0 and 
                  stride<0>(typename TiledMma::BLayout{}) == 0 and
                  size<0>(typename TiledMma::ALayout{}) == NumThreadsPerWarpGroup and
                  size<0>(typename TiledMma::BLayout{}) == NumThreadsPerWarpGroup, 
                  "Stride of the first mode must be 0 and the size of the mode must be NumThreadsPerWarpGroup");

    constexpr int MmaWarpGroups = size(TiledMma{}) / NumThreadsPerWarpGroup;
    Layout warp_group_thread_layout = make_layout(Int<MmaWarpGroups>{}, 
                                                  Int<NumThreadsPerWarpGroup>{});

    int warp_group_idx = __shfl_sync(0xFFFFFFFF, thread_idx / NumThreadsPerWarpGroup, 0);

    TiledMma tiled_mma;
    auto thread_mma = tiled_mma.get_slice(warp_group_thread_layout(warp_group_idx));

    Tensor tCsScaleAViewAsC = tiled_mma.get_slice(thread_idx).partition_C(sScaleAViewAsC);    // (MMA,MMA_M,MMA_N,PIPE), `thread_mma` above is correct when partitioning A and B, but it is not correct when partitioning C.
    Tensor tCsScaleBViewAsC = tiled_mma.get_slice(thread_idx).partition_C(sScaleBViewAsC);    // (MMA,MMA_M,MMA_N,PIPE), `thread_mma` above is correct when partitioning A and B, but it is not correct when partitioning C.

    Tensor tCsA = thread_mma.partition_A(sA);                                                 // (MMA,MMA_M,MMA_K,PIPE)
    Tensor tCsB = thread_mma.partition_B(sB);                                                 // (MMA,MMA_N,MMA_K,PIPE)

    // Allocate "fragments/descriptors"
    Tensor tCrA = thread_mma.make_fragment_A(tCsA);                                           // (MMA,MMA_M,MMA_K,PIPE)
    Tensor tCrB = thread_mma.make_fragment_B(tCsB);                                           // (MMA,MMA_N,MMA_K,PIPE)

    CUTE_STATIC_ASSERT_V(size<1>(tCsA) == size<1>(accum));                                                         // M
    CUTE_STATIC_ASSERT_V(size<1>(tCsB) == size<2>(accum));                                                         // N
    CUTE_STATIC_ASSERT_V(size<2>(tCsA) == size<2>(tCsB));                                                          // K
    CUTE_STATIC_ASSERT_V(size<3>(tCsA) == size<3>(tCsB));                                                       // PIPE
    CUTE_STATIC_ASSERT_V(Int<DispatchPolicy::Stages>{} == size<2>(sA));                                         // PIPE
    CUTE_STATIC_ASSERT_V(Int<DispatchPolicy::Stages>{} == size<2>(sB));                                         // PIPE

    //
    // PIPELINED MAIN LOOP
    //
    static_assert((0 <= K_PIPE_MMAS) && (K_PIPE_MMAS <  K_PIPE_MAX),
        "ERROR : Incorrect number of MMAs in flight");

    // We release buffers to producer warps(dma load) with some mmas in flight
    PipelineState smem_pipe_release = smem_pipe_read;

    // Per block scale values for operand A and B
    Tensor tCrScaleAViewAsC = make_tensor_like<ElementBlockScale>(tCsScaleAViewAsC(_, _, _, 0));    // (MMA,MMA_M,MMA_N)
    Tensor tCrScaleBViewAsC = make_tensor_like<ElementBlockScale>(tCsScaleBViewAsC(_, _, _, 0));    // (MMA,MMA_M,MMA_N)

    // Prologue GMMAs
    int prologue_mma_count = min(K_PIPE_MMAS, k_tile_count);

    tiled_mma.accumulate_ = GMMA::ScaleOut::Zero;

    GmmaFP8Accumulation accumulation(accum, ScalePromotionInterval, size<2>(tCrA));
    warpgroup_fence_operand(accumulation());
    CUTLASS_PRAGMA_UNROLL
    for (int k_tile_prologue = prologue_mma_count; k_tile_prologue > 0; --k_tile_prologue)
    {
      // WAIT on smem_pipe_read until its data are available (phase bit flips from rdPhaseBit value)
      auto barrier_token = pipeline.consumer_try_wait(smem_pipe_read);
      pipeline.consumer_wait(smem_pipe_read, barrier_token);

      if constexpr (ScalePromotionInterval != 4) {
        if (accumulation.prepare_if_needed()) {
          tiled_mma.accumulate_ = GMMA::ScaleOut::Zero;
        }
      }
      else {
        // Always zero out the accumulator for finest granularity
        tiled_mma.accumulate_ = GMMA::ScaleOut::Zero;
      }

      int read_stage = smem_pipe_read.index();

      // Load per block scale values from shared memory to registers
      copy(tCsScaleAViewAsC(_, _, _, read_stage), tCrScaleAViewAsC);
      copy(tCsScaleBViewAsC(_, _, _, read_stage), tCrScaleBViewAsC);
      if constexpr (ScaleMsPerTile == 1 && ScaleNsPerTile == 1) {
        tCrScaleAViewAsC.data()[0] = tCrScaleAViewAsC.data()[0] * tCrScaleBViewAsC.data()[0];
      }
      if constexpr (ScaleMsPerTile  > 1 && ScaleNsPerTile == 1) {
        ElementBlockScale scale_b = tCrScaleBViewAsC.data()[0];
        CUTLASS_PRAGMA_UNROLL
        for (int i = 0; i < size(tCrScaleAViewAsC); i++) {
          tCrScaleAViewAsC.data()[i] = tCrScaleAViewAsC.data()[i] * scale_b;
        }
      }
      if constexpr (ScaleMsPerTile == 1 && ScaleNsPerTile  > 1) {
        ElementBlockScale scale_a = tCrScaleAViewAsC.data()[0];
        CUTLASS_PRAGMA_UNROLL
        for (int i = 0; i < size(tCrScaleBViewAsC); i++) {
          tCrScaleBViewAsC.data()[i] = tCrScaleBViewAsC.data()[i] * scale_a;
        }
      }

      warpgroup_arrive();
      // Unroll the K mode manually to set scale D to 1
      CUTLASS_PRAGMA_UNROLL
      for (int k_block = 0; k_block < size<2>(tCrA); ++k_block) {
        // (V,M,K) x (V,N,K) => (V,M,N)
        cute::gemm(tiled_mma, tCrA(_,_,k_block,read_stage), tCrB(_,_,k_block,read_stage), accumulation());
        tiled_mma.accumulate_ = GMMA::ScaleOut::One;
      }
      warpgroup_commit_batch();

      // Block scale the accumulators with reg tensor `tCrScaleAViewAsC` and `tCrScaleBViewAsC`
      if constexpr (ScaleMsPerTile == 1 && ScaleNsPerTile == 1) {
        ElementBlockScale scale_ab = tCrScaleAViewAsC.data()[0];
        scale_if_needed(accumulation, scale_ab);
      }
      if constexpr (ScaleMsPerTile  > 1 && ScaleNsPerTile == 1) {
        scale_if_needed(accumulation, tCrScaleAViewAsC);
      }
      if constexpr (ScaleMsPerTile == 1 && ScaleNsPerTile  > 1) {
        scale_if_needed(accumulation, tCrScaleBViewAsC);
      }
      if constexpr (ScaleMsPerTile  > 1 && ScaleNsPerTile  > 1) {
        scale_if_needed(accumulation, tCrScaleAViewAsC, tCrScaleBViewAsC);
      }

      ++smem_pipe_read;
    }

    warpgroup_fence_operand(accumulation());
    // Mainloop GMMAs
    k_tile_count -= prologue_mma_count;

    CUTLASS_PRAGMA_NO_UNROLL
    for ( ; k_tile_count > 0; --k_tile_count)
    {
      // WAIT on smem_pipe_read until its data are available (phase bit flips from rdPhaseBit value)
      auto barrier_token = pipeline.consumer_try_wait(smem_pipe_read);
      pipeline.consumer_wait(smem_pipe_read, barrier_token);

      //
      // Compute on k_tile
      //

      int read_stage = smem_pipe_read.index();

      // Load per block scale values from shared memory to registers (at most twice per block along M and/or N)
      copy(tCsScaleAViewAsC(_, _, _, read_stage), tCrScaleAViewAsC);
      copy(tCsScaleBViewAsC(_, _, _, read_stage), tCrScaleBViewAsC);
      if constexpr (ScaleMsPerTile == 1 && ScaleNsPerTile == 1) {
        tCrScaleAViewAsC.data()[0] = tCrScaleAViewAsC.data()[0] * tCrScaleBViewAsC.data()[0];
      }
      if constexpr (ScaleMsPerTile  > 1 && ScaleNsPerTile == 1) {
        ElementBlockScale scale_b = tCrScaleBViewAsC.data()[0];
        CUTLASS_PRAGMA_UNROLL
        for (int i = 0; i < size(tCrScaleAViewAsC); i++) {
          tCrScaleAViewAsC.data()[i] = tCrScaleAViewAsC.data()[i] * scale_b;
        }
      }
      if constexpr (ScaleMsPerTile == 1 && ScaleNsPerTile  > 1) {
        ElementBlockScale scale_a = tCrScaleAViewAsC.data()[0];
        CUTLASS_PRAGMA_UNROLL
        for (int i = 0; i < size(tCrScaleBViewAsC); i++) {
          tCrScaleBViewAsC.data()[i] = tCrScaleBViewAsC.data()[i] * scale_a;
        }
      }

      if constexpr (ScalePromotionInterval != 4) {
        if (accumulation.prepare_if_needed()) {
          tiled_mma.accumulate_ = GMMA::ScaleOut::Zero;
        }
      }
      else {
        // Always zero out the accumulator for finest granularity
        tiled_mma.accumulate_ = GMMA::ScaleOut::Zero;
      }

      warpgroup_fence_operand(accumulation());
      warpgroup_arrive();
      // Unroll the K mode manually to set scale D to 1
      CUTLASS_PRAGMA_UNROLL
      for (int k_block = 0; k_block < size<2>(tCrA); ++k_block) {
        // (V,M,K) x (V,N,K) => (V,M,N)
        cute::gemm(tiled_mma, tCrA(_,_,k_block,read_stage), tCrB(_,_,k_block,read_stage), accumulation());
        tiled_mma.accumulate_ = GMMA::ScaleOut::One;
      }
      warpgroup_commit_batch();

      /// Wait on the GMMA barrier for K_PIPE_MMAS (or fewer) outstanding to ensure smem_pipe_write is consumed
      warpgroup_wait<K_PIPE_MMAS>();
      warpgroup_fence_operand(accumulation());

      // Block scale the accumulators with reg tensor `tCrScaleAViewAsC` and `tCrScaleBViewAsC`
      if constexpr (ScaleMsPerTile == 1 && ScaleNsPerTile == 1) {
        ElementBlockScale scale_ab = tCrScaleAViewAsC.data()[0];
        scale_if_needed(accumulation, scale_ab);
      }
      if constexpr (ScaleMsPerTile  > 1 && ScaleNsPerTile == 1) {
        scale_if_needed(accumulation, tCrScaleAViewAsC);
      }
      if constexpr (ScaleMsPerTile == 1 && ScaleNsPerTile  > 1) {
        scale_if_needed(accumulation, tCrScaleBViewAsC);
      }
      if constexpr (ScaleMsPerTile  > 1 && ScaleNsPerTile  > 1) {
        scale_if_needed(accumulation, tCrScaleAViewAsC, tCrScaleBViewAsC);
      }

      pipeline.consumer_release(smem_pipe_release);                 // UNLOCK smem_pipe_release, done _computing_ on it

      // Advance smem_pipe_read and smem_pipe_release
      ++smem_pipe_read;
      ++smem_pipe_release;
    }

    if constexpr (ScalePromotionInterval != 4) {
      // residues only exists when granularity is not the finnest
      if constexpr (ScaleMsPerTile == 1 && ScaleNsPerTile == 1) {
        ElementBlockScale scale_ab = tCrScaleAViewAsC.data()[0];
        accumulation.scale_residue_if_needed(scale_ab);
      }
      if constexpr (ScaleMsPerTile  > 1 && ScaleNsPerTile == 1) {
        accumulation.scale_residue_if_needed(tCrScaleAViewAsC);
      }
      if constexpr (ScaleMsPerTile == 1 && ScaleNsPerTile  > 1) {
        accumulation.scale_residue_if_needed(tCrScaleBViewAsC);
      }
      if constexpr (ScaleMsPerTile  > 1 && ScaleNsPerTile  > 1) {
        accumulation.scale_residue_if_needed(tCrScaleAViewAsC, tCrScaleBViewAsC);
      }
    }

    warpgroup_fence_operand(accumulation());
  }

  /// Perform a Consumer Epilogue to release all buffers
  CUTLASS_DEVICE void
  mma_tail(MainloopPipeline pipeline, PipelineState smem_pipe_release, int k_tile_count) {
    // Prologue GMMAs
    int prologue_mma_count = min(K_PIPE_MMAS, k_tile_count);
    k_tile_count -= prologue_mma_count;

    smem_pipe_release.advance(k_tile_count);

    // Wait on all GMMAs to complete
    warpgroup_wait<0>();

    for (int count = 0; count < prologue_mma_count; ++count) {
      pipeline.consumer_release(smem_pipe_release);                 // UNLOCK smem_pipe_release, done _computing_ on it
      ++smem_pipe_release;
    }
  }
};

/////////////////////////////////////////////////////////////////////////////////////////////////

} // namespace cutlass::gemm::collective

/////////////////////////////////////////////////////////////////////////////////////////////////
