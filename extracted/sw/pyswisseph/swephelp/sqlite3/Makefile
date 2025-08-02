# sqlite3 makefile

CC = cc
CFLAGS = -g -O2 -Wall -fPIC
OPTS = -DHAVE_LOCALTIME_R \
       -DSQLITE_DEFAULT_AUTOVACUUM=1 \
       -DSQLITE_DEFAULT_FOREIGN_KEYS=1 \
       -DSQLITE_DEFAULT_MEMSTATUS=0 \
       -DSQLITE_DEFAULT_WAL_SYNCHRONOUS=1 \
       -DSQLITE_DOESNT_MATCH_BLOBS \
       -DSQLITE_DQS=0 \
       -DSQLITE_ENABLE_COLUMN_METADATA \
       -DSQLITE_ENABLE_FTS4 \
       -DSQLITE_MAX_EXPR_DEPTH=0 \
       -DSQLITE_OMIT_DEPRECATED \
       -DSQLITE_OMIT_SHARED_CACHE \
       -DSQLITE_SECURE_DELETE \
       -DSQLITE_THREADSAFE=1 \
       -DSQLITE_USE_ALLOCA


libsqlite3.a: sqlite3.o
	ar rcs $@ $<

libsqlite3.so: sqlite3.o
	$(CC) -shared -o $@ $<

.PHONY: clean
clean:
	rm -f *.o libsqlite3.*

sqlite3.o: sqlite3.c
	$(CC) -c -o $@ $(CFLAGS) $(OPTS) $<

# vi: set sw=4 ts=4 noet
