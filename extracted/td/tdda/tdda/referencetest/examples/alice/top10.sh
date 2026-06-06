#!/bin/sh
cat "$1" | \
tr '[:upper:]' '[:lower:]' | \
grep -oE "[a-z\']{2,}" | \
sort | \
grep -Fvwf stopwords.txt | \
uniq -c | \
sort -nr | \
head -n 10
