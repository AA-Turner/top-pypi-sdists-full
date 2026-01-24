import argparse
from gqlppy import Parser

if __name__=='__main__':

   arg_parser = argparse.ArgumentParser(
      prog='gqlppy',
      description='A command-line parser invocation.'
   )
   arg_parser.add_argument('-p', '--production', default='gql_program', help='The starting production name to use.')
   arg_parser.add_argument('-s', '--starting-production', nargs='*', help='The starting production name to use.')
   arg_parser.add_argument('-k', '--kind', choices=['earley','lalr'], help='The starting production name to use.')
   arg_parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Display the post-parse tree.')
   arg_parser.add_argument('file', nargs='+', help='A file containing GQL syntax that will be parsed.')

   args = arg_parser.parse_args()

   parse_kwargs = {
      'production' : args.production
   }
   init_kwargs = {'starting_productions':args.starting_production} if args.starting_production else {}
   if args.kind:
      init_kwargs['kind'] = args.kind
   
   parser = Parser(**init_kwargs)

   for file in args.file:
      with open(file,'r') as text:
         tree = parser.parse(text,**parse_kwargs)
         if args.verbose:
            print(tree.pretty())