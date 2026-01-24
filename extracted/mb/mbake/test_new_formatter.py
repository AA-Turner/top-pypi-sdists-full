#!/usr/bin/env python3
"""
Test script for the new mbake formatter.
"""

import sys
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from mbake.config import Config
from mbake.core.formatter import MakefileFormatter


def test_basic_formatting():
    """Test basic formatting functionality."""
    print("Testing basic formatting...")
    
    # Sample Makefile content with formatting issues
    input_content = """# Sample Makefile with formatting issues
CC:=gcc
CFLAGS= -Wall -Wextra -g
SOURCES=main.c \\
  utils.c \\
    helper.c

OBJECTS=$(SOURCES:.c=.o)
TARGET=myprogram

.PHONY: clean
all: $(TARGET)

$(TARGET): $(OBJECTS)
    $(CC) $(CFLAGS) -o $@ $^

%.o: %.c
    $(CC) $(CFLAGS) -c -o $@ $<

.PHONY: install
clean:
    rm -f $(OBJECTS) $(TARGET)

install:$(TARGET)
    cp $(TARGET) /usr/local/bin/
    chmod +x /usr/local/bin/$(TARGET)

test : all
    ./$(TARGET) --test

# Another phony target
.PHONY: dist

dist:
    tar -czf $(TARGET).tar.gz *.c *.h Makefile 
"""
    
    # Expected formatted output
    expected_content = """# Sample Makefile with formatting issues
CC := gcc
CFLAGS = -Wall -Wextra -g
SOURCES = main.c utils.c helper.c

OBJECTS = $(SOURCES:.c=.o)
TARGET = myprogram

.PHONY: all clean dist install test

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f $(OBJECTS) $(TARGET)

install: $(TARGET)
	cp $(TARGET) /usr/local/bin/
	chmod +x /usr/local/bin/$(TARGET)

test: all
	./$(TARGET) --test

# Another phony target
dist:
	tar -czf $(TARGET).tar.gz *.c *.h Makefile
"""
    
    # Initialize formatter
    config = Config()
    formatter = MakefileFormatter(config)
    
    # Format the content
    result = formatter.format_content(input_content)
    
    # Get formatted content
    formatted_content = ''.join(result.lines)
    
    # Compare with expected
    if formatted_content.strip() == expected_content.strip():
        print("✓ Basic formatting test passed")
        return True
    else:
        print("✗ Basic formatting test failed")
        print("Expected:")
        print(expected_content)
        print("Got:")
        print(formatted_content)
        return False


def test_conditional_formatting():
    """Test conditional formatting."""
    print("Testing conditional formatting...")
    
    input_content = """ifeq ($(DEBUG),1)
CFLAGS += -g -O0
else
CFLAGS += -O2
endif

all: program

program: main.c
	gcc $(CFLAGS) -o program main.c
"""
    
    config = Config()
    formatter = MakefileFormatter(config)
    
    result = formatter.format_content(input_content)
    formatted_content = ''.join(result.lines)
    
    # Check that conditionals are properly indented
    lines = formatted_content.split('\n')
    conditional_indented = False
    
    for line in lines:
        if line.strip().startswith('CFLAGS'):
            if line.startswith('  '):  # Should be indented
                conditional_indented = True
                break
    
    if conditional_indented:
        print("✓ Conditional formatting test passed")
        return True
    else:
        print("✗ Conditional formatting test failed")
        print("Formatted content:")
        print(formatted_content)
        return False


def test_variable_formatting():
    """Test variable assignment formatting."""
    print("Testing variable formatting...")
    
    input_content = """CC=gcc
CFLAGS=-Wall
SOURCES=main.c utils.c
"""
    
    config = Config()
    formatter = MakefileFormatter(config)
    
    result = formatter.format_content(input_content)
    formatted_content = ''.join(result.lines)
    
    # Check that variables have consistent spacing
    lines = formatted_content.split('\n')
    consistent_spacing = True
    
    for line in lines:
        if '=' in line and not line.strip().startswith('#'):
            if ' = ' not in line:  # Should have space around =
                consistent_spacing = False
                break
    
    if consistent_spacing:
        print("✓ Variable formatting test passed")
        return True
    else:
        print("✗ Variable formatting test failed")
        print("Formatted content:")
        print(formatted_content)
        return False


def main():
    """Run all tests."""
    print("Running mbake formatter tests...\n")
    
    tests = [
        test_basic_formatting,
        test_conditional_formatting,
        test_variable_formatting,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed with exception: {e}")
        print()
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
