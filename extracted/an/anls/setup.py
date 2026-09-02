# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anls', 'anls.cli', 'anls.common', 'anls.evaluation', 'anls.metrics']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['calculate-anls = anls.cli.run:run']}

setup_kwargs = {
    'name': 'anls',
    'version': '0.0.2',
    'description': 'ANLS: Average Normalized Levenshtein Similarity',
    'long_description': '# ANLS: Average Normalized Levenshtein Similarity\n\n[![CI](https://github.com/shunk031/ANLS/actions/workflows/ci.yaml/badge.svg)](https://github.com/shunk031/ANLS/actions/workflows/ci.yaml)\n[![Release](https://github.com/shunk031/ANLS/actions/workflows/release.yaml/badge.svg)](https://github.com/shunk031/ANLS/actions/workflows/release.yaml)\n![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue?logo=python)\n[![PyPI](https://img.shields.io/pypi/v/anls.svg)](https://pypi.python.org/pypi/anls)\n\nThis python script is based on the one provided by [the Robust Reading Competition](https://rrc.cvc.uab.es/?com=introduction#) for evaluation of the InfographicVQA task.\n\n## The ANLS metric\n\nThe Average Normalized Levenshtein Similarity (ANLS) proposed by [[Biten+ ICCV\'19](https://arxiv.org/abs/1905.13648)] smoothly captures the OCR mistakes applying a slight penalization in case of correct intended responses, but badly recognized. It also makes use of a threshold of value 0.5 that dictates whether the output of the metric will be the ANLS if its value is equal or bigger than 0.5 or 0 otherwise. The key point of this threshold is to determine if the answer has been correctly selected but not properly recognized, or on the contrary, the output is a wrong text selected from the options and given as an answer.\n\nMore formally, the ANLS between the net output and the ground *truth answers is given by* equation 1. Where $N$ is the total number of questions, $M$ total number of GT answers per question, $a_{ij}$ the ground truth answers where $i = \\{0, ..., N\\}$, and $j = \\{0, ..., M\\}$, and $o_{qi}$ be the network\'s answer for the ith question $q_i$:\n\n$$\n    \\mathrm{ANLS} = \\frac{1}{N} \\sum_{i=0}^{N} \\left(\\max_{j} s(a_{ij}, o_{qi}) \\right),\n$$\n\nwhere $s(\\cdot, \\cdot)$ is defined as follows:\n\n$$\n    s(a_{ij}, o_{qi}) = \\begin{cases}\n    1 - \\mathrm{NL}(a_{ij}, o_{qi}), & \\text{if } \\mathrm{NL}(a_{ij}, o_{qi}) \\lt \\tau \\\\\n    0,                               & \\text{if } \\mathrm{NL}(a_{ij}, o_{qi}) \\ge \\tau\n    \\end{cases}\n$$\n\nThe ANLS metric is not case sensitive, but space sensitive. For example:\n\n[![Coca-Cola_example.jpg from https://rrc.cvc.uab.es/?ch=11&com=tasks](./.github/Coca-Cola_example.jpg)](https://rrc.cvc.uab.es/?ch=11&com=tasks)\n> Q: What soft drink company name is on the red disk?\n>\n> Possible answers:\n> - $a_{i1}$ : Coca Cola\n> - $a_{i2}$ : Coca Cola Company\n\n| Net output ($o_{qi}$) | $s(a_{ij}, o_{qi})$ | Score (ANLS) |\n|:---------------------:|:--------------------------------:|--------------:|\n| The Coca              | $a_{i1} = 0.44$, $a_{i2} = 0.29$ | 0.00          |\n| CocaCola              | $a_{i1} = 0.89$, $a_{i2} = 0.47$ | 0.89          |\n| Coca cola             | $a_{i1} = 1.00$, $a_{i2} = 0.53$ | 1.00          |\n| Cola                  | $a_{i1} = 0.44$, $a_{i2} = 0.23$ | 0.00          |\n| Cat                   | $a_{i1} = 0.22$, $a_{i2} = 0.12$ | 0.00          |\n\n## Installation\n\n- From pypi\n\n```shell\npip install anls\n```\n\n- From GitHub\n\n```shell\npip install git+https://github.com/shunk031/ANLS\n```\n\n## How to use\n\n## From CLI\n\n```shell\ncalculate-anls \\\n    --gold-label-file test_fixtures/evaluation/evaluate_json/gold_label.json \\\n    --submission-file test_fixtures/evaluation/evaluate_json/submission.json \\\n    --anls-threshold 0.5\n```\n\n```shell\n❯❯❯ calculate-anls --help\nusage: calculate-anls [-h] --gold-label-file GOLD_LABEL_FILE --submission-file SUBMISSION_FILE [--anls-threshold ANLS_THRESHOLD]\n\nEvaluation command using ANLS\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --gold-label-file GOLD_LABEL_FILE\n                        Path of the Ground Truth file.\n  --submission-file SUBMISSION_FILE\n                        Path of your method\'s results file.\n  --anls-threshold ANLS_THRESHOLD\n                        ANLS threshold to use (See Scene-Text VQA paper for more info.).\n```\n\n## From python script\n\n```py\n>>> from anls import anls_score\n>>> ai1 = "Coca Cola"\n>>> ai2 = "Coca Cola Company"\n>>> net_output = "The Coca"\n>>> anls_score(prediction=net_output, gold_labels=[ai1, ai2], threshold=0.5)\n0.00\n>>> net_output  = "CocaCola"\n>>> anls_score(prediction=net_output, gold_labels=[ai1, ai2], threshold=0.5)\n0.89\n>>> net_output  = "Coca cola"\n>>> anls_score(prediction=net_output, gold_labels=[ai1, ai2], threshold=0.5)\n1.0\n```\n\n## References\n\n- Biten, Ali Furkan, et al. ["Scene text visual question answering."](https://arxiv.org/abs/1905.13648) Proceedings of the IEEE/CVF international conference on computer vision. 2019.\n',
    'author': 'Shunsuke KITADA',
    'author_email': 'shunsuke.kitada.0831@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shunk031/ANLS',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
