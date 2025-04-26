#ifndef AMPL_ERRORINFO_H_
#define AMPL_ERRORINFO_H_

#include <stdexcept>

#include "ampl/amplexception.h"
#include "ampl/ep/declarations.h"
#include "ampl/ep/error_information.h"
#include "ampl/macros.h"

namespace ampl {
namespace internal {
extern "C" {
AMPLAPI void AMPL_ErrorInformation_delete(ErrorInformation *info);
}  // extern C

inline void throwException(ErrorInformation *info) {
  /**
  Represents a generic system exception with message
  */
  class StdException : public std::exception {
    std::string message_;

   public:
    ~StdException() noexcept {}
    StdException(fmt::CStringRef cause) : message_(cause.c_str()) {}
    const char *what() const noexcept { return message_.c_str(); }
  };
  switch (info->errorType) {
    case error::InfeasibilityException:
      throw InfeasibilityException(info->message);
    case error::PresolveException:
      throw PresolveException(info->message);
    case error::LicenseException:
      throw LicenseException(info->message);
    case error::FileIOException:
      throw FileIOException(info->message);
    case error::UnsupportedOperationException:
      throw UnsupportedOperationException(info->message);
    case error::InvalidSubscriptException:
      throw InvalidSubscriptException(info->source, info->line, info->offset,
                                      info->message);
    case error::SyntaxErrorException:
      throw SyntaxErrorException(info->source, info->line, info->offset,
                                 info->message);
    case error::NoDataException:
      throw NoDataException(info->message);
    case error::AMPLException:
      throw AMPLException(info->source, info->line, info->offset,
                          info->message);
    case error::Runtime_Error:
      throw std::runtime_error(info->message);
    case error::Logic_Error:
      throw std::logic_error(info->message);
    case error::Out_Of_Range:
      throw std::out_of_range(info->message);
    case error::Invalid_Argument:
      throw std::invalid_argument(info->message);
    case error::Std_Exception: {
      throw StdException(info->message);
    }
    case error::OK: {
    }
  }
}

class ErrorInfo {
 private:
  ErrorInformation result_;

 public:
  operator ErrorInformation *() { return &result_; }

  ~ErrorInfo() noexcept(false) {
    if (result_.errorType != error::OK) {
      try {
        throwException(&result_);
      } catch (...) {
        AMPL_ErrorInformation_delete(&result_);
        throw;
      }
    }
  }
};
}  // namespace internal
}  // namespace ampl
#endif  // AMPL_ERRORINFO_H_
