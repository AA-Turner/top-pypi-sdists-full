#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : playwright_types
# @Time         : 2024/9/18 16:24
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


class ScreenshotRequest(BaseModel):
    html: str
    width: int = 375
    height: int = 812

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "html": """
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        h1 {
            font-size: 24px;
        }
        p {
            font-size: 16px;
        }
        @media (max-width: 600px) {
            h1 {
                font-size: 20px;
            }
            p {
                font-size: 14px;
            }
        }
    </style>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a test with responsive design.</p>
</body>
</html>
                    """
                }
            ]
        }
