//
// SPDX-FileCopyrightText: Copyright 2026 Arm Limited and/or its affiliates <open-source-office@arm.com>
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

#include "architecture/ethosu55/ethos_u55.hpp"
#include "architecture/ethosu85/ethos_u85.hpp"
#include "compiler/graph_optimiser.hpp"
#include "util.hpp"

#include <catch_all.hpp>

#include "regor.h"

using namespace regor;

TEST_CASE("test_tflite_graph_optimiser - convert TFLite Quantization to Explicit Quantization")
{
    auto arch = CreateArchDefault<ArchEthosU55>();
    std::string err = "noerror";
    arch->CheckConfiguration(err);
    REQUIRE(err == "noerror");

    SECTION("Quantize operation with Data type int16")
    {
        std::vector<std::shared_ptr<Operation>> ops;
        auto ifm = CreateTensor("QIFM", Shape(1, 1, 1, 10), DataType::Int16);
        auto ofm = CreateTensor("QOFM", Shape(1, 1, 10, 10), DataType::Int16);
        auto quantizeOp = CreateOperation(OpType::Quantize, TensorUsage::IFM0, ifm, TensorUsage::OFM, ofm);

        auto &ifmQuant = quantizeOp->Input(TensorUsage::IFM0)->quantization;
        ifmQuant.scales.clear();
        ifmQuant.scales.push_back(QuantizedScale(int32_t(1387686912), 42));
        ifmQuant.type = QuantizationType::TFLITE;

        auto &ofmQuant = quantizeOp->Output(TensorUsage::OFM)->quantization;
        ofmQuant.scales.clear();
        ofmQuant.scales.push_back(QuantizedScale(int32_t(1899507328), 45));
        ofmQuant.type = QuantizationType::TFLITE;

        ops.push_back(std::move(quantizeOp));
        auto graph = CreateGraph(ops, GraphNotation::TFLite);

        GraphOptimiserOptions options;
        const auto &optimiser = GraphOptimiser::MakeGraphOptimiser(graph->Notation(), arch.get(), options, nullptr);
        REQUIRE(!optimiser.empty());
        optimiser.front()->Process(graph.get());

        std::vector<Operation *> allOps;
        graph->GetAllOperations(allOps);
        REQUIRE(allOps.size() == 1);

        REQUIRE(ofmQuant.type == QuantizationType::EXPLICIT);
        REQUIRE(ifmQuant.type == QuantizationType::EXPLICIT);
        REQUIRE(ifmQuant.scales[0] == QuantizedScale::Unit());

        REQUIRE(ofmQuant.scales.size() == 1);
        auto quantScale = ofmQuant.scales[0];
        REQUIRE(quantScale.scale == 1568846252);
        REQUIRE(quantScale.shift == 28);
    }
    SECTION("Mul operation with Data type int8")
    {
        std::vector<std::shared_ptr<Operation>> ops;
        auto ifm0 = CreateTensor("IFM0", Shape(1, 1, 1, 10), DataType::Int8);
        auto ifm1 = CreateTensor("IFM1", Shape(1, 1, 1, 10), DataType::Int8);
        auto ofm = CreateTensor("OFM", Shape(1, 1, 10, 10), DataType::Int8);
        auto mulOp = CreateOperation(OpType::Mul, TensorUsage::IFM0, ifm0, TensorUsage::IFM1, ifm1, TensorUsage::OFM, ofm);

        auto &ifmQuant0 = mulOp->Input(TensorUsage::IFM0)->quantization;
        ifmQuant0.scales.clear();
        ifmQuant0.scales.push_back(QuantizedScale(int32_t(1888360448), 37));
        ifmQuant0.type = QuantizationType::TFLITE;

        auto &ifmQuant1 = mulOp->Input(TensorUsage::IFM1)->quantization;
        ifmQuant1.scales.clear();
        ifmQuant1.scales.push_back(QuantizedScale(int32_t(1888360448), 37));
        ifmQuant1.type = QuantizationType::TFLITE;

        auto &ofmQuant = mulOp->Output(TensorUsage::OFM)->quantization;
        ofmQuant.scales.clear();
        ofmQuant.scales.push_back(QuantizedScale(int32_t(1578641920), 37));
        ofmQuant.type = QuantizationType::TFLITE;

        ops.push_back(std::move(mulOp));
        auto graph = CreateGraph(ops, GraphNotation::TFLite);

        GraphOptimiserOptions options;
        const auto &optimiser = GraphOptimiser::MakeGraphOptimiser(graph->Notation(), arch.get(), options, nullptr);
        REQUIRE(!optimiser.empty());
        optimiser.front()->Process(graph.get());

        std::vector<Operation *> allOps;
        graph->GetAllOperations(allOps);
        REQUIRE(allOps.size() == 1);

        REQUIRE(ofmQuant.type == QuantizationType::EXPLICIT);
        REQUIRE(ifmQuant0.type == QuantizationType::EXPLICIT);
        REQUIRE(ifmQuant0.scales[0] == QuantizedScale::Unit());
        REQUIRE(ifmQuant1.type == QuantizationType::EXPLICIT);
        REQUIRE(ifmQuant1.scales[0] == QuantizedScale::Unit());

        REQUIRE(ofmQuant.scales.size() == 1);
        auto quantScale = ofmQuant.scales[0];
        REQUIRE(quantScale.scale == 1129421696);
        REQUIRE(quantScale.shift == 36);
    }
}

TEST_CASE("test_tflite_graph_optimiser - rewrite depthwise-equivalent convolution group")
{
    auto arch = CreateArchDefault<ArchEthosU85>();
    std::string err = "noerror";
    arch->CheckConfiguration(err);
    REQUIRE(err == "noerror");

    constexpr int channels = 2;
    std::vector<int8_t> weightValues(channels * 3);
    for ( int i = 0; i < int(weightValues.size()); i++ )
    {
        weightValues[i] = int8_t(i);
    }

    auto ifm = CreateTensor("IFM", Shape(1, 1, 5, channels), DataType::Int16);
    auto weights = CreateTensor("WEIGHTS", Shape(channels, 1, 3, 1), DataType::Int8, std::move(weightValues));
    auto bias = CreateTensor("BIAS", Shape(channels), DataType::Int32, 0);
    auto ofm = CreateTensor("OFM", Shape(1, 1, 3, channels), DataType::Int16);
    auto conv = CreateOperation(OpType::Conv2D, TensorUsage::IFM, ifm, TensorUsage::Weights, weights,
        TensorUsage::Scales, bias, TensorUsage::OFM, ofm);
    conv->SetKernel(std::make_unique<Kernel>(Kernel::UnitKernel().WithSize({3, 1})));

    auto &weightQuant = conv->Input(TensorUsage::Weights)->quantization;
    weightQuant.scales.assign(channels, QuantizedScale::Unit());
    weightQuant.zeroPoints.assign(channels, 0);
    weightQuant.dimension = 0;

    std::vector<std::shared_ptr<Operation>> ops = {std::move(conv)};
    auto graph = CreateGraph(ops, GraphNotation::TFLite);
    GraphOptimiserOptions options;
    const auto &optimiser = GraphOptimiser::MakeGraphOptimiser(graph->Notation(), arch.get(), options, nullptr);
    REQUIRE(!optimiser.empty());
    optimiser.front()->Process(graph.get());

    std::vector<Operation *> allOps;
    graph->GetAllOperations(allOps);
    REQUIRE(allOps.size() == 1);
    REQUIRE(allOps[0]->Type() == OpType::DepthwiseConv2D);

    const auto *depthwiseWeights = allOps[0]->Input(TensorUsage::Weights);
    REQUIRE(depthwiseWeights->shape == Shape(1, 1, 3, channels));
    REQUIRE(depthwiseWeights->slice.shape == depthwiseWeights->shape);
    REQUIRE(depthwiseWeights->slice.stride == Shape(1, 3, 1, 3));
    REQUIRE(depthwiseWeights->quantization.scales.size() == channels);
    REQUIRE(depthwiseWeights->tensor->StorageShape() == Shape(channels, 1, 3, 1));

    auto weightView = depthwiseWeights->tensor->View().Reshape(depthwiseWeights->slice.shape, depthwiseWeights->slice.stride);
    auto weightReader = weightView.Values<int8_t>();
    REQUIRE(weightReader[{0, 0, 0, 0}] == 0);
    REQUIRE(weightReader[{0, 0, 0, 1}] == 3);
    REQUIRE(weightReader[{0, 0, 1, 0}] == 1);
}
