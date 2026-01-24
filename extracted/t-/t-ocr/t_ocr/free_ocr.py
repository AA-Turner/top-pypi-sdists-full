"""Free OCR (Tesseract) module."""
import json
from enum import Enum
from pathlib import Path
from typing import List, Tuple, Dict
from t_ocr.ocr import OCR
from t_ocr.pages import Page


class PSM(Enum):
    """PSM class object with OSD (Orientation and script detection) parameters for FreeOCR tool.

    Description:
    PSM1: Automatic page segmentation with OSD.
    PSM3: Fully automatic page segmentation, but no OSD.
    PSM4: Assume page as single column of text of variable sizes (Default).
    PSM6: Assume page as single uniform block of text.
    PSM11: Sparse text. Find as much text as possible in no particular order.
    PSM12: Sparse text with OSD.
    """

    PSM1 = "--psm 1"
    """PSM1: Automatic page segmentation with OSD."""
    PSM3 = "--psm 3"
    """PSM3: Fully automatic page segmentation, but no OSD."""
    PSM4 = "--psm 4"
    """PSM4: Assume page as single column of text of variable sizes."""
    PSM6 = "--psm 6"
    """PSM6: Assume page as single uniform block of text."""
    PSM11 = "--psm 11"
    """PSM11: Sparse text. Find as much text as possible in no particular order."""
    PSM12 = "--psm 12"
    """PSM12: Sparse text with OSD."""


class FreeOCR(OCR):
    """Creates a FreeOCR object."""

    def __init__(self):
        """Check for Tesseract to be installed and initiates class object."""
        super().__init__()
        self.__parsing_method = "tesseract"

    @staticmethod
    def __get_run_config(ocr_param: PSM = PSM.PSM4):
        return rf"{ocr_param.value}"

    def read_image_page(
        self, image_path: str, page_num: int = 0, ocr_param: PSM = PSM.PSM4, cache_data: bool = True
    ) -> Page:
        """Read an image from the given path and returns Page object remotely at AWS.

        Args:
            image_path (str): path to image
            page_num (int, optional): page number for current instance. Defaults to 0.
            ocr_param (PSM, optional): Tesseract OSD (Orientation and script detection) parameter. Defaults to PSM.PSM4.
            cache_data (bool, optional): a flag to indicate that the result should be saved locally and
                when this function is called again with the same arguments and the same file,
                the previously saved result should be returned. (Used to save time during development).
                Defaults to True.

        Returns:
            Page: page object with all data extracted
        """
        if cache_data and not self.is_local_run():
            cache_data = False

        cache_file_name = self._get_call_hash(
            action="parse_image",
            parsing_method=self.__parsing_method,
            file=image_path,
            page_num=page_num,
            ocr_param=ocr_param,
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
                    tesseract_run_config=self.__get_run_config(ocr_param),
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

        return Page(full_text=page_data["full_text"], page_number=page_data["page_number"])

    def read_pdf_page(
        self, pdf_path: str or Path, page_num: int, dpi: int = 400, ocr_param: PSM = PSM.PSM4, cache_data: bool = True
    ) -> Page:
        """Read a PDF page remotely at AWS.

        Args:
            pdf_path (str or Path): path to PDF file to parse.
            page_num (int): exact page number to read.
            dpi (int, optional): image quality in DPI. Defaults to 400.
            ocr_param (PSM, optional): Tesseract OSD (Orientation and script detection) parameter. Defaults to PSM.PSM4.
            cache_data (bool, optional): a flag to indicate that the result should be saved locally and
                when this function is called again with the same arguments and the same file,
                the previously saved result should be returned. (Used to save time during development).
                Defaults to True.

        Returns:
            Page: page object with all data extracted
        """
        return self.read_pdf(
            pdf_path=pdf_path,
            first_page=page_num,
            last_page=page_num,
            dpi=dpi,
            ocr_param=ocr_param,
            cache_data=cache_data,
        )[0]

    def read_pdf(
        self,
        pdf_path: str,
        dpi: int = 400,
        ocr_param: PSM = PSM.PSM4,
        first_page: int = "first",
        last_page: int = "last",
        page_numbers: List[int] = [],
        cache_data: bool = True,
    ) -> List[Page]:
        """Read a PDF file and returns a list of Page objects remotely at AWS.

        Args:
            pdf_path (str): path to PDF file to parse.
            dpi (int, optional): image quality in DPI. Defaults to 400.
            ocr_param (PSM, optional): Tesseract OSD (Orientation and script detection) parameter. Defaults to PSM.PSM4.
            first_page (int, optional): page number where to start OCR. Defaults to "first".
            last_page (int, optional): page number where to stop OCR. Defaults to "last".
            page_numbers (List[int], optional): list of pages to be read by OCR,
                prioritized over "first_page" and "last_page". Defaults to [].
            cache_data (bool, optional): a flag to indicate that the result should be saved locally and
                when this function is called again with the same arguments and the same file,
                the previously saved result should be returned. (Used to save time during development).
                Defaults to True.

        Returns:
            List[Page]: list of Page objects with all data extracted.
        """
        if cache_data and not self.is_local_run():
            cache_data = False

        cache_file_name = self._get_call_hash(
            action="parse_pdf",
            parsing_method=self.__parsing_method,
            file=pdf_path,
            dpi=dpi,
            ocr_param=ocr_param,
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
                    dpi=dpi,
                    tesseract_run_config=self.__get_run_config(ocr_param),
                    first_page=first_page,
                    last_page=last_page,
                    page_numbers=page_numbers,
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

        pages = []
        for page_data in parsing_results:
            pages.append(Page(full_text=page_data["full_text"], page_number=page_data["page_number"]))
        return pages

    def __read_pdfs_in_parallel(
        self,
        pdfs_path: List[str],
        dpi: int = 400,
        ocr_param: PSM = PSM.PSM4,
        first_page: int = "first",
        last_page: int = "last",
        page_numbers: List[int] = [],
    ) -> Dict[str, dict]:
        """Read a PDF files and returns a list of tuples with path and list of Page objects remotely at AWS.

        Args:
            pdfs_path (str): list of path to PDF files to parse.
            dpi (int, optional): image quality in DPI. Defaults to 400.
            ocr_param (PSM, optional): Tesseract OSD (Orientation and script detection) parameter. Defaults to PSM.PSM4.
            first_page (int, optional): page number where to start OCR. Defaults to "first".
            last_page (int, optional): page number where to stop OCR. Defaults to "last".
            page_numbers (List[int], optional): list of pages to be read by OCR,
                prioritized over "first_page" and "last_page". Defaults to [].

        Returns:
            List[Tuple[str, List[Page]]]: list of tuples with file path and Page objects with all data extracted.
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
                    dpi=dpi,
                    tesseract_run_config=self.__get_run_config(ocr_param),
                    first_page=first_page,
                    last_page=last_page,
                    page_numbers=page_numbers,
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
        dpi: int = 400,
        ocr_param: PSM = PSM.PSM4,
        first_page: int = "first",
        last_page: int = "last",
        page_numbers: List[int] = [],
        cache_data: bool = True,
    ) -> List[Tuple[str, List[Page]]]:
        """Read a PDF files and returns a list of tuples with path and list of Page objects remotely at AWS.

        Args:
            pdfs_path (List[str]): list of path to PDF files to parse.
            dpi (int, optional): image quality in DPI. Defaults to 400.
            ocr_param (PSM, optional): Tesseract OSD (Orientation and script detection) parameter. Defaults to PSM.PSM4.
            first_page (int, optional): page number where to start OCR. Defaults to "first".
            last_page (int, optional): page number where to stop OCR. Defaults to "last".
            page_numbers (List[int], optional): list of pages to be read by OCR,
                prioritized over "first_page" and "last_page". Defaults to [].
            cache_data (bool, optional): a flag to indicate that the result should be saved locally and
                when this function is called again with the same arguments and the same file,
                the previously saved result should be returned. (Used to save time during development).
                Defaults to True.

        Returns:
            List[Tuple[str, List[Page]]]: list of tuples with file path and Page objects with all data extracted.
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
                    dpi=dpi,
                    ocr_param=ocr_param,
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
                dpi=dpi,
                ocr_param=ocr_param,
                first_page=first_page,
                last_page=last_page,
                page_numbers=page_numbers,
            )

        pdfs_data: List[Tuple[str, List[Page]]] = []
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
                pdf_data.append(Page(full_text=page_data["full_text"], page_number=page_data["page_number"]))

            pdfs_data.append((pdf_path, pdf_data))

        return pdfs_data
