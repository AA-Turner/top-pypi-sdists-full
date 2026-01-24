#ifndef DS_CONFIG_HH
#define DS_CONFIG_HH

#include <cstdint>

namespace ds {
    /// @brief 用于list长度、数据长度的类型。
    ///
    /// 一般来说，list的长度和数据长度都不会超过32767，所以使用int16_t。
    /// 如果需要更大的长度或数据长度，可以修改为int32_t或更大。
    using length_t = std::int16_t;

    /// @brief 用于enum的类型。
    using min_uint_t = std::uint8_t;
} // namespace ds

#endif
