import click

'''
Parser for dictionary-like cli parameter
usage example:
python cli.py --my-dict-option key1=value1,key2=value2
'''


class DictParamType(click.ParamType):
    name = 'dictionary'

    def convert(self, value, param, ctx):
        try:
            items = value.split(',')
            return dict(item.split('=') for item in items)
        except Exception:
            self.fail(f'{value} is not a valid dictionary format', param, ctx)


DICT = DictParamType()
