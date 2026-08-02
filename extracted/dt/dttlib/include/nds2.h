#include <nds2-client/nds.hh>
#include "rust/cxx.h"

namespace NDS {
inline namespace abi_0 {
  class Parameters: public parameters {
  public:
    rust::String get_param(rust::String key) const;
  };

  std::unique_ptr<Parameters> new_parameters();

}
}
