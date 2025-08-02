# sqlite3 CMakeLists.txt

cmake_minimum_required( VERSION 3.10 )
project( sqlite3 )

message( STATUS "-- Configuring sqlite3..." )

set( SOURCES sqlite3.c )

if ( MSVC )
    add_definitions( -D_CRT_SECURE_NO_WARNINGS )
else()
    add_definitions( -g -O2 -Wall )
    if ( NOT MINGW )
        add_definitions( -fPIC )
    endif()
endif()

# options
add_definitions(
    -DSQLITE_DEFAULT_AUTOVACUUM=1
    -DSQLITE_DEFAULT_FOREIGN_KEYS=1
    -DSQLITE_DEFAULT_MEMSTATUS=0
    -DSQLITE_DEFAULT_WAL_SYNCHRONOUS=1
    -DSQLITE_DOESNT_MATCH_BLOBS
    -DSQLITE_DQS=0
    -DSQLITE_ENABLE_COLUMN_METADATA
    -DSQLITE_ENABLE_FTS4
    -DSQLITE_MAX_EXPR_DEPTH=0
    -DSQLITE_OMIT_DEPRECATED
    -DSQLITE_OMIT_SHARED_CACHE
    -DSQLITE_SECURE_DELETE
    -DSQLITE_THREADSAFE=1
    -DSQLITE_USE_ALLOCA)

if ( NOT MSVC AND NOT MINGW )
    add_definitions(-DHAVE_LOCALTIME_R)
endif()

add_library( sqlite3 STATIC ${SOURCES} )

# vi: sw=4 ts=4 et
