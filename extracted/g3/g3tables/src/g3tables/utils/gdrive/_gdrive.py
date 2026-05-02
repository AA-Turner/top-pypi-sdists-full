import gspread  # type: ignore
import json
import os
import logging
import pandas
import shutil
import typing
import pandas as pd

from platformdirs import user_config_dir


logger = logging.getLogger('g3tables.utils.gdrive')


class CredsFileManager:
    def __init__(self):
        config_dir = user_config_dir('g3tables', ensure_exists=True)
        self._file_path = os.path.join(config_dir, "creds.json")

    def validate_creds_file(self, creds_file_path: str) -> None:
        if os.path.exists(creds_file_path) is False:
            raise FileNotFoundError(f'File not found: "{creds_file_path}"')
        with open(creds_file_path, 'r') as file:
            try:
                json.load(file)
            except Exception as exp:
                raise ValueError(f'File could not be read: {exp}') from exp

    def update_creds_file(self, creds_file_path: str) -> None:
        self.validate_creds_file(creds_file_path)
        if creds_file_path != self._file_path:
            shutil.copyfile(creds_file_path, self._file_path)

    def update_creds_file_from_input(self) -> None:
        try:
            file_path = input(
                'Please provide the path to the Google Drive '
                'service account credentials file: '
                )
            self.update_creds_file(file_path)
            print('Credentials file has been updated.')
        except KeyboardInterrupt:
            print('\nCredentials file update has been aborted.')
            exit()
        except Exception as exp:
            print(f'Failed to update credentials file ({exp}).\n')
            self.update_creds_file_from_input()

    def get_creds_file(self, ensure_is_valid: bool = True) -> str:
        if ensure_is_valid is False:
            return self._file_path
        try:
            self.validate_creds_file(self._file_path)
            return self._file_path
        except Exception:
            self.update_creds_file_from_input()
            return self._file_path


def get_gspread_client(creds_file_path: str | None = None) -> gspread.Client:
    logger.info('Loading Google Drive service account credentials file')
    creds_file_manager = CredsFileManager()
    if creds_file_path:
        creds_file_manager.update_creds_file(creds_file_path)
    creds_file = creds_file_manager.get_creds_file()
    logger.info('Connecting to Google Drive repository')
    return gspread.service_account(filename=creds_file)


class TableMetadataDict(typing.TypedDict):
    id: str
    name: str
    createdTime: str
    modifiedTime: str


def list_tables_from_gdrive_with_meta(
    project: str | typing.Any | None
) -> list[TableMetadataDict]:
    client = get_gspread_client()
    logger.info('Collecting Google Drive G3 project tables')
    tables: list[TableMetadataDict] = [
        table for table in client.list_spreadsheet_files()
        ]
    if project is not None:
        logger.info('Filtering "%s" Google Drive G3 project tables', project)
        tables = [
            table for table in tables
            if str(project).casefold() in str(table['name']).casefold()
            ]
    return tables


def list_tables_from_gdrive(project: str | typing.Any | None) -> list[str]:
    tables = list_tables_from_gdrive_with_meta(project)
    return [table['name'] for table in tables]


def get_table_data_from_gdrive(
    gdrive_table_name: str,
    header_row: int = 1,
    include_sheets: typing.Optional[typing.Iterable[str]] = None,
    exclude_sheets: typing.Optional[typing.Iterable[str]] = None
) -> dict[str, pandas.DataFrame]:
    """both excluded and included == excluded"""
    client = get_gspread_client()
    try:
        logger.info('Loading spreadsheet "%s"', gdrive_table_name)
        table = client.open(gdrive_table_name)
    except gspread.exceptions.SpreadsheetNotFound:
        logger.error(
            'Unable to access spreadsheet "%s". Make sure '
            'that the table name is spelled correctly and '
            'that access to the table has been granted to '
            '"el-script@g3-spreadsheet-sync.iam.gserviceaccount.com".',
            gdrive_table_name
            )
        return {}
    sheets = {}
    for sheet in table.worksheets(exclude_hidden=True):
        if (
            (exclude_sheets and sheet.title in exclude_sheets) or
            (include_sheets and sheet.title not in include_sheets)
        ):
            logger.debug('Ignoring sheet "%s"', sheet.title)
            continue
        try:
            logger.info('Loading sheet "%s"', sheet.title)
            df = pd.DataFrame(
                sheet.get_all_records(
                    head=header_row, numericise_ignore=['all']
                )
            )

            df = df[~df.iloc[:, 4].str.contains("The script does not work with this line", na=False)]
            sheets[sheet.title] = df.reset_index(drop=True)  # Reset indexu

        except Exception as exp:
            if logger.isEnabledFor(logging.WARNING):  # optimize err str format
                err = f'Failed to load sheet "{sheet.title}"'
                if (exp_str := str(exp)):
                    err = f'{err} ({exp_str})'
                logger.warning(err)
    return sheets
