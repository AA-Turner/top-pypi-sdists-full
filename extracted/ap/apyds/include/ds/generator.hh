#ifndef DS_GENERATOR_HH
#define DS_GENERATOR_HH

#include <coroutine>

namespace ds {
    template<typename T>
    struct _generator {
        struct promise_type;
        struct iterator_type;
        using handle_type = std::coroutine_handle<promise_type>;
        handle_type handle_;

        _generator() = default;
        explicit _generator(handle_type h) : handle_(h) { }
        _generator(_generator&& other) : handle_(other.handle_) {
            other.handle_ = nullptr;
        }
        _generator& operator=(_generator&& other) {
            if (this != &other) {
                if (handle_) {
                    handle_.destroy();
                }
                handle_ = other.handle_;
                other.handle_ = nullptr;
            }
            return *this;
        }
        ~_generator() {
            if (handle_) {
                handle_.destroy();
            }
        }

        iterator_type begin() {
            if (!handle_) {
                return {nullptr};
            }
            handle_.resume();
            if (handle_.done()) {
                return {nullptr};
            }
            return {handle_};
        }
        iterator_type end() {
            return {nullptr};
        }

        struct promise_type {
            T value_;

            _generator<T> get_return_object() {
                return _generator<T>(handle_type::from_promise(*this));
            }
            std::suspend_always initial_suspend() {
                return {};
            }
            std::suspend_always final_suspend() noexcept {
                return {};
            }
            std::suspend_always yield_value(T value) {
                value_ = value;
                return {};
            }
            void unhandled_exception() {
                throw;
            }
            void return_void() { }
        };

        struct iterator_type {
            handle_type h_;

            T& operator*() const {
                return h_.promise().value_;
            }
            iterator_type& operator++() {
                if (h_) {
                    h_.resume();
                    if (h_.done()) {
                        h_ = nullptr;
                    }
                }
                return *this;
            }
            bool operator==(const iterator_type& it) const {
                return h_ == it.h_;
            }
            bool operator!=(const iterator_type& it) const {
                return h_ != it.h_;
            }
        };
    };

#if defined(__cpp_lib_generator) && 0
    template<typename T>
    using generator = std::generator<T>;
#else
    template<typename T>
    using generator = _generator<T>;
#endif
} // namespace ds

#endif
