// This file is a stub to allow compiling without google logging

#include <iostream>

// Define debug prints
#define DEBUG_LEVEL (0)

#if DEBUG_LEVEL >= 1
#define DEBUG(...) printf("%-30s: ", __func__); printf(__VA_ARGS__)
#define NAKED_DEBUG(...) printf(__VA_ARGS__)
#else
#define DEBUG(...)
#define NAKED_DEBUG(...)
#endif

#if DEBUG_LEVEL >= 2
#define DDEBUG(...) printf("%-30s: ", __func__); printf(__VA_ARGS__)
#else
#define DDEBUG(...)
#endif

#if DEBUG_LEVEL >= 3
#define DDDEBUG(...) printf("%-30s: ", __func__); printf(__VA_ARGS__)
#else
#define DDDEBUG(...)
#endif


// Define logging macros
#define LOG(...) LogSink()
#define VLOG(...) LogSink()
#define DCHECK(...) LogSink()
#define DCHECK_EQ(...) LogSink()
#define DCHECK_NE(...) LogSink()
#define DCHECK_LE(...) LogSink()

#include <string>

// Expose expected logging classes/functions
namespace google {

    const int INFO = 0;
    const int WARNING = 0;
    const int ERROR = 0;

    class LogSink {
        public:
        LogSink& operator<<(const std::string&) {
            return *this;
        }

        LogSink& operator <<(const int) {
            return *this;
        }

        LogSink& operator <<(void *) {
            return *this;
        }

        LogSink& operator <<(const char*) {
            return *this;
        }
    };

    class LogSeverity {
        public:
        LogSeverity(...) {
        }
    };

    class LogMessage {
        public:
        LogMessage(...) {
        }

        LogSink& stream() {
            return sink;
        }

        private:
        LogSink sink;
    };

    class AddLogSink {
    };

    class RemoveLogSink {
    };
}
