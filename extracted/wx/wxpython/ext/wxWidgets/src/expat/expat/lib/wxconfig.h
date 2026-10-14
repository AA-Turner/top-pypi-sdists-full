#ifndef _WXCONFIG_H_
#define _WXCONFIG_H_

#ifdef _WIN32
#  include "winconfig.h"
#elif defined(HAVE_EXPAT_CONFIG_H)
#  include <expat_config.h>
#else
#  include "macconfig.h"
#endif

#endif // _WXCONFIG_H_
