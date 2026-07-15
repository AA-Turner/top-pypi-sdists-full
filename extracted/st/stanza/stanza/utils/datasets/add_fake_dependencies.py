"""
Eval files need to have dependencies of some sort, or the eval program
fails to run, so this adds some cheap fake dependencies to a file
"""

import argparse
import sys

import stanza.utils.datasets.common as common

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='Which file to manipulate')
    parser.add_argument('outfile', help='Where to write the result')
    args = parser.parse_args()

    sentences = common.read_sentences_from_conllu(args.infile)
    sentences = [common.maybe_add_fake_dependencies(sentence) for sentence in sentences]
    common.write_sentences_to_conllu(args.outfile, sentences)
    
if __name__ == "__main__":
    main()
