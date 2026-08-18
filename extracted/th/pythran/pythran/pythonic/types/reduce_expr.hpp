#ifndef PYTHONIC_TYPES_REDUCE_EXPR_HPP
#define PYTHONIC_TYPES_REDUCE_EXPR_HPP

#include "pythonic/include/types/reduce_expr.hpp"
#include "pythonic/types/nditerator.hpp"
#include "pythonic/types/tuple.hpp"

#include <numeric>

PYTHONIC_NS_BEGIN

namespace types
{

  template <class Arg>
  long reduce_expr<Arg>::flat_size() const
  {
    auto tmp = sutils::getshape(expr);
    auto acc = std::accumulate(tmp.begin(), tmp.begin() + axis, 1L, std::multiplies<void>{});
    return std::accumulate(tmp.begin() + axis + 1, tmp.end(), acc);
  }
} // namespace types

PYTHONIC_NS_END

#endif
