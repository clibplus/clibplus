#pragma once

#ifdef CLIB_TYPES
  #include <clibs/str.h>
  #include <clibs/arr.h>
  #include <clibs/map.h>
#endif

#ifdef CLIB_GC
  #include <clibs/gc.h>
#endif

#ifdef CLIB_THREADS
  #include <clibs/thread.h>
#endif
