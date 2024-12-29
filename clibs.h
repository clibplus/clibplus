#pragma once

#ifdef CLIB_TYPES
  #include <str.h>
  #include <arr.h>
  #include <map.h>
#endif

#ifdef CLIB_GC
  #include <gc.h>
#endif

#ifdef CLIB_THREADS
  #include <thread.h>
#endif

#ifdef CLIB_NET
  #include <Net/socket.h>
  #include <Net/request.h>
  #include <Net/web.h>
#endif
