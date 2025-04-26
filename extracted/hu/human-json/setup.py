# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['human_json']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'human-json',
    'version': '0.3.0',
    'description': 'Transform JSON Objects to human readable strings',
    'long_description': '[![Build Status](https://travis-ci.com/jakubclark/human-json.svg?branch=master)](https://travis-ci.com/jakubclark/human-json)\n\n# Human JSON\n\n`human_json` is a simple python library, that can take a JSON Object, and create a pretty string for that object.\n\nJSON is easy to transport, and quite easy to read, but requires some form of prior training to properly understand it.\nThis library allows one to transform JSON Objects into an easier to read format\n\n## Example\n\nThe following Python dictionary (which can represent a JSON Object):\n\n\n```python\n{\n    \'className\': \'ComputerScience\',\n    \'classId\': 2020,\n    \'assignments\': {\n        \'assignment1\': {\n            \'average_grade\': 5.5,\n            \'description\': \'Complete Assignment 1\',\n            \'grades\': [5, 5, 5, 7]\n        },\n        \'assignment2\': {\n            \'average_grade\': None,\n            \'description\': \'Complete Assignment 2\',\n            \'grades\': ()\n        }\n    },\n    \'students\': (\'student1\', \'student2\', \'studentabc\', 2019, None, 10.5),\n}\n```\n\nturns into the following pretty string:\n\n```text\nclassName: ComputerScience\nclassId: 2020\nassignments:\n\tassignment1:\n\t\taverage_grade: 5.5\n\t\tdescription: Complete Assignment 1\n\t\tgrades:\n\t\t\t5\n\t\t\t5\n\t\t\t5\n\t\t\t7\n\tassignment2:\n\t\taverage_grade: None\n\t\tdescription: Complete Assignment 2\n\t\tgrades:\n\t\t\t-\nstudents:\n\tstudent1\n\tstudent2\n\tstudentabc\n\t2019\n\tNone\n\t10.5\n```\n\n### Custom Prefixes\n\nYou can also specify an optional prefix, that will be prefixed to each line. A possible prefix is "* ".\nUsing this prefix, will return a markdown list. This can be directly copy-pasted into a markdown file, for example:\n\n```markdown\n* className: ComputerScience\n* classId: 2020\n* assignments:\n\t* assignment1:\n\t\t* average_grade: 5.5\n\t\t* description: Complete Assignment 1\n\t\t* grades:\n\t\t\t* 5\n\t\t\t* 5\n\t\t\t* 5\n\t\t\t* 7\n\t* assignment2:\n\t\t* average_grade: None\n\t\t* description: Complete Assignment 2\n\t\t* grades:\n\t\t\t* -\n* students:\n\t* student1\n\t* student2\n\t* studentabc\n\t* 2019\n\t* None\n\t* 10.5\n```\n### Custom Indentations\n\nYou can also specify a custom indentation. The default is `"\\t"`, but you can specify `" "` or even a number of spaces.\nBelow is an example using `2`:\n\n```text\nclassName: ComputerScience\nclassId: 2020\nassignments:\n  assignment1:\n    average_grade: 5.5\n    description: Complete Assignment 1\n    grades:\n      5\n      5\n      5\n      7\n  assignment2:\n    average_grade: None\n    description: Complete Assignment 2\n    grades:\n      -\nstudents:\n  student1\n  student2\n  studentabc\n  2019\n  None\n  10.5\n```',
    'author': 'Kuba Clark',
    'author_email': 'jakub.clark@protonmail.com',
    'url': 'https://github.com/jakubclark/human-json',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
