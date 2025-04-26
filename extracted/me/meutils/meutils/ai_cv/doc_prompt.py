#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : doc_prompt
# @Time         : 2023/9/1 19:11
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

import cv2
from paddlenlp.taskflow.document_intelligence import DocPromptTask


def _preprocess(self, inputs):
    """
    Transform the raw text to the model inputs, two steps involved:
       1) Transform the raw text to token ids.
       2) Generate the other model inputs from the raw text and token ids.
    """
    preprocess_results = self._check_input_text(inputs)
    ocr_result = []
    for example in preprocess_results:
        if "word_boxes" in example.keys():
            ocr_result = example["word_boxes"]
            example["ocr_type"] = "word_boxes"
        else:
            ocr_result = self._ocr.ocr(example["doc"], cls=True)
            example["ocr_type"] = "ppocr"
            # Compatible with paddleocr>=2.6.0.2
            ocr_result = ocr_result[0] if len(ocr_result) == 1 else ocr_result
        example["ocr_result"] = ocr_result
    self.ocr_result = ocr_result
    self.ocr_result_map = {r[1][0]: r[0] for r in ocr_result}
    return preprocess_results


DocPromptTask._preprocess = _preprocess
DocPromptTask._check_input_text = _check_input_text


def result2box(result, docprompt):
    ocr_result_map = docprompt.task_instance.ocr_result_map

    result = result.copy()
    results = result.get('result', [])
    for r in results:
        word = r.get('value', '')
        for w, b in ocr_result_map.items():
            if word in w:
                r['box'] = b
    #                 continue
    return result


def image2path(image):
    filename = f"{uuid.uuid1()}.png"
    cv2.imwrite(filename, image)
    return filename


from paddlenlp import Taskflow

# device_id=-1 本地测试用cpu ，生产可以切换成gpu，删除参数即可，默认gpu
docprompt = Taskflow("document_intelligence")


if __name__ == '__main__':
    # p = "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_cv/invoice.jpg"
    # docs = [
    #     {"doc": p, "prompt": ["发票号码是多少?", "校验码是多少?"]},
    # ]
    #
    # res = docprompt(docs)
    #
    # res = list(map(lambda r: result2box(r, docprompt=docprompt), res))
    #
    # print(res)

    p = "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_cv/invoice.jpg"
    import cv2
    image = cv2.imread(p)

    docs = [
        {"doc": image2path(image), "prompt": ["发票号码是多少?", "校验码是多少?"]},
    ]

    res = docprompt(docs)

    res = list(map(lambda r: result2box(r, docprompt=docprompt), res))

    print(res)