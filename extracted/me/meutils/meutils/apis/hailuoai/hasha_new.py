import urllib.parse


def get_js_sha(t):
    from py_mini_racer import py_mini_racer

    # 创建JavaScript运行环境
    context = py_mini_racer.MiniRacer()
     
    # 定义一个JavaScript函数
    js_code = """

    function ff(e, t, n, r, o, i, a) {
        var u = e + (t & n | ~t & r) + (o >>> 0) + a;
        return (u << i | u >>> 32 - i) + t
    }

    function gg(e, t, n, r, o, i, a) {
        var u = e + (t & r | n & ~r) + (o >>> 0) + a;
        return (u << i | u >>> 32 - i) + t
    }

    function hh(e, t, n, r, o, i, a) {
        var u = e + (t ^ n ^ r) + (o >>> 0) + a;
        return (u << i | u >>> 32 - i) + t
    }

    function ii(e, t, n, r, o, i, a) {
        var u = e + (n ^ (t | ~r)) + (o >>> 0) + a;
        return (u << i | u >>> 32 - i) + t
    }


    function rotl(e, t) {
        return e << t | e >>> 32 - t
    }


    function rotr(e, t) {
        return e << 32 - t | e >>> t
    }


    function bytesToWords(e) {
        for (var t = [], n = 0, r = 0; n < e.length; n++, r += 8)
            t[r >>> 5] |= e[n] << 24 - r % 32;
        return t
    }

    function wordsToBytes(e) {
        for (var t = [], n = 0; n < 32 * e.length; n += 8)
            t.push(e[n >>> 5] >>> 24 - n % 32 & 255);
        return t
    }

    function bytesToHex(e) {
        for (var t = [], n = 0; n < e.length; n++)
            t.push((e[n] >>> 4).toString(16)),
            t.push((15 & e[n]).toString(16));
        return t.join("")
    }


    function endian(e) {
        if (e.constructor == Number)
            return 16711935 & rotl(e, 8) | 4278255360 & rotl(e, 24);
        for (var t = 0; t < e.length; t++)
            e[t] = endian(e[t]);
        return e
    }


    function stringToBytes(e) {
        var e = unescape(encodeURIComponent(e));
        for (var t = [], n = 0; n < e.length; n++)
            t.push(255 & e.charCodeAt(n));
        return t
    }


    function sha(t){
        var t = stringToBytes(t);
        for (var u = bytesToWords(t), c = 8 * t.length, s = 1732584193, l = -271733879, f = -1732584194, d = 271733878, h = 0; h < u.length; h++)
            u[h] = (u[h] << 8 | u[h] >>> 24) & 16711935 | (u[h] << 24 | u[h] >>> 8) & 4278255360;
        u[c >>> 5] |= 128 << c % 32,
        u[(c + 64 >>> 9 << 4) + 14] = c;
        for (var p = ff, v = gg, m = hh, g = ii, h = 0; h < u.length; h += 16) {
            var y = s
              , b = l
              , w = f
              , k = d;
            s = p(s, l, f, d, u[h + 0], 7, -680876936),
            d = p(d, s, l, f, u[h + 1], 12, -389564586),
            f = p(f, d, s, l, u[h + 2], 17, 606105819),
            l = p(l, f, d, s, u[h + 3], 22, -1044525330),
            s = p(s, l, f, d, u[h + 4], 7, -176418897),
            d = p(d, s, l, f, u[h + 5], 12, 1200080426),
            f = p(f, d, s, l, u[h + 6], 17, -1473231341),
            l = p(l, f, d, s, u[h + 7], 22, -45705983),
            s = p(s, l, f, d, u[h + 8], 7, 1770035416),
            d = p(d, s, l, f, u[h + 9], 12, -1958414417),
            f = p(f, d, s, l, u[h + 10], 17, -42063),
            l = p(l, f, d, s, u[h + 11], 22, -1990404162),
            s = p(s, l, f, d, u[h + 12], 7, 1804603682),
            d = p(d, s, l, f, u[h + 13], 12, -40341101),
            f = p(f, d, s, l, u[h + 14], 17, -1502002290),
            l = p(l, f, d, s, u[h + 15], 22, 1236535329),
            s = v(s, l, f, d, u[h + 1], 5, -165796510),
            d = v(d, s, l, f, u[h + 6], 9, -1069501632),
            f = v(f, d, s, l, u[h + 11], 14, 643717713),
            l = v(l, f, d, s, u[h + 0], 20, -373897302),
            s = v(s, l, f, d, u[h + 5], 5, -701558691),
            d = v(d, s, l, f, u[h + 10], 9, 38016083),
            f = v(f, d, s, l, u[h + 15], 14, -660478335),
            l = v(l, f, d, s, u[h + 4], 20, -405537848),
            s = v(s, l, f, d, u[h + 9], 5, 568446438),
            d = v(d, s, l, f, u[h + 14], 9, -1019803690),
            f = v(f, d, s, l, u[h + 3], 14, -187363961),
            l = v(l, f, d, s, u[h + 8], 20, 1163531501),
            s = v(s, l, f, d, u[h + 13], 5, -1444681467),
            d = v(d, s, l, f, u[h + 2], 9, -51403784),
            f = v(f, d, s, l, u[h + 7], 14, 1735328473),
            l = v(l, f, d, s, u[h + 12], 20, -1926607734),
            s = m(s, l, f, d, u[h + 5], 4, -378558),
            d = m(d, s, l, f, u[h + 8], 11, -2022574463),
            f = m(f, d, s, l, u[h + 11], 16, 1839030562),
            l = m(l, f, d, s, u[h + 14], 23, -35309556),
            s = m(s, l, f, d, u[h + 1], 4, -1530992060),
            d = m(d, s, l, f, u[h + 4], 11, 1272893353),
            f = m(f, d, s, l, u[h + 7], 16, -155497632),
            l = m(l, f, d, s, u[h + 10], 23, -1094730640),
            s = m(s, l, f, d, u[h + 13], 4, 681279174),
            d = m(d, s, l, f, u[h + 0], 11, -358537222),
            f = m(f, d, s, l, u[h + 3], 16, -722521979),
            l = m(l, f, d, s, u[h + 6], 23, 76029189),
            s = m(s, l, f, d, u[h + 9], 4, -640364487),
            d = m(d, s, l, f, u[h + 12], 11, -421815835),
            f = m(f, d, s, l, u[h + 15], 16, 530742520),
            l = m(l, f, d, s, u[h + 2], 23, -995338651),
            s = g(s, l, f, d, u[h + 0], 6, -198630844),
            d = g(d, s, l, f, u[h + 7], 10, 1126891415),
            f = g(f, d, s, l, u[h + 14], 15, -1416354905),
            l = g(l, f, d, s, u[h + 5], 21, -57434055),
            s = g(s, l, f, d, u[h + 12], 6, 1700485571),
            d = g(d, s, l, f, u[h + 3], 10, -1894986606),
            f = g(f, d, s, l, u[h + 10], 15, -1051523),
            l = g(l, f, d, s, u[h + 1], 21, -2054922799),
            s = g(s, l, f, d, u[h + 8], 6, 1873313359),
            d = g(d, s, l, f, u[h + 15], 10, -30611744),
            f = g(f, d, s, l, u[h + 6], 15, -1560198380),
            l = g(l, f, d, s, u[h + 13], 21, 1309151649),
            s = g(s, l, f, d, u[h + 4], 6, -145523070),
            d = g(d, s, l, f, u[h + 11], 10, -1120210379),
            f = g(f, d, s, l, u[h + 2], 15, 718787259),
            l = g(l, f, d, s, u[h + 9], 21, -343485551),
            s = s + y >>> 0,
            l = l + b >>> 0,
            f = f + w >>> 0,
            d = d + k >>> 0
        }
        return endian([s, l, f, d])
    }


    function exports(e) {
        var n = wordsToBytes(sha(e));
        return bytesToHex(n)
    }
    """
     
    # 执行JavaScript代码，这将在内部环境中编译和执行js_code
    context.eval(js_code)
     
    # 使用已定义的JavaScript函数
    result = context.call("exports", str(t))


     
    return result
from meutils.apis.hailuoai.yy import get_js_sha

print(get_js_sha("1729947920000"))
import json
import time
import subprocess
from urllib.parse import quote

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzM0MDY1MzUsInVzZXIiOnsiaWQiOiIzMDI4MzM4Njc3NzE5NDkwNTgiLCJuYW1lIjoibWUgYmV0dGVyIiwiYXZhdGFyIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSWdTU0NoczFENHNUajFTVGs3UHNUbTd5NTNKRFg5OW84QnhwWmNWNjU2MEFKYlJnPXM5Ni1jIiwiZGV2aWNlSUQiOiIifX0.mcozMacSciz0MORdleOMS_uhrixhIlpQmFmUwvn81I4"
USER_ID = "3de88ad0-8a38-48a9-8ed3-0d63f9c71296"
DEVICE_ID = "302833759512764417"


tt = "{}000".format(int(time.time()))
tt = "1730114652000"

url = "https://hailuoai.video/api/multimodal/generate/video?device_platform=web&app_id=3001&version_code=22201&uuid={}&device_id={}&os_name=Windows&browser_name=chrome&device_memory=8&cpu_core_num=20&browser_language=zh-CN&browser_platform=Win32&screen_width=2560&screen_height=1440&unix={}".format(USER_ID, DEVICE_ID, tt)


#
# params_dict = urllib.parse.parse_qs(url)
#
# # parse_qs 返回的字典中的值是列表
# # 如果想要去掉列表，可以使用字典推导式
# params_dict_cleaned = {k: v[0] for k, v in params_dict.items()}
#
# print(params_dict_cleaned)

# 原始URL字符串
original_url = url.split("hailuoai.video")[-1]

# 替换prompt
prompt = "smile"
payload = json.dumps({
    "desc": prompt,
    "useOriginPrompt": True,
    "fileList": []
}, ensure_ascii=False)
payload = payload.replace(" ", "")
un_prompt = prompt.replace(" ", "")
payload = payload.replace(un_prompt, prompt)
# 使用quote函数进行编码
encoded_url = quote(original_url)
original_url = encoded_url.replace("/", "%2F")

print(original_url)
yy_info = "{}_{}{}ooui".format(original_url, payload, get_js_sha(tt))
print(yy_info)

yy = get_js_sha(yy_info)
print(yy)


curl_cmd = [
    'curl',
    url,
    '-H', 'content-type: application/json',
    '-H',
    'token: {}'.format(TOKEN),
    '-H',
    'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    '-H', 'yy: {}'.format(yy),
    '--data-raw',
    payload
]
print(curl_cmd)
result = subprocess.run(curl_cmd, stdout=subprocess.PIPE, text=True)
res = result.stdout
print(res)