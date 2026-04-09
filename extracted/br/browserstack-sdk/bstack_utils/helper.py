# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
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
from bstack_utils.constants import (bstack1llllll11_opy_, bstack1ll1l1l1l_opy_, bstack11llll11l_opy_,
                                    bstack11111ll1l11_opy_, bstack11111ll11l1_opy_, bstack11111l11lll_opy_, bstack11111l11ll1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l11l1lll_opy_, bstack111ll11ll_opy_
from bstack_utils.proxy import bstack1111l1ll1_opy_, bstack1ll111lll1_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack11lll11l11_opy_ import bstack1111l11l1_opy_
from browserstack_sdk._version import __version__
global_config = Config.bstack111llll11_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
automation_logger = logger_utils.get_automation_logger(__name__)
def bstack1111ll11ll1_opy_(config):
    return config[bstack11ll11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭Ⅾ")]
def bstack1111llllll1_opy_(config):
    return config[bstack11ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨⅯ")]
def bstack1lll1111l_opy_():
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
def bstack1llll1l11lll_opy_(obj):
    values = []
    bstack1llll11ll1l1_opy_ = re.compile(bstack11ll11_opy_ (u"ࡸࠢ࡟ࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤࡢࡤࠬࠦࠥⅰ"), re.I)
    for key in obj.keys():
        if bstack1llll11ll1l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1llll11l111l_opy_(config):
    tags = []
    tags.extend(bstack1llll1l11lll_opy_(os.environ))
    tags.extend(bstack1llll1l11lll_opy_(config))
    return tags
def bstack1llll11l1111_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1llll1l11l11_opy_(bstack1lllll1111ll_opy_):
    if not bstack1lllll1111ll_opy_:
        return bstack11ll11_opy_ (u"ࠧࠨⅱ")
    return bstack11ll11_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤⅲ").format(bstack1lllll1111ll_opy_.name, bstack1lllll1111ll_opy_.email)
def bstack1111l1lllll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1lllll1lll1l_opy_ = repo.common_dir
        info = {
            bstack11ll11_opy_ (u"ࠤࡶ࡬ࡦࠨⅳ"): repo.head.commit.hexsha,
            bstack11ll11_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨⅴ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11ll11_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦⅵ"): repo.active_branch.name,
            bstack11ll11_opy_ (u"ࠧࡺࡡࡨࠤⅶ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11ll11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤⅷ"): bstack1llll1l11l11_opy_(repo.head.commit.committer),
            bstack11ll11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣⅸ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11ll11_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣⅹ"): bstack1llll1l11l11_opy_(repo.head.commit.author),
            bstack11ll11_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢⅺ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11ll11_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦⅻ"): repo.head.commit.message,
            bstack11ll11_opy_ (u"ࠦࡷࡵ࡯ࡵࠤⅼ"): repo.git.rev_parse(bstack11ll11_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢⅽ")),
            bstack11ll11_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢⅾ"): bstack1lllll1lll1l_opy_,
            bstack11ll11_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴࠥⅿ"): subprocess.check_output([bstack11ll11_opy_ (u"ࠣࡩ࡬ࡸࠧↀ"), bstack11ll11_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧↁ"), bstack11ll11_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨↂ")]).strip().decode(
                bstack11ll11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪↃ")),
            bstack11ll11_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢↄ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11ll11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣↅ"): repo.git.rev_list(
                bstack11ll11_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢↆ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1llll111l11l_opy_ = []
        for remote in remotes:
            bstack1llllll11l11_opy_ = {
                bstack11ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨↇ"): remote.name,
                bstack11ll11_opy_ (u"ࠤࡸࡶࡱࠨↈ"): remote.url,
            }
            bstack1llll111l11l_opy_.append(bstack1llllll11l11_opy_)
        bstack1llll1l1ll11_opy_ = {
            bstack11ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣ↉"): bstack11ll11_opy_ (u"ࠦ࡬࡯ࡴࠣ↊"),
            **info,
            bstack11ll11_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨ↋"): bstack1llll111l11l_opy_
        }
        bstack1llll1l1ll11_opy_ = bstack1llll1111ll1_opy_(bstack1llll1l1ll11_opy_)
        return bstack1llll1l1ll11_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ↌").format(err))
        return {}
def bstack1llll1111l1l_opy_(bstack1llllll1lll1_opy_=None):
    bstack11ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡈࡧࡷࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡧࡦࡲ࡬ࡺࠢࡩࡳࡷࡳࡡࡵࡶࡨࡨࠥ࡬࡯ࡳࠢࡄࡍࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡷࡶࡩࠥࡩࡡࡴࡧࡶࠤ࡫ࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡰ࡮ࡧࡩࡷࠦࡩ࡯ࠢࡷ࡬ࡪࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡩࡳࡱࡪࡥࡳࡵࠣࠬࡱ࡯ࡳࡵ࠮ࠣࡳࡵࡺࡩࡰࡰࡤࡰ࠮ࡀࠠࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡐࡲࡲࡪࡀࠠࡎࡱࡱࡳ࠲ࡸࡥࡱࡱࠣࡥࡵࡶࡲࡰࡣࡦ࡬࠱ࠦࡵࡴࡧࡶࠤࡨࡻࡲࡳࡧࡱࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡝ࡲࡷ࠳࡭ࡥࡵࡥࡺࡨ࠭࠯࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡇࡰࡴࡹࡿࠠ࡭࡫ࡶࡸࠥࡡ࡝࠻ࠢࡐࡹࡱࡺࡩ࠮ࡴࡨࡴࡴࠦࡡࡱࡲࡵࡳࡦࡩࡨࠡࡹ࡬ࡸ࡭ࠦ࡮ࡰࠢࡶࡳࡺࡸࡣࡦࡵࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠬࠡࡴࡨࡸࡺࡸ࡮ࡴࠢ࡞ࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡰࡢࡶ࡫ࡷ࠿ࠦࡍࡶ࡮ࡷ࡭࠲ࡸࡥࡱࡱࠣࡥࡵࡶࡲࡰࡣࡦ࡬ࠥࡽࡩࡵࡪࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡧࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࡴࡰࠢࡤࡲࡦࡲࡹࡻࡧࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡰ࡮ࡹࡴ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡨ࡮ࡩࡴࡴ࠮ࠣࡩࡦࡩࡨࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡣࠣࡪࡴࡲࡤࡦࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ↍")
    if bstack1llllll1lll1_opy_ is None:
        bstack1llllll1lll1_opy_ = [os.getcwd()]
    elif isinstance(bstack1llllll1lll1_opy_, list) and len(bstack1llllll1lll1_opy_) == 0:
        return []
    results = []
    for folder in bstack1llllll1lll1_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack11ll11_opy_ (u"ࠣࡈࡲࡰࡩ࡫ࡲࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂࠨ↎").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack11ll11_opy_ (u"ࠤࡳࡶࡎࡪࠢ↏"): bstack11ll11_opy_ (u"ࠥࠦ←"),
                bstack11ll11_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥ↑"): [],
                bstack11ll11_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨ→"): [],
                bstack11ll11_opy_ (u"ࠨࡰࡳࡆࡤࡸࡪࠨ↓"): bstack11ll11_opy_ (u"ࠢࠣ↔"),
                bstack11ll11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡎࡧࡶࡷࡦ࡭ࡥࡴࠤ↕"): [],
                bstack11ll11_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥ↖"): bstack11ll11_opy_ (u"ࠥࠦ↗"),
                bstack11ll11_opy_ (u"ࠦࡵࡸࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦ↘"): bstack11ll11_opy_ (u"ࠧࠨ↙"),
                bstack11ll11_opy_ (u"ࠨࡰࡳࡔࡤࡻࡉ࡯ࡦࡧࠤ↚"): bstack11ll11_opy_ (u"ࠢࠣ↛")
            }
            bstack1lllll1l1lll_opy_ = repo.active_branch.name
            bstack1llll1l1ll1l_opy_ = repo.head.commit
            result[bstack11ll11_opy_ (u"ࠣࡲࡵࡍࡩࠨ↜")] = bstack1llll1l1ll1l_opy_.hexsha
            bstack1llll1ll1111_opy_ = _1llll1ll111l_opy_(repo)
            logger.debug(bstack11ll11_opy_ (u"ࠤࡅࡥࡸ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡧࡱࡵࠤࡨࡵ࡭ࡱࡣࡵ࡭ࡸࡵ࡮࠻ࠢࠥ↝") + str(bstack1llll1ll1111_opy_) + bstack11ll11_opy_ (u"ࠥࠦ↞"))
            if bstack1llll1ll1111_opy_:
                try:
                    bstack1llllll1ll11_opy_ = repo.git.diff(bstack11ll11_opy_ (u"ࠦ࠲࠳࡮ࡢ࡯ࡨ࠱ࡴࡴ࡬ࡺࠤ↟"), bstack1l1ll1lll11_opy_ (u"ࠧࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠳࠴࠮ࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿࠥ↠")).split(bstack11ll11_opy_ (u"࠭࡜࡯ࠩ↡"))
                    logger.debug(bstack11ll11_opy_ (u"ࠢࡄࡪࡤࡲ࡬࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡣࡧࡷࡻࡪ࡫࡮ࠡࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽࠡࡣࡱࡨࠥࢁࡣࡶࡴࡵࡩࡳࡺ࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠻ࠢࠥ↢") + str(bstack1llllll1ll11_opy_) + bstack11ll11_opy_ (u"ࠣࠤ↣"))
                    result[bstack11ll11_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣ↤")] = [f.strip() for f in bstack1llllll1ll11_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1l1ll1lll11_opy_ (u"ࠥࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿ࠱࠲ࢀࡩࡵࡳࡴࡨࡲࡹࡥࡢࡳࡣࡱࡧ࡭ࢃࠢ↥")))
                except Exception:
                    logger.debug(bstack11ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡨ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡥࡶࡦࡴࡣࡩࠢࡦࡳࡲࡶࡡࡳ࡫ࡶࡳࡳ࠴ࠠࡇࡣ࡯ࡰ࡮ࡴࡧࠡࡤࡤࡧࡰࠦࡴࡰࠢࡵࡩࡨ࡫࡮ࡵࠢࡦࡳࡲࡳࡩࡵࡵ࠱ࠦ↦"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack11ll11_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦ↧")] = _1llll11111ll_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack11ll11_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧ↨")] = _1llll11111ll_opy_(commits[:5])
            bstack1lllll1l111l_opy_ = set()
            bstack1lllll11l111_opy_ = []
            for commit in commits:
                logger.debug(bstack11ll11_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡨࡵ࡭࡮࡫ࡷ࠾ࠥࠨ↩") + str(commit.message) + bstack11ll11_opy_ (u"ࠣࠤ↪"))
                bstack1lllll11l1ll_opy_ = commit.author.name if commit.author else bstack11ll11_opy_ (u"ࠤࡘࡲࡰࡴ࡯ࡸࡰࠥ↫")
                bstack1lllll1l111l_opy_.add(bstack1lllll11l1ll_opy_)
                bstack1lllll11l111_opy_.append({
                    bstack11ll11_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦ↬"): commit.message.strip(),
                    bstack11ll11_opy_ (u"ࠦࡺࡹࡥࡳࠤ↭"): bstack1lllll11l1ll_opy_
                })
            result[bstack11ll11_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨ↮")] = list(bstack1lllll1l111l_opy_)
            result[bstack11ll11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡓࡥࡴࡵࡤ࡫ࡪࡹࠢ↯")] = bstack1lllll11l111_opy_
            result[bstack11ll11_opy_ (u"ࠢࡱࡴࡇࡥࡹ࡫ࠢ↰")] = bstack1llll1l1ll1l_opy_.committed_datetime.strftime(bstack11ll11_opy_ (u"ࠣࠧ࡜࠱ࠪࡳ࠭ࠦࡦࠥ↱"))
            if (not result[bstack11ll11_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥ↲")] or result[bstack11ll11_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦ↳")].strip() == bstack11ll11_opy_ (u"ࠦࠧ↴")) and bstack1llll1l1ll1l_opy_.message:
                bstack1llllllll1l1_opy_ = bstack1llll1l1ll1l_opy_.message.strip().splitlines()
                result[bstack11ll11_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨ↵")] = bstack1llllllll1l1_opy_[0] if bstack1llllllll1l1_opy_ else bstack11ll11_opy_ (u"ࠨࠢ↶")
                if len(bstack1llllllll1l1_opy_) > 2:
                    result[bstack11ll11_opy_ (u"ࠢࡱࡴࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢ↷")] = bstack11ll11_opy_ (u"ࠨ࡞ࡱࠫ↸").join(bstack1llllllll1l1_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack11ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡃࡌࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠࠩࡨࡲࡰࡩ࡫ࡲ࠻ࠢࡾࢁ࠮ࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣ↹").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    bstack1llll1llllll_opy_ = [
        result
        for result in results
        if _1llll1l111ll_opy_(result)
    ]
    return bstack1llll1llllll_opy_
def _1llll1l111ll_opy_(result):
    bstack11ll11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡌࡪࡲࡰࡦࡴࠣࡸࡴࠦࡣࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡣࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡸࡻ࡬ࡵࠢ࡬ࡷࠥࡼࡡ࡭࡫ࡧࠤ࠭ࡴ࡯࡯࠯ࡨࡱࡵࡺࡹࠡࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠠࡢࡰࡧࠤࡦࡻࡴࡩࡱࡵࡷ࠮࠴ࠊࠡࠢࠣࠤࠧࠨࠢ↺")
    return (
        isinstance(result.get(bstack11ll11_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥ↻"), None), list)
        and len(result[bstack11ll11_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦ↼")]) > 0
        and isinstance(result.get(bstack11ll11_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢ↽"), None), list)
        and len(result[bstack11ll11_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣ↾")]) > 0
    )
def _1llll1ll111l_opy_(repo):
    bstack11ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡖࡵࡽࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡮ࡥࠡࡤࡤࡷࡪࠦࡢࡳࡣࡱࡧ࡭ࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡲࡦࡲࡲࠤࡼ࡯ࡴࡩࡱࡸࡸࠥ࡮ࡡࡳࡦࡦࡳࡩ࡫ࡤࠡࡰࡤࡱࡪࡹࠠࡢࡰࡧࠤࡼࡵࡲ࡬ࠢࡺ࡭ࡹ࡮ࠠࡢ࡮࡯ࠤ࡛ࡉࡓࠡࡲࡵࡳࡻ࡯ࡤࡦࡴࡶ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡥࡧࡩࡥࡺࡲࡴࠡࡤࡵࡥࡳࡩࡨࠡ࡫ࡩࠤࡵࡵࡳࡴ࡫ࡥࡰࡪ࠲ࠠࡦ࡮ࡶࡩࠥࡔ࡯࡯ࡧ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ↿")
    try:
        try:
            origin = repo.remotes.origin
            bstack1lllllll1lll_opy_ = origin.refs[bstack11ll11_opy_ (u"ࠩࡋࡉࡆࡊࠧ⇀")]
            target = bstack1lllllll1lll_opy_.reference.name
            if target.startswith(bstack11ll11_opy_ (u"ࠪࡳࡷ࡯ࡧࡪࡰ࠲ࠫ⇁")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack11ll11_opy_ (u"ࠫࡴࡸࡩࡨ࡫ࡱ࠳ࠬ⇂")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _1llll11111ll_opy_(commits):
    bstack11ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡍࡥࡵࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡧ࡭ࡧ࡮ࡨࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡪࡷࡵ࡭ࠡࡣࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࡷ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ⇃")
    bstack1llllll1ll11_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack1llllll11lll_opy_ in diff:
                        if bstack1llllll11lll_opy_.a_path:
                            bstack1llllll1ll11_opy_.add(bstack1llllll11lll_opy_.a_path)
                        if bstack1llllll11lll_opy_.b_path:
                            bstack1llllll1ll11_opy_.add(bstack1llllll11lll_opy_.b_path)
    except Exception:
        pass
    return list(bstack1llllll1ll11_opy_)
def bstack1llll1111ll1_opy_(bstack1llll1l1ll11_opy_):
    bstack1llll1lll1ll_opy_ = bstack1lllll111lll_opy_(bstack1llll1l1ll11_opy_)
    if bstack1llll1lll1ll_opy_ and bstack1llll1lll1ll_opy_ > bstack11111ll1l11_opy_:
        bstack1llll1ll11ll_opy_ = bstack1llll1lll1ll_opy_ - bstack11111ll1l11_opy_
        bstack1llll111lll1_opy_ = bstack1lllll11111l_opy_(bstack1llll1l1ll11_opy_[bstack11ll11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢ⇄")], bstack1llll1ll11ll_opy_)
        bstack1llll1l1ll11_opy_[bstack11ll11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ⇅")] = bstack1llll111lll1_opy_
        logger.info(bstack11ll11_opy_ (u"ࠣࡖ࡫ࡩࠥࡩ࡯࡮࡯࡬ࡸࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦ࠱ࠤࡘ࡯ࡺࡦࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࠥࡧࡦࡵࡧࡵࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࢀࢃࠠࡌࡄࠥ⇆")
                    .format(bstack1lllll111lll_opy_(bstack1llll1l1ll11_opy_) / 1024))
    return bstack1llll1l1ll11_opy_
def bstack1lllll111lll_opy_(json_data):
    try:
        if json_data:
            bstack1lllll11lll1_opy_ = json.dumps(json_data)
            bstack1llll1l11l1l_opy_ = sys.getsizeof(bstack1lllll11lll1_opy_)
            return bstack1llll1l11l1l_opy_
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡥࡤࡰࡨࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡋࡕࡒࡒࠥࡵࡢ࡫ࡧࡦࡸ࠿ࠦࡻࡾࠤ⇇").format(e))
    return -1
def bstack1lllll11111l_opy_(field, bstack1lllll111ll1_opy_):
    try:
        bstack1llll111l111_opy_ = len(bytes(bstack11111ll11l1_opy_, bstack11ll11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ⇈")))
        bstack1lllll1111l1_opy_ = bytes(field, bstack11ll11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ⇉"))
        bstack1llll11ll11l_opy_ = len(bstack1lllll1111l1_opy_)
        bstack1llllllll11l_opy_ = ceil(bstack1llll11ll11l_opy_ - bstack1lllll111ll1_opy_ - bstack1llll111l111_opy_)
        if bstack1llllllll11l_opy_ > 0:
            bstack1llll11l1l1l_opy_ = bstack1lllll1111l1_opy_[:bstack1llllllll11l_opy_].decode(bstack11ll11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ⇊"), errors=bstack11ll11_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ࠭⇋")) + bstack11111ll11l1_opy_
            return bstack1llll11l1l1l_opy_
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡪࡲࡤ࠭ࠢࡱࡳࡹ࡮ࡩ࡯ࡩࠣࡻࡦࡹࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦࠣ࡬ࡪࡸࡥ࠻ࠢࡾࢁࠧ⇌").format(e))
    return field
def bstack1ll1l1l11l_opy_():
    env = os.environ
    if (bstack11ll11_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨ⇍") in env and len(env[bstack11ll11_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢ⇎")]) > 0) or (
            bstack11ll11_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ⇏") in env and len(env[bstack11ll11_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥ⇐")]) > 0):
        return {
            bstack11ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⇑"): bstack11ll11_opy_ (u"ࠨࡊࡦࡰ࡮࡭ࡳࡹࠢ⇒"),
            bstack11ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⇓"): env.get(bstack11ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ⇔")),
            bstack11ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⇕"): env.get(bstack11ll11_opy_ (u"ࠥࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ⇖")),
            bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⇗"): env.get(bstack11ll11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ⇘"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠨࡃࡊࠤ⇙")) == bstack11ll11_opy_ (u"ࠢࡵࡴࡸࡩࠧ⇚") and bstack1lll1lll1_opy_(env.get(bstack11ll11_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡄࡋࠥ⇛"))):
        return {
            bstack11ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⇜"): bstack11ll11_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍࠧ⇝"),
            bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⇞"): env.get(bstack11ll11_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ⇟")),
            bstack11ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⇠"): env.get(bstack11ll11_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦ⇡")),
            bstack11ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⇢"): env.get(bstack11ll11_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࠧ⇣"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠥࡇࡎࠨ⇤")) == bstack11ll11_opy_ (u"ࠦࡹࡸࡵࡦࠤ⇥") and bstack1lll1lll1_opy_(env.get(bstack11ll11_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧ⇦"))):
        return {
            bstack11ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⇧"): bstack11ll11_opy_ (u"ࠢࡕࡴࡤࡺ࡮ࡹࠠࡄࡋࠥ⇨"),
            bstack11ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⇩"): env.get(bstack11ll11_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠ࡙ࡈࡆࡤ࡛ࡒࡍࠤ⇪")),
            bstack11ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⇫"): env.get(bstack11ll11_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ⇬")),
            bstack11ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⇭"): env.get(bstack11ll11_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ⇮"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠢࡄࡋࠥ⇯")) == bstack11ll11_opy_ (u"ࠣࡶࡵࡹࡪࠨ⇰") and env.get(bstack11ll11_opy_ (u"ࠤࡆࡍࡤࡔࡁࡎࡇࠥ⇱")) == bstack11ll11_opy_ (u"ࠥࡧࡴࡪࡥࡴࡪ࡬ࡴࠧ⇲"):
        return {
            bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⇳"): bstack11ll11_opy_ (u"ࠧࡉ࡯ࡥࡧࡶ࡬࡮ࡶࠢ⇴"),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⇵"): None,
            bstack11ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ⇶"): None,
            bstack11ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⇷"): None
        }
    if env.get(bstack11ll11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠧ⇸")) and env.get(bstack11ll11_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨ⇹")):
        return {
            bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⇺"): bstack11ll11_opy_ (u"ࠧࡈࡩࡵࡤࡸࡧࡰ࡫ࡴࠣ⇻"),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⇼"): env.get(bstack11ll11_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡋࡎ࡚࡟ࡉࡖࡗࡔࡤࡕࡒࡊࡉࡌࡒࠧ⇽")),
            bstack11ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⇾"): None,
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⇿"): env.get(bstack11ll11_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ∀"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠦࡈࡏࠢ∁")) == bstack11ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥ∂") and bstack1lll1lll1_opy_(env.get(bstack11ll11_opy_ (u"ࠨࡄࡓࡑࡑࡉࠧ∃"))):
        return {
            bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ∄"): bstack11ll11_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢ∅"),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ∆"): env.get(bstack11ll11_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨ∇")),
            bstack11ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ∈"): None,
            bstack11ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ∉"): env.get(bstack11ll11_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ∊"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠢࡄࡋࠥ∋")) == bstack11ll11_opy_ (u"ࠣࡶࡵࡹࡪࠨ∌") and bstack1lll1lll1_opy_(env.get(bstack11ll11_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧ∍"))):
        return {
            bstack11ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣ∎"): bstack11ll11_opy_ (u"ࠦࡘ࡫࡭ࡢࡲ࡫ࡳࡷ࡫ࠢ∏"),
            bstack11ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ∐"): env.get(bstack11ll11_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡒࡖࡌࡇࡎࡊ࡜ࡄࡘࡎࡕࡎࡠࡗࡕࡐࠧ∑")),
            bstack11ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ−"): env.get(bstack11ll11_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ∓")),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ∔"): env.get(bstack11ll11_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡍࡉࠨ∕"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠦࡈࡏࠢ∖")) == bstack11ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥ∗") and bstack1lll1lll1_opy_(env.get(bstack11ll11_opy_ (u"ࠨࡇࡊࡖࡏࡅࡇࡥࡃࡊࠤ∘"))):
        return {
            bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ∙"): bstack11ll11_opy_ (u"ࠣࡉ࡬ࡸࡑࡧࡢࠣ√"),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ∛"): env.get(bstack11ll11_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢ࡙ࡗࡒࠢ∜")),
            bstack11ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ∝"): env.get(bstack11ll11_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ∞")),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ∟"): env.get(bstack11ll11_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠥ∠"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠣࡅࡌࠦ∡")) == bstack11ll11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ∢") and bstack1lll1lll1_opy_(env.get(bstack11ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࠨ∣"))):
        return {
            bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ∤"): bstack11ll11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧ࡯࡮ࡺࡥࠣ∥"),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ∦"): env.get(bstack11ll11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ∧")),
            bstack11ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ∨"): env.get(bstack11ll11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡒࡁࡃࡇࡏࠦ∩")) or env.get(bstack11ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨ∪")),
            bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ∫"): env.get(bstack11ll11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ∬"))
        }
    if bstack1lll1lll1_opy_(env.get(bstack11ll11_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣ∭"))):
        return {
            bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ∮"): bstack11ll11_opy_ (u"ࠣࡘ࡬ࡷࡺࡧ࡬ࠡࡕࡷࡹࡩ࡯࡯ࠡࡖࡨࡥࡲࠦࡓࡦࡴࡹ࡭ࡨ࡫ࡳࠣ∯"),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ∰"): bstack11ll11_opy_ (u"ࠥࡿࢂࢁࡽࠣ∱").format(env.get(bstack11ll11_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧ∲")), env.get(bstack11ll11_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࡌࡈࠬ∳"))),
            bstack11ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ∴"): env.get(bstack11ll11_opy_ (u"ࠢࡔ࡛ࡖࡘࡊࡓ࡟ࡅࡇࡉࡍࡓࡏࡔࡊࡑࡑࡍࡉࠨ∵")),
            bstack11ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ∶"): env.get(bstack11ll11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤ∷"))
        }
    if bstack1lll1lll1_opy_(env.get(bstack11ll11_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࠧ∸"))):
        return {
            bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ∹"): bstack11ll11_opy_ (u"ࠧࡇࡰࡱࡸࡨࡽࡴࡸࠢ∺"),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ∻"): bstack11ll11_opy_ (u"ࠢࡼࡿ࠲ࡴࡷࡵࡪࡦࡥࡷ࠳ࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠨ∼").format(env.get(bstack11ll11_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢ࡙ࡗࡒࠧ∽")), env.get(bstack11ll11_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡆࡉࡃࡐࡗࡑࡘࡤࡔࡁࡎࡇࠪ∾")), env.get(bstack11ll11_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡓࡍࡗࡊࠫ∿")), env.get(bstack11ll11_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ≀"))),
            bstack11ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ≁"): env.get(bstack11ll11_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ≂")),
            bstack11ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ≃"): env.get(bstack11ll11_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ≄"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖࠥ≅")) and env.get(bstack11ll11_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧ≆")):
        return {
            bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ≇"): bstack11ll11_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢ≈"),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ≉"): bstack11ll11_opy_ (u"ࠢࡼࡿࡾࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡿࠥ≊").format(env.get(bstack11ll11_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫ≋")), env.get(bstack11ll11_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࠧ≌")), env.get(bstack11ll11_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪ≍"))),
            bstack11ll11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ≎"): env.get(bstack11ll11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧ≏")),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ≐"): env.get(bstack11ll11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢ≑"))
        }
    if any([env.get(bstack11ll11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ≒")), env.get(bstack11ll11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣ≓")), env.get(bstack11ll11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢ≔"))]):
        return {
            bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ≕"): bstack11ll11_opy_ (u"ࠧࡇࡗࡔࠢࡆࡳࡩ࡫ࡂࡶ࡫࡯ࡨࠧ≖"),
            bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ≗"): env.get(bstack11ll11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡔ࡚ࡈࡌࡊࡅࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ≘")),
            bstack11ll11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ≙"): env.get(bstack11ll11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ≚")),
            bstack11ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ≛"): env.get(bstack11ll11_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ≜"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥ≝")):
        return {
            bstack11ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ≞"): bstack11ll11_opy_ (u"ࠢࡃࡣࡰࡦࡴࡵࠢ≟"),
            bstack11ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ≠"): env.get(bstack11ll11_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡓࡧࡶࡹࡱࡺࡳࡖࡴ࡯ࠦ≡")),
            bstack11ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ≢"): env.get(bstack11ll11_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡸ࡮࡯ࡳࡶࡍࡳࡧࡔࡡ࡮ࡧࠥ≣")),
            bstack11ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ≤"): env.get(bstack11ll11_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦ≥"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࠣ≦")) or env.get(bstack11ll11_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥ≧")):
        return {
            bstack11ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ≨"): bstack11ll11_opy_ (u"࡛ࠥࡪࡸࡣ࡬ࡧࡵࠦ≩"),
            bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ≪"): env.get(bstack11ll11_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ≫")),
            bstack11ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ≬"): bstack11ll11_opy_ (u"ࠢࡎࡣ࡬ࡲࠥࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠢ≭") if env.get(bstack11ll11_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥ≮")) else None,
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ≯"): env.get(bstack11ll11_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡌࡏࡔࡠࡅࡒࡑࡒࡏࡔࠣ≰"))
        }
    if any([env.get(bstack11ll11_opy_ (u"ࠦࡌࡉࡐࡠࡒࡕࡓࡏࡋࡃࡕࠤ≱")), env.get(bstack11ll11_opy_ (u"ࠧࡍࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ≲")), env.get(bstack11ll11_opy_ (u"ࠨࡇࡐࡑࡊࡐࡊࡥࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ≳"))]):
        return {
            bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ≴"): bstack11ll11_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡅ࡯ࡳࡺࡪࠢ≵"),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ≶"): None,
            bstack11ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ≷"): env.get(bstack11ll11_opy_ (u"ࠦࡕࡘࡏࡋࡇࡆࡘࡤࡏࡄࠣ≸")),
            bstack11ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ≹"): env.get(bstack11ll11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ≺"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࠥ≻")):
        return {
            bstack11ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ≼"): bstack11ll11_opy_ (u"ࠤࡖ࡬࡮ࡶࡰࡢࡤ࡯ࡩࠧ≽"),
            bstack11ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ≾"): env.get(bstack11ll11_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ≿")),
            bstack11ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⊀"): bstack11ll11_opy_ (u"ࠨࡊࡰࡤࠣࠧࢀࢃࠢ⊁").format(env.get(bstack11ll11_opy_ (u"ࠧࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠪ⊂"))) if env.get(bstack11ll11_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠦ⊃")) else None,
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⊄"): env.get(bstack11ll11_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ⊅"))
        }
    if bstack1lll1lll1_opy_(env.get(bstack11ll11_opy_ (u"ࠦࡓࡋࡔࡍࡋࡉ࡝ࠧ⊆"))):
        return {
            bstack11ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⊇"): bstack11ll11_opy_ (u"ࠨࡎࡦࡶ࡯࡭࡫ࡿࠢ⊈"),
            bstack11ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⊉"): env.get(bstack11ll11_opy_ (u"ࠣࡆࡈࡔࡑࡕ࡙ࡠࡗࡕࡐࠧ⊊")),
            bstack11ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⊋"): env.get(bstack11ll11_opy_ (u"ࠥࡗࡎ࡚ࡅࡠࡐࡄࡑࡊࠨ⊌")),
            bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⊍"): env.get(bstack11ll11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ⊎"))
        }
    if bstack1lll1lll1_opy_(env.get(bstack11ll11_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡁࡄࡖࡌࡓࡓ࡙ࠢ⊏"))):
        return {
            bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⊐"): bstack11ll11_opy_ (u"ࠣࡉ࡬ࡸࡍࡻࡢࠡࡃࡦࡸ࡮ࡵ࡮ࡴࠤ⊑"),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⊒"): bstack11ll11_opy_ (u"ࠥࡿࢂ࠵ࡻࡾ࠱ࡤࡧࡹ࡯࡯࡯ࡵ࠲ࡶࡺࡴࡳ࠰ࡽࢀࠦ⊓").format(env.get(bstack11ll11_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡘࡋࡒࡗࡇࡕࡣ࡚ࡘࡌࠨ⊔")), env.get(bstack11ll11_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚ࠩ⊕")), env.get(bstack11ll11_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉ࠭⊖"))),
            bstack11ll11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ⊗"): env.get(bstack11ll11_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙ࠥ⊘")),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⊙"): env.get(bstack11ll11_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠥ⊚"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠦࡈࡏࠢ⊛")) == bstack11ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥ⊜") and env.get(bstack11ll11_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨ⊝")) == bstack11ll11_opy_ (u"ࠢ࠲ࠤ⊞"):
        return {
            bstack11ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ⊟"): bstack11ll11_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤ⊠"),
            bstack11ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⊡"): bstack11ll11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀࢃࠢ⊢").format(env.get(bstack11ll11_opy_ (u"ࠬ࡜ࡅࡓࡅࡈࡐࡤ࡛ࡒࡍࠩ⊣"))),
            bstack11ll11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⊤"): None,
            bstack11ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⊥"): None,
        }
    if env.get(bstack11ll11_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠦ⊦")):
        return {
            bstack11ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⊧"): bstack11ll11_opy_ (u"ࠥࡘࡪࡧ࡭ࡤ࡫ࡷࡽࠧ⊨"),
            bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⊩"): None,
            bstack11ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⊪"): env.get(bstack11ll11_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠢ⊫")),
            bstack11ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⊬"): env.get(bstack11ll11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ⊭"))
        }
    if any([env.get(bstack11ll11_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࠧ⊮")), env.get(bstack11ll11_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡓࡎࠥ⊯")), env.get(bstack11ll11_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤ⊰")), env.get(bstack11ll11_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡖࡈࡅࡒࠨ⊱"))]):
        return {
            bstack11ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⊲"): bstack11ll11_opy_ (u"ࠢࡄࡱࡱࡧࡴࡻࡲࡴࡧࠥ⊳"),
            bstack11ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⊴"): None,
            bstack11ll11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⊵"): env.get(bstack11ll11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ⊶")) or None,
            bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⊷"): env.get(bstack11ll11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ⊸"), 0)
        }
    if env.get(bstack11ll11_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ⊹")):
        return {
            bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⊺"): bstack11ll11_opy_ (u"ࠣࡉࡲࡇࡉࠨ⊻"),
            bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⊼"): None,
            bstack11ll11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⊽"): env.get(bstack11ll11_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ⊾")),
            bstack11ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⊿"): env.get(bstack11ll11_opy_ (u"ࠨࡇࡐࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡈࡕࡕࡏࡖࡈࡖࠧ⋀"))
        }
    if env.get(bstack11ll11_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ⋁")):
        return {
            bstack11ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ⋂"): bstack11ll11_opy_ (u"ࠤࡆࡳࡩ࡫ࡆࡳࡧࡶ࡬ࠧ⋃"),
            bstack11ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⋄"): env.get(bstack11ll11_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ⋅")),
            bstack11ll11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⋆"): env.get(bstack11ll11_opy_ (u"ࠨࡃࡇࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤ⋇")),
            bstack11ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⋈"): env.get(bstack11ll11_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ⋉"))
        }
    return {bstack11ll11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⋊"): None}
def get_host_info():
    return {
        bstack11ll11_opy_ (u"ࠥ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠧ⋋"): platform.node(),
        bstack11ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨ⋌"): platform.system(),
        bstack11ll11_opy_ (u"ࠧࡺࡹࡱࡧࠥ⋍"): platform.machine(),
        bstack11ll11_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢ⋎"): platform.version(),
        bstack11ll11_opy_ (u"ࠢࡢࡴࡦ࡬ࠧ⋏"): platform.architecture()[0]
    }
def bstack1l11ll1111_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1llll1l1l1ll_opy_():
    if global_config.get_property(bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ⋐")):
        return bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ⋑")
    return bstack11ll11_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠩ⋒")
def bstack1lll111l1ll_opy_(driver):
    info = {
        bstack11ll11_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ⋓"): driver.capabilities,
        bstack11ll11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩ⋔"): driver.session_id,
        bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ⋕"): driver.capabilities.get(bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ⋖"), None),
        bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ⋗"): driver.capabilities.get(bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ⋘"), None),
        bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬ⋙"): driver.capabilities.get(bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ⋚"), None),
        bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⋛"):driver.capabilities.get(bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⋜"), None),
    }
    if bstack1llll1l1l1ll_opy_() == bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭⋝"):
        if bstack11l11lll1_opy_():
            info[bstack11ll11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ⋞")] = bstack11ll11_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⋟")
        elif driver.capabilities.get(bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ⋠"), {}).get(bstack11ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⋡"), False):
            info[bstack11ll11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭⋢")] = bstack11ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ⋣")
        else:
            info[bstack11ll11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ⋤")] = bstack11ll11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⋥")
    return info
def bstack11l11lll1_opy_():
    if global_config.get_property(bstack11ll11_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ⋦")):
        return True
    if bstack1lll1lll1_opy_(os.environ.get(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ⋧"), None)):
        return True
    return False
def bstack1lllll1lllll_opy_(bstack1llll11l1lll_opy_, url, response, headers=None, data=None):
    bstack11ll11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡇࡻࡩ࡭ࡦࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠ࡭ࡱࡪࠤࡵࡧࡲࡢ࡯ࡨࡸࡪࡸࡳࠡࡨࡲࡶࠥࡸࡥࡲࡷࡨࡷࡹ࠵ࡲࡦࡵࡳࡳࡳࡹࡥࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡳࡸࡩࡸࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡈࡕࡖࡓࠤࡲ࡫ࡴࡩࡱࡧࠤ࠭ࡍࡅࡕ࠮ࠣࡔࡔ࡙ࡔ࠭ࠢࡨࡸࡨ࠴ࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࡸࡶࡱࡀࠠࡓࡧࡴࡹࡪࡹࡴࠡࡗࡕࡐ࠴࡫࡮ࡥࡲࡲ࡭ࡳࡺࠊࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡦࡳࡱࡰࠤࡷ࡫ࡱࡶࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࡩࡧࡤࡨࡪࡸࡳ࠻ࠢࡕࡩࡶࡻࡥࡴࡶࠣ࡬ࡪࡧࡤࡦࡴࡶࠤࡴࡸࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡤࡢࡶࡤ࠾ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡊࡔࡑࡑࠤࡩࡧࡴࡢࠢࡲࡶࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡉࡳࡷࡳࡡࡵࡶࡨࡨࠥࡲ࡯ࡨࠢࡰࡩࡸࡹࡡࡨࡧࠣࡻ࡮ࡺࡨࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡤࡲࡩࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡦࡤࡸࡦࠐࠠࠡࠢࠣࠦࠧࠨ⋨")
    bstack1llll1llll1l_opy_ = {
        bstack11ll11_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨ⋩"): headers,
        bstack11ll11_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨ⋪"): bstack1llll11l1lll_opy_.upper(),
        bstack11ll11_opy_ (u"ࠢࡢࡩࡨࡲࡹࠨ⋫"): None,
        bstack11ll11_opy_ (u"ࠣࡧࡱࡨࡵࡵࡩ࡯ࡶࠥ⋬"): url,
        bstack11ll11_opy_ (u"ࠤ࡭ࡷࡴࡴࠢ⋭"): data
    }
    try:
        bstack1llll1l1111l_opy_ = response.json()
        if isinstance(bstack1llll1l1111l_opy_, dict) and bstack1llll1l1111l_opy_.get(bstack11ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⋮"), {}).get(bstack11ll11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⋯"), {}).get(bstack11ll11_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭⋰")):
            bstack1llll1l1l1l1_opy_ = json.loads(json.dumps(bstack1llll1l1111l_opy_))
            bstack1llll1l1l1l1_opy_[bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⋱")][bstack11ll11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⋲")][bstack11ll11_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ⋳")] = bstack11ll11_opy_ (u"ࠤ࡞ࡶࡪࡪࡡࡤࡶࡨࡨࠥ࡬࡯ࡳࠢࡥࡶࡪࡼࡩࡵࡻࡠࠦ⋴")
            bstack1llll1l1111l_opy_ = bstack1llll1l1l1l1_opy_
    except Exception:
        bstack1llll1l1111l_opy_ = response.text
    bstack1lllll11llll_opy_ = {
        bstack11ll11_opy_ (u"ࠥࡦࡴࡪࡹࠣ⋵"): bstack1llll1l1111l_opy_,
        bstack11ll11_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࡇࡴࡪࡥࠣ⋶"): response.status_code
    }
    return {
        bstack11ll11_opy_ (u"ࠧࡸࡥࡲࡷࡨࡷࡹࠨ⋷"): bstack1llll1llll1l_opy_,
        bstack11ll11_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣ⋸"): bstack1lllll11llll_opy_
    }
def bstack1l11lll11l_opy_(bstack1llll11l1lll_opy_, url, data, config):
    headers = config.get(bstack11ll11_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ⋹"), None)
    proxies = bstack1111l1ll1_opy_(config, url)
    auth = config.get(bstack11ll11_opy_ (u"ࠨࡣࡸࡸ࡭࠭⋺"), None)
    response = requests.request(
            bstack1llll11l1lll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1lllll1lllll_opy_(bstack1llll11l1lll_opy_, url, response, headers, data)
        automation_logger.debug(json.dumps(log_message, separators=(bstack11ll11_opy_ (u"ࠩ࠯ࠫ⋻"), bstack11ll11_opy_ (u"ࠪ࠾ࠬ⋼"))))
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴ࠻ࠢࡾࢁࠧ⋽").format(e))
    return response
def bstack1llllll1ll1_opy_(bstack11l1l11ll_opy_, size):
    bstack111l11ll11_opy_ = []
    while len(bstack11l1l11ll_opy_) > size:
        bstack111l11l11l_opy_ = bstack11l1l11ll_opy_[:size]
        bstack111l11ll11_opy_.append(bstack111l11l11l_opy_)
        bstack11l1l11ll_opy_ = bstack11l1l11ll_opy_[size:]
    bstack111l11ll11_opy_.append(bstack11l1l11ll_opy_)
    return bstack111l11ll11_opy_
def bstack1llllll1ll1l_opy_(message, bstack1llllll111l1_opy_=False):
    os.write(1, bytes(message, bstack11ll11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ⋾")))
    os.write(1, bytes(bstack11ll11_opy_ (u"࠭࡜࡯ࠩ⋿"), bstack11ll11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭⌀")))
    if bstack1llllll111l1_opy_:
        with open(bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧ⌁") + os.environ[bstack11ll11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨ⌂")] + bstack11ll11_opy_ (u"ࠪ࠲ࡱࡵࡧࠨ⌃"), bstack11ll11_opy_ (u"ࠫࡦ࠭⌄")) as f:
            f.write(message + bstack11ll11_opy_ (u"ࠬࡢ࡮ࠨ⌅"))
def bstack1l1ll1ll1l_opy_():
    return os.environ[bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ⌆")].lower() == bstack11ll11_opy_ (u"ࠧࡵࡴࡸࡩࠬ⌇")
def bstack1l1l111l1l_opy_():
    return bstack1lll1ll1l11_opy_().replace(tzinfo=None).isoformat() + bstack11ll11_opy_ (u"ࠨ࡜ࠪ⌈")
def bstack1ll1l1llll1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11ll11_opy_ (u"ࠩ࡝ࠫ⌉"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11ll11_opy_ (u"ࠪ࡞ࠬ⌊")))).total_seconds() * 1000
def bstack1lllllll1l1l_opy_(timestamp):
    return bstack1llll1lllll1_opy_(timestamp).isoformat() + bstack11ll11_opy_ (u"ࠫ࡟࠭⌋")
def bstack1llll1l11111_opy_(bstack1llll11ll111_opy_):
    date_format = bstack11ll11_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪ⌌")
    bstack1lllll1l1ll1_opy_ = datetime.datetime.strptime(bstack1llll11ll111_opy_, date_format)
    return bstack1lllll1l1ll1_opy_.isoformat() + bstack11ll11_opy_ (u"࡚࠭ࠨ⌍")
def bstack1lllll1l1l1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⌎")
    else:
        return bstack11ll11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⌏")
def bstack1lll1lll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11ll11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⌐")
def bstack1llll111llll_opy_(val):
    return val.__str__().lower() == bstack11ll11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ⌑")
def error_handler(bstack1llll11l1ll1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1llll11l1ll1_opy_ as e:
                print(bstack11ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦ⌒").format(func.__name__, bstack1llll11l1ll1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1llllll11111_opy_(bstack1lllllll1l11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1lllllll1l11_opy_(cls, *args, **kwargs)
            except bstack1llll11l1ll1_opy_ as e:
                print(bstack11ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧ⌓").format(bstack1lllllll1l11_opy_.__name__, bstack1llll11l1ll1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1llllll11111_opy_
    else:
        return decorator
def bstack1llll1l1l_opy_(bstack1lllll11111_opy_):
    if os.getenv(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ⌔")) is not None:
        return bstack1lll1lll1_opy_(os.getenv(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ⌕")))
    if bstack11ll11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⌖") in bstack1lllll11111_opy_ and bstack1llll111llll_opy_(bstack1lllll11111_opy_[bstack11ll11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⌗")]):
        return False
    if bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⌘") in bstack1lllll11111_opy_ and bstack1llll111llll_opy_(bstack1lllll11111_opy_[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⌙")]):
        return False
    return True
def bstack1lll1l111_opy_():
    try:
        from pytest_bdd import reporting
        bstack1llll1111l11_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧ⌚"), None)
        return bstack1llll1111l11_opy_ is None or bstack1llll1111l11_opy_ == bstack11ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ⌛")
    except Exception as e:
        return False
def bstack111ll11l11_opy_(hub_url, CONFIG):
    if bstack1lll1l11l1_opy_() <= version.parse(bstack11ll11_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ⌜")):
        if hub_url:
            return bstack11ll11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ⌝") + hub_url + bstack11ll11_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ⌞")
        return bstack1ll1l1l1l_opy_
    if hub_url:
        return bstack11ll11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ⌟") + hub_url + bstack11ll11_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ⌠")
    return bstack11llll11l_opy_
def bstack1llll1lll111_opy_():
    return isinstance(os.getenv(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫ⌡")), str)
def bstack1l111l1l1l_opy_(url):
    return urlparse(url).hostname
def bstack111l1llll1_opy_(hostname):
    for bstack1l1l1l111l_opy_ in bstack1llllll11_opy_:
        regex = re.compile(bstack1l1l1l111l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1lllll1l11l1_opy_(bstack1llll11l11l1_opy_, file_name, logger):
    bstack11l111llll_opy_ = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"࠭ࡾࠨ⌢")), bstack1llll11l11l1_opy_)
    try:
        if not os.path.exists(bstack11l111llll_opy_):
            os.makedirs(bstack11l111llll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠧࡿࠩ⌣")), bstack1llll11l11l1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11ll11_opy_ (u"ࠨࡹࠪ⌤")):
                pass
            with open(file_path, bstack11ll11_opy_ (u"ࠤࡺ࠯ࠧ⌥")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l11l1lll_opy_.format(str(e)))
def bstack1llll1llll11_opy_(file_name, key, value, logger):
    file_path = bstack1lllll1l11l1_opy_(bstack11ll11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ⌦"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lll111l1l_opy_ = json.load(open(file_path, bstack11ll11_opy_ (u"ࠫࡷࡨࠧ⌧")))
        else:
            bstack1lll111l1l_opy_ = {}
        bstack1lll111l1l_opy_[key] = value
        with open(file_path, bstack11ll11_opy_ (u"ࠧࡽࠫࠣ⌨")) as outfile:
            json.dump(bstack1lll111l1l_opy_, outfile)
def bstack1l11ll11ll_opy_(file_name, logger):
    file_path = bstack1lllll1l11l1_opy_(bstack11ll11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭〈"), file_name, logger)
    bstack1lll111l1l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11ll11_opy_ (u"ࠧࡳࠩ〉")) as bstack111ll1l11l_opy_:
            bstack1lll111l1l_opy_ = json.load(bstack111ll1l11l_opy_)
    return bstack1lll111l1l_opy_
def bstack1ll1llll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ⌫") + file_path + bstack11ll11_opy_ (u"ࠩࠣࠫ⌬") + str(e))
def bstack1lll1l11l1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11ll11_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧ⌭")
def bstack1l111l111l_opy_(config):
    if bstack11ll11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ⌮") in config:
        del (config[bstack11ll11_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ⌯")])
        return False
    if bstack1lll1l11l1_opy_() < version.parse(bstack11ll11_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬ⌰")):
        return False
    if bstack1lll1l11l1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭⌱")):
        return True
    if bstack11ll11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ⌲") in config and config[bstack11ll11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ⌳")] is False:
        return False
    else:
        return True
def bstack1111lll11l_opy_(args_list, bstack1llllll1l111_opy_):
    index = -1
    for value in bstack1llllll1l111_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack1111l1llll1_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack1111l1llll1_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1llll11ll1l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1llll11ll1l_opy_ = bstack1llll11ll1l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⌴"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⌵"), exception=exception)
    def bstack1ll111ll11l_opy_(self):
        if self.result != bstack11ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⌶"):
            return None
        if isinstance(self.exception_type, str) and bstack11ll11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ⌷") in self.exception_type:
            return bstack11ll11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ⌸")
        return bstack11ll11_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ⌹")
    def bstack1llllll1l1ll_opy_(self):
        if self.result != bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⌺"):
            return None
        if self.bstack1llll11ll1l_opy_:
            return self.bstack1llll11ll1l_opy_
        return bstack1llllll11l1l_opy_(self.exception)
def bstack1llllll11l1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1lllll1llll1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11ll1l11l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack111l111111_opy_(config, logger):
    try:
        import playwright
        bstack1lllll11l11l_opy_ = playwright.__file__
        bstack1llll1ll1ll1_opy_ = os.path.split(bstack1lllll11l11l_opy_)
        bstack1llll1lll1l1_opy_ = bstack1llll1ll1ll1_opy_[0] + bstack11ll11_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭⌻")
        os.environ[bstack11ll11_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧ⌼")] = bstack1ll111lll1_opy_(config)
        with open(bstack1llll1lll1l1_opy_, bstack11ll11_opy_ (u"ࠬࡸࠧ⌽")) as f:
            file_content = f.read()
            bstack1llllll111ll_opy_ = bstack11ll11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ⌾")
            bstack1lllll111111_opy_ = file_content.find(bstack1llllll111ll_opy_)
            if bstack1lllll111111_opy_ == -1:
              process = subprocess.Popen(bstack11ll11_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦ⌿"), shell=True, cwd=bstack1llll1ll1ll1_opy_[0])
              process.wait()
              bstack1llllll11ll1_opy_ = bstack11ll11_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨ⍀")
              bstack1llll1l1l111_opy_ = bstack11ll11_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨ⍁")
              bstack1lllllll11l1_opy_ = file_content.replace(bstack1llllll11ll1_opy_, bstack1llll1l1l111_opy_)
              with open(bstack1llll1lll1l1_opy_, bstack11ll11_opy_ (u"ࠪࡻࠬ⍂")) as f:
                f.write(bstack1lllllll11l1_opy_)
    except Exception as e:
        logger.error(bstack111ll11ll_opy_.format(str(e)))
def bstack1l11l11111_opy_():
  try:
    bstack1llll1ll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫ⍃"))
    bstack1llllll1l1l1_opy_ = []
    if os.path.exists(bstack1llll1ll11l1_opy_):
      with open(bstack1llll1ll11l1_opy_) as f:
        bstack1llllll1l1l1_opy_ = json.load(f)
      os.remove(bstack1llll1ll11l1_opy_)
    return bstack1llllll1l1l1_opy_
  except:
    pass
  return []
def bstack11ll111l_opy_(bstack1ll11l1lll_opy_):
  try:
    bstack1llllll1l1l1_opy_ = []
    bstack1llll1ll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬ⍄"))
    if os.path.exists(bstack1llll1ll11l1_opy_):
      with open(bstack1llll1ll11l1_opy_) as f:
        bstack1llllll1l1l1_opy_ = json.load(f)
    bstack1llllll1l1l1_opy_.append(bstack1ll11l1lll_opy_)
    with open(bstack1llll1ll11l1_opy_, bstack11ll11_opy_ (u"࠭ࡷࠨ⍅")) as f:
        json.dump(bstack1llllll1l1l1_opy_, f)
  except:
    pass
def bstack1111ll1l11_opy_(logger, bstack1llll11llll1_opy_ = False):
  try:
    test_name = os.environ.get(bstack11ll11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⍆"), bstack11ll11_opy_ (u"ࠨࠩ⍇"))
    if test_name == bstack11ll11_opy_ (u"ࠩࠪ⍈"):
        test_name = threading.current_thread().__dict__.get(bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩ⍉"), bstack11ll11_opy_ (u"ࠫࠬ⍊"))
    bstack1lllll1l1l11_opy_ = bstack11ll11_opy_ (u"ࠬ࠲ࠠࠨ⍋").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1llll11llll1_opy_:
        bstack1l11l11ll_opy_ = os.environ.get(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⍌"), bstack11ll11_opy_ (u"ࠧ࠱ࠩ⍍"))
        bstack1ll1l11111_opy_ = {bstack11ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭⍎"): test_name, bstack11ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ⍏"): bstack1lllll1l1l11_opy_, bstack11ll11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ⍐"): bstack1l11l11ll_opy_}
        bstack1lllll1lll11_opy_ = []
        bstack1llll1l1llll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ⍑"))
        if os.path.exists(bstack1llll1l1llll_opy_):
            with open(bstack1llll1l1llll_opy_) as f:
                bstack1lllll1lll11_opy_ = json.load(f)
        bstack1lllll1lll11_opy_.append(bstack1ll1l11111_opy_)
        with open(bstack1llll1l1llll_opy_, bstack11ll11_opy_ (u"ࠬࡽࠧ⍒")) as f:
            json.dump(bstack1lllll1lll11_opy_, f)
    else:
        bstack1ll1l11111_opy_ = {bstack11ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⍓"): test_name, bstack11ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⍔"): bstack1lllll1l1l11_opy_, bstack11ll11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ⍕"): str(multiprocessing.current_process().name)}
        if bstack11ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭⍖") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll1l11111_opy_)
  except Exception as e:
      logger.warn(bstack11ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ⍗").format(e))
def bstack111l1111ll_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11ll11_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧ⍘"))
    try:
      bstack1llll1ll1l11_opy_ = []
      bstack1ll1l11111_opy_ = {bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⍙"): test_name, bstack11ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⍚"): error_message, bstack11ll11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⍛"): index}
      bstack1lllll1ll111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ⍜"))
      if os.path.exists(bstack1lllll1ll111_opy_):
          with open(bstack1lllll1ll111_opy_) as f:
              bstack1llll1ll1l11_opy_ = json.load(f)
      bstack1llll1ll1l11_opy_.append(bstack1ll1l11111_opy_)
      with open(bstack1lllll1ll111_opy_, bstack11ll11_opy_ (u"ࠩࡺࠫ⍝")) as f:
          json.dump(bstack1llll1ll1l11_opy_, f)
    except Exception as e:
      logger.warn(bstack11ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ⍞").format(e))
    return
  bstack1llll1ll1l11_opy_ = []
  bstack1ll1l11111_opy_ = {bstack11ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⍟"): test_name, bstack11ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⍠"): error_message, bstack11ll11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⍡"): index}
  bstack1lllll1ll111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ⍢"))
  lock_file = bstack1lllll1ll111_opy_ + bstack11ll11_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧ⍣")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1lllll1ll111_opy_):
          with open(bstack1lllll1ll111_opy_, bstack11ll11_opy_ (u"ࠩࡵࠫ⍤")) as f:
              content = f.read().strip()
              if content:
                  bstack1llll1ll1l11_opy_ = json.load(open(bstack1lllll1ll111_opy_))
      bstack1llll1ll1l11_opy_.append(bstack1ll1l11111_opy_)
      with open(bstack1lllll1ll111_opy_, bstack11ll11_opy_ (u"ࠪࡻࠬ⍥")) as f:
          json.dump(bstack1llll1ll1l11_opy_, f)
  except Exception as e:
    logger.warn(bstack11ll11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡨ࡬ࡰࡪࠦ࡬ࡰࡥ࡮࡭ࡳ࡭࠺ࠡࡽࢀࠦ⍦").format(e))
def bstack111ll111l_opy_(bstack1l111ll111_opy_, name, logger):
  try:
    bstack1ll1l11111_opy_ = {bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⍧"): name, bstack11ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⍨"): bstack1l111ll111_opy_, bstack11ll11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⍩"): str(threading.current_thread()._name)}
    return bstack1ll1l11111_opy_
  except Exception as e:
    logger.warn(bstack11ll11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ⍪").format(e))
  return
def bstack1llll1lll11l_opy_():
    return platform.system() == bstack11ll11_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪ⍫")
def bstack1l1lllllll_opy_(bstack1llll11ll1ll_opy_, config, logger):
    bstack1llll11l11ll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1llll11ll1ll_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ⍬").format(e))
    return bstack1llll11l11ll_opy_
def bstack1llll111l1l1_opy_(bstack1llll11lllll_opy_, bstack1lllll111l1l_opy_):
    bstack1llllll1111l_opy_ = version.parse(bstack1llll11lllll_opy_)
    bstack1llll1l11ll1_opy_ = version.parse(bstack1lllll111l1l_opy_)
    if bstack1llllll1111l_opy_ > bstack1llll1l11ll1_opy_:
        return 1
    elif bstack1llllll1111l_opy_ < bstack1llll1l11ll1_opy_:
        return -1
    else:
        return 0
def bstack1lll1ll1l11_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1llll1lllll1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1llll111ll1l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1lllll1l1l_opy_(options, framework, config, bstack1l1lll1lll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11ll11_opy_ (u"ࠫ࡬࡫ࡴࠨ⍭"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11lll11111_opy_ = caps.get(bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭⍮"))
    bstack1llll1l1l11l_opy_ = True
    bstack11l1l11l11_opy_ = os.environ[bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⍯")]
    bstack1l1111l1l11_opy_ = config.get(bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⍰"), False)
    if bstack1l1111l1l11_opy_:
        bstack1l1l1llll1l_opy_ = config.get(bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⍱"), {})
        bstack1l1l1llll1l_opy_[bstack11ll11_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬ⍲")] = os.getenv(bstack11ll11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⍳"))
        bstack11ll1l111_opy_ = json.loads(os.getenv(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ⍴"), bstack11ll11_opy_ (u"ࠬࢁࡽࠨ⍵"))).get(bstack11ll11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ⍶"))
    if bstack1llll111llll_opy_(caps.get(bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭⍷"))) or bstack1llll111llll_opy_(caps.get(bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨ⍸"))):
        bstack1llll1l1l11l_opy_ = False
    if bstack1l111l111l_opy_({bstack11ll11_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤ⍹"): bstack1llll1l1l11l_opy_}):
        bstack11lll11111_opy_ = bstack11lll11111_opy_ or {}
        bstack11lll11111_opy_[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⍺")] = bstack1llll111ll1l_opy_(framework)
        bstack11lll11111_opy_[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⍻")] = bstack1l1ll1ll1l_opy_()
        bstack11lll11111_opy_[bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ⍼")] = bstack11l1l11l11_opy_
        bstack11lll11111_opy_[bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ⍽")] = bstack1l1lll1lll_opy_
        if bstack1l1111l1l11_opy_:
            bstack11lll11111_opy_[bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⍾")] = bstack1l1111l1l11_opy_
            bstack11lll11111_opy_[bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⍿")] = bstack1l1l1llll1l_opy_
            bstack11lll11111_opy_[bstack11ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⎀")][bstack11ll11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ⎁")] = bstack11ll1l111_opy_
        if getattr(options, bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ⎂"), None):
            options.set_capability(bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭⎃"), bstack11lll11111_opy_)
        else:
            options[bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⎄")] = bstack11lll11111_opy_
    else:
        if getattr(options, bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⎅"), None):
            options.set_capability(bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⎆"), bstack1llll111ll1l_opy_(framework))
            options.set_capability(bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⎇"), bstack1l1ll1ll1l_opy_())
            options.set_capability(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ⎈"), bstack11l1l11l11_opy_)
            options.set_capability(bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ⎉"), bstack1l1lll1lll_opy_)
            if bstack1l1111l1l11_opy_:
                options.set_capability(bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⎊"), bstack1l1111l1l11_opy_)
                options.set_capability(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ⎋"), bstack1l1l1llll1l_opy_)
                options.set_capability(bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ⎌"), bstack11ll1l111_opy_)
        else:
            options[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⎍")] = bstack1llll111ll1l_opy_(framework)
            options[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⎎")] = bstack1l1ll1ll1l_opy_()
            options[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ⎏")] = bstack11l1l11l11_opy_
            options[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ⎐")] = bstack1l1lll1lll_opy_
            if bstack1l1111l1l11_opy_:
                options[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⎑")] = bstack1l1111l1l11_opy_
                options[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ⎒")] = bstack1l1l1llll1l_opy_
                options[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭⎓")][bstack11ll11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ⎔")] = bstack11ll1l111_opy_
    return options
def bstack1lllll11ll1l_opy_(ws_endpoint, framework):
    bstack1l1lll1lll_opy_ = global_config.get_property(bstack11ll11_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦ⎕"))
    if ws_endpoint and len(ws_endpoint.split(bstack11ll11_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ⎖"))) > 1:
        ws_url = ws_endpoint.split(bstack11ll11_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ⎗"))[0]
        if bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ⎘") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1llll111ll11_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack11ll11_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ⎙"))[1]))
            bstack1llll111ll11_opy_ = bstack1llll111ll11_opy_ or {}
            bstack11l1l11l11_opy_ = os.environ[bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⎚")]
            bstack1llll111ll11_opy_[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⎛")] = str(framework) + str(__version__)
            bstack1llll111ll11_opy_[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⎜")] = bstack1l1ll1ll1l_opy_()
            bstack1llll111ll11_opy_[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ⎝")] = bstack11l1l11l11_opy_
            bstack1llll111ll11_opy_[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ⎞")] = bstack1l1lll1lll_opy_
            ws_endpoint = ws_endpoint.split(bstack11ll11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ⎟"))[0] + bstack11ll11_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ⎠") + urllib.parse.quote(json.dumps(bstack1llll111ll11_opy_))
    return ws_endpoint
def bstack1lll1lllll_opy_():
    global bstack1ll11111l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll11111l_opy_ = BrowserType.connect
    return bstack1ll11111l_opy_
def bstack1lllll1l1111_opy_(framework_name):
    global FRAMEWORK_NAME
    FRAMEWORK_NAME = framework_name
    return framework_name
def bstack1l11l11lll1_opy_(self, *args, **kwargs):
    global bstack1ll11111l_opy_
    try:
        global FRAMEWORK_NAME
        if bstack11ll11_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫ⎡") in kwargs:
            kwargs[bstack11ll11_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ⎢")] = bstack1lllll11ll1l_opy_(
                kwargs.get(bstack11ll11_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭⎣"), None),
                FRAMEWORK_NAME
            )
    except Exception as e:
        logger.error(bstack11ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥ⎤").format(str(e)))
    return bstack1ll11111l_opy_(self, *args, **kwargs)
def bstack1lllll11l1l1_opy_(bstack1lllllll111l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1111l1ll1_opy_(bstack1lllllll111l_opy_, bstack11ll11_opy_ (u"ࠦࠧ⎥"))
        if proxies and proxies.get(bstack11ll11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦ⎦")):
            parsed_url = urlparse(proxies.get(bstack11ll11_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧ⎧")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11ll11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ⎨")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11ll11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫ⎩")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11ll11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬ⎪")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11ll11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭⎫")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11ll11ll1_opy_(bstack1lllllll111l_opy_):
    bstack1llll1l1lll1_opy_ = {
        bstack11111l11ll1_opy_[bstack1llll1ll1l1l_opy_]: bstack1lllllll111l_opy_[bstack1llll1ll1l1l_opy_]
        for bstack1llll1ll1l1l_opy_ in bstack1lllllll111l_opy_
        if bstack1llll1ll1l1l_opy_ in bstack11111l11ll1_opy_
    }
    bstack1llll1l1lll1_opy_[bstack11ll11_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦ⎬")] = bstack1lllll11l1l1_opy_(bstack1lllllll111l_opy_, global_config.get_property(bstack11ll11_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧ⎭")))
    bstack1llllllll111_opy_ = [element.lower() for element in bstack11111l11lll_opy_]
    bstack1lllllll1ll1_opy_(bstack1llll1l1lll1_opy_, bstack1llllllll111_opy_)
    return bstack1llll1l1lll1_opy_
def bstack1lllllll1ll1_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11ll11_opy_ (u"ࠨࠪࠫࠬ࠭ࠦ⎮")
    for value in d.values():
        if isinstance(value, dict):
            bstack1lllllll1ll1_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1lllllll1ll1_opy_(item, keys)
def bstack11ll1ll11ll_opy_():
    bstack1llll111l1ll_opy_ = [os.environ.get(bstack11ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡊࡎࡈࡗࡤࡊࡉࡓࠤ⎯")), os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠣࢀࠥ⎰")), bstack11ll11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ⎱")), os.path.join(bstack11ll11_opy_ (u"ࠪ࠳ࡹࡳࡰࠨ⎲"), bstack11ll11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ⎳"))]
    for path in bstack1llll111l1ll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11ll11_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧ⎴") + str(path) + bstack11ll11_opy_ (u"ࠨࠧࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤ⎵"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11ll11_opy_ (u"ࠢࡈ࡫ࡹ࡭ࡳ࡭ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠥ࡬࡯ࡳࠢࠪࠦ⎶") + str(path) + bstack11ll11_opy_ (u"ࠣࠩࠥ⎷"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11ll11_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤ⎸") + str(path) + bstack11ll11_opy_ (u"ࠥࠫࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡨࡢࡵࠣࡸ࡭࡫ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹ࠮ࠣ⎹"))
            else:
                logger.debug(bstack11ll11_opy_ (u"ࠦࡈࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࠬࠨ⎺") + str(path) + bstack11ll11_opy_ (u"ࠧ࠭ࠠࡸ࡫ࡷ࡬ࠥࡽࡲࡪࡶࡨࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮࠯ࠤ⎻"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11ll11_opy_ (u"ࠨࡏࡱࡧࡵࡥࡹ࡯࡯࡯ࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨࠥ࡬࡯ࡳࠢࠪࠦ⎼") + str(path) + bstack11ll11_opy_ (u"ࠢࠨ࠰ࠥ⎽"))
            return path
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡷࡳࠤ࡫࡯࡬ࡦࠢࠪࡿࡵࡧࡴࡩࡿࠪ࠾ࠥࠨ⎾") + str(e) + bstack11ll11_opy_ (u"ࠤࠥ⎿"))
    logger.debug(bstack11ll11_opy_ (u"ࠥࡅࡱࡲࠠࡱࡣࡷ࡬ࡸࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠢ⏀"))
    return None
@measure(event_name=EVENTS.bstack11111l11l11_opy_, stage=STAGE.bstack1111l1111l_opy_)
def bstack1ll1l11l1ll_opy_(binary_path, bstack1ll1l111lll_opy_, bs_config):
    logger.debug(bstack11ll11_opy_ (u"ࠦࡈࡻࡲࡳࡧࡱࡸࠥࡉࡌࡊࠢࡓࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࡀࠠࡼࡿࠥ⏁").format(binary_path))
    bstack1llll11l1l11_opy_ = bstack11ll11_opy_ (u"ࠬ࠭⏂")
    bstack1llll1l111l1_opy_ = {
        bstack11ll11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⏃"): __version__,
        bstack11ll11_opy_ (u"ࠢࡰࡵࠥ⏄"): platform.system(),
        bstack11ll11_opy_ (u"ࠣࡱࡶࡣࡦࡸࡣࡩࠤ⏅"): platform.machine(),
        bstack11ll11_opy_ (u"ࠤࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ⏆"): bstack11ll11_opy_ (u"ࠪ࠴ࠬ⏇"),
        bstack11ll11_opy_ (u"ࠦࡸࡪ࡫ࡠ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠥ⏈"): bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ⏉")
    }
    bstack1llll11lll11_opy_(bstack1llll1l111l1_opy_)
    try:
        if binary_path:
            if bstack1llll1lll11l_opy_():
                bstack1llll1l111l1_opy_[bstack11ll11_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⏊")] = subprocess.check_output([binary_path, bstack11ll11_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣ⏋")]).strip().decode(bstack11ll11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ⏌"))
            else:
                bstack1llll1l111l1_opy_[bstack11ll11_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⏍")] = subprocess.check_output([binary_path, bstack11ll11_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦ⏎")], stderr=subprocess.DEVNULL).strip().decode(bstack11ll11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ⏏"))
        response = requests.request(
            bstack11ll11_opy_ (u"ࠬࡍࡅࡕࠩ⏐"),
            url=bstack1111l11l1_opy_(bstack111111lllll_opy_),
            headers=None,
            auth=(bs_config[bstack11ll11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ⏑")], bs_config[bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ⏒")]),
            json=None,
            params=bstack1llll1l111l1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11ll11_opy_ (u"ࠨࡷࡵࡰࠬ⏓") in data.keys() and bstack11ll11_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦࡢࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⏔") in data.keys():
            logger.debug(bstack11ll11_opy_ (u"ࠥࡒࡪ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡧ࡯࡮ࡢࡴࡼ࠰ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠦ⏕").format(bstack1llll1l111l1_opy_[bstack11ll11_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⏖")]))
            if bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠨ⏗") in os.environ:
                logger.debug(bstack11ll11_opy_ (u"ࠨࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡤ࡬ࡲࡦࡸࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡥࡸࠦࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠢ࡬ࡷࠥࡹࡥࡵࠤ⏘"))
                data[bstack11ll11_opy_ (u"ࠧࡶࡴ࡯ࠫ⏙")] = os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠫ⏚")]
            bstack1lllll1ll1l1_opy_ = bstack1llllll1l11l_opy_(data[bstack11ll11_opy_ (u"ࠩࡸࡶࡱ࠭⏛")], bstack1ll1l111lll_opy_)
            bstack1llll11l1l11_opy_ = os.path.join(bstack1ll1l111lll_opy_, bstack1lllll1ll1l1_opy_)
            os.chmod(bstack1llll11l1l11_opy_, 0o777) # bstack1lllll1l11ll_opy_ permission
            return bstack1llll11l1l11_opy_
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦ࡮ࡦࡹࠣࡗࡉࡑࠠࡼࡿࠥ⏜").format(e))
    return binary_path
def bstack1llll11lll11_opy_(bstack1llll1l111l1_opy_):
    try:
        if bstack11ll11_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪ⏝") not in bstack1llll1l111l1_opy_[bstack11ll11_opy_ (u"ࠬࡵࡳࠨ⏞")].lower():
            return
        if os.path.exists(bstack11ll11_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡴࡹ࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣ⏟")):
            with open(bstack11ll11_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡵࡳ࠮ࡴࡨࡰࡪࡧࡳࡦࠤ⏠"), bstack11ll11_opy_ (u"ࠣࡴࠥ⏡")) as f:
                bstack1llll1111lll_opy_ = {}
                for line in f:
                    if bstack11ll11_opy_ (u"ࠤࡀࠦ⏢") in line:
                        key, value = line.rstrip().split(bstack11ll11_opy_ (u"ࠥࡁࠧ⏣"), 1)
                        bstack1llll1111lll_opy_[key] = value.strip(bstack11ll11_opy_ (u"ࠫࠧࡢࠧࠨ⏤"))
                bstack1llll1l111l1_opy_[bstack11ll11_opy_ (u"ࠬࡪࡩࡴࡶࡵࡳࠬ⏥")] = bstack1llll1111lll_opy_.get(bstack11ll11_opy_ (u"ࠨࡉࡅࠤ⏦"), bstack11ll11_opy_ (u"ࠢࠣ⏧"))
        elif os.path.exists(bstack11ll11_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵ࡡ࡭ࡲ࡬ࡲࡪ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢ⏨")):
            bstack1llll1l111l1_opy_[bstack11ll11_opy_ (u"ࠩࡧ࡭ࡸࡺࡲࡰࠩ⏩")] = bstack11ll11_opy_ (u"ࠪࡥࡱࡶࡩ࡯ࡧࠪ⏪")
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡩ࡯ࡳࡵࡴࡲࠤࡴ࡬ࠠ࡭࡫ࡱࡹࡽࠨ⏫") + e)
@measure(event_name=EVENTS.bstack11111ll11ll_opy_, stage=STAGE.bstack1111l1111l_opy_)
def bstack1llllll1l11l_opy_(bstack1lllll1ll11l_opy_, bstack1lllllll1111_opy_):
    logger.debug(bstack11ll11_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱ࠿ࠦࠢ⏬") + str(bstack1lllll1ll11l_opy_) + bstack11ll11_opy_ (u"ࠨࠢ⏭"))
    zip_path = os.path.join(bstack1lllllll1111_opy_, bstack11ll11_opy_ (u"ࠢࡥࡱࡺࡲࡱࡵࡡࡥࡧࡧࡣ࡫࡯࡬ࡦ࠰ࡽ࡭ࡵࠨ⏮"))
    bstack1lllll1ll1l1_opy_ = bstack11ll11_opy_ (u"ࠨࠩ⏯")
    with requests.get(bstack1lllll1ll11l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11ll11_opy_ (u"ࠤࡺࡦࠧ⏰")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11ll11_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼ࠲ࠧ⏱"))
    with zipfile.ZipFile(zip_path, bstack11ll11_opy_ (u"ࠫࡷ࠭⏲")) as zip_ref:
        bstack1llll1ll1lll_opy_ = zip_ref.namelist()
        if len(bstack1llll1ll1lll_opy_) > 0:
            bstack1lllll1ll1l1_opy_ = bstack1llll1ll1lll_opy_[0] # bstack1llllll1llll_opy_ bstack111111l111l_opy_ will be bstack1lllll1ll1ll_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack1lllllll1111_opy_)
        logger.debug(bstack11ll11_opy_ (u"ࠧࡌࡩ࡭ࡧࡶࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡩࡽࡺࡲࡢࡥࡷࡩࡩࠦࡴࡰࠢࠪࠦ⏳") + str(bstack1lllllll1111_opy_) + bstack11ll11_opy_ (u"ࠨࠧࠣ⏴"))
    os.remove(zip_path)
    return bstack1lllll1ll1l1_opy_
def get_cli_dir():
    bstack1lllll111l11_opy_ = bstack11ll1ll11ll_opy_()
    if bstack1lllll111l11_opy_:
        bstack1ll1l111lll_opy_ = os.path.join(bstack1lllll111l11_opy_, bstack11ll11_opy_ (u"ࠢࡤ࡮࡬ࠦ⏵"))
        if not os.path.exists(bstack1ll1l111lll_opy_):
            os.makedirs(bstack1ll1l111lll_opy_, mode=0o777, exist_ok=True)
        return bstack1ll1l111lll_opy_
    else:
        raise FileNotFoundError(bstack11ll11_opy_ (u"ࠣࡐࡲࠤࡼࡸࡩࡵࡣࡥࡰࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻ࠱ࠦ⏶"))
def bstack1ll1l1l111l_opy_(bstack1ll1l111lll_opy_):
    bstack11ll11_opy_ (u"ࠤࠥࠦࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡰࠣࡥࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠱ࠦࠧࠨ⏷")
    bstack1llll11lll1l_opy_ = [
        os.path.join(bstack1ll1l111lll_opy_, f)
        for f in os.listdir(bstack1ll1l111lll_opy_)
        if os.path.isfile(os.path.join(bstack1ll1l111lll_opy_, f)) and f.startswith(bstack11ll11_opy_ (u"ࠥࡦ࡮ࡴࡡࡳࡻ࠰ࠦ⏸"))
    ]
    if len(bstack1llll11lll1l_opy_) > 0:
        return max(bstack1llll11lll1l_opy_, key=os.path.getmtime) # get bstack1lllll11ll11_opy_ binary
    return bstack11ll11_opy_ (u"ࠦࠧ⏹")
def bstack1111lll1lll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l111ll11l1_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l111ll11l1_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11lll1lll_opy_(data, keys, default=None):
    bstack11ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡙ࠥࡡࡧࡧ࡯ࡽࠥ࡭ࡥࡵࠢࡤࠤࡳ࡫ࡳࡵࡧࡧࠤࡻࡧ࡬ࡶࡧࠣࡪࡷࡵ࡭ࠡࡣࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡰࡴࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡤࡢࡶࡤ࠾࡚ࠥࡨࡦࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦ࡯ࡳࠢ࡯࡭ࡸࡺࠠࡵࡱࠣࡸࡷࡧࡶࡦࡴࡶࡩ࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣ࡯ࡪࡿࡳ࠻ࠢࡄࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡱࡥࡺࡵ࠲࡭ࡳࡪࡩࡤࡧࡶࠤࡷ࡫ࡰࡳࡧࡶࡩࡳࡺࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡨࡪ࡬ࡡࡶ࡮ࡷ࠾ࠥ࡜ࡡ࡭ࡷࡨࠤࡹࡵࠠࡳࡧࡷࡹࡷࡴࠠࡪࡨࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤ࠿ࡸࡥࡵࡷࡵࡲ࠿ࠦࡔࡩࡧࠣࡺࡦࡲࡵࡦࠢࡤࡸࠥࡺࡨࡦࠢࡱࡩࡸࡺࡥࡥࠢࡳࡥࡹ࡮ࠬࠡࡱࡵࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥ࡯ࡦࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ⏺")
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
def bstack1l1l111l11_opy_(bstack1lllllll11ll_opy_, key, value):
    bstack11ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡓࡵࡱࡵࡩࠥࡉࡌࡊࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠣࡱࡦࡶࡰࡪࡰࡪࠤ࡮ࡴࠠࡵࡪࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥ࡯࡭ࡤ࡫࡮ࡷࡡࡹࡥࡷࡹ࡟࡮ࡣࡳ࠾ࠥࡊࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠤࡲࡧࡰࡱ࡫ࡱ࡫ࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠ࡬ࡧࡼ࠾ࠥࡑࡥࡺࠢࡩࡶࡴࡳࠠࡄࡎࡌࡣࡈࡇࡐࡔࡡࡗࡓࡤࡉࡏࡏࡈࡌࡋࠏࠦࠠࠡࠢࠣࠤࠥࠦࡶࡢ࡮ࡸࡩ࠿ࠦࡖࡢ࡮ࡸࡩࠥ࡬ࡲࡰ࡯ࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡱ࡯࡮ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠏࠦࠠࠡࠢࠥࠦࠧ⏻")
    if key in bstack1l11111l1_opy_:
        bstack1ll11l1l_opy_ = bstack1l11111l1_opy_[key]
        if isinstance(bstack1ll11l1l_opy_, list):
            for env_name in bstack1ll11l1l_opy_:
                bstack1lllllll11ll_opy_[env_name] = value
        else:
            bstack1lllllll11ll_opy_[bstack1ll11l1l_opy_] = value