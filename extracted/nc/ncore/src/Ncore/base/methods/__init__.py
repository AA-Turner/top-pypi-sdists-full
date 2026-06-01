# Copyright 2026 zovdev
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

from __future__ import annotations
from typing import Generic, TypeVar

ReturnT = TypeVar('ReturnT')

class TLMethod(dict, Generic[ReturnT]):
    __slots__ = ()

from .account import *
from .auth import *
from .bots import *
from .channels import *
from .chatlists import *
from .contacts import *
from .folders import *
from .fragment import *
from .general import *
from .help import *
from .langpack import *
from .messages import *
from .payments import *
from .phone import *
from .photos import *
from .premium import *
from .smsjobs import *
from .stats import *
from .stickers import *
from .stories import *
from .updates import *
from .upload import *
from .users import *
