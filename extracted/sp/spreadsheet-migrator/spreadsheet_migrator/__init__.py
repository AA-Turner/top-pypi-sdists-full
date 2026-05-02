from plugins import TestyPluginConfig


class ExcelParserConfig(TestyPluginConfig):
    name = 'spreadsheet_migrator'
    verbose_name = 'Spreadsheet migrator'
    description = 'Plugin to migrate your data from spreadsheets'
    version = '0.1'
    plugin_base_url = 'spreadsheet-migrator'
    index_reverse_name = 'spreadsheet-migrator-index'


config = ExcelParserConfig
