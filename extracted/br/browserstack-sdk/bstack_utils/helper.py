# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import collections
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
from math import ceil
from unittest import result
import urllib
from urllib.parse import urlparse
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11llllllll_opy_, bstack11l111ll11_opy_, bstack1ll1l11l1l_opy_,
                                    bstack11111ll1111_opy_, bstack11111l1llll_opy_, bstack11111ll111l_opy_, bstack111111l1lll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1ll11l1l_opy_, bstack1l11l111_opy_
from bstack_utils.proxy import bstack1l1l1l11l1_opy_, bstack111111lll_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack1lll11l11l_opy_ import bstack1111ll1ll1_opy_
from browserstack_sdk._version import __version__
global_config = Config.bstack1lllllll1_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
automation_logger = logger_utils.get_automation_logger(__name__)
def bstack1111ll11lll_opy_(config):
    return config[bstack1ll1l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬⅭ")]
def bstack1111l1ll1l1_opy_(config):
    return config[bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧⅮ")]
def bstack111l11lll_opy_():
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
def bstack1lllll11l111_opy_(obj):
    values = []
    bstack1llll1l1llll_opy_ = re.compile(bstack1ll1l11_opy_ (u"ࡷࠨ࡞ࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣࡡࡪࠫࠥࠤⅯ"), re.I)
    for key in obj.keys():
        if bstack1llll1l1llll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1lllll1l111l_opy_(config):
    tags = []
    tags.extend(bstack1lllll11l111_opy_(os.environ))
    tags.extend(bstack1lllll11l111_opy_(config))
    return tags
def bstack1llll1l1l11l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1lllllll11l1_opy_(bstack1lllll1l1111_opy_):
    if not bstack1lllll1l1111_opy_:
        return bstack1ll1l11_opy_ (u"࠭ࠧⅰ")
    return bstack1ll1l11_opy_ (u"ࠢࡼࡿࠣࠬࢀࢃࠩࠣⅱ").format(bstack1lllll1l1111_opy_.name, bstack1lllll1l1111_opy_.email)
def bstack1111l1lll11_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1llll1ll11l1_opy_ = repo.common_dir
        info = {
            bstack1ll1l11_opy_ (u"ࠣࡵ࡫ࡥࠧⅲ"): repo.head.commit.hexsha,
            bstack1ll1l11_opy_ (u"ࠤࡶ࡬ࡴࡸࡴࡠࡵ࡫ࡥࠧⅳ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1ll1l11_opy_ (u"ࠥࡦࡷࡧ࡮ࡤࡪࠥⅴ"): repo.active_branch.name,
            bstack1ll1l11_opy_ (u"ࠦࡹࡧࡧࠣⅵ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1ll1l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࠣⅶ"): bstack1lllllll11l1_opy_(repo.head.commit.committer),
            bstack1ll1l11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࡡࡧࡥࡹ࡫ࠢⅷ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1ll1l11_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࠢⅸ"): bstack1lllllll11l1_opy_(repo.head.commit.author),
            bstack1ll1l11_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡠࡦࡤࡸࡪࠨⅹ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1ll1l11_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥⅺ"): repo.head.commit.message,
            bstack1ll1l11_opy_ (u"ࠥࡶࡴࡵࡴࠣⅻ"): repo.git.rev_parse(bstack1ll1l11_opy_ (u"ࠦ࠲࠳ࡳࡩࡱࡺ࠱ࡹࡵࡰ࡭ࡧࡹࡩࡱࠨⅼ")),
            bstack1ll1l11_opy_ (u"ࠧࡩ࡯࡮࡯ࡲࡲࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨⅽ"): bstack1llll1ll11l1_opy_,
            bstack1ll1l11_opy_ (u"ࠨࡷࡰࡴ࡮ࡸࡷ࡫ࡥࡠࡩ࡬ࡸࡤࡪࡩࡳࠤⅾ"): subprocess.check_output([bstack1ll1l11_opy_ (u"ࠢࡨ࡫ࡷࠦⅿ"), bstack1ll1l11_opy_ (u"ࠣࡴࡨࡺ࠲ࡶࡡࡳࡵࡨࠦↀ"), bstack1ll1l11_opy_ (u"ࠤ࠰࠱࡬࡯ࡴ࠮ࡥࡲࡱࡲࡵ࡮࠮ࡦ࡬ࡶࠧↁ")]).strip().decode(
                bstack1ll1l11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩↂ")),
            bstack1ll1l11_opy_ (u"ࠦࡱࡧࡳࡵࡡࡷࡥ࡬ࠨↃ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1ll1l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡸࡥࡳࡪࡰࡦࡩࡤࡲࡡࡴࡶࡢࡸࡦ࡭ࠢↄ"): repo.git.rev_list(
                bstack1ll1l11_opy_ (u"ࠨࡻࡾ࠰࠱ࡿࢂࠨↅ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1llll1111ll1_opy_ = []
        for remote in remotes:
            bstack1llllllll1ll_opy_ = {
                bstack1ll1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧↆ"): remote.name,
                bstack1ll1l11_opy_ (u"ࠣࡷࡵࡰࠧↇ"): remote.url,
            }
            bstack1llll1111ll1_opy_.append(bstack1llllllll1ll_opy_)
        bstack1llll11l1lll_opy_ = {
            bstack1ll1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢↈ"): bstack1ll1l11_opy_ (u"ࠥ࡫࡮ࡺࠢ↉"),
            **info,
            bstack1ll1l11_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡷࠧ↊"): bstack1llll1111ll1_opy_
        }
        bstack1llll11l1lll_opy_ = bstack1llllll1ll11_opy_(bstack1llll11l1lll_opy_)
        return bstack1llll11l1lll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ↋").format(err))
        return {}
def bstack1lllllll1l1l_opy_(bstack1llll1lllll1_opy_=None):
    bstack1ll1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡇࡦࡶࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡶࡴࡪࡩࡩࡧ࡫ࡦࡥࡱࡲࡹࠡࡨࡲࡶࡲࡧࡴࡵࡧࡧࠤ࡫ࡵࡲࠡࡃࡌࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠࡶࡵࡨࠤࡨࡧࡳࡦࡵࠣࡪࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬࡯࡭ࡦࡨࡶࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡨࡲࡰࡩ࡫ࡲࡴࠢࠫࡰ࡮ࡹࡴ࠭ࠢࡲࡴࡹ࡯࡯࡯ࡣ࡯࠭࠿ࠦࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡏࡱࡱࡩ࠿ࠦࡍࡰࡰࡲ࠱ࡷ࡫ࡰࡰࠢࡤࡴࡵࡸ࡯ࡢࡥ࡫࠰ࠥࡻࡳࡦࡵࠣࡧࡺࡸࡲࡦࡰࡷࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡜ࡱࡶ࠲࡬࡫ࡴࡤࡹࡧࠬ࠮ࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡆ࡯ࡳࡸࡾࠦ࡬ࡪࡵࡷࠤࡠࡣ࠺ࠡࡏࡸࡰࡹ࡯࠭ࡳࡧࡳࡳࠥࡧࡰࡱࡴࡲࡥࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥࡴ࡯ࠡࡵࡲࡹࡷࡩࡥࡴࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࡩ࠲ࠠࡳࡧࡷࡹࡷࡴࡳࠡ࡝ࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡶࡡࡵࡪࡶ࠾ࠥࡓࡵ࡭ࡶ࡬࠱ࡷ࡫ࡰࡰࠢࡤࡴࡵࡸ࡯ࡢࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡶࡴࡪࡩࡩࡧ࡫ࡦࠤ࡫ࡵ࡬ࡥࡧࡵࡷࠥࡺ࡯ࠡࡣࡱࡥࡱࡿࡺࡦࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡯࡭ࡸࡺ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡧ࡭ࡨࡺࡳ࠭ࠢࡨࡥࡨ࡮ࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡪࡴࡸࠠࡢࠢࡩࡳࡱࡪࡥࡳ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ↌")
    if bstack1llll1lllll1_opy_ is None:
        bstack1llll1lllll1_opy_ = [os.getcwd()]
    elif isinstance(bstack1llll1lllll1_opy_, list) and len(bstack1llll1lllll1_opy_) == 0:
        return []
    results = []
    for folder in bstack1llll1lllll1_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1ll1l11_opy_ (u"ࠢࡇࡱ࡯ࡨࡪࡸࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠧ↍").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1ll1l11_opy_ (u"ࠣࡲࡵࡍࡩࠨ↎"): bstack1ll1l11_opy_ (u"ࠤࠥ↏"),
                bstack1ll1l11_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤ←"): [],
                bstack1ll1l11_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡷࠧ↑"): [],
                bstack1ll1l11_opy_ (u"ࠧࡶࡲࡅࡣࡷࡩࠧ→"): bstack1ll1l11_opy_ (u"ࠨࠢ↓"),
                bstack1ll1l11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡍࡦࡵࡶࡥ࡬࡫ࡳࠣ↔"): [],
                bstack1ll1l11_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤ↕"): bstack1ll1l11_opy_ (u"ࠤࠥ↖"),
                bstack1ll1l11_opy_ (u"ࠥࡴࡷࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥ↗"): bstack1ll1l11_opy_ (u"ࠦࠧ↘"),
                bstack1ll1l11_opy_ (u"ࠧࡶࡲࡓࡣࡺࡈ࡮࡬ࡦࠣ↙"): bstack1ll1l11_opy_ (u"ࠨࠢ↚")
            }
            bstack1lllll11l11l_opy_ = repo.active_branch.name
            bstack1llllll11l11_opy_ = repo.head.commit
            result[bstack1ll1l11_opy_ (u"ࠢࡱࡴࡌࡨࠧ↛")] = bstack1llllll11l11_opy_.hexsha
            bstack1llll111lll1_opy_ = _1lllll11l1ll_opy_(repo)
            logger.debug(bstack1ll1l11_opy_ (u"ࠣࡄࡤࡷࡪࠦࡢࡳࡣࡱࡧ࡭ࠦࡦࡰࡴࠣࡧࡴࡳࡰࡢࡴ࡬ࡷࡴࡴ࠺ࠡࠤ↜") + str(bstack1llll111lll1_opy_) + bstack1ll1l11_opy_ (u"ࠤࠥ↝"))
            if bstack1llll111lll1_opy_:
                try:
                    bstack1llll11llll1_opy_ = repo.git.diff(bstack1ll1l11_opy_ (u"ࠥ࠱࠲ࡴࡡ࡮ࡧ࠰ࡳࡳࡲࡹࠣ↞"), bstack1l1ll1ll11l_opy_ (u"ࠦࢀࡨࡡࡴࡧࡢࡦࡷࡧ࡮ࡤࡪࢀ࠲࠳࠴ࡻࡤࡷࡵࡶࡪࡴࡴࡠࡤࡵࡥࡳࡩࡨࡾࠤ↟")).split(bstack1ll1l11_opy_ (u"ࠬࡢ࡮ࠨ↠"))
                    logger.debug(bstack1ll1l11_opy_ (u"ࠨࡃࡩࡣࡱ࡫ࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡢࡦࡶࡺࡩࡪࡴࠠࡼࡤࡤࡷࡪࡥࡢࡳࡣࡱࡧ࡭ࢃࠠࡢࡰࡧࠤࢀࡩࡵࡳࡴࡨࡲࡹࡥࡢࡳࡣࡱࡧ࡭ࢃ࠺ࠡࠤ↡") + str(bstack1llll11llll1_opy_) + bstack1ll1l11_opy_ (u"ࠢࠣ↢"))
                    result[bstack1ll1l11_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢ↣")] = [f.strip() for f in bstack1llll11llll1_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1l1ll1ll11l_opy_ (u"ࠤࡾࡦࡦࡹࡥࡠࡤࡵࡥࡳࡩࡨࡾ࠰࠱ࡿࡨࡻࡲࡳࡧࡱࡸࡤࡨࡲࡢࡰࡦ࡬ࢂࠨ↤")))
                except Exception:
                    logger.debug(bstack1ll1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡶࠣࡧ࡭ࡧ࡮ࡨࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡪࡷࡵ࡭ࠡࡤࡵࡥࡳࡩࡨࠡࡥࡲࡱࡵࡧࡲࡪࡵࡲࡲ࠳ࠦࡆࡢ࡮࡯࡭ࡳ࡭ࠠࡣࡣࡦ࡯ࠥࡺ࡯ࠡࡴࡨࡧࡪࡴࡴࠡࡥࡲࡱࡲ࡯ࡴࡴ࠰ࠥ↥"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1ll1l11_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥ↦")] = _1llll1111l1l_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1ll1l11_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦ↧")] = _1llll1111l1l_opy_(commits[:5])
            bstack1llll11l11l1_opy_ = set()
            bstack1llll1l11ll1_opy_ = []
            for commit in commits:
                logger.debug(bstack1ll1l11_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡪࡶ࠽ࠤࠧ↨") + str(commit.message) + bstack1ll1l11_opy_ (u"ࠢࠣ↩"))
                bstack1llll11lllll_opy_ = commit.author.name if commit.author else bstack1ll1l11_opy_ (u"ࠣࡗࡱ࡯ࡳࡵࡷ࡯ࠤ↪")
                bstack1llll11l11l1_opy_.add(bstack1llll11lllll_opy_)
                bstack1llll1l11ll1_opy_.append({
                    bstack1ll1l11_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥ↫"): commit.message.strip(),
                    bstack1ll1l11_opy_ (u"ࠥࡹࡸ࡫ࡲࠣ↬"): bstack1llll11lllll_opy_
                })
            result[bstack1ll1l11_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡷࠧ↭")] = list(bstack1llll11l11l1_opy_)
            result[bstack1ll1l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡒ࡫ࡳࡴࡣࡪࡩࡸࠨ↮")] = bstack1llll1l11ll1_opy_
            result[bstack1ll1l11_opy_ (u"ࠨࡰࡳࡆࡤࡸࡪࠨ↯")] = bstack1llllll11l11_opy_.committed_datetime.strftime(bstack1ll1l11_opy_ (u"࡛ࠢࠦ࠰ࠩࡲ࠳ࠥࡥࠤ↰"))
            if (not result[bstack1ll1l11_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤ↱")] or result[bstack1ll1l11_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥ↲")].strip() == bstack1ll1l11_opy_ (u"ࠥࠦ↳")) and bstack1llllll11l11_opy_.message:
                bstack1llllll111ll_opy_ = bstack1llllll11l11_opy_.message.strip().splitlines()
                result[bstack1ll1l11_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧ↴")] = bstack1llllll111ll_opy_[0] if bstack1llllll111ll_opy_ else bstack1ll1l11_opy_ (u"ࠧࠨ↵")
                if len(bstack1llllll111ll_opy_) > 2:
                    result[bstack1ll1l11_opy_ (u"ࠨࡰࡳࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨ↶")] = bstack1ll1l11_opy_ (u"ࠧ࡝ࡰࠪ↷").join(bstack1llllll111ll_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1ll1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡌ࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡪࡴࡸࠠࡂࡋࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳࠦࠨࡧࡱ࡯ࡨࡪࡸ࠺ࠡࡽࢀ࠭࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢ↸").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    bstack1llll111ll1l_opy_ = [
        result
        for result in results
        if _1lllll1l1l11_opy_(result)
    ]
    return bstack1llll111ll1l_opy_
def _1lllll1l1l11_opy_(result):
    bstack1ll1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡋࡩࡱࡶࡥࡳࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡢࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡷࡺࡲࡴࠡ࡫ࡶࠤࡻࡧ࡬ࡪࡦࠣࠬࡳࡵ࡮࠮ࡧࡰࡴࡹࡿࠠࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠦࡡ࡯ࡦࠣࡥࡺࡺࡨࡰࡴࡶ࠭࠳ࠐࠠࠡࠢࠣࠦࠧࠨ↹")
    return (
        isinstance(result.get(bstack1ll1l11_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤ↺"), None), list)
        and len(result[bstack1ll1l11_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥ↻")]) > 0
        and isinstance(result.get(bstack1ll1l11_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨ↼"), None), list)
        and len(result[bstack1ll1l11_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢ↽")]) > 0
    )
def _1lllll11l1ll_opy_(repo):
    bstack1ll1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡕࡴࡼࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡸ࡭࡫ࠠࡣࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡸࡥࡱࡱࠣࡻ࡮ࡺࡨࡰࡷࡷࠤ࡭ࡧࡲࡥࡥࡲࡨࡪࡪࠠ࡯ࡣࡰࡩࡸࠦࡡ࡯ࡦࠣࡻࡴࡸ࡫ࠡࡹ࡬ࡸ࡭ࠦࡡ࡭࡮࡚ࠣࡈ࡙ࠠࡱࡴࡲࡺ࡮ࡪࡥࡳࡵ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡷ࡬ࡪࠦࡤࡦࡨࡤࡹࡱࡺࠠࡣࡴࡤࡲࡨ࡮ࠠࡪࡨࠣࡴࡴࡹࡳࡪࡤ࡯ࡩ࠱ࠦࡥ࡭ࡵࡨࠤࡓࡵ࡮ࡦ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ↾")
    try:
        try:
            origin = repo.remotes.origin
            bstack1lllllll1l11_opy_ = origin.refs[bstack1ll1l11_opy_ (u"ࠨࡊࡈࡅࡉ࠭↿")]
            target = bstack1lllllll1l11_opy_.reference.name
            if target.startswith(bstack1ll1l11_opy_ (u"ࠩࡲࡶ࡮࡭ࡩ࡯࠱ࠪ⇀")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1ll1l11_opy_ (u"ࠪࡳࡷ࡯ࡧࡪࡰ࠲ࠫ⇁")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _1llll1111l1l_opy_(commits):
    bstack1ll1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡌ࡫ࡴࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡦ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡩࡶࡴࡳࠠࡢࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࡶ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ⇂")
    bstack1llll11llll1_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack1llll1l11lll_opy_ in diff:
                        if bstack1llll1l11lll_opy_.a_path:
                            bstack1llll11llll1_opy_.add(bstack1llll1l11lll_opy_.a_path)
                        if bstack1llll1l11lll_opy_.b_path:
                            bstack1llll11llll1_opy_.add(bstack1llll1l11lll_opy_.b_path)
    except Exception:
        pass
    return list(bstack1llll11llll1_opy_)
def bstack1llllll1ll11_opy_(bstack1llll11l1lll_opy_):
    bstack1llllll1l111_opy_ = bstack1llll1l1ll1l_opy_(bstack1llll11l1lll_opy_)
    if bstack1llllll1l111_opy_ and bstack1llllll1l111_opy_ > bstack11111ll1111_opy_:
        bstack1lllllll1ll1_opy_ = bstack1llllll1l111_opy_ - bstack11111ll1111_opy_
        bstack1lllll11111l_opy_ = bstack1llll11l1l1l_opy_(bstack1llll11l1lll_opy_[bstack1ll1l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨ⇃")], bstack1lllllll1ll1_opy_)
        bstack1llll11l1lll_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢ⇄")] = bstack1lllll11111l_opy_
        logger.info(bstack1ll1l11_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤ⇅")
                    .format(bstack1llll1l1ll1l_opy_(bstack1llll11l1lll_opy_) / 1024))
    return bstack1llll11l1lll_opy_
def bstack1llll1l1ll1l_opy_(json_data):
    try:
        if json_data:
            bstack1llll1l11111_opy_ = json.dumps(json_data)
            bstack1llll11l11ll_opy_ = sys.getsizeof(bstack1llll1l11111_opy_)
            return bstack1llll11l11ll_opy_
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣ⇆").format(e))
    return -1
def bstack1llll11l1l1l_opy_(field, bstack1llllll11111_opy_):
    try:
        bstack1llll111l1ll_opy_ = len(bytes(bstack11111l1llll_opy_, bstack1ll1l11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ⇇")))
        bstack1lllll1lllll_opy_ = bytes(field, bstack1ll1l11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ⇈"))
        bstack1lllll1111l1_opy_ = len(bstack1lllll1lllll_opy_)
        bstack1llllll11ll1_opy_ = ceil(bstack1lllll1111l1_opy_ - bstack1llllll11111_opy_ - bstack1llll111l1ll_opy_)
        if bstack1llllll11ll1_opy_ > 0:
            bstack1llllll1lll1_opy_ = bstack1lllll1lllll_opy_[:bstack1llllll11ll1_opy_].decode(bstack1ll1l11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ⇉"), errors=bstack1ll1l11_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬ⇊")) + bstack11111l1llll_opy_
            return bstack1llllll1lll1_opy_
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦ⇋").format(e))
    return field
def bstack1111l1111l_opy_():
    env = os.environ
    if (bstack1ll1l11_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ⇌") in env and len(env[bstack1ll1l11_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨ⇍")]) > 0) or (
            bstack1ll1l11_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ⇎") in env and len(env[bstack1ll1l11_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ⇏")]) > 0):
        return {
            bstack1ll1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⇐"): bstack1ll1l11_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨ⇑"),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⇒"): env.get(bstack1ll1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ⇓")),
            bstack1ll1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⇔"): env.get(bstack1ll1l11_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦ⇕")),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⇖"): env.get(bstack1ll1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ⇗"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠧࡉࡉࠣ⇘")) == bstack1ll1l11_opy_ (u"ࠨࡴࡳࡷࡨࠦ⇙") and bstack1l111l11l1_opy_(env.get(bstack1ll1l11_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤ⇚"))):
        return {
            bstack1ll1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨ⇛"): bstack1ll1l11_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦ⇜"),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⇝"): env.get(bstack1ll1l11_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ⇞")),
            bstack1ll1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⇟"): env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥ⇠")),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⇡"): env.get(bstack1ll1l11_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦ⇢"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠤࡆࡍࠧ⇣")) == bstack1ll1l11_opy_ (u"ࠥࡸࡷࡻࡥࠣ⇤") and bstack1l111l11l1_opy_(env.get(bstack1ll1l11_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦ⇥"))):
        return {
            bstack1ll1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⇦"): bstack1ll1l11_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤ⇧"),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⇨"): env.get(bstack1ll1l11_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣ⇩")),
            bstack1ll1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⇪"): env.get(bstack1ll1l11_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ⇫")),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⇬"): env.get(bstack1ll1l11_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ⇭"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡊࠤ⇮")) == bstack1ll1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧ⇯") and env.get(bstack1ll1l11_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤ⇰")) == bstack1ll1l11_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦ⇱"):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣ⇲"): bstack1ll1l11_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨ⇳"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ⇴"): None,
            bstack1ll1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⇵"): None,
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⇶"): None
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦ⇷")) and env.get(bstack1ll1l11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧ⇸")):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣ⇹"): bstack1ll1l11_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢ⇺"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ⇻"): env.get(bstack1ll1l11_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦ⇼")),
            bstack1ll1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ⇽"): None,
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⇾"): env.get(bstack1ll1l11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ⇿"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡎࠨ∀")) == bstack1ll1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤ∁") and bstack1l111l11l1_opy_(env.get(bstack1ll1l11_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦ∂"))):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ∃"): bstack1ll1l11_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨ∄"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ∅"): env.get(bstack1ll1l11_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧ∆")),
            bstack1ll1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ∇"): None,
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ∈"): env.get(bstack1ll1l11_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ∉"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡊࠤ∊")) == bstack1ll1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧ∋") and bstack1l111l11l1_opy_(env.get(bstack1ll1l11_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦ∌"))):
        return {
            bstack1ll1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ∍"): bstack1ll1l11_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨ∎"),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ∏"): env.get(bstack1ll1l11_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦ∐")),
            bstack1ll1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ∑"): env.get(bstack1ll1l11_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ−")),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ∓"): env.get(bstack1ll1l11_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧ∔"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡎࠨ∕")) == bstack1ll1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤ∖") and bstack1l111l11l1_opy_(env.get(bstack1ll1l11_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣ∗"))):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ∘"): bstack1ll1l11_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢ∙"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ√"): env.get(bstack1ll1l11_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨ∛")),
            bstack1ll1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ∜"): env.get(bstack1ll1l11_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ∝")),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ∞"): env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤ∟"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠢࡄࡋࠥ∠")) == bstack1ll1l11_opy_ (u"ࠣࡶࡵࡹࡪࠨ∡") and bstack1l111l11l1_opy_(env.get(bstack1ll1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧ∢"))):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣ∣"): bstack1ll1l11_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢ∤"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ∥"): env.get(bstack1ll1l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ∦")),
            bstack1ll1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ∧"): env.get(bstack1ll1l11_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥ∨")) or env.get(bstack1ll1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧ∩")),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ∪"): env.get(bstack1ll1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ∫"))
        }
    if bstack1l111l11l1_opy_(env.get(bstack1ll1l11_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢ∬"))):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ∭"): bstack1ll1l11_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢ∮"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ∯"): bstack1ll1l11_opy_ (u"ࠤࡾࢁࢀࢃࠢ∰").format(env.get(bstack1ll1l11_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭∱")), env.get(bstack1ll1l11_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫ∲"))),
            bstack1ll1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ∳"): env.get(bstack1ll1l11_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧ∴")),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ∵"): env.get(bstack1ll1l11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣ∶"))
        }
    if bstack1l111l11l1_opy_(env.get(bstack1ll1l11_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦ∷"))):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣ∸"): bstack1ll1l11_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨ∹"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ∺"): bstack1ll1l11_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧ∻").format(env.get(bstack1ll1l11_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭∼")), env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩ∽")), env.get(bstack1ll1l11_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪ∾")), env.get(bstack1ll1l11_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧ∿"))),
            bstack1ll1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ≀"): env.get(bstack1ll1l11_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ≁")),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ≂"): env.get(bstack1ll1l11_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ≃"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤ≄")) and env.get(bstack1ll1l11_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦ≅")):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣ≆"): bstack1ll1l11_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨ≇"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ≈"): bstack1ll1l11_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤ≉").format(env.get(bstack1ll1l11_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪ≊")), env.get(bstack1ll1l11_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭≋")), env.get(bstack1ll1l11_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩ≌"))),
            bstack1ll1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ≍"): env.get(bstack1ll1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦ≎")),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ≏"): env.get(bstack1ll1l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨ≐"))
        }
    if any([env.get(bstack1ll1l11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ≑")), env.get(bstack1ll1l11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢ≒")), env.get(bstack1ll1l11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ≓"))]):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣ≔"): bstack1ll1l11_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦ≕"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ≖"): env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ≗")),
            bstack1ll1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ≘"): env.get(bstack1ll1l11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ≙")),
            bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ≚"): env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ≛"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤ≜")):
        return {
            bstack1ll1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ≝"): bstack1ll1l11_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨ≞"),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ≟"): env.get(bstack1ll1l11_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥ≠")),
            bstack1ll1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ≡"): env.get(bstack1ll1l11_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤ≢")),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ≣"): env.get(bstack1ll1l11_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥ≤"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢ≥")) or env.get(bstack1ll1l11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤ≦")):
        return {
            bstack1ll1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨ≧"): bstack1ll1l11_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥ≨"),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ≩"): env.get(bstack1ll1l11_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ≪")),
            bstack1ll1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ≫"): bstack1ll1l11_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨ≬") if env.get(bstack1ll1l11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤ≭")) else None,
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ≮"): env.get(bstack1ll1l11_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢ≯"))
        }
    if any([env.get(bstack1ll1l11_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣ≰")), env.get(bstack1ll1l11_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧ≱")), env.get(bstack1ll1l11_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧ≲"))]):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ≳"): bstack1ll1l11_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨ≴"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ≵"): None,
            bstack1ll1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ≶"): env.get(bstack1ll1l11_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢ≷")),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ≸"): env.get(bstack1ll1l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ≹"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤ≺")):
        return {
            bstack1ll1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ≻"): bstack1ll1l11_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦ≼"),
            bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ≽"): env.get(bstack1ll1l11_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ≾")),
            bstack1ll1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ≿"): bstack1ll1l11_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨ⊀").format(env.get(bstack1ll1l11_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩ⊁"))) if env.get(bstack1ll1l11_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥ⊂")) else None,
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⊃"): env.get(bstack1ll1l11_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ⊄"))
        }
    if bstack1l111l11l1_opy_(env.get(bstack1ll1l11_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦ⊅"))):
        return {
            bstack1ll1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⊆"): bstack1ll1l11_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨ⊇"),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⊈"): env.get(bstack1ll1l11_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦ⊉")),
            bstack1ll1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⊊"): env.get(bstack1ll1l11_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧ⊋")),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⊌"): env.get(bstack1ll1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ⊍"))
        }
    if bstack1l111l11l1_opy_(env.get(bstack1ll1l11_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨ⊎"))):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⊏"): bstack1ll1l11_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣ⊐"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⊑"): bstack1ll1l11_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥ⊒").format(env.get(bstack1ll1l11_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧ⊓")), env.get(bstack1ll1l11_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨ⊔")), env.get(bstack1ll1l11_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬ⊕"))),
            bstack1ll1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⊖"): env.get(bstack1ll1l11_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤ⊗")),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⊘"): env.get(bstack1ll1l11_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤ⊙"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡎࠨ⊚")) == bstack1ll1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤ⊛") and env.get(bstack1ll1l11_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧ⊜")) == bstack1ll1l11_opy_ (u"ࠨ࠱ࠣ⊝"):
        return {
            bstack1ll1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⊞"): bstack1ll1l11_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣ⊟"),
            bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⊠"): bstack1ll1l11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨ⊡").format(env.get(bstack1ll1l11_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨ⊢"))),
            bstack1ll1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⊣"): None,
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ⊤"): None,
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥ⊥")):
        return {
            bstack1ll1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨ⊦"): bstack1ll1l11_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦ⊧"),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⊨"): None,
            bstack1ll1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ⊩"): env.get(bstack1ll1l11_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨ⊪")),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ⊫"): env.get(bstack1ll1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ⊬"))
        }
    if any([env.get(bstack1ll1l11_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦ⊭")), env.get(bstack1ll1l11_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤ⊮")), env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣ⊯")), env.get(bstack1ll1l11_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧ⊰"))]):
        return {
            bstack1ll1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⊱"): bstack1ll1l11_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤ⊲"),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⊳"): None,
            bstack1ll1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⊴"): env.get(bstack1ll1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ⊵")) or None,
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⊶"): env.get(bstack1ll1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ⊷"), 0)
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ⊸")):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⊹"): bstack1ll1l11_opy_ (u"ࠢࡈࡱࡆࡈࠧ⊺"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⊻"): None,
            bstack1ll1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⊼"): env.get(bstack1ll1l11_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ⊽")),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⊾"): env.get(bstack1ll1l11_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦ⊿"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ⋀")):
        return {
            bstack1ll1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⋁"): bstack1ll1l11_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦ⋂"),
            bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⋃"): env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ⋄")),
            bstack1ll1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ⋅"): env.get(bstack1ll1l11_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣ⋆")),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ⋇"): env.get(bstack1ll1l11_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ⋈"))
        }
    return {bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⋉"): None}
def get_host_info():
    return {
        bstack1ll1l11_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦ⋊"): platform.node(),
        bstack1ll1l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧ⋋"): platform.system(),
        bstack1ll1l11_opy_ (u"ࠦࡹࡿࡰࡦࠤ⋌"): platform.machine(),
        bstack1ll1l11_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨ⋍"): platform.version(),
        bstack1ll1l11_opy_ (u"ࠨࡡࡳࡥ࡫ࠦ⋎"): platform.architecture()[0]
    }
def bstack11l111l111_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1llll1ll1111_opy_():
    if global_config.get_property(bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ⋏")):
        return bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ⋐")
    return bstack1ll1l11_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨ⋑")
def bstack1lll11111ll_opy_(driver):
    info = {
        bstack1ll1l11_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ⋒"): driver.capabilities,
        bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨ⋓"): driver.session_id,
        bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭⋔"): driver.capabilities.get(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ⋕"), None),
        bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⋖"): driver.capabilities.get(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ⋗"), None),
        bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫ⋘"): driver.capabilities.get(bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩ⋙"), None),
        bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⋚"):driver.capabilities.get(bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ⋛"), None),
    }
    if bstack1llll1ll1111_opy_() == bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ⋜"):
        if bstack111l1lll1_opy_():
            info[bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ⋝")] = bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⋞")
        elif driver.capabilities.get(bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ⋟"), {}).get(bstack1ll1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ⋠"), False):
            info[bstack1ll1l11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬ⋡")] = bstack1ll1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ⋢")
        else:
            info[bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ⋣")] = bstack1ll1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ⋤")
    return info
def bstack111l1lll1_opy_():
    if global_config.get_property(bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⋥")):
        return True
    if bstack1l111l11l1_opy_(os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ⋦"), None)):
        return True
    return False
def bstack1lllll111l11_opy_(bstack1llll11ll1ll_opy_, url, response, headers=None, data=None):
    bstack1ll1l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡆࡺ࡯࡬ࡥࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦ࡬ࡰࡩࠣࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠠࡧࡱࡵࠤࡷ࡫ࡱࡶࡧࡶࡸ࠴ࡸࡥࡴࡲࡲࡲࡸ࡫ࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡲࡷࡨࡷࡹࡥࡴࡺࡲࡨ࠾ࠥࡎࡔࡕࡒࠣࡱࡪࡺࡨࡰࡦࠣࠬࡌࡋࡔ࠭ࠢࡓࡓࡘ࡚ࠬࠡࡧࡷࡧ࠳࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡷࡵࡰ࠿ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡖࡔࡏ࠳ࡪࡴࡤࡱࡱ࡬ࡲࡹࠐࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡵࡢ࡫ࡧࡦࡸࠥ࡬ࡲࡰ࡯ࠣࡶࡪࡷࡵࡦࡵࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࡨࡦࡣࡧࡩࡷࡹ࠺ࠡࡔࡨࡵࡺ࡫ࡳࡵࠢ࡫ࡩࡦࡪࡥࡳࡵࠣࡳࡷࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡡࡵࡣ࠽ࠤࡗ࡫ࡱࡶࡧࡶࡸࠥࡐࡓࡐࡐࠣࡨࡦࡺࡡࠡࡱࡵࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡈࡲࡶࡲࡧࡴࡵࡧࡧࠤࡱࡵࡧࠡ࡯ࡨࡷࡸࡧࡧࡦࠢࡺ࡭ࡹ࡮ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡣࡱࡨࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡥࡣࡷࡥࠏࠦࠠࠡࠢࠥࠦࠧ⋧")
    bstack1llll1lll111_opy_ = {
        bstack1ll1l11_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧ⋨"): headers,
        bstack1ll1l11_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧ⋩"): bstack1llll11ll1ll_opy_.upper(),
        bstack1ll1l11_opy_ (u"ࠨࡡࡨࡧࡱࡸࠧ⋪"): None,
        bstack1ll1l11_opy_ (u"ࠢࡦࡰࡧࡴࡴ࡯࡮ࡵࠤ⋫"): url,
        bstack1ll1l11_opy_ (u"ࠣ࡬ࡶࡳࡳࠨ⋬"): data
    }
    try:
        bstack1lllll111ll1_opy_ = response.json()
        if isinstance(bstack1lllll111ll1_opy_, dict) and bstack1lllll111ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⋭"), {}).get(bstack1ll1l11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ⋮"), {}).get(bstack1ll1l11_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬ⋯")):
            bstack1llll1lll1ll_opy_ = json.loads(json.dumps(bstack1lllll111ll1_opy_))
            bstack1llll1lll1ll_opy_[bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⋰")][bstack1ll1l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ⋱")][bstack1ll1l11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ⋲")] = bstack1ll1l11_opy_ (u"ࠣ࡝ࡵࡩࡩࡧࡣࡵࡧࡧࠤ࡫ࡵࡲࠡࡤࡵࡩࡻ࡯ࡴࡺ࡟ࠥ⋳")
            bstack1lllll111ll1_opy_ = bstack1llll1lll1ll_opy_
    except Exception:
        bstack1lllll111ll1_opy_ = response.text
    bstack1lllll1l1ll1_opy_ = {
        bstack1ll1l11_opy_ (u"ࠤࡥࡳࡩࡿࠢ⋴"): bstack1lllll111ll1_opy_,
        bstack1ll1l11_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࡆࡳࡩ࡫ࠢ⋵"): response.status_code
    }
    return {
        bstack1ll1l11_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧ⋶"): bstack1llll1lll111_opy_,
        bstack1ll1l11_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢ⋷"): bstack1lllll1l1ll1_opy_
    }
def bstack11llll11ll_opy_(bstack1llll11ll1ll_opy_, url, data, config):
    headers = config.get(bstack1ll1l11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ⋸"), None)
    proxies = bstack1l1l1l11l1_opy_(config, url)
    auth = config.get(bstack1ll1l11_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ⋹"), None)
    response = requests.request(
            bstack1llll11ll1ll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1lllll111l11_opy_(bstack1llll11ll1ll_opy_, url, response, headers, data)
        automation_logger.debug(json.dumps(log_message, separators=(bstack1ll1l11_opy_ (u"ࠨ࠮ࠪ⋺"), bstack1ll1l11_opy_ (u"ࠩ࠽ࠫ⋻"))))
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺ࠺ࠡࡽࢀࠦ⋼").format(e))
    return response
def bstack11lll1ll11_opy_(bstack1l1l111ll_opy_, size):
    bstack11lll11lll_opy_ = []
    while len(bstack1l1l111ll_opy_) > size:
        bstack1l11l11l_opy_ = bstack1l1l111ll_opy_[:size]
        bstack11lll11lll_opy_.append(bstack1l11l11l_opy_)
        bstack1l1l111ll_opy_ = bstack1l1l111ll_opy_[size:]
    bstack11lll11lll_opy_.append(bstack1l1l111ll_opy_)
    return bstack11lll11lll_opy_
def bstack1llll1l11l1l_opy_(message, bstack1lllll1l11l1_opy_=False):
    os.write(1, bytes(message, bstack1ll1l11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ⋽")))
    os.write(1, bytes(bstack1ll1l11_opy_ (u"ࠬࡢ࡮ࠨ⋾"), bstack1ll1l11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ⋿")))
    if bstack1lllll1l11l1_opy_:
        with open(bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭ࡰ࠳࠴ࡽ࠲࠭⌀") + os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ⌁")] + bstack1ll1l11_opy_ (u"ࠩ࠱ࡰࡴ࡭ࠧ⌂"), bstack1ll1l11_opy_ (u"ࠪࡥࠬ⌃")) as f:
            f.write(message + bstack1ll1l11_opy_ (u"ࠫࡡࡴࠧ⌄"))
def bstack1l1lllllll_opy_():
    return os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ⌅")].lower() == bstack1ll1l11_opy_ (u"࠭ࡴࡳࡷࡨࠫ⌆")
def bstack111ll1ll1l_opy_():
    return bstack1lll1l11ll1_opy_().replace(tzinfo=None).isoformat() + bstack1ll1l11_opy_ (u"࡛ࠧࠩ⌇")
def bstack1ll1l1ll111_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1ll1l11_opy_ (u"ࠨ࡜ࠪ⌈"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1ll1l11_opy_ (u"ࠩ࡝ࠫ⌉")))).total_seconds() * 1000
def bstack1lllll11lll1_opy_(timestamp):
    return bstack1llll11ll111_opy_(timestamp).isoformat() + bstack1ll1l11_opy_ (u"ࠪ࡞ࠬ⌊")
def bstack1llllllll11l_opy_(bstack1llllll1llll_opy_):
    date_format = bstack1ll1l11_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩ⌋")
    bstack1lllll11l1l1_opy_ = datetime.datetime.strptime(bstack1llllll1llll_opy_, date_format)
    return bstack1lllll11l1l1_opy_.isoformat() + bstack1ll1l11_opy_ (u"ࠬࡠࠧ⌌")
def bstack1lllllll111l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⌍")
    else:
        return bstack1ll1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⌎")
def bstack1l111l11l1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1ll1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭⌏")
def bstack1llll1llll11_opy_(val):
    return val.__str__().lower() == bstack1ll1l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ⌐")
def error_handler(bstack1lllll11llll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1lllll11llll_opy_ as e:
                print(bstack1ll1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥ⌑").format(func.__name__, bstack1lllll11llll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1llllll1l1l1_opy_(bstack1llll11lll1l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1llll11lll1l_opy_(cls, *args, **kwargs)
            except bstack1lllll11llll_opy_ as e:
                print(bstack1ll1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦ⌒").format(bstack1llll11lll1l_opy_.__name__, bstack1lllll11llll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1llllll1l1l1_opy_
    else:
        return decorator
def bstack111l1lll1l_opy_(bstack1lllll111l1_opy_):
    if os.getenv(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ⌓")) is not None:
        return bstack1l111l11l1_opy_(os.getenv(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ⌔")))
    if bstack1ll1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⌕") in bstack1lllll111l1_opy_ and bstack1llll1llll11_opy_(bstack1lllll111l1_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⌖")]):
        return False
    if bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⌗") in bstack1lllll111l1_opy_ and bstack1llll1llll11_opy_(bstack1lllll111l1_opy_[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⌘")]):
        return False
    return True
def bstack1ll1111ll1_opy_():
    try:
        from pytest_bdd import reporting
        bstack1llllll11l1l_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦ⌙"), None)
        return bstack1llllll11l1l_opy_ is None or bstack1llllll11l1l_opy_ == bstack1ll1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ⌚")
    except Exception as e:
        return False
def bstack1lll1lll11_opy_(hub_url, CONFIG):
    if bstack11lll1ll_opy_() <= version.parse(bstack1ll1l11_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭⌛")):
        if hub_url:
            return bstack1ll1l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ⌜") + hub_url + bstack1ll1l11_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ⌝")
        return bstack11l111ll11_opy_
    if hub_url:
        return bstack1ll1l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ⌞") + hub_url + bstack1ll1l11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ⌟")
    return bstack1ll1l11l1l_opy_
def bstack1llllll111l1_opy_():
    return isinstance(os.getenv(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪ⌠")), str)
def bstack11l1l1111_opy_(url):
    return urlparse(url).hostname
def bstack1l1l11111l_opy_(hostname):
    for bstack1l1111lll_opy_ in bstack11llllllll_opy_:
        regex = re.compile(bstack1l1111lll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1llll1111lll_opy_(bstack1llll1l1l1ll_opy_, file_name, logger):
    bstack1l1ll1l1ll_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠬࢄࠧ⌡")), bstack1llll1l1l1ll_opy_)
    try:
        if not os.path.exists(bstack1l1ll1l1ll_opy_):
            os.makedirs(bstack1l1ll1l1ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"࠭ࡾࠨ⌢")), bstack1llll1l1l1ll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1ll1l11_opy_ (u"ࠧࡸࠩ⌣")):
                pass
            with open(file_path, bstack1ll1l11_opy_ (u"ࠣࡹ࠮ࠦ⌤")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1ll11l1l_opy_.format(str(e)))
def bstack1llll1ll1l11_opy_(file_name, key, value, logger):
    file_path = bstack1llll1111lll_opy_(bstack1ll1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ⌥"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1l11111_opy_ = json.load(open(file_path, bstack1ll1l11_opy_ (u"ࠪࡶࡧ࠭⌦")))
        else:
            bstack1ll1l11111_opy_ = {}
        bstack1ll1l11111_opy_[key] = value
        with open(file_path, bstack1ll1l11_opy_ (u"ࠦࡼ࠱ࠢ⌧")) as outfile:
            json.dump(bstack1ll1l11111_opy_, outfile)
def bstack1l1l111lll_opy_(file_name, logger):
    file_path = bstack1llll1111lll_opy_(bstack1ll1l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ⌨"), file_name, logger)
    bstack1ll1l11111_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1ll1l11_opy_ (u"࠭ࡲࠨ〈")) as bstack1l1ll11l1_opy_:
            bstack1ll1l11111_opy_ = json.load(bstack1l1ll11l1_opy_)
    return bstack1ll1l11111_opy_
def bstack11ll1111_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫ〉") + file_path + bstack1ll1l11_opy_ (u"ࠨࠢࠪ⌫") + str(e))
def bstack11lll1ll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1ll1l11_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦ⌬")
def bstack111l11l1_opy_(config):
    if bstack1ll1l11_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ⌭") in config:
        del (config[bstack1ll1l11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ⌮")])
        return False
    if bstack11lll1ll_opy_() < version.parse(bstack1ll1l11_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫ⌯")):
        return False
    if bstack11lll1ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬ⌰")):
        return True
    if bstack1ll1l11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ⌱") in config and config[bstack1ll1l11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ⌲")] is False:
        return False
    else:
        return True
def bstack1ll1111l11_opy_(args_list, bstack1llllll1l11l_opy_):
    index = -1
    for value in bstack1llllll1l11l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack1111ll1l1ll_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack1111ll1l1ll_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1llll1l11l1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1llll1l11l1_opy_ = bstack1llll1l11l1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1ll1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⌳"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⌴"), exception=exception)
    def bstack1ll111l1lll_opy_(self):
        if self.result != bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⌵"):
            return None
        if isinstance(self.exception_type, str) and bstack1ll1l11_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ⌶") in self.exception_type:
            return bstack1ll1l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ⌷")
        return bstack1ll1l11_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ⌸")
    def bstack1lllll1lll1l_opy_(self):
        if self.result != bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⌹"):
            return None
        if self.bstack1llll1l11l1_opy_:
            return self.bstack1llll1l11l1_opy_
        return bstack1lllll1lll11_opy_(self.exception)
def bstack1lllll1lll11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1llllll1l1ll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11l11l1ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l11lllll_opy_(config, logger):
    try:
        import playwright
        bstack1llll1l1l1l1_opy_ = playwright.__file__
        bstack1llll1ll111l_opy_ = os.path.split(bstack1llll1l1l1l1_opy_)
        bstack1lllll1ll11l_opy_ = bstack1llll1ll111l_opy_[0] + bstack1ll1l11_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷࠬ⌺")
        os.environ[bstack1ll1l11_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭⌻")] = bstack111111lll_opy_(config)
        with open(bstack1lllll1ll11l_opy_, bstack1ll1l11_opy_ (u"ࠫࡷ࠭⌼")) as f:
            file_content = f.read()
            bstack1llll1llll1l_opy_ = bstack1ll1l11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ⌽")
            bstack1llll1lll11l_opy_ = file_content.find(bstack1llll1llll1l_opy_)
            if bstack1llll1lll11l_opy_ == -1:
              process = subprocess.Popen(bstack1ll1l11_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥ⌾"), shell=True, cwd=bstack1llll1ll111l_opy_[0])
              process.wait()
              bstack1llll1l111ll_opy_ = bstack1ll1l11_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧ⌿")
              bstack1llll111llll_opy_ = bstack1ll1l11_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧ⍀")
              bstack1lllll11ll11_opy_ = file_content.replace(bstack1llll1l111ll_opy_, bstack1llll111llll_opy_)
              with open(bstack1lllll1ll11l_opy_, bstack1ll1l11_opy_ (u"ࠩࡺࠫ⍁")) as f:
                f.write(bstack1lllll11ll11_opy_)
    except Exception as e:
        logger.error(bstack1l11l111_opy_.format(str(e)))
def bstack1lll1lll1_opy_():
  try:
    bstack1lllll111l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪ⍂"))
    bstack1llll1lll1l1_opy_ = []
    if os.path.exists(bstack1lllll111l1l_opy_):
      with open(bstack1lllll111l1l_opy_) as f:
        bstack1llll1lll1l1_opy_ = json.load(f)
      os.remove(bstack1lllll111l1l_opy_)
    return bstack1llll1lll1l1_opy_
  except:
    pass
  return []
def bstack1ll1l11ll_opy_(bstack11l1l1ll1_opy_):
  try:
    bstack1llll1lll1l1_opy_ = []
    bstack1lllll111l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫ⍃"))
    if os.path.exists(bstack1lllll111l1l_opy_):
      with open(bstack1lllll111l1l_opy_) as f:
        bstack1llll1lll1l1_opy_ = json.load(f)
    bstack1llll1lll1l1_opy_.append(bstack11l1l1ll1_opy_)
    with open(bstack1lllll111l1l_opy_, bstack1ll1l11_opy_ (u"ࠬࡽࠧ⍄")) as f:
        json.dump(bstack1llll1lll1l1_opy_, f)
  except:
    pass
def bstack1lllllll11l_opy_(logger, bstack1llll11lll11_opy_ = False):
  try:
    test_name = os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⍅"), bstack1ll1l11_opy_ (u"ࠧࠨ⍆"))
    if test_name == bstack1ll1l11_opy_ (u"ࠨࠩ⍇"):
        test_name = threading.current_thread().__dict__.get(bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨ⍈"), bstack1ll1l11_opy_ (u"ࠪࠫ⍉"))
    bstack1lllll1ll1ll_opy_ = bstack1ll1l11_opy_ (u"ࠫ࠱ࠦࠧ⍊").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1llll11lll11_opy_:
        bstack11ll1l111_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⍋"), bstack1ll1l11_opy_ (u"࠭࠰ࠨ⍌"))
        bstack1l11111lll_opy_ = {bstack1ll1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⍍"): test_name, bstack1ll1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ⍎"): bstack1lllll1ll1ll_opy_, bstack1ll1l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ⍏"): bstack11ll1l111_opy_}
        bstack1llll1l1l111_opy_ = []
        bstack1lllll111111_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ⍐"))
        if os.path.exists(bstack1lllll111111_opy_):
            with open(bstack1lllll111111_opy_) as f:
                bstack1llll1l1l111_opy_ = json.load(f)
        bstack1llll1l1l111_opy_.append(bstack1l11111lll_opy_)
        with open(bstack1lllll111111_opy_, bstack1ll1l11_opy_ (u"ࠫࡼ࠭⍑")) as f:
            json.dump(bstack1llll1l1l111_opy_, f)
    else:
        bstack1l11111lll_opy_ = {bstack1ll1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⍒"): test_name, bstack1ll1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⍓"): bstack1lllll1ll1ll_opy_, bstack1ll1l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⍔"): str(multiprocessing.current_process().name)}
        if bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬ⍕") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l11111lll_opy_)
  except Exception as e:
      logger.warn(bstack1ll1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ⍖").format(e))
def bstack11ll1111l_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥࡨࡡࡴ࡫ࡦࠤ࡫࡯࡬ࡦࠢࡲࡴࡪࡸࡡࡵ࡫ࡲࡲࡸ࠭⍗"))
    try:
      bstack1lllll1l1l1l_opy_ = []
      bstack1l11111lll_opy_ = {bstack1ll1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⍘"): test_name, bstack1ll1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⍙"): error_message, bstack1ll1l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⍚"): index}
      bstack1llll1ll1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ⍛"))
      if os.path.exists(bstack1llll1ll1lll_opy_):
          with open(bstack1llll1ll1lll_opy_) as f:
              bstack1lllll1l1l1l_opy_ = json.load(f)
      bstack1lllll1l1l1l_opy_.append(bstack1l11111lll_opy_)
      with open(bstack1llll1ll1lll_opy_, bstack1ll1l11_opy_ (u"ࠨࡹࠪ⍜")) as f:
          json.dump(bstack1lllll1l1l1l_opy_, f)
    except Exception as e:
      logger.warn(bstack1ll1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ⍝").format(e))
    return
  bstack1lllll1l1l1l_opy_ = []
  bstack1l11111lll_opy_ = {bstack1ll1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ⍞"): test_name, bstack1ll1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ⍟"): error_message, bstack1ll1l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ⍠"): index}
  bstack1llll1ll1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧ⍡"))
  lock_file = bstack1llll1ll1lll_opy_ + bstack1ll1l11_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭⍢")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1llll1ll1lll_opy_):
          with open(bstack1llll1ll1lll_opy_, bstack1ll1l11_opy_ (u"ࠨࡴࠪ⍣")) as f:
              content = f.read().strip()
              if content:
                  bstack1lllll1l1l1l_opy_ = json.load(open(bstack1llll1ll1lll_opy_))
      bstack1lllll1l1l1l_opy_.append(bstack1l11111lll_opy_)
      with open(bstack1llll1ll1lll_opy_, bstack1ll1l11_opy_ (u"ࠩࡺࠫ⍤")) as f:
          json.dump(bstack1lllll1l1l1l_opy_, f)
  except Exception as e:
    logger.warn(bstack1ll1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࡀࠠࡼࡿࠥ⍥").format(e))
def bstack1lll1l1l1l_opy_(bstack1ll11lll1l_opy_, name, logger):
  try:
    bstack1l11111lll_opy_ = {bstack1ll1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⍦"): name, bstack1ll1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⍧"): bstack1ll11lll1l_opy_, bstack1ll1l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⍨"): str(threading.current_thread()._name)}
    return bstack1l11111lll_opy_
  except Exception as e:
    logger.warn(bstack1ll1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡥࡩ࡭ࡧࡶࡦࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ⍩").format(e))
  return
def bstack1llll11l111l_opy_():
    return platform.system() == bstack1ll1l11_opy_ (u"ࠨ࡙࡬ࡲࡩࡵࡷࡴࠩ⍪")
def bstack1lllll111_opy_(bstack1llll1l1lll1_opy_, config, logger):
    bstack1llll1l11l11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1llll1l1lll1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡭ࡶࡨࡶࠥࡩ࡯࡯ࡨ࡬࡫ࠥࡱࡥࡺࡵࠣࡦࡾࠦࡲࡦࡩࡨࡼࠥࡳࡡࡵࡥ࡫࠾ࠥࢁࡽࠣ⍫").format(e))
    return bstack1llll1l11l11_opy_
def bstack1llll11ll1l1_opy_(bstack1llllllll111_opy_, bstack1lllll1ll111_opy_):
    bstack1lllllll11ll_opy_ = version.parse(bstack1llllllll111_opy_)
    bstack1llll1ll1ll1_opy_ = version.parse(bstack1lllll1ll111_opy_)
    if bstack1lllllll11ll_opy_ > bstack1llll1ll1ll1_opy_:
        return 1
    elif bstack1lllllll11ll_opy_ < bstack1llll1ll1ll1_opy_:
        return -1
    else:
        return 0
def bstack1lll1l11ll1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1llll11ll111_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1llll111l1l1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1111lll1l1_opy_(options, framework, config, bstack11l1l111ll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1ll1l11_opy_ (u"ࠪ࡫ࡪࡺࠧ⍬"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1ll11l11ll_opy_ = caps.get(bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ⍭"))
    bstack1llll111ll11_opy_ = True
    bstack11ll111111_opy_ = os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⍮")]
    bstack11lllll1l1l_opy_ = config.get(bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⍯"), False)
    if bstack11lllll1l1l_opy_:
        bstack1l11llll1l1_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ⍰"), {})
        bstack1l11llll1l1_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫ⍱")] = os.getenv(bstack1ll1l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ⍲"))
        bstack1l1l111l1_opy_ = json.loads(os.getenv(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ⍳"), bstack1ll1l11_opy_ (u"ࠫࢀࢃࠧ⍴"))).get(bstack1ll1l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⍵"))
    if bstack1llll1llll11_opy_(caps.get(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦ࡙࠶ࡇࠬ⍶"))) or bstack1llll1llll11_opy_(caps.get(bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡢࡻ࠸ࡩࠧ⍷"))):
        bstack1llll111ll11_opy_ = False
    if bstack111l11l1_opy_({bstack1ll1l11_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣ⍸"): bstack1llll111ll11_opy_}):
        bstack1ll11l11ll_opy_ = bstack1ll11l11ll_opy_ or {}
        bstack1ll11l11ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ⍹")] = bstack1llll111l1l1_opy_(framework)
        bstack1ll11l11ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⍺")] = bstack1l1lllllll_opy_()
        bstack1ll11l11ll_opy_[bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ⍻")] = bstack11ll111111_opy_
        bstack1ll11l11ll_opy_[bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ⍼")] = bstack11l1l111ll_opy_
        if bstack11lllll1l1l_opy_:
            bstack1ll11l11ll_opy_[bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⍽")] = bstack11lllll1l1l_opy_
            bstack1ll11l11ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ⍾")] = bstack1l11llll1l1_opy_
            bstack1ll11l11ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⍿")][bstack1ll1l11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ⎀")] = bstack1l1l111l1_opy_
        if getattr(options, bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫ⎁"), None):
            options.set_capability(bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ⎂"), bstack1ll11l11ll_opy_)
        else:
            options[bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭⎃")] = bstack1ll11l11ll_opy_
    else:
        if getattr(options, bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧ⎄"), None):
            options.set_capability(bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ⎅"), bstack1llll111l1l1_opy_(framework))
            options.set_capability(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ⎆"), bstack1l1lllllll_opy_())
            options.set_capability(bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ⎇"), bstack11ll111111_opy_)
            options.set_capability(bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ⎈"), bstack11l1l111ll_opy_)
            if bstack11lllll1l1l_opy_:
                options.set_capability(bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⎉"), bstack11lllll1l1l_opy_)
                options.set_capability(bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ⎊"), bstack1l11llll1l1_opy_)
                options.set_capability(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷ࠳ࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⎋"), bstack1l1l111l1_opy_)
        else:
            options[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ⎌")] = bstack1llll111l1l1_opy_(framework)
            options[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ⎍")] = bstack1l1lllllll_opy_()
            options[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ⎎")] = bstack11ll111111_opy_
            options[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ⎏")] = bstack11l1l111ll_opy_
            if bstack11lllll1l1l_opy_:
                options[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⎐")] = bstack11lllll1l1l_opy_
                options[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ⎑")] = bstack1l11llll1l1_opy_
                options[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ⎒")][bstack1ll1l11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⎓")] = bstack1l1l111l1_opy_
    return options
def bstack1llll1l1111l_opy_(ws_endpoint, framework):
    bstack11l1l111ll_opy_ = global_config.get_property(bstack1ll1l11_opy_ (u"ࠣࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡖࡒࡐࡆࡘࡇ࡙ࡥࡍࡂࡒࠥ⎔"))
    if ws_endpoint and len(ws_endpoint.split(bstack1ll1l11_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ⎕"))) > 1:
        ws_url = ws_endpoint.split(bstack1ll1l11_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ⎖"))[0]
        if bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ⎗") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1llll1111l11_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack1ll1l11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ⎘"))[1]))
            bstack1llll1111l11_opy_ = bstack1llll1111l11_opy_ or {}
            bstack11ll111111_opy_ = os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⎙")]
            bstack1llll1111l11_opy_[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ⎚")] = str(framework) + str(__version__)
            bstack1llll1111l11_opy_[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ⎛")] = bstack1l1lllllll_opy_()
            bstack1llll1111l11_opy_[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ⎜")] = bstack11ll111111_opy_
            bstack1llll1111l11_opy_[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ⎝")] = bstack11l1l111ll_opy_
            ws_endpoint = ws_endpoint.split(bstack1ll1l11_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ⎞"))[0] + bstack1ll1l11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ⎟") + urllib.parse.quote(json.dumps(bstack1llll1111l11_opy_))
    return ws_endpoint
def bstack1111l1ll1l_opy_():
    global bstack1l1l11l1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l1l11l1_opy_ = BrowserType.connect
    return bstack1l1l11l1_opy_
def bstack1llll11ll11l_opy_(framework_name):
    global FRAMEWORK_NAME
    FRAMEWORK_NAME = framework_name
    return framework_name
def bstack1l1l1l11111_opy_(self, *args, **kwargs):
    global bstack1l1l11l1_opy_
    try:
        global FRAMEWORK_NAME
        if bstack1ll1l11_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪ⎠") in kwargs:
            kwargs[bstack1ll1l11_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫ⎡")] = bstack1llll1l1111l_opy_(
                kwargs.get(bstack1ll1l11_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ⎢"), None),
                FRAMEWORK_NAME
            )
    except Exception as e:
        logger.error(bstack1ll1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡗࡉࡑࠠࡤࡣࡳࡷ࠿ࠦࡻࡾࠤ⎣").format(str(e)))
    return bstack1l1l11l1_opy_(self, *args, **kwargs)
def bstack1lllll1llll1_opy_(bstack1llll1ll1l1l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1l1l1l11l1_opy_(bstack1llll1ll1l1l_opy_, bstack1ll1l11_opy_ (u"ࠥࠦ⎤"))
        if proxies and proxies.get(bstack1ll1l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥ⎥")):
            parsed_url = urlparse(proxies.get(bstack1ll1l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦ⎦")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩ⎧")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪ⎨")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1ll1l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫ⎩")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1ll1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬ⎪")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l11l1ll1_opy_(bstack1llll1ll1l1l_opy_):
    bstack1lllllll1111_opy_ = {
        bstack111111l1lll_opy_[bstack1llllll1111l_opy_]: bstack1llll1ll1l1l_opy_[bstack1llllll1111l_opy_]
        for bstack1llllll1111l_opy_ in bstack1llll1ll1l1l_opy_
        if bstack1llllll1111l_opy_ in bstack111111l1lll_opy_
    }
    bstack1lllllll1111_opy_[bstack1ll1l11_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥ⎫")] = bstack1lllll1llll1_opy_(bstack1llll1ll1l1l_opy_, global_config.get_property(bstack1ll1l11_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦ⎬")))
    bstack1llll11l1ll1_opy_ = [element.lower() for element in bstack11111ll111l_opy_]
    bstack1lllllll1lll_opy_(bstack1lllllll1111_opy_, bstack1llll11l1ll1_opy_)
    return bstack1lllllll1111_opy_
def bstack1lllllll1lll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1ll1l11_opy_ (u"ࠧ࠰ࠪࠫࠬࠥ⎭")
    for value in d.values():
        if isinstance(value, dict):
            bstack1lllllll1lll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1lllllll1lll_opy_(item, keys)
def bstack11ll11ll11l_opy_():
    bstack1llllll11lll_opy_ = [os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡉࡍࡇࡖࡣࡉࡏࡒࠣ⎮")), os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠢࡿࠤ⎯")), bstack1ll1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ⎰")), os.path.join(bstack1ll1l11_opy_ (u"ࠩ࠲ࡸࡲࡶࠧ⎱"), bstack1ll1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ⎲"))]
    for path in bstack1llllll11lll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1ll1l11_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦ⎳") + str(path) + bstack1ll1l11_opy_ (u"ࠧ࠭ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠣ⎴"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1ll1l11_opy_ (u"ࠨࡇࡪࡸ࡬ࡲ࡬ࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶࠤ࡫ࡵࡲࠡࠩࠥ⎵") + str(path) + bstack1ll1l11_opy_ (u"ࠢࠨࠤ⎶"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1ll1l11_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣ⎷") + str(path) + bstack1ll1l11_opy_ (u"ࠤࠪࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡮ࡡࡴࠢࡷ࡬ࡪࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠴ࠢ⎸"))
            else:
                logger.debug(bstack1ll1l11_opy_ (u"ࠥࡇࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࠫࠧ⎹") + str(path) + bstack1ll1l11_opy_ (u"ࠦࠬࠦࡷࡪࡶ࡫ࠤࡼࡸࡩࡵࡧࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴ࠮ࠣ⎺"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1ll1l11_opy_ (u"ࠧࡕࡰࡦࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡸࡧࡨ࡫ࡥࡥࡧࡧࠤ࡫ࡵࡲࠡࠩࠥ⎻") + str(path) + bstack1ll1l11_opy_ (u"ࠨࠧ࠯ࠤ⎼"))
            return path
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡶࡲࠣࡪ࡮ࡲࡥࠡࠩࡾࡴࡦࡺࡨࡾࠩ࠽ࠤࠧ⎽") + str(e) + bstack1ll1l11_opy_ (u"ࠣࠤ⎾"))
    logger.debug(bstack1ll1l11_opy_ (u"ࠤࡄࡰࡱࠦࡰࡢࡶ࡫ࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠨ⎿"))
    return None
@measure(event_name=EVENTS.bstack11111ll1ll1_opy_, stage=STAGE.bstack1ll11l11_opy_)
def bstack1ll1l11lll1_opy_(binary_path, bstack1ll1l11l111_opy_, bs_config):
    logger.debug(bstack1ll1l11_opy_ (u"ࠥࡇࡺࡸࡲࡦࡰࡷࠤࡈࡒࡉࠡࡒࡤࡸ࡭ࠦࡦࡰࡷࡱࡨ࠿ࠦࡻࡾࠤ⏀").format(binary_path))
    bstack1llllllll1l1_opy_ = bstack1ll1l11_opy_ (u"ࠫࠬ⏁")
    bstack1lllll11ll1l_opy_ = {
        bstack1ll1l11_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ⏂"): __version__,
        bstack1ll1l11_opy_ (u"ࠨ࡯ࡴࠤ⏃"): platform.system(),
        bstack1ll1l11_opy_ (u"ࠢࡰࡵࡢࡥࡷࡩࡨࠣ⏄"): platform.machine(),
        bstack1ll1l11_opy_ (u"ࠣࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ⏅"): bstack1ll1l11_opy_ (u"ࠩ࠳ࠫ⏆"),
        bstack1ll1l11_opy_ (u"ࠥࡷࡩࡱ࡟࡭ࡣࡱ࡫ࡺࡧࡧࡦࠤ⏇"): bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⏈")
    }
    bstack1llllll1ll1l_opy_(bstack1lllll11ll1l_opy_)
    try:
        if binary_path:
            if bstack1llll11l111l_opy_():
                bstack1lllll11ll1l_opy_[bstack1ll1l11_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪ⏉")] = subprocess.check_output([binary_path, bstack1ll1l11_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢ⏊")]).strip().decode(bstack1ll1l11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭⏋"))
            else:
                bstack1lllll11ll1l_opy_[bstack1ll1l11_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⏌")] = subprocess.check_output([binary_path, bstack1ll1l11_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥ⏍")], stderr=subprocess.DEVNULL).strip().decode(bstack1ll1l11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ⏎"))
        response = requests.request(
            bstack1ll1l11_opy_ (u"ࠫࡌࡋࡔࠨ⏏"),
            url=bstack1111ll1ll1_opy_(bstack11111l111l1_opy_),
            headers=None,
            auth=(bs_config[bstack1ll1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ⏐")], bs_config[bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ⏑")]),
            json=None,
            params=bstack1lllll11ll1l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1ll1l11_opy_ (u"ࠧࡶࡴ࡯ࠫ⏒") in data.keys() and bstack1ll1l11_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥࡡࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⏓") in data.keys():
            logger.debug(bstack1ll1l11_opy_ (u"ࠤࡑࡩࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡦ࡮ࡴࡡࡳࡻ࠯ࠤࡨࡻࡲࡳࡧࡱࡸࠥࡨࡩ࡯ࡣࡵࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࡀࠠࡼࡿࠥ⏔").format(bstack1lllll11ll1l_opy_[bstack1ll1l11_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⏕")]))
            if bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠧ⏖") in os.environ:
                logger.debug(bstack1ll1l11_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡣ࡫ࡱࡥࡷࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡤࡷࠥࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠡ࡫ࡶࠤࡸ࡫ࡴࠣ⏗"))
                data[bstack1ll1l11_opy_ (u"࠭ࡵࡳ࡮ࠪ⏘")] = os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠪ⏙")]
            bstack1lllll1111ll_opy_ = bstack1llll1l111l1_opy_(data[bstack1ll1l11_opy_ (u"ࠨࡷࡵࡰࠬ⏚")], bstack1ll1l11l111_opy_)
            bstack1llllllll1l1_opy_ = os.path.join(bstack1ll1l11l111_opy_, bstack1lllll1111ll_opy_)
            os.chmod(bstack1llllllll1l1_opy_, 0o777) # bstack1lllll1l11ll_opy_ permission
            return bstack1llllllll1l1_opy_
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡴࡥࡸࠢࡖࡈࡐࠦࡻࡾࠤ⏛").format(e))
    return binary_path
def bstack1llllll1ll1l_opy_(bstack1lllll11ll1l_opy_):
    try:
        if bstack1ll1l11_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩ⏜") not in bstack1lllll11ll1l_opy_[bstack1ll1l11_opy_ (u"ࠫࡴࡹࠧ⏝")].lower():
            return
        if os.path.exists(bstack1ll1l11_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡳࡸ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢ⏞")):
            with open(bstack1ll1l11_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡴࡹ࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣ⏟"), bstack1ll1l11_opy_ (u"ࠢࡳࠤ⏠")) as f:
                bstack1lllll111lll_opy_ = {}
                for line in f:
                    if bstack1ll1l11_opy_ (u"ࠣ࠿ࠥ⏡") in line:
                        key, value = line.rstrip().split(bstack1ll1l11_opy_ (u"ࠤࡀࠦ⏢"), 1)
                        bstack1lllll111lll_opy_[key] = value.strip(bstack1ll1l11_opy_ (u"ࠪࠦࡡ࠭ࠧ⏣"))
                bstack1lllll11ll1l_opy_[bstack1ll1l11_opy_ (u"ࠫࡩ࡯ࡳࡵࡴࡲࠫ⏤")] = bstack1lllll111lll_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡏࡄࠣ⏥"), bstack1ll1l11_opy_ (u"ࠨࠢ⏦"))
        elif os.path.exists(bstack1ll1l11_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡧ࡬ࡱ࡫ࡱࡩ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨ⏧")):
            bstack1lllll11ll1l_opy_[bstack1ll1l11_opy_ (u"ࠨࡦ࡬ࡷࡹࡸ࡯ࠨ⏨")] = bstack1ll1l11_opy_ (u"ࠩࡤࡰࡵ࡯࡮ࡦࠩ⏩")
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡶࠣࡨ࡮ࡹࡴࡳࡱࠣࡳ࡫ࠦ࡬ࡪࡰࡸࡼࠧ⏪") + e)
@measure(event_name=EVENTS.bstack111111l1ll1_opy_, stage=STAGE.bstack1ll11l11_opy_)
def bstack1llll1l111l1_opy_(bstack1llll11l1111_opy_, bstack1llll1llllll_opy_):
    logger.debug(bstack1ll1l11_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰ࠾ࠥࠨ⏫") + str(bstack1llll11l1111_opy_) + bstack1ll1l11_opy_ (u"ࠧࠨ⏬"))
    zip_path = os.path.join(bstack1llll1llllll_opy_, bstack1ll1l11_opy_ (u"ࠨࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࡢࡪ࡮ࡲࡥ࠯ࡼ࡬ࡴࠧ⏭"))
    bstack1lllll1111ll_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨ⏮")
    with requests.get(bstack1llll11l1111_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1ll1l11_opy_ (u"ࠣࡹࡥࠦ⏯")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1ll1l11_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻ࠱ࠦ⏰"))
    with zipfile.ZipFile(zip_path, bstack1ll1l11_opy_ (u"ࠪࡶࠬ⏱")) as zip_ref:
        bstack1llll111l11l_opy_ = zip_ref.namelist()
        if len(bstack1llll111l11l_opy_) > 0:
            bstack1lllll1111ll_opy_ = bstack1llll111l11l_opy_[0] # bstack1lllll1ll1l1_opy_ bstack11111l1ll1l_opy_ will be bstack1llll111l111_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack1llll1llllll_opy_)
        logger.debug(bstack1ll1l11_opy_ (u"ࠦࡋ࡯࡬ࡦࡵࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡨࡼࡹࡸࡡࡤࡶࡨࡨࠥࡺ࡯ࠡࠩࠥ⏲") + str(bstack1llll1llllll_opy_) + bstack1ll1l11_opy_ (u"ࠧ࠭ࠢ⏳"))
    os.remove(zip_path)
    return bstack1lllll1111ll_opy_
def get_cli_dir():
    bstack1llll1l1ll11_opy_ = bstack11ll11ll11l_opy_()
    if bstack1llll1l1ll11_opy_:
        bstack1ll1l11l111_opy_ = os.path.join(bstack1llll1l1ll11_opy_, bstack1ll1l11_opy_ (u"ࠨࡣ࡭࡫ࠥ⏴"))
        if not os.path.exists(bstack1ll1l11l111_opy_):
            os.makedirs(bstack1ll1l11l111_opy_, mode=0o777, exist_ok=True)
        return bstack1ll1l11l111_opy_
    else:
        raise FileNotFoundError(bstack1ll1l11_opy_ (u"ࠢࡏࡱࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤ࡫ࡵࡲࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺ࠰ࠥ⏵"))
def bstack1ll1l111lll_opy_(bstack1ll1l11l111_opy_):
    bstack1ll1l11_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠࡵࡪࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾࠦࡩ࡯ࠢࡤࠤࡼࡸࡩࡵࡣࡥࡰࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠰ࠥࠦࠧ⏶")
    bstack1llll11l1l11_opy_ = [
        os.path.join(bstack1ll1l11l111_opy_, f)
        for f in os.listdir(bstack1ll1l11l111_opy_)
        if os.path.isfile(os.path.join(bstack1ll1l11l111_opy_, f)) and f.startswith(bstack1ll1l11_opy_ (u"ࠤࡥ࡭ࡳࡧࡲࡺ࠯ࠥ⏷"))
    ]
    if len(bstack1llll11l1l11_opy_) > 0:
        return max(bstack1llll11l1l11_opy_, key=os.path.getmtime) # get bstack1llll1ll11ll_opy_ binary
    return bstack1ll1l11_opy_ (u"ࠥࠦ⏸")
def bstack1111l1lllll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l111l11lll_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l111l11lll_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l111l1ll1_opy_(data, keys, default=None):
    bstack1ll1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡘࡧࡦࡦ࡮ࡼࠤ࡬࡫ࡴࠡࡣࠣࡲࡪࡹࡴࡦࡦࠣࡺࡦࡲࡵࡦࠢࡩࡶࡴࡳࠠࡢࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦ࡯ࡳࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡪࡡࡵࡣ࠽ࠤ࡙࡮ࡥࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡵࡲࠡ࡮࡬ࡷࡹࠦࡴࡰࠢࡷࡶࡦࡼࡥࡳࡵࡨ࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢ࡮ࡩࡾࡹ࠺ࠡࡃࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡰ࡫ࡹࡴ࠱࡬ࡲࡩ࡯ࡣࡦࡵࠣࡶࡪࡶࡲࡦࡵࡨࡲࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢࡧࡩ࡫ࡧࡵ࡭ࡶ࠽ࠤ࡛ࡧ࡬ࡶࡧࠣࡸࡴࠦࡲࡦࡶࡸࡶࡳࠦࡩࡧࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫ࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣ࠾ࡷ࡫ࡴࡶࡴࡱ࠾࡚ࠥࡨࡦࠢࡹࡥࡱࡻࡥࠡࡣࡷࠤࡹ࡮ࡥࠡࡰࡨࡷࡹ࡫ࡤࠡࡲࡤࡸ࡭࠲ࠠࡰࡴࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤ࡮࡬ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ⏹")
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
def bstack11l1llll1l_opy_(bstack1lllll1l1lll_opy_, key, value):
    bstack1ll1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡙ࠥࡴࡰࡴࡨࠤࡈࡒࡉࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴࠢࡰࡥࡵࡶࡩ࡯ࡩࠣ࡭ࡳࠦࡴࡩࡧࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤ࡮࡬ࡣࡪࡴࡶࡠࡸࡤࡶࡸࡥ࡭ࡢࡲ࠽ࠤࡉ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠣࡱࡦࡶࡰࡪࡰࡪࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦ࡫ࡦࡻ࠽ࠤࡐ࡫ࡹࠡࡨࡵࡳࡲࠦࡃࡍࡋࡢࡇࡆࡖࡓࡠࡖࡒࡣࡈࡕࡎࡇࡋࡊࠎࠥࠦࠠࠡࠢࠣࠤࠥࡼࡡ࡭ࡷࡨ࠾ࠥ࡜ࡡ࡭ࡷࡨࠤ࡫ࡸ࡯࡮ࠢࡦࡳࡲࡳࡡ࡯ࡦࠣࡰ࡮ࡴࡥࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠎࠥࠦࠠࠡࠤࠥࠦ⏺")
    if key in bstack11l1l111l_opy_:
        bstack1l1l111l_opy_ = bstack11l1l111l_opy_[key]
        if isinstance(bstack1l1l111l_opy_, list):
            for env_name in bstack1l1l111l_opy_:
                bstack1lllll1l1lll_opy_[env_name] = value
        else:
            bstack1lllll1l1lll_opy_[bstack1l1l111l_opy_] = value