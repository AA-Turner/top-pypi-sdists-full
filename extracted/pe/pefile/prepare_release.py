import datetime
import fileinput
import os
import re

# Generate version string
new_version = datetime.datetime.now().strftime("%Y.%-m.%-d")
year = datetime.datetime.now().year

# Update __version__ variable in pefile.py
pefile_path = "./pefile.py"
version_pattern = r"__version__\s*=\s*['\"]\d{4}\.\d{1,2}\.\d{1,2}['\"]"
new_version_line = f"__version__ = \"{new_version}\""

with fileinput.FileInput(pefile_path, inplace=True) as file:
    for line in file:
        new_line = re.sub(version_pattern, new_version_line, line)
        print(new_line, end="")

# Update version-like strings in setup.py and CITATION.cff
files_to_update = [
    "./setup.py",
    "./CITATION.cff",
]

for file_path in files_to_update:
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            new_line = re.sub(r"\d{4}\.\d{1,2}\.\d{1,2}", new_version, line)
            print(new_line, end="")

# Update last year occurrences in pefile.py, CITATION.cff, and LICENSE
files_to_update = [
    pefile_path,
    "./CITATION.cff",
    "./LICENSE",
]

for file_path in files_to_update:
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            new_line = line.replace(str(year - 1), str(year)).replace(
                str(year - 2), str(year)
            )
            print(new_line, end="")

# Update version-like strings in setup.py, CITATION.cff, and LICENSE
files_to_update = ["./CITATION.cff"]

for file_path in files_to_update:
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            new_line = re.sub(
                r"\d{4}-\d{2}-\d{2}", datetime.datetime.now().strftime("%Y-%m-%d"), line
            )  # Update the regex pattern
            print(new_line, end="")

# Log the changes
log_message = (
    f"Version updated to {new_version}. Last year occurrences updated to {year}."
)
print(log_message)
