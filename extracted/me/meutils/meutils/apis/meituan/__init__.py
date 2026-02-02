#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__.py
# @Time         : 2025/9/3 14:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

def main(arg1: dict):
    if docs := arg1:
        contents = []
        for i, doc in enumerate(docs, 1):
            _ = f"""
            [{i}] {doc.get("title")}

            {doc.get("content")}
            """
            contents.append(_)
        return {
            "result": "\n\n\n".join(contents)
        }

def main(arg1: list):
    docs = arg1

    _docs = []
    for i, doc in enumerate(docs, 1):

        doc['content'] = f"""
        [{i}] {doc.get("title")}

        {doc.get("content")}
        """.strip()
        _docs.append(doc)

    return {
        "result": _docs
    }


if __name__ == '__main__':
    print(main([]))