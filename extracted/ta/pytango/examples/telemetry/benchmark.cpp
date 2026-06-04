/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

// build and run (at least on macOS with pixi installed):
//   pixi run sh -c 'clang++ -std=c++17 -isystem "$CONDA_PREFIX/include" -L"$CONDA_PREFIX/lib"
//   -Wl,-rpath,"$CONDA_PREFIX/lib" benchmark.cpp -o benchmark -ltango -lomniORB4 -lomnithread'
// To run with telemetry send to local collector via gRPC:
//   TANGO_TELEMETRY_ENABLE=on TANGO_TELEMETRY_LOGGING_EXPORTERS=grpc TANGO_TELEMETRY_TRACING_EXPORTERS=grpc ./benchmark
//

#include <cstdlib>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <tango/tango.h>
#include <vector>

constexpr const char *DEFAULT_DEVICE_NAME = "sys/tg_test/1";
constexpr int DEFAULT_NUM_READS_PER_ITERATION = 100;
constexpr int DEFAULT_NUM_ITERATIONS = 300;

struct Options {
    std::string device_name = DEFAULT_DEVICE_NAME;
    int num_reads_per_iteration = DEFAULT_NUM_READS_PER_ITERATION;
    int num_iterations = DEFAULT_NUM_ITERATIONS;
};

void print_usage(const char *program_name) {
    std::cout << "Usage: " << program_name << " [OPTIONS]\n\n"
              << "Options:\n"
              << "  --device DEVICE              Tango device name to read from.\n"
              << "  --reads-per-iteration READS  Number of reads per timed iteration.\n"
              << "  --iterations ITERATIONS      Number of timed iterations.\n"
              << "  -h, --help                   Show this help message.\n";
}

int parse_positive_int(const std::string &value, const std::string &option_name) {
    std::size_t parsed_chars = 0;
    int parsed_value = std::stoi(value, &parsed_chars);
    if(parsed_chars != value.size() || parsed_value <= 0) {
        throw std::invalid_argument(option_name + " must be a positive integer");
    }
    return parsed_value;
}

Options parse_options(int argc, char **argv) {
    Options options;
    for(int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if(arg == "-h" || arg == "--help") {
            print_usage(argv[0]);
            std::exit(0);
        }

        if(i + 1 >= argc) {
            throw std::invalid_argument("Missing value for " + arg);
        }

        std::string value = argv[++i];
        if(arg == "--device") {
            options.device_name = value;
        } else if(arg == "--reads-per-iteration") {
            options.num_reads_per_iteration = parse_positive_int(value, arg);
        } else if(arg == "--iterations") {
            options.num_iterations = parse_positive_int(value, arg);
        } else {
            throw std::invalid_argument("Unknown option: " + arg);
        }
    }
    return options;
}

double percentile(const std::vector<double> &sorted_values, double percentile) {
    auto rank = static_cast<std::size_t>(std::ceil((percentile / 100.0) * sorted_values.size()));
    rank = std::max<std::size_t>(rank, 1);
    return sorted_values[rank - 1];
}

void eval_telemetry_overhead(const Options &options) {
    std::vector<double> time_per_iteration;
    time_per_iteration.reserve(options.num_iterations);
    auto dp = Tango::DeviceProxy(options.device_name);
    for(int i = 0; i < options.num_iterations; ++i) {
        auto start = std::chrono::steady_clock::now();
        for(int i = 0; i < options.num_reads_per_iteration; ++i) {
            dp.read_attribute("double_scalar");
        }
        auto end = std::chrono::steady_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
        double tpi = static_cast<double>(duration) / options.num_reads_per_iteration;
        time_per_iteration.push_back(tpi);
    }

    double average_tpi =
        std::accumulate(time_per_iteration.begin(), time_per_iteration.end(), 0.0) / options.num_iterations;

    double square_sum = 0.0;
    for(double tpi : time_per_iteration) {
        square_sum += (tpi - average_tpi) * (tpi - average_tpi);
    }

    double rms_tpi = std::sqrt(square_sum / static_cast<double>(options.num_iterations));
    auto sorted_time_per_iteration = time_per_iteration;
    std::sort(sorted_time_per_iteration.begin(), sorted_time_per_iteration.end());
    double p50_tpi = percentile(sorted_time_per_iteration, 50.0);
    double p90_tpi = percentile(sorted_time_per_iteration, 90.0);
    double p95_tpi = percentile(sorted_time_per_iteration, 95.0);

    std::cout << std::fixed << std::setprecision(0);
    std::cout << "Average execution time: " << average_tpi << " microseconds." << std::endl;
    std::cout << "Standard deviation of execution times: " << rms_tpi << " microseconds." << std::endl;
    std::cout << "50th percentile execution time: " << p50_tpi << " microseconds." << std::endl;
    std::cout << "90th percentile execution time: " << p90_tpi << " microseconds." << std::endl;
    std::cout << "95th percentile execution time: " << p95_tpi << " microseconds." << std::endl;
}

int main(int argc, char **argv) {
    try {
        auto options = parse_options(argc, argv);
        eval_telemetry_overhead(options);
    } catch(const std::exception &ex) {
        std::cerr << "Error: " << ex.what() << std::endl;
        print_usage(argv[0]);
        return 1;
    }
}
