

from meutils.config_utils.lark_utils import get_next_token, aget_spreadsheet_values

feishu_url = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=Hcr2i8"


if __name__ == '__main__':
    from meutils.pipe import *

    df = arun(get_next_token(feishu_url=feishu_url))


