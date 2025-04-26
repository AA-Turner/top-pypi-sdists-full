import lark_oapi as lark
from lark_oapi.api.sheets.v3 import *


# SDK 使用说明: https://github.com/larksuite/oapi-sdk-python#readme
def main():
    # 创建client
    # 使用 user_access_token 需开启 token 配置, 并在 request_option 中配置 token
    client = lark.Client.builder() \
        .enable_set_token(True) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()



    # 构造请求对象
    request: FindSpreadsheetSheetRequest = FindSpreadsheetSheetRequest.builder() \
        .spreadsheet_token("APMRsoxW4hkIzwt693Bc9kWtnSd") \
        .sheet_id("95c9b1") \
        .request_body(Find.builder()
            .find_condition(FindCondition.builder()
                .range("PNIfrm!A1:C5")
                .match_case(True)
                .match_entire_cell(False)
                .search_by_regex(False)
                .include_formulas(False)
                .build())
            .find("hello")
            .build()) \
        .build()

    # 发起请求
    option = lark.RequestOption.builder().user_access_token("u-cyzn34LK53b8WEt6sihwnB1kiLCg1gDHra0011o00adz").build()
    response: FindSpreadsheetSheetResponse = client.sheets.v3.spreadsheet_sheet.find(request, option)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.sheets.v3.spreadsheet_sheet.find failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


if __name__ == "__main__":
    main()

# curl --location --request GET 'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/APMRsoxW4hkIzwt693Bc9kWtnSd/values/8DkMAI?valueRenderOption=ToString&dateTimeRenderOption=FormattedString' \
# --header 'Authorization: Bearer t-ce3540c5f02ac074535f1f14d64fa90fa49621c0'