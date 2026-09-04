//
// SPDX-FileCopyrightText: Copyright 2024, 2026 Arm Limited and/or its affiliates <open-source-office@arm.com>
//
// SPDX-License-Identifier: Apache-2.0
//
// Licensed under the Apache License, Version 2.0 (the License); you may
// not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an AS IS BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

#include "common/common.hpp"

#include "architecture/ethosu85/ethos_u85.hpp"
#include "architecture/ethosu85/ethos_u85_register_cs_generator.hpp"
#include "compiler/high_level_command_stream_generator.hpp"
#include "compiler/scheduler_packing.hpp"
#include "util.hpp"

#include <catch_all.hpp>

#include "regor.h"

using namespace regor;

namespace
{

std::vector<uint32_t> CompileOpsToRegisterCommandStream(ArchEthosU85 *arch, std::vector<std::shared_ptr<Operation>> &ops)
{
    auto graph = CreateGraph(ops);

    std::unordered_map<UniqueId, UniqueId> tensorEquivalenceIdMap;
    SchedulerPacking packing(arch, false, tensorEquivalenceIdMap);
    auto schedOps = packing.Process(graph.get());

    SchedulerOptions opts;
    // Keep the two scheduled op-groups separate so the generated RCS has an inter-group BLOCKDEP to inspect.
    opts.disabled.Set(SchedulerFeature::Cascading);
    SchedulerOpConfigMap configMap;
    Scheduler scheduler(arch, opts, "test", schedOps, configMap);
    auto schedule = scheduler.Process();

    NPUOperation npuOp;
    for ( auto &op : schedOps )
    {
        npuOp.AddOperation(std::move(op));
    }

    HLCStreamGenerator hlcsGenerator(0, false);
    SubGraphs subgraphs;
    auto hlcs = hlcsGenerator.GenerateCommandStream(&npuOp, schedule.get(), subgraphs);
    REQUIRE_FALSE(hlcs.empty());

    EthosU85RCSGenerator rcsGenerator(arch);
    auto stream = rcsGenerator.GenerateCommandStream(hlcs, nullptr, false);
    REQUIRE_FALSE(stream.empty());
    return stream;
}

std::vector<int> DecodeBlockdeps(ArchEthosU85 *arch, const std::vector<uint32_t> &stream)
{
    EthosU85RCSGenerator decoder(arch);
    std::vector<int> blockdeps;
    for ( int pos = 0; pos < int(stream.size()); )
    {
        std::string op;
        std::vector<std::pair<std::string, std::string>> fields;
        int words = decoder.Disassemble(stream.data() + pos, op, fields);
        if ( op == "NPU_SET_BLOCKDEP" )
        {
            auto blockdep = std::find_if(
                fields.begin(), fields.end(), [](const auto &field) { return field.first == "blockdep"; });
            REQUIRE(blockdep != fields.end());
            blockdeps.push_back(std::stoi(blockdep->second));
        }
        pos += words;
    }

    return blockdeps;
}

}  // namespace

TEST_CASE("arch_ethos_u85 GetOpConfig")
{
    auto arch = CreateArchDefault<ArchEthosU85>(1024);
    ArchitectureConfigQuery query{};
    Kernel kernel({1, 1}, {1, 1}, {0, 0});
    query.ifmBits = 8;
    query.lutBytes = 0;
    query.scaled = false;
    query.ifmResampling = ArchResampling::None;
    query.transpose = TransposeType::None;
    query.ofmFormat = TensorFormat::NHCWB16;
    query.accOutputEnabled = true;

    SECTION("No waste")
    {
        OpType type = OpType::Add;
        query.ofmShape = {1, 8, 8, 32};
        query.ifmShape[0] = query.ofmShape;
        query.kernel = &kernel;
        auto archOpConfig = arch->GetOpConfig(type, query);
        EthosU85OpConfig *ethosU85OpConfig = static_cast<EthosU85OpConfig *>(archOpConfig.get());
        REQUIRE(ethosU85OpConfig->OfmUBlock() == Shape(2, 2, 32));
    }

    SECTION("Waste in H")
    {
        OpType type = OpType::Add;
        query.ofmShape = {1, 1, 8, 32};
        query.ifmShape[0] = query.ofmShape;
        query.kernel = &kernel;
        auto archOpConfig = arch->GetOpConfig(type, query);
        EthosU85OpConfig *ethosU85OpConfig = static_cast<EthosU85OpConfig *>(archOpConfig.get());
        REQUIRE(ethosU85OpConfig->OfmUBlock() == Shape(1, 4, 32));
    }

    SECTION("Waste in W")
    {
        OpType type = OpType::Add;
        query.ofmShape = {1, 8, 1, 16};
        query.ifmShape[0] = query.ofmShape;
        query.kernel = &kernel;
        auto archOpConfig = arch->GetOpConfig(type, query);
        EthosU85OpConfig *ethosU85OpConfig = static_cast<EthosU85OpConfig *>(archOpConfig.get());
        REQUIRE(ethosU85OpConfig->OfmUBlock() == Shape(2, 2, 32));
    }

    SECTION("Waste in C")
    {
        OpType type = OpType::Add;
        query.ofmShape = {1, 8, 8, 1};
        query.ifmShape[0] = query.ofmShape;
        query.kernel = &kernel;
        auto archOpConfig = arch->GetOpConfig(type, query);
        EthosU85OpConfig *ethosU85OpConfig = static_cast<EthosU85OpConfig *>(archOpConfig.get());
        REQUIRE(ethosU85OpConfig->OfmUBlock() == Shape(2, 4, 16));
    }
}


TEST_CASE("arch_ethos_u85 UpscaleAndRounding")
{
    auto arch = CreateArchDefault<ArchEthosU85>(1024);
    SECTION("Resampling None")
    {
        int rounding;
        int upscale = arch->UpscaleAndRounding(ArchResampling::None, rounding);
        REQUIRE(rounding == 0);
        REQUIRE(upscale == 1);
    }
    SECTION("Resampling Zero")
    {
        int rounding;
        int upscale = arch->UpscaleAndRounding(ArchResampling::Zeros, rounding);
        REQUIRE(rounding == 0);
        REQUIRE(upscale == 2);
    }
    SECTION("Resampling Nearest")
    {
        int rounding;
        int upscale = arch->UpscaleAndRounding(ArchResampling::Nearest, rounding);
        REQUIRE(rounding == 1);
        REQUIRE(upscale == 2);
    }
}

TEST_CASE("Test blockdep support for chained ops")
{
    auto arch = CreateArchDefault<ArchEthosU85>(1024);
    auto *ethosU85 = static_cast<ArchEthosU85 *>(arch.get());
    constexpr int maxBlockdep = 7;

    SECTION("Zero when chained subOp consumes the previous op OFM")
    {
        const Shape shape(1, 8, 8, 32);
        auto op0Ifm0 = CreateTensor("op0_ifm0", shape, DataType::Int8);
        auto op0Ifm1 = CreateTensor("op0_ifm1", shape, DataType::Int8);
        auto op0Ofm = CreateTensor("op0_ofm", shape, DataType::Int8);

        auto op1Ifm0 = CreateTensor("op1_ifm0", shape, DataType::Int8);
        auto op1Ifm1 = CreateTensor("op1_ifm1", shape, DataType::Int8);
        auto op1Ofm = CreateTensor("op1_ofm", shape, DataType::Int8);
        auto op2Ofm = CreateTensor("op2_ofm", shape, DataType::Int8);

        auto op0 = CreateOperation(OpType::Add, TensorUsage::IFM0, op0Ifm0, TensorUsage::IFM1, op0Ifm1, TensorUsage::OFM, op0Ofm);
        auto op1 = CreateOperation(OpType::Add, TensorUsage::IFM0, op1Ifm0, TensorUsage::IFM1, op1Ifm1, TensorUsage::OFM, op1Ofm);
        auto op2 = CreateOperation(OpType::Add, TensorUsage::IFM0, op1Ofm, TensorUsage::IFM1, op0Ofm, TensorUsage::OFM, op2Ofm);

        std::vector<std::shared_ptr<Operation>> ops = {op0, op1, op2};
        auto stream = CompileOpsToRegisterCommandStream(ethosU85, ops);
        auto blockdeps = DecodeBlockdeps(ethosU85, stream);

        REQUIRE(blockdeps.size() == 1);
        CHECK(blockdeps[0] == 0);
    }

    SECTION("Non-zero when chained subop IFM overlaps after later jobs")
    {
        const Shape shape(1, 8, 8, 1024);
        auto op0Ifm0 = CreateTensor("op0_ifm0", shape, DataType::Int8);
        auto op0Ifm1 = CreateTensor("op0_ifm1", shape, DataType::Int8);
        auto op0Ofm = CreateTensor("op0_ofm", shape, DataType::Int8);

        auto op1Ifm0 = CreateTensor("op1_ifm0", shape, DataType::Int8);
        auto op1Ifm1 = CreateTensor("op1_ifm1", shape, DataType::Int8);
        auto op1Ofm = CreateTensor("op1_ofm", shape, DataType::Int8);
        auto op2Ofm = CreateTensor("op2_ofm", shape, DataType::Int8);

        auto op0 = CreateOperation(OpType::Add, TensorUsage::IFM0, op0Ifm0, TensorUsage::IFM1, op0Ifm1, TensorUsage::OFM, op0Ofm);
        auto op1 = CreateOperation(OpType::Add, TensorUsage::IFM0, op1Ifm0, TensorUsage::IFM1, op1Ifm1, TensorUsage::OFM, op1Ofm);
        auto op2 = CreateOperation(OpType::Add, TensorUsage::IFM0, op1Ofm, TensorUsage::IFM1, op0Ofm, TensorUsage::OFM, op2Ofm);

        std::vector<std::shared_ptr<Operation>> ops = {op0, op1, op2};
        auto stream = CompileOpsToRegisterCommandStream(ethosU85, ops);
        auto blockdeps = DecodeBlockdeps(ethosU85, stream);

        REQUIRE(blockdeps.size() == 2);
        CHECK(blockdeps[0] == 0);
        CHECK(blockdeps[1] == 1);
    }

    SECTION("Maximum when current op group does not consume the prev op OFM")
    {
        const Shape shape(1, 8, 8, 32);
        auto op0Ifm0 = CreateTensor("op0_ifm0", shape, DataType::Int8);
        auto op0Ifm1 = CreateTensor("op0_ifm1", shape, DataType::Int8);
        auto op0Ofm = CreateTensor("op0_ofm", shape, DataType::Int8);

        auto op1Ifm0 = CreateTensor("op1_ifm0", shape, DataType::Int8);
        auto op1Ifm1 = CreateTensor("op1_ifm1", shape, DataType::Int8);
        auto op1Ofm = CreateTensor("op1_ofm", shape, DataType::Int8);
        auto op2Ifm1 = CreateTensor("op2_ifm1", shape, DataType::Int8);
        auto op2Ofm = CreateTensor("op2_ofm", shape, DataType::Int8);

        auto op0 = CreateOperation(OpType::Add, TensorUsage::IFM0, op0Ifm0, TensorUsage::IFM1, op0Ifm1, TensorUsage::OFM, op0Ofm);
        auto op1 = CreateOperation(OpType::Add, TensorUsage::IFM0, op1Ifm0, TensorUsage::IFM1, op1Ifm1, TensorUsage::OFM, op1Ofm);
        auto op2 = CreateOperation(OpType::Add, TensorUsage::IFM0, op1Ofm, TensorUsage::IFM1, op2Ifm1, TensorUsage::OFM, op2Ofm);

        std::vector<std::shared_ptr<Operation>> ops = {op1, op2, op0};
        auto stream = CompileOpsToRegisterCommandStream(ethosU85, ops);
        auto blockdeps = DecodeBlockdeps(ethosU85, stream);

        REQUIRE(blockdeps.size() == 2);
        CHECK(blockdeps[0] == 0);
        CHECK(blockdeps[1] == maxBlockdep);
    }
}
