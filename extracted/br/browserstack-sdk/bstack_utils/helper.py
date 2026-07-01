# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import collections
import copy
import datetime
import json
import errno
import os
import shutil
import platform
import re
import subprocess
import time
import traceback
import tempfile
import multiprocessing
import threading
import sys
from math import ceil
from typing import Optional
from unittest import result
import urllib
from urllib.parse import urlparse
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack1l1l111lll1_opy_, bstack1lll1111ll1_opy_, bstack1ll1111ll_opy_,
                                    bstack1llllll11lll_opy_, bstack1111111llll_opy_, bstack11111111111_opy_, bstack11111111ll1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1lll11lll1l_opy_, bstack1ll1l1l1l1_opy_
from bstack_utils.proxy import bstack1ll11l111l1_opy_, bstack1l111ll111_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack1lll11111l1_opy_ import bstack11l11111l1_opy_
from browserstack_sdk._version import __version__
global_config = Config.bstack1lll1l11_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
automation_logger = logger_utils.get_automation_logger(__name__)
def bstack11111ll111l_opy_(config):
    return config[bstack1l1llll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ⒐")]
def bstack1111l11111l_opy_(config):
    return config[bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ⒑")]
def bstack1ll1lll11l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def is_robot_playwright_installed():
    try:
        import Browser
        return True
    except ImportError:
        return False
def is_robot_with_playwright():
    bstack1l1llll_opy_ (u"ࠥࠦࠧࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࠬࠢࡵࡥࡼࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࠬࡓࡕࡔࠡࡴࡲࡦࡴࡺࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠯ࡥࡶࡴࡽࡳࡦࡴࠬ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡘࡷࡻࡥࠡࡱࡱࡰࡾࠦࡷࡩࡧࡱࠤࡆࡒࡌࠡࡖࡋࡖࡊࡋࠠࡩࡱ࡯ࡨ࠿ࠐࠠࠡࠢࠣࠤࠥ࠰ࠠࡡࡴࡲࡦࡴࡺࡠࠡ࡫ࡶࠤ࡮ࡳࡰࡰࡴࡷࡥࡧࡲࡥࠋࠢࠣࠤࠥࠦࠠࠫࠢࡣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡠࠡ࡫ࡶࠤ࡮ࡳࡰࡰࡴࡷࡥࡧࡲࡥࠋࠢࠣࠤࠥࠦࠠࠫࠢࡣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡦࠠࡪࡵࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠦࠨࡵࡪࡨࠤࡲࡧࡲ࡬ࡧࡵࠤࡩ࡯ࡳࡵࡴ࡬ࡦࡺࡺࡩࡰࡰࠣ⠘ࠥࡸࡡࡸࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡴࡨ࡯ࡵ࠭ࡓ࡛ࠥࡻࡳࡦࡴࡶࠤࡪࡾࡰ࡭࡫ࡦ࡭ࡹࡲࡹࠡࡣࡧࡨࠥࡺࡨࡪࡵ࠾ࠤࡸ࡫ࡥࠡࡶ࡫ࡩࠥࡈࡓࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡴࡨ࡫ࡷ࡫ࡳࡴ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࡠࡳࡧࡴࡹ࡮ࡸࡥ࡮ࡧࡱࡸࡸ࠴ࡴࡹࡶࡣࠤࡼ࡮ࡩࡤࡪࠣࡴ࡮ࡴࡳࠡࡢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡃࡃ࠱࠯࠷࠹࠲࠶ࡦࠩࠋࠢࠣࠤ࡚ࠥࡨࡦࠢࡧ࡭ࡸࡺࡲࡪࡤࡸࡸ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡪࡵࠣࡸ࡭࡫ࠠ࡯ࡣࡵࡶࡴࡽࡩ࡯ࡩࠣ࡫ࡦࡺࡥ࠯࡚ࠢ࡭ࡹ࡮࡯ࡶࡶࠣ࡭ࡹ࠲ࠠࡓࡱࡥࡳࡹ࠱ࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࠋࠢࠣࠤ࡙ࠥࡄࡌࠢࡸࡷࡪࡸࡳࠡࡹ࡫ࡳࡸ࡫ࠠࡄࡋࠣ࡬ࡦࡶࡰࡦࡰࡶࠤࡹࡵࠠࡩࡣࡹࡩࠥࡦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡣࠤࡵࡸࡥ࠮࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠤࡼࡵࡵ࡭ࡦࠣ࡫ࡪࡺࠊࠡࠢࠣࠤࡸ࡯࡬ࡦࡰࡷࡰࡾࠦࡲࡦ࠯ࡵࡳࡺࡺࡥࡥࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡉ࡯ࡲࡦࡥࡷࠤ࠭ࡎࡔࡕࡒࠬࠤ࡫ࡲ࡯ࡸࠢࡷࡳࠥࡺࡨࡦࠢࡅ࡭ࡳࡧࡲࡺࠢࠫ࡫ࡗࡖࡃࠪࠢࡩࡰࡴࡽࠠ⠕ࠌࠣࠤࠥࠦࡢࡳࡧࡤ࡯࡮ࡴࡧࠡࡶ࡫ࡩ࡮ࡸࠠࡵࡧࡶࡸࡸࠦ࡯࡯ࠢࡤࠤࡧ࡯࡮ࡢࡴࡼࠤࡨࡵࡤࡦࠢࡳࡥࡹ࡮ࠠࡵࡪࡤࡸࠥࡪ࡯ࡦࡵࡱࠫࡹࠦࡨࡢࡰࡧࡰࡪࠐࠠࠡࠢࠣࡗࡪࡲࡥ࡯࡫ࡸࡱ࠰ࡘ࡯ࡣࡱࡷ࠲ࠥࡇࠠࡓࡱࡥࡳࡹ࠱ࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡕࡇࡏࠥࡻࡳࡦࡴࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱࠐࠠࠡࠢࠣࡤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡠ࠭ࠢࡶࡳࠥࡺࡨࡪࡵࠣ࡫ࡦࡺࡥࠡࡵࡷࡥࡾࡹࠠࡇࡣ࡯ࡷࡪࠦࡦࡰࡴࠣࡸ࡭࡫࡭࠯ࠌࠣࠤࠥࠦࡉ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴࠠ࡯ࡱࡷࡩ࠿ࠦࡤࡪࡵࡷࡶ࡮ࡨࡵࡵ࡫ࡲࡲࠥࡲ࡯ࡰ࡭ࡸࡴࠥ࡯ࡳࠡࡸ࡬ࡥࠥࡦࡩ࡮ࡲࡲࡶࡹࡲࡩࡣ࠰ࡰࡩࡹࡧࡤࡢࡶࡤࡤ࠱ࠦ࡮ࡰࡶࠍࠤࠥࠦࠠࡡ࡫ࡰࡴࡴࡸࡴࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡤ࠳ࠦࡔࡩࡧࠣࡔࡾࡖࡉࠡࡲࡤࡧࡰࡧࡧࡦࠢࡣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡦࠊࠡࠢࠣࠤࡲࡧࡹࠡࡰࡲࡸࠥ࡫ࡸࡱࡱࡶࡩࠥࡧࠠࡵࡱࡳ࠱ࡱ࡫ࡶࡦ࡮ࠣࡔࡾࡺࡨࡰࡰࠣࡱࡴࡪࡵ࡭ࡧࠣࡳ࡫ࠦࡴࡩࡣࡷࠤࡳࡧ࡭ࡦࠢ⠗ࠤࡹ࡮ࡥࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠍࠤࠥࠦࠠ࡭ࡱࡲ࡯ࡺࡶࠠࡪࡵࠣࡸ࡭࡫ࠠࡳࡧ࡯࡭ࡦࡨ࡬ࡦࠢࡦ࡬ࡪࡩ࡫࠯ࠌࠣࠤࠥࠦࡒࡦ࡮ࡤࡸ࡮ࡵ࡮ࡴࡪ࡬ࡴࠥࡺ࡯ࠡࡢ࡬ࡷࡤࡸ࡯ࡣࡱࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡠ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠬ࠮ࡦ࠺ࠋࠢࠣࠤࠥ࠰ࠠࡡ࡫ࡶࡣࡷࡵࡢࡰࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࡟ࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠫ࠭ࡥࠦ⦒ࠡࡖࡵࡹࡪࠦ࡯࡯࡮ࡼࠤࡼ࡮ࡥ࡯ࠢࡣࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠱ࡧࡸ࡯ࡸࡵࡨࡶࡥࠐࠠࠡࠢࠣࠤࠥ࠮ࡴࡩࡧࠣࡤࡇࡸ࡯ࡸࡵࡨࡶࡥࠦ࡫ࡦࡻࡺࡳࡷࡪࠠ࡭࡫ࡥࡶࡦࡸࡹࠪࠢ࡬ࡷࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠪࠡࡢ࡬ࡷࡤࡸ࡯ࡣࡱࡷࡣࡼ࡯ࡴࡩࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠮ࠩࡡࠢ⦕ࠤ࡙ࡸࡵࡦࠢࡲࡲࡱࡿࠠࡧࡱࡵࠤࡷࡧࡷࠡࡢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡥࠐࠠࠡࠢࠣࠤࠥࡱࡥࡺࡹࡲࡶࡩ࠳࡬ࡪࡤࡵࡥࡷࡿࠠࡴࡧࡷࡹࡵࡹࠠࠩࡧ࠱࡫࠳࠲ࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡅࡳࡪࡲࡰ࡫ࡧࡐ࡮ࡨࡲࡢࡴࡼ࠭࠳ࠐࠠࠡࠢࠣࡍࡒࡖࡏࡓࡖࡄࡒ࡙ࡀࠠࡕࡪ࡬ࡷࠥ࡮ࡥ࡭ࡲࡨࡶࠥ࡯ࡳࠡࡐࡒࡘࠥࡳࡵࡵࡷࡤࡰࡱࡿࠠࡦࡺࡦࡰࡺࡹࡩࡷࡧࠣࡻ࡮ࡺࡨࠋࠢࠣࠤࠥࡦࡩࡴࡡࡵࡳࡧࡵࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡤ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠩࠫࡣ࠲ࠥࡈ࡯ࡵࡪࠣࡇࡆࡔࠠࡳࡧࡷࡹࡷࡴࠠࡕࡴࡸࡩࠥࡹࡩ࡮ࡷ࡯ࡸࡦࡴࡥࡰࡷࡶࡰࡾࠦࡩࡧࠌࠣࠤࠥࠦࡴࡩࡧࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡪࡤࡷࠥࡈࡏࡕࡊࠣࡤࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠲ࡨࡲࡰࡹࡶࡩࡷࡦࠠࡂࡐࡇࠎࠥࠦࠠࠡࡢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡥࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠢࠫࡩ࠳࡭࠮࠭ࠢࡤࠤࡸ࡮ࡡࡳࡧࡧࠤࡈࡏࠠࡪ࡯ࡤ࡫ࡪࠦࡵࡴࡧࡧࠤ࡫ࡵࡲࠡࡤࡲࡸ࡭ࠐࠠࠡࠢࠣࡆࡷࡵࡷࡴࡧࡵ࠱ࡱ࡯ࡢࡳࡣࡵࡽࠥࡺࡥࡴࡶࡶࠤࡦࡴࡤࠡࡴࡤࡻ࠲ࡖࡗࠡࡶࡨࡷࡹࡹࠩ࠯ࠢࡗ࡬ࡪࠦࡨࡦ࡮ࡳࡩࡷࠦࡩࡵࡵࡨࡰ࡫ࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡱࡪࡴࡸࡣࡦࠌࠣࠤࠥࠦࡤࡪࡵ࡭ࡳ࡮ࡴࡴ࡯ࡧࡶࡷࠥ⠚ࠠࡤࡣ࡯ࡰࡪࡸࡳࠡࡰࡨࡩࡩ࡯࡮ࡨࠢࡰࡹࡹࡻࡡ࡭ࠢࡨࡼࡨࡲࡵࡴ࡫ࡲࡲࠥࡳࡵࡴࡶࠣࡧࡴࡳࡢࡪࡰࡨࠤࡼ࡯ࡴࡩࠌࠣࠤࠥࠦࡠ࡯ࡱࡷࠤ࡮ࡹ࡟ࡳࡱࡥࡳࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡢ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩ࠮ࠩࡡࠢࡤࡸࠥࡺࡨࡦࠢࡦࡥࡱࡲࠠࡴ࡫ࡷࡩࠥ࠮ࡴࡩ࡫ࡶࠤ࡮ࡹࠠࡦࡺࡤࡧࡹࡲࡹࠋࠢࠣࠤࠥࡽࡨࡢࡶࠣࡤ࡮ࡹ࡟ࡳࡣࡺࡣࡷࡵࡢࡰࡶࡢࡴࡼࡥࡢࡪࡰࡤࡶࡾࡥࡦ࡭ࡱࡺࠬ࠮ࡦࠠࡣࡧ࡯ࡳࡼࠦࡤࡰࡧࡶ࠭࠳ࠐࠠࠡࠢࠣࠦࠧࠨ⒒")
    try:
        import robot
        import playwright
    except ImportError:
        return False
    try:
        try:
            from importlib.metadata import distribution as _1llll1l1ll1l_opy_
            from importlib.metadata import PackageNotFoundError as _1lll11l11ll1_opy_
        except ImportError:
            return False
        try:
            _1llll1l1ll1l_opy_(bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ⒓"))
            return True
        except _1lll11l11ll1_opy_:
            return False
    except Exception as e:
        try:
            logger.debug(bstack1l1llll_opy_ (u"ࠧ࡯ࡳࡠࡴࡲࡦࡴࡺ࡟ࡸ࡫ࡷ࡬ࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡱࡵ࡯࡬ࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣ⒔").format(e))
        except Exception:
            pass
        return False
def robot_pw_binary_flow():
    bstack1l1llll_opy_ (u"ࠨࠢࠣࡕ࡬ࡲ࡬ࡲࡥࠡࡵࡲࡹࡷࡩࡥࠡࡱࡩࠤࡹࡸࡵࡵࡪࠣࡪࡴࡸࠠࠣࡔࡲࡦࡴࡺࠠࠬࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡴࡩࡴࡲࡹ࡬࡮ࠠࡵࡪࡨࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡲ࡯ࡸࠤ࠱ࠎࠥࠦࠠࠡࡅࡲࡲࡸࡵ࡬ࡪࡦࡤࡸࡴࡸ࠮ࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡗࡶࡺ࡫ࠠࡧࡱࡵࠤࡇࡕࡔࡉ࠼ࠍࠤࠥࠦࠠࠡࠢ࠭ࠤࡗࡵࡢࡰࡶࠣ࠯ࠥࡦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠭ࡣࡴࡲࡻࡸ࡫ࡲࡡࠢࠫࡆࡷࡵࡷࡴࡧࡵࠤࡰ࡫ࡹࡸࡱࡵࡨࠥࡲࡩࡣࡴࡤࡶࡾ࠯ࠊࠡࠢࠣࠤࠥࠦࠪࠡࡔࡲࡦࡴࡺࠠࠬࠢࡵࡥࡼࠦࡠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡣࠤࡰ࡫ࡹࡸࡱࡵࡨࠥࡲࡩࡣࡴࡤࡶ࡮࡫ࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠫࡩ࠳࡭࠮ࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡆࡴࡤࡳࡱ࡬ࡨࡑ࡯ࡢࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡫ࡶࠤࡹ࡮ࡥࠡࡩࡤࡸࡪࠦࡴࡩࡧࠣࡗࡉࡑࠠࡶࡵࡨࡷࠥࡺ࡯ࠡࡦࡨࡧ࡮ࡪࡥࠡࡹ࡫ࡩࡹ࡮ࡥࡳࠢࡷࡳࠥࡸ࡯ࡶࡶࡨࠤࡦࠦࡒࡰࡤࡲࡸࠥࡸࡵ࡯ࠌࠣࠤࠥࠦࡴࡩࡴࡲࡹ࡬࡮ࠠࡵࡪࡨࠤࡧ࡯࡮ࡢࡴࡼࠤ࠭࡭ࡒࡑࡅࠬࠤ࡫ࡲ࡯ࡸࠢࡹࡷࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࠢࠫࡌ࡙࡚ࡐࠪࠢࡩࡰࡴࡽ࠮ࠡࡄࡲࡸ࡭ࠦࡒࡰࡤࡲࡸ࠰ࡖࡗࠋࠢࠣࠤࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡯࡯ࡵࠣࡲࡪ࡫ࡤࠡࡤ࡬ࡲࡦࡸࡹࠡࡴࡲࡹࡹ࡯࡮ࡨࠢࡥࡩࡨࡧࡵࡴࡧࠣࡸ࡭࡫ࠠࡣ࡫ࡱࡥࡷࡿࠧࡴࠢࡳࡶࡴࡪࡵࡤࡶࠣࡱࡴࡪࡵ࡭ࡧࡶࠎࠥࠦࠠࠡࠪࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠮ࠣࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠬࠤࡴࡽ࡮ࠡࡶ࡫ࡩࠥࡶࡥࡳ࠯ࡷࡩࡸࡺࠠࡦࡸࡨࡲࡹࠦࡰࡪࡲࡨࡰ࡮ࡴࡥ࠯ࠌࠣࠤࠥࠦࠢࠣࠤ⒕")
    return is_robot_playwright_installed() or is_robot_with_playwright()
def is_raw_robot_pw_binary_flow():
    bstack1l1llll_opy_ (u"ࠢࠣࠤࡕࡳࡧࡵࡴࠡ࠭ࠣࡶࡦࡽࠠࡡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡤࠥࡕࡎࡍ࡛ࠣࠬࡪࡾࡣ࡭ࡷࡧࡩࡸࠦࡂࡳࡱࡺࡷࡪࡸࠠ࡭࡫ࡥࡶࡦࡸࡹࠪ࠰ࠍࠤࠥࠦࠠࡅ࡫ࡶ࡮ࡴ࡯࡮ࡵࡰࡨࡷࡸࠦࡣࡰࡰࡷࡶࡦࡩࡴ࠻ࠢࡷ࡬࡮ࡹࠠࡳࡧࡷࡹࡷࡴࡳࠡࡖࡵࡹࡪࠦ࡯࡯࡮ࡼࠤࡼ࡮ࡥ࡯ࠢࡷ࡬ࡪࠦࡵࡴࡧࡵࠤ࡮ࡹࠠࡶࡵ࡬ࡲ࡬ࠦࡲࡢࡹࠍࠤࠥࠦࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣ࡯ࡪࡿࡷࡰࡴࡧࠤࡱ࡯ࡢࡳࡣࡵ࡭ࡪࡹࠠࠩࡧ࠱࡫࠳ࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡄࡲࡩࡸ࡯ࡪࡦࡏ࡭ࡧࡸࡡࡳࡻࠬࠎࠥࠦࠠࠡࡃࡑࡈࠥࡪ࡯ࡦࡵࠣࡒࡔ࡚ࠠࡩࡣࡹࡩࠥࡦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠭ࡣࡴࡲࡻࡸ࡫ࡲࡡࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨ࠳ࠦࡔࡩࡧࠣࡩࡽࡶ࡬ࡪࡥ࡬ࡸࠏࠦࠠࠡࠢࡣࡲࡴࡺࠠࡪࡵࡢࡶࡴࡨ࡯ࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡥࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠪࠬࡤࠥࡩ࡬ࡢࡷࡶࡩࠥ࡫࡮ࡧࡱࡵࡧࡪࡹࠠࡵࡪࡨࠤࡩ࡯ࡳ࡫ࡱ࡬ࡲࡹࡴࡥࡴࡵࠣࡥࡹࠐࠠࠡࠢࠣࡸ࡭࡫ࠠࡤࡣ࡯ࡰࠥࡹࡩࡵࡧࠣࡷ࡮ࡴࡣࡦࠢࡣ࡭ࡸࡥࡲࡰࡤࡲࡸࡤࡽࡩࡵࡪࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠨࠪࡢࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫࡮ࡧࡱࡵࡧࡪࠦࡩࡵࠢࡲࡲࠏࠦࠠࠡࠢ࡬ࡸࡸࠦ࡯ࡸࡰࠣࠬࡸ࡫ࡥࠡ࡫ࡷࡷࠥࡪ࡯ࡤࡵࡷࡶ࡮ࡴࡧࠪ࠰ࠍࠤࠥࠦࠠࡖࡵࡨࡨࠥࡨࡹࠡࡥࡤࡰࡱࠦࡳࡪࡶࡨࡷࠥࡺࡨࡢࡶࠣࡲࡪ࡫ࡤࠡࡶࡲࠤࡩ࡯ࡳࡵ࡫ࡱ࡫ࡺ࡯ࡳࡩࠢࡵࡥࡼࠦࡒࡰࡤࡲࡸ࠰ࡖࡗࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࡆࡷࡵࡷࡴࡧࡵ࠱ࡱ࡯ࡢࡳࡣࡵࡽࠥࡘ࡯ࡣࡱࡷ࠯ࡕ࡝ࠠࠩࡧ࠱࡫࠳ࠦࡳࡦࡶࡸࡴࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩࡶࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠋࠢࠣࠤࠥࡪࡥࡵࡧࡦࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡲࡩ࠯ࡲࡼࠤࡦࡴࡤࠡࡶ࡫ࡩࠥ࡭ࡥࡵࡡࡦࡦࡹࡥࡥࡷࡧࡱࡸࠥ࡬ࡩ࡭ࡶࡨࡶࠥ࡯࡮ࠡ࡯ࡲࡨࡺࡲࡥࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡤࡺࡥࡴࡶ࠱ࡴࡾ࠯࠮ࠋࠢࠣࠤࠥࠨࠢࠣ⒖")
    return is_robot_with_playwright() and not is_robot_playwright_installed()
_1llll111l111_opy_ = None
_1lllll11ll1l_opy_ = None
def _1lll1l1l111l_opy_():
    global _1llll111l111_opy_, _1lllll11ll1l_opy_
    if _1llll111l111_opy_ is None:
        _1llll111l111_opy_ = robot_pw_binary_flow()
    if _1lllll11ll1l_opy_ is None:
        _1lllll11ll1l_opy_ = is_raw_robot_pw_binary_flow()
def cached_robot_pw_binary_flow():
    bstack1l1llll_opy_ (u"ࠣࠤࠥࡇࡦࡩࡨࡦࡦࠣࡥࡨࡩࡥࡴࡵࡲࡶࠥ࡬࡯ࡳࠢࡣࡶࡴࡨ࡯ࡵࡡࡳࡻࡤࡨࡩ࡯ࡣࡵࡽࡤ࡬࡬ࡰࡹࠫ࠭ࡥ࠴ࠊࠡࠢࠣࠤࡎࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡴࠢ࡯ࡥࡿ࡯࡬ࡺࠢࡲࡲࠥ࡬ࡩࡳࡵࡷࠤࡨࡧ࡬࡭ࠢࡷࡳࠥࡧࡶࡰ࡫ࡧࠤࡪࡼࡡ࡭ࡷࡤࡸ࡮ࡴࡧࠡࡦ࡬ࡷࡹࡸࡩࡣࡷࡷ࡭ࡴࡴࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠌࠣࠤࠥࠦࡤࡶࡴ࡬ࡲ࡬ࠦ࡭ࡰࡦࡸࡰࡪࠦࡩ࡮ࡲࡲࡶࡹࠦࠨࡴࡱࡰࡩ࡙ࠥࡄࡌࠢ࡬ࡲ࡮ࡺࠠࡱࡣࡷ࡬ࡸࠦࡩ࡮ࡲࡲࡶࡹࠦࡨࡦ࡮ࡳࡩࡷ࠴ࡰࡺࠢࡹࡩࡷࡿࠠࡦࡣࡵࡰࡾ࠯࠮ࠋࠢࠣࠤࠥࠨࠢࠣ⒗")
    if _1llll111l111_opy_ is None:
        _1lll1l1l111l_opy_()
    return _1llll111l111_opy_
def cached_raw_robot_pw_binary_flow():
    bstack1l1llll_opy_ (u"ࠤࠥࠦࡈࡧࡣࡩࡧࡧࠤࡦࡩࡣࡦࡵࡶࡳࡷࠦࡦࡰࡴࠣࡤ࡮ࡹ࡟ࡳࡣࡺࡣࡷࡵࡢࡰࡶࡢࡴࡼࡥࡢࡪࡰࡤࡶࡾࡥࡦ࡭ࡱࡺࠬ࠮ࡦ࠮ࠣࠤࠥ⒘")
    if _1lllll11ll1l_opy_ is None:
        _1lll1l1l111l_opy_()
    return _1lllll11ll1l_opy_
def is_behave_playwright_installed():
    try:
        import behave
        import playwright
        return True
    except ImportError:
        return False
def bstack1llll111ll1l_opy_(obj):
    values = []
    bstack1llll11llll1_opy_ = re.compile(bstack1l1llll_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢ⒙"), re.I)
    for key in obj.keys():
        if bstack1llll11llll1_opy_.match(key):
            values.append(obj[key])
    return values
def get_custom_tags(config):
    tags = []
    tags.extend(bstack1llll111ll1l_opy_(os.environ))
    tags.extend(bstack1llll111ll1l_opy_(config))
    return tags
def bstack1llll1ll11l1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def _1lll11llll1l_opy_(bstack1llll1ll1l11_opy_):
    bstack1l1llll_opy_ (u"ࠦࠧࠨࡔࡳ࡫ࡰࠤࡼ࡮ࡩࡵࡧࡶࡴࡦࡩࡥ࠼ࠢࡷࡶࡪࡧࡴࠡࡰࡲࡲ࠲ࡹࡴࡳ࡫ࡱ࡫ࡸࠦࡡ࡯ࡦࠣࡩࡲࡶࡴࡺࠢࡶࡸࡷ࡯࡮ࡨࡵࠣࡥࡸࠦ࡮ࡰࡶ࠰ࡷࡪࡺࠠࠩࡐࡲࡲࡪ࠯࠮ࠣࠤࠥ⒚")
    if not isinstance(bstack1llll1ll1l11_opy_, str):
        return None
    normalized = bstack1llll1ll1l11_opy_.strip()
    return normalized if len(normalized) > 0 else None
def _1llll1l1llll_opy_(argv):
    bstack1l1llll_opy_ (u"ࠧࠨࠢࡓࡧࡤࡨࠥ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷࡑࡦࡴࡡࡨࡧࡰࡩࡳࡺࡏࡱࡶ࡬ࡳࡳࡹ࠮ࡵࡧࡶࡸࡕࡲࡡ࡯ࡋࡧࠤ࡫ࡸ࡯࡮ࠢࡤࡶ࡬ࡼ࠮ࠋࠢࠣࠤ࡙ࠥࡵࡱࡲࡲࡶࡹࡹࠠࡣࡱࡷ࡬ࠥ࠭࠭࠮ࡨ࡯ࡥ࡬ࠦࡶࡢ࡮ࡸࡩࠬࠦࡡ࡯ࡦࠣࠫ࠲࠳ࡦ࡭ࡣࡪࡁࡻࡧ࡬ࡶࡧࠪࠤ࡫ࡵࡲ࡮ࡵ࠱ࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡔ࡯࡯ࡧࠣࡻ࡭࡫࡮ࠋࠢࠣࠤࠥࡧࡢࡴࡧࡱࡸࠥࡵࡲࠡࡹ࡫ࡩࡳࠦࡴࡩࡧࠣࡪࡱࡧࡧࠡࡪࡤࡷࠥࡴ࡯ࠡࡷࡶࡥࡧࡲࡥࠡࡸࡤࡰࡺ࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣ⒛")
    bstack1lll11ll1l1l_opy_ = bstack1l1llll_opy_ (u"࠭࠭࠮ࡽࢀࠫ⒜").format(bstack1111111ll1l_opy_)
    for index, bstack1lll1l111lll_opy_ in enumerate(argv):
        if not isinstance(bstack1lll1l111lll_opy_, str):
            continue
        if bstack1lll1l111lll_opy_ == bstack1lll11ll1l1l_opy_:
            bstack1llll1lll1ll_opy_ = argv[index + 1] if index + 1 < len(argv) else None
            if not bstack1llll1lll1ll_opy_ or (isinstance(bstack1llll1lll1ll_opy_, str) and bstack1llll1lll1ll_opy_.startswith(bstack1l1llll_opy_ (u"ࠧ࠮࠯ࠪ⒝"))):
                return None
            return bstack1llll1lll1ll_opy_
        if bstack1lll1l111lll_opy_.startswith(bstack1l1llll_opy_ (u"ࠨࡽࢀࡁࠬ⒞").format(bstack1lll11ll1l1l_opy_)):
            return bstack1lll1l111lll_opy_[len(bstack1lll11ll1l1l_opy_) + 1:] or None
    return None
def _1lll11lll11l_opy_(config):
    bstack1l1llll_opy_ (u"ࠤࠥࠦࡗ࡫ࡡࡥࠢࡷࡩࡸࡺࡍࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶࡒࡴࡹ࡯࡯࡯ࡵ࠱ࡸࡪࡹࡴࡑ࡮ࡤࡲࡎࡪࠬࠡࡨࡤࡰࡱ࡯࡮ࡨࠢࡥࡥࡨࡱࠠࡵࡱࠣࡥࠥ࡬࡬ࡢࡶࠣࡸࡪࡹࡴࡑ࡮ࡤࡲࡎࡪ࠮ࠣࠤࠥ⒟")
    if not isinstance(config, dict):
        return None
    nested = config.get(bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡎࡣࡱࡥ࡬࡫࡭ࡦࡰࡷࡓࡵࡺࡩࡰࡰࡶࠫ⒠"))
    if isinstance(nested, dict):
        bstack1lll1l1lll11_opy_ = _1lll11llll1l_opy_(nested.get(bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡒ࡯ࡥࡳࡏࡤࠨ⒡")))
        if bstack1lll1l1lll11_opy_:
            return bstack1lll1l1lll11_opy_
    return _1lll11llll1l_opy_(config.get(bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡓࡰࡦࡴࡉࡥࠩ⒢")))
def bstack11lll1l1l1_opy_(config=None, argv=None, env=None):
    bstack1l1llll_opy_ (u"ࠨࠢࠣࡔࡨࡷࡴࡲࡶࡦࠢࡷ࡬ࡪࠦࡔࡦࡵࡷࠤࡕࡲࡡ࡯ࠢࡌࡈࠥ࡬ࡲࡰ࡯ࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡣ࡭࡫ࡨࡲࡹ࠳ࡳࡪࡦࡨࠤ࡮ࡴࡰࡶࡶࡶ࠲ࠏࠦࠠࠡࠢࡓࡶࡪࡩࡥࡥࡧࡱࡧࡪࠦࠨࡄࡎࡌࠤࡃࠦࡅࡏࡘࠣࡂࠥࡉࡏࡏࡈࡌࡋ࠮ࡀࠊࠡࠢࠣࠤࠥࠦ࠱࠯ࠢࡆࡐࡎࠦࡡࡳࡩࠣࠤ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶࡐࡥࡳࡧࡧࡦ࡯ࡨࡲࡹࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡴࡦࡵࡷࡔࡱࡧ࡮ࡊࡦࠣࠬࡂࡼࡡ࡭ࡷࡨࠤࡴࡸࠠࡴࡲࡤࡧࡪ࠳ࡳࡦࡲࡤࡶࡦࡺࡥࡥࠫࠍࠤࠥࠦࠠࠡࠢ࠵࠲ࠥࡋ࡮ࡷࠢࡹࡥࡷࠦࠠࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡕࡒࡁࡏࡡࡌࡈࠏࠦࠠࠡࠢࠣࠤ࠸࠴ࠠࡄࡱࡱࡪ࡮࡭ࠠࠡࠢࡷࡩࡸࡺࡍࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶࡒࡴࡹ࡯࡯࡯ࡵ࠱ࡸࡪࡹࡴࡑ࡮ࡤࡲࡎࡪࠬࠡࡶ࡫ࡩࡳࠦࡦ࡭ࡣࡷࠤࡹ࡫ࡳࡵࡒ࡯ࡥࡳࡏࡤࠋࠢࠣࠤࠥ࡝ࡨࡪࡶࡨࡷࡵࡧࡣࡦࠢ࡬ࡷࠥࡺࡲࡪ࡯ࡰࡩࡩࡁࠠࡦ࡯ࡳࡸࡾࠦࡳࡵࡴ࡬ࡲ࡬ࡹࠠࡢࡴࡨࠤࡹࡸࡥࡢࡶࡨࡨࠥࡧࡳࠡࡰࡲࡸ࠲ࡹࡥࡵ࠰ࠣࡖࡪࡺࡵࡳࡰࡶࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࡷࡩࡧࡱࠤࡦࡨࡳࡦࡰࡷ࠲ࠥࡔࡥࡷࡧࡵࠤࡷࡧࡩࡴࡧࡶࠤ⠙ࠦࡡ࡯ࡻࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡦࡴࡵࡳࡷࠦࡲࡦࡵࡲࡰࡻ࡫ࡳࠡࡶࡲࠤࡓࡵ࡮ࡦࠢࡶࡳࠥࡨࡵࡪ࡮ࡧࠎࠥࠦࠠࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡥࡱࡽࡡࡺࡵࠣࡴࡷࡵࡣࡦࡧࡧࡷ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ⒣")
    try:
        argv = sys.argv if argv is None else argv
        env = os.environ if env is None else env
        config = {} if config is None else config
        bstack1lll1l11l1l1_opy_ = _1lll11llll1l_opy_(_1llll1l1llll_opy_(argv))
        if bstack1lll1l11l1l1_opy_:
            return bstack1lll1l11l1l1_opy_
        bstack1llll1lll11l_opy_ = _1lll11llll1l_opy_(env.get(bstack1lllllllll11_opy_))
        if bstack1llll1lll11l_opy_:
            return bstack1llll1lll11l_opy_
        return _1lll11lll11l_opy_(config)
    except Exception as error:
        logger.debug(bstack1l1llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡩࡸࡵ࡬ࡷ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡴࡱࡧ࡮ࠡ࡫ࡧ࠾ࠥࢁࡽࠣ⒤").format(str(error)))
        return None
def bstack1llll11l11l1_opy_(bstack1lll1lll1l1l_opy_):
    if not bstack1lll1lll1l1l_opy_:
        return bstack1l1llll_opy_ (u"ࠨࠩ⒥")
    return bstack1l1llll_opy_ (u"ࠤࡾࢁࠥ࠮ࡻࡾࠫࠥ⒦").format(bstack1lll1lll1l1l_opy_.name, bstack1lll1lll1l1l_opy_.email)
def bstack1111l111111_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1lllll11llll_opy_ = repo.common_dir
        info = {
            bstack1l1llll_opy_ (u"ࠥࡷ࡭ࡧࠢ⒧"): repo.head.commit.hexsha,
            bstack1l1llll_opy_ (u"ࠦࡸ࡮࡯ࡳࡶࡢࡷ࡭ࡧࠢ⒨"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1llll_opy_ (u"ࠧࡨࡲࡢࡰࡦ࡬ࠧ⒩"): repo.active_branch.name,
            bstack1l1llll_opy_ (u"ࠨࡴࡢࡩࠥ⒪"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1llll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࠥ⒫"): bstack1llll11l11l1_opy_(repo.head.commit.committer),
            bstack1l1llll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࡣࡩࡧࡴࡦࠤ⒬"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1llll_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࠤ⒭"): bstack1llll11l11l1_opy_(repo.head.commit.author),
            bstack1l1llll_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡢࡨࡦࡺࡥࠣ⒮"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1llll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧ⒯"): repo.head.commit.message,
            bstack1l1llll_opy_ (u"ࠧࡸ࡯ࡰࡶࠥ⒰"): repo.git.rev_parse(bstack1l1llll_opy_ (u"ࠨ࠭࠮ࡵ࡫ࡳࡼ࠳ࡴࡰࡲ࡯ࡩࡻ࡫࡬ࠣ⒱")),
            bstack1l1llll_opy_ (u"ࠢࡤࡱࡰࡱࡴࡴ࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣ⒲"): bstack1lllll11llll_opy_,
            bstack1l1llll_opy_ (u"ࠣࡹࡲࡶࡰࡺࡲࡦࡧࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦ⒳"): subprocess.check_output([bstack1l1llll_opy_ (u"ࠤࡪ࡭ࡹࠨ⒴"), bstack1l1llll_opy_ (u"ࠥࡶࡪࡼ࠭ࡱࡣࡵࡷࡪࠨ⒵"), bstack1l1llll_opy_ (u"ࠦ࠲࠳ࡧࡪࡶ࠰ࡧࡴࡳ࡭ࡰࡰ࠰ࡨ࡮ࡸࠢⒶ")]).strip().decode(
                bstack1l1llll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫⒷ")),
            bstack1l1llll_opy_ (u"ࠨ࡬ࡢࡵࡷࡣࡹࡧࡧࠣⒸ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1llll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡳࡠࡵ࡬ࡲࡨ࡫࡟࡭ࡣࡶࡸࡤࡺࡡࡨࠤⒹ"): repo.git.rev_list(
                bstack1l1llll_opy_ (u"ࠣࡽࢀ࠲࠳ࢁࡽࠣⒺ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1lll1l1l1ll1_opy_ = []
        for remote in remotes:
            bstack1llll1l11l1l_opy_ = {
                bstack1l1llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢⒻ"): remote.name,
                bstack1l1llll_opy_ (u"ࠥࡹࡷࡲࠢⒼ"): remote.url,
            }
            bstack1lll1l1l1ll1_opy_.append(bstack1llll1l11l1l_opy_)
        bstack1lll1l1111l1_opy_ = {
            bstack1l1llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤⒽ"): bstack1l1llll_opy_ (u"ࠧ࡭ࡩࡵࠤⒾ"),
            **info,
            bstack1l1llll_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡹࠢⒿ"): bstack1lll1l1l1ll1_opy_
        }
        bstack1lll1l1111l1_opy_ = bstack1lll1llllll1_opy_(bstack1lll1l1111l1_opy_)
        return bstack1lll1l1111l1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l1llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥⓀ").format(err))
        return {}
def bstack1lll1lll1lll_opy_(bstack1lll1ll1llll_opy_=None):
    bstack1l1llll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡉࡨࡸࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡸࡶࡥࡤ࡫ࡩ࡭ࡨࡧ࡬࡭ࡻࠣࡪࡴࡸ࡭ࡢࡶࡷࡩࡩࠦࡦࡰࡴࠣࡅࡎࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࡸࡷࡪࠦࡣࡢࡵࡨࡷࠥ࡬࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧࡱ࡯ࡨࡪࡸࠠࡪࡰࠣࡸ࡭࡫ࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡪࡴࡲࡤࡦࡴࡶࠤ࠭ࡲࡩࡴࡶ࠯ࠤࡴࡶࡴࡪࡱࡱࡥࡱ࠯࠺ࠡࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡑࡳࡳ࡫࠺ࠡࡏࡲࡲࡴ࠳ࡲࡦࡲࡲࠤࡦࡶࡰࡳࡱࡤࡧ࡭࠲ࠠࡶࡵࡨࡷࠥࡩࡵࡳࡴࡨࡲࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡞ࡳࡸ࠴ࡧࡦࡶࡦࡻࡩ࠮ࠩ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡈࡱࡵࡺࡹࠡ࡮࡬ࡷࡹ࡛ࠦ࡞࠼ࠣࡑࡺࡲࡴࡪ࠯ࡵࡩࡵࡵࠠࡢࡲࡳࡶࡴࡧࡣࡩࠢࡺ࡭ࡹ࡮ࠠ࡯ࡱࠣࡷࡴࡻࡲࡤࡧࡶࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࡤ࠭ࠢࡵࡩࡹࡻࡲ࡯ࡵࠣ࡟ࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡱࡣࡷ࡬ࡸࡀࠠࡎࡷ࡯ࡸ࡮࠳ࡲࡦࡲࡲࠤࡦࡶࡰࡳࡱࡤࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡸࡶࡥࡤ࡫ࡩ࡭ࡨࠦࡦࡰ࡮ࡧࡩࡷࡹࠠࡵࡱࠣࡥࡳࡧ࡬ࡺࡼࡨࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡱ࡯ࡳࡵ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡩ࡯ࡣࡵࡵ࠯ࠤࡪࡧࡣࡩࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡤࠤ࡫ࡵ࡬ࡥࡧࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧⓁ")
    if bstack1lll1ll1llll_opy_ is None:
        bstack1lll1ll1llll_opy_ = [os.getcwd()]
    elif isinstance(bstack1lll1ll1llll_opy_, list) and len(bstack1lll1ll1llll_opy_) == 0:
        return []
    results = []
    for folder in bstack1lll1ll1llll_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1l1llll_opy_ (u"ࠤࡉࡳࡱࡪࡥࡳࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠢⓂ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1l1llll_opy_ (u"ࠥࡴࡷࡏࡤࠣⓃ"): bstack1l1llll_opy_ (u"ࠦࠧⓄ"),
                bstack1l1llll_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦⓅ"): [],
                bstack1l1llll_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢⓆ"): [],
                bstack1l1llll_opy_ (u"ࠢࡱࡴࡇࡥࡹ࡫ࠢⓇ"): bstack1l1llll_opy_ (u"ࠣࠤⓈ"),
                bstack1l1llll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡏࡨࡷࡸࡧࡧࡦࡵࠥⓉ"): [],
                bstack1l1llll_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦⓊ"): bstack1l1llll_opy_ (u"ࠦࠧⓋ"),
                bstack1l1llll_opy_ (u"ࠧࡶࡲࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠧⓌ"): bstack1l1llll_opy_ (u"ࠨࠢⓍ"),
                bstack1l1llll_opy_ (u"ࠢࡱࡴࡕࡥࡼࡊࡩࡧࡨࠥⓎ"): bstack1l1llll_opy_ (u"ࠣࠤⓏ")
            }
            bstack1lllll11lll1_opy_ = repo.active_branch.name
            bstack1llll11ll111_opy_ = repo.head.commit
            result[bstack1l1llll_opy_ (u"ࠤࡳࡶࡎࡪࠢⓐ")] = bstack1llll11ll111_opy_.hexsha
            bstack1llll11ll1l1_opy_ = _1lll1lll111l_opy_(repo)
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡆࡦࡹࡥࠡࡤࡵࡥࡳࡩࡨࠡࡨࡲࡶࠥࡩ࡯࡮ࡲࡤࡶ࡮ࡹ࡯࡯࠼ࠣࠦⓑ") + str(bstack1llll11ll1l1_opy_) + bstack1l1llll_opy_ (u"ࠦࠧⓒ"))
            if bstack1llll11ll1l1_opy_:
                try:
                    bstack1llll11l11ll_opy_ = repo.git.diff(bstack1l1llll_opy_ (u"ࠧ࠳࠭࡯ࡣࡰࡩ࠲ࡵ࡮࡭ࡻࠥⓓ"), bstack1l11lll11ll_opy_ (u"ࠨࡻࡣࡣࡶࡩࡤࡨࡲࡢࡰࡦ࡬ࢂ࠴࠮࠯ࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀࠦⓔ")).split(bstack1l1llll_opy_ (u"ࠧ࡝ࡰࠪⓕ"))
                    logger.debug(bstack1l1llll_opy_ (u"ࠣࡅ࡫ࡥࡳ࡭ࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡤࡨࡸࡼ࡫ࡥ࡯ࠢࡾࡦࡦࡹࡥࡠࡤࡵࡥࡳࡩࡨࡾࠢࡤࡲࡩࠦࡻࡤࡷࡵࡶࡪࡴࡴࡠࡤࡵࡥࡳࡩࡨࡾ࠼ࠣࠦⓖ") + str(bstack1llll11l11ll_opy_) + bstack1l1llll_opy_ (u"ࠤࠥⓗ"))
                    result[bstack1l1llll_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤⓘ")] = [f.strip() for f in bstack1llll11l11ll_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1l11lll11ll_opy_ (u"ࠦࢀࡨࡡࡴࡧࡢࡦࡷࡧ࡮ࡤࡪࢀ࠲࠳ࢁࡣࡶࡴࡵࡩࡳࡺ࡟ࡣࡴࡤࡲࡨ࡮ࡽࠣⓙ")))
                except Exception:
                    logger.debug(bstack1l1llll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡩࡨࡢࡰࡪࡩࡩࠦࡦࡪ࡮ࡨࡷࠥ࡬ࡲࡰ࡯ࠣࡦࡷࡧ࡮ࡤࡪࠣࡧࡴࡳࡰࡢࡴ࡬ࡷࡴࡴ࠮ࠡࡈࡤࡰࡱ࡯࡮ࡨࠢࡥࡥࡨࡱࠠࡵࡱࠣࡶࡪࡩࡥ࡯ࡶࠣࡧࡴࡳ࡭ࡪࡶࡶ࠲ࠧⓚ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1l1llll_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧⓛ")] = _1lllll11l11l_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1l1llll_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨⓜ")] = _1lllll11l11l_opy_(commits[:5])
            bstack1lll1ll1l1l1_opy_ = set()
            bstack1llll1111ll1_opy_ = []
            for commit in commits:
                logger.debug(bstack1l1llll_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯࡬ࡸ࠿ࠦࠢⓝ") + str(commit.message) + bstack1l1llll_opy_ (u"ࠤࠥⓞ"))
                bstack1lll1ll11ll1_opy_ = commit.author.name if commit.author else bstack1l1llll_opy_ (u"࡙ࠥࡳࡱ࡮ࡰࡹࡱࠦⓟ")
                bstack1lll1ll1l1l1_opy_.add(bstack1lll1ll11ll1_opy_)
                bstack1llll1111ll1_opy_.append({
                    bstack1l1llll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧⓠ"): commit.message.strip(),
                    bstack1l1llll_opy_ (u"ࠧࡻࡳࡦࡴࠥⓡ"): bstack1lll1ll11ll1_opy_
                })
            result[bstack1l1llll_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢⓢ")] = list(bstack1lll1ll1l1l1_opy_)
            result[bstack1l1llll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡍࡦࡵࡶࡥ࡬࡫ࡳࠣⓣ")] = bstack1llll1111ll1_opy_
            result[bstack1l1llll_opy_ (u"ࠣࡲࡵࡈࡦࡺࡥࠣⓤ")] = bstack1llll11ll111_opy_.committed_datetime.strftime(bstack1l1llll_opy_ (u"ࠤࠨ࡝࠲ࠫ࡭࠮ࠧࡧࠦⓥ"))
            if (not result[bstack1l1llll_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦⓦ")] or result[bstack1l1llll_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧⓧ")].strip() == bstack1l1llll_opy_ (u"ࠧࠨⓨ")) and bstack1llll11ll111_opy_.message:
                bstack1lll1ll11lll_opy_ = bstack1llll11ll111_opy_.message.strip().splitlines()
                result[bstack1l1llll_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢⓩ")] = bstack1lll1ll11lll_opy_[0] if bstack1lll1ll11lll_opy_ else bstack1l1llll_opy_ (u"ࠢࠣ⓪")
                if len(bstack1lll1ll11lll_opy_) > 2:
                    result[bstack1l1llll_opy_ (u"ࠣࡲࡵࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣ⓫")] = bstack1l1llll_opy_ (u"ࠩ࡟ࡲࠬ⓬").join(bstack1lll1ll11lll_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1l1llll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡄࡍࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࠪࡩࡳࡱࡪࡥࡳ࠼ࠣࡿࢂ࠯࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤ⓭").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    bstack1llll111ll11_opy_ = [
        result
        for result in results
        if _1lll1l1l11ll_opy_(result)
    ]
    return bstack1llll111ll11_opy_
def _1lll1l1l11ll_opy_(result):
    bstack1l1llll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡍ࡫࡬ࡱࡧࡵࠤࡹࡵࠠࡤࡪࡨࡧࡰࠦࡩࡧࠢࡤࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡹࡵ࡭ࡶࠣ࡭ࡸࠦࡶࡢ࡮࡬ࡨࠥ࠮࡮ࡰࡰ࠰ࡩࡲࡶࡴࡺࠢࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠡࡣࡱࡨࠥࡧࡵࡵࡪࡲࡶࡸ࠯࠮ࠋࠢࠣࠤࠥࠨࠢࠣ⓮")
    return (
        isinstance(result.get(bstack1l1llll_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦ⓯"), None), list)
        and len(result[bstack1l1llll_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧ⓰")]) > 0
        and isinstance(result.get(bstack1l1llll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣ⓱"), None), list)
        and len(result[bstack1l1llll_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤ⓲")]) > 0
    )
def _1lll1lll111l_opy_(repo):
    bstack1l1llll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡗࡶࡾࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡺࡨࡦࠢࡥࡥࡸ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡳࡧࡳࡳࠥࡽࡩࡵࡪࡲࡹࡹࠦࡨࡢࡴࡧࡧࡴࡪࡥࡥࠢࡱࡥࡲ࡫ࡳࠡࡣࡱࡨࠥࡽ࡯ࡳ࡭ࠣࡻ࡮ࡺࡨࠡࡣ࡯ࡰࠥ࡜ࡃࡔࠢࡳࡶࡴࡼࡩࡥࡧࡵࡷ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡥࡶࡦࡴࡣࡩࠢ࡬ࡪࠥࡶ࡯ࡴࡵ࡬ࡦࡱ࡫ࠬࠡࡧ࡯ࡷࡪࠦࡎࡰࡰࡨ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ⓳")
    try:
        try:
            origin = repo.remotes.origin
            bstack1lll11lll1ll_opy_ = origin.refs[bstack1l1llll_opy_ (u"ࠪࡌࡊࡇࡄࠨ⓴")]
            target = bstack1lll11lll1ll_opy_.reference.name
            if target.startswith(bstack1l1llll_opy_ (u"ࠫࡴࡸࡩࡨ࡫ࡱ࠳ࠬ⓵")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1l1llll_opy_ (u"ࠬࡵࡲࡪࡩ࡬ࡲ࠴࠭⓶")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _1lllll11l11l_opy_(commits):
    bstack1l1llll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡇࡦࡶࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡨ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡤࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࡸ࠴ࠊࠡࠢࠣࠤࠧࠨࠢ⓷")
    bstack1llll11l11ll_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack1lll1l1ll1l1_opy_ in diff:
                        if bstack1lll1l1ll1l1_opy_.a_path:
                            bstack1llll11l11ll_opy_.add(bstack1lll1l1ll1l1_opy_.a_path)
                        if bstack1lll1l1ll1l1_opy_.b_path:
                            bstack1llll11l11ll_opy_.add(bstack1lll1l1ll1l1_opy_.b_path)
    except Exception:
        pass
    return list(bstack1llll11l11ll_opy_)
def bstack1lll1llllll1_opy_(bstack1lll1l1111l1_opy_):
    bstack1lll1ll1ll11_opy_ = bstack1llll1l111l1_opy_(bstack1lll1l1111l1_opy_)
    if bstack1lll1ll1ll11_opy_ and bstack1lll1ll1ll11_opy_ > bstack1llllll11lll_opy_:
        bstack1lll1l11lll1_opy_ = bstack1lll1ll1ll11_opy_ - bstack1llllll11lll_opy_
        bstack1lll1l111l11_opy_ = bstack1lll1lll1111_opy_(bstack1lll1l1111l1_opy_[bstack1l1llll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ⓸")], bstack1lll1l11lll1_opy_)
        bstack1lll1l1111l1_opy_[bstack1l1llll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤ⓹")] = bstack1lll1l111l11_opy_
        logger.info(bstack1l1llll_opy_ (u"ࠤࡗ࡬ࡪࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡨࡢࡵࠣࡦࡪ࡫࡮ࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧ࠲࡙ࠥࡩࡻࡧࠣࡳ࡫ࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡡࡧࡶࡨࡶࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥࢁࡽࠡࡍࡅࠦ⓺")
                    .format(bstack1llll1l111l1_opy_(bstack1lll1l1111l1_opy_) / 1024))
    return bstack1lll1l1111l1_opy_
def bstack1llll1l111l1_opy_(json_data):
    try:
        if json_data:
            bstack1lll1lll11l1_opy_ = json.dumps(json_data)
            bstack1lll1l11111l_opy_ = sys.getsizeof(bstack1lll1lll11l1_opy_)
            return bstack1lll1l11111l_opy_
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠥࡗࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡦࡥࡱࡩࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡴ࡫ࡽࡩࠥࡵࡦࠡࡌࡖࡓࡓࠦ࡯ࡣ࡬ࡨࡧࡹࡀࠠࡼࡿࠥ⓻").format(e))
    return -1
def bstack1lll1lll1111_opy_(field, bstack1lll1ll1111l_opy_):
    try:
        bstack1lll1l11ll1l_opy_ = len(bytes(bstack1111111llll_opy_, bstack1l1llll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ⓼")))
        bstack1lll11ll111l_opy_ = bytes(field, bstack1l1llll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ⓽"))
        bstack1llll11111ll_opy_ = len(bstack1lll11ll111l_opy_)
        bstack1lll1ll11l1l_opy_ = ceil(bstack1llll11111ll_opy_ - bstack1lll1ll1111l_opy_ - bstack1lll1l11ll1l_opy_)
        if bstack1lll1ll11l1l_opy_ > 0:
            bstack1lll11l11lll_opy_ = bstack1lll11ll111l_opy_[:bstack1lll1ll11l1l_opy_].decode(bstack1l1llll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ⓾"), errors=bstack1l1llll_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࠧ⓿")) + bstack1111111llll_opy_
            return bstack1lll11l11lll_opy_
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡴࡳࡷࡱࡧࡦࡺࡩ࡯ࡩࠣࡪ࡮࡫࡬ࡥ࠮ࠣࡲࡴࡺࡨࡪࡰࡪࠤࡼࡧࡳࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧࠤ࡭࡫ࡲࡦ࠼ࠣࡿࢂࠨ─").format(e))
    return field
def bstack11111l1lll_opy_():
    env = os.environ
    if (bstack1l1llll_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢ━") in env and len(env[bstack1l1llll_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣ│")]) > 0) or (
            bstack1l1llll_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥ┃") in env and len(env[bstack1l1llll_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦ┄")]) > 0):
        return {
            bstack1l1llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ┅"): bstack1l1llll_opy_ (u"ࠢࡋࡧࡱ࡯࡮ࡴࡳࠣ┆"),
            bstack1l1llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ┇"): env.get(bstack1l1llll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ┈")),
            bstack1l1llll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ┉"): env.get(bstack1l1llll_opy_ (u"ࠦࡏࡕࡂࡠࡐࡄࡑࡊࠨ┊")),
            bstack1l1llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ┋"): env.get(bstack1l1llll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ┌"))
        }
    if env.get(bstack1l1llll_opy_ (u"ࠢࡄࡋࠥ┍")) == bstack1l1llll_opy_ (u"ࠣࡶࡵࡹࡪࠨ┎") and bstack11lll11l1l_opy_(env.get(bstack1l1llll_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡅࡌࠦ┏"))):
        return {
            bstack1l1llll_opy_ (u"ࠥࡲࡦࡳࡥࠣ┐"): bstack1l1llll_opy_ (u"ࠦࡈ࡯ࡲࡤ࡮ࡨࡇࡎࠨ┑"),
            bstack1l1llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ┒"): env.get(bstack1l1llll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ┓")),
            bstack1l1llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ└"): env.get(bstack1l1llll_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡌࡒࡆࠧ┕")),
            bstack1l1llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ┖"): env.get(bstack1l1llll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࠨ┗"))
        }
    if env.get(bstack1l1llll_opy_ (u"ࠦࡈࡏࠢ┘")) == bstack1l1llll_opy_ (u"ࠧࡺࡲࡶࡧࠥ┙") and bstack11lll11l1l_opy_(env.get(bstack1l1llll_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࠨ┚"))):
        return {
            bstack1l1llll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ┛"): bstack1l1llll_opy_ (u"ࠣࡖࡵࡥࡻ࡯ࡳࠡࡅࡌࠦ├"),
            bstack1l1llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ┝"): env.get(bstack1l1llll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡ࡚ࡉࡇࡥࡕࡓࡎࠥ┞")),
            bstack1l1llll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ┟"): env.get(bstack1l1llll_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ┠")),
            bstack1l1llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ┡"): env.get(bstack1l1llll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ┢"))
        }
    if env.get(bstack1l1llll_opy_ (u"ࠣࡅࡌࠦ┣")) == bstack1l1llll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ┤") and env.get(bstack1l1llll_opy_ (u"ࠥࡇࡎࡥࡎࡂࡏࡈࠦ┥")) == bstack1l1llll_opy_ (u"ࠦࡨࡵࡤࡦࡵ࡫࡭ࡵࠨ┦"):
        return {
            bstack1l1llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ┧"): bstack1l1llll_opy_ (u"ࠨࡃࡰࡦࡨࡷ࡭࡯ࡰࠣ┨"),
            bstack1l1llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ┩"): None,
            bstack1l1llll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ┪"): None,
            bstack1l1llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ┫"): None
        }
    if env.get(bstack1l1llll_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡓࡃࡑࡇࡍࠨ┬")) and env.get(bstack1l1llll_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢ┭")):
        return {
            bstack1l1llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ┮"): bstack1l1llll_opy_ (u"ࠨࡂࡪࡶࡥࡹࡨࡱࡥࡵࠤ┯"),
            bstack1l1llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ┰"): env.get(bstack1l1llll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡌࡏࡔࡠࡊࡗࡘࡕࡥࡏࡓࡋࡊࡍࡓࠨ┱")),
            bstack1l1llll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ┲"): None,
            bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ┳"): env.get(bstack1l1llll_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ┴"))
        }
    if env.get(bstack1l1llll_opy_ (u"ࠧࡉࡉࠣ┵")) == bstack1l1llll_opy_ (u"ࠨࡴࡳࡷࡨࠦ┶") and bstack11lll11l1l_opy_(env.get(bstack1l1llll_opy_ (u"ࠢࡅࡔࡒࡒࡊࠨ┷"))):
        return {
            bstack1l1llll_opy_ (u"ࠣࡰࡤࡱࡪࠨ┸"): bstack1l1llll_opy_ (u"ࠤࡇࡶࡴࡴࡥࠣ┹"),
            bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ┺"): env.get(bstack1l1llll_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡏࡍࡓࡑࠢ┻")),
            bstack1l1llll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ┼"): None,
            bstack1l1llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ┽"): env.get(bstack1l1llll_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ┾"))
        }
    if env.get(bstack1l1llll_opy_ (u"ࠣࡅࡌࠦ┿")) == bstack1l1llll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ╀") and bstack11lll11l1l_opy_(env.get(bstack1l1llll_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࠨ╁"))):
        return {
            bstack1l1llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ╂"): bstack1l1llll_opy_ (u"࡙ࠧࡥ࡮ࡣࡳ࡬ࡴࡸࡥࠣ╃"),
            bstack1l1llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ╄"): env.get(bstack1l1llll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡓࡗࡍࡁࡏࡋ࡝ࡅ࡙ࡏࡏࡏࡡࡘࡖࡑࠨ╅")),
            bstack1l1llll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ╆"): env.get(bstack1l1llll_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ╇")),
            bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ╈"): env.get(bstack1l1llll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡎࡊࠢ╉"))
        }
    if env.get(bstack1l1llll_opy_ (u"ࠧࡉࡉࠣ╊")) == bstack1l1llll_opy_ (u"ࠨࡴࡳࡷࡨࠦ╋") and bstack11lll11l1l_opy_(env.get(bstack1l1llll_opy_ (u"ࠢࡈࡋࡗࡐࡆࡈ࡟ࡄࡋࠥ╌"))):
        return {
            bstack1l1llll_opy_ (u"ࠣࡰࡤࡱࡪࠨ╍"): bstack1l1llll_opy_ (u"ࠤࡊ࡭ࡹࡒࡡࡣࠤ╎"),
            bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ╏"): env.get(bstack1l1llll_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣ࡚ࡘࡌࠣ═")),
            bstack1l1llll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ║"): env.get(bstack1l1llll_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ╒")),
            bstack1l1llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ╓"): env.get(bstack1l1llll_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡋࡇࠦ╔"))
        }
    if env.get(bstack1l1llll_opy_ (u"ࠤࡆࡍࠧ╕")) == bstack1l1llll_opy_ (u"ࠥࡸࡷࡻࡥࠣ╖") and bstack11lll11l1l_opy_(env.get(bstack1l1llll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋࠢ╗"))):
        return {
            bstack1l1llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ╘"): bstack1l1llll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡰ࡯ࡴࡦࠤ╙"),
            bstack1l1llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ╚"): env.get(bstack1l1llll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ╛")),
            bstack1l1llll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ╜"): env.get(bstack1l1llll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡌࡂࡄࡈࡐࠧ╝")) or env.get(bstack1l1llll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢ╞")),
            bstack1l1llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ╟"): env.get(bstack1l1llll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ╠"))
        }
    if bstack11lll11l1l_opy_(env.get(bstack1l1llll_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤ╡"))):
        return {
            bstack1l1llll_opy_ (u"ࠣࡰࡤࡱࡪࠨ╢"): bstack1l1llll_opy_ (u"ࠤ࡙࡭ࡸࡻࡡ࡭ࠢࡖࡸࡺࡪࡩࡰࠢࡗࡩࡦࡳࠠࡔࡧࡵࡺ࡮ࡩࡥࡴࠤ╣"),
            bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ╤"): bstack1l1llll_opy_ (u"ࠦࢀࢃࡻࡾࠤ╥").format(env.get(bstack1l1llll_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨ╦")), env.get(bstack1l1llll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࡍࡉ࠭╧"))),
            bstack1l1llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ╨"): env.get(bstack1l1llll_opy_ (u"ࠣࡕ࡜ࡗ࡙ࡋࡍࡠࡆࡈࡊࡎࡔࡉࡕࡋࡒࡒࡎࡊࠢ╩")),
            bstack1l1llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ╪"): env.get(bstack1l1llll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥ╫"))
        }
    if bstack11lll11l1l_opy_(env.get(bstack1l1llll_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࠨ╬"))):
        return {
            bstack1l1llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ╭"): bstack1l1llll_opy_ (u"ࠨࡁࡱࡲࡹࡩࡾࡵࡲࠣ╮"),
            bstack1l1llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ╯"): bstack1l1llll_opy_ (u"ࠣࡽࢀ࠳ࡵࡸ࡯࡫ࡧࡦࡸ࠴ࢁࡽ࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠢ╰").format(env.get(bstack1l1llll_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣ࡚ࡘࡌࠨ╱")), env.get(bstack1l1llll_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡇࡃࡄࡑࡘࡒ࡙ࡥࡎࡂࡏࡈࠫ╲")), env.get(bstack1l1llll_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡔࡎࡘࡋࠬ╳")), env.get(bstack1l1llll_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ╴"))),
            bstack1l1llll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ╵"): env.get(bstack1l1llll_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ╶")),
            bstack1l1llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ╷"): env.get(bstack1l1llll_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ╸"))
        }
    if env.get(bstack1l1llll_opy_ (u"ࠥࡅ࡟࡛ࡒࡆࡡࡋࡘ࡙ࡖ࡟ࡖࡕࡈࡖࡤࡇࡇࡆࡐࡗࠦ╹")) and env.get(bstack1l1llll_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨ╺")):
        return {
            bstack1l1llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ╻"): bstack1l1llll_opy_ (u"ࠨࡁࡻࡷࡵࡩࠥࡉࡉࠣ╼"),
            bstack1l1llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ╽"): bstack1l1llll_opy_ (u"ࠣࡽࢀࡿࢂ࠵࡟ࡣࡷ࡬ࡰࡩ࠵ࡲࡦࡵࡸࡰࡹࡹ࠿ࡣࡷ࡬ࡰࡩࡏࡤ࠾ࡽࢀࠦ╾").format(env.get(bstack1l1llll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬ╿")), env.get(bstack1l1llll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࠨ▀")), env.get(bstack1l1llll_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠫ▁"))),
            bstack1l1llll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ▂"): env.get(bstack1l1llll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨ▃")),
            bstack1l1llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ▄"): env.get(bstack1l1llll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣ▅"))
        }
    if any([env.get(bstack1l1llll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ▆")), env.get(bstack1l1llll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤ▇")), env.get(bstack1l1llll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣ█"))]):
        return {
            bstack1l1llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ▉"): bstack1l1llll_opy_ (u"ࠨࡁࡘࡕࠣࡇࡴࡪࡥࡃࡷ࡬ࡰࡩࠨ▊"),
            bstack1l1llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ▋"): env.get(bstack1l1llll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡕ࡛ࡂࡍࡋࡆࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ▌")),
            bstack1l1llll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ▍"): env.get(bstack1l1llll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ▎")),
            bstack1l1llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ▏"): env.get(bstack1l1llll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ▐"))
        }
    if env.get(bstack1l1llll_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦ░")):
        return {
            bstack1l1llll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ▒"): bstack1l1llll_opy_ (u"ࠣࡄࡤࡱࡧࡵ࡯ࠣ▓"),
            bstack1l1llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ▔"): env.get(bstack1l1llll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡔࡨࡷࡺࡲࡴࡴࡗࡵࡰࠧ▕")),
            bstack1l1llll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ▖"): env.get(bstack1l1llll_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡹࡨࡰࡴࡷࡎࡴࡨࡎࡢ࡯ࡨࠦ▗")),
            bstack1l1llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ▘"): env.get(bstack1l1llll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧ▙"))
        }
    if env.get(bstack1l1llll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࠤ▚")) or env.get(bstack1l1llll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦ▛")):
        return {
            bstack1l1llll_opy_ (u"ࠥࡲࡦࡳࡥࠣ▜"): bstack1l1llll_opy_ (u"ࠦ࡜࡫ࡲࡤ࡭ࡨࡶࠧ▝"),
            bstack1l1llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ▞"): env.get(bstack1l1llll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ▟")),
            bstack1l1llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ■"): bstack1l1llll_opy_ (u"ࠣࡏࡤ࡭ࡳࠦࡐࡪࡲࡨࡰ࡮ࡴࡥࠣ□") if env.get(bstack1l1llll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦ▢")) else None,
            bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ▣"): env.get(bstack1l1llll_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡍࡉࡕࡡࡆࡓࡒࡓࡉࡕࠤ▤"))
        }
    if any([env.get(bstack1l1llll_opy_ (u"ࠧࡍࡃࡑࡡࡓࡖࡔࡐࡅࡄࡖࠥ▥")), env.get(bstack1l1llll_opy_ (u"ࠨࡇࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ▦")), env.get(bstack1l1llll_opy_ (u"ࠢࡈࡑࡒࡋࡑࡋ࡟ࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ▧"))]):
        return {
            bstack1l1llll_opy_ (u"ࠣࡰࡤࡱࡪࠨ▨"): bstack1l1llll_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡆࡰࡴࡻࡤࠣ▩"),
            bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ▪"): None,
            bstack1l1llll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ▫"): env.get(bstack1l1llll_opy_ (u"ࠧࡖࡒࡐࡌࡈࡇ࡙ࡥࡉࡅࠤ▬")),
            bstack1l1llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ▭"): env.get(bstack1l1llll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤ▮"))
        }
    if env.get(bstack1l1llll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࠦ▯")):
        return {
            bstack1l1llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ▰"): bstack1l1llll_opy_ (u"ࠥࡗ࡭࡯ࡰࡱࡣࡥࡰࡪࠨ▱"),
            bstack1l1llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ▲"): env.get(bstack1l1llll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ△")),
            bstack1l1llll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ▴"): bstack1l1llll_opy_ (u"ࠢࡋࡱࡥࠤࠨࢁࡽࠣ▵").format(env.get(bstack1l1llll_opy_ (u"ࠨࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠫ▶"))) if env.get(bstack1l1llll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠧ▷")) else None,
            bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ▸"): env.get(bstack1l1llll_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ▹"))
        }
    if bstack11lll11l1l_opy_(env.get(bstack1l1llll_opy_ (u"ࠧࡔࡅࡕࡎࡌࡊ࡞ࠨ►"))):
        return {
            bstack1l1llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ▻"): bstack1l1llll_opy_ (u"ࠢࡏࡧࡷࡰ࡮࡬ࡹࠣ▼"),
            bstack1l1llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ▽"): env.get(bstack1l1llll_opy_ (u"ࠤࡇࡉࡕࡒࡏ࡚ࡡࡘࡖࡑࠨ▾")),
            bstack1l1llll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ▿"): env.get(bstack1l1llll_opy_ (u"ࠦࡘࡏࡔࡆࡡࡑࡅࡒࡋࠢ◀")),
            bstack1l1llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ◁"): env.get(bstack1l1llll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ◂"))
        }
    if bstack11lll11l1l_opy_(env.get(bstack1l1llll_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡂࡅࡗࡍࡔࡔࡓࠣ◃"))):
        return {
            bstack1l1llll_opy_ (u"ࠣࡰࡤࡱࡪࠨ◄"): bstack1l1llll_opy_ (u"ࠤࡊ࡭ࡹࡎࡵࡣࠢࡄࡧࡹ࡯࡯࡯ࡵࠥ◅"),
            bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ◆"): bstack1l1llll_opy_ (u"ࠦࢀࢃ࠯ࡼࡿ࠲ࡥࡨࡺࡩࡰࡰࡶ࠳ࡷࡻ࡮ࡴ࠱ࡾࢁࠧ◇").format(env.get(bstack1l1llll_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤ࡙ࡅࡓࡘࡈࡖࡤ࡛ࡒࡍࠩ◈")), env.get(bstack1l1llll_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡆࡒࡒࡗࡎ࡚ࡏࡓ࡛ࠪ◉")), env.get(bstack1l1llll_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠧ◊"))),
            bstack1l1llll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ○"): env.get(bstack1l1llll_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡ࡚ࡓࡗࡑࡆࡍࡑ࡚ࠦ◌")),
            bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ◍"): env.get(bstack1l1llll_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠦ◎"))
        }
    if env.get(bstack1l1llll_opy_ (u"ࠧࡉࡉࠣ●")) == bstack1l1llll_opy_ (u"ࠨࡴࡳࡷࡨࠦ◐") and env.get(bstack1l1llll_opy_ (u"ࠢࡗࡇࡕࡇࡊࡒࠢ◑")) == bstack1l1llll_opy_ (u"ࠣ࠳ࠥ◒"):
        return {
            bstack1l1llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ◓"): bstack1l1llll_opy_ (u"࡚ࠥࡪࡸࡣࡦ࡮ࠥ◔"),
            bstack1l1llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ◕"): bstack1l1llll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࢁࡽࠣ◖").format(env.get(bstack1l1llll_opy_ (u"࠭ࡖࡆࡔࡆࡉࡑࡥࡕࡓࡎࠪ◗"))),
            bstack1l1llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ◘"): None,
            bstack1l1llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ◙"): None,
        }
    if env.get(bstack1l1llll_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣ࡛ࡋࡒࡔࡋࡒࡒࠧ◚")):
        return {
            bstack1l1llll_opy_ (u"ࠥࡲࡦࡳࡥࠣ◛"): bstack1l1llll_opy_ (u"࡙ࠦ࡫ࡡ࡮ࡥ࡬ࡸࡾࠨ◜"),
            bstack1l1llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ◝"): None,
            bstack1l1llll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ◞"): env.get(bstack1l1llll_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠣ◟")),
            bstack1l1llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ◠"): env.get(bstack1l1llll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ◡"))
        }
    if any([env.get(bstack1l1llll_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࠨ◢")), env.get(bstack1l1llll_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡔࡏࠦ◣")), env.get(bstack1l1llll_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥ◤")), env.get(bstack1l1llll_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡗࡉࡆࡓࠢ◥"))]):
        return {
            bstack1l1llll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ◦"): bstack1l1llll_opy_ (u"ࠣࡅࡲࡲࡨࡵࡵࡳࡵࡨࠦ◧"),
            bstack1l1llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ◨"): None,
            bstack1l1llll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ◩"): env.get(bstack1l1llll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ◪")) or None,
            bstack1l1llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ◫"): env.get(bstack1l1llll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ◬"), 0)
        }
    if env.get(bstack1l1llll_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ◭")):
        return {
            bstack1l1llll_opy_ (u"ࠣࡰࡤࡱࡪࠨ◮"): bstack1l1llll_opy_ (u"ࠤࡊࡳࡈࡊࠢ◯"),
            bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ◰"): None,
            bstack1l1llll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ◱"): env.get(bstack1l1llll_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ◲")),
            bstack1l1llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ◳"): env.get(bstack1l1llll_opy_ (u"ࠢࡈࡑࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡉࡏࡖࡐࡗࡉࡗࠨ◴"))
        }
    if env.get(bstack1l1llll_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ◵")):
        return {
            bstack1l1llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ◶"): bstack1l1llll_opy_ (u"ࠥࡇࡴࡪࡥࡇࡴࡨࡷ࡭ࠨ◷"),
            bstack1l1llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ◸"): env.get(bstack1l1llll_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ◹")),
            bstack1l1llll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ◺"): env.get(bstack1l1llll_opy_ (u"ࠢࡄࡈࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥ◻")),
            bstack1l1llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ◼"): env.get(bstack1l1llll_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ◽"))
        }
    return {bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ◾"): None}
def get_host_info():
    return {
        bstack1l1llll_opy_ (u"ࠦ࡭ࡵࡳࡵࡰࡤࡱࡪࠨ◿"): platform.node(),
        bstack1l1llll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢ☀"): platform.system(),
        bstack1l1llll_opy_ (u"ࠨࡴࡺࡲࡨࠦ☁"): platform.machine(),
        bstack1l1llll_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣ☂"): platform.version(),
        bstack1l1llll_opy_ (u"ࠣࡣࡵࡧ࡭ࠨ☃"): platform.architecture()[0]
    }
def bstack1l1111l1ll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1lll11llllll_opy_():
    if global_config.get_property(bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ☄")):
        return bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ★")
    return bstack1l1llll_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠪ☆")
def bstack1l1l11ll1_opy_(driver):
    info = {
        bstack1l1llll_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ☇"): driver.capabilities,
        bstack1l1llll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪ☈"): driver.session_id,
        bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ☉"): driver.capabilities.get(bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭☊"), None),
        bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ☋"): driver.capabilities.get(bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ☌"), None),
        bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࠭☍"): driver.capabilities.get(bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫ☎"), None),
        bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ☏"):driver.capabilities.get(bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ☐"), None),
    }
    device_name = driver.capabilities.get(bstack1l1llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ☑"), None)
    if device_name:
        info[bstack1l1llll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡡࡱࡥࡲ࡫ࠧ☒")] = device_name
    if bstack11ll11lll1_opy_():
        info[bstack1l1llll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ☓")] = bstack1l1llll_opy_ (u"ࠫࡱࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࠩ☔")
    elif bstack1lll11llllll_opy_() == bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ☕"):
        if bstack1ll1111l1l1_opy_():
            info[bstack1l1llll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ☖")] = bstack1l1llll_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭☗")
        elif driver.capabilities.get(bstack1l1llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ☘"), {}).get(bstack1l1llll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭☙"), False):
            info[bstack1l1llll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ☚")] = bstack1l1llll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ☛")
        else:
            info[bstack1l1llll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭☜")] = bstack1l1llll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ☝")
    return info
def bstack1ll1111l1l1_opy_():
    if global_config.get_property(bstack1l1llll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭☞")):
        return True
    if bstack11lll11l1l_opy_(os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ☟"), None)):
        return True
    return False
def bstack11ll11lll1_opy_():
    bstack1l1llll_opy_ (u"ࠤࠥࠦࡗ࡫ࡴࡶࡴࡱࡷ࡚ࠥࡲࡶࡧࠣࡻ࡭࡫࡮ࠡࡶ࡫࡭ࡸࠦࡲࡶࡰࠣ࡭ࡸࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࡦࠣࡪࡴࡸࠠࡍࡱࡤࡨ࡚ࠥࡥࡴࡶ࡬ࡲ࡬ࠦࡓࡦࡵࡶ࡭ࡴࡴࠠࠩࡎࡗࡗ࠮࠴ࠊࠡࠢࠣࠤࡒ࡯ࡲࡳࡱࡵࠤࡴ࡬ࠠࡋࡣࡹࡥࠬࡹࠠࡍࡱࡤࡨ࡙࡫ࡳࡵࡗࡷ࡭ࡱࡹ࠮ࡪࡵࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭࠽ࡵࡴࡸࡩࠏࠦࠠࠡࠢࡄࡒࡉࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠾ࡨࡤࡰࡸ࡫࠮ࠋࠢࠣࠤࠥࡋ࡮ࡷࠢࡹࡥࡷࡹࠠࡵࡣ࡮ࡩࠥࡶࡲࡦࡥࡨࡨࡪࡴࡣࡦࠢࡲࡺࡪࡸࠠࡨ࡮ࡲࡦࡦࡲ࡟ࡤࡱࡱࡪ࡮࡭ࠠࡣࡧࡦࡥࡺࡹࡥࠡࡵࡸࡦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡴࡲࡤࡻࡳ࡫ࡤࠡࡤࡼࠎࠥࠦࠠࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࠫࡩ࠳࡭࠮ࠡࡶ࡫ࡩࠥࡼࡡ࡯࡫࡯ࡰࡦ࠳ࡰࡺࡶ࡫ࡳࡳࠦࡥࡹࡧࡦࠤࡵࡧࡴࡩࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡹࡳ࡯ࡴࡵࡧࡶࡸࠥࡺࡥࡴࡶࡶ࠭ࠥ࡯࡮ࡩࡧࡵ࡭ࡹࠐࠠࠡࠢࠣࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊࠤ࠴ࠦࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡵࡧࡲࡦࡰࡷࠤࡸ࡮ࡥ࡭࡮ࠣࡦࡺࡺࠊࠡࠢࠣࠤࡷ࡫࠭ࡪ࡯ࡳࡳࡷࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡶࡶ࡬ࡰࡸࠦࡷࡪࡶ࡫ࠤࡦࠦࡦࡳࡧࡶ࡬ࠥࡳ࡯ࡥࡷ࡯ࡩ࠲ࡲࡥࡷࡧ࡯ࠤࡥ࡭࡬ࡰࡤࡤࡰࡤࡩ࡯࡯ࡨ࡬࡫ࡥࠦࡷࡩࡱࡶࡩࠏࠦࠠࠡࠢࡣࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡤࠥࡶࡲࡰࡲࡨࡶࡹࡿࠠࡥࡧࡩࡥࡺࡲࡴࡴࠢࡷࡳ࡚ࠥࡲࡶࡧࠣࠬࡸ࡫ࡴࠡࡦࡸࡶ࡮ࡴࡧࠡࡃࡸࡸࡴࡳࡡࡵࡧ࠰ࡷࡹࡿ࡬ࡦࠢࡖࡈࡐࠐࠠࠡࠢࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦ࡯ࡧࠢࡷ࡬ࡪࠦࡳࡶࡤࡳࡶࡴࡩࡥࡴࡵࠬ࠲ࠥࡘࡥࡢࡦ࡬ࡲ࡬ࠦࡧ࡭ࡱࡥࡥࡱࡥࡣࡰࡰࡩ࡭࡬ࠦࡦࡪࡴࡶࡸࠥࡺࡨࡦࡴࡨࠤ࡬࡯ࡶࡦࡵࠣࡸ࡭࡫ࠊࠡࠢࠣࠤࡼࡸ࡯࡯ࡩࠣࡥࡳࡹࡷࡦࡴࠣࡥࡳࡪࠠࡥ࡫ࡶࡥࡧࡲࡥࡴࠢࡏࡘࡘࠦࡩ࡯ࡵࡷࡶࡺࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠡࡵ࡬ࡰࡪࡴࡴ࡭ࡻ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ☠")
    bstack111llll11l1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠪࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊࠫ☡"), None)
    if bstack111llll11l1_opy_ is not None:
        override = bstack11lll11l1l_opy_(bstack111llll11l1_opy_)
    else:
        override = global_config.get_property(bstack1l1llll_opy_ (u"ࠫࡴࡼࡥࡳࡴ࡬ࡨࡪࡥ࡬ࡰࡣࡧࡣࡹ࡫ࡳࡵ࡫ࡱ࡫ࠬ☢"))
    if not bool(override):
        return False
    bstack1lll1l11l1ll_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ☣"), None)
    if bstack1lll1l11l1ll_opy_ is not None:
        bstack1llll1lll111_opy_ = bstack11lll11l1l_opy_(bstack1lll1l11l1ll_opy_)
    else:
        bstack1llll1lll111_opy_ = global_config.get_property(bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ☤"))
    return not bool(bstack1llll1lll111_opy_)
def bstack111lll111l1_opy_():
    bstack1l1llll_opy_ (u"ࠢࠣࠤࡕࡩࡹࡸࡩࡦࡸࡨࡷࠥࡺࡨࡦࠢࡏࡘࡘࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡪࡦࠣࡪࡷࡵ࡭ࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹ࠴ࠊࠡࠢࠣࠤࡒ࡯ࡲࡳࡱࡵࠤࡴ࡬ࠠࡋࡣࡹࡥࠬࡹࠠࡍࡱࡤࡨ࡙࡫ࡳࡵࡗࡷ࡭ࡱࡹ࠮ࡨࡧࡷࡐࡹࡹࡓࡦࡵࡶ࡭ࡴࡴࡉࡥ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡧࡰࡴࡹࡿࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡸࡪࡨࡲࠥࡴ࡯ࡵࠢࡳࡶࡪࡹࡥ࡯ࡶ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ☥")
    bstack1llll111l1l1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡖࡖࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠨ☦"), None)
    if bstack1llll111l1l1_opy_ is not None and bstack1llll111l1l1_opy_.strip() != bstack1l1llll_opy_ (u"ࠩࠪ☧"):
        return bstack1llll111l1l1_opy_.strip()
    return bstack1l1llll_opy_ (u"ࠪࠫ☨")
_1lllll111111_opy_ = re.compile(
    bstack1l1llll_opy_ (u"ࡶࠬ࠮࡜࡝ࡁࠥࠬࡄࡀࠧ☩") + bstack1l1llll_opy_ (u"ࠬࢂࠧ☪").join(re.escape(k) for k in bstack11111111111_opy_) + bstack1l1llll_opy_ (u"ࡸࠧࠪ࡞࡟ࡃࠧࡢࡳࠫ࠼࡟ࡷ࠯ࡢ࡜ࡀࠤࠬࠬࡠࡤࠢ࡝࡞ࡠ࠮࠮࠮࡜࡝ࡁࠥ࠭ࠬ☫"),
    re.IGNORECASE,
)
_1lll11l1l1ll_opy_ = re.compile(
    bstack1l1llll_opy_ (u"ࡲࠨࠪࠨ࠶࠷࠮࠿࠻ࠩ☬") + bstack1l1llll_opy_ (u"ࠨࡾࠪ☭").join(re.escape(k) for k in bstack11111111111_opy_) + bstack1l1llll_opy_ (u"ࡴࠪ࠭ࠪ࠸࠲ࠦ࠵ࡄࠬࡄࡀࠥ࠳࠲ࠬࡃࠪ࠸࠲ࠪࠪ࠱࠮ࡄ࠯ࠨࠦ࠴࠵࠭ࠬ☮"),
    re.IGNORECASE,
)
def _1llll1l1lll1_opy_(s):
    s = _1lllll111111_opy_.sub(lambda m: m.group(1) + bstack1l1llll_opy_ (u"ࠪ࠮࠯࠰ࠪࠨ☯") + m.group(3), s)
    s = _1lll11l1l1ll_opy_.sub(lambda m: m.group(1) + bstack1l1llll_opy_ (u"ࠫ࠯࠰ࠪࠫࠩ☰") + m.group(3), s)
    return s
def bstack1lll1llll11l_opy_(obj):
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if isinstance(v, str):
                obj[k] = _1llll1l1lll1_opy_(v)
            else:
                bstack1lll1llll11l_opy_(v)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str):
                obj[i] = _1llll1l1lll1_opy_(v)
            else:
                bstack1lll1llll11l_opy_(v)
def bstack1llll111111l_opy_(bstack1llll111lll1_opy_, url, response, headers=None, data=None):
    bstack1l1llll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡈࡵࡪ࡮ࡧࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡮ࡲ࡫ࠥࡶࡡࡳࡣࡰࡩࡹ࡫ࡲࡴࠢࡩࡳࡷࠦࡲࡦࡳࡸࡩࡸࡺ࠯ࡳࡧࡶࡴࡴࡴࡳࡦࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡴࡹࡪࡹࡴࡠࡶࡼࡴࡪࡀࠠࡉࡖࡗࡔࠥࡳࡥࡵࡪࡲࡨࠥ࠮ࡇࡆࡖ࠯ࠤࡕࡕࡓࡕ࠮ࠣࡩࡹࡩ࠮ࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࡹࡷࡲ࠺ࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡘࡖࡑ࠵ࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠋࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡰࡤ࡭ࡩࡨࡺࠠࡧࡴࡲࡱࠥࡸࡥࡲࡷࡨࡷࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࡪࡨࡥࡩ࡫ࡲࡴ࠼ࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡭࡫ࡡࡥࡧࡵࡷࠥࡵࡲࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࡥࡣࡷࡥ࠿ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡋࡕࡒࡒࠥࡪࡡࡵࡣࠣࡳࡷࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡊࡴࡸ࡭ࡢࡶࡷࡩࡩࠦ࡬ࡰࡩࠣࡱࡪࡹࡳࡢࡩࡨࠤࡼ࡯ࡴࡩࠢࡵࡩࡶࡻࡥࡴࡶࠣࡥࡳࡪࠠࡳࡧࡶࡴࡴࡴࡳࡦࠢࡧࡥࡹࡧࠊࠡࠢࠣࠤࠧࠨࠢ☱")
    bstack1llll1l11111_opy_ = [k.lower() for k in bstack11111111111_opy_]
    bstack1lllll1l1111_opy_ = None
    if isinstance(data, dict):
        bstack1lllll1l1111_opy_ = data
        bstack1llll11l1l1l_opy_(bstack1lllll1l1111_opy_, bstack1llll1l11111_opy_)
        bstack1lll1llll11l_opy_(bstack1lllll1l1111_opy_)
    elif isinstance(data, list):
        bstack1lllll1l1111_opy_ = data
        for item in bstack1lllll1l1111_opy_:
            if isinstance(item, dict):
                bstack1llll11l1l1l_opy_(item, bstack1llll1l11111_opy_)
        bstack1lll1llll11l_opy_(bstack1lllll1l1111_opy_)
    else:
        bstack1lllll1l1111_opy_ = data
    bstack1lll1lllll1l_opy_ = None
    if isinstance(headers, dict):
        bstack1lll1lllll1l_opy_ = copy.deepcopy(headers)
        bstack1llll11l1l1l_opy_(bstack1lll1lllll1l_opy_, bstack1llll1l11111_opy_)
        bstack1lll1llll11l_opy_(bstack1lll1lllll1l_opy_)
    else:
        bstack1lll1lllll1l_opy_ = headers
    bstack1lll1l1111ll_opy_ = {
        bstack1l1llll_opy_ (u"ࠨࡨࡦࡣࡧࡩࡷࡹࠢ☲"): bstack1lll1lllll1l_opy_,
        bstack1l1llll_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢ☳"): bstack1llll111lll1_opy_.upper(),
        bstack1l1llll_opy_ (u"ࠣࡣࡪࡩࡳࡺࠢ☴"): None,
        bstack1l1llll_opy_ (u"ࠤࡨࡲࡩࡶ࡯ࡪࡰࡷࠦ☵"): url,
        bstack1l1llll_opy_ (u"ࠥ࡮ࡸࡵ࡮ࠣ☶"): bstack1lllll1l1111_opy_
    }
    try:
        bstack1lllll11l111_opy_ = response.json()
        if isinstance(bstack1lllll11l111_opy_, dict) and bstack1lllll11l111_opy_.get(bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ☷"), {}).get(bstack1l1llll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭☸"), {}).get(bstack1l1llll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ☹")):
            bstack1lll1lllllll_opy_ = json.loads(json.dumps(bstack1lllll11l111_opy_))
            bstack1lll1lllllll_opy_[bstack1l1llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ☺")][bstack1l1llll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ☻")][bstack1l1llll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ☼")] = bstack1l1llll_opy_ (u"ࠥ࡟ࡷ࡫ࡤࡢࡥࡷࡩࡩࠦࡦࡰࡴࠣࡦࡷ࡫ࡶࡪࡶࡼࡡࠧ☽")
            bstack1lllll11l111_opy_ = bstack1lll1lllllll_opy_
        if isinstance(bstack1lllll11l111_opy_, dict):
            bstack1llll11l1l1l_opy_(bstack1lllll11l111_opy_, bstack1llll1l11111_opy_)
            bstack1lll1llll11l_opy_(bstack1lllll11l111_opy_)
    except Exception:
        bstack1lllll11l111_opy_ = response.text
    bstack1lll11ll1ll1_opy_ = {
        bstack1l1llll_opy_ (u"ࠦࡧࡵࡤࡺࠤ☾"): bstack1lllll11l111_opy_,
        bstack1l1llll_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࡈࡵࡤࡦࠤ☿"): response.status_code
    }
    return {
        bstack1l1llll_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢ♀"): bstack1lll1l1111ll_opy_,
        bstack1l1llll_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤ♁"): bstack1lll11ll1ll1_opy_
    }
_1lll1lll1ll1_opy_ = None
def _resolve_proxy_ca_cert(config=None) -> Optional[str]:
    bstack1l1llll_opy_ (u"ࠣࠤࠥࡖࡪࡹ࡯࡭ࡸࡨࠤࡹ࡮ࡥࠡࡴࡤࡻࠥࡩࡵࡴࡶࡲࡱࡪࡸࠠࡄࡃࠣࡴࡦࡺࡨࠡࠪࡨࡲࡻࠦ࠾ࠡࡲࡤࡷࡸ࡫ࡤࠡࡥࡲࡲ࡫࡯ࡧࠡࡀࠣ࡫ࡱࡵࡢࡢ࡮ࠣࡇࡔࡔࡆࡊࡉࠬ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡥࡳࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡴࡨࡥࡩࡧࡢ࡭ࡧࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭࠲ࠠࡦ࡮ࡶࡩࠥࡔ࡯࡯ࡧ࠱ࠤࡓ࡫ࡶࡦࡴࠣࡶࡦ࡯ࡳࡦࡵ࠱ࠦࠧࠨ♂")
    candidates = []
    bstack1llll111l1ll_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡇ࡛ࡘࡗࡇ࡟ࡄࡃࡢࡇࡊࡘࡔࡔࠩ♃"))
    if bstack1llll111l1ll_opy_:
        candidates.append(bstack1llll111l1ll_opy_)
    if isinstance(config, dict) and config.get(bstack1l1llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡅࡤࡇࡪࡸࡴࡪࡨ࡬ࡧࡦࡺࡥࠨ♄")):
        candidates.append(config.get(bstack1l1llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡆࡥࡈ࡫ࡲࡵ࡫ࡩ࡭ࡨࡧࡴࡦࠩ♅")))
    try:
        from browserstack_sdk import CONFIG as _1111l1l11l_opy_
        if isinstance(_1111l1l11l_opy_, dict) and _1111l1l11l_opy_.get(bstack1l1llll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡇࡦࡉࡥࡳࡶ࡬ࡪ࡮ࡩࡡࡵࡧࠪ♆")):
            candidates.append(_1111l1l11l_opy_.get(bstack1l1llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡈࡧࡃࡦࡴࡷ࡭࡫࡯ࡣࡢࡶࡨࠫ♇")))
    except Exception:
        pass
    seen = set()
    candidates = [c for c in candidates if c and not (c in seen or seen.add(c))]
    for cand in candidates:
        try:
            p = str(cand)
            if os.path.isfile(p):
                return p
            logger.warning(bstack1l1llll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡉࡡࡄࡧࡵࡸ࡮࡬ࡩࡤࡣࡷࡩ࠿ࠦࡰࡢࡶ࡫ࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࠥࡵࡲࠡ࡫ࡶࠤࡳࡵࡴࠡࡣࠣࡪ࡮ࡲࡥ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪ࠾ࠥࡶࡡࡵࡪࡀࡿࢂ࠭♈").format(p))
        except Exception as e:
            logger.warning(bstack1l1llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡃࡢࡅࡨࡶࡹ࡯ࡦࡪࡥࡤࡸࡪࡀࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡴࠡࡥࡨࡶࡹࠦࡰࡢࡶ࡫࠾ࠥࡶࡡࡵࡪࡀࡿࢂࠦࡥࡳࡴࡲࡶࡂࢁࡽࠨ♉").format(cand, e))
    return None
def _load_custom_cert_pem(path) -> Optional[str]:
    bstack1l1llll_opy_ (u"ࠤࠥࠦࡗ࡫ࡡࡥࠢࡷ࡬ࡪࠦࡣࡶࡵࡷࡳࡲ࡫ࡲࠡࡅࡄࠤ࡫࡯࡬ࡦࠢࡤࡲࡩࠦࡲࡦࡶࡸࡶࡳࠦࡩࡵࡵࠣࡔࡊࡓࠠࡵࡧࡻࡸ࠱ࠦࡳࡶࡲࡳࡳࡷࡺࡩ࡯ࡩࠣࡆࡔ࡚ࡈࠡࡒࡈࡑࠏࠦࠠࠡࠢࠫࡷ࡮ࡴࡧ࡭ࡧࠣࡳࡷࠦ࡭ࡶ࡮ࡷ࡭࠲ࡩࡥࡳࡶࠣࡦࡺࡴࡤ࡭ࡧࠬࠤࡦࡴࡤࠡࡆࡈࡖࠥ࠮ࡢࡪࡰࡤࡶࡾ࠯ࠠ⠕ࠢࡤࡲࡩࠦࡡ࡯ࡻࠣࡪ࡮ࡲࡥࠡࡧࡻࡸࡪࡴࡳࡪࡱࡱࠎࠥࠦࠠࠡࠪ࠱ࡴࡪࡳࠠ࠰ࠢ࠱ࡧࡷࡺࠠ࠰ࠢ࠱ࡧࡪࡸࠠ࠰ࠢ࠱ࡨࡪࡸࠩ࠯ࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡒࡴࡴࡥࠡࡱࡱࠤ࡫ࡧࡩ࡭ࡷࡵࡩ࠳ࠦࡎࡦࡸࡨࡶࠥࡸࡡࡪࡵࡨࡷ࠳ࠨࠢࠣ♊")
    try:
        with open(path, bstack1l1llll_opy_ (u"ࠪࡶࡧ࠭♋")) as f:
            data = f.read()
        text = data.decode(bstack1l1llll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ♌"), errors=bstack1l1llll_opy_ (u"ࠬࡸࡥࡱ࡮ࡤࡧࡪ࠭♍"))
        if bstack1l1llll_opy_ (u"࠭࠭࠮࠯࠰࠱ࡇࡋࡇࡊࡐࠣࡇࡊࡘࡔࡊࡈࡌࡇࡆ࡚ࡅ࠮࠯࠰࠱࠲࠭♎") in text:
            return text
        import ssl as _ssl
        return _ssl.DER_cert_to_PEM_cert(data)
    except Exception as e:
        logger.warning(bstack1l1llll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡉࡡࡄࡧࡵࡸ࡮࡬ࡩࡤࡣࡷࡩ࠿ࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡳࡥࡷࡹࡥࠡࡽࢀࠤࡦࡹࠠࡑࡇࡐࠤࡴࡸࠠࡅࡇࡕ࠾ࠥࢁࡽࠨ♏").format(path, e))
        return None
def get_merged_ca_bundle(config=None) -> Optional[str]:
    bstack1l1llll_opy_ (u"ࠣࠤࠥࡆࡺ࡯࡬ࡥࠢࠫࡳࡳࡩࡥ࠭ࠢࡦࡥࡨ࡮ࡥࡥࠫࠣࡥࠥࡉࡁࠡࡤࡸࡲࡩࡲࡥࠡ࠿ࠣࡧࡪࡸࡴࡪࡨ࡬ࠤࡩ࡫ࡦࡢࡷ࡯ࡸࡸࠦࠫࠡࡶ࡫ࡩࠥࡩࡵࡴࡶࡲࡱࡪࡸࠠࡤࡧࡵࡸ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡ࡯ࡨࡶ࡬࡫ࡤࠡࡤࡸࡲࡩࡲࡥࠡࡲࡤࡸ࡭࠲ࠠࡰࡴࠣࡒࡴࡴࡥࠡࡹ࡫ࡩࡳࠦ࡮ࡰࠢࡦࡹࡸࡺ࡯࡮ࡧࡵࠤࡨ࡫ࡲࡵࠢ࡬ࡷࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠌࠣࠤࠥࠦ࡯ࡳࠢࡥࡹ࡮ࡲࡤࡪࡰࡪࠤ࡫ࡧࡩ࡭ࡵࠣࠬࡨࡧ࡬࡭ࡧࡵࠤ࡫ࡧ࡬࡭ࡵࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡹ࡮ࡥࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡷࡶࡺࡹࡴࠡࡵࡷࡳࡷ࡫ࠩ࠯ࠢࡑࡩࡻ࡫ࡲࠡࡴࡤ࡭ࡸ࡫ࡳ࠯ࠌࠣࠤࠥࠦࡓࡶࡲࡳࡳࡷࡺࡳࠡࡒࡈࡑࠥࡧ࡮ࡥࠢࡇࡉࡗࠦࡣࡶࡵࡷࡳࡲ࡫ࡲࠡࡥࡨࡶࡹࡹࠠࠩࡣࡱࡽࠥ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠪ࠰ࠥࠦࠧ♐")
    global _1lll1lll1ll1_opy_
    if _1lll1lll1ll1_opy_:
        return _1lll1lll1ll1_opy_
    raw = _resolve_proxy_ca_cert(config)
    if not raw:
        return None
    try:
        import certifi
        with open(certifi.where(), bstack1l1llll_opy_ (u"ࠩࡵࠫ♑"), encoding=bstack1l1llll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ♒"), errors=bstack1l1llll_opy_ (u"ࠫࡷ࡫ࡰ࡭ࡣࡦࡩࠬ♓")) as bstack1llll1llll11_opy_:
            base = bstack1llll1llll11_opy_.read()
        bstack1lll11lll111_opy_ = {os.path.abspath(certifi.where())}
        for _1llll1lll1l1_opy_ in (bstack1l1llll_opy_ (u"ࠬࡘࡅࡒࡗࡈࡗ࡙࡙࡟ࡄࡃࡢࡆ࡚ࡔࡄࡍࡇࠪ♔"), bstack1l1llll_opy_ (u"࠭ࡓࡔࡎࡢࡇࡊࡘࡔࡠࡈࡌࡐࡊ࠭♕")):
            _1llll11ll1ll_opy_ = os.environ.get(_1llll1lll1l1_opy_)
            if _1llll11ll1ll_opy_ and os.path.isfile(_1llll11ll1ll_opy_) and os.path.abspath(_1llll11ll1ll_opy_) not in bstack1lll11lll111_opy_:
                bstack1lll11lll111_opy_.add(os.path.abspath(_1llll11ll1ll_opy_))
                try:
                    with open(_1llll11ll1ll_opy_, bstack1l1llll_opy_ (u"ࠧࡳࠩ♖"), encoding=bstack1l1llll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ♗"), errors=bstack1l1llll_opy_ (u"ࠩࡵࡩࡵࡲࡡࡤࡧࠪ♘")) as _1lll1l11l111_opy_:
                        _extra = _1lll1l11l111_opy_.read()
                    if not base.endswith(bstack1l1llll_opy_ (u"ࠪࡠࡳ࠭♙")):
                        base += bstack1l1llll_opy_ (u"ࠫࡡࡴࠧ♚")
                    base += _extra
                except Exception as _1lll1l11ll11_opy_:
                    logger.debug(bstack1l1llll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡇࡦࡉࡥࡳࡶ࡬ࡪ࡮ࡩࡡࡵࡧ࠽ࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡧࡱ࡯ࡨࠥࢁࡽࠡ࡫ࡱࡸࡴࠦ࡭ࡦࡴࡪࡩࡩࠦࡢࡶࡰࡧࡰࡪࡀࠠࡼࡿࠪ♛").format(_1llll1lll1l1_opy_, _1lll1l11ll11_opy_))
        custom = _load_custom_cert_pem(raw)
        if not custom:
            return None
        bstack1lll1lll11ll_opy_ = tempfile.mkdtemp(prefix=bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬ࡡࡦࡥࡤ࠭♜"))
        bstack1llll1llll1l_opy_ = os.path.join(bstack1lll1lll11ll_opy_, bstack1l1llll_opy_ (u"ࠧࡤࡣࡢࡦࡺࡴࡤ࡭ࡧ࠱ࡴࡪࡳࠧ♝"))
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, bstack1l1llll_opy_ (u"ࠨࡑࡢࡒࡔࡌࡏࡍࡎࡒ࡛ࠬ♞"), 0)
        with os.fdopen(os.open(bstack1llll1llll1l_opy_, flags, 0o600), bstack1l1llll_opy_ (u"ࠩࡺࠫ♟"), encoding=bstack1l1llll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ♠")) as bstack1lll11ll1lll_opy_:
            bstack1lll11ll1lll_opy_.write(base)
            if not base.endswith(bstack1l1llll_opy_ (u"ࠫࡡࡴࠧ♡")):
                bstack1lll11ll1lll_opy_.write(bstack1l1llll_opy_ (u"ࠬࡢ࡮ࠨ♢"))
            bstack1lll11ll1lll_opy_.write(custom)
            if not custom.endswith(bstack1l1llll_opy_ (u"࠭࡜࡯ࠩ♣")):
                bstack1lll11ll1lll_opy_.write(bstack1l1llll_opy_ (u"ࠧ࡝ࡰࠪ♤"))
        import atexit
        import shutil
        atexit.register(shutil.rmtree, bstack1lll1lll11ll_opy_, ignore_errors=True)
        _1lll1lll1ll1_opy_ = bstack1llll1llll1l_opy_
        logger.debug(bstack1l1llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡃࡢࡅࡨࡶࡹ࡯ࡦࡪࡥࡤࡸࡪࡀࠠࡣࡷ࡬ࡰࡹࠦ࡭ࡦࡴࡪࡩࡩࠦࡃࡂࠢࡥࡹࡳࡪ࡬ࡦࠢࡤࡸࠥࢁࡽࠨ♥").format(bstack1llll1llll1l_opy_))
        return bstack1llll1llll1l_opy_
    except Exception as e:
        logger.warning(bstack1l1llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡄࡣࡆࡩࡷࡺࡩࡧ࡫ࡦࡥࡹ࡫࠺ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡧࡻࡩ࡭ࡦࠣࡱࡪࡸࡧࡦࡦࠣࡇࡆࠦࡢࡶࡰࡧࡰࡪ࠲ࠠࡧࡣ࡯ࡰ࡮ࡴࡧࠡࡤࡤࡧࡰࠦࡴࡰࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡸࡷࡻࡳࡵࠢࡶࡸࡴࡸࡥ࠻ࠢࡨࡶࡷࡵࡲ࠾ࡽࢀࠫ♦").format(e))
        return None
def configure_ca_environment(config=None) -> None:
    bstack1l1llll_opy_ (u"ࠥࠦࠧࡋࡸࡱࡱࡵࡸࠥࡺࡨࡦࠢࡰࡩࡷ࡭ࡥࡥࠢࡆࡅࠥࡨࡵ࡯ࡦ࡯ࡩࠥࡼࡩࡢࠢࡨࡲࡻࠦࡶࡢࡴࡶࠤࡸࡵࠠࡂࡎࡏࠤࡴࡻࡴࡣࡱࡸࡲࡩࠦࡈࡕࡖࡓࡗࠥ࡮࡯࡯ࡱࡵࡷࠥࡺࡨࡦࠌࠣࠤࠥࠦࡣࡶࡵࡷࡳࡲ࡫ࡲࠡࡅࡄࠤࡼ࡯ࡴࡩࡱࡸࡸࠥ࡫ࡶࡦࡴࡼࠤࡨࡧ࡬࡭ࠢࡶ࡭ࡹ࡫ࠠ࡯ࡧࡨࡨ࡮ࡴࡧࠡࡣࠣࡴࡦࡺࡣࡩ࠼ࠍࠤࠥࠦࠠࠡࠢ࠰ࠤࡗࡋࡑࡖࡇࡖࡘࡘࡥࡃࡂࡡࡅ࡙ࡓࡊࡌࡆࠢ࠲ࠤࡘ࡙ࡌࡠࡅࡈࡖ࡙ࡥࡆࡊࡎࡈࠤ࠲ࡄࠠࡵࡪࡨࠤࡘࡊࡋࠨࡵࠣࡳࡼࡴࠠࡳࡧࡴࡹࡪࡹࡴࡴࠢ࠲ࠤࡺࡸ࡬࡭࡫ࡥࠤࡨࡧ࡬࡭ࡵࠍࠤࠥࠦࠠࠡࠢ࠰ࠤࡓࡕࡄࡆࡡࡈ࡜࡙ࡘࡁࡠࡅࡄࡣࡈࡋࡒࡕࡕࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࡄࠠࡵࡪࡨࠤࡸࡶࡡࡸࡰࡨࡨࠥࡔ࡯ࡥࡧࠣࡦ࡮ࡴࡡࡳࡻࠪࡷࠥࡎࡔࡕࡒࡖࠎࠥࠦࠠࠡࡋࡧࡩࡲࡶ࡯ࡵࡧࡱࡸࡀࠦ࡮ࡦࡸࡨࡶࠥࡸࡡࡪࡵࡨࡷ࠳ࠦࡃࡢ࡮࡯ࠤࡴࡴࡣࡦࠢࡤࡪࡹ࡫ࡲࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡶࠤࡵࡧࡲࡴࡧࡧࠤ࠭ࡨࡥࡧࡱࡵࡩࠥࡧ࡮ࡺࠌࠣࠤࠥࠦࡦࡶࡰࡱࡩࡱࠦ࠯ࠡࡖࡨࡷࡹࡎࡵࡣࠢ࠲ࠤࡊࡊࡓࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡩ࡭ࡷ࡫ࡳࠪ࠰ࠥࠦࠧ♧")
    try:
        merged = get_merged_ca_bundle(config)
        if not merged:
            return
        os.environ[bstack1l1llll_opy_ (u"ࠫࡗࡋࡑࡖࡇࡖࡘࡘࡥࡃࡂࡡࡅ࡙ࡓࡊࡌࡆࠩ♨")] = merged
        os.environ[bstack1l1llll_opy_ (u"࡙ࠬࡓࡍࡡࡆࡉࡗ࡚࡟ࡇࡋࡏࡉࠬ♩")] = merged
        raw = _resolve_proxy_ca_cert(config)
        if raw:
            bstack1lll1ll1l111_opy_ = raw
            try:
                with open(raw, bstack1l1llll_opy_ (u"࠭ࡲࡣࠩ♪")) as _1lll1ll11l11_opy_:
                    if bstack1l1llll_opy_ (u"ࠧ࠮࠯࠰࠱࠲ࡈࡅࡈࡋࡑࠤࡈࡋࡒࡕࡋࡉࡍࡈࡇࡔࡆ࠯࠰࠱࠲࠳ࠧ♫") not in _1lll1ll11l11_opy_.read().decode(bstack1l1llll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ♬"), errors=bstack1l1llll_opy_ (u"ࠩࡵࡩࡵࡲࡡࡤࡧࠪ♭")):
                        bstack1lll1ll1l111_opy_ = merged
            except Exception:
                pass
            if not os.environ.get(bstack1l1llll_opy_ (u"ࠪࡒࡔࡊࡅࡠࡇ࡛ࡘࡗࡇ࡟ࡄࡃࡢࡇࡊࡘࡔࡔࠩ♮")):
                os.environ[bstack1l1llll_opy_ (u"ࠫࡓࡕࡄࡆࡡࡈ࡜࡙ࡘࡁࡠࡅࡄࡣࡈࡋࡒࡕࡕࠪ♯")] = bstack1lll1ll1l111_opy_
            os.environ.setdefault(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡊ࡞ࡔࡓࡃࡢࡇࡆࡥࡃࡆࡔࡗࡗࠬ♰"), bstack1lll1ll1l111_opy_)
        logger.debug(bstack1l1llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡈࡧࡃࡦࡴࡷ࡭࡫࡯ࡣࡢࡶࡨ࠾ࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢࡆࡅࠥ࡫࡮ࡷࠢࡹࡥࡷࡹࠠ࠮ࡀࠣࡿࢂ࠭♱").format(merged))
    except Exception as e:
        logger.warning(bstack1l1llll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡉࡡࡄࡧࡵࡸ࡮࡬ࡩࡤࡣࡷࡩ࠿ࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࡡࡦࡥࡤ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠧ♲").format(e))
def get_ca_cert_path(config) -> Optional[str]:
    return get_merged_ca_bundle(config)
def bstack1111ll1111_opy_(bstack1llll111lll1_opy_, url, data, config):
    headers = config.get(bstack1l1llll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ♳"), None)
    proxies = bstack1ll11l111l1_opy_(config, url)
    auth = config.get(bstack1l1llll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ♴"), None)
    timeout = config.get(bstack1l1llll_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࠫ♵"), None)
    bstack1llll1ll1ll1_opy_ = {
        bstack1l1llll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ♶"): headers,
        bstack1l1llll_opy_ (u"ࠬࡧࡵࡵࡪࠪ♷"): auth,
        bstack1l1llll_opy_ (u"࠭ࡪࡴࡱࡱࠫ♸"): data,
        bstack1l1llll_opy_ (u"ࠧࡱࡴࡲࡼ࡮࡫ࡳࠨ♹"): proxies,
        bstack1l1llll_opy_ (u"ࠨࡶ࡬ࡱࡪࡵࡵࡵࠩ♺"): timeout
    }
    if bstack1l1llll_opy_ (u"ࠩࡹࡩࡷ࡯ࡦࡺࠩ♻") in config:
        bstack1llll1ll1ll1_opy_[bstack1l1llll_opy_ (u"ࠪࡺࡪࡸࡩࡧࡻࠪ♼")] = config[bstack1l1llll_opy_ (u"ࠫࡻ࡫ࡲࡪࡨࡼࠫ♽")]
    else:
        cert_path = get_ca_cert_path(config)
        if cert_path:
            bstack1llll1ll1ll1_opy_[bstack1l1llll_opy_ (u"ࠬࡼࡥࡳ࡫ࡩࡽࠬ♾")] = cert_path
    response = requests.request(
            bstack1llll111lll1_opy_,
            url=url,
            **bstack1llll1ll1ll1_opy_
        )
    try:
        log_message = bstack1llll111111l_opy_(bstack1llll111lll1_opy_, url, response, headers, data)
        automation_logger.debug(json.dumps(log_message, separators=(bstack1l1llll_opy_ (u"࠭ࠬࠨ♿"), bstack1l1llll_opy_ (u"ࠧ࠻ࠩ⚀"))))
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶࡧࡶࡸ࠿ࠦࡻࡾࠤ⚁").format(e))
    return response
def instrument_driver_init_failure_event(error, bstack1lllll11111l_opy_=bstack1l1llll_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥ⚂")):
    try:
        try:
            stack = bstack1l1llll_opy_ (u"ࠥࠦ⚃").join(traceback.format_tb(error.__traceback__))
        except Exception:
            stack = bstack1l1llll_opy_ (u"ࠦࠧ⚄")
        bstack1lll11lllll1_opy_ = bstack1l1llll_opy_ (u"ࠧࡡࡄࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࡈࡶࡷࡵࡲ࡞ࠢࡾࢁࡡࡴࡻࡾࠤ⚅").format(error, stack)
        bstack1lll1l1l1lll_opy_ = len(bstack1lll11lllll1_opy_.encode(bstack1l1llll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ⚆"), errors=bstack1l1llll_opy_ (u"ࠢࡳࡧࡳࡰࡦࡩࡥࠣ⚇"))) - MAX_DRIVER_INIT_ERROR_BYTES
        error_message = bstack1lll1lll1111_opy_(bstack1lll11lllll1_opy_, bstack1lll1l1l1lll_opy_) if bstack1lll1l1l1lll_opy_ > 0 else bstack1lll11lllll1_opy_
        try:
            platform_index = int(os.environ.get(bstack1l1llll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣ⚈")) or bstack1l1llll_opy_ (u"ࠤ࠳ࠦ⚉"))
        except (TypeError, ValueError):
            platform_index = 0
        event_json = {
            bstack1l1llll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࡏࡨࡷࡸࡧࡧࡦࠤ⚊"): error_message,
            bstack1l1llll_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢ⚋"): os.environ.get(bstack1l1llll_opy_ (u"ࠧࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉࠨ⚌")) or bstack1l1llll_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢ⚍"),
            bstack1l1llll_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸࡔࡺࡲࡨࠦ⚎"): bstack1lllll11111l_opy_,
            bstack1l1llll_opy_ (u"ࠣࡧࡹࡩࡳࡺࠢ⚏"): EVENTS.SDK_DRIVER_INIT_FAILURE.value,
            bstack1l1llll_opy_ (u"ࠤࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠧ⚐"): int(time.time() * 1000),
            bstack1l1llll_opy_ (u"ࠥࡻࡴࡸ࡫ࡦࡴࠥ⚑"): os.environ.get(bstack1l1llll_opy_ (u"ࠦࡕ࡟ࡔࡆࡕࡗࡣ࡝ࡊࡉࡔࡖࡢ࡛ࡔࡘࡋࡆࡔࠥ⚒")) or os.environ.get(bstack1l1llll_opy_ (u"ࠧࡖࡁࡃࡑࡗࡣࡖ࡛ࡅࡖࡇࡌࡒࡉࡋࡘࠣ⚓")) or str(os.getpid()),
            bstack1l1llll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣ⚔"): platform_index,
            bstack1l1llll_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤ⚕"): global_config.get_property(bstack1l1llll_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥ⚖")) or os.environ.get(BROWSERSTACK_SDK_RUN_ID_ENV),
        }
        bstack11111ll1l1l_opy_ = global_config.get_property(bstack1l1llll_opy_ (u"ࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦ⚗")) or os.environ.get(bstack1l1llll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦ⚘"))
        bstack1111l1l1lll_opy_ = global_config.get_property(bstack1l1llll_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶࡏࡪࡿࠢ⚙")) or os.environ.get(bstack1l1llll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠣ⚚"))
        auth = (bstack11111ll1l1l_opy_, bstack1111l1l1lll_opy_) if bstack11111ll1l1l_opy_ and bstack1111l1l1lll_opy_ else None
        send_eds_event(bstack1l1llll_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࡉࡥ࡮ࡲࡵࡳࡧࠥ⚛"), event_json, bstack1lll1ll11111_opy_=bstack11111ll1l1l_opy_, auth=auth)
    except Exception as bstack1lll1l1ll1ll_opy_:
        logger.debug(bstack1l1llll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡࡆࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࡋࡧࡩ࡭ࡷࡵࡩࠥࡺ࡯ࠡࡇࡇࡗ࠿ࠦࡻࡾࠤ⚜").format(bstack1lll1l1ll1ll_opy_))
def send_eds_event(event_name, event_json, bstack1llll1111l1l_opy_=None, bstack1lll1ll11111_opy_=None, auth=None):
    if bstack1llll1111l1l_opy_ is None:
        bstack1llll1111l1l_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⚝")) or global_config.get_property(bstack1l1llll_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧࠦ⚞"))
    if bstack1lll1ll11111_opy_ is None:
        bstack1lll1ll11111_opy_ = global_config.get_property(bstack1l1llll_opy_ (u"ࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧ⚟"))
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        override = bstack11l11l111l_opy_(cli.config, [bstack1l1llll_opy_ (u"ࠦࡦࡶࡩࡴࠤ⚠"), bstack1l1llll_opy_ (u"ࠧ࡫ࡤࡴࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡦࡺࡩࡰࡰࠥ⚡"), bstack1l1llll_opy_ (u"ࠨࡡࡱ࡫ࠥ⚢")], None) if cli and cli.config else None
        url = bstack1l1llll_opy_ (u"ࠢࡼࡿ࠲ࡷࡪࡴࡤࡠࡵࡧ࡯ࡤ࡫ࡶࡦࡰࡷࡷࠧ⚣").format(override.rstrip(bstack1l1llll_opy_ (u"ࠣ࠱ࠥ⚤"))) if override else bstack1l1ll1l1ll_opy_
    except Exception:
        url = bstack1l1ll1l1ll_opy_
    payload = {
        bstack1l1llll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࠨ⚥"): bstack1l1llll_opy_ (u"ࠥࡷࡩࡱ࡟ࡦࡸࡨࡲࡹࡹࠢ⚦"),
        bstack1l1llll_opy_ (u"ࠦࡩࡧࡴࡢࠤ⚧"): {
            bstack1l1llll_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡵࡶ࡫ࡧࠦ⚨"): bstack1llll1111l1l_opy_,
            bstack1l1llll_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪ࡟ࡥࡣࡼࠦ⚩"): datetime.datetime.utcnow().strftime(bstack1l1llll_opy_ (u"࡛ࠢࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠠࡖࡖࡆࠦ⚪")),
            bstack1l1llll_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࠧ⚫"): event_name,
            bstack1l1llll_opy_ (u"ࠤࡸࡷࡪࡸ࡟ࡥࡣࡷࡥࠧ⚬"): bstack1lll1ll11111_opy_,
            bstack1l1llll_opy_ (u"ࠥ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴࠨ⚭"): get_host_info(),
            bstack1l1llll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢ࡮ࡸࡵ࡮ࠣ⚮"): event_json,
        },
    }
    config = {
        bstack1l1llll_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨ⚯"): {bstack1l1llll_opy_ (u"ࠨࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠧ⚰"): bstack1l1llll_opy_ (u"ࠢࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠥ⚱")},
        bstack1l1llll_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ⚲"): DRIVER_INIT_FAILURE_EDS_TIMEOUT_SECONDS,
    }
    if auth is not None:
        config[bstack1l1llll_opy_ (u"ࠤࡤࡹࡹ࡮ࠢ⚳")] = auth
    logger.debug(bstack1l1llll_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࡆࡢ࡫࡯ࡹࡷ࡫ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡽࢀࠦ⚴").format(json.dumps(event_json, default=str)))
    response = bstack1111ll1111_opy_(bstack1l1llll_opy_ (u"ࠦࡕࡕࡓࡕࠤ⚵"), url, payload, config)
    if response.status_code >= 400:
        logger.debug(bstack1l1llll_opy_ (u"ࠧࡋࡄࡔࠢࡨࡺࡪࡴࡴࠡࠩࡾࢁࠬࠦࡲࡦ࡬ࡨࡧࡹ࡫ࡤࠡࡾࠣࡗࡹࡧࡴࡶࡵࠣࡿࢂࠦࡼࠡࡒࡤࡽࡱࡵࡡࡥࠢࡾࢁࠧ⚶").format(
            event_name,
            response.status_code,
            json.dumps(event_json, default=str)
        ))
    else:
        logger.info(bstack1l1llll_opy_ (u"ࠨࡓࡦࡰࡷࠤࡊࡊࡓࠡࡧࡹࡩࡳࡺࠠࠨࡽࢀࠫࠥࢂࠠࡔࡶࡤࡸࡺࡹࠠࡼࡿࠥ⚷").format(event_name, response.status_code))
    return response
def bstack1ll1l11111l_opy_(bstack111111111_opy_, size):
    bstack1l1l11ll11l_opy_ = []
    while len(bstack111111111_opy_) > size:
        bstack1l1ll11l111_opy_ = bstack111111111_opy_[:size]
        bstack1l1l11ll11l_opy_.append(bstack1l1ll11l111_opy_)
        bstack111111111_opy_ = bstack111111111_opy_[size:]
    bstack1l1l11ll11l_opy_.append(bstack111111111_opy_)
    return bstack1l1l11ll11l_opy_
def bstack1llll1l111ll_opy_(message, bstack1lllll111ll1_opy_=False):
    os.write(1, bytes(message, bstack1l1llll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭⚸")))
    os.write(1, bytes(bstack1l1llll_opy_ (u"ࠨ࡞ࡱࠫ⚹"), bstack1l1llll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ⚺")))
    if bstack1lllll111ll1_opy_:
        with open(bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡳ࠶࠷ࡹ࠮ࠩ⚻") + os.environ[bstack1l1llll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪ⚼")] + bstack1l1llll_opy_ (u"ࠬ࠴࡬ࡰࡩࠪ⚽"), bstack1l1llll_opy_ (u"࠭ࡡࠨ⚾")) as f:
            f.write(message + bstack1l1llll_opy_ (u"ࠧ࡝ࡰࠪ⚿"))
def is_bstack_automation():
    return os.environ[bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ⛀")].lower() == bstack1l1llll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⛁")
def bstack1l1111ll_opy_():
    return bstack1llllllll_opy_().replace(tzinfo=None).isoformat() + bstack1l1llll_opy_ (u"ࠪ࡞ࠬ⛂")
def bstack1ll1l11ll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1llll_opy_ (u"ࠫ࡟࠭⛃"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1llll_opy_ (u"ࠬࡠࠧ⛄")))).total_seconds() * 1000
def bstack1lll1ll111l1_opy_(timestamp):
    return bstack1lll1lll1l11_opy_(timestamp).isoformat() + bstack1l1llll_opy_ (u"࡚࠭ࠨ⛅")
def bstack1lllll111l1l_opy_(bstack1lll11l1ll11_opy_):
    date_format = bstack1l1llll_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬ⛆")
    bstack1llll1ll1l1l_opy_ = datetime.datetime.strptime(bstack1lll11l1ll11_opy_, date_format)
    return bstack1llll1ll1l1l_opy_.isoformat() + bstack1l1llll_opy_ (u"ࠨ࡜ࠪ⛇")
def bstack1lll11ll11l1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⛈")
    else:
        return bstack1l1llll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⛉")
def bstack11lll11l1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1llll_opy_ (u"ࠫࡹࡸࡵࡦࠩ⛊")
def bstack1llll11lll1l_opy_(val):
    return val.__str__().lower() == bstack1l1llll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ⛋")
def error_handler(bstack1lll11ll1l11_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1lll11ll1l11_opy_ as e:
                print(bstack1l1llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨ⛌").format(func.__name__, bstack1lll11ll1l11_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1llll1l1l1ll_opy_(bstack1llll1ll1111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1llll1ll1111_opy_(cls, *args, **kwargs)
            except bstack1lll11ll1l11_opy_ as e:
                print(bstack1l1llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢ⛍").format(bstack1llll1ll1111_opy_.__name__, bstack1lll11ll1l11_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1llll1l1l1ll_opy_
    else:
        return decorator
def bstack111l11l11l_opy_(bstack1ll1llll_opy_):
    if os.getenv(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ⛎")) is not None:
        return bstack11lll11l1l_opy_(os.getenv(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ⛏")))
    if bstack1l1llll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ⛐") in bstack1ll1llll_opy_ and bstack1llll11lll1l_opy_(bstack1ll1llll_opy_[bstack1l1llll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ⛑")]):
        return False
    if bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ⛒") in bstack1ll1llll_opy_ and bstack1llll11lll1l_opy_(bstack1ll1llll_opy_[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ⛓")]):
        return False
    return True
def bstack1llll1l11l1_opy_():
    try:
        from pytest_bdd import reporting
        bstack1lll1ll1l1ll_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠢ⛔"), None)
        return bstack1lll1ll1l1ll_opy_ is None or bstack1lll1ll1l1ll_opy_ == bstack1l1llll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧ⛕")
    except Exception as e:
        return False
def bstack1l1l111ll11_opy_(hub_url, CONFIG):
    if bstack1l1ll11111_opy_() <= version.parse(bstack1l1llll_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ⛖")):
        if hub_url:
            return bstack1l1llll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ⛗") + hub_url + bstack1l1llll_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ⛘")
        return bstack1lll1111ll1_opy_
    if hub_url:
        return bstack1l1llll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ⛙") + hub_url + bstack1l1llll_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢ⛚")
    return bstack1ll1111ll_opy_
def bstack1llll1l11lll_opy_():
    return isinstance(os.getenv(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭⛛")), str)
def bstack11l1ll1l11_opy_(url):
    return urlparse(url).hostname
def bstack1lllll11ll1_opy_(hostname):
    for bstack1l1l1l1l1l1_opy_ in bstack1l1l111lll1_opy_:
        regex = re.compile(bstack1l1l1l1l1l1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1lllll1111l1_opy_(bstack1lll1l1l1l1l_opy_, file_name, logger):
    bstack111lll111l_opy_ = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠨࢀࠪ⛜")), bstack1lll1l1l1l1l_opy_)
    try:
        if not os.path.exists(bstack111lll111l_opy_):
            os.makedirs(bstack111lll111l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠩࢁࠫ⛝")), bstack1lll1l1l1l1l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1llll_opy_ (u"ࠪࡻࠬ⛞")):
                pass
            with open(file_path, bstack1l1llll_opy_ (u"ࠦࡼ࠱ࠢ⛟")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1lll11lll1l_opy_.format(str(e)))
def bstack1llll1l1l1l1_opy_(file_name, key, value, logger):
    file_path = bstack1lllll1111l1_opy_(bstack1l1llll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ⛠"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lll111111l_opy_ = json.load(open(file_path, bstack1l1llll_opy_ (u"࠭ࡲࡣࠩ⛡")))
        else:
            bstack1lll111111l_opy_ = {}
        bstack1lll111111l_opy_[key] = value
        with open(file_path, bstack1l1llll_opy_ (u"ࠢࡸ࠭ࠥ⛢")) as outfile:
            json.dump(bstack1lll111111l_opy_, outfile)
def bstack1ll1ll1llll_opy_(file_name, logger):
    file_path = bstack1lllll1111l1_opy_(bstack1l1llll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ⛣"), file_name, logger)
    bstack1lll111111l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1llll_opy_ (u"ࠩࡵࠫ⛤")) as bstack1l111ll1ll_opy_:
            bstack1lll111111l_opy_ = json.load(bstack1l111ll1ll_opy_)
    return bstack1lll111111l_opy_
def bstack11llll11l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧ⛥") + file_path + bstack1l1llll_opy_ (u"ࠫࠥ࠭⛦") + str(e))
def bstack1l1ll11111_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1llll_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢ⛧")
def bstack11l1ll1111_opy_(config):
    if bstack1l1llll_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ⛨") in config:
        del (config[bstack1l1llll_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭⛩")])
        return False
    if bstack1l1ll11111_opy_() < version.parse(bstack1l1llll_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧ⛪")):
        return False
    if bstack1l1ll11111_opy_() >= version.parse(bstack1l1llll_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨ⛫")):
        return True
    if bstack1l1llll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ⛬") in config and config[bstack1l1llll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ⛭")] is False:
        return False
    else:
        return True
def bstack11l11111ll_opy_(args_list, bstack1llll11ll11l_opy_):
    index = -1
    for value in bstack1llll11ll11l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11111lllll1_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11111lllll1_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l1l1ll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l1l1ll1_opy_ = bstack1l1l1ll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⛮"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⛯"), exception=exception)
    def failure_type(self):
        if self.result != bstack1l1llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⛰"):
            return None
        if isinstance(self.exception_type, str) and bstack1l1llll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦ⛱") in self.exception_type:
            return bstack1l1llll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥ⛲")
        return bstack1l1llll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ⛳")
    def bstack1lll11l11l1l_opy_(self):
        if self.result != bstack1l1llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⛴"):
            return None
        if self.bstack1l1l1ll1_opy_:
            return self.bstack1l1l1ll1_opy_
        return bstack1lll1l1l1l11_opy_(self.exception)
def bstack1lll1l1l1l11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1llll1111l11_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11llll11_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack111l11111_opy_(config, logger):
    try:
        import playwright
        bstack1llll1111lll_opy_ = playwright.__file__
        bstack1llll1ll111l_opy_ = os.path.split(bstack1llll1111lll_opy_)
        bstack1lll1l111l1l_opy_ = bstack1llll1ll111l_opy_[0] + bstack1l1llll_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨ⛵")
        os.environ[bstack1l1llll_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩ⛶")] = bstack1l111ll111_opy_(config)
        with open(bstack1lll1l111l1l_opy_, bstack1l1llll_opy_ (u"ࠧࡳࠩ⛷")) as f:
            file_content = f.read()
            bstack1lll1llll1l1_opy_ = bstack1l1llll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧ⛸")
            bstack1lll1l111ll1_opy_ = file_content.find(bstack1lll1llll1l1_opy_)
            if bstack1lll1l111ll1_opy_ == -1:
              process = subprocess.Popen(bstack1l1llll_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨ⛹"), shell=True, cwd=bstack1llll1ll111l_opy_[0])
              process.wait()
              bstack1lll11l1ll1l_opy_ = bstack1l1llll_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪ⛺")
              bstack1lll1l1lllll_opy_ = bstack1l1llll_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣ⛻")
              bstack1lll1l1llll1_opy_ = file_content.replace(bstack1lll11l1ll1l_opy_, bstack1lll1l1lllll_opy_)
              with open(bstack1lll1l111l1l_opy_, bstack1l1llll_opy_ (u"ࠬࡽࠧ⛼")) as f:
                f.write(bstack1lll1l1llll1_opy_)
    except Exception as e:
        logger.error(bstack1ll1l1l1l1_opy_.format(str(e)))
def bstack1ll11ll1ll1_opy_():
  try:
    bstack1llll1lllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1llll_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭⛽"))
    bstack1lll1l1ll11l_opy_ = []
    if os.path.exists(bstack1llll1lllll1_opy_):
      with open(bstack1llll1lllll1_opy_) as f:
        bstack1lll1l1ll11l_opy_ = json.load(f)
      os.remove(bstack1llll1lllll1_opy_)
    return bstack1lll1l1ll11l_opy_
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠢࡨࡧࡷࡣࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱࡹࠠࡳࡧࡤࡨ࠴ࡶࡡࡳࡵࡨࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽ࠻ࠢࡾࢁࠧ⛾").format(type(e).__name__, e))
  return []
def bstack1lll11l111_opy_(bstack1l1l1llllll_opy_):
  try:
    bstack1lll1l1ll11l_opy_ = []
    bstack1llll1lllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1llll_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨ⛿"))
    if os.path.exists(bstack1llll1lllll1_opy_):
      with open(bstack1llll1lllll1_opy_) as f:
        bstack1lll1l1ll11l_opy_ = json.load(f)
    bstack1lll1l1ll11l_opy_.append(bstack1l1l1llllll_opy_)
    with open(bstack1llll1lllll1_opy_, bstack1l1llll_opy_ (u"ࠩࡺࠫ✀")) as f:
        json.dump(bstack1lll1l1ll11l_opy_, f)
  except Exception as e:
    logger.debug(bstack1l1llll_opy_ (u"ࠥࡷࡪࡺ࡟ࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭ࡵࠣࡻࡷ࡯ࡴࡦࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࡀࠠࡼࡿࠥ✁").format(type(e).__name__, e))
def bstack11l1ll11ll_opy_(logger, bstack1lll1l1ll111_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1llll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ✂"), bstack1l1llll_opy_ (u"ࠬ࠭✃"))
    if test_name == bstack1l1llll_opy_ (u"࠭ࠧ✄"):
        test_name = threading.current_thread().__dict__.get(bstack1l1llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭✅"), bstack1l1llll_opy_ (u"ࠨࠩ✆"))
    bstack1llll1l11l11_opy_ = bstack1l1llll_opy_ (u"ࠩ࠯ࠤࠬ✇").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1lll1l1ll111_opy_:
        bstack1ll1l111l1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ✈"), bstack1l1llll_opy_ (u"ࠫ࠵࠭✉"))
        bstack1111lllll1_opy_ = {bstack1l1llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ✊"): test_name, bstack1l1llll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ✋"): bstack1llll1l11l11_opy_, bstack1l1llll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭✌"): bstack1ll1l111l1_opy_}
        bstack1lll1lllll11_opy_ = []
        bstack1llll1111111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧ✍"))
        if os.path.exists(bstack1llll1111111_opy_):
            with open(bstack1llll1111111_opy_) as f:
                bstack1lll1lllll11_opy_ = json.load(f)
        bstack1lll1lllll11_opy_.append(bstack1111lllll1_opy_)
        with open(bstack1llll1111111_opy_, bstack1l1llll_opy_ (u"ࠩࡺࠫ✎")) as f:
            json.dump(bstack1lll1lllll11_opy_, f)
    else:
        bstack1111lllll1_opy_ = {bstack1l1llll_opy_ (u"ࠪࡲࡦࡳࡥࠨ✏"): test_name, bstack1l1llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ✐"): bstack1llll1l11l11_opy_, bstack1l1llll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ✑"): str(multiprocessing.current_process().name)}
        if bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪ✒") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1111lllll1_opy_)
  except Exception as e:
      logger.warn(bstack1l1llll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ✓").format(e))
def bstack1ll1l1l11l_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫ✔"))
    try:
      bstack1lll1l11llll_opy_ = []
      bstack1111lllll1_opy_ = {bstack1l1llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ✕"): test_name, bstack1l1llll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ✖"): error_message, bstack1l1llll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ✗"): index}
      bstack1llll11lll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭✘"))
      if os.path.exists(bstack1llll11lll11_opy_):
          with open(bstack1llll11lll11_opy_) as f:
              bstack1lll1l11llll_opy_ = json.load(f)
      bstack1lll1l11llll_opy_.append(bstack1111lllll1_opy_)
      with open(bstack1llll11lll11_opy_, bstack1l1llll_opy_ (u"࠭ࡷࠨ✙")) as f:
          json.dump(bstack1lll1l11llll_opy_, f)
    except Exception as e:
      logger.warn(bstack1l1llll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥ✚").format(e))
    return
  bstack1lll1l11llll_opy_ = []
  bstack1111lllll1_opy_ = {bstack1l1llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭✛"): test_name, bstack1l1llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ✜"): error_message, bstack1l1llll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ✝"): index}
  bstack1llll11lll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ✞"))
  lock_file = bstack1llll11lll11_opy_ + bstack1l1llll_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮ࠫ✟")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1llll11lll11_opy_):
          with open(bstack1llll11lll11_opy_, bstack1l1llll_opy_ (u"࠭ࡲࠨ✠")) as f:
              content = f.read().strip()
              if content:
                  bstack1lll1l11llll_opy_ = json.load(open(bstack1llll11lll11_opy_))
      bstack1lll1l11llll_opy_.append(bstack1111lllll1_opy_)
      with open(bstack1llll11lll11_opy_, bstack1l1llll_opy_ (u"ࠧࡸࠩ✡")) as f:
          json.dump(bstack1lll1l11llll_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1llll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡬ࡩ࡭ࡧࠣࡰࡴࡩ࡫ࡪࡰࡪ࠾ࠥࢁࡽࠣ✢").format(e))
def bstack1ll11l11ll1_opy_(bstack1l11ll1l11_opy_, name, logger):
  try:
    bstack1111lllll1_opy_ = {bstack1l1llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ✣"): name, bstack1l1llll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ✤"): bstack1l11ll1l11_opy_, bstack1l1llll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ✥"): str(threading.current_thread()._name)}
    return bstack1111lllll1_opy_
  except Exception as e:
    logger.warn(bstack1l1llll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤ✦").format(e))
  return
def bstack1lll1l1lll1l_opy_():
    return platform.system() == bstack1l1llll_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼࡹࠧ✧")
def bstack1llll1l1l111_opy_(binary_path):
    if not binary_path or not os.path.exists(binary_path):
        return False
    if platform.system() == bstack1l1llll_opy_ (u"ࠧࡅࡣࡵࡻ࡮ࡴࠧ✨"):
        return False
    try:
        with open(binary_path, bstack1l1llll_opy_ (u"ࠨࡴ࠮ࡦࠬ✩")) as f:
            pass
        return False
    except OSError as e:
        if hasattr(e, bstack1l1llll_opy_ (u"ࠩࡨࡶࡷࡴ࡯ࠨ✪")) and e.errno == getattr(errno, bstack1l1llll_opy_ (u"ࠪࡉ࡙࡞ࡔࡃࡕ࡜ࠫ✫"), 26):
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡇ࡯࡮ࡢࡴࡼࠤ࡮ࡹࠠࡣࡷࡶࡽࠥ࠮ࡅࡕ࡚ࡗࡆࡘ࡟ࠩ࠻ࠢࠥ✬") + str(binary_path) + bstack1l1llll_opy_ (u"ࠧࠨ✭"))
            return True
        if hasattr(e, bstack1l1llll_opy_ (u"࠭ࡷࡪࡰࡨࡶࡷࡵࡲࠨ✮")) and e.bstack11lll1ll111_opy_ == bstack11lll1l11l1_opy_:
            logger.debug(bstack1l1llll_opy_ (u"ࠢࡃ࡫ࡱࡥࡷࡿࠠࡪࡵࠣࡦࡺࡹࡹ࡚ࠡࠪ࡭ࡳࡪ࡯ࡸࡵࠬ࠾ࠥࠨ✯") + str(binary_path) + bstack1l1llll_opy_ (u"ࠣࠤ✰"))
            return True
        logger.debug(bstack1l1llll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣ࡭࡫ࠦࡢࡪࡰࡤࡶࡾࠦࡩࡴࠢࡥࡹࡸࡿ࠺ࠡࠤ✱") + str(e) + bstack1l1llll_opy_ (u"ࠥࠦ✲"))
        return False
def _1llll111l11l_opy_(err):
    bstack1l1llll_opy_ (u"ࠦࠧࠨࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡣࡱࠤࡔ࡙ࡅࡳࡴࡲࡶࠥ࡯࡮ࡥ࡫ࡦࡥࡹ࡫ࡳࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡶࠤࡧࡻࡳࡺࠢࠫࡐ࡮ࡴࡵࡹࠢࡈࡘ࡝࡚ࡂࡔ࡛ࠣࡳࡷࠦࡗࡪࡰࡧࡳࡼࡹࠠࡴࡪࡤࡶ࡮ࡴࡧࠡࡸ࡬ࡳࡱࡧࡴࡪࡱࡱ࠭࠳ࠨࠢࠣ✳")
    if hasattr(err, bstack1l1llll_opy_ (u"ࠬ࡫ࡲࡳࡰࡲࠫ✴")) and err.errno == getattr(errno, bstack1l1llll_opy_ (u"࠭ࡅࡕ࡚ࡗࡆࡘ࡟ࠧ✵"), 26):
        return True
    if hasattr(err, bstack1l1llll_opy_ (u"ࠧࡸ࡫ࡱࡩࡷࡸ࡯ࡳࠩ✶")) and err.bstack11lll1ll111_opy_ == bstack11lll1l11l1_opy_:
        return True
    return False
def _1lll1ll111ll_opy_(filepath):
    bstack1l1llll_opy_ (u"ࠣࠤࠥࡗࡦ࡬ࡥ࡭ࡻࠣࡨࡪࡲࡥࡵࡧࠣࡥࠥ࡬ࡩ࡭ࡧ࠯ࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠥࡽࡡࡳࡰ࡬ࡲ࡬ࠦ࡯࡯ࠢࡩࡥ࡮ࡲࡵࡳࡧ࠱ࠦࠧࠨ✷")
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        logger.warning(bstack1l1llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥ࡭ࡧࡷࡩࠥ࡬ࡩ࡭ࡧࠣࡿ࡫࡯࡬ࡦࡲࡤࡸ࡭ࢃ࠺ࠡࠤ✸") + str(e) + bstack1l1llll_opy_ (u"ࠥࠦ✹"))
_1llll11lllll_opy_ = re.compile(bstack1l1llll_opy_ (u"ࡶࠬ࠴ࠪ࡝࠰ࡷࡱࡵࡢ࠮࡝ࡦ࠮ࠨࠬ✺"))
def _1lll1ll1lll1_opy_(bstack1llll11111l1_opy_, bstack1lll11lll1l1_opy_=120):
    bstack1l1llll_opy_ (u"ࠧࠨࠢࡔࡹࡨࡩࡵࠦ࡯ࡳࡲ࡫ࡥࡳࠦࡻ࡯ࡣࡰࡩࢂ࠴ࡴ࡮ࡲ࠱ࡿࡵ࡯ࡤࡾࠢࡩ࡭ࡱ࡫ࡳࠡ࡮ࡨࡪࡹࠦࡢࡺࠢࡦࡶࡦࡹࡨࡦࡦࠣࡴࡪ࡫ࡲࠡࡹࡲࡶࡰ࡫ࡲࡴ࠰ࠍࠤࠥࠦࠠࡔ࡭࡬ࡴࠥ࡬ࡩ࡭ࡧࡶࠤࡳ࡫ࡷࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࡯ࡤࡼࡤࡧࡧࡦࡡࡶࠤ⠙ࠦࡣࡰࡷ࡯ࡨࠥࡨࡥࠡࡣࠣࡰ࡮ࡼࡥࠡࡧࡻࡸࡷࡧࡣࡵࠢࡩࡶࡴࡳࠠࡢࠢࡳࡩࡪࡸ࠮ࠋࠢࠣࠤࠥࠨࠢࠣ✻")
    threshold = time.time() - bstack1lll11lll1l1_opy_
    try:
        for name in os.listdir(bstack1llll11111l1_opy_):
            if not _1llll11lllll_opy_.match(name):
                continue
            path = os.path.join(bstack1llll11111l1_opy_, name)
            try:
                if os.path.getmtime(path) < threshold:
                    _1lll1ll111ll_opy_(path)
            except OSError:
                continue
    except OSError as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡧࡦࡴࠠࡴࡶࡤࡰࡪࠦࡴࡦ࡯ࡳࠤ࡫࡯࡬ࡦࡵ࠽ࠤࠧ✼") + str(e) + bstack1l1llll_opy_ (u"ࠢࠣ✽"))
def bstack1ll111lllll_opy_(bstack1lll1l11l11l_opy_, config, logger):
    bstack1lll11l1llll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1lll1l11l11l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡬ࡵࡧࡵࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡰ࡫ࡹࡴࠢࡥࡽࠥࡸࡥࡨࡧࡻࠤࡲࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ✾").format(e))
    return bstack1lll11l1llll_opy_
def bstack1111l111l1l_opy_(bstack1llll1l11ll1_opy_, bstack1llll1llllll_opy_):
    bstack1llll11l1111_opy_ = version.parse(bstack1llll1l11ll1_opy_)
    bstack1lll11ll1111_opy_ = version.parse(bstack1llll1llllll_opy_)
    if bstack1llll11l1111_opy_ > bstack1lll11ll1111_opy_:
        return 1
    elif bstack1llll11l1111_opy_ < bstack1lll11ll1111_opy_:
        return -1
    else:
        return 0
def bstack1llllllll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1lll1lll1l11_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1lll11l1l11l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1ll11ll1l1_opy_(options, framework, config, bstack1l1l111lll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l1llll_opy_ (u"ࠩࡪࡩࡹ࠭✿"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1l11l1l_opy_ = caps.get(bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ❀"))
    bstack1llll111llll_opy_ = True
    bstack1111l1ll11_opy_ = os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ❁")]
    bstack11ll1l111ll_opy_ = config.get(bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ❂"), False)
    if bstack11ll1l111ll_opy_:
        bstack11llll1lll1_opy_ = config.get(bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭❃"), {})
        bstack11llll1lll1_opy_[bstack1l1llll_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪ❄")] = os.getenv(bstack1l1llll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭❅"))
        bstack11111lll1_opy_ = json.loads(os.getenv(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ❆"), bstack1l1llll_opy_ (u"ࠪࡿࢂ࠭❇"))).get(bstack1l1llll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ❈"))
    if bstack1llll11lll1l_opy_(caps.get(bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡘ࠵ࡆࠫ❉"))) or bstack1llll11lll1l_opy_(caps.get(bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ࠭❊"))):
        bstack1llll111llll_opy_ = False
    if bstack11l1ll1111_opy_({bstack1l1llll_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢ❋"): bstack1llll111llll_opy_}):
        bstack1l1l11l1l_opy_ = bstack1l1l11l1l_opy_ or {}
        bstack1l1l11l1l_opy_[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ❌")] = bstack1lll11l1l11l_opy_(framework)
        bstack1l1l11l1l_opy_[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ❍")] = is_bstack_automation()
        bstack1l1l11l1l_opy_[bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭❎")] = bstack1111l1ll11_opy_
        bstack1l1l11l1l_opy_[bstack1l1llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭❏")] = bstack1l1l111lll_opy_
        if bstack11ll1l111ll_opy_:
            bstack1l1l11l1l_opy_[bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ❐")] = bstack11ll1l111ll_opy_
            bstack1l1l11l1l_opy_[bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭❑")] = bstack11llll1lll1_opy_
            bstack1l1l11l1l_opy_[bstack1l1llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ❒")][bstack1l1llll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ❓")] = bstack11111lll1_opy_
        if getattr(options, bstack1l1llll_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪ❔"), None):
            options.set_capability(bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ❕"), bstack1l1l11l1l_opy_)
        else:
            options[bstack1l1llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ❖")] = bstack1l1l11l1l_opy_
    else:
        if getattr(options, bstack1l1llll_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭❗"), None):
            options.set_capability(bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ❘"), bstack1lll11l1l11l_opy_(framework))
            options.set_capability(bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ❙"), is_bstack_automation())
            options.set_capability(bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ❚"), bstack1111l1ll11_opy_)
            options.set_capability(bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ❛"), bstack1l1l111lll_opy_)
            if bstack11ll1l111ll_opy_:
                options.set_capability(bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ❜"), bstack11ll1l111ll_opy_)
                options.set_capability(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ❝"), bstack11llll1lll1_opy_)
                options.set_capability(bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ࠲ࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ❞"), bstack11111lll1_opy_)
        else:
            options[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ❟")] = bstack1lll11l1l11l_opy_(framework)
            options[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ❠")] = is_bstack_automation()
            options[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ❡")] = bstack1111l1ll11_opy_
            options[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ❢")] = bstack1l1l111lll_opy_
            if bstack11ll1l111ll_opy_:
                options[bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ❣")] = bstack11ll1l111ll_opy_
                options[bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ❤")] = bstack11llll1lll1_opy_
                options[bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ❥")][bstack1l1llll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ❦")] = bstack11111lll1_opy_
    return options
def bstack1lll1l1l11l1_opy_(ws_endpoint, framework):
    bstack1l1l111lll_opy_ = global_config.get_property(bstack1l1llll_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤ❧"))
    if ws_endpoint and len(ws_endpoint.split(bstack1l1llll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ❨"))) > 1:
        ws_url = ws_endpoint.split(bstack1l1llll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ❩"))[0]
        if bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭❪") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1lll1ll1ll1l_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack1l1llll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ❫"))[1]))
            bstack1lll1ll1ll1l_opy_ = bstack1lll1ll1ll1l_opy_ or {}
            bstack1111l1ll11_opy_ = os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ❬")]
            bstack1lll1ll1ll1l_opy_[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ❭")] = str(framework) + str(__version__)
            bstack1lll1ll1ll1l_opy_[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ❮")] = is_bstack_automation()
            bstack1lll1ll1ll1l_opy_[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ❯")] = bstack1111l1ll11_opy_
            bstack1lll1ll1ll1l_opy_[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ❰")] = bstack1l1l111lll_opy_
            ws_endpoint = ws_endpoint.split(bstack1l1llll_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ❱"))[0] + bstack1l1llll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ❲") + urllib.parse.quote(json.dumps(bstack1lll1ll1ll1l_opy_))
    return ws_endpoint
def bstack1l1l11l1l1l_opy_():
    global bstack11l1111lll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11l1111lll_opy_ = BrowserType.connect
    return bstack11l1111lll_opy_
def bstack1llll11l1lll_opy_(framework_name):
    global FRAMEWORK_NAME
    FRAMEWORK_NAME = framework_name
    return framework_name
def bstack1l11l1l11l1_opy_(self, *args, **kwargs):
    global bstack11l1111lll_opy_
    try:
        global FRAMEWORK_NAME
        if bstack1l1llll_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ❳") in kwargs:
            kwargs[bstack1l1llll_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪ❴")] = bstack1lll1l1l11l1_opy_(
                kwargs.get(bstack1l1llll_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫ❵"), None),
                FRAMEWORK_NAME
            )
    except Exception as e:
        logger.error(bstack1l1llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣ❶").format(str(e)))
    return bstack11l1111lll_opy_(self, *args, **kwargs)
def bstack1lllll111lll_opy_(bstack1lll11ll11ll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1ll11l111l1_opy_(bstack1lll11ll11ll_opy_, bstack1l1llll_opy_ (u"ࠤࠥ❷"))
        if proxies and proxies.get(bstack1l1llll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤ❸")):
            parsed_url = urlparse(proxies.get(bstack1l1llll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥ❹")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l1llll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨ❺")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l1llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩ❻")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l1llll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ❼")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l1llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫ❽")] = str(parsed_url.password)
        return proxy_settings
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠤࡳࡶࡴࡾࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡴࡦࡸࡳࡦࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࡀࠠࡼࡿࠥ❾").format(type(e).__name__, e))
        return proxy_settings
def bstack1lll11l11l1_opy_(bstack1lll11ll11ll_opy_):
    bstack1llll1l1l11l_opy_ = {
        bstack11111111ll1_opy_[bstack1lll11llll11_opy_]: bstack1lll11ll11ll_opy_[bstack1lll11llll11_opy_]
        for bstack1lll11llll11_opy_ in bstack1lll11ll11ll_opy_
        if bstack1lll11llll11_opy_ in bstack11111111ll1_opy_
    }
    bstack1llll1l1l11l_opy_[bstack1l1llll_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥ❿")] = bstack1lllll111lll_opy_(bstack1lll11ll11ll_opy_, global_config.get_property(bstack1l1llll_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦ➀")))
    bstack1lllll11ll11_opy_ = [element.lower() for element in bstack11111111111_opy_]
    bstack1llll11l1l1l_opy_(bstack1llll1l1l11l_opy_, bstack1lllll11ll11_opy_)
    return bstack1llll1l1l11l_opy_
def bstack1llll11l1l1l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l1llll_opy_ (u"ࠧ࠰ࠪࠫࠬࠥ➁")
    for value in d.values():
        if isinstance(value, dict):
            bstack1llll11l1l1l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1llll11l1l1l_opy_(item, keys)
def get_writable_dir():
    bstack1lll11l1lll1_opy_ = [os.environ.get(bstack1l1llll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡉࡍࡇࡖࡣࡉࡏࡒࠣ➂")), os.path.join(os.path.expanduser(bstack1l1llll_opy_ (u"ࠢࡿࠤ➃")), bstack1l1llll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ➄")), os.path.join(bstack1l1llll_opy_ (u"ࠩ࠲ࡸࡲࡶࠧ➅"), bstack1l1llll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ➆"))]
    for path in bstack1lll11l1lll1_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l1llll_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦ➇") + str(path) + bstack1l1llll_opy_ (u"ࠧ࠭ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠣ➈"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l1llll_opy_ (u"ࠨࡇࡪࡸ࡬ࡲ࡬ࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶࠤ࡫ࡵࡲࠡࠩࠥ➉") + str(path) + bstack1l1llll_opy_ (u"ࠢࠨࠤ➊"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l1llll_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣ➋") + str(path) + bstack1l1llll_opy_ (u"ࠤࠪࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡮ࡡࡴࠢࡷ࡬ࡪࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠴ࠢ➌"))
            else:
                logger.debug(bstack1l1llll_opy_ (u"ࠥࡇࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࠫࠧ➍") + str(path) + bstack1l1llll_opy_ (u"ࠦࠬࠦࡷࡪࡶ࡫ࠤࡼࡸࡩࡵࡧࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴ࠮ࠣ➎"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡕࡰࡦࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡸࡧࡨ࡫ࡥࡥࡧࡧࠤ࡫ࡵࡲࠡࠩࠥ➏") + str(path) + bstack1l1llll_opy_ (u"ࠨࠧ࠯ࠤ➐"))
            return path
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡶࡲࠣࡪ࡮ࡲࡥࠡࠩࡾࡴࡦࡺࡨࡾࠩ࠽ࠤࠧ➑") + str(e) + bstack1l1llll_opy_ (u"ࠣࠤ➒"))
    logger.debug(bstack1l1llll_opy_ (u"ࠤࡄࡰࡱࠦࡰࡢࡶ࡫ࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠨ➓"))
    return None
@measure(event_name=EVENTS.bstack11111111l1l_opy_, stage=STAGE.SINGLE)
def bstack1l11l11ll_opy_(binary_path, bstack1l11ll11l_opy_, bs_config):
    logger.debug(bstack1l1llll_opy_ (u"ࠥࡇࡺࡸࡲࡦࡰࡷࠤࡈࡒࡉࠡࡒࡤࡸ࡭ࠦࡦࡰࡷࡱࡨ࠿ࠦࡻࡾࠤ➔").format(binary_path))
    bstack1lllll1111ll_opy_ = bstack1l1llll_opy_ (u"ࠫࠬ➕")
    bstack1llll11l1l11_opy_ = {
        bstack1l1llll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ➖"): __version__,
        bstack1l1llll_opy_ (u"ࠨ࡯ࡴࠤ➗"): platform.system(),
        bstack1l1llll_opy_ (u"ࠢࡰࡵࡢࡥࡷࡩࡨࠣ➘"): platform.machine(),
        bstack1l1llll_opy_ (u"ࠣࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ➙"): bstack1l1llll_opy_ (u"ࠩ࠳ࠫ➚"),
        bstack1l1llll_opy_ (u"ࠥࡷࡩࡱ࡟࡭ࡣࡱ࡫ࡺࡧࡧࡦࠤ➛"): bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ➜")
    }
    bstack1llll1l1111l_opy_(bstack1llll11l1l11_opy_)
    try:
        if binary_path:
            if bstack1llll1l1l111_opy_(binary_path):
                logger.warning(bstack1l1llll_opy_ (u"ࠧࡋࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡵࠣࡧࡺࡸࡲࡦࡰࡷࡰࡾࠦࡩ࡯ࠢࡸࡷࡪ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡸࡴࡩࡧࡴࡦ࠼ࠣࠦ➝") + str(binary_path) + bstack1l1llll_opy_ (u"ࠨࠢ➞"))
                return binary_path
            try:
                if bstack1lll1l1lll1l_opy_():
                    bstack1llll11l1l11_opy_[bstack1l1llll_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ➟")] = subprocess.check_output([binary_path, bstack1l1llll_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤ➠")]).strip().decode(bstack1l1llll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ➡"))
                else:
                    bstack1llll11l1l11_opy_[bstack1l1llll_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ➢")] = subprocess.check_output([binary_path, bstack1l1llll_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧ➣")], stderr=subprocess.DEVNULL).strip().decode(bstack1l1llll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ➤"))
            except OSError as bstack1lll11l1l111_opy_:
                if _1llll111l11l_opy_(bstack1lll11l1l111_opy_):
                    logger.warning(bstack1l1llll_opy_ (u"ࠨࡂࡪࡰࡤࡶࡾࠦࡢࡶࡵࡼࠤࡩࡻࡲࡪࡰࡪࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡶࡲࡧࡥࡹ࡫࠺ࠡࠤ➥") + str(binary_path) + bstack1l1llll_opy_ (u"ࠢࠣ➦"))
                    return binary_path
                raise
        bstack11l11111ll1_opy_ = {
            bstack1l1llll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ➧"): None,
            bstack1l1llll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ➨"): (bs_config[bstack1l1llll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ➩")], bs_config[bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ➪")]),
            bstack1l1llll_opy_ (u"ࠬࡰࡳࡰࡰࠪ➫"): None,
            bstack1l1llll_opy_ (u"࠭ࡰࡢࡴࡤࡱࡸ࠭➬"): bstack1llll11l1l11_opy_,
        }
        cert_path = get_ca_cert_path(bs_config)
        if cert_path:
            bstack11l11111ll1_opy_[bstack1l1llll_opy_ (u"ࠧࡷࡧࡵ࡭࡫ࡿࠧ➭")] = cert_path
        response = requests.request(
            bstack1l1llll_opy_ (u"ࠨࡉࡈࡘࠬ➮"),
            url=bstack11l11111l1_opy_(bstack1111111l11l_opy_),
            **bstack11l11111ll1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l1llll_opy_ (u"ࠩࡸࡶࡱ࠭➯") in data.keys() and bstack1l1llll_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧࡣࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ➰") in data.keys():
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡓ࡫ࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡨࡩ࡯ࡣࡵࡽ࠱ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠧ➱").format(bstack1llll11l1l11_opy_[bstack1l1llll_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪ➲")]))
            if bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩ➳") in os.environ:
                logger.debug(bstack1l1llll_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡥ࡭ࡳࡧࡲࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡦࡹࠠࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠣ࡭ࡸࠦࡳࡦࡶࠥ➴"))
                data[bstack1l1llll_opy_ (u"ࠨࡷࡵࡰࠬ➵")] = os.environ[bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠬ➶")]
            bstack1lll1l111111_opy_ = bstack1llll11l111l_opy_(data[bstack1l1llll_opy_ (u"ࠪࡹࡷࡲࠧ➷")], bstack1l11ll11l_opy_)
            bstack1lllll1111ll_opy_ = os.path.join(bstack1l11ll11l_opy_, bstack1lll1l111111_opy_)
            os.chmod(bstack1lllll1111ll_opy_, 0o777) # bstack1lll1ll1l11l_opy_ permission
            return bstack1lllll1111ll_opy_
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡘࡊࡋࠡࡽࢀࠦ➸").format(e))
    return binary_path
def bstack1llll1l1111l_opy_(bstack1llll11l1l11_opy_):
    try:
        if bstack1l1llll_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫ➹") not in bstack1llll11l1l11_opy_[bstack1l1llll_opy_ (u"࠭࡯ࡴࠩ➺")].lower():
            return
        if os.path.exists(bstack1l1llll_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡵࡳ࠮ࡴࡨࡰࡪࡧࡳࡦࠤ➻")):
            with open(bstack1l1llll_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥ➼"), bstack1l1llll_opy_ (u"ࠤࡵࠦ➽")) as f:
                bstack1lll1llll111_opy_ = {}
                for line in f:
                    if bstack1l1llll_opy_ (u"ࠥࡁࠧ➾") in line:
                        key, value = line.rstrip().split(bstack1l1llll_opy_ (u"ࠦࡂࠨ➿"), 1)
                        bstack1lll1llll111_opy_[key] = value.strip(bstack1l1llll_opy_ (u"ࠬࠨ࡜ࠨࠩ⟀"))
                bstack1llll11l1l11_opy_[bstack1l1llll_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭⟁")] = bstack1lll1llll111_opy_.get(bstack1l1llll_opy_ (u"ࠢࡊࡆࠥ⟂"), bstack1l1llll_opy_ (u"ࠣࠤ⟃"))
        elif os.path.exists(bstack1l1llll_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡢ࡮ࡳ࡭ࡳ࡫࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣ⟄")):
            bstack1llll11l1l11_opy_[bstack1l1llll_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪ⟅")] = bstack1l1llll_opy_ (u"ࠫࡦࡲࡰࡪࡰࡨࠫ⟆")
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡪࡩࡴࡶࡵࡳࠥࡵࡦࠡ࡮࡬ࡲࡺࡾࠢ⟇") + e)
@measure(event_name=EVENTS.bstack1llllll1ll11_opy_, stage=STAGE.SINGLE)
def bstack1llll11l111l_opy_(bstack1lllll11l1ll_opy_, bstack1llll11111l1_opy_):
    logger.debug(bstack1l1llll_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࡀࠠࠣ⟈") + str(bstack1lllll11l1ll_opy_) + bstack1l1llll_opy_ (u"ࠢࠣ⟉"))
    _1lll1ll1lll1_opy_(bstack1llll11111l1_opy_)
    pid = os.getpid()
    zip_name = bstack1l1llll_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࡤ࡬ࡩ࡭ࡧࡢࡿࢂ࠴ࡺࡪࡲࠥ⟊").format(pid)
    zip_path = os.path.join(bstack1llll11111l1_opy_, zip_name)
    bstack1lll1l111111_opy_ = bstack1l1llll_opy_ (u"ࠩࠪ⟋")
    from browserstack_sdk import CONFIG as _1111l1l11l_opy_
    bstack1llll11l1ll1_opy_ = {bstack1l1llll_opy_ (u"ࠪࡷࡹࡸࡥࡢ࡯ࠪ⟌"): True}
    cert_path = get_ca_cert_path(_1111l1l11l_opy_)
    if cert_path:
        bstack1llll11l1ll1_opy_[bstack1l1llll_opy_ (u"ࠫࡻ࡫ࡲࡪࡨࡼࠫ⟍")] = cert_path
    with requests.get(bstack1lllll11l1ll_opy_, **bstack1llll11l1ll1_opy_) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l1llll_opy_ (u"ࠧࡽࡢࠣ⟎")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l1llll_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿ࠮ࠣ⟏"))
    with zipfile.ZipFile(zip_path, bstack1l1llll_opy_ (u"ࠧࡳࠩ⟐")) as zip_ref:
        bstack1llll1ll11ll_opy_ = zip_ref.namelist()
        if len(bstack1llll1ll11ll_opy_) > 0:
            bstack1lll1l111111_opy_ = bstack1llll1ll11ll_opy_[0]
        for name in bstack1llll1ll11ll_opy_:
            final_path = os.path.join(bstack1llll11111l1_opy_, name)
            bstack1lll1l1l1111_opy_ = bstack1l1llll_opy_ (u"ࠣࡽࢀ࠲ࡹࡳࡰ࠯ࡽࢀࠦ⟑").format(name, pid)
            temp_path = os.path.join(bstack1llll11111l1_opy_, bstack1lll1l1l1111_opy_)
            try:
                with zip_ref.open(name) as src, open(temp_path, bstack1l1llll_opy_ (u"ࠩࡺࡦࠬ⟒")) as dst:
                    while True:
                        chunk = src.read(8192)
                        if not chunk:
                            break
                        dst.write(chunk)
                    dst.flush()
                    os.fsync(dst.fileno())
            except OSError:
                _1lll1ll111ll_opy_(temp_path)
                raise
            try:
                os.replace(temp_path, final_path)
            except OSError as bstack1llll1ll1lll_opy_:
                if bstack1llll1ll1lll_opy_.errno != errno.EXDEV:
                    _1lll1ll111ll_opy_(temp_path)
                    raise
                logger.warning(bstack1l1llll_opy_ (u"ࠥࡅࡹࡵ࡭ࡪࡥࠣࡶࡪࡴࡡ࡮ࡧࠣࡥࡨࡸ࡯ࡴࡵࠣࡨࡪࡼࡩࡤࡧࡶ࠰ࠥ࡬ࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠤࡹࡵࠠࡤࡱࡳࡽ࠿ࠦࠢ⟓") + str(bstack1llll1ll1lll_opy_) + bstack1l1llll_opy_ (u"ࠦࠧ⟔"))
                try:
                    shutil.copy2(temp_path, final_path)
                    _1lll1ll111ll_opy_(temp_path)
                except Exception as bstack1llll1l1ll11_opy_:
                    _1lll1ll111ll_opy_(temp_path)
                    raise bstack1llll1l1ll11_opy_
        logger.debug(bstack1l1llll_opy_ (u"ࠧࡌࡩ࡭ࡧࡶࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡩࡽࡺࡲࡢࡥࡷࡩࡩࠦࡴࡰࠢࠪࠦ⟕") + str(bstack1llll11111l1_opy_) + bstack1l1llll_opy_ (u"ࠨࠧࠣ⟖"))
    _1lll1ll111ll_opy_(zip_path)
    return bstack1lll1l111111_opy_
def get_cli_dir():
    bstack1lllll111l11_opy_ = get_writable_dir()
    if bstack1lllll111l11_opy_:
        bstack1l11ll11l_opy_ = os.path.join(bstack1lllll111l11_opy_, bstack1l1llll_opy_ (u"ࠢࡤ࡮࡬ࠦ⟗"))
        if not os.path.exists(bstack1l11ll11l_opy_):
            os.makedirs(bstack1l11ll11l_opy_, mode=0o777, exist_ok=True)
        return bstack1l11ll11l_opy_
    else:
        raise FileNotFoundError(bstack1l1llll_opy_ (u"ࠣࡐࡲࠤࡼࡸࡩࡵࡣࡥࡰࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻ࠱ࠦ⟘"))
def bstack1l11l1111_opy_(bstack1l11ll11l_opy_):
    bstack1l1llll_opy_ (u"ࠤࠥࠦࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡰࠣࡥࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠱ࠦࠧࠨ⟙")
    bstack1lll11l1l1l1_opy_ = [
        os.path.join(bstack1l11ll11l_opy_, f)
        for f in os.listdir(bstack1l11ll11l_opy_)
        if os.path.isfile(os.path.join(bstack1l11ll11l_opy_, f)) and f.startswith(bstack1l1llll_opy_ (u"ࠥࡦ࡮ࡴࡡࡳࡻ࠰ࠦ⟚"))
    ]
    if len(bstack1lll11l1l1l1_opy_) > 0:
        return max(bstack1lll11l1l1l1_opy_, key=os.path.getmtime) # get bstack1lll1llll1ll_opy_ binary
    return bstack1l1llll_opy_ (u"ࠦࠧ⟛")
def bstack1111l11l11l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11ll1l11l11_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack11ll1l11l11_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11l11l111l_opy_(data, keys, default=None):
    bstack1l1llll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡙ࠥࡡࡧࡧ࡯ࡽࠥ࡭ࡥࡵࠢࡤࠤࡳ࡫ࡳࡵࡧࡧࠤࡻࡧ࡬ࡶࡧࠣࡪࡷࡵ࡭ࠡࡣࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡰࡴࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡤࡢࡶࡤ࠾࡚ࠥࡨࡦࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦ࡯ࡳࠢ࡯࡭ࡸࡺࠠࡵࡱࠣࡸࡷࡧࡶࡦࡴࡶࡩ࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣ࡯ࡪࡿࡳ࠻ࠢࡄࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡱࡥࡺࡵ࠲࡭ࡳࡪࡩࡤࡧࡶࠤࡷ࡫ࡰࡳࡧࡶࡩࡳࡺࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡨࡪ࡬ࡡࡶ࡮ࡷ࠾ࠥ࡜ࡡ࡭ࡷࡨࠤࡹࡵࠠࡳࡧࡷࡹࡷࡴࠠࡪࡨࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤ࠿ࡸࡥࡵࡷࡵࡲ࠿ࠦࡔࡩࡧࠣࡺࡦࡲࡵࡦࠢࡤࡸࠥࡺࡨࡦࠢࡱࡩࡸࡺࡥࡥࠢࡳࡥࡹ࡮ࠬࠡࡱࡵࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥ࡯ࡦࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ⟜")
    if not data:
        return default
    current = data
    try:
        for key in keys:
            if isinstance(current, dict):
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int):
                current = current[key]
            else:
                return default
        return current
    except (KeyError, IndexError, TypeError):
        return default
def bstack1llll1l1l11_opy_(bstack1lllll11l1l1_opy_, key, value):
    bstack1l1llll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡓࡵࡱࡵࡩࠥࡉࡌࡊࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠣࡱࡦࡶࡰࡪࡰࡪࠤ࡮ࡴࠠࡵࡪࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥ࡯࡭ࡤ࡫࡮ࡷࡡࡹࡥࡷࡹ࡟࡮ࡣࡳ࠾ࠥࡊࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠤࡲࡧࡰࡱ࡫ࡱ࡫ࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠ࡬ࡧࡼ࠾ࠥࡑࡥࡺࠢࡩࡶࡴࡳࠠࡄࡎࡌࡣࡈࡇࡐࡔࡡࡗࡓࡤࡉࡏࡏࡈࡌࡋࠏࠦࠠࠡࠢࠣࠤࠥࠦࡶࡢ࡮ࡸࡩ࠿ࠦࡖࡢ࡮ࡸࡩࠥ࡬ࡲࡰ࡯ࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡱ࡯࡮ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠏࠦࠠࠡࠢࠥࠦࠧ⟝")
    if key in bstack1l1ll1lllll_opy_:
        bstack111l11l1l1_opy_ = bstack1l1ll1lllll_opy_[key]
        if isinstance(bstack111l11l1l1_opy_, list):
            for env_name in bstack111l11l1l1_opy_:
                bstack1lllll11l1l1_opy_[env_name] = value
        else:
            bstack1lllll11l1l1_opy_[bstack111l11l1l1_opy_] = value