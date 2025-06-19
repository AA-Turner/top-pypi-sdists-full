#ifndef AMPL_DECLARATION_C_H
#define AMPL_DECLARATION_C_H

#ifdef __cplusplus
extern "C"
{
#endif

#ifdef _WIN32
#ifdef AMPLAPI_EXPORTS
#define AMPLAPI __declspec(dllexport)
#else
#define AMPLAPI __declspec(dllimport)
#endif
#else
#define AMPLAPI __attribute__((visibility("default")))
#endif

typedef enum {
  AMPL_EMPTY, 
  AMPL_NUMERIC, 
  AMPL_STRING 
} AMPL_TYPE;

typedef enum {
  AMPL_ASTATUS,
  AMPL_SSTATUS,
  AMPL_STATUS,
  AMPL_MESSAGE,
  AMPL_RESULT,
  AMPL_SENSE 
} AMPL_STRINGSUFFIX;

typedef enum {
  AMPL_VALUE,
  AMPL_DEFEQN,
  AMPL_DUAL,
  AMPL_INIT,
  AMPL_INIT0,
  AMPL_LB,
  AMPL_UB,
  AMPL_LB0,
  AMPL_UB0,
  AMPL_LB1,
  AMPL_UB1,
  AMPL_LB2,
  AMPL_UB2,
  AMPL_LRC,
  AMPL_URC,
  AMPL_LSLACK,
  AMPL_USLACK,
  AMPL_RC,
  AMPL_SLACK,

  // CONSTRAINTS
  AMPL_BODY,
  AMPL_DEFVAR,
  AMPL_DINIT,
  AMPL_DINIT0,
  AMPL_LBS,
  AMPL_UBS,
  AMPL_LDUAL,
  AMPL_UDUAL,
  AMPL_VAL,  // for logical constraints

  // OBJECTIVES
  AMPL_EXITCODE
} AMPL_NUMERICSUFFIX;

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // AMPL_DECLARATION_C_H
