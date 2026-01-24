"""Textract module."""
import json
from pathlib import Path
from typing import List, Tuple, Dict

from t_ocr.ocr import OCR
from t_ocr.pages import TextractPage


class Textract(OCR):
    """
    Creates a Textract object.

    This class uses AWS Textract to read PDF files and images with OCR.
    """

    def __init__(self):
        """Initialize the Textract."""
        super().__init__()
        self.__client = None
        self.__parsing_method = "textract"

    @staticmethod
    def __get_features_type(key_values: bool, table: bool, signatures: bool) -> List[str]:
        if key_values or table or signatures:
            # Analyze Document API – Forms and Tables
            table_type = ["TABLES"] if table else []
            forms_type = ["FORMS"] if key_values else []
            signatures_type = ["SIGNATURES"] if signatures else []
            return table_type + forms_type + signatures_type
        else:
            return []

    def read_image_page(
        self,
        image_path: str,
        page_num: int = 0,
        key_values: bool = False,
        table: bool = False,
        signatures: bool = False,
        cache_data: bool = True,
    ) -> TextractPage:
        """
        Read an image from the given path and returns TextractPage object remotely at AWS.

        Args:
            image_path (str): path to image
            page_num (int, optional): page number for current instance. Defaults to 0.
            key_values (bool, optional): flag to indicate if key-values (fields-values) data need to be extracted.
                                Defaults to False.
            table (bool, optional): flag to indicate if table data need to be extracted. Defaults to False.
            cache_data (bool, optional): a flag to indicate that the result should be saved locally and
                when this function is called again with the same arguments and the same file,
                the previously saved result should be returned. (Used to save time during development).
                Defaults to True.

        Returns:
            TextractPage: page object with all data extracted

        Pricing:                          Per page               Per 10000 pages
            - just text:                  $0.0015                ~ $15
            - with table:                 $0.015                 ~ $150
            - with form (key-value pair): $0.05                  ~ $500 (10000 pages)
            - Total with table and form:  $0.065                 ~ $650 (10000 pages)
        """
        if cache_data and not self.is_local_run():
            cache_data = False

        cache_file_name = self._get_call_hash(
            action="parse_image",
            parsing_method=self.__parsing_method,
            file=image_path,
            page_num=page_num,
            key_values=key_values,
            table=table,
            signatures=signatures,
        )

        if cache_data and self._is_cache_exists(cache_file_name):
            result_file_path = self._get_cache_file(cache_file_name)
        else:
            s3_work_folder, image_s3_key = self._upload_s3_file(image_path)

            try:
                payload = self._get_parsing_configuration_payload(
                    bucket_name=self.bucket_name(),
                    image_s3_key=image_s3_key,
                    method_type="parse_image",
                    s3_work_folder=s3_work_folder,
                    parsing_tool=self.__parsing_method,
                    textract_features_type=self.__get_features_type(key_values, table, signatures),
                    page_num=page_num,
                )
                response = self._run_t_ocr_step_function(payload, work_dir=s3_work_folder)
                result_s3_key = json.loads(response["output"])["result_s3_key"]

                result_file_path = self._download_s3_file(result_s3_key)
                if cache_data:
                    self._save_cache(result_file_path, cache_file_name)
            finally:
                self._delete_s3_folder(s3_work_folder)

        with open(result_file_path) as f:
            page_data: dict = json.load(f)

        return TextractPage(blocks=page_data["blocks"], page_number=page_data["page_number"])

    def read_pdf_page(
        self,
        pdf_path: str or Path,
        page_num: int,
        key_values: bool = False,
        table: bool = False,
        signatures: bool = False,
        cache_data: bool = True,
    ) -> TextractPage:
        """Read a PDF page remotely at AWS.

        Args:
            pdf_path (str or Path): path to PDF file to parce.
            page_num (int): exact page number to read.
            key_values (bool, optional): flag to indicate if key-values (fields-values) data need to be extracted.
                                Defaults to False.
            table (bool, optional): flag to indicate if table data need to be extracted. Defaults to False.
            signatures (bool, optional): flag to indicate if signatures data need to be extracted. Defaults to False.
            cache_data (bool, optional): a flag to indicate that the result should be saved locally and
                when this function is called again with the same arguments and the same file,
                the previously saved result should be returned. (Used to save time during development).
                Defaults to True.

        Returns:
            TextractPage: TextractPage object with all data extracted
        """
        return self.read_pdf(
            pdf_path=pdf_path,
            first_page=page_num,
            last_page=page_num,
            key_values=key_values,
            table=table,
            signatures=signatures,
            cache_data=cache_data,
        )[0]

    def read_pdf(
        self,
        pdf_path: str,
        key_values: bool = False,
        table: bool = False,
        signatures: bool = False,
        first_page: int = "first",
        last_page: int = "last",
        page_numbers: List[int] = [],
        cache_data: bool = True,
    ) -> List[TextractPage]:
        """Read a PDF file and returns a list of TextractPage objects remotely at AWS.

        Args:
            pdf_path (str): path to PDF file to parce.
            key_values (bool, optional): flag to indicate if key-values (fields-values) data need to be extracted.
                                Defaults to False.
            table (bool, optional): flag to indicate if table data need to be extracted. Defaults to False.
            signatures (bool, optional): flag to indicate if signatures data need to be extracted. Defaults to False.
            first_page (int, optional): page number where to start OCR. Defaults to "first".
            last_page (int, optional): page number where to stop OCR. Defaults to "last".
            page_numbers (List[int], optional): list of pages to be read by OCR,
                prioritized over "first_page" and "last_page". Defaults to [].
            cache_data (bool, optional): a flag to indicate that the result should be saved locally and
                when this function is called again with the same arguments and the same file,
                the previously saved result should be returned. (Used to save time during development).
                Defaults to True.

        Returns:
            List[TextractPage]: list of TextractPage objects with all data extracted.
        """
        if cache_data and not self.is_local_run():
            cache_data = False

        cache_file_name = self._get_call_hash(
            action="parse_pdf",
            parsing_method=self.__parsing_method,
            file=pdf_path,
            key_values=key_values,
            table=table,
            signatures=signatures,
            first_page=first_page,
            last_page=last_page,
            page_numbers=page_numbers,
        )

        if cache_data and self._is_cache_exists(cache_file_name):
            result_file_path = self._get_cache_file(cache_file_name)
        else:
            s3_work_folder, pdf_s3_key = self._upload_s3_file(pdf_path)

            try:
                payload = self._get_parsing_configuration_payload(
                    bucket_name=self.bucket_name(),
                    pdf_s3_key=pdf_s3_key,
                    method_type="parse_pdf",
                    s3_work_folder=s3_work_folder,
                    parsing_tool=self.__parsing_method,
                    first_page=first_page,
                    last_page=last_page,
                    page_numbers=page_numbers,
                    textract_features_type=self.__get_features_type(key_values, table, signatures),
                )

                response = self._run_t_ocr_step_function(payload, work_dir=s3_work_folder)
                result_s3_key = json.loads(response["output"])["all_data_s3_key"]

                result_file_path = self._download_s3_file(result_s3_key)
                if cache_data:
                    self._save_cache(result_file_path, cache_file_name)
            finally:
                self._delete_s3_folder(s3_work_folder)

        with open(result_file_path) as f:
            parsing_results: List[dict] = json.load(f)

        textract_pages = []
        for page_data in parsing_results:
            textract_pages.append(TextractPage(blocks=page_data["blocks"], page_number=page_data["page_number"]))
        return textract_pages

    def __read_pdfs_in_parallel(
        self,
        pdfs_path: List[str],
        key_values: bool = False,
        table: bool = False,
        signatures: bool = False,
        first_page: int = "first",
        last_page: int = "last",
        page_numbers: List[int] = [],
    ) -> Dict[str, dict]:
        """Read a PDF files and returns a list of tuples with path and list of TextractPage objects remotely at AWS.

        Args:
            pdfs_path (str): list of path to PDF files to parse.
            key_values (bool, optional): flag to indicate if key-values (fields-values) data need to be extracted.
                                Defaults to False.
            table (bool, optional): flag to indicate if table data need to be extracted. Defaults to False.
            signatures (bool, optional): flag to indicate if signatures data need to be extracted. Defaults to False.
            first_page (int, optional): page number where to start OCR. Defaults to "first".
            last_page (int, optional): page number where to stop OCR. Defaults to "last".
            page_numbers (List[int], optional): list of pages to be read by OCR,
                prioritized over "first_page" and "last_page". Defaults to [].

        Returns:
            List[Tuple[str, List[TextractPage]]]: list of tuples with file path and
            TextractPage objects with all data extracted.
        """
        pdfs_path, first_page, last_page, page_numbers = self._check_parameters_for_parallel_method(
            pdfs_path, first_page, last_page, page_numbers
        )

        s3_work_folder, zip_s3_key, zip_file_names = self._zip_and_upload_s3_files(pdfs_path)

        try:
            payload = self._get_parsing_parallel_configuration_payload(
                bucket_name=self.bucket_name(),
                s3_work_folder=s3_work_folder,
                zip_s3_key=zip_s3_key,
                files_names=zip_file_names,
                parsing_payload=self._get_parsing_configuration_payload(
                    bucket_name=self.bucket_name(),
                    method_type="parse_pdf",
                    parsing_tool=self.__parsing_method,
                    first_page=first_page,
                    last_page=last_page,
                    page_numbers=page_numbers,
                    textract_features_type=self.__get_features_type(key_values, table, signatures),
                ),
            )
            response = self._run_t_ocr_parallel_step_function(payload, work_dir=s3_work_folder)

            result_s3_key = json.loads(response["output"])["all_data_s3_key"]

            result_file_path = self._download_s3_file(result_s3_key)
        finally:
            self._delete_s3_folder(s3_work_folder)

        with open(result_file_path) as f:
            parsing_results: List[dict] = json.load(f)

        pdfs_data = {}
        for pdf_path, zip_file_name in zip(pdfs_path, zip_file_names):
            try:
                pdf_result = [p_r for p_r in parsing_results if p_r["file_name"] == zip_file_name][0]
            except IndexError:
                raise Exception(
                    f"Parsing result for file '{pdf_path}' (s3 file name '{zip_file_name}') "
                    f"doesn't exist in AWS Step Function response"
                )

            pdfs_data[pdf_path] = pdf_result["result"]

        return pdfs_data

    def read_pdfs_in_parallel(
        self,
        pdfs_path: List[str],
        key_values: bool = False,
        table: bool = False,
        signatures: bool = False,
        first_page: int = "first",
        last_page: int = "last",
        page_numbers: List[int] = [],
        cache_data: bool = True,
    ) -> List[Tuple[str, List[TextractPage]]]:
        """Read a PDF files and returns a list of tuples with path and list of TextractPage objects remotely at AWS.

        Args:
            pdfs_path (str): list of path to PDF files to parse.
            key_values (bool, optional): flag to indicate if key-values (fields-values) data need to be extracted.
                                Defaults to False.
            table (bool, optional): flag to indicate if table data need to be extracted. Defaults to False.
            signatures (bool, optional): flag to indicate if signatures data need to be extracted. Defaults to False.
            first_page (int, optional): page number where to start OCR. Defaults to "first".
            last_page (int, optional): page number where to stop OCR. Defaults to "last".
            page_numbers (List[int], optional): list of pages to be read by OCR,
                prioritized over "first_page" and "last_page". Defaults to [].
            cache_data (bool, optional): a flag to indicate that the result should be saved locally and
                when this function is called again with the same arguments and the same file,
                the previously saved result should be returned. (Used to save time during development).
                Defaults to True.

        Returns:
            List[Tuple[str, List[TextractPage]]]: list of tuples with file path and
            TextractPage objects with all data extracted.
        """
        if cache_data and not self.is_local_run():
            cache_data = False

        pdfs_path, first_page, last_page, page_numbers = self._check_parameters_for_parallel_method(
            pdfs_path, first_page, last_page, page_numbers
        )

        cache_names = {}
        cashed_data = {}
        if cache_data:
            for pdf_path in pdfs_path:
                cache_file_name = self._get_call_hash(
                    action="parse_pdf",
                    parsing_method=self.__parsing_method,
                    file=pdf_path,
                    key_values=key_values,
                    table=table,
                    signatures=signatures,
                    first_page=first_page,
                    last_page=last_page,
                    page_numbers=page_numbers,
                )
                cache_names[pdf_path] = cache_file_name

                if self._is_cache_exists(cache_file_name):
                    cashed_data[pdf_path] = self._get_cache_data(cache_file_name)

        pdfs_path_for_aws = [pdf_path for pdf_path in pdfs_path if pdf_path not in cashed_data]

        pdfs_aws_result = []
        if pdfs_path_for_aws:
            pdfs_aws_result = self.__read_pdfs_in_parallel(
                pdfs_path=pdfs_path_for_aws,
                key_values=key_values,
                table=table,
                signatures=signatures,
                first_page=first_page,
                last_page=last_page,
                page_numbers=page_numbers,
            )

        pdfs_data: List[Tuple[str, List[TextractPage]]] = []
        for idx, pdf_path in enumerate(pdfs_path):
            if pdf_path in cashed_data:
                pdf_result = cashed_data[pdf_path]
            else:
                try:
                    pdf_result = pdfs_aws_result[pdf_path]
                except KeyError:
                    raise Exception(f"Parsing result for file '{pdf_path}' doesn't exist in AWS Step Function response")

                if cache_data:
                    self._save_cache_from_dict(pdf_result, cache_names[pdf_path])

            pdf_data = []
            for page_data in pdf_result:
                pdf_data.append(TextractPage(blocks=page_data["blocks"], page_number=page_data["page_number"]))

            pdfs_data.append((pdf_path, pdf_data))

        return pdfs_data
