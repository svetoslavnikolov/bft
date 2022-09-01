#ifndef __error_h
#define __error_h

#include "msgprint.h"
#include <assert.h>


//#ifdef __MSCVC_
//#define errprintf(x) printf(x)
//#define eprintf(x) printf(x)
//#else
//#define errprintf(fmt, args...){fprintf(stderr, __FUNCTION__ fmt, ## args); }

#ifdef _MSC_VER
 #define eprintf(fmt, ...) msgprint("%s  : " fmt, __FUNCTION__, __VA_ARGS__);
#else
#define eprintf(fmt, args...) msgprint("%s  : " fmt, __FUNCTION__, ## args);
#endif

#define errprintf  eprintf
//#endif

#ifdef DEBUG_TRACE
#define PFUNC msgprint("%s\n",__FUNCTION__);
#else
  #define PFUNC
#endif

#if (defined(DEBUG_TRACE) || defined(DEBUG))
#define assertp(x) {msgprint("%s : in \"%s\" line %d \n", __FILE__, __FUNCTION__, __LINE__);assert(x);}
#else
  #define assertp(x) assert(x)
#endif

/* To avoid all the time "#ifdef " ...*/

#ifdef _MSC_VER
 #if (defined(DEBUG_TRACE) || defined(DEBUG))
   #define dprintf(fmt, ...)  msgprint("%s  : " fmt, __FUNCTION__,  __VA_ARGS__)
 #else
   #define dprintf(fmt, ...)
 #endif
#else
 #if (defined(DEBUG_TRACE) || defined(DEBUG))
   #define dprintf(fmt,args...)  msgprint("%s  : " fmt, __FUNCTION__,  ## args)
 #else
   #define dprintf(fmt, ...)
 #endif
#endif

#endif
