import re
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8', errors='ignore')

import execjs
import requests

cookies = {
    # '_gcl_au': '1.1.520552479.1766574531',
    # 'cna': 'w7fSISpY0WMCAcqbmNg2Xh5n',
    # '_bl_uid': 'jmmnajghj4twXOvyC4F5xtFgIsg2',
    # 'x-ap': 'ap-southeast-1',
    # 'xlly_s': '1',
    # 'sca': 'd9d12363',
    # 'atpsida': '7dea819a897619bb522a467d_1766919102_6',
    # 'acw_tc': '0a03e59217669205688717944e4458cade96377fed36e33672972e2ef0079d',
    # 'tfstk': 'gO0xKwXUrLvmG0LWpZxkI5Khh4Okt3c2ixlCSR2cfYH-CxOVSfZcCNH8EIl0lKkRBXDdoN0t_NFs1AR4II-ogjza5pvhWecqgACdCOgYG8NSa5B_C3qjdvKkEpvH-UDk2y3JKjq4DAa7_8Nb1iw6wgNLFSw_hAw7VWNhhPasCQe7T5e1cS_1VuN0FRa_5AGWw527GPasCbO8_v8ks8saCNn0HL198O_JDn38MoeOS-7TJ4_3cJZaeN9IySBzdjwR5NwIsG6swjvA8b4qNvFnnU_xpXure7MBWLUZUcM_6YTFIron32r-aH_SGrezAWgW1wwik0cQeyC6lbUYHkgmH6QSdbhsxu3kOezYl-iguffpnb3xnju-s1s7krm8vqUB8twiqX3T6VJwyvhEzYFSdFpf4dunJu4FKJFGcQdRbGrbazScFjTa_vG3wJAoZGSa23P8KQLFfG6i47eHZ8jNbuKP.',
    # 'isg': 'BHFxKhfRvFHu_RBfCvIPg21GgP0LXuXQvS7YcFOGqThXepDMnazjoKvUnA4csn0I',
    # 'ssxmod_itna': '1-eqAxuD0DgDBDcGiDODh=WD2GY07bo5DODzxC5iO7DuP4jKidbDU7YNBitDCqG=l3HF7G0DzwmG7nDDl1keDZDG9dDqx0ErXY0YOr1YCCwgDoSDfmDxeda0kZDqDkbi2b5QF/fGSglkdEXcD40cbbhrDB3DbqDyQi_wY7eD4R3Dt4DIDAYDDxDWj4DLDYoDY8noxGPtPcWWgnRTD0YDzqDgBBetxi3DA4DjBe4yBeT3DDtDAw9whPDADAfNrDDl_Y4o3cxPDYPtdarkNhwm=AnxKGTDjTPD/Rh9rGuw15zeF6WurvMpjmF8x0ODG=1=3K2xOlEF1fo26Y6eoYEmYxKQ45neqQDKADc7DzYooBwN0GxGGeQ_5BGB0q1BDwQGrnp7t4DnnQM4Qo_rlHDoYvQY4rEb0ThFbhKhxnrYxqN7GOjAbS2Ni_q8OrQR98qxWfqGmTmG4eD',
    # 'ssxmod_itna2': '1-eqAxuD0DgDBDcGiDODh=WD2GY07bo5DODzxC5iO7DuP4jKidbDU7YNBitDCqG=l3HF7G0DzwmG7eGIKpjgAIPm0uxD/i00icxo9S03_XkaAPMc5kgE1DRLY5Q8Dlmo1eXyNmtngAArSNorT4D',
}

prox = requests.get(
    'https://service.ipzan.com/core-extract?num=1&no=20250215641992155893&minute=1&format=txt&protocol=1&pool=quality&mode=whitelist&secret=28kgr1md6l5k5d').text

print(prox)

# prox = ''

proxy = {
    "https": "http://" + prox,
    "http": "http://" + prox,
}


# proxy = None

def getali231():
    # node执行231.js
    res = subprocess.run(['node', 'fireyejs.js'], capture_output=True, text=True)
    ali231 = re.search(r'###(.*?)###', res.stdout).group(1)
    print(ali231)
    return ali231

# # 只在第一次调用时编译，后面可以复用
# with open('fireyejs.js', encoding='utf-8') as f:
#     ctx = execjs.compile(f.read())
#
# def getali231():
#     # 假设 JS 里暴露了一个全局函数 getToken()
#     ali231 = ctx.call('getAli231')          # 或者 ctx.eval('getToken()')
#     print(ali231)
#     return ali231
#
_ = getali231()
print(_)


headers = {
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://chat.qwen.ai',
    'Pragma': 'no-cache',
    'Referer': 'https://chat.qwen.ai/c/guest',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Timezone': 'Sun Dec 28 2025 19:16:11 GMT+0800',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
    'X-Accel-Buffering': 'no',
    'X-Request-Id': '9135bdef-6c41-4fe6-8723-1f5940266a27',
    'bx-ua': _,
    'bx-umidtoken': 'T2gArVHIe2NFGKh-iplWivdyb0Syj0WAMgcIXr5YMQxs0esIcy1072i0wGeIqDOcR2M=',
    'bx-v': '2.5.31',
    'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'source': 'web',
    # 'Cookie': '_gcl_au=1.1.520552479.1766574531; cna=w7fSISpY0WMCAcqbmNg2Xh5n; _bl_uid=jmmnajghj4twXOvyC4F5xtFgIsg2; x-ap=ap-southeast-1; xlly_s=1; sca=d9d12363; atpsida=7dea819a897619bb522a467d_1766919102_6; acw_tc=0a03e59217669205688717944e4458cade96377fed36e33672972e2ef0079d; tfstk=gO0xKwXUrLvmG0LWpZxkI5Khh4Okt3c2ixlCSR2cfYH-CxOVSfZcCNH8EIl0lKkRBXDdoN0t_NFs1AR4II-ogjza5pvhWecqgACdCOgYG8NSa5B_C3qjdvKkEpvH-UDk2y3JKjq4DAa7_8Nb1iw6wgNLFSw_hAw7VWNhhPasCQe7T5e1cS_1VuN0FRa_5AGWw527GPasCbO8_v8ks8saCNn0HL198O_JDn38MoeOS-7TJ4_3cJZaeN9IySBzdjwR5NwIsG6swjvA8b4qNvFnnU_xpXure7MBWLUZUcM_6YTFIron32r-aH_SGrezAWgW1wwik0cQeyC6lbUYHkgmH6QSdbhsxu3kOezYl-iguffpnb3xnju-s1s7krm8vqUB8twiqX3T6VJwyvhEzYFSdFpf4dunJu4FKJFGcQdRbGrbazScFjTa_vG3wJAoZGSa23P8KQLFfG6i47eHZ8jNbuKP.; isg=BHFxKhfRvFHu_RBfCvIPg21GgP0LXuXQvS7YcFOGqThXepDMnazjoKvUnA4csn0I; ssxmod_itna=1-eqAxuD0DgDBDcGiDODh=WD2GY07bo5DODzxC5iO7DuP4jKidbDU7YNBitDCqG=l3HF7G0DzwmG7nDDl1keDZDG9dDqx0ErXY0YOr1YCCwgDoSDfmDxeda0kZDqDkbi2b5QF/fGSglkdEXcD40cbbhrDB3DbqDyQi_wY7eD4R3Dt4DIDAYDDxDWj4DLDYoDY8noxGPtPcWWgnRTD0YDzqDgBBetxi3DA4DjBe4yBeT3DDtDAw9whPDADAfNrDDl_Y4o3cxPDYPtdarkNhwm=AnxKGTDjTPD/Rh9rGuw15zeF6WurvMpjmF8x0ODG=1=3K2xOlEF1fo26Y6eoYEmYxKQ45neqQDKADc7DzYooBwN0GxGGeQ_5BGB0q1BDwQGrnp7t4DnnQM4Qo_rlHDoYvQY4rEb0ThFbhKhxnrYxqN7GOjAbS2Ni_q8OrQR98qxWfqGmTmG4eD; ssxmod_itna2=1-eqAxuD0DgDBDcGiDODh=WD2GY07bo5DODzxC5iO7DuP4jKidbDU7YNBitDCqG=l3HF7G0DzwmG7eGIKpjgAIPm0uxD/i00icxo9S03_XkaAPMc5kgE1DRLY5Q8Dlmo1eXyNmtngAArSNorT4D',
}

params = {
    'chat_id': '614da17c-3d24-4712-8649-9e25d56ce4f2',
}

json_data = {"stream": True, "version": "2.1", "incremental_output": True,
             "chat_id": "614da17c-3d24-4712-8649-9e25d56ce4f2", "chat_mode": "guest", "model": "qwen3-max-2025-10-30",
             "parent_id": "2fb4ae1c-c64d-4114-b571-7960dac32202", "messages": [
        {"fid": "eac08083-90b0-43b0-85fa-5a3a4e34c7ac", "parentId": "2fb4ae1c-c64d-4114-b571-7960dac32202",
         "childrenIds": ["f60cb605-3bb0-4c71-ba8f-a3cfaea8ed6b"], "role": "user", "content": "你好",
         "user_action": "chat", "files": [], "timestamp": 1766922940, "models": ["qwen3-max-2025-10-30"],
         "chat_type": "t2t",
         "feature_config": {"thinking_enabled": False, "output_schema": "phase", "research_mode": "normal"},
         "extra": {"meta": {"subChatType": "t2t"}}, "sub_chat_type": "t2t",
         "parent_id": "2fb4ae1c-c64d-4114-b571-7960dac32202"}], "timestamp": 1766922940}

response = requests.post(
    'https://chat.qwen.ai/api/v2/chat/completions',
    params=params,
    cookies=cookies,
    headers=headers,
    json=json_data,
    # proxies=proxy
)

print(response.text)
