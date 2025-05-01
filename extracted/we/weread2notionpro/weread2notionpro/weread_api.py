import hashlib
import json
import os
import re

import requests
from retrying import retry
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()
WEREAD_URL = "https://weread.qq.com/"
WEREAD_NOTEBOOKS_URL = "https://i.weread.qq.com/user/notebooks"
WEREAD_BOOKMARKLIST_URL = "https://i.weread.qq.com/book/bookmarklist"
WEREAD_CHAPTER_INFO = "https://i.weread.qq.com/book/chapterInfos"
WEREAD_READ_INFO_URL = "https://i.weread.qq.com/book/readinfo"
WEREAD_REVIEW_LIST_URL = "https://i.weread.qq.com/review/list"
WEREAD_BOOK_INFO = "https://i.weread.qq.com/book/info"
WEREAD_READDATA_DETAIL = "https://i.weread.qq.com/readdata/detail"
WEREAD_HISTORY_URL = "https://i.weread.qq.com/readdata/summary?synckey=0"
headers = {
    'User-Agent': "WeRead/8.2.5 WRBrand/xiaomi Dalvik/2.1.0 (Linux; U; Android 12; Redmi Note 7 Pro Build/SQ3A.220705.004)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'baseapi': "32",
    'appver': "8.2.5.10163885",
    'osver': "12",
    'channelId': "11",
    'basever': "8.2.5.10163885",
    'Content-Type': "application/json; charset=UTF-8"
}

class WeReadApi:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = headers
        self.refresh_token()

    def refresh_token(self):
        weread = json.loads(os.getenv("WEREAD"))
        body = {"deviceId": weread.get("generatedDeviceId"), "refreshToken": weread.get("refreshToken")}
        r = self.session.post(
            "https://api.notionhub.app/refresh-weread-token", json=body
        )
        if r.ok:
            response_data = r.json()
            vid = response_data.get("vid")
            accessToken = response_data.get("accessToken")
            if vid and accessToken:
                self.session.headers.update({"vid": str(vid), "accessToken": accessToken})
        else:
            print("Failed to refresh token")
       
        
    def handle_errcode(self, errcode):
        if errcode == -2012 or errcode == -2010:
            print(f"::error::微信读书Cookie过期了，请参考文档重新设置。https://mp.weixin.qq.com/s/B_mqLUZv7M1rmXRsMlBf7A")
            self.refresh_token()
            return True
        return False

    def get_bookshelf(self):
        r = self.session.get(
            "https://i.weread.qq.com/shelf/sync?synckey=0&teenmode=0&album=1&onlyBookid=0"
        )
        if r.ok:
            return r.json()
        else:
            errcode = r.json().get("errcode", 0)
            if self.handle_errcode(errcode):
                return self.get_bookshelf()
            raise Exception(f"Could not get bookshelf {r.text}")
        
    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def get_notebooklist(self):
        """获取笔记本列表"""
        r = self.session.get(WEREAD_NOTEBOOKS_URL)
        if r.ok:
            data = r.json()
            books = data.get("books")
            books.sort(key=lambda x: x["sort"])
            return books
        else:
            errcode = r.json().get("errcode", 0)
            if self.handle_errcode(errcode):
                return self.get_notebooklist()
            raise Exception(f"Could not get notebook list {r.text}")

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def get_bookinfo(self, bookId):
        """获取书的详情"""
        params = dict(bookId=bookId)
        r = self.session.get(WEREAD_BOOK_INFO, params=params)
        if r.ok:
            return r.json()
        else:
            errcode = r.json().get("errcode", 0)
            if self.handle_errcode(errcode):
                return self.get_bookinfo(bookId)
            print(f"Could not get book info {r.text}")

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def get_bookmark_list(self, bookId):
        params = dict(bookId=bookId)
        r = self.session.get(WEREAD_BOOKMARKLIST_URL, params=params)
        if r.ok:
            with open("bookmark.json", "w") as f:
                f.write(json.dumps(r.json(), indent=4, ensure_ascii=False))
            bookmarks = r.json().get("updated")
            return bookmarks
        else:
            errcode = r.json().get("errcode", 0)
            if self.handle_errcode(errcode):
                return self.get_bookmark_list(bookId)
            raise Exception(f"Could not get {bookId} bookmark list")

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def get_read_info(self, bookId):
        params = dict(
            noteCount=1,
            readingDetail=1,
            finishedBookIndex=1,
            readingBookCount=1,
            readingBookIndex=1,
            finishedBookCount=1,
            bookId=bookId,
            finishedDate=1,
        )
        r = self.session.get(WEREAD_READ_INFO_URL, params=params)
        if r.ok:
            return r.json()
        else:
            errcode = r.json().get("errcode", 0)
            if self.handle_errcode(errcode):
                return self.get_read_info(bookId)
            raise Exception(f"get {bookId} read info failed {r.text}")

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def get_review_list(self, bookId):
        params = dict(bookId=bookId, listType=11, mine=1, syncKey=0)
        r = self.session.get(WEREAD_REVIEW_LIST_URL, params=params)
        if r.ok:
            reviews = r.json().get("reviews")
            reviews = list(map(lambda x: x.get("review"), reviews))
            reviews = [
                {"chapterUid": 1000000, **x} if x.get("type") == 4 else x
                for x in reviews
            ]
            return reviews
        else:
            errcode = r.json().get("errcode", 0)
            if self.handle_errcode(errcode):
                return self.get_review_list(bookId)
            raise Exception(f"get {bookId} review list failed {r.text}")

    def get_api_data(self):
        r = self.session.get(WEREAD_HISTORY_URL)
        if r.ok:
            return r.json()
        else:
            errcode = r.json().get("errcode", 0)
            if self.handle_errcode(errcode):
                return self.get_api_data()
            raise Exception(f"get history data failed {r.text}")

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def get_chapter_info(self, bookId):
        body = {"bookIds": [bookId], "synckeys": [0], "teenmode": 0}
        r = self.session.post(WEREAD_CHAPTER_INFO, json=body)
        if (
            r.ok
            and "data" in r.json()
            and len(r.json()["data"]) == 1
            and "updated" in r.json()["data"][0]
        ):
            update = r.json()["data"][0]["updated"]
            update.append(
                {
                    "chapterUid": 1000000,
                    "chapterIdx": 1000000,
                    "updateTime": 1683825006,
                    "readAhead": 0,
                    "title": "点评",
                    "level": 1,
                }
            )
            return {item["chapterUid"]: item for item in update}
        else:
            errcode = r.json().get("errcode", 0)
            if self.handle_errcode(errcode):
                return self.get_chapter_info(bookId)
            raise Exception(f"get {bookId} chapter info failed {r.text}")

    def transform_id(self, book_id):
        id_length = len(book_id)
        if re.match("^\\d*$", book_id):
            ary = []
            for i in range(0, id_length, 9):
                ary.append(format(int(book_id[i : min(i + 9, id_length)]), "x"))
            return "3", ary

        result = ""
        for i in range(id_length):
            result += format(ord(book_id[i]), "x")
        return "4", [result]

    def calculate_book_str_id(self, book_id):
        md5 = hashlib.md5()
        md5.update(book_id.encode("utf-8"))
        digest = md5.hexdigest()
        result = digest[0:3]
        code, transformed_ids = self.transform_id(book_id)
        result += code + "2" + digest[-2:]

        for i in range(len(transformed_ids)):
            hex_length_str = format(len(transformed_ids[i]), "x")
            if len(hex_length_str) == 1:
                hex_length_str = "0" + hex_length_str

            result += hex_length_str + transformed_ids[i]

            if i < len(transformed_ids) - 1:
                result += "g"

        if len(result) < 20:
            result += digest[0 : 20 - len(result)]

        md5 = hashlib.md5()
        md5.update(result.encode("utf-8"))
        result += md5.hexdigest()[0:3]
        return result

    def get_url(self, book_id):
        return f"https://weread.qq.com/web/reader/{self.calculate_book_str_id(book_id)}"
