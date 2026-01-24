/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#define DO_PRAGMA(X) _Pragma(#X)

#if defined(__GNUC__) && !defined(__clang__)
  #define DISABLE_WARNING(warningName) \
      DO_PRAGMA(GCC diagnostic push)   \
      DO_PRAGMA(GCC diagnostic ignored warningName)
  #define RESTORE_WARNING DO_PRAGMA(GCC diagnostic pop)

#elif defined(__clang__)
  #define DISABLE_WARNING(warningName) \
      DO_PRAGMA(clang diagnostic push) \
      DO_PRAGMA(clang diagnostic ignored warningName)
  #define RESTORE_WARNING DO_PRAGMA(clang diagnostic pop)

#else
  #define DISABLE_WARNING(warningName)
  #define RESTORE_WARNING
#endif
