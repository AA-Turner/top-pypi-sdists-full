#!/bin/bash

# Run the pipeline to get the sequences, format them and build the databases

set -euo pipefail

cd "$(dirname "$(realpath "$0")")"

PATH="$(dirname "$(pwd)")/bin:$PATH"
export PATH

rm -rf curated_alignments muscle_alignments HMMs IMGT_sequence_files

# Rip the sequences from the imgt website. HTML may change in the future.
mkdir -p ./IMGT_sequence_files/htmlfiles
mkdir -p ./IMGT_sequence_files/fastafiles
python3 ./RipIMGT.py

# Format the alignments and handle imgt oddities to put into a consistent alignment format
mkdir -p ./curated_alignments
mkdir -p ./muscle_alignments
python3 ./FormatAlignments.py

# Build the hmms for each species and chain.
# --hand option required otherwise it will delete columns that are mainly gaps. We want 128 columns otherwise ARNACI will fall over.
mkdir -p ./HMMs
hmmbuild --hand ./HMMs/ALL.hmm ./curated_alignments/ALL.stockholm

# Turn the output HMMs file into a binary form. This is required for hmmscan that is used in ARNACI.
hmmpress -f ./HMMs/ALL.hmm

cp curated_alignments/germlines.py ../lib/python/anarci/
cp -a HMMs ../lib/python/anarci/dat/
