#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements.  See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import glob
import os.path
from typing import Iterator, List, Union


def get_project_root():
    """Get the path to the project root"""
    return os.path.abspath(os.path.dirname(get_module_root()))


def get_module_root():
    """Get the path to the module root"""
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def read_file(path: str):
    """Read a file"""
    with open(path, "r", encoding="utf-8") as fp:
        return fp.read().strip()


def get_sql_files(path: str) -> Union[List[str], Iterator[str]]:
    """Get a list of SQL files"""
    if os.path.isfile(path):
        return [path]
    elif os.path.isdir(path):
        return glob.glob(f"{path}/**/*.sql", recursive=True)
    else:
        raise ValueError(f"{path} is not a file or a directory.")
