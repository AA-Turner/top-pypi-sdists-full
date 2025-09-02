#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

MAJOR = 1
MINOR = 0
PATCH = 9
PRE_RELEASE = ''
# Use the following formatting: (major, minor, patch, prerelease)
VERSION = (MAJOR, MINOR, PATCH, PRE_RELEASE)

__shortversion__ = '.'.join(map(str, VERSION[:3]))
__version__ = '.'.join(map(str, VERSION[:3])) + '.'.join(VERSION[3:])

__package_name__ = 'nvidia-pyindex'
__contact_names__ = 'Jonathan Dekhtiar'
__contact_emails__ = 'jdekhtiar@nvidia.com'
__homepage__ = 'http://www.nvidia.com/'
__repository_url__ = 'http://www.nvidia.com/'
__download_url__ = 'http://www.nvidia.com/'
__description__ = 'A tool that adds the NVIDIA PIP Index to the environment.'
__license__ = 'Apache2'
__keywords__ = 'nvidia, deep learning, machine learning, supervised learning,'
__keywords__ += 'unsupervised learning, reinforcement learning, logging'
