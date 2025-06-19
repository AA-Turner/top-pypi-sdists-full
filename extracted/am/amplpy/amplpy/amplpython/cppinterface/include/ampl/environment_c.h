#ifndef AMPL_ENVIRONMENT_C_H
#define AMPL_ENVIRONMENT_C_H

#ifdef __cplusplus
extern "C"
{
#endif

#include <stddef.h>

#include "ampl/declaration_c.h"

/**
 * \defgroup AMPL_ENVIRONMENT AMPL Environment functions
 * @{
 * These fuctions provide access to the environment variables and provides facilities to specify where to load the underlying AMPL interpreter. 
 *
 */

typedef struct {
  char *name;
  char *value;
} AMPL_ENVIRONMENTVAR;

AMPLAPI int AMPL_EnvironmentVarGetName(AMPL_ENVIRONMENTVAR *envvar, char **name);

AMPLAPI int AMPL_EnvironmentVarGetValue(AMPL_ENVIRONMENTVAR *envvar, char **value);


/**
 * An AMPL Environment.
 */
typedef struct AMPL_Environment AMPL_ENVIRONMENT;

/**
 * Allocates the AMPL_ENVIRONMENT struct.
 *
 * \param env Pointer to the pointer of the AMPL_ENVIRONMENT struct.
 * \return .
 */
//AMPLAPI int AMPL_EnvironmentCreate(AMPL_ENVIRONMENT **env);

/**
 * Allocates the AMPL_ENVIRONMENT struct with ability to select the location of the AMPL binary. 
 * Note that if this function is used, the automatic lookup for an AMPL executable will not be executed.
 *
 * \param env Pointer to the pointer of the AMPL_ENVIRONMENT struct.
 * \param binaryDirectory The directory in which to look for the AMPL binary.
 * \param binaryName The name of the AMPL executable if other than “ampl”.
 * \return .
 */
AMPLAPI int AMPL_EnvironmentCreate(AMPL_ENVIRONMENT **env, const char *binaryDirectory, const char *binaryName);

/**
 * Frees the AMPL_ENVIRONMENT struct.
 *
 * \param env Pointer to the pointer of the AMPL_ENVIRONMENT struct.
 * \return .
 */
AMPLAPI int AMPL_EnvironmentFree(AMPL_ENVIRONMENT **env);

/**
 * Allocates a copy of an AMPL_ENVIRONMENT struct.
 *
 * \param copy Pointer to the pointer of the AMPL_ENVIRONMENT struct.
 * \param src Pointer to the AMPL_ENVIRONMENT struct to copy.
 * \return .
 */
AMPLAPI int AMPL_EnvironmentCopy(AMPL_ENVIRONMENT **copy, AMPL_ENVIRONMENT *src);

/**
 * Add an environment variable to the environment, or change its value if already defined.
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param name The name of the environment variable.
 * \param value The value of the environment variable.
 * \return .
 */
AMPLAPI int AMPL_EnvironmentAddEnvironmentVariable(AMPL_ENVIRONMENT *env, const char *name, const char *value);

/**
 * Get the location where AMPLAPI will search for the AMPL executable.
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param binaryDirectory Pointer to the string where the binary directory will be stored.
 * \return .
 */
AMPLAPI int AMPL_EnvironmentGetBinaryDirectory(AMPL_ENVIRONMENT *env, char **binaryDirectory);

/**
 * Get the interpreter that will be used for an AMPL struct constructed
 * using this environment
 * 
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param amplCommand Pointer to the string where the interpreter will be stored.
 * \return .
 */
AMPLAPI int AMPL_EnvironmentGetAMPLCommand(AMPL_ENVIRONMENT *env, char **amplCommand);

/**
 * Set the location where AMPLAPI will search for the AMPL executable. 
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param binaryDirectory The directory in which to search for the AMPL executable.
 * \return .
 */
AMPLAPI int AMPL_EnvironmentSetBinaryDirectory(AMPL_ENVIRONMENT *env, const char *binaryDirectory);

/**
 * Get the name of the AMPL executable.
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param binaryName Pointer to the string where the executable name will be stored.
 * \return .
 */
AMPLAPI int AMPL_EnvironmentGetBinaryName(AMPL_ENVIRONMENT *env, char **binaryName);

/**
 * Set the name of the AMPL executable.
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param binaryName The name of the AMPL executable.
 * \return .
 */
AMPLAPI int AMPL_EnvironmentSetBinaryName(AMPL_ENVIRONMENT *env, const char *binaryName);

/**
 * Store all variables into string.
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param str Pointer to the string where the environment variables will be stored.
 * \return .
 */
AMPLAPI int AMPL_EnvironmentToString(AMPL_ENVIRONMENT *env, char **str);

/**
 * Get the size of the environment variables.
 *
 * \param env Pointer to the AMPL_ENVIRONMENT struct.
 * \param size Pointer to the size of the environment variables will be stored.
 * \return .
 */
AMPLAPI int AMPL_EnvironmentGetSize(AMPL_ENVIRONMENT *env, size_t *size);

AMPLAPI int AMPL_EnvironmentGetEnvironmentVar(AMPL_ENVIRONMENT *env, AMPL_ENVIRONMENTVAR **envvar);

AMPLAPI int AMPL_EnvironmentFindEnvironmentVar(AMPL_ENVIRONMENT *env, const char *name, AMPL_ENVIRONMENTVAR **envvar);

/**@}*/

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // AMPL_ENVIRONMENT_C_H
