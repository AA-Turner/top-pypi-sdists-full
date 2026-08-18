#ifndef PYTHONIC_INCLUDE_TYPES_REDUCE_EXPR_HPP
#define PYTHONIC_INCLUDE_TYPES_REDUCE_EXPR_HPP

#include "pythonic/include/types/nditerator.hpp"
#include "pythonic/include/types/tuple.hpp"
#include <cstddef>
#include <type_traits>

PYTHONIC_NS_BEGIN

namespace types
{
  template <class Arg>
  struct reduce_expr {
    static constexpr size_t value = std::decay_t<Arg>::value - 1;
    static constexpr bool is_vectorizable = false;
    static constexpr bool is_flat = false;
    using dtype = typename std::decay_t<Arg>::dtype;
    using shape_t = types::array_tuple<long, value>;
    std::decay_t<Arg> expr;
    long axis;
    shape_t shape_;

    reduce_expr(Arg arg, long axis) : expr(arg), axis(axis)
    {
      auto tmp = sutils::getshape(expr);
      auto next = std::copy(tmp.begin(), tmp.begin() + axis, shape_.begin());
      std::copy(tmp.begin() + axis + 1, tmp.end(), next);
    }
    long flat_size() const;
    template <size_t I>
    auto shape() const
    {
      return std::get<I>(shape_);
    }
  };
} // namespace types
template <class Arg>
struct assignable<types::reduce_expr<Arg>> {
  using type = types::ndarray<typename types::reduce_expr<Arg>::dtype,
                              typename types::reduce_expr<Arg>::shape_t>;
};

PYTHONIC_NS_END

#endif
