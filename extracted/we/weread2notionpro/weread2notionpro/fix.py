import pendulum
from weread2notionpro.notion_helper import NotionHelper
from weread2notionpro.weread_api import WeReadApi
from weread2notionpro import utils
from weread2notionpro.config import book_properties_type_dict, tz
TAG_ICON_URL = "https://www.notion.so/icons/tag_gray.svg"
USER_ICON_URL = "https://www.notion.so/icons/user-circle-filled_gray.svg"
BOOK_ICON_URL = "https://www.notion.so/icons/book_gray.svg"
rating = {"poor": "⭐️", "fair": "⭐️⭐️⭐️", "good": "⭐️⭐️⭐️⭐️⭐️"}



def insert_book_to_notion(books, index, bookId,status):
    """插入Book到Notion"""
    book = {}
    if bookId in archive_dict:
        book["书架分类"] = archive_dict.get(bookId).replace(',', '') if archive_dict.get(bookId) else None
    if bookId in notion_books:
        book.update(notion_books.get(bookId))
    bookInfo = weread_api.get_bookinfo(bookId)
    if bookInfo != None:
        book.update(bookInfo)
    readInfo = weread_api.get_read_info(bookId)
    # 研究了下这个状态不知道什么情况有的虽然读了状态还是1 markedStatus = 1 想读 4 读完 其他为在读
    readInfo.update(readInfo.get("readDetail", {}))
    readInfo.update(readInfo.get("bookInfo", {}))
    book.update(readInfo)
    book["阅读进度"] = (
        100 if (book.get("markedStatus") == 4) else book.get("readingProgress", 0)
    ) / 100
    #这里的状态拿原来的状态，不从readInfo中取，readInfo中有的不对
    book["阅读状态"] = status
    book["阅读时长"] = book.get("readingTime")
    book["阅读天数"] = book.get("totalReadDay")
    book["价格"] = book.get("price")
    book["字数"] = book.get("totalWords")
    book["评分"] = book.get("newRating")
    if book.get("newRatingDetail") and book.get("newRatingDetail").get("myRating"):
        book["我的评分"] = rating.get(book.get("newRatingDetail").get("myRating"))
    elif status == utils.get_complete_status():
        book["我的评分"] = "未评分"
    book["时间"] = (
        book.get("finishedDate")
        or book.get("lastReadingDate")
        or book.get("readingBookDate")
    )
    book["开始阅读时间"] = book.get("beginReadingDate")
    book["最后阅读时间"] = book.get("lastReadingDate")
    cover = book.get("cover").replace("/s_", "/t7_")
    if not cover or not cover.strip() or not cover.startswith("http"):
        cover = BOOK_ICON_URL
    book["封面"] = cover
    if book.get("bookId") not in notion_books:
        book["书名"] = book.get("title")
        book["BookId"] = book.get("bookId")
        book["ISBN"] = book.get("isbn")
        book["链接"] = weread_api.get_url(bookId)
        book["简介"] = book.get("intro")
        if notion_helper.author_database_id is not None:
            book["作者"] = [
                notion_helper.get_relation_id(
                    x, notion_helper.author_database_id, USER_ICON_URL
                )
                for x in book.get("author").split(" ")
            ]
        if book.get("categories"):
            book["分类"] = [
                notion_helper.get_relation_id(
                    x.get("title"), notion_helper.category_database_id, TAG_ICON_URL
                )
                for x in book.get("categories")
            ]
    properties = utils.get_properties(book, book_properties_type_dict)
    if book.get("时间"):
        notion_helper.get_date_relation(
            properties,
            pendulum.from_timestamp(book.get("时间"), tz="Asia/Shanghai"),
        )
    print(
        f"正在插入《{book.get('title')}》,一共{len(books)}本，当前是第{index+1}本 {status}。"
    )
    parent = {"database_id": notion_helper.book_database_id, "type": "database_id"}
    result = None
    if book.get("bookId") in notion_books:
        result = notion_helper.update_page(
            page_id=notion_books.get(book.get("bookId")).get("pageId"),
            properties=properties,
            cover=utils.get_icon(cover),
        )
    else:
        result = notion_helper.create_book_page(
            parent=parent,
            properties=properties,
            icon=utils.get_icon(cover),
        )
    page_id = result.get("id")
    if book.get("readDetail") and book.get("readDetail").get("data"):
        data = book.get("readDetail").get("data")
        data = {item.get("readDate"): item.get("readTime") for item in data}
        insert_read_data(page_id, data)


def insert_read_data(page_id, readTimes):
    readTimes = dict(sorted(readTimes.items()))
    filter = {"property": "书架", "relation": {"contains": page_id}}
    results = notion_helper.query_all_by_book(notion_helper.read_database_id, filter)
    for result in results:
        timestamp = result.get("properties").get("时间戳").get("number")
        duration = result.get("properties").get("时长").get("number")
        id = result.get("id")
        if timestamp in readTimes:
            value = readTimes.pop(timestamp)
            if value != duration:
                insert_to_notion(
                    page_id=id,
                    timestamp=timestamp,
                    duration=value,
                    book_database_id=page_id,
                )
    for key, value in readTimes.items():
        insert_to_notion(None, int(key), value, page_id)


def insert_to_notion(page_id, timestamp, duration, book_database_id):
    parent = {"database_id": notion_helper.read_database_id, "type": "database_id"}
    properties = {
        "标题": utils.get_title(
            pendulum.from_timestamp(timestamp, tz=tz).to_date_string()
        ),
        "日期": utils.get_date(
            start=pendulum.from_timestamp(timestamp, tz=tz).format(
                "YYYY-MM-DD HH:mm:ss"
            )
        ),
        "时长": utils.get_number(duration),
        "时间戳": utils.get_number(timestamp),
        "书架": utils.get_relation([book_database_id]),
    }
    if page_id != None:
        notion_helper.update_page(page_id=page_id, properties=properties)
    else:
        notion_helper.create_page(parent, properties, utils.get_icon("https://www.notion.so/icons/target_red.svg"))


weread_api = WeReadApi()
notion_helper = NotionHelper()
archive_dict = {}
notion_books = {}


def main():
    global notion_books
    global archive_dict
    books = weread_api.get_read_book()
    notion_books = notion_helper.get_all_book()
    for book in books:
        if book.get("markStatus") == 4:
            book["status"] = utils.get_complete_status()
        elif book.get("markStatus") in [2, 3]:
            book["status"] = "在读"
    bookshelf_books_dict = {x.get("bookId"):x for x in books}
    not_need_sync = []
    for key, value in bookshelf_books_dict.items():
        if ((key in notion_books) and (value.get("status") == notion_books.get(key).get("status"))):
            not_need_sync.append(key)
    books = [item for item in books if item.get("bookId") not in not_need_sync]
    for index, book in enumerate(books):
        insert_book_to_notion(books, index, book.get("bookId"), book.get("status"))


if __name__ == "__main__":
    main()
