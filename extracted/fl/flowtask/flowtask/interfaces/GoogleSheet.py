from abc import ABC
from typing import Union
from pathlib import PurePath, Path
import pandas as pd
import asyncio
from googleapiclient.errors import HttpError
from .GoogleClient import GoogleClient
from ..exceptions import ComponentError


class GoogleSheetsClient(GoogleClient, ABC):
    """
    Google Sheets Client for downloading and interacting with Google Sheets.
    """

    async def download_file(
        self,
        sheet_id: str,
        worksheet_name: str = None,
        file_type: str = "dataframe"
    ) -> Union[pd.DataFrame, str]:
        """
        Download the content of a Google Sheet in various formats.

        Args:
            sheet_id (str): The ID of the Google Sheet.
            worksheet_name (str): The name of the worksheet (optional, defaults to the first sheet).
            file_type (str): Desired format - 'dataframe', 'json', 'excel', or 'csv'.

        Returns:
            pd.DataFrame or str: DataFrame if requested, or the file path for other formats.
        """
        try:
            sheets_service = await asyncio.to_thread(self.get_sheets_client)
            sheet = await asyncio.to_thread(
                sheets_service.spreadsheets().get, spreadsheetId=sheet_id
            )
            sheet = sheet.execute()
            sheet_name = worksheet_name or sheet['sheets'][0]['properties']['title']

            # Fetch data as a DataFrame
            result = await asyncio.to_thread(
                sheets_service.spreadsheets().values().get,
                spreadsheetId=sheet_id,
                range=sheet_name
            )
            result = result.execute()
            values = result.get('values', [])
            dataframe = pd.DataFrame(values[1:], columns=values[0])  # Assumes first row is the header

            # Format-based handling
            if file_type == "dataframe":
                return dataframe
            elif file_type == "json":
                return await asyncio.to_thread(dataframe.to_json)
            elif file_type == "excel":
                file_path = Path(f"{sheet_name}.xlsx")
                await asyncio.to_thread(dataframe.to_excel, file_path, index=False)
                return str(file_path)
            elif file_type == "csv":
                file_path = Path(f"{sheet_name}.csv")
                await asyncio.to_thread(dataframe.to_csv, file_path, index=False)
                return str(file_path)
            else:
                raise ValueError("Invalid file_type. Use 'dataframe', 'json', 'excel', or 'csv'.")

        except HttpError as error:
            raise ComponentError(f"Error downloading Google Sheet: {error}")
