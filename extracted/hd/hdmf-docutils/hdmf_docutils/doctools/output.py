"""
Module with helper classes for printing and other input/output related tasks
"""
import os
import subprocess


class PrintHelper:
    """
    Helper functions used for printing color-coded progress and status messages.
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[32m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\33[1m'
    URL = '\33[4m'
    BLINK = '\33[5m'
    BLINK2 = '\33[6m'
    SELECTED = '\33[7m'
    GRAY = '\033[90m'
    BLACK = '\033[90m'

    @classmethod
    def print(cls, text, col, indent=0, indent_step='   '):
        """
        Print color coded, indented text to standard out using Python print

        :param indent_step: String of spaces with the number of spaces per indent step (Default='    ')
        :param indent: Integer indicating the indentation level for the print (Default=0)
        :param text: The text to be printed
        :param col: One of PrintHelper.HEADER, OKBLUE etc.
        """
        indent_str = indent_step * indent
        print(col + indent_str + text + cls.ENDC)

    @staticmethod
    def print_type_hierarchy(type_hierarchy, depth=0):
        """
        Helper function used to print a hierarchy of data_types

        :param type_hierarchy: Hierarchical OrderedDict containing for each type an OrderDict of its subtype.
                               A typically way to compute this is to hdmf.spec.catalog.SpecCatalog.get_full_hierarchy()
        :param depth: Recursion depth of the print used to indent the hierarchy. This is mainly an internal
                      parameter and is typically left at the default 0 when calling the function.å
        """
        for k, v in type_hierarchy.items():
            msg = k
            PrintHelper.print(msg, PrintHelper.OKBLUE + PrintHelper.BOLD if depth == 0 else PrintHelper.OKBLUE, depth)
            PrintHelper.print_type_hierarchy(v, depth=depth+1)


########################################################
#  Internal helper classes
########################################################
class GitHashHelper(object):
    """
    Helper class for retrieving and comparing git hashes for a repo.
    """

    @classmethod
    def get_git_revision_hash(cls, cwd=None):
        """
        Helper function used to retrieve the git hash from the repo

        :param cwd: Current working directory where the git command should be run to retrieve the current hash

        :return: String with the git hash
        """
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=cwd)

    @classmethod
    def git_hash_match(cls, hashfilename, cwd=None):
        """
        Helper function used to check if the current git hash matches the version of the files

        :param hashfilename: Path to the file with the previously stored hash.
        :param cwd: Current working directory where the git command should be run to retrieve the current hash

        :return: True if match
        """
        if hashfilename is None:  # No hash file given
            return False
        elif os.path.exists(hashfilename):
            # Read the hash from the file
            f = open(hashfilename, 'rb')
            prev_hash = f.read()
            f.close()
            # Get the current hash and compare to the previous one
            curr_hash = cls.get_git_revision_hash(cwd=cwd)
            return curr_hash == prev_hash
        else:  # Hash file does not exist
            return False
