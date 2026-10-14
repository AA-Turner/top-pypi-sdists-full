//
// Created by korniltsev on 2/6/2026.
//
#pragma once

#include <optional>
#include <string_view>
#include <vector>

#include "dd_wrapper/include/profile_borrow.hpp"


extern "C" {
#include "pyroscope_ffi.h"
}

namespace Pyroscope
{
    /* Upstream's ddog_prof_StringId2; ours indexes the table in rust/src/encode/interner.rs. */
    using string_id = FFIInternedString;

    inline string_id intern_utf8_string(const std::string_view s)
    {
        return pyroscope_string_table_intern_utf8(FFIStringView{
            .data = s.data(),
            .len = s.length()
        });
    }

    inline string_id intern_ascii_string(const std::string_view s)
    {
        return pyroscope_string_table_intern_ascii(FFIStringView{
            .data = s.data(),
            .len = s.length()
        });
    }

    class Sample
    {
        std::vector<FFIFrame> frames;
        size_t max_nframes;
        PprofBuilderType builder_type;
        FFISampleValues values{};
        bool truncated = false;

        void push_frame_impl(const string_id function_name, const string_id file_name, const int line)
        {
            frames.emplace_back(
                FFIFrame{
                    .function_name = function_name,
                    .file_name = file_name,
                    .line = line,
                }
            );
        }

    public:
        Sample(const size_t _max_nframes, const PprofBuilderType _builder_type)
            : max_nframes{_max_nframes}, builder_type{_builder_type}
        {
            frames.reserve(max_nframes + 1);
        }



        void set_builder_type(const PprofBuilderType _builder_type)
        {
            builder_type = _builder_type;
        }

        void push_frame(const string_id function_name, const string_id file_name, const int line)
        {
            if (frames.size() >= max_nframes)
            {
                incr_dropped_frames();
                return;
            }
            push_frame_impl(function_name, file_name, line);
        }


        void push_frame(const std::string_view function_name, const std::string_view file_name,
                        [[maybe_unused]] int address, const int line)
        {
            if (frames.size() >= max_nframes)
            {
                incr_dropped_frames();
                return;
            }
            push_frame(intern_ascii_string(function_name), intern_ascii_string(file_name), line);
        }


        void push_alloc(const size_t size, const size_t count)
        {
            values.alloc_space += size;
            values.alloc_count += count;
        }

        void push_heap(const size_t size, const size_t count)
        {
            values.heap_space += size;
            values.heap_count += count;
        }

        void reset_alloc()
        {
            values.alloc_space = 0;
            values.alloc_count = 0;
        }

        void clear()
        {
            values = {};
            frames.clear();
            truncated = false;
        }

        void export_sample()
        {
            if (truncated)
            {
                static constexpr std::string_view marker = "<truncated>";
                const string_id id = intern_ascii_string(marker);
                push_frame_impl(id, id, 0);
                truncated = false;
            }
            pyroscope_push_sample(builder_type, frames.data(), frames.size(), &values);
        }

        void push_threadinfo([[maybe_unused]] int64_t thread_id,
                             [[maybe_unused]] int64_t thread_native_id,
                             [[maybe_unused]] const std::string_view name)
        {
            // no-op
        }

        void push_monotonic_ns([[maybe_unused]] int64_t monotonic_ns)
        {
            // no-op
        }

        void push_walltime(const int64_t walltime, [[maybe_unused]] const int64_t count)
        {
            values.wall_time += walltime;
        }

        void push_cputime(const int64_t cputime, [[maybe_unused]] const int64_t count)
        {
            values.cpu_time += cputime;
        }

        void push_span_id([[maybe_unused]] uint64_t span_id)
        {
            // no-op
        }

        void push_local_root_span_id([[maybe_unused]] uint64_t local_root_span_id)
        {
            // no-op
        }

        void push_trace_type([[maybe_unused]] const std::string_view trace_type)
        {
            // no-op
        }

        void push_task_name([[maybe_unused]] const std::string_view task_name)
        {
            // no-op
        }

        void push_task_id([[maybe_unused]] uint64_t task_id)
        {
            // no-op
        }

        void push_origin_task_id([[maybe_unused]] uint64_t origin_task_id)
        {
            // no-op
        }

        void push_origin_task_name([[maybe_unused]] const std::string_view origin_task_name)
        {
            // no-op
        }


        void flush_sample()
        {
            export_sample();
            clear();
        }

        // Pyroscope patch: appends one countless "<truncated>" frame where
        // upstream appends "<N frame(s) omitted>".
        void incr_dropped_frames([[maybe_unused]] size_t count = 1)
        {
            truncated = true;
        }

        /* Stats sink for the vendored stack sampler; see ProfilerStats. */
        static Datadog::ProfileBorrow profile_borrow()
        {
            return Datadog::ProfileBorrow{};
        }
    };
}

namespace Datadog {

using Sample = Pyroscope::Sample;
using string_id = Pyroscope::string_id;

// Pyroscope patch: never nullopt; a failed intern yields index 0.
inline std::optional<Pyroscope::string_id>
intern_string(std::string_view s)
{
    return Pyroscope::intern_utf8_string(s);
}

} // namespace Datadog
