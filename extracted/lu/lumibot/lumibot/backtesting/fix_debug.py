import re

with open('thetadata_backtesting_polars.py', 'r') as f:
    lines = f.readlines()

output = []
skip_next_dedent = False
dedent_count = 0

for i, line in enumerate(lines):
    # Check if this is the debug flag declaration
    if '_THETA_PARITY_DEBUG = os.getenv' in line:
        continue  # Skip this line entirely
    
    # Check if this is a conditional debug check
    if 'if _THETA_PARITY_DEBUG:' in line:
        skip_next_dedent = True
        dedent_count = len(line) - len(line.lstrip())
        continue  # Skip the if line
    
    # If we're in a block that needs dedenting
    if skip_next_dedent:
        current_indent = len(line) - len(line.lstrip())
        # If this line is indented more than the if statement, dedent it
        if current_indent > dedent_count and line.strip():
            line = line[4:]  # Remove 4 spaces
        # Check if we've exited the block (line at same or less indent than if)
        elif line.strip() and current_indent <= dedent_count:
            skip_next_dedent = False
            dedent_count = 0
    
    output.append(line)

with open('thetadata_backtesting_polars.py', 'w') as f:
    f.writelines(output)

print("Fixed indentation")
