from test.test_kp_len import TestKPLen
from flashtext import KeywordProcessor
from collections import defaultdict
t = TestKPLen()

t.setUp()
test_case = t.test_cases[8]
keyword_processor = KeywordProcessor()


keyword_processor.add_keywords_from_dict(test_case['keyword_dict'])
keyword_processor.remove_keywords_from_dict(test_case['remove_keyword_dict'])

kp_len = len(keyword_processor)

new_dictionary = defaultdict(list)
for key, values in test_case['keyword_dict'].items():
    for value in values:
        if not(key in test_case['remove_keyword_dict'] and value in test_case['remove_keyword_dict'][key]):
            new_dictionary[key].append(value)

keyword_processor_two = KeywordProcessor()
keyword_processor_two.add_keywords_from_dict(new_dictionary)
kp_len_two = len(keyword_processor_two)
