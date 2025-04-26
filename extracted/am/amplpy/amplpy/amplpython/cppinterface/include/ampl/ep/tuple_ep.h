#ifndef AMPL_TUPLE_EP_H
#define AMPL_TUPLE_EP_H

#include <assert.h>

#include "ampl/ep/scopedarray.h"  // for AMPL_CopyString
#include "ampl/variant.h"
#include "ampl/macros.h"

namespace ampl {

namespace internal {
/**
POD structure representing a Tuple
*/
struct Tuple {
  Variant *data;
  std::size_t size;
};

inline void deleteTuple(Tuple &t) {
  if (t.size == 0) return;
  for (std::size_t i = 0; i < t.size; i++)
    if (t.data[i].type == STRING) AMPL_DeleteString(t.data[i].data.svalue.ptr);
  AMPL_Variant_DeleteArray(t.data);
  t.size = 0;
  t.data = nullptr;
}

class TupleBuilder {
  AMPL_DISALLOW_COPY_AND_ASSIGN(TupleBuilder);

  Variant *data_;
  std::size_t size_;
  std::size_t current_;

 public:
  explicit TupleBuilder(std::size_t size) : size_(size), current_(0) {
    if (size == 0) return;
    data_ = AMPL_Variant_CreateArray(size, internal::ErrorInfo());

  }
  ~TupleBuilder() {
    for (std::size_t i = 0; i < current_; i++)
      internal::deleteVariant(data_[i]);
    AMPL_Variant_DeleteArray(data_);
  }
  void add(VariantRef data) {
    assert(current_ < size_);
    data_[current_] = internal::copyVariant(data.impl());
    current_++;
  }

  internal::Tuple release() {
    internal::Tuple t = {data_, size_};
    data_ = NULL;
    size_ = 0;
    current_ = 0;
    return t;
  }
};

AMPLAPI const char* AMPL_Tuple_ToString(const Tuple* t);

}  // namespace internal
}  // namespace ampl

#endif  // AMPL_TUPLE_EP_H
