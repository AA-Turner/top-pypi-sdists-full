#ifndef AMPL_TUPLE_C_H
#define AMPL_TUPLE_C_H

#ifdef __cplusplus
extern "C"
{
#endif

#include <stddef.h>

#include "ampl/declaration_c.h"
#include "ampl/variant_c.h"


/**
 * \defgroup AMPL_TUPLE AMPL Tuple struct functions
 * @{
 * The struct can represent a tuple with AMPL_VARIANTs as its members and maps directly to
 * the underlying %AMPL tuple.
 *
 */

/**
 * An AMPL tuple.
 */
typedef struct AMPL_Tuple AMPL_TUPLE;

AMPLAPI void retainTuple(AMPL_TUPLE *t);
AMPLAPI void releaseTuple(AMPL_TUPLE *t);

/**
 * Allocates an AMPL_TUPLE struct.
 *
 * \param t Pointer to the pointer of the AMPL_TUPLE struct.
 * \param size Size of the tuple.
 * \param v Pointer to the pointer of AMPL_VARIANT structs.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_TupleCreate(AMPL_TUPLE **t, size_t size, AMPL_VARIANT **v);

/**
 * Allocates an AMPL_TUPLE struct with numeric variants.
 *
 * \param t Pointer to the pointer of the AMPL_TUPLE struct.
 * \param size Size of the tuple.
 * \param v Pointer to doubles.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_TupleCreateNumeric(AMPL_TUPLE **t, size_t size, double *v);

/**
 * Allocates an AMPL_TUPLE struct with string variants.
 *
 * \param t Pointer to the pointer of the AMPL_TUPLE struct.
 * \param size Size of the tuple.
 * \param v Pointer to strings.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_TupleCreateString(AMPL_TUPLE **t, size_t size, const char *const *v);

/**
 * Allocates a copy of an AMPL_TUPLE struct.
 *
 * \param t Pointer to the pointer of the AMPL_TUPLE struct.
 * \param copy Pointer to the AMPL_TUPLE struct to copy.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_TupleCopy(AMPL_TUPLE **t, AMPL_TUPLE *copy);

/**
 * Frees the AMPL_TUPLE struct.
 *
 * \param t Pointer to the pointer of the AMPL_TUPLE struct.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_TupleFree(AMPL_TUPLE **t);

/**
 * Compares two AMPL_TUPLE structs.
 *
 * \param t1 Pointer to the first AMPL_TUPLE struct.
 * \param t2 Pointer to the second AMPL_TUPLE struct.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_TupleCompare(AMPL_TUPLE *t1, AMPL_TUPLE *t2);

/**
 * Get the size of an AMPL_TUPLE struct.
 *
 * \param t Pointer to the AMPL_TUPLE struct.
 * \param size Pointer to the size.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_TupleGetSize(AMPL_TUPLE *t, size_t *size);

/**
 * Get the AMPL_VARIANT at a given index of an AMPL_TUPLE struct.
 *
 * \param t Pointer to the AMPL_TUPLE struct.
 * \param v Pointer to the pointer of the AMPL_VARIANT struct.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_TupleGetVariantPtr(AMPL_TUPLE *t, AMPL_VARIANT ***v);

/**
 * Get the AMPL_VARIANT at a given index of an AMPL_TUPLE struct.
 *
 * \param t Pointer to the AMPL_TUPLE struct.
 * \param index Index of the AMPL_VARIANT.
 * \param v Pointer to the pointer of the AMPL_VARIANT struct.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_TupleGetVariant(AMPL_TUPLE *t, size_t index, AMPL_VARIANT **v);

/**
 * Get the string representation of an AMPL_TUPLE struct.
 *
 * \param t Pointer to the AMPL_TUPLE struct.
 * \param cstr Pointer to the string representation.
 * \return 0 iff successful.
 */
AMPLAPI int AMPL_TupleToString(AMPL_TUPLE *t, char **cstr);

/**@}*/

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // AMPL_TUPLE_C_H
