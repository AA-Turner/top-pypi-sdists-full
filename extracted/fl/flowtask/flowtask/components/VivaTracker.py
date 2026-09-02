from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import magic
import orjson
import pandas as pd
from ..exceptions import ComponentError
from .ASPX import ASPX
from ..conf import TASK_PATH


class VivaTracker(ASPX):
    """
    VivaTracker.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          VivaTracker:
          # attributes here
        ```
    """
    _version = "1.0.0"
    async def start(self, **kwargs):
        directory = Path(TASK_PATH, self._program, "reports")
        report_json_path = Path(directory).joinpath(self.report_filename)

        try:
            with open(report_json_path) as f:
                report_values_dict = orjson.loads(f.read())
        except FileNotFoundError as ex:
            raise ComponentError(
                f"Can't read the additional params file. Make sure there's a file {report_json_path}"
            ) from ex

        additional_component_attrs = {
            "base_url": "https://mso.vivatracker.com",
            "login_user_payload_key": "ctl00$ContentPlaceHolder1$txtEmail",
            "login_password_payload_key": "ctl00$ContentPlaceHolder1$txtPassword",
            "login_button_payload_key": "ctl00$ContentPlaceHolder1$btnSubmit",
            "login_button_payload_value": "Login",
            **report_values_dict,
        }

        for attr, value in additional_component_attrs.items():
            self.__setattr__(attr, value)

        self.additional_payload_params = self.process_mask("additional_payload_params")

        self._report_url = urljoin(self.base_url, f"{self.report_path}.aspx")

        return await super().start()

    async def _go_to_report(self):
        await self.aspx_session(self._report_url)

    def _get_report_payload(self, btn_id, btn_value):
        return {
            **self._views,
            **self.additional_payload_params,
            f"ctl00$ContentPlaceHolder1${btn_id}": btn_value,
        }

    def _extract_additional_values(self, soup: BeautifulSoup):
        """Extract additional values from the html report given a df column and
        an element id present in the DOM

        Args:
            response (requests.Response): http response

        Returns:
            dict: key: dataframe column, value: value extracted
        

        Example:

        ```yaml
        VivaTracker:
          credentials:
            username: VIVATRACKER_USERNAME
            password: VIVATRACKER_PASSWORD
          report_filename: sales_by_invoice_report.json
          masks:
            '{yesterday}':
            - yesterday
            - mask: '%m-%d-%Y'
            '{today}':
            - today
            - mask: '%m-%d-%Y'
        ```

    """
        self._extracted_additional_values = {}

        if hasattr(self, "additional_values_to_extract"):
            for _field, _elem_id in self.additional_values_to_extract.items():
                s_elem = soup.find(id=_elem_id)

                if s_elem:
                    self._extracted_additional_values[_field] = s_elem.get(
                        "value", s_elem.text
                    )

    async def _get_report_html(self):
        self._logger.info("Waiting for data to be displayed in html...")
        report_payload = self._get_report_payload(
            btn_id="btnSubmit", btn_value="Get Report"
        )
        payload = self._get_payload_with_views(**report_payload)
        result = await self.aspx_session(self._report_url, method="post", data=payload)
        self._extract_additional_values(result)

    async def _extract_file_report(self) -> bytes:
        self._logger.info("Downloading file...")
        report_payload = self._get_report_payload(
            btn_id=self.export_to_excel_btn_id,
            btn_value="Export to Excel",
        )
        payload = self._get_payload_with_views(**report_payload)

        self.accept = "application/xml"
        result = await self.aspx_session(
            self._report_url,
            method="post",
            data=payload,
            follow_redirects=True,
        )

        return result

    async def _get_df_from_report_bytes(self, result: bytes) -> pd.DataFrame:
        if "text/html" in magic.from_buffer(result, mime=True):
            df = pd.read_html(result, header=0)[0]
        else:
            df = pd.read_excel(result, header=0)

        df = df.assign(**self._extracted_additional_values)
        df.reset_index(drop=True, inplace=True)

        return await self.create_dataframe(df)

    async def run(self):
        await self._go_to_report()
        await self._get_report_html()
        result = await self._extract_file_report()
        df = await self._get_df_from_report_bytes(result)

        await super().run()

        self._result = df
        return self._result
