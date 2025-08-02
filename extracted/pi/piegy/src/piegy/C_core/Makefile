# Compiler and flags
CC = gcc

#### Common Flags ####

## Flags for Max Speed ##
CFLAGS_COMMON = -O3 -march=native -flto -std=c99 -DNDEBUG -ffp-contract=fast -funroll-loops -fomit-frame-pointer -MMD -MP
LDFLAGS_COMMON = -flto

## Flags for Debugging ##
# slower, debuggable with lldb, with Address Sanitizer. Don't use in python
#CFLAGS_COMMON = -g -std=c99 -Wall -Wextra -MMD -MP -fsanitize=address,undefined -fno-omit-frame-pointer
#LDFLAGS_COMMON = -fsanitize=address,undefined
# slower, regular build, allow lldb
#CFLAGS_COMMON = -g -std=c99 -Wall -Wextra -MMD -MP
#LDFLAGS_COMMON = 


#### OS specific ####
OS := $(shell uname)

ifeq ($(OS),Darwin)
    # macOS flags
    CFLAGS = $(CFLAGS_COMMON) -fPIC -mmacosx-version-min=11.0 -arch arm64
    LDFLAGS = $(LDFLAGS_COMMON)
else ifeq ($(OS),Linux)
    # Linux flags
    CFLAGS = $(CFLAGS_COMMON) -fPIC 
    LDFLAGS = $(LDFLAGS_COMMON)
else ifeq '$(findstring ;,$(PATH))' ';'
    # windows flags
    CFLAGS = $(CFLAGS_COMMON) -D_WIN32_WINNT=0x0A00 -DWINVER=0x0A00
    LDFLAGS = $(LDFLAGS_COMMON)
else
    # Default fallback
    CFLAGS = $(CFLAGS_COMMON) -fPIC
    LDFLAGS = $(LDFLAGS_COMMON)
endif



#### Targets and Commands ####

# Source and object files
SRC = sim_funcs.c model.c patch.c 
RUNNER_SRC = runner.c
OBJ = $(SRC:.c=.o)
RUNNER_OBJ = $(RUNNER_SRC:.c=.o)
RUNNER_DEPS = $(RUNNER_OBJ:.o=.d)
DEPS = $(OBJ:.o=.d) $(RUNNER_DEPS)

# Executable name
TEST = runner
ifeq '$(findstring ;,$(PATH))' ';'
    # windows
    SHARED_LIB = piegyc.pyd
else
    SHARED_LIB = piegyc.so
endif


# Default target
all: $(SHARED_LIB) $(TEST)

# test file
test: $(TEST)

# shared library
so: $(SHARED_LIB)

# make runner
$(TEST): $(OBJ) $(RUNNER_OBJ)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

# Shared library target
$(SHARED_LIB): $(OBJ)
	$(CC) $(CFLAGS) $(LDFLAGS) -shared -o $@ $^

# Compile source files to object files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean build files
clean:
	rm -f $(OBJ) $(RUNNER_OBJ) $(TEST) $(SHARED_LIB) $(DEPS) *.so

# Rebuild target: clean then all
re: clean all

# Include auto-generated dependency files
-include $(DEPS)

.PHONY: all clean re test so



