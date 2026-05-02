import sys
from argparse import ArgumentParser
from sppcls.check import check

# Only import tokenise if spacy is found. It is overkill to always install spacy which is normally not needed as
# tokenization is only done a single time per literary work.
try:
    from sppcls.tokenise import tokenise
except ModuleNotFoundError:
    pass


def main(argv=None):
    argument_parser = ArgumentParser(description="Accessing and processing data from the DFG-funded SPP Computational Literary Studies")

    subparsers = argument_parser.add_subparsers(dest="command")
    subparsers.required = True

    parser_tokenise = subparsers.add_parser("tokenise", help="Tokenize text file and create output tsv.",
                                            description="Tokenize text file and create output tsv.")

    parser_tokenise.add_argument("input_file", help="Path to the input txt file.")
    parser_tokenise.add_argument("output_folder", help="Path to the output folder where the output tsv will be saved.")

    parser_check = subparsers.add_parser("check", help="Compare two tsv files and check that the structures matches.",
                                         description="Compare two tsv files and check that the structures matches.")

    parser_check.add_argument("org_tokens_file_path", metavar="org-tokens-file-path",
                                 help="Path to the original tokens tsv file")
    parser_check.add_argument("project_tokens_file_path", metavar="project-tokens-file-path",
                                 help="Path to the project tokens tsv file")

    args = argument_parser.parse_args(argv)

    if args.command == "tokenise":
        in_file_path = args.input_file
        output_folder_path = args.output_folder
        tokenise.main(in_file_path, output_folder_path)

    elif args.command == "check":
        org_tokens_file_path = args.org_tokens_file_path
        project_tokens_file_path = args.project_tokens_file_path
        check.main(org_tokens_file_path, project_tokens_file_path)


if __name__ == '__main__':
    sys.exit(main())
