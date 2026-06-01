'Process the given template to stdout using config from stdin.'
from .config import ConfigCtrl
from argparse import ArgumentParser
import sys

def main():
    parser = ArgumentParser()
    parser.add_argument('templatepath')
    args = parser.parse_args()
    cc = ConfigCtrl()
    cc.load(sys.stdin)
    cc.processtemplate(args.templatepath, sys.stdout)

if '__main__' == __name__:
    main()
