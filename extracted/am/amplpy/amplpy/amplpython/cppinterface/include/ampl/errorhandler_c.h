#ifndef AMPL_ERRORHANDLER_C_H
#define AMPL_ERRORHANDLER_C_H

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>

#include "ampl/declaration_c.h"


typedef enum {
  AMPL_EXCEPTION = 0,
  AMPL_LICENSE_EXCEPTION,
  AMPL_FILE_IO_EXCEPTION,
  AMPL_UNSUPPORTED_OPERATION_EXCEPTION,
  AMPL_INVALID_SUBSCRIPT_EXCEPTION,
  AMPL_SYNTAX_ERROR_EXCEPTION,
  AMPL_NO_DATA_EXCEPTION,
  AMPL_LOGIC_ERROR,
  AMPL_RUNTIME_ERROR,
  AMPL_INVALID_ARGUMENT,
  AMPL_OUT_OF_RANGE,
  AMPL_STD_EXCEPTION,
  AMPL_PRESOLVE_EXCEPTION,
  AMPL_INFEASIBILITY_EXCEPTION
} AMPL_ERRORCODE;

typedef struct AMPL_ErrorInfo AMPL_ERRORINFO;

#define AMPL_CALL(x)                                                 \
    do {                                                             \
        AMPL_ERRORINFO *call = (x);                                  \
        if (call) {                                                  \
            fprintf(stderr, "%s\n", AMPL_ErrorInfoGetMessage(call)); \
        }                                                            \
    }                                                                \
    while(0)

AMPLAPI AMPL_ERRORCODE AMPL_ErrorInfoGetError(AMPL_ERRORINFO *error);
AMPLAPI char *AMPL_ErrorInfoGetMessage(AMPL_ERRORINFO *error);
AMPLAPI int AMPL_ErrorInfoGetLine(AMPL_ERRORINFO *error);
AMPLAPI int AMPL_ErrorInfoGetOffset(AMPL_ERRORINFO *error);
AMPLAPI char *AMPL_ErrorInfoGetSource(AMPL_ERRORINFO *error);
AMPLAPI int AMPL_ErrorInfoFree(AMPL_ERRORINFO **error);

typedef void (*ErrorHandlerCbPtr)(bool isWarning, const char* filename, int row,
                                  int offset, const char* message,
                                  void* errorHandler);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // AMPL_ERRORHANDLER_C_H
