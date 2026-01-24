"""Module for PageModel, Page, and Texstract page classes."""
from typing import List, Dict


class PageModel:
    """Class for base page model."""

    def __init__(self, page_number: int = 0):
        """Initialize the base page class.

        Args:
            page_number (int, optional): current page number. Defaults to 0.
        """
        self.raw_text: List[str] = []
        self.full_text: str = ""
        self.number: int = page_number


class Page(PageModel):
    """Page class for free (Tesseract) OCR."""

    def __init__(self, full_text: str, extra_data: str = "", page_number: int = 0):
        """Initialize the Free OCR page object with the raw_text.

        Args:
            full_text (str): full output from Tesseract recognition
            extra_data (str, optional): extra data. Not used. Defaults to "".
            page_number (int, optional): page number to pass to super class. Defaults to 0.
        """
        super().__init__(page_number=page_number)
        self.raw_text: List[str] = full_text.split("\n")
        self.full_text: str = full_text
        # self.data = self.__translate_data(extra_data)

    # def __translate_data(self, extra_data: str) -> list:
    #     """Translate the extra_data into a list of dictionaries.
    #
    #     Args:
    #         extra_data (str): raw datatable from Tesseract OCR
    #
    #     Returns:
    #         list: list of dictionaries with text block coordinates and other extracted data.
    #     """
    #     data = []
    #     data_rows = extra_data.split("\n")
    #     data_column_names = data_rows[0].split("\t")
    #     for data_row in data_rows:
    #         if "level" in data_row:
    #             continue
    #         else:
    #             row_to_convert = data_row.split("\t")
    #             converted_row = {}
    #             i = 0
    #             while i < len(data_column_names):
    #                 try:
    #                     converted_row[data_column_names[i]] = row_to_convert[i]
    #                 except IndexError:
    #                     converted_row[data_column_names[i]] = ""
    #                 i += 1
    #             data.append(converted_row)
    #     return data


class TextractSignature:
    """Signature class for Textract OCR."""

    def __init__(self, block: dict):
        self.confidence = block["Confidence"]

    def __repr__(self):
        return f"Signature (conf. - {self.confidence})"

    def __str__(self):
        return self.__repr__()


class TextractPage(PageModel):
    """Page class for Textract OCR."""

    def __init__(self, blocks: List[dict], page_number: int = 0):
        """Initialize the page object from the given list of parsed arguments .

        Args:
            blocks (List[dict]): textract blocks got from API.
            page_number (int, optional): page number to pass to super class. Defaults to 0.
        """
        super().__init__(page_number=page_number)
        self.raw_text: List[str] = self._get_raw_text(blocks)
        self.full_text: str = "\n".join(self.raw_text)
        self.key_values: Dict[str] = self._get_key_value_pair(blocks)
        self.table: List[List[str]] = self._get_table_results(blocks)
        self.signatures: List[TextractSignature] = self.__get_signatures(blocks)
        self.blocks: List[dict] = blocks

    @staticmethod
    def _get_raw_text(blocks: list):
        return [block["Text"] for block in blocks if block["BlockType"] == "LINE"]

    @staticmethod
    def _get_text(result, blocks_map) -> str:
        text: str = ""

        if "Relationships" in result:
            for relationship in result["Relationships"]:
                if relationship["Type"] == "CHILD":
                    for child_id in relationship["Ids"]:
                        word = blocks_map[child_id]
                        if word["BlockType"] == "WORD":
                            text += word["Text"] + " "
                        if word["BlockType"] == "SELECTION_ELEMENT":
                            if word["SelectionStatus"] == "SELECTED":
                                text += "X "
        return text

    @classmethod
    def _get_rows_columns_map(cls, table_info, blocks_map) -> dict:
        rows: dict = {}

        for relationship in table_info["Relationships"]:
            if relationship["Type"] == "CHILD":
                for child_id in relationship["Ids"]:
                    if child_id in blocks_map:
                        cell = blocks_map[child_id]
                        if cell["BlockType"] == "CELL":
                            row_index = cell["RowIndex"]
                            col_index = cell["ColumnIndex"]
                            if row_index not in rows:
                                rows[row_index] = {}
                            rows[row_index][col_index] = cls._get_text(cell, blocks_map)
        return rows

    @classmethod
    def _generate_table(cls, table_info, blocks_map) -> list:
        rows = cls._get_rows_columns_map(table_info, blocks_map)

        table: list = []
        for cols in rows.values():
            row_data = [str(value).strip() for value in cols.values()]
            table.append(row_data)
        return table

    @classmethod
    def _get_table_results(cls, blocks: list) -> list:
        blocks_map: dict = {}
        table_blocks: list = []

        for block in blocks:
            blocks_map[block["Id"]] = block
            if block["BlockType"] == "TABLE":
                table_blocks.append(block)

        result_table: list = []
        for table_info in table_blocks:
            result_table += cls._generate_table(table_info, blocks_map)

        final_table: list = []
        for row in result_table:
            if list(filter(None, row)):
                final_table.append(row)
        return final_table

    @classmethod
    def _get_key_value_pair(cls, blocks: list) -> dict:
        key_map, value_map, block_map = cls.__get_kv_map(blocks)
        key_value_pair = cls.__get_kv_relationship(key_map, value_map, block_map)

        return key_value_pair

    @staticmethod
    def __get_kv_map(blocks: list):
        key_map = {}
        value_map = {}
        block_map = {}

        for block in blocks:
            block_id = block["Id"]
            block_map[block_id] = block
            if block["BlockType"] == "KEY_VALUE_SET":
                if "KEY" in block["EntityTypes"]:
                    key_map[block_id] = block
                else:
                    value_map[block_id] = block

        return key_map, value_map, block_map

    @classmethod
    def __get_kv_relationship(cls, key_map, value_map, block_map):
        kvs = {}

        for block_id, key_block in key_map.items():
            value_block = cls.__find_value_block(key_block, value_map)
            key = cls._get_text(key_block, block_map)
            val = cls._get_text(value_block, block_map)
            kvs[key.strip()] = val.strip()

        return kvs

    @staticmethod
    def __find_value_block(key_block: dict, value_map: dict) -> dict:
        value_block = {}

        for relationship in key_block["Relationships"]:
            if relationship["Type"] == "VALUE":
                for value_id in relationship["Ids"]:
                    if value_id in value_map:
                        value_block = value_map[value_id]

        return value_block

    @staticmethod
    def __get_signatures(blocks: list) -> List[TextractSignature]:
        signatures: List[TextractSignature] = []
        for block in blocks:
            if block["BlockType"] == "SIGNATURE":
                signatures.append(TextractSignature(block))
        return signatures
