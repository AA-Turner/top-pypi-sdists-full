/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

// build and run (at least on macOS within conda environment):
//   clang++ -isystem $CONDA_PREFIX/include -L$CONDA_PREFIX/lib -rpath $CONDA_PREFIX/lib -ltango -lomniORB4 -lomnithread
//   benchmark.cpp -o benchmark
// To run with telemetry send to local collector via gRPC:
//   TANGO_TELEMETRY_ENABLE=on TANGO_TELEMETRY_LOGS_EXPORTER=grpc TANGO_TELEMETRY_TRACES_EXPORTER=grpc ./benchmark
//

#include <iostream>
#include <numeric>
#include <tango/tango.h>

void eval_telemetry_overhead(const int n = 100, const int m = 100) {
    std::vector<double> time_per_iteration;
    time_per_iteration.reserve(m);
    // auto dp = Tango::DeviceProxy("tango://127.0.0.1:44555/test/device/1#dbase=no");
    auto dp = Tango::DeviceProxy("sys/tg_test/1");
    for(int i = 0; i < m; ++i) {
        auto start = std::chrono::steady_clock::now();
        for(int i = 0; i < n; ++i) {
            dp.read_attribute("double_scalar");
        }
        auto end = std::chrono::steady_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
        double tpi = static_cast<double>(duration) / n;
        time_per_iteration.push_back(tpi);
    }

    double average_tpi = std::accumulate(time_per_iteration.begin(), time_per_iteration.end(), 0.0) / m;

    double square_sum = 0.0;
    for(double tpi : time_per_iteration) {
        square_sum += (tpi - average_tpi) * (tpi - average_tpi);
    }

    double rms_tpi = std::sqrt(square_sum / static_cast<double>(m));

    std::cout << "Average execution time: " << average_tpi << " milliseconds." << std::endl;
    std::cout << "Standard deviation of execution times: " << rms_tpi << " milliseconds." << std::endl;
}

int main(int argc, char **argv) {
    eval_telemetry_overhead(100, 200);
}
